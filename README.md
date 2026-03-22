# Prompt Mirror

![banner](banner.png)

**プロンプトは鏡。** あなたが直感的に理解している技術概念と、まだギャップがある概念を映し出す。

Prompt Mirror は [Claude Code Skill](https://docs.anthropic.com/en/docs/claude-code/skills) です。前日のセッションプロンプトを読み、概念ギャップを1つ見つけ、朝のレッスンとして届けます。日常のアナロジーが先、エンジニア用語は後。

**コードを書かない人のためのスキル** — 創業者、PM、デザイナー、オペレーター。AIを毎日使うけどコードは書かない。でもエンジニアと同じ言葉で話したい。そういう人のために作りました。

## やること

毎朝、Prompt Mirror は:

1. **抽出** — 前日の Claude Code セッションからプロンプトを収集
2. **分析** — 概念ギャップを探す（技術用語の不正確な使用、関連概念の混同、AIの出力品質を判断できなかった瞬間）
3. **選定** — 最もインパクトの高い1概念を選ぶ（1日1つだけ）
4. **配信** — ジャーナルにレッスンを追記: 昨日の出来事 → 日常例 → エンジニア用語 → なぜ得か → アクション

## 実際のレッスン例

### Day 1: Precision vs Recall

> ### 検索結果を絞り込むとき「精度」と「網羅性」はシーソーの関係になる
>
> **昨日あったこと**:
> newssenseのニューススキャンで、最初は `--limit 15 --since 24h` で広く取り、次に `--limit 10 --since 12h` で絞り、最終的に `--limit 50 --since 12h` で量を増やしつつ厳しいスコアリング基準を追加した。パラメータを4回調整して、ちょうどいいバランスを探していた。
>
> **日常例で言うと**:
> Amazonで「ワイヤレスイヤホン」を検索すると1万件出る。「ノイキャン 1万円以下」に絞ると50件になるけど、「ノイキャン」と書いていないだけで実は付いてる良い商品を見逃す。逆に広すぎると全部見きれない。この「絞る↔広げる」のジレンマは、検索やデータ収集では常に起きる。
>
> **エンジニアはこう呼ぶ**:
> **Precision vs Recall（適合率 vs 再現率）** — Precision = 返された結果のうち本当に欲しいものの割合。Recall = 欲しいもの全体のうち実際に返されたものの割合。両方100%にするのは原理的に難しい。
>
> **なぜ知っておくと得か**:
> AIにニュースを集めさせたり検索を頼むとき、「今は網羅性が大事か、ノイズを減らしたいか」を意識するだけでパラメータ調整の試行回数が減る。昨日の最終形「50件取ってから厳しくスコアリング」はrecall→precisionの二段階戦略で、これが正解パターン。
>
> **明日から使えるアクション**:
> AIに検索や収集を頼むとき、先に戦略を宣言する（例: 「まずrecall重視で50件取って、その後precision重視でTop 7に絞って」）

### Day 2: Event Time vs Processing Time

> ### 「いつ起きたか」と「いつ処理したか」は別物
>
> **昨日あったこと**:
> PPPレポートであやみさんの記事（03/18 23:53 JST更新）が翌日のジャーナルに入っていることに気づいた。「なんかズレてるかもです」と指摘して修正を促した場面。
>
> **日常例で言うと**:
> 金曜23:55にピザを注文して、届いたのが土曜0:05。お店の売上レポートに「金曜の注文」と書くか「土曜の注文」と書くかで数字が変わる。どちらが正しいかはルール次第で、ルールが曖昧だとズレが起きる。
>
> **エンジニアはこう呼ぶ**:
> **Event Time vs Processing Time** — イベントが実際に発生した時刻（event time）と、システムがそれを処理・記録した時刻（processing time）の区別。データパイプライン、ログ管理、ストリーム処理で必ず出てくる概念。
>
> **なぜ知っておくと得か**:
> newssense、finance-cli、voice-inboxなど、プロジェクトはすべて「いつのデータか」を扱う。AIに「日次レポートを作って」と頼むとき、event timeとprocessing timeのどちらで集計するか指定できると、昨日のようなズレを未然に防げる。
>
> **明日から使えるアクション**:
> 日付で集計するプロンプトを書くとき、「いつ起きたか（event time）で集計して」と一言添える。

### Day 3: Secrets Management

> ### 設定値と秘密情報は別モノ
>
> **昨日あったこと**:
> newssenseのX API認証用に、CLIENT_IDとCLIENT_SECRETをプロンプトに直書きして.zshrcに追記を指示した。この値はセッションログ（~/.claude/projects/のJSONLファイル）に平文のまま永久に残る。
>
> **日常例で言うと**:
> 家の住所は人に教えても大丈夫。でも鍵の暗証番号を紙に書いて玄関のポストに貼ったら、通りがかりの誰でも家に入れてしまう。設定値にも「見られてOKなもの」と「見られたらまずいもの」がある。
>
> **エンジニアはこう呼ぶ**:
> Secrets management（シークレット管理）。CLIENT_IDは「住所」に近い準公開情報、CLIENT_SECRETは「鍵」にあたる秘密情報。エンジニアは秘密情報をKeychain・Vault・.envファイル（gitignore対象）に入れ、ログやチャット履歴には絶対に残さない。
>
> **なぜ知っておくと得か**:
> AIエージェントへのプロンプトは自動でJSONLに記録される。秘密情報を直書きすると、そのファイルにアクセスできる人全員にAPI認証が丸見えになる。特にautorunで毎日動くスキルほど、この区別が重要。
>
> **明日から使えるアクション**:
> API秘密情報をプロンプトに直接書かず、「.envに既にある値を使って」と伝える。値そのものではなく、値の置き場所を指示する。

## Jaggedness Map

> AIモデルは「同時に超優秀な博士課程の学生であり10歳児でもある」(Andrej Karpathy)。
> 人間のプロンプト能力も同じようにジャギッド（凸凹）。この機能は taught.jsonl の蓄積から、あなた個人の強み/弱みマップを自動構築します。

### 実例: 作者のマップ（7日間・119プロンプト・7レッスンから生成）

```
Strong (自信を持って正確にプロンプトできている領域)
└── ツール活用
    OAuth認証、CLI操作、Electron/CDP自動化、cron設定、複数AIプロバイダ使い分け
    7日間で概念ギャップがほぼ検出されなかった領域

Weak (レッスンが集中した領域)
├── 信頼性設計 (1 lesson)
│   同一プロンプトを5-6回リトライ
│   失敗が一時的か構造的かの判断が弱い (transient vs persistent failure)
└── 仕様伝達 (1 lesson)
    暗黙の参照パターンが持続的に出現
    「なんかズレてる」系の曖昧指示が改善途上

Improving (レッスン後に行動変化が確認された領域)
├── システム設計 (2 lessons)
│   セッション共有→ハンドオフ文書 (shared state vs message passing)
│   拡張ポイントの識別 (extension points vs core modification)
│   直感は正しく、議論後に概念を獲得するパターン
└── データ概念 (3 lessons)
    precision/recall、event/processing time、batch/stream
    7日で3概念に遭遇し、試行錯誤→体得のサイクルが回っている

Stats: 7 lessons | 0 "no lesson" days
Trend: データ概念の学習速度が最も速い。信頼性設計が最大のギャップ — 次のフォーカスポイント
```

7日分以上のデータが溜まると、週次でジャーナルにマップが自動追記されます。

## インストール

```bash
claude install-skill KaishuShito/prompt-mirror
```

## セットアップ

インストール後、スキルディレクトリの `config.json` を自分の環境に合わせて編集:

```json
{
  "journal_dir": "~/Documents/Journal",
  "projects_dir": "~/.claude/projects",
  "codex_dir": "~/.codex",
  "timezone": "Asia/Tokyo",
  "hour_cutoff": 6,
  "max_prompts_per_session": 20,
  "min_prompt_length": 30
}
```

| フィールド | 説明 | デフォルト |
|-----------|------|-----------|
| `journal_dir` | 日次ジャーナルの保存先 | `~/Documents/Journal` |
| `projects_dir` | Claude Code セッション JSONL のディレクトリ | `~/.claude/projects` |
| `codex_dir` | Codex CLI セッションディレクトリ（任意） | `~/.codex` |
| `timezone` | 日付境界のタイムゾーン | `Asia/Tokyo` |
| `hour_cutoff` | この時刻より前は「昨日」扱い | `6` |

## 使い方

### 手動

Claude Code で:

```
/prompt-mirror
```

### 定期実行（推奨）

このスキルは毎朝の自動実行を前提に設計されています。以下のいずれかで設定:

**Claude Code デスクトップアプリ（推奨）**

Claude Code のデスクトップアプリでスキルをインストールし、定期実行を設定するだけです。

**[AGI Cockpit](https://chatgpt-lab.com/n/nd2e5ef201888) autorun**

AGI Cockpit を使っている場合、Master エージェントに以下のように指示するだけです:

> 「prompt-mirror スキルを毎朝5時に実行するようにautorunを設定して」

Master エージェントが `./cockpit autorun create` を実行してスケジュールを設定します。

**Cron + Claude Code CLI**
```bash
# crontab -e
0 5 * * * cd ~/your-project && claude -p "/prompt-mirror"
```

朝に実行する理由 — Prompt Mirror は*昨日*のプロンプトを読むので、今日の作業を始める前にレッスンを受けると、その日のプロンプティングに活かせます。

## スキル構成

```
prompt-mirror/
├── SKILL.md                    # スキル本体の指示
├── config.json                 # ユーザー設定
├── gotchas.md                  # 実運用で見つかった失敗パターン
├── scripts/
│   └── extract_prompts.py      # セッション JSONL → プロンプト抽出
├── templates/
│   ├── lesson.md               # レッスン出力テンプレート
│   └── jaggedness-map.md       # Jaggedness Map出力テンプレート
└── data/
    ├── taught.jsonl            # 記憶: 教えたトピック（自動生成）
    └── jaggedness-map.json     # 強み/弱みマップ（自動生成）
```

Anthropic の [スキル設計ガイドライン](https://x.com/trq212/article/2033949937936085378) に従い、progressive disclosure パターンを採用。`SKILL.md` がエントリーポイントで、Claude は必要に応じて `gotchas.md` や `templates/` を読みます。

### 設計判断

- **1日1レッスン** — 複数あっても読まれない。量より質
- **日常例が先** — 技術用語から入らない。アナロジーがフック
- **taught.jsonl が記憶** — 同じトピックの繰り返しを防ぎ、概念の深度が時間とともに上がる
- **独立した抽出スクリプト** — `extract_prompts.py` は外部依存なしで単体動作
- **レッスンにコードなし** — ユーザーはコードを書かない。概念だけで説明する
- **Jaggedness Map** — 7レッスン以上で自動生成。プロンプト能力の凸凹を可視化

## カスタマイズ

### 言語

デフォルトではプロンプトで使われている言語に合わせます。`templates/lesson.md` を編集して出力言語を固定できます。

### ジャーナル形式

デフォルトでは `YYYY-MM-DD.md` ファイルに `## Prompt Mirror` セクションとして追記。`templates/lesson.md` を自分のジャーナル構造に合わせて変更可能。

### 概念の深度

`data/taught.jsonl` のエントリ数に応じて自動的に概念の複雑さが上がります。初期は基礎（stateless vs stateful）、蓄積が増えるとより高度なトピック（event-driven vs polling）へ進行。

## 仕組み

`scripts/extract_prompts.py` が `~/.claude/projects/` の JSONL セッションファイルを走査し、JST 日付でフィルタし、以下をスキップしながらユーザーメッセージを抽出:
- システムリマインダーとコマンド呼び出し
- 30文字未満のメッセージ
- サブエージェント（委任）セッション

Claude が抽出されたプロンプトを `SKILL.md` のコンセプトレンズで分析し、`data/taught.jsonl` で重複チェックし、レッスンを書きます。

## クレジット

[@KaishuShito](https://github.com/KaishuShito) が Claude Code で構築。

Anthropic の [Lessons from Building Claude Code: How We Use Skills](https://x.com/trq212/article/2033949937936085378) のスキル設計パターンと、Andrej Karpathy の [Jaggedness（凸凹性）の概念](https://www.youtube.com/watch?v=kwSVtQ7dziU) にインスパイアされました。
