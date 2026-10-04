# Phase 2 Results — who performs the join

## Key Findings

- **Accuracy is not where the difference lives.** 8 of 12 graded runs scored a perfect f1. 12 of 12 passed the grounding check. That check asks whether each *correct* value an answer states appears in the tool results that arrived — retrieval-happened, not per-fact provenance, so a run that flips a verdict scores f1 0.00 and still passes it. It does not license "nothing was fabricated". 1 of 4 condition/task cells are perfect. The agents get the answer either way. What differs is what it costs to get it, which is why this report leads with payload and calls rather than correctness.

All values are **mean ± stdev** across reps. Source: per-call proxy logs (raw Anthropic `usage`). Cache tokens are reported **separately** and are never folded into `input_tokens`.

> Cross-check the headline numbers against the audit section and the raw logs in `runs/` before publishing.


## MCP conditions (M-R6-lean / M-R7-lean / M-R8-lean)


### Task M1@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | 2.0 ± 0.0 | 1.0 ± 0.0 | 4,889 ± 162 | 695 ± 26 | 0.0 ± 0.0 | 0.0 ± 0.0 | 1,747 ± 153 |

### Task M3@20

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | 5.0 ± 1.0 | 4.7 ± 0.6 | 4,039 ± 3 | 2,742 ± 113 | 114,050 ± 86,614 | 58,131 ± 30,511 | 45,452 ± 25,336 |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | 4.3 ± 0.6 | 41.3 ± 32.3 | 2,752 ± 2,360 | 4,310 ± 1,962 | 18,848 ± 7,062 | 20,708 ± 2,018 | 11,393 ± 730 |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | 4.7 ± 2.9 | 16.0 ± 24.2 | 5,449 ± 3,133 | 2,981 ± 2,052 | 19,794 ± 34,285 | 14,979 ± 10,837 | 9,883 ± 6,616 |

### All tasks combined (per-run totals)

| Condition | inference calls | tool calls | input tok | output tok | cache-read tok | cache-create tok | tool-payload tok |
|---|---|---|---|---|---|---|---|
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | 5.0 ± 1.0 | 4.7 ± 0.6 | 4,039 ± 3 | 2,742 ± 113 | 114,050 ± 86,614 | 58,131 ± 30,511 | 45,452 ± 25,336 |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | 4.3 ± 0.6 | 41.3 ± 32.3 | 2,752 ± 2,360 | 4,310 ± 1,962 | 18,848 ± 7,062 | 20,708 ± 2,018 | 11,393 ± 730 |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | 6.7 ± 2.9 | 17.0 ± 24.2 | 10,339 ± 3,017 | 3,676 ± 2,026 | 19,794 ± 34,285 | 14,979 ± 10,837 | 11,630 ± 6,480 |

## Accuracy

`answer_f1` is field-level precision/recall against `tasks/expected.json`, whose `grading` block defines the rules per task. **coverage** is the fraction of the records the prompt asked about that the answer mentions at all — reported separately because a truncated answer can be perfectly accurate on what it does say.

| Condition | M1@20 f1 | M3@20 f1 |
|---|---|---|
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | — | 0.93 ± 0.06 |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | — | 0.95 ± 0.09 |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | 1.00 ± 0.00 | 0.97 ± 0.06 |

**On grounding.** 12 of 12 finished run(s) are fact-verified: every fact the answer states was traced to a `tool_result` that entered the context before it, using the proxy's `tool_io.jsonl` sidecar. 0 failed that check. `answer_grounded` is never `True` by default, so a blank means unassessed, not passed.


## Join tax — pass-through tokens and forced serial depth

**pass-through** is tool-result tokens whose values never appear in the answer: payload the agent carried through its context and did not use. **depth** is the longest chain of calls where each consumed an identifier the previous one returned — ids the prompt supplied are excluded, so reading the instructions does not count as a dependency.

**disc** is the same measure over *schema and spec lookup* — search feeding describe. That serialization is real latency, but it is a property of the tool surface rather than of the join, and it exists only in the on-demand conditions. Folding it into `depth` would make the headline metric track tool packaging instead of who performs the join, so the two are reported side by side.

**ex-disc** applies the same reasoning to the token figure, and it is shown wherever it changes the number. Schema and OpenAPI text is ~100% pass-through by this definition — the agent reads an SDL fragment to write a query and quotes none of it back — so `pass-through` charges the on-demand conditions for finding their own way around, while `depth` explicitly does not. That disagreement was silent until it was measured; it is not small, and it does not favour the hypothesis. Both numbers are here because which one a reader wants is an editorial call: **pass-through** is every token carried, **ex-disc** is the join tax alone.

| Condition | M1@20 | M3@20 |
|---|---|---|
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | — | 43,230 tok<br>(92% unused)<br>depth 2.7 |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | — | 8,823 tok<br>(77% unused)<br>depth 2.7 |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | 858 tok<br>(49% unused)<br>depth 1.0 | 7,506 tok<br>(74% unused)<br>depth 1.0 |

*Token figures apportion the proxy's `tool_result_tokens` by the fraction of result bytes whose values never reach the answer; `ex-disc` uses the same denominator with DISCOVERY_TOOLS results dropped from the numerator, so the two are directly comparable. The approximation is confined to that ratio.*

*⚠️ **Unit caveat.** `tool_result_tokens` is the one token column here that is not Anthropic's own `usage` figure: the proxy counts it with `cl100k_base`, which is OpenAI's tokenizer, not Claude's. Cross-checked against per-call context growth over 429 consecutive-call pairs it runs **~15% low** (median implied/counted 1.18; 14–22% by condition, and the implied side also carries per-result message framing, so 15% is an upper bound on the tokenizer error). Every figure in this table is therefore a same-signed underestimate: the ratios between conditions hold, the absolute counts are conservative. A previous version of this footnote claimed these "share units with every other token column here"; they do not. See `grade.pass_through_tokens`.*


### Ranked by pass-through tokens — the metric caching cannot touch

The cost table above is inflated by the caching result and the inflation scales with call count, so it penalises many-call conditions as a measurement artifact. `pass_through_tokens` carries no such exposure. Where the two orderings disagree, this is the one to read first.

| rank | cell | mean pass-through | median cell | task cells |
|--:|---|--:|--:|--:|
| 1 | **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | 4,182 | 4,182 | 2 |
| 2 | **M-R7-lean** — REST (Jev prunes every response), lean payloads | 8,823 | 8,823 | 1 |
| 3 | **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | 43,230 | 43,230 | 1 |

*Both statistics are taken over task cells rather than over runs: three replicates of `M3@50` would otherwise outvote one of `M1@1` in a matrix whose point is the sweep. The mean is still weighted by N through the back door, which is why the median is beside it.*


## Prompt prefix and the cache minimum

The prefix is what the model receives on the first call that carries the tool surface: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. All three, because on a warm call `cache_creation` is only the delta — the same call can read 15,911 tokens back and write 2,525, and 2,525 is not the prompt.

| Condition | Tools forwarded | Tool surface | Prefix tokens (min–max) | Cache minimum | Schema cached? |
|---|---|---|---|---|---|
| **M-R6-lean** | 8 | — | 4,017–4,019 | 4,096 | **no** — every prefix is below the minimum |
| **M-R7-lean** | 9 | — | 4,097–4,100 | 4,096 | yes |
| **M-R8-lean** | 1 | — | 1,335–1,347 | 4,096 | **no** — every prefix is below the minimum |

**9 of 12 runs carry a prefix below their model's cache minimum (M-R6-lean, M-R8-lean), so in those runs the tool surface is never written to cache at all.** Their first `cache_creation` charge fires when the *conversation* crosses the minimum, several tool rounds in — which is why Stage 1 below is labelled for that event and not for schema loading. Where a surface does clear the minimum on its own, a fatter one really does buy a bigger Stage 1; where it does not, it buys a bigger uncached `input_tokens` bill on every call until the conversation grows past the threshold. The two are not the same cost and the Stage 1 column does not distinguish them — this table is how you tell which one a row is.


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
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | M3@20 | $0.0215 | $0.0512 | $0.0292 | **$0.1018** |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | M3@20 | $0.0061 | $0.0197 | $0.0262 | **$0.0521** |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | M1@20 | $0.0000 | $0.0000 | $0.0084 | **$0.0084** |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | M3@20 | $0.0090 | $0.0097 | $0.0223 | **$0.0411** |

*Stage 1: first non-zero `cache_creation_input_tokens` call. Stage 2: all subsequent `cache_creation_input_tokens`. Stage 3: `input_tokens` + `output_tokens` + `cache_read_input_tokens` across all calls. **Cross-condition caveat:** the Stage 1 / Stage 2 boundary falls at a different point in the conversation for each condition. No phase-2 tool surface clears Haiku 4.5's 4,096-token cache minimum (prefixes run 1,491–4,053), so in every cell the first write fires on conversation growth, not on schema load — several discovery or fan-out rounds in, at a different turn per condition. A larger Stage 1 here means a larger conversation at the crossing point. The Stage 1 + Stage 2 sum (total cache-create cost) and Stage 3 are the reliable cross-condition comparators; the individual stage split reflects within-condition structure, not a symmetric breakdown.*


## Estimated cost (USD)

Pricing per model (USD/1M tokens) — claude-haiku-4-5-20251001: input $1.0/1M out $5.0/1M cc $1.25/1M cr $0.1/1M.

| Condition | Task | Reps | mean $/run | total $ (all reps) |
|---|---|---|---|---|
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | M3@20 | 3 | $0.1018 | $0.3055 |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | M3@20 | 3 | $0.0521 | $0.1562 |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | M1@20 | 3 | $0.0084 | $0.0251 |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | M3@20 | 3 | $0.0411 | $0.1232 |

**Grand total across all conditions/tasks/reps: $0.6099**


## Timing (seconds)

`wall_s` = total run duration including MCP server cold-start. `active_s` = first inference response → last inference response — excludes initialization overhead. In persistent-server deployments (the typical MCP usage pattern) `active_s` is the operative metric.

| Condition | Task | wall_s (mean ± sd) | active_s (mean ± sd) |
|---|---|---|---|
| **M-R6-lean** — REST (Jev picks which endpoint tools to expose), lean payloads | M3@20 | 27.3 ± 2.9s | 18.1 ± 8.3s |
| **M-R7-lean** — REST (Jev prunes every response), lean payloads | M3@20 | 32.3 ± 7.6s | 17.1 ± 7.2s |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | M1@20 | 10.6 ± 0.0s | 2.3 ± 0.1s |
| **M-R8-lean** — REST (Jev plan + code fetch as one tool), lean payloads | M3@20 | 35.6 ± 26.0s | 19.8 ± 23.2s |

## Audit — per-run disclosure & completion

Headline metrics count only **task-model** (`claude-haiku-4-5-20251001`) calls. `aux` = auxiliary calls on a different model (e.g. Goose session-title generation on Haiku) — excluded from the headline, shown here for full disclosure. `unparsed` should be 0.

| Cond | Task | Rep | calls | input | cache-read | cost $ | wall_s | active_s | aux calls | aux tok | unparsed | completed | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M-R6 | M3@20 | 1 | 4 | 4036 | 16653 | $0.048 | 25.7s | 8.5s | 0 | 0 | 0 | yes | 0 |
| M-R6 | M3@20 | 2 | 6 | 4042 | 182431 | $0.130 | 30.6s | 23.7s | 0 | 0 | 0 | yes | 0 |
| M-R6 | M3@20 | 3 | 5 | 4039 | 143065 | $0.128 | 25.6s | 22.0s | 0 | 0 | 0 | yes | 0 |
| M-R7 | M3@20 | 1 | 4 | 4116 | 15201 | $0.056 | 30.7s | 17.4s | 0 | 0 | 0 | yes | 0 |
| M-R7 | M3@20 | 2 | 4 | 4114 | 14355 | $0.040 | 25.6s | 9.7s | 0 | 0 | 0 | yes | 0 |
| M-R7 | M3@20 | 3 | 5 | 27 | 26987 | $0.061 | 40.6s | 24.1s | 0 | 0 | 0 | yes | 0 |
| M-R8 | M1@20 | 1 | 2 | 4750 | 0 | $0.008 | 10.6s | 2.2s | 0 | 0 | 0 | yes | 0 |
| M-R8 | M1@20 | 2 | 2 | 4851 | 0 | $0.008 | 10.6s | 2.4s | 0 | 0 | 0 | yes | 0 |
| M-R8 | M1@20 | 3 | 2 | 5067 | 0 | $0.009 | 10.6s | 2.4s | 0 | 0 | 0 | yes | 0 |
| M-R8 | M3@20 | 1 | 8 | 9066 | 59383 | $0.076 | 65.7s | 46.6s | 0 | 0 | 0 | yes | 0 |
| M-R8 | M3@20 | 2 | 3 | 3563 | 0 | $0.024 | 20.6s | 6.3s | 0 | 0 | 0 | yes | 0 |
| M-R8 | M3@20 | 3 | 3 | 3719 | 0 | $0.023 | 20.6s | 6.6s | 0 | 0 | 0 | yes | 0 |

*Every figure comes from the per-run proxy log — raw `usage` off the wire, one file per run, no shared state. Anything but `yes` under `completed` names what stopped the run: a **turn cap** exits 0 and is invisible everywhere else in this row, so this column is the only place it shows. `budget kill` = the runner killed goose when per-run cost exceeded `PER_RUN_BUDGET_USD` — the partial cost is real and reported; the answer is incomplete. Both should be re-run or excluded.*

