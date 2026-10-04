# Phase 2 Results — who performs the join

## Key Findings

- _Key findings skipped: this run covers a subset of the phase-2 matrix._

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (M-R1-fat / M-G2)


### Task M1@1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 147 ± 13 | 7,847 ± 2,441 | 3,808 ± 2,437 | 888 ± 5 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 117 ± 0 | 3,891 ± 126 | 987 ± 127 | 103 ± 0 |

### Task M1@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 331 ± 30 | 9,276 ± 0 | 7,573 ± 0 | 4,026 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 286 ± 4 | 3,838 ± 1 | 1,698 ± 1 | 478 ± 0 |

### Task M1@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 912 ± 99 | 9,352 ± 1 | 27,254 ± 1 | 15,837 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 830 ± 84 | 3,910 ± 1 | 4,072 ± 1 | 1,878 ± 0 |

### Task M1@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 1,898 ± 4 | 9,501 ± 1 | 66,731 ± 5 | 39,607 ± 1 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 34.0 ± 0.0 | 2,278 ± 475 | 4,207 ± 127 | 8,684 ± 126 | 4,681 ± 0 |

### Task M3@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 3.0 ± 0.0 | 4.0 ± 0.0 | 66.0 ± 0.0 | 1,579 ± 78 | 24,115 ± 1 | 26,313 ± 72 | 15,622 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 10.0 ± 0.0 | 34.0 ± 0.0 | 1,327 ± 38 | 4,048 ± 1 | 8,377 ± 12 | 4,465 ± 0 |

### Task M3@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 5.3 ± 4.0 | 6.0 ± 3.5 | 121 ± 96 | 5,377 ± 2,709 | 104,508 ± 92,349 | 130,688 ± 56,142 | 95,553 ± 61,665 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 4.7 ± 2.9 | 43.3 ± 5.8 | 109 ± 75 | 5,937 ± 2,863 | 33,616 ± 20,155 | 35,633 ± 4,831 | 23,928 ± 10,561 |

### Task M3@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 3.0 ± 0.0 | 4.0 ± 0.0 | 66.0 ± 0.0 | 10,312 ± 289 | 105,365 ± 17 | 227,024 ± 7 | 139,536 ± 1 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 3.3 ± 0.6 | 100 ± 0 | 76.7 ± 18.5 | 9,704 ± 857 | 29,343 ± 31,216 | 79,454 ± 727 | 44,461 ± 0 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 19.3 ± 4.0 | 18.0 ± 3.5 | 389 ± 96 | 20,555 ± 2,676 | 269,962 ± 93,608 | 489,392 ± 54,946 | 311,069 ± 61,662 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 18.0 ± 2.6 | 157 ± 6 | 356 ± 68 | 20,480 ± 1,921 | 82,853 ± 29,357 | 138,904 ± 4,585 | 79,994 ± 10,561 |

## Accuracy

`answer_f1` is field-level precision/recall against `tasks/expected.json`, whose `grading` block defines the rules per task. **coverage** is the fraction of the records the prompt asked about that the answer mentions at all — reported separately because a truncated answer can be perfectly accurate on what it does say.

| Condition | M1@1 f1 | M1@5 f1 | M1@20 f1 | M1@50 f1 | M3@5 f1 | M3@20 f1 | M3@50 f1 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |

**On grounding.** 42 of 42 finished run(s) are fact-verified: every fact the answer states was traced to a `tool_result` that entered the context before it, using the proxy's `tool_io.jsonl` sidecar. 0 failed that check. `answer_grounded` is never `True` by default, so a blank means unassessed, not passed.


## Join tax — pass-through tokens and forced serial depth

**pass-through** is tool-result tokens whose values never appear in the answer: payload the agent carried through its context and did not use. **depth** is the longest chain of calls where each consumed an identifier the previous one returned — ids the prompt supplied are excluded, so reading the instructions does not count as a dependency.

**disc** is the same measure over *schema and spec lookup* — search feeding describe. That serialization is real latency, but it is a property of the tool surface rather than of the join, and it exists only in the on-demand conditions. Folding it into `depth` would make the headline metric track tool packaging instead of who performs the join, so the two are reported side by side.

**ex-disc** applies the same reasoning to the token figure, and it is shown wherever it changes the number. Schema and OpenAPI text is ~100% pass-through by this definition — the agent reads an SDL fragment to write a query and quotes none of it back — so `pass-through` charges the on-demand conditions for finding their own way around, while `depth` explicitly does not. That disagreement was silent until it was measured; it is not small, and it does not favour the hypothesis. Both numbers are here because which one a reader wants is an editorial call: **pass-through** is every token carried, **ex-disc** is the join tax alone.

| Condition | M1@1 | M1@5 | M1@20 | M1@50 | M3@5 | M3@20 | M3@50 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 832 tok<br>(94% unused)<br>depth 1.0 | 3,778 tok<br>(94% unused)<br>depth 1.0 | 14,649 tok<br>(92% unused)<br>depth 1.0 | 36,553 tok<br>(92% unused)<br>depth 1.0 | 14,645 tok<br>(94% unused)<br>depth 2.0 | 91,250 tok<br>(95% unused)<br>depth 2.7 | 132,550 tok<br>(95% unused)<br>depth 2.0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 52 tok<br>(50% unused)<br>depth 1.0 | 242 tok<br>(51% unused)<br>depth 1.0 | 942 tok<br>(50% unused)<br>depth 1.0 | 2,351 tok<br>(50% unused)<br>depth 1.0 | 4,060 tok<br>(91% unused)<br>depth 1.0 | 22,356 tok<br>(93% unused)<br>depth 1.0 | 41,857 tok<br>(94% unused)<br>depth 1.0 |

*Token figures apportion the proxy's `tool_result_tokens` by the fraction of result bytes whose values never reach the answer; `ex-disc` uses the same denominator with DISCOVERY_TOOLS results dropped from the numerator, so the two are directly comparable. The approximation is confined to that ratio.*

*⚠️ **Unit caveat.** `tool_result_tokens` is the one token column here that is not Anthropic's own `usage` figure: the proxy counts it with `cl100k_base`, which is OpenAI's tokenizer, not Claude's. Cross-checked against per-call context growth over 429 consecutive-call pairs it runs **~15% low** (median implied/counted 1.18; 14–22% by condition, and the implied side also carries per-result message framing, so 15% is an upper bound on the tokenizer error). Every figure in this table is therefore a same-signed underestimate: the ratios between conditions hold, the absolute counts are conservative. A previous version of this footnote claimed these "share units with every other token column here"; they do not. See `grade.pass_through_tokens`.*


### Ranked by pass-through tokens — the metric caching cannot touch

The cost table above is inflated by the caching result and the inflation scales with call count, so it penalises many-call conditions as a measurement artifact. `pass_through_tokens` carries no such exposure. Where the two orderings disagree, this is the one to read first.

| rank | cell | mean pass-through | median cell | task cells |
|--:|---|--:|--:|--:|
| 1 | **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 10,266 | 2,351 | 7 |
| 2 | **M-R1-fat** — REST (one tool per endpoint), fat payloads | 42,037 | 14,649 | 7 |

*Both statistics are taken over task cells rather than over runs: three replicates of `M3@50` would otherwise outvote one of `M1@1` in a matrix whose point is the sweep. The mean is still weighted by N through the back door, which is why the median is beside it.*


## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **M-R1-fat** | 9 | 9 tools / 9,601 B | 5,028–5,311 | 512 | yes |
| **M-G2** | 7 | 7 tools / 4,040 B | 2,308–10,371 | 512 | yes |

## How to read these numbers

Every inference run goes through three phases. Understanding them explains why the token counts look the way they do.

**First cache write (Stage 1)** — Before Claude can act, the harness sends it a full description of every available tool. For the front-loaded conditions that's nine generated endpoint tools (M-R1) or seven frozen persisted operations (M-G2); for the on-demand pair it is three generic tools each (M-R2, M-G1). Measured `tools/list` sizes: 9,601 / 4,040 bytes front-loaded against 2,652 / 2,270 on-demand (capture/expected-tool-surfaces.json, which owns these numbers). Anthropic will cache that context, but only once the prompt clears the model's **minimum cacheable prefix** — which is model-dependent and not monotonic in model size (4,096 tokens on Haiku 4.5, 1,024 on Sonnet 5, 512 on Opus 5), so it cannot be inferred from the model name. Stage 1 captures the `cache_creation` charge for the first write that happens. **It is named for that event, not for schema loading**, and the two coincide only when the tool surface alone clears the minimum — see the prefix table above for whether it does here. When it does not, the first write fires several tool rounds in, once the *conversation* has grown past the threshold, and the tool surface is paid at the uncached `input_tokens` rate on every call until then. This section previously read "once it exceeds ~1 000 tokens" and attributed Stage 1 to schema size; ~1,000 is Sonnet's minimum, and the wrong threshold is what left the zero-cache-read finding without a mechanism.

**Context growth (Stage 2)** — Each tool call extends the conversation: the tool's response is appended and the *now-longer* context must be written to cache again so the next inference call can read it cheaply. Stage 2 sums those incremental `cache_creation` charges — the cost of *maintaining* the cache as it grows, not of using it. Two factors drive Stage 2 higher: more round trips (more re-writes) and larger payloads per round trip (more new tokens to cache each time). The REST conditions are penalised on both axes, and phase 2 is built to separate them: an agent-side join needs one call per record where a federated query needs one in total, and a `-fat` REST response carries every field whether or not the task asked for it (49,049 B against GraphQL's 1,683 B for the same twenty flights, §5.1). The `-lean` profile holds the call count fixed and removes the over-fetch, which is how the two effects are told apart. Stage 2 is where most of the REST–GraphQL cost difference accumulates.

**Inference compute (Stage 3)** — The cost of the model *reading and generating*, not writing. It has three components: `cache_read_input_tokens` (tokens pulled from the cache Stages 1–2 built — cheap but not free), `input_tokens` (any prompt tokens processed fresh, not from cache), and `output_tokens` (tokens Claude generates). Stage 3 is roughly constant across conditions for the same task, because the task prompt and final answer are similar in size regardless of which API protocol answered the question. It does not include cache-write charges — those are entirely in Stages 1 and 2.

The three stages are additive — total cost = Stage 1 + Stage 2 + Stage 3. **One cross-condition caveat:** no phase-2 condition's tool surface clears Haiku 4.5's 4,096-token cache minimum on its own — the prefixes run 1,491 to 4,053 — so in every cell the first cache write fires on conversation growth rather than on schema load. The Stage 1 / Stage 2 boundary therefore falls at a different *turn* in each condition, and a bigger Stage 1 here means the conversation was bigger when it crossed the threshold, not that the schema was. The Stage 1 + Stage 2 sum and Stage 3 are the reliable cross-condition comparators. The stage split is most useful within a single condition to understand how its cost is structured.


## Cost breakdown by prompt lifecycle stage

Each run's cost is split across the three stages of the inference prompt lifecycle. All values are **mean USD/run** across reps.


![Cost by stage and tool-response size per task](summary_charts.png)

| Condition | Task | Stage 1 — First cache write | Stage 2 — Context growth | Stage 3 — Inference compute | Total |
|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | $0.0276 | $0.0200 | $0.0096 | **$0.0572** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | $0.0102 | $0.0844 | $0.0192 | **$0.1139** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | $0.0112 | $0.3295 | $0.0483 | **$0.3889** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | $0.0130 | $0.8211 | $0.0976 | **$0.9317** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | $0.0073 | $0.3216 | $0.0856 | **$0.4146** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | $0.0103 | $1.6233 | $0.2962 | **$1.9298** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | $0.0135 | $2.8243 | $0.5426 | **$3.3804** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | $0.0090 | $0.0033 | $0.0072 | **$0.0195** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | $0.0102 | $0.0110 | $0.0156 | **$0.0368** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | $0.0111 | $0.0398 | $0.0428 | **$0.0937** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | $0.0112 | $0.0974 | $0.1153 | **$0.2238** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | $0.0073 | $0.0974 | $0.0677 | **$0.1724** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | $0.0112 | $0.4342 | $0.3063 | **$0.7518** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | $0.0135 | $0.9797 | $0.4933 | **$1.4865** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. No phase-2 tool surface clears Haiku 4.5's 4,096-token cache minimum (prefixes run 1,491–4,053), so in every cell the first write fires on conversation growth, not on schema load — several discovery or fan-out rounds in, at a different turn per condition. A larger Stage 1 here means a larger conversation at the crossing point. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-fable-5-1: input $10.0/1M out $50.0/1M cc $12.5/1M cr $0.25/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 3 | $0.0572 | $0.1717 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 3 | $0.1139 | $0.3417 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 3 | $0.3889 | $1.1668 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 3 | $0.9317 | $2.7952 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 3 | $0.4146 | $1.2437 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 3 | $1.9298 | $5.7893 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 3 | $3.3804 | $10.1412 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 3 | $0.0195 | $0.0585 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 3 | $0.0368 | $0.1105 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 3 | $0.0937 | $0.2812 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 3 | $0.2238 | $0.6715 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 3 | $0.1724 | $0.5172 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 3 | $0.7518 | $2.2553 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 3 | $1.4865 | $4.4595 |

**Grand total across all conditions/tasks/reps: $30.0033**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 7.3 ± 3.0s | 2.9 ± 0.4s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 10.6 ± 0.1s | 3.3 ± 0.9s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 17.3 ± 2.9s | 3.6 ± 0.2s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 27.3 ± 2.9s | 6.6 ± 2.6s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 24.0 ± 5.7s | 10.9 ± 3.8s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 39.0 ± 2.9s | 16.0 ± 0.6s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 95.6 ± 0.1s | 25.7 ± 0.3s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 10.6 ± 0.0s | 2.3 ± 0.0s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 10.6 ± 0.0s | 2.5 ± 0.1s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 20.6 ± 0.1s | 5.5 ± 2.2s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 30.6 ± 5.1s | 4.1 ± 0.3s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 20.6 ± 0.0s | 6.5 ± 0.3s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 47.3 ± 2.9s | 28.5 ± 0.4s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 92.3 ± 5.8s | 57.9 ± 7.6s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-fable-5-1`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-G2 | M1@1 | 1 | 2 | 34 | 4036 | $0.018 | 10.6s | 2.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 2 | 2 | 34 | 3817 | $0.020 | 10.6s | 2.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 3 | 2 | 34 | 3819 | $0.020 | 10.6s | 2.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 1 | 2 | 34 | 3911 | $0.092 | 20.7s | 6.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 2 | 2 | 34 | 3911 | $0.091 | 20.5s | 7.1s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 3 | 2 | 34 | 3909 | $0.099 | 20.6s | 3.0s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 1 | 2 | 34 | 3839 | $0.037 | 10.6s | 2.6s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 2 | 2 | 34 | 3838 | $0.037 | 10.6s | 2.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 3 | 2 | 34 | 3837 | $0.037 | 10.6s | 2.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 1 | 2 | 34 | 4060 | $0.220 | 30.5s | 4.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 2 | 2 | 34 | 4280 | $0.202 | 25.6s | 3.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 3 | 2 | 34 | 4280 | $0.249 | 35.7s | 3.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 1 | 8 | 196 | 56889 | $0.993 | 45.7s | 28.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 2 | 3 | 66 | 21979 | $0.628 | 45.6s | 28.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 3 | 3 | 66 | 21979 | $0.634 | 50.6s | 29.0s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 1 | 2 | 34 | 4047 | $0.171 | 20.6s | 6.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 2 | 2 | 34 | 4048 | $0.172 | 20.6s | 6.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 3 | 2 | 34 | 4049 | $0.175 | 20.6s | 6.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 1 | 3 | 66 | 14480 | $1.430 | 85.6s | 53.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 2 | 3 | 66 | 8336 | $1.509 | 95.7s | 53.1s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 3 | 4 | 98 | 65214 | $1.520 | 95.6s | 66.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 1 | 2 | 34 | 5028 | $0.091 | 5.5s | 2.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 2 | 2 | 34 | 9255 | $0.039 | 5.6s | 2.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 3 | 2 | 34 | 9257 | $0.041 | 10.7s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 1 | 2 | 34 | 9351 | $0.385 | 15.6s | 3.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 2 | 2 | 34 | 9352 | $0.388 | 20.7s | 3.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 3 | 2 | 34 | 9352 | $0.394 | 15.6s | 3.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 1 | 2 | 34 | 9276 | $0.113 | 10.5s | 2.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 2 | 2 | 34 | 9276 | $0.113 | 10.6s | 2.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 3 | 2 | 34 | 9276 | $0.116 | 10.6s | 4.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 1 | 2 | 34 | 9500 | $0.932 | 25.6s | 5.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 2 | 2 | 34 | 9501 | $0.932 | 25.6s | 5.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 3 | 2 | 34 | 9501 | $0.932 | 30.7s | 9.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 1 | 3 | 66 | 51296 | $1.433 | 40.7s | 16.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 2 | 10 | 232 | 211143 | $2.924 | 35.7s | 15.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 3 | 3 | 66 | 51084 | $1.432 | 40.7s | 15.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 1 | 3 | 66 | 24114 | $0.418 | 20.7s | 9.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 2 | 3 | 66 | 24115 | $0.416 | 20.6s | 8.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 3 | 3 | 66 | 24115 | $0.409 | 30.6s | 15.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 1 | 3 | 66 | 105353 | $3.367 | 95.6s | 26.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 2 | 3 | 66 | 105384 | $3.378 | 95.6s | 25.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 3 | 3 | 66 | 105357 | $3.396 | 95.7s | 25.5s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

