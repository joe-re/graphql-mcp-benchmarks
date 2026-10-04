# Benchmark Results — REST-backed MCP vs GraphQL-backed MCP

## Key Findings

- **T1 (5 PRs + changed files) — REST vs GraphQL:** A1 uses **2 inference calls** vs B2's **2** (no material difference). REST requires one get_pull_request + one get_pull_request_files call per PR; B2 fetches all five in one aliased GraphQL query. Cost: A1 $0.328 vs B2 $0.033 per run (**10.0× cheaper with B2**).
- **REST context overhead:** A1's tool schema and accumulated REST tool responses write **55K cache-creation tokens** ($0.275/run, 84% of total T1 cost). Each of A1's 2 inference calls extends the cached context with a full REST API payload; B2 writes only 3K tokens across its 2 calls.
- **T1 GraphQL comparison (B vs B2):** B2 (Rover Schema MCP, 3 tools) uses 2 vs B's 2 inference calls on T1, costing $0.033 vs $0.029/run. Rover's smaller tool schema and targeted keyword search keep schema-discovery overhead low.
- **T2 (single PR lookup) — B2 costs 1.2× more** than B on a one-entity lookup (2.0 vs 2.0 calls, $0.010 vs $0.008). Both reach the answer; the gap is schema-discovery overhead before the single execute, so it is a property of the tool surface rather than of the query.
- **Overall (all tasks):** B and B2 are close in combined cost ($0.038 vs $0.043/run); both are substantially cheaper than A1 ($0.361/run).

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (A1 / A2 / B / B2)


### Task T1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 2.0 ± 0.0 | 10.0 ± 0.0 | 6.0 ± 0.0 | 2,234 ± 119 | 41,082 ± 13,246 | 55,015 ± 13,246 | 26,993 ± 0 |
| **A2** — REST (minimal toolset) | 2.0 ± 0.0 | 10.0 ± 0.0 | 6.0 ± 0.0 | 2,234 ± 68 | 18,002 ± 5,925 | 48,843 ± 5,925 | 26,993 ± 0 |
| **B** — GraphQL (Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 6.0 ± 0.0 | 962 ± 30 | 2,777 ± 0 | 1,884 ± 14 | 426 ± 14 |
| **B2** — GraphQL (Rover Schema MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 6.0 ± 0.0 | 983 ± 46 | 2,335 ± 610 | 2,515 ± 588 | 439 ± 26 |

### Task T2

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 2.0 ± 0.0 | 1.0 ± 0.0 | 6.0 ± 0.0 | 198 ± 1 | 48,729 ± 0 | 3,927 ± 0 | 334 ± 0 |
| **A2** — REST (minimal toolset) | 2.0 ± 0.0 | 1.0 ± 0.0 | 6.0 ± 0.0 | 193 ± 25 | 21,423 ± 0 | 1,981 ± 0 | 334 ± 0 |
| **B** — GraphQL (Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 6.0 ± 0.0 | 172 ± 1 | 2,890 ± 196 | 850 ± 196 | 47.0 ± 0.0 |
| **B2** — GraphQL (Rover Schema MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 6.0 ± 0.0 | 177 ± 1 | 2,687 ± 0 | 1,212 ± 5 | 53.3 ± 2.3 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **A1** — REST (default toolset) | 4.0 ± 0.0 | 11.0 ± 0.0 | 12.0 ± 0.0 | 2,431 ± 119 | 89,811 ± 13,246 | 58,942 ± 13,246 | 27,327 ± 0 |
| **A2** — REST (minimal toolset) | 4.0 ± 0.0 | 11.0 ± 0.0 | 12.0 ± 0.0 | 2,427 ± 43 | 39,425 ± 5,925 | 50,824 ± 5,925 | 27,327 ± 0 |
| **B** — GraphQL (Apollo MCP) | 4.0 ± 0.0 | 2.0 ± 0.0 | 12.0 ± 0.0 | 1,135 ± 30 | 5,667 ± 196 | 2,734 ± 182 | 473 ± 14 |
| **B2** — GraphQL (Rover Schema MCP) | 4.0 ± 0.0 | 2.0 ± 0.0 | 12.0 ± 0.0 | 1,159 ± 46 | 5,022 ± 610 | 3,726 ± 586 | 492 ± 27 |

## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **A1** | 56 | — | 26,001–26,037 | 512 | yes |
| **A2** | 22 | — | 11,375–11,411 | 512 | yes |
| **B** | 4 | — | 1,772–1,808 | 512 | yes |
| **B2** | 3 | — | 1,844–1,880 | 512 | yes |

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
| **A1** — REST (default toolset) | T1 | $0.0537 | $0.2214 | $0.0529 | **$0.3280** |
| **A1** — REST (default toolset) | T2 | $0.0153 | $0.0044 | $0.0137 | **$0.0334** |
| **A2** — REST (minimal toolset) | T1 | $0.0228 | $0.2214 | $0.0483 | **$0.2925** |
| **A2** — REST (minimal toolset) | T2 | $0.0055 | $0.0044 | $0.0082 | **$0.0181** |
| **B** — GraphQL (Apollo MCP) | T1 | $0.0029 | $0.0065 | $0.0198 | **$0.0292** |
| **B** — GraphQL (Apollo MCP) | T2 | $0.0022 | $0.0021 | $0.0040 | **$0.0083** |
| **B2** — GraphQL (Rover Schema MCP) | T1 | $0.0059 | $0.0067 | $0.0201 | **$0.0327** |
| **B2** — GraphQL (Rover Schema MCP) | T2 | $0.0039 | $0.0021 | $0.0041 | **$0.0102** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. A1/A2's 18,438-token prefix clears the 4,096-token minimum on call 1, so their Stage 1 is schema injection. B/B2's small surface does not, so their first write waits for the conversation to grow and their Stage 1 absorbs early tool rounds that REST pays in Stage 2. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-opus-5-5: input $4.0/1M out $20.0/1M cc $5.0/1M cr $0.2/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **A1** — REST (default toolset) | T1 | 3 | $0.3280 | $0.9840 |
| **A1** — REST (default toolset) | T2 | 3 | $0.0334 | $0.1001 |
| **A2** — REST (minimal toolset) | T1 | 3 | $0.2925 | $0.8775 |
| **A2** — REST (minimal toolset) | T2 | 3 | $0.0181 | $0.0542 |
| **B** — GraphQL (Apollo MCP) | T1 | 3 | $0.0292 | $0.0877 |
| **B** — GraphQL (Apollo MCP) | T2 | 3 | $0.0083 | $0.0249 |
| **B2** — GraphQL (Rover Schema MCP) | T1 | 3 | $0.0327 | $0.0982 |
| **B2** — GraphQL (Rover Schema MCP) | T2 | 3 | $0.0102 | $0.0305 |

**Grand total across all conditions/tasks/reps: $2.2571**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **A1** — REST (default toolset) | T1 | 25.6 ± 0.1s | 12.3 ± 0.7s |
| **A1** — REST (default toolset) | T2 | 10.6 ± 0.0s | 4.7 ± 1.4s |
| **A2** — REST (minimal toolset) | T1 | 25.6 ± 0.0s | 11.7 ± 0.2s |
| **A2** — REST (minimal toolset) | T2 | 10.5 ± 0.1s | 3.8 ± 0.4s |
| **B** — GraphQL (Apollo MCP) | T1 | 15.6 ± 0.0s | 4.7 ± 0.4s |
| **B** — GraphQL (Apollo MCP) | T2 | 10.5 ± 0.1s | 3.5 ± 0.6s |
| **B2** — GraphQL (Rover Schema MCP) | T1 | 15.6 ± 0.1s | 4.2 ± 0.7s |
| **B2** — GraphQL (Rover Schema MCP) | T2 | 8.9 ± 2.9s | 3.4 ± 0.4s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-opus-5-5`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | T1 | 1 | 2 | 6 | 25787 | $0.401 | 25.6s | 11.6s | 1 | 210 | 0 | yes | 0 |
| A1 | T1 | 2 | 2 | 6 | 48729 | $0.289 | 25.6s | 12.4s | 1 | 210 | 0 | yes | 0 |
| A1 | T1 | 3 | 2 | 6 | 48729 | $0.294 | 25.5s | 12.9s | 1 | 210 | 0 | yes | 0 |
| A1 | T2 | 1 | 2 | 6 | 48729 | $0.033 | 10.6s | 3.2s | 1 | 180 | 0 | yes | 0 |
| A1 | T2 | 2 | 2 | 6 | 48729 | $0.033 | 10.6s | 5.9s | 1 | 180 | 0 | yes | 0 |
| A1 | T2 | 3 | 2 | 6 | 48729 | $0.033 | 10.6s | 5.1s | 1 | 177 | 0 | yes | 0 |
| A2 | T1 | 1 | 2 | 6 | 11161 | $0.326 | 25.6s | 11.5s | 1 | 210 | 0 | yes | 0 |
| A2 | T1 | 2 | 2 | 6 | 21423 | $0.277 | 25.6s | 11.7s | 1 | 210 | 0 | yes | 0 |
| A2 | T1 | 3 | 2 | 6 | 21423 | $0.275 | 25.6s | 11.9s | 1 | 210 | 0 | yes | 0 |
| A2 | T2 | 1 | 2 | 6 | 21423 | $0.018 | 10.6s | 3.9s | 1 | 180 | 0 | yes | 0 |
| A2 | T2 | 2 | 2 | 6 | 21423 | $0.018 | 10.5s | 3.3s | 1 | 177 | 0 | yes | 0 |
| A2 | T2 | 3 | 2 | 6 | 21423 | $0.019 | 10.5s | 4.1s | 1 | 180 | 0 | yes | 0 |
| B | T1 | 1 | 2 | 6 | 2777 | $0.030 | 15.6s | 4.5s | 1 | 210 | 0 | yes | 0 |
| B | T1 | 2 | 2 | 6 | 2777 | $0.029 | 15.6s | 5.1s | 1 | 210 | 0 | yes | 0 |
| B | T1 | 3 | 2 | 6 | 2777 | $0.029 | 15.6s | 4.4s | 1 | 211 | 0 | yes | 0 |
| B | T2 | 1 | 2 | 6 | 3116 | $0.007 | 10.5s | 3.4s | 1 | 180 | 0 | yes | 0 |
| B | T2 | 2 | 2 | 6 | 2777 | $0.009 | 10.5s | 3.0s | 1 | 180 | 0 | yes | 0 |
| B | T2 | 3 | 2 | 6 | 2777 | $0.009 | 10.6s | 4.2s | 1 | 180 | 0 | yes | 0 |
| B2 | T1 | 1 | 2 | 6 | 1630 | $0.037 | 15.6s | 5.0s | 1 | 210 | 0 | yes | 0 |
| B2 | T1 | 2 | 2 | 6 | 2687 | $0.031 | 15.5s | 3.7s | 1 | 210 | 0 | yes | 0 |
| B2 | T1 | 3 | 2 | 6 | 2687 | $0.030 | 15.6s | 3.8s | 1 | 209 | 0 | yes | 0 |
| B2 | T2 | 1 | 2 | 6 | 2687 | $0.010 | 5.6s | 2.9s | 1 | 180 | 0 | yes | 0 |
| B2 | T2 | 2 | 2 | 6 | 2687 | $0.010 | 10.6s | 3.7s | 1 | 180 | 0 | yes | 0 |
| B2 | T2 | 3 | 2 | 6 | 2687 | $0.010 | 10.5s | 3.5s | 1 | 180 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

