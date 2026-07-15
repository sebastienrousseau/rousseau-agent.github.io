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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "Guia: multi-provedor"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: multi-provedor"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: multi-provedor"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: multi-provedor"
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

## Por que você pode querer isto

O campo `provider` do rousseau é um único escalar (`internal/config/config.go` `Config.Provider`). Um único processo do rousseau fala com exatamente um provider. Quando você quer mais de um — mais comumente, `claudecli` para uso interativo na TUI porque herda uma sessão OAuth, e um provider de API pago (Bedrock, Anthropic direct, Vertex) para daemons em background onde o OAuth de tier por assinatura do `claude` é inconveniente — você roda **dois processos rousseau** com arquivos de config diferentes.

Pareamentos razoáveis:

| Interativo | Sem supervisão | Por quê |
|---|---|---|
| `claudecli` | `anthropic` ou `bedrock` | OAuth para chat no laptop, API key para um daemon em VPS. |
| `claudecli` | `vertex` | O mesmo, no GCP. |
| `anthropic` | `openai` ou `ollama` | Compare respostas, ou caia para um modelo mais barato/local para cron. |
| `claudecli` | `openai` (OpenRouter) | Claude na TUI, modelo OpenRouter barato para resumos agendados. |

## Como o rousseau resolve config

`config.Load` (em `internal/config/config.go`) aplica flag > env > arquivo > padrão. O arquivo que ele lê tem padrão `~/.config/rousseau/config.yaml`, mas a flag persistente `--config` no comando raiz (`internal/cli/root.go`) sobrescreve. Isso te dá uma separação limpa.

## Layout de duas configs

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

Rode cada comando com o arquivo certo:

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## Estado compartilhado vs particionado

Ambos os processos apontam para o mesmo session store SQLite por padrão (`~/.local/share/rousseau/sessions.db`) — e isso geralmente é o que você quer, para que o bridge do WhatsApp e o chat na TUI compartilhem o histórico.

Para particionar totalmente o estado, sobrescreva `state.path` por config:

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

O acesso cross-process ao SQLite é seguro por causa do journaling WAL e do `busy_timeout` de 15 segundos definido por `Open()` em `internal/state/sqlite/store.go`.

## Wiring com systemd

Duas unidades Quadlet, uma por config. O `Exec=` de cada unidade inclui `--config /home/rousseau/.config/rousseau/<name>.yaml`:

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

Veja [Implantação](/pt-BR/deployment/) para a unidade base.

## Políticas de approver por config

Providers diferentes merecem aprovações diferentes. O `claudecli` interativo pode ficar em `mode: allow_all` com segurança porque o Claude Code tem sua própria UI de aprovação por call. O daemon Bedrock/Anthropic deve rodar em `mode: pattern` com `default: deny`. Ponha cada um sob seu próprio YAML.

## Testando

Confirme que cada processo fala com o endpoint correto:

```sh
# Interactive shows the claudecli subprocess path in strace / lsof
lsof -c rousseau | grep -E 'claude|CLAUDE'

# Background shows outbound HTTPS to bedrock-runtime.<region>.amazonaws.com
ss -tanp | grep rousseau
```

## O que isto NÃO te dá

- **Não é roteamento por requisição.** O rousseau não cai de um provider para outro dentro de um único turno. Falha do provider configurado aparece como `whatsapp.handler_failed` / `turn.failed` e o modelo não repete contra um provider diferente. Isso é item de roadmap.
- **Não é cache compartilhado.** O prompt cache da Anthropic (veja `applyCacheMarkers` em `internal/llm/anthropic/client.go`) é por endpoint. Um hit no Anthropic direct não é um hit no Bedrock, mesmo para a mesma família de modelo.

## Relacionados

- [Providers](/pt-BR/providers/) — comparação dos cinco tipos de provider.
- [Configuração](/pt-BR/configuration/) — cada botão.
- [Referência: Variáveis de ambiente](/pt-BR/reference/environment-variables/) — overrides por env.
- [Guias: Implantação em produção](/pt-BR/guides/production-deployment/).
