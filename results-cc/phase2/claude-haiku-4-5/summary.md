# Phase 2 Results — who performs the join

## Key Findings

- _Key findings skipped: this run covers a subset of the phase-2 matrix._

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (M-R1-fat / M-G2)


### Task M1@1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,010 ± 1 | 123 ± 10 | 0.0 ± 0.0 | 5,149 ± 6 | 890 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,295 ± 8 | 105 ± 11 | 0.0 ± 0.0 | 0.0 ± 0.0 | 126 ± 0 |

### Task M1@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,029 ± 2 | 255 ± 18 | 0.0 ± 0.0 | 8,937 ± 33 | 4,042 ± 10 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,784 ± 3 | 242 ± 2 | 0.0 ± 0.0 | 0.0 ± 0.0 | 501 ± 0 |

### Task M1@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,090 ± 1 | 714 ± 23 | 0.0 ± 0.0 | 23,072 ± 26 | 15,854 ± 10 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 2,118 ± 1 | 701 ± 12 | 0.0 ± 0.0 | 4,467 ± 1 | 1,901 ± 0 |

### Task M1@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 8.0 ± 0.0 | 1,606 ± 19 | 4,208 ± 1 | 51,456 ± 28 | 39,625 ± 10 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 2,242 ± 1 | 1,546 ± 62 | 0.0 ± 0.0 | 7,936 ± 1 | 4,704 ± 0 |

### Task M3@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 4.3 ± 0.6 | 25.0 ± 0.0 | 4,045 ± 4 | 2,042 ± 113 | 31,276 ± 8,239 | 26,358 ± 119 | 17,609 ± 11 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.7 ± 0.6 | 10.0 ± 0.0 | 2,059 ± 4 | 1,102 ± 71 | 4,457 ± 3,860 | 7,862 ± 61 | 4,504 ± 14 |

### Task M3@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 4.3 ± 0.6 | 29.0 ± 28.5 | 4,116 ± 4 | 4,709 ± 1,534 | 89,289 ± 24,480 | 79,209 ± 5,156 | 62,265 ± 2,474 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 3.0 ± 0.0 | 40.0 ± 0.0 | 2,136 ± 1 | 3,478 ± 148 | 19,189 ± 6 | 24,973 ± 14 | 17,878 ± 0 |

### Task M3@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 5.3 ± 0.6 | 4.7 ± 1.2 | 25.3 ± 4.0 | 3,803 ± 1,322 | 310,002 ± 101,366 | 165,800 ± 1,585 | 138,675 ± 1,197 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.7 ± 0.6 | 83.3 ± 28.9 | 2,285 ± 4 | 8,128 ± 537 | 29,878 ± 25,875 | 54,270 ± 8,177 | 41,555 ± 5,115 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 22.0 ± 1.0 | 62.7 ± 27.6 | 20,323 ± 4 | 13,252 ± 2,705 | 434,775 ± 94,615 | 359,980 ± 3,656 | 278,960 ± 1,390 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 16.3 ± 1.2 | 137 ± 29 | 19,918 ± 19 | 15,303 ± 692 | 53,524 ± 29,740 | 99,508 ± 8,254 | 71,169 ± 5,129 |

## Accuracy

`answer_f1` is field-level precision/recall against `tasks/expected.json`, whose `grading` block defines the rules per task. **coverage** is the fraction of the records the prompt asked about that the answer mentions at all — reported separately because a truncated answer can be perfectly accurate on what it does say.

| Condition | M1@1 f1 | M1@5 f1 | M1@20 f1 | M1@50 f1 | M3@5 f1 | M3@20 f1 | M3@50 f1 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.97 ± 0.06 | 0.63 ± 0.40 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.98 ± 0.03 | 0.84 ± 0.22 |

**On grounding.** 42 of 42 finished run(s) are fact-verified: every fact the answer states was traced to a `tool_result` that entered the context before it, using the proxy's `tool_io.jsonl` sidecar. 0 failed that check. `answer_grounded` is never `True` by default, so a blank means unassessed, not passed.


## Join tax — pass-through tokens and forced serial depth

**pass-through** is tool-result tokens whose values never appear in the answer: payload the agent carried through its context and did not use. **depth** is the longest chain of calls where each consumed an identifier the previous one returned — ids the prompt supplied are excluded, so reading the instructions does not count as a dependency.

**disc** is the same measure over *schema and spec lookup* — search feeding describe. That serialization is real latency, but it is a property of the tool surface rather than of the join, and it exists only in the on-demand conditions. Folding it into `depth` would make the headline metric track tool packaging instead of who performs the join, so the two are reported side by side.

**ex-disc** applies the same reasoning to the token figure, and it is shown wherever it changes the number. Schema and OpenAPI text is ~100% pass-through by this definition — the agent reads an SDL fragment to write a query and quotes none of it back — so `pass-through` charges the on-demand conditions for finding their own way around, while `depth` explicitly does not. That disagreement was silent until it was measured; it is not small, and it does not favour the hypothesis. Both numbers are here because which one a reader wants is an editorial call: **pass-through** is every token carried, **ex-disc** is the join tax alone.

| Condition | M1@1 | M1@5 | M1@20 | M1@50 | M3@5 | M3@20 | M3@50 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 835 tok<br>(94% unused)<br>depth 1.0 | 3,767 tok<br>(93% unused)<br>depth 1.0 | 14,659 tok<br>(92% unused)<br>depth 1.0 | 36,617 tok<br>(92% unused)<br>depth 1.0 | 16,283 tok<br>(92% unused)<br>depth 2.7 | 57,252 tok<br>(92% unused)<br>depth 2.3 | 132,342 tok<br>(95% unused)<br>depth 2.3 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 63 tok<br>(50% unused)<br>depth 1.0 | 253 tok<br>(51% unused)<br>depth 1.0 | 953 tok<br>(50% unused)<br>depth 1.0 | 2,368 tok<br>(50% unused)<br>depth 1.0 | 4,051 tok<br>(90% unused)<br>depth 1.0 | 16,269 tok<br>(91% unused)<br>depth 1.0 | 37,281 tok<br>(90% unused)<br>depth 1.0 |

*Token figures apportion the proxy's `tool_result_tokens` by the fraction of result bytes whose values never reach the answer; `ex-disc` uses the same denominator with DISCOVERY_TOOLS results dropped from the numerator, so the two are directly comparable. The approximation is confined to that ratio.*

*⚠️ **Unit caveat.** `tool_result_tokens` is the one token column here that is not Anthropic's own `usage` figure: the proxy counts it with `cl100k_base`, which is OpenAI's tokenizer, not Claude's. Cross-checked against per-call context growth over 429 consecutive-call pairs it runs **~15% low** (median implied/counted 1.18; 14–22% by condition, and the implied side also carries per-result message framing, so 15% is an upper bound on the tokenizer error). Every figure in this table is therefore a same-signed underestimate: the ratios between conditions hold, the absolute counts are conservative. A previous version of this footnote claimed these "share units with every other token column here"; they do not. See `grade.pass_through_tokens`.*


### Ranked by pass-through tokens — the metric caching cannot touch

The cost table above is inflated by the caching result and the inflation scales with call count, so it penalises many-call conditions as a measurement artifact. `pass_through_tokens` carries no such exposure. Where the two orderings disagree, this is the one to read first.

| rank | cell | mean pass-through | median cell | task cells |
|--:|---|--:|--:|--:|
| 1 | **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 8,748 | 2,368 | 7 |
| 2 | **M-R1-fat** — REST (one tool per endpoint), fat payloads | 37,393 | 16,283 | 7 |

*Both statistics are taken over task cells rather than over runs: three replicates of `M3@50` would otherwise outvote one of `M1@1` in a matrix whose point is the sweep. The mean is still weighted by N through the back door, which is why the median is beside it.*


## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **M-R1-fat** | 9 | 9 tools / 9,601 B | 4,005–4,246 | 4,096 | partly — 8 of 21 runs |
| **M-G2** | 7 | 7 tools / 4,040 B | 2,033–2,273 | 4,096 | **no** — every prefix is below the minimum |

**34 of 42 runs carry a prefix below their model's cache minimum (M-R1-fat, M-G2), so in those runs the tool surface is never written to cache at all.** Their first `cache_creation` charge fires when the *conversation* crosses the minimum, several tool rounds in — which is why Stage 1 below is labelled for that event and not for schema loading. Where a surface does clear the minimum on its own, a fatter one really does buy a bigger Stage 1; where it does not, it buys a bigger uncached `input_tokens` bill on every call until the conversation grows past the threshold. The two are not the same cost and the Stage 1 column does not distinguish them — this table is how you tell which one a row is.


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
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | $0.0064 | $0.0000 | $0.0046 | **$0.0111** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | $0.0112 | $0.0000 | $0.0053 | **$0.0165** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | $0.0288 | $0.0000 | $0.0077 | **$0.0365** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | $0.0053 | $0.0591 | $0.0085 | **$0.0728** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | $0.0122 | $0.0208 | $0.0174 | **$0.0503** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | $0.0319 | $0.0671 | $0.0366 | **$0.1356** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | $0.0053 | $0.2019 | $0.0500 | **$0.2573** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | $0.0000 | $0.0000 | $0.0048 | **$0.0048** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | $0.0000 | $0.0000 | $0.0060 | **$0.0060** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | $0.0056 | $0.0000 | $0.0056 | **$0.0112** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | $0.0099 | $0.0000 | $0.0100 | **$0.0199** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | $0.0088 | $0.0010 | $0.0080 | **$0.0178** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | $0.0240 | $0.0072 | $0.0214 | **$0.0527** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | $0.0560 | $0.0118 | $0.0459 | **$0.1138** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. No phase-2 tool surface clears Haiku 4.5's 4,096-token cache minimum (prefixes run 1,491–4,053), so in every cell the first write fires on conversation growth, not on schema load — several discovery or fan-out rounds in, at a different turn per condition. A larger Stage 1 here means a larger conversation at the crossing point. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-haiku-4-5-20251001: input $1.0/1M out $5.0/1M cc $1.25/1M cr $0.1/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 3 | $0.0111 | $0.0332 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 3 | $0.0165 | $0.0494 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 3 | $0.0365 | $0.1095 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 3 | $0.0728 | $0.2183 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 3 | $0.0503 | $0.1510 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 3 | $0.1356 | $0.4068 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 3 | $0.2573 | $0.7719 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 3 | $0.0048 | $0.0145 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 3 | $0.0060 | $0.0180 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 3 | $0.0112 | $0.0336 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 3 | $0.0199 | $0.0597 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 3 | $0.0178 | $0.0535 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 3 | $0.0527 | $0.1580 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 3 | $0.1138 | $0.3413 |

**Grand total across all conditions/tasks/reps: $2.4186**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 5.6 ± 0.0s | 1.5 ± 0.0s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 5.6 ± 0.0s | 1.7 ± 0.3s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 12.2 ± 2.9s | 3.7 ± 1.9s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 20.6 ± 0.0s | 3.0 ± 0.3s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 22.2 ± 2.8s | 13.1 ± 2.2s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 43.9 ± 12.6s | 22.5 ± 11.9s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 37.3 ± 5.8s | 16.6 ± 3.8s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 10.6 ± 0.0s | 1.2 ± 0.1s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 10.6 ± 0.1s | 1.4 ± 0.1s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 15.6 ± 0.0s | 1.9 ± 0.3s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 22.3 ± 2.9s | 2.8 ± 0.4s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 17.2 ± 2.9s | 4.9 ± 0.6s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 32.3 ± 2.9s | 13.3 ± 2.3s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 60.6 ± 8.6s | 22.2 ± 4.3s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-haiku-4-5-20251001`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-G2 | M1@1 | 1 | 2 | 4290 | 0 | $0.005 | 10.6s | 1.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 2 | 2 | 4290 | 0 | $0.005 | 10.6s | 1.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 3 | 2 | 4304 | 0 | $0.005 | 10.6s | 1.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 1 | 2 | 2117 | 0 | $0.011 | 15.6s | 1.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 2 | 2 | 2118 | 0 | $0.011 | 15.6s | 2.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 3 | 2 | 2118 | 0 | $0.011 | 15.6s | 1.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 1 | 2 | 4781 | 0 | $0.006 | 10.6s | 1.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 2 | 2 | 4783 | 0 | $0.006 | 10.6s | 1.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 3 | 2 | 4787 | 0 | $0.006 | 10.7s | 1.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 1 | 2 | 2241 | 0 | $0.020 | 20.6s | 2.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 2 | 2 | 2243 | 0 | $0.020 | 25.7s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 3 | 2 | 2243 | 0 | $0.020 | 20.6s | 2.6s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 1 | 3 | 2137 | 19183 | $0.052 | 30.6s | 11.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 2 | 3 | 2135 | 19190 | $0.053 | 35.7s | 15.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 3 | 3 | 2137 | 19194 | $0.053 | 30.6s | 12.0s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 1 | 2 | 2054 | 0 | $0.017 | 15.6s | 4.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 2 | 3 | 2061 | 6689 | $0.018 | 20.6s | 5.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 3 | 3 | 2061 | 6681 | $0.018 | 15.5s | 4.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 1 | 2 | 2280 | 0 | $0.096 | 70.6s | 17.3s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 2 | 3 | 2287 | 44820 | $0.124 | 55.6s | 24.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 3 | 3 | 2287 | 44814 | $0.121 | 55.7s | 24.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 1 | 2 | 4010 | 0 | $0.011 | 5.6s | 1.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 2 | 2 | 4011 | 0 | $0.011 | 5.6s | 1.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 3 | 2 | 4010 | 0 | $0.011 | 5.6s | 1.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 1 | 2 | 4090 | 0 | $0.036 | 15.6s | 5.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 2 | 2 | 4091 | 0 | $0.036 | 10.6s | 2.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 3 | 2 | 4089 | 0 | $0.037 | 10.5s | 2.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 1 | 2 | 4027 | 0 | $0.016 | 5.6s | 1.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 2 | 2 | 4029 | 0 | $0.017 | 5.6s | 1.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 3 | 2 | 4030 | 0 | $0.017 | 5.6s | 1.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 1 | 2 | 8 | 4207 | $0.073 | 20.6s | 2.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 2 | 2 | 8 | 4208 | $0.073 | 20.6s | 3.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 3 | 2 | 8 | 4208 | $0.073 | 20.6s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 1 | 4 | 4113 | 70098 | $0.121 | 30.6s | 10.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 2 | 4 | 4114 | 80911 | $0.133 | 45.6s | 22.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 3 | 5 | 4121 | 116858 | $0.153 | 55.6s | 34.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 1 | 5 | 4049 | 40790 | $0.052 | 25.5s | 15.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 2 | 4 | 4043 | 26544 | $0.049 | 20.6s | 12.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 3 | 4 | 4042 | 26495 | $0.050 | 20.6s | 11.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 1 | 6 | 30 | 427048 | $0.264 | 30.6s | 21.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 2 | 5 | 23 | 251932 | $0.254 | 40.6s | 14.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 3 | 5 | 23 | 251025 | $0.254 | 40.7s | 14.5s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

