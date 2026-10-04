# Phase 2 Results — who performs the join

## Key Findings

- **Accuracy is not where the difference lives.** 18 of 18 graded runs scored a perfect f1. 18 of 18 passed the grounding check. That check asks whether each *correct* value an answer states appears in the tool results that arrived — retrieval-happened, not per-fact provenance, so a run that flips a verdict scores f1 0.00 and still passes it. It does not license "nothing was fabricated". The widest protocol gap is **M2@1: GraphQL 1.00 against REST 1.00** — and 6 of 6 condition/task cells are perfect outright, so most of the matrix shows no accuracy difference at all. The agents get the answer either way. What differs is what it costs to get it, which is why this report leads with payload and calls rather than correctness.

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (M-R1-lean / M-G2 / M-G3)


### Task M1@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | 2.0 ± 0.0 | 7.3 ± 11.0 | 4.0 ± 0.0 | 1,431 ± 1,025 | 8,333 ± 2,669 | 7,652 ± 2,691 | 2,578 ± 1,037 |

### Task M2@1

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | 3.0 ± 0.0 | 5.0 ± 0.0 | 6.0 ± 0.0 | 556 ± 57 | 17,835 ± 378 | 7,119 ± 1,214 | 3,454 ± 659 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 2.0 ± 0.0 | 4.0 ± 0.0 | 327 ± 32 | 3,192 ± 1,020 | 3,745 ± 834 | 884 ± 0 |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | 9.3 ± 1.5 | 8.3 ± 1.5 | 18.7 ± 3.1 | 1,494 ± 168 | 43,876 ± 9,479 | 8,436 ± 799 | 2,768 ± 449 |

### Task M3@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | 3.7 ± 0.6 | 4.7 ± 0.6 | 7.3 ± 1.2 | 2,990 ± 377 | 31,005 ± 2,947 | 29,241 ± 1,820 | 17,631 ± 1,406 |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | 6.7 ± 0.6 | 6.0 ± 0.0 | 13.3 ± 1.2 | 2,548 ± 62 | 26,625 ± 2,136 | 13,056 ± 42 | 5,877 ± 126 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | 8.7 ± 0.6 | 17.0 ± 10.4 | 17.3 ± 1.2 | 4,977 ± 854 | 57,173 ± 3,425 | 44,012 ± 4,235 | 23,663 ± 2,831 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 2.0 ± 0.0 | 2.0 ± 0.0 | 4.0 ± 0.0 | 327 ± 32 | 3,192 ± 1,020 | 3,745 ± 834 | 884 ± 0 |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | 16.0 ± 1.0 | 14.3 ± 1.5 | 32.0 ± 2.0 | 4,042 ± 179 | 70,501 ± 8,011 | 21,491 ± 799 | 8,644 ± 548 |

## Accuracy

`answer_f1` is field-level precision/recall against `tasks/expected.json`, whose `grading` block defines the rules per task. **coverage** is the fraction of the records the prompt asked about that the answer mentions at all — reported separately because a truncated answer can be perfectly accurate on what it does say.

| Condition | M1@20 f1 | M2@1 f1 | M3@20 f1 |
|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | — | 1.00 ± 0.00 | — |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | — | 1.00 ± 0.00 | 1.00 ± 0.00 |

**On grounding.** 18 of 18 finished run(s) are fact-verified: every fact the answer states was traced to a `tool_result` that entered the context before it, using the proxy's `tool_io.jsonl` sidecar. 0 failed that check. `answer_grounded` is never `True` by default, so a blank means unassessed, not passed.


## Join tax — pass-through tokens and forced serial depth

**pass-through** is tool-result tokens whose values never appear in the answer: payload the agent carried through its context and did not use. **depth** is the longest chain of calls where each consumed an identifier the previous one returned — ids the prompt supplied are excluded, so reading the instructions does not count as a dependency.

**disc** is the same measure over *schema and spec lookup* — search feeding describe. That serialization is real latency, but it is a property of the tool surface rather than of the join, and it exists only in the on-demand conditions. Folding it into `depth` would make the headline metric track tool packaging instead of who performs the join, so the two are reported side by side.

**ex-disc** applies the same reasoning to the token figure, and it is shown wherever it changes the number. Schema and OpenAPI text is ~100% pass-through by this definition — the agent reads an SDL fragment to write a query and quotes none of it back — so `pass-through` charges the on-demand conditions for finding their own way around, while `depth` explicitly does not. That disagreement was silent until it was measured; it is not small, and it does not favour the hypothesis. Both numbers are here because which one a reader wants is an editorial call: **pass-through** is every token carried, **ex-disc** is the join tax alone.

| Condition | M1@20 | M2@1 | M3@20 |
|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | 1,697 tok<br>(63% unused)<br>depth 1.0 | 3,294 tok<br>(95% unused)<br>depth 2.0 | 14,887 tok<br>(84% unused)<br>depth 2.7 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | — | 835 tok<br>(94% unused)<br>depth 1.0 | — |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | — | 2,728 tok<br>(99% unused)<br>ex-disc 120 tok<br>depth 1.0 | 5,049 tok<br>(86% unused)<br>ex-disc 2,051 tok<br>depth 1.0 |

*Token figures apportion the proxy's `tool_result_tokens` by the fraction of result bytes whose values never reach the answer; `ex-disc` uses the same denominator with DISCOVERY_TOOLS results dropped from the numerator, so the two are directly comparable. The approximation is confined to that ratio.*

*⚠️ **Unit caveat.** `tool_result_tokens` is the one token column here that is not Anthropic's own `usage` figure: the proxy counts it with `cl100k_base`, which is OpenAI's tokenizer, not Claude's. Cross-checked against per-call context growth over 429 consecutive-call pairs it runs **~15% low** (median implied/counted 1.18; 14–22% by condition, and the implied side also carries per-result message framing, so 15% is an upper bound on the tokenizer error). Every figure in this table is therefore a same-signed underestimate: the ratios between conditions hold, the absolute counts are conservative. A previous version of this footnote claimed these "share units with every other token column here"; they do not. See `grade.pass_through_tokens`.*


### Ranked by pass-through tokens — the metric caching cannot touch

The cost table above is inflated by the caching result and the inflation scales with call count, so it penalises many-call conditions as a measurement artifact. `pass_through_tokens` carries no such exposure. Where the two orderings disagree, this is the one to read first.

| rank | cell | mean pass-through | median cell | task cells |
|--:|---|--:|--:|--:|
| 1 | **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | 835 | 835 | 1 |
| 2 | **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | 3,888 | 3,888 | 2 |
| 3 | **M-R1-lean** — REST (one tool per endpoint), lean payloads | 6,626 | 3,294 | 3 |

*Both statistics are taken over task cells rather than over runs: three replicates of `M3@50` would otherwise outvote one of `M1@1` in a matrix whose point is the sweep. The mean is still weighted by N through the back door, which is why the median is beside it.*


## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **M-R1-lean** | 9 | 9 tools / 9,601 B | 5,172–5,585 | 1,024 | yes |
| **M-G2** | 7 | 7 tools / 4,040 B | 2,450–2,778 | 1,024 | yes |
| **M-G3** | 3 | 3 tools / 1,940 B | 1,865–2,280 | 1,024 | yes |

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
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M1@20 | $0.0065 | $0.0126 | $0.0160 | **$0.0351** |
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M2@1 | $0.0027 | $0.0151 | $0.0091 | **$0.0269** |
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M3@20 | $0.0029 | $0.0702 | $0.0361 | **$0.1092** |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M2@1 | $0.0053 | $0.0040 | $0.0039 | **$0.0133** |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | M2@1 | $0.0052 | $0.0159 | $0.0237 | **$0.0448** |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | M3@20 | $0.0054 | $0.0272 | $0.0308 | **$0.0635** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. No phase-2 tool surface clears Haiku 4.5's 4,096-token cache minimum (prefixes run 1,491–4,053), so in every cell the first write fires on conversation growth, not on schema load — several discovery or fan-out rounds in, at a different turn per condition. A larger Stage 1 here means a larger conversation at the crossing point. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-sonnet-5: input $2.0/1M out $10.0/1M cc $2.5/1M cr $0.2/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M1@20 | 3 | $0.0351 | $0.1053 |
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M2@1 | 3 | $0.0269 | $0.0808 |
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M3@20 | 3 | $0.1092 | $0.3277 |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M2@1 | 3 | $0.0133 | $0.0398 |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | M2@1 | 3 | $0.0448 | $0.1345 |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | M3@20 | 3 | $0.0635 | $0.1904 |

**Grand total across all conditions/tasks/reps: $0.8786**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M1@20 | 14.0 ± 5.7s | 6.3 ± 5.8s |
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M2@1 | 14.0 ± 2.9s | 7.7 ± 1.8s |
| **M-R1-lean** — REST (one tool per endpoint), lean payloads | M3@20 | 29.0 ± 2.9s | 12.9 ± 3.1s |
| **M-G2** — GraphQL (frozen persisted operations, Apollo MCP) | M2@1 | 12.2 ± 2.9s | 2.8 ± 1.0s |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | M2@1 | 37.3 ± 12.6s | 24.3 ± 8.0s |
| **M-G3** — GraphQL (search + validate + execute, Apollo MCP) | M3@20 | 39.0 ± 7.6s | 20.7 ± 6.6s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-sonnet-5`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-G2 | M2@1 | 1 | 2 | 4 | 2448 | $0.014 | 10.5s | 1.8s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M2@1 | 2 | 2 | 4 | 2774 | $0.015 | 15.6s | 3.7s | 0 | 0 | 0 | yes | 0 |
| M-G2 | M2@1 | 3 | 2 | 4 | 4355 | $0.011 | 10.6s | 2.8s | 0 | 0 | 0 | yes | 0 |
| M-G3 | M2@1 | 1 | 11 | 22 | 54817 | $0.051 | 35.6s | 23.2s | 0 | 0 | 0 | yes | 0 |
| M-G3 | M2@1 | 2 | 9 | 18 | 38679 | $0.041 | 50.7s | 32.7s | 0 | 0 | 0 | yes | 0 |
| M-G3 | M2@1 | 3 | 8 | 16 | 38133 | $0.042 | 25.6s | 16.9s | 0 | 0 | 0 | yes | 0 |
| M-G3 | M3@20 | 1 | 6 | 12 | 24737 | $0.063 | 30.7s | 13.3s | 0 | 0 | 0 | yes | 0 |
| M-G3 | M3@20 | 2 | 7 | 14 | 28944 | $0.065 | 45.7s | 26.0s | 0 | 0 | 0 | yes | 0 |
| M-G3 | M3@20 | 3 | 7 | 14 | 26194 | $0.063 | 40.7s | 22.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 1 | 2 | 4 | 5251 | $0.031 | 10.7s | 2.7s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 2 | 2 | 4 | 9875 | $0.052 | 20.6s | 13.0s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M1@20 | 3 | 2 | 4 | 9872 | $0.022 | 10.7s | 3.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M2@1 | 1 | 3 | 6 | 17399 | $0.024 | 10.6s | 6.1s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M2@1 | 2 | 3 | 6 | 18051 | $0.028 | 15.6s | 7.3s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M2@1 | 3 | 3 | 6 | 18055 | $0.028 | 15.7s | 9.6s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 1 | 4 | 8 | 32187 | $0.104 | 25.6s | 10.4s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 2 | 3 | 6 | 27650 | $0.112 | 30.7s | 11.9s | 0 | 0 | 0 | yes | 0 |
| M-R1 | M3@20 | 3 | 4 | 8 | 33178 | $0.112 | 30.7s | 16.3s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

