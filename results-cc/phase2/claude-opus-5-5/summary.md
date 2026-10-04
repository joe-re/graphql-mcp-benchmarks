# Phase 2 Results — who performs the join

## Key Findings

- _Key findings skipped: this run covers a subset of the phase-2 matrix._

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (M-R1-fat / M-G2)


### Task M1@1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 167 ± 11 | 7,848 ± 2,442 | 3,811 ± 2,441 | 888 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 132 ± 1 | 3,891 ± 126 | 987 ± 127 | 103 ± 0 |

### Task M1@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 364 ± 40 | 9,277 ± 1 | 7,583 ± 1 | 4,030 ± 1 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 366 ± 43 | 3,839 ± 1 | 1,699 ± 1 | 478 ± 0 |

### Task M1@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 863 ± 70 | 9,351 ± 2 | 27,256 ± 6 | 15,838 ± 2 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 883 ± 45 | 3,912 ± 1 | 4,074 ± 1 | 1,878 ± 0 |

### Task M1@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 1,892 ± 3 | 9,500 ± 1 | 66,690 ± 5 | 39,609 ± 2 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 2,031 ± 44 | 4,061 ± 2 | 8,830 ± 2 | 4,681 ± 0 |

### Task M3@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 3.0 ± 0.0 | 4.0 ± 0.0 | 6.0 ± 0.0 | 1,199 ± 23 | 23,854 ± 3 | 26,277 ± 1 | 15,608 ± 1 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 10.0 ± 0.0 | 4.0 ± 0.0 | 1,216 ± 14 | 3,829 ± 1 | 8,532 ± 1 | 4,465 ± 0 |

### Task M3@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 3.0 ± 0.0 | 4.0 ± 0.0 | 6.0 ± 0.0 | 2,575 ± 130 | 51,022 ± 2 | 97,879 ± 146 | 59,938 ± 2 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 5.3 ± 0.6 | 40.0 ± 0.0 | 10.7 ± 1.2 | 3,590 ± 60 | 49,372 ± 11,426 | 32,617 ± 145 | 17,831 ± 0 |

### Task M3@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 4.0 ± 0.0 | 4.3 ± 0.6 | 91,605 ± 1 | 9,274 ± 806 | 19,297 ± 2 | 230,250 ± 263 | 139,565 ± 54 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 9.7 ± 0.6 | 100 ± 0 | 19.3 ± 1.2 | 8,369 ± 244 | 276,862 ± 35,330 | 80,273 ± 151 | 44,461 ± 0 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 18.0 ± 0.0 | 16.3 ± 0.6 | 91,633 ± 1 | 16,333 ± 855 | 130,148 ± 2,438 | 459,746 ± 2,834 | 275,476 ± 57 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 25.0 ± 1.0 | 154 ± 0 | 50.0 ± 2.0 | 16,586 ± 276 | 345,766 ± 42,206 | 137,012 ± 262 | 73,897 ± 0 |

## Accuracy

`answer_f1` is field-level precision/recall against `tasks/expected.json`, whose `grading` block defines the rules per task. **coverage** is the fraction of the records the prompt asked about that the answer mentions at all — reported separately because a truncated answer can be perfectly accurate on what it does say.

| Condition | M1@1 f1 | M1@5 f1 | M1@20 f1 | M1@50 f1 | M3@5 f1 | M3@20 f1 | M3@50 f1 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.99 ± 0.01 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.01 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |

**On grounding.** 42 of 42 finished run(s) are fact-verified: every fact the answer states was traced to a `tool_result` that entered the context before it, using the proxy's `tool_io.jsonl` sidecar. 0 failed that check. `answer_grounded` is never `True` by default, so a blank means unassessed, not passed.


## Join tax — pass-through tokens and forced serial depth

**pass-through** is tool-result tokens whose values never appear in the answer: payload the agent carried through its context and did not use. **depth** is the longest chain of calls where each consumed an identifier the previous one returned — ids the prompt supplied are excluded, so reading the instructions does not count as a dependency.

**disc** is the same measure over *schema and spec lookup* — search feeding describe. That serialization is real latency, but it is a property of the tool surface rather than of the join, and it exists only in the on-demand conditions. Folding it into `depth` would make the headline metric track tool packaging instead of who performs the join, so the two are reported side by side.

**ex-disc** applies the same reasoning to the token figure, and it is shown wherever it changes the number. Schema and OpenAPI text is ~100% pass-through by this definition — the agent reads an SDL fragment to write a query and quotes none of it back — so `pass-through` charges the on-demand conditions for finding their own way around, while `depth` explicitly does not. That disagreement was silent until it was measured; it is not small, and it does not favour the hypothesis. Both numbers are here because which one a reader wants is an editorial call: **pass-through** is every token carried, **ex-disc** is the join tax alone.

| Condition | M1@1 | M1@5 | M1@20 | M1@50 | M3@5 | M3@20 | M3@50 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 815 tok<br>(92% unused)<br>depth 1.0 | 3,732 tok<br>(93% unused)<br>depth 1.0 | 14,647 tok<br>(92% unused)<br>depth 1.0 | 36,594 tok<br>(92% unused)<br>depth 1.0 | 14,850 tok<br>(95% unused)<br>depth 2.0 | 57,547 tok<br>(96% unused)<br>depth 2.0 | 133,619 tok<br>(96% unused)<br>depth 2.0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 37 tok<br>(35% unused)<br>depth 1.0 | 228 tok<br>(48% unused)<br>depth 1.0 | 923 tok<br>(49% unused)<br>depth 1.0 | 2,287 tok<br>(49% unused)<br>depth 1.0 | 4,060 tok<br>(91% unused)<br>depth 1.0 | 16,643 tok<br>(93% unused)<br>depth 1.0 | 42,976 tok<br>(97% unused)<br>depth 1.0 |

*Token figures apportion the proxy's `tool_result_tokens` by the fraction of result bytes whose values never reach the answer; `ex-disc` uses the same denominator with DISCOVERY_TOOLS results dropped from the numerator, so the two are directly comparable. The approximation is confined to that ratio.*

*⚠️ **Unit caveat.** `tool_result_tokens` is the one token column here that is not Anthropic's own `usage` figure: the proxy counts it with `cl100k_base`, which is OpenAI's tokenizer, not Claude's. Cross-checked against per-call context growth over 429 consecutive-call pairs it runs **~15% low** (median implied/counted 1.18; 14–22% by condition, and the implied side also carries per-result message framing, so 15% is an upper bound on the tokenizer error). Every figure in this table is therefore a same-signed underestimate: the ratios between conditions hold, the absolute counts are conservative. A previous version of this footnote claimed these "share units with every other token column here"; they do not. See `grade.pass_through_tokens`.*


### Ranked by pass-through tokens — the metric caching cannot touch

The cost table above is inflated by the caching result and the inflation scales with call count, so it penalises many-call conditions as a measurement artifact. `pass_through_tokens` carries no such exposure. Where the two orderings disagree, this is the one to read first.

| rank | cell | mean pass-through | median cell | task cells |
|--:|---|--:|--:|--:|
| 1 | **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 9,593 | 2,287 | 7 |
| 2 | **M-R1-fat** — REST (one tool per endpoint), fat payloads | 37,401 | 14,850 | 7 |

*Both statistics are taken over task cells rather than over runs: three replicates of `M3@50` would otherwise outvote one of `M1@1` in a matrix whose point is the sweep. The mean is still weighted by N through the back door, which is why the median is beside it.*


## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **M-R1-fat** | 9 | 9 tools / 9,601 B | 5,030–5,312 | 512 | yes |
| **M-G2** | 7 | 7 tools / 4,040 B | 2,309–2,590 | 512 | yes |

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
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | $0.0110 | $0.0080 | $0.0049 | **$0.0240** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | $0.0041 | $0.0338 | $0.0092 | **$0.0471** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | $0.0045 | $0.1318 | $0.0191 | **$0.1554** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | $0.0052 | $0.3282 | $0.0398 | **$0.3732** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | $0.0040 | $0.1273 | $0.0288 | **$0.1602** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | $0.0045 | $0.4849 | $0.0617 | **$0.5511** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | $0.0054 | $1.1459 | $0.5558 | **$1.7070** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | $0.0036 | $0.0013 | $0.0034 | **$0.0084** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | $0.0041 | $0.0044 | $0.0081 | **$0.0166** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | $0.0045 | $0.0159 | $0.0185 | **$0.0388** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | $0.0052 | $0.0390 | $0.0414 | **$0.0856** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | $0.0040 | $0.0386 | $0.0251 | **$0.0678** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | $0.0045 | $0.1586 | $0.0817 | **$0.2448** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | $0.0054 | $0.3960 | $0.2228 | **$0.6242** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. No phase-2 tool surface clears Haiku 4.5's 4,096-token cache minimum (prefixes run 1,491–4,053), so in every cell the first write fires on conversation growth, not on schema load — several discovery or fan-out rounds in, at a different turn per condition. A larger Stage 1 here means a larger conversation at the crossing point. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-opus-5-5: input $4.0/1M out $20.0/1M cc $5.0/1M cr $0.2/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 3 | $0.0240 | $0.0719 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 3 | $0.0471 | $0.1412 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 3 | $0.1554 | $0.4663 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 3 | $0.3732 | $1.1196 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 3 | $0.1602 | $0.4805 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 3 | $0.5511 | $1.6534 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 3 | $1.7070 | $5.1210 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 3 | $0.0084 | $0.0251 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 3 | $0.0166 | $0.0498 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 3 | $0.0388 | $0.1165 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 3 | $0.0856 | $0.2568 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 3 | $0.0678 | $0.2033 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 3 | $0.2448 | $0.7344 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 3 | $0.6242 | $1.8726 |

**Grand total across all conditions/tasks/reps: $12.3122**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 10.6 ± 0.1s | 3.3 ± 0.3s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 10.6 ± 0.1s | 3.5 ± 0.6s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 17.3 ± 2.9s | 3.6 ± 0.6s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 23.9 ± 2.9s | 4.8 ± 0.7s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 20.6 ± 0.1s | 9.2 ± 1.2s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 32.3 ± 2.9s | 14.0 ± 1.1s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 87.3 ± 10.4s | 52.1 ± 6.0s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 15.6 ± 0.0s | 4.0 ± 1.1s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 15.6 ± 0.0s | 3.0 ± 0.2s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 17.2 ± 2.8s | 3.3 ± 0.0s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 25.5 ± 0.1s | 4.4 ± 0.2s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 20.6 ± 0.1s | 7.2 ± 0.8s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 45.6 ± 5.0s | 28.4 ± 1.5s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 90.6 ± 0.1s | 74.0 ± 2.3s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-opus-5-5`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-G2 | M1@1 | 1 | 2 | 4 | 4037 | $0.008 | 15.6s | 2.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 2 | 2 | 4 | 3818 | $0.009 | 15.6s | 4.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 3 | 2 | 4 | 3819 | $0.009 | 15.6s | 4.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 1 | 2 | 4 | 3912 | $0.038 | 15.6s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 2 | 2 | 4 | 3912 | $0.040 | 15.6s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 3 | 2 | 4 | 3913 | $0.039 | 20.5s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 1 | 2 | 4 | 3839 | $0.017 | 15.6s | 2.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 2 | 2 | 4 | 3839 | $0.016 | 15.6s | 3.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 3 | 2 | 4 | 3838 | $0.017 | 15.6s | 2.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 1 | 2 | 4 | 4062 | $0.086 | 25.5s | 4.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 2 | 2 | 4 | 4061 | $0.085 | 25.6s | 4.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 3 | 2 | 4 | 4059 | $0.086 | 25.5s | 4.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 1 | 5 | 10 | 42782 | $0.242 | 40.7s | 26.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 2 | 5 | 10 | 42768 | $0.244 | 45.6s | 28.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 3 | 6 | 12 | 62565 | $0.249 | 50.6s | 29.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 1 | 2 | 4 | 3830 | $0.068 | 20.7s | 7.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 2 | 2 | 4 | 3828 | $0.068 | 20.6s | 6.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 3 | 2 | 4 | 3829 | $0.068 | 20.6s | 7.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 1 | 10 | 20 | 297494 | $0.628 | 90.7s | 76.0s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 2 | 9 | 18 | 236067 | $0.611 | 90.6s | 74.6s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 3 | 10 | 20 | 297025 | $0.634 | 90.6s | 71.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 1 | 2 | 4 | 5028 | $0.037 | 10.6s | 3.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 2 | 2 | 4 | 9258 | $0.017 | 10.5s | 3.2s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 3 | 2 | 4 | 9258 | $0.017 | 10.6s | 3.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 1 | 2 | 4 | 9352 | $0.156 | 20.6s | 3.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 2 | 2 | 4 | 9351 | $0.154 | 15.6s | 4.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 3 | 2 | 4 | 9349 | $0.157 | 15.6s | 3.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 1 | 2 | 4 | 9277 | $0.047 | 10.5s | 4.2s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 2 | 2 | 4 | 9278 | $0.046 | 10.6s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 3 | 2 | 4 | 9276 | $0.048 | 10.6s | 3.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 1 | 2 | 4 | 9501 | $0.373 | 20.6s | 4.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 2 | 2 | 4 | 9500 | $0.373 | 25.6s | 5.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 3 | 2 | 4 | 9499 | $0.373 | 25.6s | 5.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 1 | 3 | 6 | 51023 | $0.555 | 35.7s | 15.2s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 2 | 3 | 6 | 51023 | $0.550 | 30.6s | 13.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 3 | 3 | 6 | 51019 | $0.549 | 30.7s | 13.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 1 | 3 | 6 | 23852 | $0.160 | 20.6s | 9.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 2 | 3 | 6 | 23852 | $0.161 | 20.6s | 10.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 3 | 3 | 6 | 23857 | $0.160 | 20.7s | 8.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 1 | 4 | 91606 | 19300 | $1.705 | 90.6s | 53.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 2 | 4 | 91604 | 19296 | $1.692 | 75.6s | 45.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 3 | 4 | 91605 | 19296 | $1.723 | 95.6s | 57.3s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

