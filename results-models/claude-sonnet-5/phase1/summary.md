# Benchmark Results — REST-backed MCP vs GraphQL-backed MCP

## Key Findings

- **T1 (5 PRs + changed files) — REST vs GraphQL:** A1 uses **2 inference calls** vs B2's **2** (no material difference). REST requires one get_pull_request + one get_pull_request_files call per PR; B2 fetches all five in one aliased GraphQL query. Cost: A1 $0.193 vs B2 $0.018 per run (**10.9× cheaper with B2**).
- **REST context overhead:** A1's tool schema and accumulated REST tool responses write **65K cache-creation tokens** ($0.163/run, 84% of total T1 cost). Each of A1's 2 inference calls extends the cached context with a full REST API payload; B2 writes only 3K tokens across its 2 calls.
- **T1 GraphQL comparison (B vs B2):** B2 (Rover Schema MCP, 3 tools) uses 2 vs B's 3 inference calls on T1, costing $0.018 vs $0.028/run. Rover's smaller tool schema and targeted keyword search keep schema-discovery overhead low.
- **T2 (single PR lookup) — B costs 1.4× more** than B2 on a one-entity lookup (2.0 vs 2.7 calls, $0.006 vs $0.008). Both reach the answer; the gap is schema-discovery overhead before the single execute, so it is a property of the tool surface rather than of the query.
- **Overall (all tasks):** B2 is **1.5× cheaper** than B ($0.023 vs $0.036/run) and **9.2×** cheaper than A1 ($0.214/run), driven primarily by T1's GraphQL nested-query advantage.

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (A1 / A2 / B / B2)


### Task T1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 2.0 ± 0.0 | 10.0 ± 0.0 | 3.0 ± 0.0 | 2,199 ± 64 | 41,152 ± 13,248 | 65,009 ± 15,605 | 33,208 ± 10,765 |
| **A2** — REST (minimal toolset) | 2.0 ± 0.0 | 10.0 ± 0.0 | 3.0 ± 0.0 | 2,104 ± 21 | 18,073 ± 5,927 | 78,698 ± 5,927 | 45,639 ± 0 |
| **B** — GraphQL (Apollo MCP) | 3.3 ± 0.6 | 2.3 ± 0.6 | 5.7 ± 1.2 | 1,245 ± 77 | 5,017 ± 939 | 5,663 ± 1,259 | 1,342 ± 387 |
| **B2** — GraphQL (Rover Schema MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 3.0 ± 0.0 | 1,050 ± 38 | 2,405 ± 613 | 2,666 ± 584 | 444 ± 0 |

### Task T2

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 2.0 ± 0.0 | 1.0 ± 0.0 | 3.0 ± 0.0 | 185 ± 5 | 48,801 ± 0 | 3,990 ± 0 | 334 ± 0 |
| **A2** — REST (minimal toolset) | 2.0 ± 0.0 | 1.0 ± 0.0 | 3.0 ± 0.0 | 187 ± 6 | 21,495 ± 0 | 2,044 ± 0 | 334 ± 0 |
| **B** — GraphQL (Apollo MCP) | 2.7 ± 1.2 | 1.7 ± 1.2 | 4.3 ± 2.3 | 237 ± 100 | 4,067 ± 1,773 | 1,927 ± 1,918 | 263 ± 374 |
| **B2** — GraphQL (Rover Schema MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 3.0 ± 0.0 | 185 ± 37 | 2,759 ± 0 | 1,270 ± 10 | 47.0 ± 0.0 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 4.0 ± 0.0 | 11.0 ± 0.0 | 6.0 ± 0.0 | 2,384 ± 65 | 89,953 ± 13,248 | 68,999 ± 15,605 | 33,542 ± 10,765 |
| **A2** — REST (minimal toolset) | 4.0 ± 0.0 | 11.0 ± 0.0 | 6.0 ± 0.0 | 2,290 ± 19 | 39,568 ± 5,927 | 80,742 ± 5,927 | 45,973 ± 0 |
| **B** — GraphQL (Apollo MCP) | 6.0 ± 1.0 | 4.0 ± 1.0 | 10.0 ± 2.0 | 1,482 ± 95 | 9,084 ± 1,429 | 7,590 ± 1,073 | 1,604 ± 321 |
| **B2** — GraphQL (Rover Schema MCP) | 4.0 ± 0.0 | 2.0 ± 0.0 | 6.0 ± 0.0 | 1,235 ± 30 | 5,164 ± 613 | 3,936 ± 594 | 491 ± 0 |

## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **A1** | 56 | — | 26,067–26,103 | 1,024 | yes |
| **A2** | 22 | — | 11,441–11,477 | 1,024 | yes |
| **B** | 4 | — | 1,838–1,874 | 1,024 | yes |
| **B2** | 3 | — | 1,910–1,946 | 1,024 | yes |

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
| **A1** — REST (default toolset) | T1 | $0.0270 | $0.1355 | $0.0302 | **$0.1927** |
| **A1** — REST (default toolset) | T2 | $0.0078 | $0.0022 | $0.0116 | **$0.0216** |
| **A2** — REST (minimal toolset) | T1 | $0.0116 | $0.1852 | $0.0247 | **$0.2214** |
| **A2** — REST (minimal toolset) | T2 | $0.0029 | $0.0022 | $0.0062 | **$0.0113** |
| **B** — GraphQL (Apollo MCP) | T1 | $0.0016 | $0.0125 | $0.0135 | **$0.0276** |
| **B** — GraphQL (Apollo MCP) | T2 | $0.0012 | $0.0036 | $0.0032 | **$0.0080** |
| **B2** — GraphQL (Rover Schema MCP) | T1 | $0.0031 | $0.0036 | $0.0110 | **$0.0177** |
| **B2** — GraphQL (Rover Schema MCP) | T2 | $0.0021 | $0.0011 | $0.0024 | **$0.0056** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. A1/A2's 18,438-token prefix clears the 4,096-token minimum on call 1, so their Stage 1 is schema injection. B/B2's small surface does not, so their first write waits for the conversation to grow and their Stage 1 absorbs early tool rounds that REST pays in Stage 2. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-sonnet-5: input $2.0/1M out $10.0/1M cc $2.5/1M cr $0.2/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **A1** — REST (default toolset) | T1 | 3 | $0.1927 | $0.5782 |
| **A1** — REST (default toolset) | T2 | 3 | $0.0216 | $0.0648 |
| **A2** — REST (minimal toolset) | T1 | 3 | $0.2214 | $0.6642 |
| **A2** — REST (minimal toolset) | T2 | 3 | $0.0113 | $0.0338 |
| **B** — GraphQL (Apollo MCP) | T1 | 3 | $0.0276 | $0.0829 |
| **B** — GraphQL (Apollo MCP) | T2 | 3 | $0.0080 | $0.0240 |
| **B2** — GraphQL (Rover Schema MCP) | T1 | 3 | $0.0177 | $0.0530 |
| **B2** — GraphQL (Rover Schema MCP) | T2 | 3 | $0.0056 | $0.0168 |

**Grand total across all conditions/tasks/reps: $1.5177**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **A1** — REST (default toolset) | T1 | 22.3 ± 2.9s | 10.0 ± 0.7s |
| **A1** — REST (default toolset) | T2 | 12.3 ± 2.9s | 4.6 ± 2.3s |
| **A2** — REST (minimal toolset) | T1 | 22.3 ± 2.9s | 10.8 ± 1.6s |
| **A2** — REST (minimal toolset) | T2 | 10.6 ± 0.1s | 4.8 ± 0.3s |
| **B** — GraphQL (Apollo MCP) | T1 | 15.6 ± 0.0s | 8.5 ± 1.2s |
| **B** — GraphQL (Apollo MCP) | T2 | 10.6 ± 0.1s | 5.5 ± 2.3s |
| **B2** — GraphQL (Rover Schema MCP) | T1 | 10.7 ± 0.1s | 4.1 ± 0.3s |
| **B2** — GraphQL (Rover Schema MCP) | T2 | 7.2 ± 2.8s | 3.7 ± 1.6s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-sonnet-5`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | T1 | 1 | 2 | 3 | 25855 | $0.203 | 20.6s | 10.2s | 1 | 209 | 0 | yes | 0 |
| A1 | T1 | 2 | 2 | 3 | 48801 | $0.224 | 25.6s | 9.2s | 1 | 210 | 0 | yes | 0 |
| A1 | T1 | 3 | 2 | 3 | 48801 | $0.151 | 20.6s | 10.5s | 1 | 210 | 0 | yes | 0 |
| A1 | T2 | 1 | 2 | 3 | 48801 | $0.022 | 10.6s | 3.3s | 1 | 180 | 0 | yes | 0 |
| A1 | T2 | 2 | 2 | 3 | 48801 | $0.022 | 10.6s | 3.3s | 1 | 180 | 0 | yes | 0 |
| A1 | T2 | 3 | 2 | 3 | 48801 | $0.022 | 15.6s | 7.3s | 1 | 180 | 0 | yes | 0 |
| A2 | T1 | 1 | 2 | 3 | 11229 | $0.237 | 20.6s | 11.9s | 1 | 210 | 0 | yes | 0 |
| A2 | T1 | 2 | 2 | 3 | 21495 | $0.214 | 25.6s | 11.6s | 1 | 210 | 0 | yes | 0 |
| A2 | T1 | 3 | 2 | 3 | 21495 | $0.213 | 20.6s | 9.0s | 1 | 210 | 0 | yes | 0 |
| A2 | T2 | 1 | 2 | 3 | 21495 | $0.011 | 10.7s | 5.2s | 1 | 180 | 0 | yes | 0 |
| A2 | T2 | 2 | 2 | 3 | 21495 | $0.011 | 10.5s | 4.7s | 1 | 180 | 0 | yes | 0 |
| A2 | T2 | 3 | 2 | 3 | 21495 | $0.011 | 10.5s | 4.6s | 1 | 180 | 0 | yes | 0 |
| B | T1 | 1 | 3 | 5 | 4475 | $0.030 | 15.6s | 9.2s | 1 | 210 | 0 | yes | 0 |
| B | T1 | 2 | 4 | 7 | 6101 | $0.028 | 15.6s | 9.1s | 1 | 209 | 0 | yes | 0 |
| B | T1 | 3 | 3 | 5 | 4475 | $0.024 | 15.6s | 7.1s | 1 | 210 | 0 | yes | 0 |
| B | T2 | 1 | 2 | 3 | 3252 | $0.004 | 10.5s | 6.1s | 1 | 180 | 0 | yes | 0 |
| B | T2 | 2 | 2 | 3 | 2849 | $0.005 | 10.6s | 2.9s | 1 | 180 | 0 | yes | 0 |
| B | T2 | 3 | 4 | 7 | 6101 | $0.015 | 10.6s | 7.4s | 1 | 180 | 0 | yes | 0 |
| B2 | T1 | 1 | 2 | 3 | 1698 | $0.019 | 10.7s | 3.8s | 1 | 210 | 0 | yes | 0 |
| B2 | T1 | 2 | 2 | 3 | 2759 | $0.017 | 10.6s | 4.2s | 1 | 211 | 0 | yes | 0 |
| B2 | T1 | 3 | 2 | 3 | 2759 | $0.017 | 10.7s | 4.3s | 1 | 210 | 0 | yes | 0 |
| B2 | T2 | 1 | 2 | 3 | 2759 | $0.006 | 10.5s | 5.5s | 1 | 180 | 0 | yes | 0 |
| B2 | T2 | 2 | 2 | 3 | 2759 | $0.005 | 5.6s | 2.7s | 1 | 180 | 0 | yes | 0 |
| B2 | T2 | 3 | 2 | 3 | 2759 | $0.005 | 5.6s | 2.9s | 1 | 180 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

