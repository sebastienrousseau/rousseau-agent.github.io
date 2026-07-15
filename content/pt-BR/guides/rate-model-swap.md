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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "Guia: troca do modelo a quente"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: troca do modelo a quente"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: troca do modelo a quente"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: troca do modelo a quente"
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

## Por que funciona

O rousseau lê seu provider e modelo do `config.yaml` uma vez no início do processo (`config.Load` em `internal/config/config.go`). O estado da sessão vive no SQLite. Trocar o modelo significa editar a config, reiniciar o daemon e deixar a próxima mensagem inbound ser tratada pelo novo modelo — enquanto cada sessão da qual o modelo anterior participou permanece intacta em `sessions.db`.

Nada sobre o session store está atrelado a um modelo específico. A coluna `payload` (`internal/state/sqlite/schema.sql`) é um blob JSON simples de `agent.Session`; role, content, blocos de tool-use. Qualquer modelo que fale a convenção de blocos de conteúdo da Anthropic (ou seja adaptado pelos adapters de SDK em `internal/llm/*/client.go`) pode continuar de onde o anterior parou.

## Troca dentro do mesmo provider

O caso fácil. Edite o campo do modelo:

```yaml
# was:
anthropic:
  model: claude-sonnet-4-6

# now:
anthropic:
  model: claude-opus-4-6
```

Reinicie:

```sh
systemctl --user restart rousseau-agent
# or, if you're running rousseau chat interactively, quit and relaunch
```

Envie a próxima mensagem. A resposta vem do Opus; o contexto da sessão não muda.

## Troca entre providers

Um pouco mais envolvido porque as formas de bloco de conteúdo variam. Os adapters do rousseau (`internal/llm/anthropic/client.go`, `internal/llm/openai/client.go`) fazem round-trip de valores `agent.Message` pelos tipos nativos do SDK a cada turno. Isso significa:

- **`claudecli` → `anthropic`** — troca limpa. Ambos usam a mesma forma de bloco de conteúdo.
- **`claudecli` → `bedrock` / `vertex`** — troca limpa. Anthropic-em-Bedrock e Anthropic-em-Vertex falam o mesmo formato de messages.
- **Família Anthropic → `openai` / `openrouter` / `ollama`** — Blocos de tool-use são reformatados para o formato function-call da OpenAI. Pares tool_use / tool_result anteriores na sessão fazem round-trip pelo adapter. Deve ser transparente para texto; casos de borda (multi-tool-use em um único turno, streaming parcial) podem renderizar diferente.

Se a sessão tem histórico pesado de tool-use e você está cruzando famílias de provider, teste com uma sessão nova primeiro.

## Trocar o provider de implantação sem tocar no estado

Mesmo session store, config de daemon diferente:

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # change provider + model
systemctl --user restart rousseau-agent
```

`state.path` não mudou, então o mapeamento JID→session (tabela `jid_sessions` em `internal/state/sqlite/jidmap.go`) ainda aponta para o mesmo histórico de conversa para cada remetente do WhatsApp / Slack / Matrix.

## O que é preservado

| Estado | Sobrevive ao restart | Notas |
|---|---|---|
| Transcripts de sessão | Sim | Tabela `sessions`. |
| Índice de recall FTS5 | Sim | Tabela virtual `sessions_fts`. Re-tokenizada no backfill. |
| Mapeamento JID → sessão | Sim | Tabela `jid_sessions`. |
| Jobs de cron | Sim | Tabela `cron_jobs`. |
| Pareamento de device do WhatsApp | Sim | `whatsapp.db` (arquivo separado). |
| Hit de prompt cache da Anthropic | **Não** | O cache é por endpoint. Um novo modelo ou endpoint começa frio. |

## O que é perdido

Os marcadores de prompt-cache da Anthropic (`applyCacheMarkers` em `internal/llm/anthropic/client.go`) vivem dentro do cache efêmero do modelo — não persistem entre restarts do modelo ou provider. Os próximos turnos após uma troca pagam tokens de entrada cheios; turnos subsequentes reconstroem o cache. Vale saber para orçamento de custo mas não para correção.

## Quando trocar vs. começar do zero

Troque no lugar quando:

- A sessão vale a pena preservar e o conteúdo é rico em texto.
- Os modelos são da mesma família (ambos Anthropic, ou via Bedrock/Vertex).
- Você aceita um cache miss único.

Comece do zero quando:

- A sessão tem contexto stale que você não quer que um modelo mais esperto persiga.
- Você está cruzando famílias de provider e quer comportamento determinístico.
- A contagem de tokens está no gatilho de compressão de qualquer forma — comprima e troque de uma vez.

## Testando após uma troca

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# in TUI or via a transport:
> what did we just decide about X?
```

Se a resposta referencia a conversa anterior de forma coerente, a troca está funcionando. Se o modelo se desculpa por "not having context" ou se repete, o round-trip do adapter pode estar perdendo metadata de tool-use — abra um bug ou faça fallback para o modelo anterior.

## Relacionado

- [Providers](/pt-BR/providers/) — cada provider suportado.
- [Configuração](/pt-BR/configuration/) — os nomes exatos dos campos.
- [Guias: Rate limits](/pt-BR/guides/rate-limits/) — discussão de marcador de cache.
- [Guias: Gerenciamento de sessão](/pt-BR/guides/session-management/) — ciclo de vida completo.
