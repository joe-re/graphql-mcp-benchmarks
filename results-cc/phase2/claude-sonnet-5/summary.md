# Phase 2 Results — who performs the join

## Key Findings

- _Key findings skipped: this run covers a subset of the phase-2 matrix._

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (M-R1-fat / M-G2)


### Task M1@1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 103 ± 8 | 8,024 ± 2,481 | 3,839 ± 2,477 | 866 ± 1 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 105 ± 0 | 4,090 ± 126 | 1,066 ± 127 | 103 ± 0 |

### Task M1@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 2.3 ± 2.3 | 4.0 ± 0.0 | 445 ± 207 | 9,475 ± 1 | 8,092 ± 740 | 4,183 ± 277 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 290 ± 12 | 4,037 ± 2 | 1,795 ± 3 | 478 ± 0 |

### Task M1@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 1,178 ± 118 | 9,550 ± 1 | 27,345 ± 4 | 15,834 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.7 ± 0.6 | 4.0 ± 0.0 | 858 ± 28 | 4,110 ± 1 | 4,274 ± 87 | 1,884 ± 5 |

### Task M1@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 2.7 ± 0.6 | 1.7 ± 0.6 | 5.3 ± 1.2 | 2,356 ± 69 | 57,086 ± 41,039 | 89,330 ± 37,518 | 53,107 ± 22,602 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 1.0 ± 0.0 | 4.0 ± 0.0 | 1,766 ± 7 | 4,260 ± 0 | 8,929 ± 0 | 4,681 ± 0 |

### Task M3@5

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 3.0 ± 0.0 | 4.0 ± 0.0 | 6.0 ± 0.0 | 1,114 ± 37 | 24,105 ± 5 | 26,306 ± 3 | 15,582 ± 0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.7 ± 0.6 | 10.0 ± 0.0 | 5.3 ± 1.2 | 1,163 ± 31 | 9,875 ± 5,064 | 8,701 ± 51 | 4,465 ± 0 |

### Task M3@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 3.7 ± 0.6 | 4.7 ± 0.6 | 7.3 ± 1.2 | 3,168 ± 410 | 87,696 ± 31,483 | 98,497 ± 508 | 59,998 ± 60 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 3.0 ± 0.0 | 40.0 ± 0.0 | 6.0 ± 0.0 | 4,159 ± 61 | 30,244 ± 12 | 32,261 ± 10 | 17,831 ± 0 |

### Task M3@50

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 7.0 ± 3.5 | 11.0 ± 6.9 | 141,648 ± 106,264 | 27,524 ± 16,849 | 263,347 ± 183,631 | 348,524 ± 192,600 | 204,913 ± 112,649 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 3.0 ± 0.0 | 100 ± 0 | 6.0 ± 0.0 | 10,079 ± 48 | 65,789 ± 24 | 78,933 ± 33 | 44,461 ± 0 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 22.3 ± 4.2 | 25.7 ± 7.0 | 141,679 ± 106,265 | 35,888 ± 16,829 | 459,283 ± 230,460 | 601,933 ± 228,856 | 354,482 ± 135,132 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 16.7 ± 0.6 | 155 ± 1 | 33.3 ± 1.2 | 18,420 ± 64 | 122,405 ± 4,925 | 135,960 ± 233 | 73,903 ± 5 |

## Accuracy

`answer_f1` is field-level precision/recall against `tasks/expected.json`, whose `grading` block defines the rules per task. **coverage** is the fraction of the records the prompt asked about that the answer mentions at all — reported separately because a truncated answer can be perfectly accurate on what it does say.

| Condition | M1@1 f1 | M1@5 f1 | M1@20 f1 | M1@50 f1 | M3@5 f1 | M3@20 f1 | M3@50 f1 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.97 ± 0.02 | 0.99 ± 0.01 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.99 ± 0.01 |

**On grounding.** 42 of 42 finished run(s) are fact-verified: every fact the answer states was traced to a `tool_result` that entered the context before it, using the proxy's `tool_io.jsonl` sidecar. 0 failed that check. `answer_grounded` is never `True` by default, so a blank means unassessed, not passed.


## Join tax — pass-through tokens and forced serial depth

**pass-through** is tool-result tokens whose values never appear in the answer: payload the agent carried through its context and did not use. **depth** is the longest chain of calls where each consumed an identifier the previous one returned — ids the prompt supplied are excluded, so reading the instructions does not count as a dependency.

**disc** is the same measure over *schema and spec lookup* — search feeding describe. That serialization is real latency, but it is a property of the tool surface rather than of the join, and it exists only in the on-demand conditions. Folding it into `depth` would make the headline metric track tool packaging instead of who performs the join, so the two are reported side by side.

**ex-disc** applies the same reasoning to the token figure, and it is shown wherever it changes the number. Schema and OpenAPI text is ~100% pass-through by this definition — the agent reads an SDL fragment to write a query and quotes none of it back — so `pass-through` charges the on-demand conditions for finding their own way around, while `depth` explicitly does not. That disagreement was silent until it was measured; it is not small, and it does not favour the hypothesis. Both numbers are here because which one a reader wants is an editorial call: **pass-through** is every token carried, **ex-disc** is the join tax alone.

| Condition | M1@1 | M1@5 | M1@20 | M1@50 | M3@5 | M3@20 | M3@50 |
|---|---|---|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | 817 tok<br>(94% unused)<br>depth 1.0 | 3,934 tok<br>(94% unused)<br>depth 1.0 | 14,596 tok<br>(92% unused)<br>depth 1.0 | 49,011 tok<br>(92% unused)<br>depth 1.0 | 14,682 tok<br>(94% unused)<br>depth 2.0 | 56,778 tok<br>(95% unused)<br>depth 2.7 | 194,294 tok<br>(95% unused)<br>depth 3.0 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 52 tok<br>(50% unused)<br>depth 1.0 | 242 tok<br>(51% unused)<br>depth 1.0 | 945 tok<br>(50% unused)<br>depth 1.0 | 2,353 tok<br>(50% unused)<br>depth 1.0 | 4,047 tok<br>(91% unused)<br>depth 1.0 | 16,390 tok<br>(92% unused)<br>depth 1.0 | 40,215 tok<br>(90% unused)<br>depth 1.0 |

*Token figures apportion the proxy's `tool_result_tokens` by the fraction of result bytes whose values never reach the answer; `ex-disc` uses the same denominator with DISCOVERY_TOOLS results dropped from the numerator, so the two are directly comparable. The approximation is confined to that ratio.*

*⚠️ **Unit caveat.** `tool_result_tokens` is the one token column here that is not Anthropic's own `usage` figure: the proxy counts it with `cl100k_base`, which is OpenAI's tokenizer, not Claude's. Cross-checked against per-call context growth over 429 consecutive-call pairs it runs **~15% low** (median implied/counted 1.18; 14–22% by condition, and the implied side also carries per-result message framing, so 15% is an upper bound on the tokenizer error). Every figure in this table is therefore a same-signed underestimate: the ratios between conditions hold, the absolute counts are conservative. A previous version of this footnote claimed these "share units with every other token column here"; they do not. See `grade.pass_through_tokens`.*


### Ranked by pass-through tokens — the metric caching cannot touch

The cost table above is inflated by the caching result and the inflation scales with call count, so it penalises many-call conditions as a measurement artifact. `pass_through_tokens` carries no such exposure. Where the two orderings disagree, this is the one to read first.

| rank | cell | mean pass-through | median cell | task cells |
|--:|---|--:|--:|--:|
| 1 | **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 9,178 | 2,353 | 7 |
| 2 | **M-R1-fat** — REST (one tool per endpoint), fat payloads | 47,730 | 14,682 | 7 |

*Both statistics are taken over task cells rather than over runs: three replicates of `M3@50` would otherwise outvote one of `M1@1` in a matrix whose point is the sweep. The mean is still weighted by N through the back door, which is why the median is beside it.*


## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **M-R1-fat** | 9 | 9 tools / 9,601 B | 5,161–5,443 | 1,024 | yes |
| **M-G2** | 7 | 7 tools / 4,040 B | 2,440–2,722 | 1,024 | yes |

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
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | $0.0057 | $0.0039 | $0.0026 | **$0.0122** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | $0.0022 | $0.0180 | $0.0063 | **$0.0266** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | $0.0024 | $0.0660 | $0.0137 | **$0.0821** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | $0.0028 | $0.2206 | $0.0350 | **$0.2583** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | $0.0022 | $0.0636 | $0.0160 | **$0.0817** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | $0.0024 | $0.2438 | $0.0492 | **$0.2955** |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | $0.0029 | $0.8685 | $0.6112 | **$1.4825** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | $0.0020 | $0.0007 | $0.0019 | **$0.0045** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | $0.0022 | $0.0023 | $0.0037 | **$0.0082** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | $0.0024 | $0.0083 | $0.0094 | **$0.0201** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | $0.0028 | $0.0196 | $0.0185 | **$0.0408** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | $0.0022 | $0.0196 | $0.0136 | **$0.0354** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | $0.0024 | $0.0783 | $0.0477 | **$0.1283** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | $0.0029 | $0.1945 | $0.1140 | **$0.3113** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. No phase-2 tool surface clears Haiku 4.5's 4,096-token cache minimum (prefixes run 1,491–4,053), so in every cell the first write fires on conversation growth, not on schema load — several discovery or fan-out rounds in, at a different turn per condition. A larger Stage 1 here means a larger conversation at the crossing point. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-sonnet-5: input $2.0/1M out $10.0/1M cc $2.5/1M cr $0.2/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 3 | $0.0122 | $0.0367 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 3 | $0.0266 | $0.0797 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 3 | $0.0821 | $0.2462 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 3 | $0.2583 | $0.7749 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 3 | $0.0817 | $0.2452 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 3 | $0.2955 | $0.8864 |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 3 | $1.4825 | $4.4476 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 3 | $0.0045 | $0.0136 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 3 | $0.0082 | $0.0246 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 3 | $0.0201 | $0.0603 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 3 | $0.0408 | $0.1225 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 3 | $0.0354 | $0.1061 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 3 | $0.1283 | $0.3849 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 3 | $0.3113 | $0.9339 |

**Grand total across all conditions/tasks/reps: $8.3627**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@1 | 5.6 ± 0.0s | 1.5 ± 0.2s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@5 | 9.0 ± 2.8s | 3.1 ± 1.6s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@20 | 14.0 ± 2.8s | 2.7 ± 0.5s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M1@50 | 23.9 ± 2.8s | 7.6 ± 4.5s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@5 | 15.6 ± 5.0s | 6.5 ± 1.4s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@20 | 29.0 ± 5.7s | 13.7 ± 3.0s |
| **M-R1-fat** — REST (one tool per endpoint), fat payloads | M3@50 | 207 ± 120s | 181 ± 122s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@1 | 12.3 ± 2.9s | 2.7 ± 1.4s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@5 | 10.5 ± 0.1s | 2.2 ± 0.5s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@20 | 17.3 ± 2.9s | 3.6 ± 1.4s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M1@50 | 23.9 ± 2.9s | 3.4 ± 0.4s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@5 | 17.3 ± 2.9s | 5.6 ± 1.0s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@20 | 35.7 ± 0.1s | 17.4 ± 1.1s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M3@50 | 74.1 ± 2.7s | 39.6 ± 1.0s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-sonnet-5`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-G2 | M1@1 | 1 | 2 | 4 | 4236 | $0.004 | 10.6s | 1.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 2 | 2 | 4 | 4018 | $0.005 | 10.6s | 2.0s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@1 | 3 | 2 | 4 | 4017 | $0.005 | 15.6s | 4.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 1 | 2 | 4 | 4109 | $0.020 | 15.6s | 2.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 2 | 2 | 4 | 4110 | $0.020 | 20.6s | 5.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@20 | 3 | 2 | 4 | 4110 | $0.020 | 15.6s | 2.9s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 1 | 2 | 4 | 4035 | $0.008 | 10.6s | 2.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 2 | 2 | 4 | 4038 | $0.008 | 10.5s | 2.2s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@5 | 3 | 2 | 4 | 4037 | $0.008 | 10.5s | 1.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 1 | 2 | 4 | 4260 | $0.041 | 20.6s | 3.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 2 | 2 | 4 | 4260 | $0.041 | 25.6s | 3.1s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M1@50 | 3 | 2 | 4 | 4260 | $0.041 | 25.5s | 3.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 1 | 3 | 6 | 30240 | $0.128 | 35.7s | 16.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 2 | 3 | 6 | 30258 | $0.128 | 35.7s | 18.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@20 | 3 | 3 | 6 | 30234 | $0.129 | 35.6s | 16.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 1 | 2 | 4 | 4028 | $0.034 | 15.6s | 4.6s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 2 | 3 | 6 | 12798 | $0.036 | 20.6s | 6.6s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@5 | 3 | 3 | 6 | 12799 | $0.036 | 15.6s | 5.6s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 1 | 3 | 6 | 65810 | $0.312 | 75.6s | 40.4s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 2 | 3 | 6 | 65795 | $0.311 | 71.0s | 38.5s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M3@50 | 3 | 3 | 6 | 65763 | $0.311 | 75.7s | 40.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 1 | 2 | 4 | 5160 | $0.019 | 5.6s | 1.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 2 | 2 | 4 | 9457 | $0.009 | 5.6s | 1.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@1 | 3 | 2 | 4 | 9456 | $0.009 | 5.6s | 1.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 1 | 2 | 4 | 9551 | $0.083 | 15.6s | 3.2s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 2 | 2 | 4 | 9549 | $0.083 | 15.6s | 2.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 3 | 2 | 4 | 9550 | $0.081 | 10.7s | 2.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 1 | 2 | 4 | 9476 | $0.024 | 10.6s | 2.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 2 | 2 | 4 | 9475 | $0.031 | 10.6s | 4.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@5 | 3 | 2 | 4 | 9475 | $0.024 | 5.7s | 1.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 1 | 2 | 4 | 9698 | $0.192 | 20.6s | 3.2s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 2 | 3 | 6 | 80778 | $0.211 | 25.5s | 7.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@50 | 3 | 3 | 6 | 80782 | $0.372 | 25.5s | 12.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 1 | 3 | 6 | 51342 | $0.282 | 25.6s | 10.5s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 2 | 4 | 8 | 105894 | $0.303 | 35.6s | 16.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 3 | 4 | 8 | 105851 | $0.302 | 25.7s | 14.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 1 | 3 | 6 | 24109 | $0.082 | 15.6s | 6.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 2 | 3 | 6 | 24100 | $0.082 | 10.6s | 5.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@5 | 3 | 3 | 6 | 24106 | $0.082 | 20.6s | 7.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 1 | 5 | 80297 | 157327 | $0.958 | 130.7s | 102.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 2 | 5 | 80297 | 157328 | $0.969 | 145.6s | 119.8s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@50 | 3 | 11 | 264351 | 475386 | $2.521 | 345.9s | 322.1s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

