# Benchmark Results — REST-backed MCP vs GraphQL-backed MCP

## Key Findings

- **T1 (5 PRs + changed files) — REST vs GraphQL:** A1 uses **3 inference calls** vs B2's **2** (1.5× more). REST requires one get_pull_request + one get_pull_request_files call per PR; B2 fetches all five in one aliased GraphQL query. Cost: A1 $0.059 vs B2 $0.009 per run (**6.4× cheaper with B2**).
- **REST context overhead:** A1's tool schema and accumulated REST tool responses write **36K cache-creation tokens** ($0.045/run, 76% of total T1 cost). Each of A1's 3 inference calls extends the cached context with a full REST API payload; B2 writes only 0K tokens across its 2 calls.
- **T1 GraphQL comparison (B vs B2):** B2 (Rover Schema MCP, 3 tools) uses 2 vs B's 2 inference calls on T1, costing $0.009 vs $0.009/run. Rover's smaller tool schema and targeted keyword search keep schema-discovery overhead low.
- **T2 (single PR lookup):** B and B2 are indistinguishable ($0.005 vs $0.005/run, 2.0 vs 2.0 calls) — as expected for a control task both conditions answer in one execute. No claim is made about a difference this small.
- **Overall (all tasks):** B and B2 are close in combined cost ($0.014 vs $0.014/run); both are substantially cheaper than A1 ($0.066/run).

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (A1 / A2 / B / B2)


### Task T1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 3.0 ± 0.0 | 10.0 ± 0.0 | 17.0 ± 0.0 | 1,692 ± 56 | 58,343 ± 1 | 35,889 ± 1 | 27,039 ± 0 |
| **A2** — REST (minimal toolset) | 3.0 ± 0.0 | 10.0 ± 0.0 | 17.0 ± 0.0 | 1,766 ± 3 | 29,344 ± 2 | 35,811 ± 7 | 27,039 ± 0 |
| **B** — GraphQL (Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,538 ± 1 | 883 ± 19 | 0.0 ± 0.0 | 0.0 ± 0.0 | 443 ± 0 |
| **B2** — GraphQL (Rover Schema MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,682 ± 102 | 916 ± 67 | 0.0 ± 0.0 | 0.0 ± 0.0 | 464 ± 40 |

### Task T2

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 2.0 ± 0.0 | 1.0 ± 0.0 | 8.0 ± 0.0 | 199 ± 0 | 36,348 ± 1 | 1,824 ± 1 | 357 ± 0 |
| **A2** — REST (minimal toolset) | 2.0 ± 0.0 | 1.0 ± 0.0 | 8.0 ± 0.0 | 195 ± 8 | 17,043 ± 1 | 1,743 ± 1 | 357 ± 0 |
| **B** — GraphQL (Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 3,742 ± 0 | 204 ± 1 | 0.0 ± 0.0 | 0.0 ± 0.0 | 70.0 ± 0.0 |
| **B2** — GraphQL (Rover Schema MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 3,834 ± 4 | 208 ± 2 | 0.0 ± 0.0 | 0.0 ± 0.0 | 70.0 ± 0.0 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 5.0 ± 0.0 | 11.0 ± 0.0 | 25.0 ± 0.0 | 1,891 ± 56 | 94,691 ± 1 | 37,714 ± 1 | 27,396 ± 0 |
| **A2** — REST (minimal toolset) | 5.0 ± 0.0 | 11.0 ± 0.0 | 25.0 ± 0.0 | 1,961 ± 5 | 46,387 ± 2 | 37,555 ± 6 | 27,396 ± 0 |
| **B** — GraphQL (Apollo MCP) | 4.0 ± 0.0 | 2.0 ± 0.0 | 8,280 ± 1 | 1,087 ± 20 | 0.0 ± 0.0 | 0.0 ± 0.0 | 513 ± 0 |
| **B2** — GraphQL (Rover Schema MCP) | 4.0 ± 0.0 | 2.0 ± 0.0 | 8,516 ± 104 | 1,124 ± 69 | 0.0 ± 0.0 | 0.0 ± 0.0 | 534 ± 40 |

## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **A1** | 56 | — | 18,805–18,839 | 4,096 | yes |
| **A2** | 22 | — | 9,111–9,146 | 4,096 | yes |
| **B** | 4 | — | 1,753–1,788 | 4,096 | **no** — every prefix is below the minimum |
| **B2** | 3 | — | 1,797–1,833 | 4,096 | **no** — every prefix is below the minimum |

**12 of 24 runs carry a prefix below their model's cache minimum (B, B2), so in those runs the tool surface is never written to cache at all.** Their first `cache_creation` charge fires when the *conversation* crosses the minimum, several tool rounds in — which is why Stage 1 below is labelled for that event and not for schema loading. Where a surface does clear the minimum on its own, a fatter one really does buy a bigger Stage 1; where it does not, it buys a bigger uncached `input_tokens` bill on every call until the conversation grows past the threshold. The two are not the same cost and the Stage 1 column does not distinguish them — this table is how you tell which one a row is.


## How to read these numbers

Every inference run goes through three phases. Understanding them explains why the token counts look the way they do.

**First cache write (Stage 1)** — Before Claude can act, the harness sends it a full description of every available tool. For REST conditions (A1/A2) that's 17–22 endpoint definitions; for GraphQL (B/B2) it's just 3–4 generic tools. Anthropic will cache that context, but only once the prompt clears the model's **minimum cacheable prefix** — which is model-dependent and not monotonic in model size (4,096 tokens on Haiku 4.5, 1,024 on Sonnet 5, 512 on Opus 5), so it cannot be inferred from the model name. Stage 1 captures the `cache_creation` charge for the first write that happens. **It is named for that event, not for schema loading**, and the two coincide only when the tool surface alone clears the minimum — see the prefix table above for whether it does here. When it does not, the first write fires several tool rounds in, once the *conversation* has grown past the threshold, and the tool surface is paid at the uncached `input_tokens` rate on every call until then. This section previously read "once it exceeds ~1 000 tokens" and attributed Stage 1 to schema size; ~1,000 is Sonnet's minimum, and the wrong threshold is what left the zero-cache-read finding without a mechanism.

**Context growth (Stage 2)** — Each tool call extends the conversation: the tool's response is appended and the *now-longer* context must be written to cache again so the next inference call can read it cheaply. Stage 2 sums those incremental `cache_creation` charges — the cost of *maintaining* the cache as it grows, not of using it. Two factors drive Stage 2 higher: more round trips (more re-writes) and larger payloads per round trip (more new tokens to cache each time). REST conditions are penalised on both axes: 10 tool calls vs. 1, and full REST API objects (~82 KB for 5 PRs) vs. GraphQL's field-precise responses (~1 KB). Stage 2 is where most of the REST–GraphQL cost difference accumulates.

**Inference compute (Stage 3)** — The cost of the model *reading and generating*, not writing. It has three components: `cache_read_input_tokens` (tokens pulled from the cache Stages 1–2 built — cheap but not free), `input_tokens` (any prompt tokens processed fresh, not from cache), and `output_tokens` (tokens Claude generates). Stage 3 is roughly constant across conditions for the same task, because the task prompt and final answer are similar in size regardless of which API protocol answered the question. It does not include cache-write charges — those are entirely in Stages 1 and 2.

The three stages are additive — total cost = Stage 1 + Stage 2 + Stage 3. **One cross-condition caveat:** A1/A2's tool surface clears the cache minimum on its own (an 18,438-token prefix against Haiku 4.5's 4,096), so their first write really is schema injection. B/B2's does not, so their Stage 1 fires later in the conversation and includes early turns that REST pays in Stage 2. The two arms' Stage 1 figures are therefore not the same quantity. The Stage 1 + Stage 2 sum and Stage 3 are the reliable cross-condition comparators. The stage split is most useful within a single condition to understand how its cost is structured.


## Cost breakdown by prompt lifecycle stage

Each run's cost is split across the three stages of the inference prompt lifecycle. All values are **mean USD/run** across reps.


![Cost by stage and tool-response size per task](summary_charts.png)

| Condition | Task | Stage 1 — First cache write | Stage 2 — Context growth | Stage 3 — Inference compute | Total |
|---|---|---|---|---|---|
| **A1** — REST (default toolset) | T1 | $0.0016 | $0.0433 | $0.0143 | **$0.0592** |
| **A1** — REST (default toolset) | T2 | $0.0016 | $0.0007 | $0.0046 | **$0.0069** |
| **A2** — REST (minimal toolset) | T1 | $0.0015 | $0.0433 | $0.0118 | **$0.0565** |
| **A2** — REST (minimal toolset) | T2 | $0.0015 | $0.0007 | $0.0027 | **$0.0049** |
| **B** — GraphQL (Apollo MCP) | T1 | $0.0000 | $0.0000 | $0.0090 | **$0.0090** |
| **B** — GraphQL (Apollo MCP) | T2 | $0.0000 | $0.0000 | $0.0048 | **$0.0048** |
| **B2** — GraphQL (Rover Schema MCP) | T1 | $0.0000 | $0.0000 | $0.0093 | **$0.0093** |
| **B2** — GraphQL (Rover Schema MCP) | T2 | $0.0000 | $0.0000 | $0.0049 | **$0.0049** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. A1/A2's 18,438-token prefix clears the 4,096-token minimum on call 1, so their Stage 1 is schema injection. B/B2's small surface does not, so their first write waits for the conversation to grow and their Stage 1 absorbs early tool rounds that REST pays in Stage 2. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-haiku-4-5-20251001: input $1.0/1M out $5.0/1M cc $1.25/1M cr $0.1/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **A1** — REST (default toolset) | T1 | 3 | $0.0592 | $0.1775 |
| **A1** — REST (default toolset) | T2 | 3 | $0.0069 | $0.0208 |
| **A2** — REST (minimal toolset) | T1 | 3 | $0.0565 | $0.1696 |
| **A2** — REST (minimal toolset) | T2 | 3 | $0.0049 | $0.0146 |
| **B** — GraphQL (Apollo MCP) | T1 | 3 | $0.0090 | $0.0269 |
| **B** — GraphQL (Apollo MCP) | T2 | 3 | $0.0048 | $0.0143 |
| **B2** — GraphQL (Rover Schema MCP) | T1 | 3 | $0.0093 | $0.0278 |
| **B2** — GraphQL (Rover Schema MCP) | T2 | 3 | $0.0049 | $0.0146 |

**Grand total across all conditions/tasks/reps: $0.4661**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **A1** — REST (default toolset) | T1 | 17.2 ± 2.9s | 8.3 ± 0.3s |
| **A1** — REST (default toolset) | T2 | 5.6 ± 0.0s | 2.2 ± 0.2s |
| **A2** — REST (minimal toolset) | T1 | 18.9 ± 2.9s | 8.2 ± 0.1s |
| **A2** — REST (minimal toolset) | T2 | 5.6 ± 0.0s | 2.0 ± 0.1s |
| **B** — GraphQL (Apollo MCP) | T1 | 15.6 ± 0.0s | 3.1 ± 0.1s |
| **B** — GraphQL (Apollo MCP) | T2 | 10.6 ± 0.0s | 2.0 ± 0.1s |
| **B2** — GraphQL (Rover Schema MCP) | T1 | 10.6 ± 0.1s | 3.5 ± 0.4s |
| **B2** — GraphQL (Rover Schema MCP) | T2 | 5.6 ± 0.0s | 2.2 ± 0.2s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-haiku-4-5-20251001`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | T1 | 1 | 3 | 17 | 58342 | $0.059 | 15.6s | 8.0s | 0 | 0 | 0 | yes | 0 |
| A1 | T1 | 2 | 3 | 17 | 58344 | $0.059 | 20.6s | 8.6s | 0 | 0 | 0 | yes | 0 |
| A1 | T1 | 3 | 3 | 17 | 58342 | $0.059 | 15.5s | 8.2s | 0 | 0 | 0 | yes | 0 |
| A1 | T2 | 1 | 2 | 8 | 36348 | $0.007 | 5.6s | 2.1s | 0 | 0 | 0 | yes | 0 |
| A1 | T2 | 2 | 2 | 8 | 36348 | $0.007 | 5.6s | 2.1s | 0 | 0 | 0 | yes | 0 |
| A1 | T2 | 3 | 2 | 8 | 36349 | $0.007 | 5.6s | 2.4s | 0 | 0 | 0 | yes | 0 |
| A2 | T1 | 1 | 3 | 17 | 29344 | $0.057 | 20.6s | 8.3s | 0 | 0 | 0 | yes | 0 |
| A2 | T1 | 2 | 3 | 17 | 29342 | $0.057 | 20.6s | 8.3s | 0 | 0 | 0 | yes | 0 |
| A2 | T1 | 3 | 3 | 17 | 29346 | $0.057 | 15.6s | 8.1s | 0 | 0 | 0 | yes | 0 |
| A2 | T2 | 1 | 2 | 8 | 17044 | $0.005 | 5.6s | 2.1s | 0 | 0 | 0 | yes | 0 |
| A2 | T2 | 2 | 2 | 8 | 17043 | $0.005 | 5.6s | 1.9s | 0 | 0 | 0 | yes | 0 |
| A2 | T2 | 3 | 2 | 8 | 17042 | $0.005 | 5.6s | 2.1s | 0 | 0 | 0 | yes | 0 |
| B | T1 | 1 | 2 | 4537 | 0 | $0.009 | 15.6s | 3.0s | 0 | 0 | 0 | yes | 0 |
| B | T1 | 2 | 2 | 4539 | 0 | $0.009 | 15.6s | 3.2s | 0 | 0 | 0 | yes | 0 |
| B | T1 | 3 | 2 | 4537 | 0 | $0.009 | 15.6s | 3.1s | 0 | 0 | 0 | yes | 0 |
| B | T2 | 1 | 2 | 3742 | 0 | $0.005 | 10.6s | 2.0s | 0 | 0 | 0 | yes | 0 |
| B | T2 | 2 | 2 | 3742 | 0 | $0.005 | 10.6s | 1.9s | 0 | 0 | 0 | yes | 0 |
| B | T2 | 3 | 2 | 3742 | 0 | $0.005 | 10.6s | 2.0s | 0 | 0 | 0 | yes | 0 |
| B2 | T1 | 1 | 2 | 4616 | 0 | $0.009 | 10.6s | 3.2s | 0 | 0 | 0 | yes | 0 |
| B2 | T1 | 2 | 2 | 4631 | 0 | $0.009 | 10.5s | 3.9s | 0 | 0 | 0 | yes | 0 |
| B2 | T1 | 3 | 2 | 4799 | 0 | $0.010 | 10.6s | 3.5s | 0 | 0 | 0 | yes | 0 |
| B2 | T2 | 1 | 2 | 3835 | 0 | $0.005 | 5.6s | 2.4s | 0 | 0 | 0 | yes | 0 |
| B2 | T2 | 2 | 2 | 3830 | 0 | $0.005 | 5.6s | 2.2s | 0 | 0 | 0 | yes | 0 |
| B2 | T2 | 3 | 2 | 3837 | 0 | $0.005 | 5.6s | 2.1s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

