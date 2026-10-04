# 追試と追加実験（`cc/`）

[apollographql/graphql-mcp-benchmarks](https://github.com/apollographql/graphql-mcp-benchmarks)（コミット `faa9169`）を手元で追試し、GraphQL が有利になる理由を切り分けるための実験を追加した一式です。

記事: <!-- TODO: Zenn の記事 URL -->

upstream のコード（runner、ロギング用のプロキシ、採点、集計）は変更せず、`cc/` の中から import して差し替える形にしています。upstream 側のファイルで変更したのは、router のホスト側ポート（5000 → 5050）だけです（後述）。

## 何をしたか

| 実験 | 中身 | 実行方法 | 結果 |
|---|---|---|---|
| Phase 1 の追試（Goose） | 公開値と同じ Goose 1.37.0 + Haiku 4.5 | upstream の `./bench.sh` | `results-goose/phase1/` |
| Phase 1 の追試（`claude -p`） | エージェントの起動だけを Claude Code に差し替え | `cc/run_cc.py` | `results-cc/phase1/` |
| Phase 1、他のモデル | Sonnet 5 / Opus 5.5 / Fable 5.1 を Goose で | `cc/run_goose_nosampling.py` | `results-models/<model>/phase1/` |
| Phase 2、4 モデル | M-R1（fat）と M-G2 × M1・M3 × 3 回 | `cc/run_cc.py` | `results-cc/phase2/`（比較は `comparison.md`） |
| 要因の切り分け | lean の REST、M-G2、M-G3 × M1@20・M3@20・M2@1、Haiku 4.5 / Sonnet 5 × 3 回 | `cc/run_factors.sh`、`cc/run_baselines.sh` | `results-cc/phase2-factors/` |
| REST + BFF（M-R4） | `expand` / `fields` を持つ BFF を 1 本足す | `cc/bff/` | `results-cc/phase2-bff/` |
| Jev（M-R5〜M-R8） | フィールドと関連の選択を Jev とコードに任せる | `cc/jev/` | `results-cc/jev/`（集計は `summary_3reps.md`） |

`claude -p` での実行は 2026-09-28〜10-01 です。Claude Code は Phase 1・Phase 2 が 2.1.283、要因の切り分け以降が 2.1.284〜2.1.286 で、各回の版は `meta.json` に記録されています。

生ログ（`runs-cc/` など）は、upstream の `runs/` と同じくコミットしていません。集計済みの `raw.csv`（1 回ごとの行）と `summary.md` をコミットしています。

## 準備

upstream の README の手順（`./bench.sh setup`、Docker、`gh auth login`）に加えて、次が必要です。

- Claude Code（`claude` コマンド）。`claude -p` はサブスクリプションのログインで動き、`ANTHROPIC_API_KEY` は使いません
- Python 3.12 以上（upstream の `parse_logs.py` が 3.12 の構文を使っています）。`.tools/bin/python3` に置くと、`cc/env.sh` が PATH に入れます
- [uv](https://docs.astral.sh/uv/)
- Jev の実験のみ: `.env` に `JEV_API_KEY`

```bash
source cc/env.sh          # claude -p 用（PATH、GitHub token、MODEL=claude-haiku-4-5）
source cc/goose_env.sh    # Goose 用（.env の API キーを読む）
```

## 実行

### Phase 1（`claude -p`）

```bash
source cc/env.sh
RUNS_DIR=$PWD/runs-cc/phase1 uv run cc/run_cc.py
RESULTS_DIR=$PWD/results-cc/phase1 python3 parse_logs.py runs-cc/phase1
```

### Phase 1（Goose、Sonnet 5 / Opus 5.5 / Fable 5.1）

```bash
source cc/goose_env.sh
MODEL=claude-sonnet-5 RUNS_DIR=$PWD/runs-models/claude-sonnet-5/phase1 uv run cc/run_goose_nosampling.py
MODEL=claude-sonnet-5 RESULTS_DIR=$PWD/results-models/claude-sonnet-5/phase1 \
  python3 cc/parse_with_prices.py runs-models/claude-sonnet-5/phase1
```

### Phase 2（M1・M3、4 モデル）

```bash
source cc/env.sh
MODEL=claude-opus-5-5 PAYLOAD_PROFILE=fat CONDITIONS=M-R1,M-G2 TASKS=M1,M3 \
  RUNS_DIR=$PWD/runs-cc/phase2/claude-opus-5-5 uv run cc/run_cc.py
MODEL=claude-opus-5-5 RESULTS_DIR=$PWD/results-cc/phase2/claude-opus-5-5 \
  python3 cc/parse_with_prices.py runs-cc/phase2/claude-opus-5-5
python3 cc/compare_phase2.py > results-cc/phase2/comparison.md   # 4 モデル + 公開値
```

特定の回だけを実行し直すときは、`uv run cc/rerun_cc.py 条件:タスク:回`（例: `M-R1:M1@50:3`）を使います。

### 要因の切り分け

REST は lean プロファイルで起動しておきます（`PAYLOAD_PROFILE=lean`）。

```bash
bash cc/run_factors.sh      # 1 回目
bash cc/run_baselines.sh    # 2・3 回目（BFF の 2・3 回目も含む）
```

### REST + BFF（M-R4）

`cc/bff/bff_server.py` は、既存の 3 サービスを呼んでサーバー側で join する BFF です。次のエンドポイントを持ちます。

```http
GET /v2/flights?ids=FL-0001,FL-0002
  &expand=aircraft,assignments.crew
  &fields=aircraft.model.code,assignments.role,assignments.crew.typeRatings.expiresAt
  &assignmentRoles=CAPTAIN,FIRST_OFFICER
```

M-R4 は、M-R1 の 9 本のツールにこの 1 本（`listFlightExpanded`）を足した条件です。ツールは M-R1 と同じ `servers/openapi_mcp.py --mode tools` で、OpenAPI 仕様（`cc/bff/spec/gateway/openapi.json`）から生成しています。

```bash
python3 cc/bff/bff_server.py --port 4004 &
source cc/env.sh
PAYLOAD_PROFILE=lean MODEL=claude-sonnet-5 RUNS_DIR=$PWD/runs-cc/phase2-bff/claude-sonnet-5 \
  uv run cc/bff/run_bff.py M-R4:M3@20:1
MODEL=claude-sonnet-5 RESULTS_DIR=$PWD/results-cc/phase2-bff/claude-sonnet-5 \
  python3 cc/parse_with_prices.py runs-cc/phase2-bff/claude-sonnet-5
```

### Jev（M-R5〜M-R8）

[Jev](https://docs.typesafe.ai/introduction)（TypeSafe AI の System One API、`jev-1.13.0`）は文章を生成せず、状態と型付きの質問（Noul / Choice / Score）に確率付きで答えるモデルです。コードはタスクごとの処理を持たず、資源・関連・フィールドはすべて OpenAPI 仕様から機械的に取り出しています（`cc/jev/catalog.py`）。

| 条件 | 記事での名前 | 中身 | 実装 |
|---|---|---|---|
| M-R5 | A: 事前取得 | Jev がタスク文と OpenAPI 仕様から取得計画を立て、コードが lean の REST を取得・join・射影する。Claude はツールを持たず、取得済みのデータだけで答える | `prefetch.py`、`run_prefetch.py` |
| M-R6 | B: ツールの絞り込み | Jev が 9 本のツールのうち見せるものを選ぶ | `openapi_mcp_jev.py --gate`、`run_bc.py` |
| M-R7 | C: 応答の後処理 | エージェントは 9 本を使い、REST の応答を Jev が末端フィールドの単位で削る | `openapi_mcp_jev.py --prune`、`run_bc.py` |
| M-R8 | A をツールにした形 | M-R5 の計画と取得を MCP のツール 1 本 `fetch_airline_data(question)` にする | `mcp_jev_fetch.py`、`run_bc.py` |

```bash
bash cc/jev/run_all.sh                        # M-R5〜M-R7 の 1 回目
uv run cc/jev/run_bc.py M-R8:M3@20:1 M-R8:M1@20:1   # M-R8 の 1 回目（MODEL ごと）
bash cc/jev/run_reps.sh                       # 全条件の 2・3 回目
python3 cc/jev/export_runs.py                 # runs-cc/ から M-R5 の結果と Jev の費用を results-cc/jev/ に書き出す
python3 cc/jev/summarize.py > results-cc/jev/summary_3reps.md
uv run cc/jev/dry_run.py M3@20                # LLM を使わず、Jev の計画と取得だけを試す
```

`summarize.py` は `results-cc/` だけを読むので、生ログがなくても集計を再現できます。

## 追加したファイル

| ファイル | 役割 |
|---|---|
| `run_cc.py` | `run_benchmark` を import し、`goose run` の起動だけを `claude_shim.py` に置き換える。タイムアウト時はプロセスグループごと止める |
| `claude_shim.py` | recipe を `claude -p` の引数に変換する。`instructions` → `--system-prompt`、`extensions` → `--mcp-config`。組み込みツールと thinking は無効 |
| `mcp_meta_relay.py` | MCP サーバーとの間に入り、`tools/list` の各ツールに `_meta["anthropic/maxResultSizeChars"]=500000` を付ける |
| `rerun_cc.py` | 指定した（条件, タスク, 回）だけを実行する |
| `run_goose_nosampling.py` | Goose で、描画後の recipe から `temperature` の行を取り除いて実行する |
| `parse_with_prices.py` | `parse_logs.py` に新しいモデルの料金と M-R4〜M-R8 を登録し、Claude Code が足す通知を取り除いてから採点する |
| `models.py` | Sonnet 5 / Opus 5.5 / Fable 5.1 の料金 |
| `compare_phase2.py` | Phase 2 の 4 モデルと公開値の比較表 |
| `rover_schema_mcp.sh` | B2 のサーバーを指定した Python で起動する（後述） |
| `recipes/` | M-R4、M-R6〜M-R8 の recipe。`instructions` は M-R1 と同じ |
| `bff/` | M-R4 の BFF と MCP サーバー |
| `jev/` | M-R5〜M-R8 |

## `claude -p` と Goose の違い（結果を読むときの前提）

- **大きなツール結果の切り詰め**: Claude Code は、50,000 文字を超える MCP のツール結果をファイルに保存し、モデルには先頭 2KB のプレビューだけを渡します。対策しないと、T1 の REST 側のツール結果が 9,337 token に縮みました（正しくは 27,039）。`mcp_meta_relay.py` が各ツールの `_meta` で上限を引き上げます。`_meta` はクライアントが読むもので、モデルには送られません。対策前の結果は `results-cc/phase1-clipped/` に残しています
- **ツール結果への通知の付加**: Claude Code は、MCP のツール結果の末尾に `<system-reminder><total_tokens>N tokens left</total_tokens></system-reminder>` を付けます（1 件あたり約 23 token）。ツール結果が JSON として読めなくなり、`grade.pass_through_tokens` がツール結果を丸ごと未使用と判定します。`parse_with_prices.py` が採点の前に取り除きます。token 数には含めたままです（モデルが実際に読んでいるため）
- **システムプロンプト**: `--system-prompt` で recipe の `instructions` に置き換えても、Claude Code が固定で約 330〜400 token を付け足します
- **キャッシュの TTL**: 書き込みはすべて 1 時間 TTL（単価は入力の 2 倍）です。`parse_logs.py` は 5 分 TTL（1.25 倍）で計算するので、`compare_phase2.py` と `jev/summarize.py` は 2 倍で計算し直しています
- **推論回数**: Goose より少なくなります。Goose は並列のツール呼び出しを 1 回ずつ別の往復に分けて送るためです。公開値で M3@50 の GraphQL（M-G2）が REST より高くなっていたのは、この影響です
- **temperature**: `claude -p` には指定する手段がなく、既定値のままです（upstream の recipe は `temperature: 0`）
- **タイムアウト**: upstream の runner はタイムアウトで shim だけを止め、`claude -p` は動き続けていました。`run_cc.py` はプロセスグループごと止めます
- **スリープ**: 実行中に Mac がスリープするとタイムアウトします。長い実行には `caffeinate -i -s` を付けています（バッテリー駆動では、蓋を閉じたときのスリープは防げません）

## 新しいモデルでの注意

- Sonnet 5 / Opus 5.5 / Fable 5.1 は `temperature` を受け付けません（`400: temperature is deprecated for this model`）。Goose では `run_goose_nosampling.py` で取り除いています
- upstream の `./bench.sh precheck` は、この 400 エラーのときも `PASS` と表示します。エラー応答にもキャッシュの欄があり、そこだけを見て判定しているためです
- upstream の料金表にないモデルは Sonnet 4.6 の料金で計算されるので、`models.py` で追加しています。runner の予算による停止の判定にも使われます
- thinking は、Goose ではモデルの既定のまま（Sonnet 5 は adaptive、Opus 5.5 と Fable 5.1 は常にオン）、`claude -p` では無効です

## upstream で見つかった再現上の問題

- `parse_logs.py` は Python 3.12 以上が必要です（README は 3.10 以上と書いています）
- `bench.sh test` は Node 23 の出力形式（`ℹ tests`）を拾えず、全件成功しても失敗と表示します
- `docker compose up` を初めて実行すると、同じイメージを並列でビルドして失敗します。先に `docker compose build personnel-rest` を 1 回実行します
- macOS ではポート 5000 を AirPlay レシーバーが使っています。router のホスト側ポートを 5050 に変更しました（`docker-compose.yml`、`services/src/entities/index.ts`、`config/apollo-mcp.phase2*.yaml`、`servers/supergraph_mcp.py`）
- Goose で実行すると、B2 のサーバー（`servers/rover_schema_mcp.py` の `#!/usr/bin/env python3`）は PATH 上の Python で起動します。それが証明書の設定されていない python.org 版だと、GitHub への TLS 接続が `CERTIFICATE_VERIFY_FAILED` で失敗します。このときエージェントはエラー文を答えとして返し、終了コードは 0 のままでした。`cc/goose_env.sh` は `B2_BIN=cc/rover_schema_mcp.sh` で起動する Python を指定します（`B2_PYTHON` で変更できます）
- GitHub MCP Server のイメージは `latest` で、版が固定されていません。今回は v1.12.2 で、A1 のツール数は公開時の 54 本から 56 本に増えていました
- 失敗した回も終了コードは 0 になるので、答えは必ず採点結果（`answer_f1`）で確認します

## ライセンス

upstream と同じ MIT License です（`LICENSE`）。
