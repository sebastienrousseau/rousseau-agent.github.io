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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/configuration/"
subtitle: "Cada campo de internal/config/config.go."
tags: "configuration, reference"
title: "Referência de configuração"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência de configuração"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Referência de configuração"
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
twitter_description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referência de configuração"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Precedência

O `rousseau` resolve a configuração na ordem **flag > env > arquivo > padrão**. O arquivo fica em `~/.config/rousseau/config.yaml` por padrão; sobrescreva com `--config`.

Variáveis de ambiente usam o prefixo `ROUSSEAU_` com `.` substituído por `_` — então `provider` vira `ROUSSEAU_PROVIDER`, `anthropic.api_key` vira `ROUSSEAU_ANTHROPIC_API_KEY`. `ANTHROPIC_API_KEY` também é reconhecida diretamente (ela é vinculada a `anthropic.api_key` no momento do carregamento).

## Nível superior

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `provider` | string | `claudecli` | Backend LLM: `claudecli`, `anthropic`, `bedrock`, `vertex`, `openai`, `openrouter`, `ollama`. |

## `anthropic` — API direta da Anthropic

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `api_key` | string | *de `ANTHROPIC_API_KEY`* | Bearer para `api.anthropic.com`. Rejeitado se vazio quando o provider é selecionado. |
| `model` | string | `claude-sonnet-4-6` | Identificador do modelo passado para o SDK. |
| `max_tokens` | int64 | `4096` | Limita os tokens de saída por completion. |

Veja [/providers/anthropic/](/pt-BR/providers/anthropic/).

## `bedrock` — AWS Bedrock

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `region` | string | *obrigatório* | Região AWS (`us-east-1`, `eu-west-2`). |
| `model` | string | *obrigatório* | ID do modelo Bedrock (`anthropic.claude-sonnet-4-6-20260101-v1:0`). |
| `profile` | string | *vazio* | Perfil de credenciais de `~/.aws/credentials`. Vazio recorre à cadeia de credenciais padrão da AWS. |
| `max_tokens` | int64 | padrão do SDK | Limita os tokens de saída. |

Veja [/providers/bedrock/](/pt-BR/providers/bedrock/).

## `vertex` — Google Vertex AI

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `project` | string | *obrigatório* | ID do projeto GCP. |
| `region` | string | *obrigatório* | Região Vertex (`us-central1`). |
| `model` | string | *obrigatório* | ID do modelo Anthropic-on-Vertex (`claude-sonnet-4-6@20260101`). |
| `credentials_file` | string | *vazio* | Caminho para o JSON de service-account ou authorized-user. Vazio usa Application Default Credentials. |
| `max_tokens` | int64 | `4096` | Limita os tokens de saída. |

Veja [/providers/vertex/](/pt-BR/providers/vertex/).

## `claudecli` — subprocesso contra o `claude` CLI local

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `binary` | string | `claude` | Executável, resolvido no `$PATH`. |
| `model` | string | *vazio* | Passado para `--model`. Vazio usa o padrão do claude. |
| `permission_mode` | string | *vazio* | Passado para `--permission-mode`. Valores: `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Daemons não-atendidos geralmente precisam de `bypassPermissions`. |
| `extra_args` | []string | `[]` | Antepostos antes de `-p` em cada invocação. Útil para `--add-dir`, `--allowed-tools`, `--disallowed-tools`, `--plugin-dir`. |

Veja [/providers/claudecli/](/pt-BR/providers/claudecli/).

## `openai` / `openrouter` / `ollama` — endpoints compatíveis com OpenAI

Formato compartilhado. `openrouter.base_url` tem padrão `https://openrouter.ai/api/v1`; `ollama.base_url` tem padrão `http://localhost:11434/v1`; `ollama.api_key` tem padrão `not-required`.

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `api_key` | string | *obrigatório* | Token bearer. Não-vazio mesmo para Ollama (qualquer placeholder funciona). |
| `model` | string | *obrigatório* | Identificador do modelo. Não há padrão universal entre endpoints. |
| `base_url` | string | *padrão do provider* | URL completa do endpoint. |
| `max_tokens` | int64 | padrão do SDK | Limita os tokens de saída. |

Veja [/providers/openai-compatible/](/pt-BR/providers/openai-compatible/).

## `log`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `level` | string | `info` | `debug`, `info`, `warn`, `error`. |
| `format` | string | `text` | `text` (humano) ou `json` (produção / agregação de logs). |

## `state`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | Caminho do banco SQLite (modo WAL, `busy_timeout=15s`). |

## `agent`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `system_prompt` | string | *vazio* | Sobrescreve o padrão embutido. |
| `max_iterations` | int | `32` | Limita os round-trips do modelo por `Turn`. |
| `skills_dir` | string | *vazio* | Diretório de arquivos de skill `*.md`. Vazio desabilita skills. |

### `agent.compression`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `enabled` | bool | `false` | Habilita compressão de sessão baseada em LLM. |
| `trigger_messages` | int | `60` | Contagem de mensagens acima da qual a compressão dispara. |
| `keep_recent` | int | `8` | Mensagens recentes preservadas literalmente. |
| `prompt` | string | *embutido* | Sobrescreve a instrução de sumarização padrão. |

### `agent.approver`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`, `deny_all` ou `pattern`. |
| `reason` | string | *vazio* | Motivo de negação exposto ao modelo. |
| `default` | string | `deny` | Fallback quando nenhuma regra `allow` ou `deny` casa (modo pattern). |
| `allow` | []PatternEntry | `[]` | Regras regex de permissão por tool. |
| `deny` | []PatternEntry | `[]` | Regras regex de negação por tool. Deny prevalece sobre allow. |

Cada `PatternEntry` é `{tool: <name>, match: <regex>}`. `tool: ""` casa com qualquer tool; `match: ""` casa com qualquer entrada.

## Blocos de transporte

### `whatsapp`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | Anteposto a cada mensagem de saída. Defina como `" "` para desabilitar. |
| `voice.enabled` | bool | `false` | Transcrição baseada em Whisper para notas de voz recebidas. |
| `voice.binary` | string | `whisper` | Executável do Whisper CLI. |
| `voice.model` | string | *vazio* | Passado para `--model` (`base.en`, `small`). |
| `voice.model_path` | string | *vazio* | Caminho explícito do `.bin`, tem precedência sobre `model`. |
| `voice.language` | string | *vazio* | Passado para `--language`. Vazio detecta automaticamente. |
| `voice.extra_args` | []string | `[]` | Anexado a cada invocação do whisper. |

### `signal`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `binary` | string | `signal-cli` | Executável a invocar em modo daemon JSON-RPC. |
| `account` | string | *obrigatório* | Número de telefone E.164 sob o qual o daemon roda. |
| `extra_args` | []string | `[]` | Inserido entre `-a <account>` e `jsonRpc`. |
| `reply_header` | string | *vazio* | Anteposto a cada mensagem de saída. |
| `allowlist` | []string | `[]` | Números E.164 cujas mensagens são tratadas. Vazio aceita qualquer remetente. |

### `telegram`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `token` | string | *obrigatório* | Token do bot do BotFather. |
| `base_url` | string | `https://api.telegram.org` | Sobrescreve para um servidor Bot API local. |
| `reply_header` | string | *vazio* | Anteposto a cada resposta de saída. |
| `allowlist` | []string | `[]` | IDs de usuário do Telegram cujas mensagens são tratadas. |

### `matrix`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `homeserver_url` | string | *obrigatório* | URL base, ex.: `https://matrix.org`. |
| `access_token` | string | *obrigatório* | Access token do usuário bot. |
| `user_id` | string | *vazio* | MXID completo do usuário bot (`@bot:matrix.org`). Opcional, mas recomendado (supressão de eco de mensagens próprias). |
| `reply_header` | string | *vazio* | Anteposto a cada resposta de saída. |
| `allowlist` | []string | `[]` | IDs Matrix cujas mensagens são tratadas. |

### `slack`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `app_token` | string | *obrigatório* | Token app-level `xapp-*` com `connections:write`. |
| `bot_token` | string | *obrigatório* | Token de bot `xoxb-*` com `chat:write`. |
| `bot_user_id` | string | *vazio* | ID `U…` do próprio bot para prevenção de loop de mensagens próprias. |
| `reply_header` | string | *vazio* | Anteposto a cada mensagem de saída. |
| `allowlist` | []string | `[]` | IDs de usuário Slack cujas mensagens são tratadas. |

### `discord`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `token` | string | *obrigatório* | Token do bot do Developer Portal. |
| `reply_header` | string | *vazio* | Anteposto a cada resposta de saída. |
| `allowlist` | []string | `[]` | IDs de usuário Discord cujas mensagens são tratadas. |

### `sms`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `provider` | string | *obrigatório* | `twilio` ou `vonage`. |
| `from` | string | *obrigatório* | Remetente E.164 ou SID de Messaging Service do Twilio. |
| `account_sid` | string | *obrigatório para twilio* | Account SID do Twilio (`AC…`). |
| `auth_token` | string | *obrigatório* | Auth token do Twilio ou API secret do Vonage. |
| `api_key` | string | *obrigatório para vonage* | API key do Vonage. |
| `base_url` | string | *padrão do provider* | Sobrescreve para endpoints regionais ou de teste. |
| `reply_header` | string | *vazio* | Anteposto a cada mensagem de saída. |

### `imessage`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `base_url` | string | *obrigatório* | URL do servidor BlueBubbles (`http://localhost:1234`). |
| `password` | string | *obrigatório* | Senha do servidor BlueBubbles. |
| `chat_guid` | string | *vazio* | GUID de destino para saída. |
| `poll_interval` | duration | `5s` | Cadência de polling em `/api/v1/message`. |
| `reply_header` | string | *vazio* | Anteposto a cada mensagem de saída. |

### `email`

| Campo | Tipo | Padrão | Efeito |
|---|---|---|---|
| `imap_addr` | string | *obrigatório* | `host:port` para IMAP com TLS (tipicamente `:993`). |
| `imap_username` | string | *obrigatório* | Usuário IMAP. |
| `imap_password` | string | *obrigatório* | Senha IMAP. |
| `mailbox` | string | `INBOX` | Caixa de correio para polling. |
| `poll_interval` | duration | `30s` | Frequência de busca por e-mails UNSEEN. |
| `smtp_addr` | string | *obrigatório* | `host:port` para submissão SMTP (tipicamente `:587`). |
| `smtp_username` | string | *obrigatório* | Usuário SMTP. |
| `smtp_password` | string | *obrigatório* | Senha SMTP. |
| `from` | string | *obrigatório* | Endereço `From` do envelope + cabeçalho. |
| `reply_header` | string | *vazio* | Anteposto ao corpo de cada mensagem de saída. |

## Exemplo completo

```yaml
provider: claudecli

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args: []

log:
  level: info
  format: json

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  system_prompt: ""
  max_iterations: 32
  skills_dir: ~/.local/share/rousseau/skills
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "^./workspace/.*"}
    deny:
      - {tool: bash, match: "rm -rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: false

signal:
  account: "+447900123456"
  allowlist: ["+447900654321"]

telegram:
  token: "123:ABC"
  allowlist: ["12345678"]

matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@bot:matrix.org"
  allowlist: ["@alice:matrix.org"]

slack:
  app_token: "xapp-..."
  bot_token: "xoxb-..."
  bot_user_id: "U0123ABCD"

discord:
  token: "bot-token"
  allowlist: ["123456789012345678"]

sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."

imessage:
  base_url: "http://localhost:1234"
  password: "..."
  poll_interval: "5s"

email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  smtp_addr: "smtp.example.com:587"
  smtp_username: "bot@example.com"
  smtp_password: "..."
  from: "bot@example.com"
  poll_interval: "30s"
```

## Solução de problemas

### `config: unmarshal: 1 error(s) decoding: ...`

O YAML é válido, mas um campo tem o tipo errado. A mensagem de erro nomeia o campo — verifique o tipo em `internal/config/config.go`.

### Sobrescrita por variável de ambiente não é aplicada

O rousseau prefixa variáveis de ambiente com `ROUSSEAU_` e substitui pontos por underscores. `anthropic.model` vira `ROUSSEAU_ANTHROPIC_MODEL`. `ANTHROPIC_API_KEY` é um caso especial ligado diretamente a `anthropic.api_key`.

### `config: read: yaml: line X: found character that cannot start any token`

Indentação por tabs. YAML requer espaços.

### Alterações em `config.yaml` não têm efeito

O rousseau lê a configuração uma única vez na inicialização. Reinicie o daemon.

### Dois valores de configuração parecem estar em vigor

A precedência é **flag > env > arquivo > padrão**. Habilite `log.level: debug` e faça grep por `config.loaded` para ver o valor resolvido.

## Páginas relacionadas

- [Referência: Config Schema](/pt-BR/reference/config-schema/) — todos os campos.
- [Referência: Variáveis de ambiente](/pt-BR/reference/environment-variables/) — matriz de sobrescritas.
- [Referência: Comandos CLI](/pt-BR/reference/cli-commands/) — flags por transporte.
- [Providers](/pt-BR/providers/) — blocos específicos por provider.
- [Transportes](/pt-BR/transports/) — blocos específicos por transporte.

## Leitura complementar

- `internal/config/config.go` — a struct autoritativa.
- `internal/cli/root.go` — onde a configuração é carregada.
- `internal/config/config_test.go` — a matriz de testes da semântica de carregamento.
