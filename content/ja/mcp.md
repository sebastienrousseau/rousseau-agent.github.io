---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau)"
banner_alt: "rousseau-agent banner"
banner_height: "398"
banner_width: "1440"
banner: ""
cdn: "https://cloudcdn.pro"
charset: "utf-8"
cname: "docs.rousseau-agent.dev"
copyright: "Copyright © 2026 Sebastien Rousseau. Released under the MIT License."
date: "July 12, 2026"
download: ""
format-detection: "telephone=no"
hreflang: "ja"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "ja"
locale: "ja_JP"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
theme-color: "26, 58, 138"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "weekly"
description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/mcp/"
subtitle: "stdio 上の JSON-RPC 2.0、仕様リビジョン 2024-11-05。"
tags: "MCP, reference"
title: "MCP サーバー"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP サーバー"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "MCP サーバー"
last_build_date: "Sun, 12 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(26,58,138)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP サーバー"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "自らのコーディングエージェントを運用するすべてのオペレーターに感謝します。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau が話す完全な JSON-RPC 2.0 のワイヤーフォーマット、rousseau の MCP サーバーが実装するすべてのメソッドと例示的なリクエスト/レスポンスのペア、エラーコードのセマンティクス、そしてサーバーに到達させるための Claude Desktop / Cursor / IDE の MCP ホストの設定方法を扱います。このページと合わせて <code>internal/mcp/protocol.go</code> および <code>internal/mcp/server.go</code> を参照してください。</p></aside>

## ワイヤーフォーマット

`rousseau mcp` は、[Model Context Protocol](https://modelcontextprotocol.io) 仕様のリビジョン **2024-11-05** (`internal/mcp/protocol.go` の `ProtocolVersion` で宣言) に従い、stdio 上で JSON-RPC 2.0 を扱う MCP サーバーを起動します。

- stdin では 1 行につき 1 リクエスト (`bufio.Scanner` は 1 行あたり最大 8 MiB を読み取ります)。
- stdout では 1 行につき 1 レスポンス (`json.NewEncoder` が改行区切りの JSON を出力します)。
- サーバーは、stdin がクローズされるか `ctx` がキャンセルされるまでブロックします。

### JSON-RPC 2.0 エンベロープ

すべてのリクエスト、通知、レスポンスは次のエンベロープを使用します (`internal/mcp/protocol.go` 38 行目より)。

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

存在するフィールドはエンベロープの種類によって異なります。

| フィールド | リクエスト | 通知 | レスポンス |
|---|:---:|:---:|:---:|
| `jsonrpc` | 常に `"2.0"` | 常に `"2.0"` | 常に `"2.0"` |
| `id` | 必須 | なし | リクエストから反映 |
| `method` | 必須 | 必須 | なし |
| `params` | 任意 | 任意 | なし |
| `result` | なし | なし | 成功時のみ |
| `error` | なし | なし | 失敗時のみ |

通知は `id` を持たず、レスポンスもありません。rousseau が受け取る通知は `notifications/initialized` のみで、これはサイレントに受理されます。

### メソッドリファレンス

Rousseau の `Server.dispatch` (`internal/mcp/server.go` 112 行目) は次のメソッドをルーティングします。

| メソッド | 目的 | レスポンス |
|---|---|---|
| `initialize` | ハンドシェイク。クライアントがプロトコルバージョンと機能を宣言します。 | `InitializeResult` |
| `notifications/initialized` | クライアントが準備完了を通知します。 | (通知のため、レスポンスなし) |
| `ping` | 生存確認。 | `{}` |
| `tools/list` | 登録済みツールを列挙します。 | `ToolsListResult` |
| `tools/call` | ツールを呼び出します。 | `ToolsCallResult` |
| `resources/list` | プレースホルダー。現在は `{ "resources": [] }` を返します。 | `{"resources": []}` |
| `prompts/list` | プレースホルダー。`{ "prompts": [] }` を返します。 | `{"prompts": []}` |
| `shutdown` | クライアント起点のシャットダウン。 | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">未実装のメソッド</span><p><code>resources/list</code> と <code>prompts/list</code> は、これらを確認するホストがエラーにならないよう、空の配列を返します。リソース/プロンプトの完全なサポートはロードマップに含まれています。<code>docs/GAP_ANALYSIS_2026.md</code> を参照してください。</p></aside>

## リクエスト/レスポンスの例

### 1. `initialize`

クライアントの送信:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

サーバーの応答:

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false` は、rousseau のツールセットがプロセス起動時点で静的であり、実行時の追加/削除がないためです。

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

サーバーは登録された順序で登録済みツールを応答します。

```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"read","description":"Read a file...","inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
  {"name":"grep","description":"Search for a regex...","inputSchema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}},
  {"name":"bash","description":"Execute a shell command...","inputSchema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}
]}}
```

### 3. `tools/call`

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read","arguments":{"path":"/etc/hostname"}}}
```

成功時:

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

ハンドラーレベルの失敗 (JSON-RPC エラーではなく、コンテンツとして表面化されます。これは MCP の慣習です):

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"read: open /nope: no such file or directory"}],"isError":true}}
```

### 4. `ping`

```json
{"jsonrpc":"2.0","id":4,"method":"ping"}
```

```json
{"jsonrpc":"2.0","id":4,"result":{}}
```

## エラーコード

Rousseau は標準の JSON-RPC 2.0 エラー範囲に加え、1 つの MCP 拡張を使用します。

| コード | 定数 | 意味 | 発行タイミング |
|---|---|---|---|
| -32700 | `CodeParseError` | エンベロープの JSON が無効。 | エンベロープの `json.Unmarshal` が失敗しました。 |
| -32600 | `CodeInvalidRequest` | エンベロープの形状が誤っている。 | `jsonrpc` フィールドが `"2.0"` ではありません。 |
| -32601 | `CodeMethodNotFound` | メソッドが未実装。 | ディスパッチが default 節に到達しました。 |
| -32602 | `CodeInvalidParams` | パラメータのデコードに失敗。 | `params` が期待される形状にアンマーシャルできませんでした。 |
| -32603 | `CodeInternalError` | レスポンスのマーシャリング中に問題が発生。 | まれです。バグを示します。 |
| -32000 | `CodeToolNotFound` | ツール名が登録されていない。 | `tools/call` で未知の `name` を呼び出しました。 |

<aside class="admonition" data-type="warning"><span class="admonition-title">ツールエラーと JSON-RPC エラーの違い</span><p>ハンドラーレベルの失敗 (非ゼロ終了した <code>bash</code> コマンドや、存在しないファイルに対する <code>read</code> など) は、JSON-RPC の <code>error</code> フィールドではなく、<code>isError: true</code> を付けて <code>result.content</code> を通じて返されます。<code>error</code> はプロトコルレベルの失敗にのみ使用されます。両方のチャネルを同等に扱うホストでは、リカバリ可能な失敗を誤って分類してしまいます。</p></aside>

## 公開されているもの

サーフェスは 2 つあります。

- **ツール。** `Serve` の前に登録されたすべての `mcp.ToolSpec` は `tools/list` で告知され、`tools/call` から呼び出せます。rousseau はローカルのエージェントループが使うのと同じツール実装を配線しています: `read`、`write`、`edit`、`grep`、`bash`。
- **セッション。** rousseau の SQLite セッションストアが公開されており、MCP ホストは過去の会話を列挙および読み取ることができます。`resources/list` はセッション 1 件につき 1 エントリを返します。

ツールの失敗は、JSON-RPC エラーチャネルではなく、`isError=true` を付けた `content` チャネルを通じて表面化されます。これは MCP の慣習です。

## クライアント設定 — Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)、あるいはプラットフォームの相当ファイルに次を追加します。

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"],
      "env": {
        "HOME": "/Users/you"
      }
    }
  }
}
```

Claude Desktop を再起動します。`rousseau` がツールパレットに表示され、登録済みのすべてのツールが呼び出し可能になります。

Podman イメージにビルドされた rousseau の場合、エントリは次のようになります。

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z",
        "localhost/rousseau-agent:local",
        "mcp"
      ]
    }
  }
}
```

MCP ホストがデーモンと同じセッションを参照できるよう、ステートディレクトリをバインドマウントしてください。

## カスタムツールの登録

MCP サーバーを独自のバイナリに埋め込む例:

```go
srv := mcp.NewServer("rousseau", "0.1.0", logger)

srv.MustRegister(mcp.ToolSpec{
    Name:        "count_files",
    Description: "Count files under a path.",
    InputSchema: json.RawMessage(`{
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }`),
    Handler: func(ctx context.Context, args json.RawMessage) ([]mcp.Content, error) {
        var in struct{ Path string }
        if err := json.Unmarshal(args, &in); err != nil {
            return nil, fmt.Errorf("bad input: %w", err)
        }
        // ... count files ...
        return []mcp.Content{{Type: "text", Text: fmt.Sprintf("%d", n)}}, nil
    },
})

_ = srv.Serve(ctx, os.Stdin, os.Stdout)
```

重複登録はエラーを返します。`MustRegister` は重複時にパニックします (`main` での配線用に予約されています)。

## 並行性

`Serve` は独立したトランスポート (MCP ホスト向けの stdin/stdout に加え、必要に応じて制御チャネル) 上で並行に呼び出せます。サーバーのツールマップは RWMutex で保護されていますが、ハンドラーの実行は直列化されません。実装は並行使用に対して安全である必要があります。

## デバッグ

各リクエスト/レスポンスのエンベロープは、デフォルトで `debug` レベルでログに記録されます。有効化する方法:

```yaml
log:
  level: debug
  format: text
```

Or:

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

MCP ホストは stdout を消費します。ログストリームは stderr に保ってください。

## トラブルシューティング

### Claude Desktop / Cursor に rousseau のツールが表示されない

ほぼ常に配線の誤りであり、rousseau の問題ではありません。次を確認してください: (1) ホスト設定の `command` と `args` が `rousseau mcp` を起動していること (`rousseau chat` ではない)、(2) 設定ファイルが保存されホストが再起動されていること、(3) シェルから `rousseau mcp </dev/null` を実行してもクラッシュしないこと。クラッシュする場合は、まずそれを修正してください。

### 最初のメッセージで `parse error`

ホストが改行区切りの JSON を送信していません。初期の MCP 実装の一部はフレーム化されたメッセージ (`Content-Length: N\r\n\r\n<body>`) を送信しますが、rousseau は `\n` 区切りを期待します。stdio フレーミングを使用するビルドにホストを更新してください (現行の主要ホストはすべてそうなっています)。

### `method not found: <foo>`

ホストが rousseau で実装されていないメソッドを呼び出しています。空の `resources/list` と `prompts/list` は一般的なプローブ用のノーオペレーションとして提供されており、それ以外は `-32601` を返します。メソッドの一覧は `internal/mcp/server.go` の `dispatch()` を参照してください。

### ツール呼び出しは成功するが、ホストがエラーとして報告する

ツールハンドラーがエラーを誤った方法で返却しています。ハンドラーは `[]Content{{Type: "text", Text: err.Error()}}, err != nil` を返すべきです。rousseau がエラーを捕捉し、`isError: true` にラップします。プロトコルレベルの失敗でない限り、JSON-RPC の `error` チャネル経由でエラーを返してはいけません。

### コンテナベースの MCP がステートディレクトリで `permission denied`

Claude Desktop からの `podman run` 呼び出しには、適切な SELinux ラベル付きでステートディレクトリの `-v` を含める必要があります。他の Podman ワークロードとコンテナを共有しない限り、`:Z` (プライベート) を使用してください。また、コンテナ内のホスト UID がファイル所有者と一致していることも確認してください。

## 関連ページ

- [MCP: Exposed Tools](/ja/mcp/exposed-tools/) — rousseau が公開するツールセット。
- [MCP: Exposed Resources](/ja/mcp/exposed-resources/) — セッションの列挙と読み取り。
- [MCP: Compatibility](/ja/mcp/compatibility/) — 検証済みホストの一覧。
- [Tutorials: Expose Tools via MCP](/ja/tutorials/expose-tools-via-mcp/) — エンドツーエンドのウォークスルー。
- [Agent loop](/ja/agent-loop/) — 同じツールが rousseau 内でどう使われるか。

## さらに読む

- `internal/mcp/protocol.go` — エンベロープ、メソッド名、エラーコード。
- `internal/mcp/server.go` — `Serve`、`dispatch`、ツールレジストリ。
- `internal/mcp/tools.go` — rousseau の組み込みツールを登録するヘルパー。
- `internal/cli/mcp.go` — `rousseau mcp` コマンドの配線。
- [Model Context Protocol spec](https://modelcontextprotocol.io) — 外部リファレンス。
