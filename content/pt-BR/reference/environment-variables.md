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
date: "July 13, 2026"
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
changefreq: "monthly"
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "Referência: variáveis de ambiente"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência: variáveis de ambiente"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referência: variáveis de ambiente"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referência: variáveis de ambiente"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Como o rousseau lê o ambiente

Dois mecanismos, nesta ordem (veja `config.Load` em `internal/config/config.go`):

1. **Binding automático de env do Viper.** `SetEnvPrefix("ROUSSEAU")` mais `SetEnvKeyReplacer(".", "_")` significa que cada campo de config é acessível como `ROUSSEAU_<UPPER_SNAKE>`. Então `provider` vira `ROUSSEAU_PROVIDER`, `agent.approver.mode` vira `ROUSSEAU_AGENT_APPROVER_MODE`.
2. **Override explícito.** `ANTHROPIC_API_KEY` é lido diretamente do ambiente e forçado para `anthropic.api_key`, para que a convenção padrão do SDK Anthropic simplesmente funcione. Nenhuma outra chave é pega implicitamente.

Todo o resto nesta página é ou uma variável mapeada pelo Viper, uma variável gerenciada por SDK que o rousseau não toca mas a biblioteca subjacente sim, ou um path XDG usado para computar padrões.

A precedência se mantém: **flag > env > file > default**.

## Prefixo `ROUSSEAU_*`

Cada tag `mapstructure` em `internal/config/config.go` é acessível via `ROUSSEAU_<UPPER_SNAKE_PATH>`. Exemplos selecionados — lista completa segue o struct de config:

| Variável | Categoria | Padrão | Descrição |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | core | `claudecli` | Identificador de provider: `claudecli`, `anthropic`, `openai`, `openrouter`, `ollama`, `bedrock`, `vertex`. |
| `ROUSSEAU_LOG_LEVEL` | logging | `info` | Nível de slog: `debug`, `info`, `warn`, `error`. |
| `ROUSSEAU_LOG_FORMAT` | logging | `text` | `text` ou `json`. |
| `ROUSSEAU_STATE_PATH` | state | `$HOME/.local/share/rousseau/sessions.db` | DSN do session store. |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | agent | `32` | Limite de iteração de tool-use por turno. |
| `ROUSSEAU_AGENT_APPROVER_MODE` | agent | `` | `allow_all`, `deny_all`, `pattern`. |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | agent | `` | Para `pattern`: `allow` ou `deny` em calls não correspondidas. |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | agent | `false` | Liga o compressor LLM. |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | agent | `60` | Comprime quando a contagem de mensagens excede isso. |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | agent | `8` | Quantas mensagens recentes preservar na íntegra. |
| `ROUSSEAU_AGENT_SKILLS_DIR` | agent | `$HOME/.local/share/rousseau/skills` | Diretório de skills. |
| `ROUSSEAU_ANTHROPIC_API_KEY` | provider | — | Igual a `ANTHROPIC_API_KEY`. |
| `ROUSSEAU_ANTHROPIC_MODEL` | provider | `claude-sonnet-4-6` | ID de modelo Anthropic. |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | provider | `4096` | Máx de tokens de resposta. |
| `ROUSSEAU_CLAUDECLI_BINARY` | provider | `claude` | Nome do executável para o provider `claudecli`. |
| `ROUSSEAU_CLAUDECLI_MODEL` | provider | — | Passado para `claude --model`. |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | provider | — | `default`, `acceptEdits`, `bypassPermissions`, `plan`, etc. |
| `ROUSSEAU_OPENAI_API_KEY` | provider | — | Bearer para endpoints OpenAI-compat. |
| `ROUSSEAU_OPENAI_MODEL` | provider | — | ID de modelo. |
| `ROUSSEAU_OPENAI_BASE_URL` | provider | — | Sobrescreve o endpoint. |
| `ROUSSEAU_OPENROUTER_API_KEY` | provider | — | Bearer para OpenRouter. |
| `ROUSSEAU_OPENROUTER_MODEL` | provider | — | Slug do modelo. |
| `ROUSSEAU_OPENROUTER_BASE_URL` | provider | `https://openrouter.ai/api/v1` | Sobrescreve endpoint. |
| `ROUSSEAU_OLLAMA_MODEL` | provider | — | Tag do modelo. |
| `ROUSSEAU_OLLAMA_BASE_URL` | provider | `http://localhost:11434/v1` | Endpoint local do Ollama. |
| `ROUSSEAU_BEDROCK_REGION` | provider | — | Região AWS. |
| `ROUSSEAU_BEDROCK_MODEL` | provider | — | ID de modelo Bedrock. |
| `ROUSSEAU_BEDROCK_PROFILE` | provider | — | Profile nomeado da AWS. |
| `ROUSSEAU_VERTEX_PROJECT` | provider | — | Projeto GCP. |
| `ROUSSEAU_VERTEX_REGION` | provider | — | Região Vertex. |
| `ROUSSEAU_VERTEX_MODEL` | provider | — | Modelo Anthropic-em-Vertex. |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | provider | — | Path para JSON de service-account. |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | transport | `💎 *Rousseau Agent*\n\n` | Prependado a cada mensagem outbound do WhatsApp. |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | transport | `false` | Habilita transcrição whisper de voice notes. |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | transport | `whisper` | Executável whisper.cpp. |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | transport | — | Nome do modelo whisper (`base.en`, `small`). |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | transport | — | Path .bin explícito (tem precedência sobre model). |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | transport | — | Código ISO; vazio faz auto-detect. |
| `ROUSSEAU_SIGNAL_BINARY` | transport | `signal-cli` | Executável signal-cli. |
| `ROUSSEAU_SIGNAL_ACCOUNT` | transport | — | Número de telefone E.164. |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | transport | — | Header de resposta. |
| `ROUSSEAU_TELEGRAM_TOKEN` | transport | — | Token da Bot API. |
| `ROUSSEAU_TELEGRAM_BASE_URL` | transport | — | Sobrescreve endpoint da Bot API. |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | transport | — | URL base do homeserver. |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | transport | — | Access token do Matrix. |
| `ROUSSEAU_MATRIX_USER_ID` | transport | — | MXID completo (`@bot:example.org`). |
| `ROUSSEAU_SLACK_APP_TOKEN` | transport | — | Token de app-level `xapp-…`. |
| `ROUSSEAU_SLACK_BOT_TOKEN` | transport | — | Token de bot `xoxb-…`. |
| `ROUSSEAU_SLACK_BOT_USER_ID` | transport | — | User id do bot para supressão de self-echo. |
| `ROUSSEAU_DISCORD_TOKEN` | transport | — | Token de bot Discord. |
| `ROUSSEAU_SMS_PROVIDER` | transport | — | `twilio` ou `vonage`. |
| `ROUSSEAU_SMS_FROM` | transport | — | Número de remetente. |
| `ROUSSEAU_SMS_ACCOUNT_SID` | transport | — | SID de conta Twilio. |
| `ROUSSEAU_SMS_AUTH_TOKEN` | transport | — | Segredo Twilio/Vonage. |
| `ROUSSEAU_SMS_API_KEY` | transport | — | API key Vonage. |
| `ROUSSEAU_SMS_BASE_URL` | transport | — | Sobrescreve para endpoints regionais ou testes. |
| `ROUSSEAU_IMESSAGE_BASE_URL` | transport | — | URL do servidor BlueBubbles. |
| `ROUSSEAU_IMESSAGE_PASSWORD` | transport | — | Senha do BlueBubbles. |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | transport | — | Alvo de outbound. |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | transport | `2s` | String de duration. |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | transport | — | Servidor IMAP. |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | transport | — | Usuário IMAP. |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | transport | — | Senha IMAP. |
| `ROUSSEAU_EMAIL_MAILBOX` | transport | — | Pasta a observar. |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | transport | — | String de duration. |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | transport | — | Host de submissão SMTP. |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | transport | — | Usuário SMTP. |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | transport | — | Senha SMTP. |
| `ROUSSEAU_EMAIL_FROM` | transport | — | Endereço From. |

**Arrays de allowlist** (`ROUSSEAU_SLACK_ALLOWLIST`, `ROUSSEAU_DISCORD_ALLOWLIST`, `ROUSSEAU_TELEGRAM_ALLOWLIST`, …) são suportados pelo Viper, mas parsing de string de env separada por vírgula é chato — prefira defini-los em `config.yaml`.

## Vars de env explícitas (fora do prefixo ROUSSEAU_)

| Variável | Fonte | Propósito |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load` (`internal/config/config.go` linha 275) | Popula `anthropic.api_key`. Convenção padrão do SDK Anthropic. |
| `HOME` | `internal/cli/init.go` | Usado por `rousseau init` para computar o path padrão de estado. |

## Variáveis pertencentes ao SDK que o rousseau não toca

Algumas bibliotecas de provider pegam seu próprio ambiente. O rousseau não as lê por conta própria, mas elas influenciam o comportamento quando o provider correspondente é selecionado:

| Variável | Consumidor | Notas |
|---|---|---|
| `AWS_PROFILE`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2` (Bedrock) | A cadeia padrão de credenciais. Prefira credenciais baseadas em IRSA ou profile a chaves estáticas. |
| `GOOGLE_APPLICATION_CREDENTIALS` | bibliotecas de auth do Google (Vertex) | Path para um JSON de service-account. Substituído por `vertex.credentials_file` em `config.yaml` se definido. |
| `OPENAI_API_KEY` | Os clientes Go OpenAI upstream tipicamente leem isso | O rousseau explicitamente conecta a chave via `openai.api_key`; nada implícito. |
| `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | Go net/http | Variáveis universais de proxy do Go. Úteis para caminhos de egress corporativo. |

## Variáveis de path XDG

O rousseau segue a XDG Base Directory Specification para estado e config, com dois fallbacks:

| Variável | Efeito |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` é o path padrão de config (referenciado em `internal/cli/root.go`). |
| `XDG_DATA_HOME` | Path padrão de estado `$XDG_DATA_HOME/rousseau/sessions.db` (referenciado por `whatsapp.go`, `skills.go`, `init.go`). |
| `HOME` | Fallback quando as variáveis XDG estão vazias; o rousseau usa `os.UserHomeDir()` em `internal/config/config.go`. |

A unidade Quadlet de contêiner em `docker/rousseau-agent.container` define ambos `HOME=/home/rousseau` e `XDG_DATA_HOME=/home/rousseau/.local/share`.

## Higiene de segredos

Armazene segredos em um de três lugares:

1. **Um `EnvironmentFile=` de unidade systemd** — `chmod 0600`, dono root ou dono do usuário conforme apropriado. Referenciado da unidade Quadlet — veja o [tutorial de deploy VPS](/pt-BR/tutorials/deploy-to-a-vps/).
2. **Um arquivo `.env` carregado pelo seu shell.** Só para uso desktop; mantenha fora de source control.
3. **Um secret manager.** AWS Secrets Manager, HashiCorp Vault, ou `pass`/`gopass`. Faça pipe do valor para o processo no start.

Nunca faça commit de segredos em `config.yaml`. `config.yaml` é o lugar certo para allowlists, base URLs e configuração não-secreta; é o lugar errado para API keys e tokens de bot.

## Solução de problemas

### `ROUSSEAU_...` definido mas o rousseau ainda usa o padrão

Env vars são lidas no start. Reinicie o daemon após export. Verifique também a regra de transformação: pontos na key de config viram underscores, e o prefixo é `ROUSSEAU_` (maiúscula, exato).

### `ANTHROPIC_API_KEY` aparentemente ignorado

A env var só é consultada quando `provider: anthropic` está ativo. Sob `provider: claudecli`, o CLI `claude` lê suas próprias credenciais.

### Valor diferente em hosts diferentes

A precedência é **flag &gt; env &gt; file &gt; default**. Se uma flag é definida (do `ExecStart` da unidade systemd por exemplo), ela vence tanto env quanto file.

### `GOOGLE_APPLICATION_CREDENTIALS` ilegível dentro do contêiner

Garanta que o arquivo é bind-mountado somente leitura no contêiner e que o UID do contêiner (1000 por padrão) pode lê-lo.

## Páginas relacionadas

- [Configuração](/pt-BR/configuration/) — cada campo de config com padrão.
- [Referência: Schema de config](/pt-BR/reference/config-schema/) — a estrutura YAML.
- [Referência: Comandos CLI](/pt-BR/reference/cli-commands/) — flags por transporte.
- [Guias: Onboarding Corporativo](/pt-BR/guides/enterprise-onboarding/) — manejo de segredos em produção.
- [Implantação](/pt-BR/deployment/) — opções de gestão de segredos.

## Leitura adicional

- `internal/config/config.go` — `Load` define o prefixo de env e o replacer de key ponto-underscore.
- `internal/cli/root.go` — onde `Load` é chamado.
