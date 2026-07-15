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
changefreq: "monthly"
description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/matrix/"
subtitle: "Matrix client-server API with long-polling /sync."
tags: "transports, Matrix"
title: "Transporte Matrix"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Matrix"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Matrix"
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
twitter_description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Matrix"
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

## Visão geral

O transporte Matrix (`internal/transport/matrix/`) fala diretamente com a API cliente-servidor Matrix — sem SDK de terceiros. Long-polling em `/sync` para entrada; `/rooms/{room}/send/{event_type}/{txn_id}` para saída.

Funciona contra qualquer homeserver compatível com a spec: Synapse, Dendrite, Conduit.

## Pré-requisitos

1. **Uma conta de bot** no homeserver de sua escolha. Registre-se pelo cliente Matrix padrão ou pela API de administração do homeserver.
2. **Um access token** para essa conta. Faça login com o bot em um cliente Matrix normal uma vez, depois copie o token em **Configurações → Ajuda & Sobre → Access Token**. Alternativamente, use a API de login diretamente:

   ```sh
   curl -X POST https://matrix.org/_matrix/client/v3/login \
     -H 'Content-Type: application/json' \
     -d '{"type":"m.login.password","user":"bot","password":"..."}'
   ```

3. **O MXID completo do bot** (ex.: `@rousseau-bot:matrix.org`) para supressão de eco das próprias mensagens.

## Configuração

```yaml
matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@rousseau-bot:matrix.org"
  reply_header: ""
  allowlist:
    - "@alice:matrix.org"
    - "@bob:example.com"
```

| Campo | Padrão | Efeito |
|---|---|---|
| `homeserver_url` | *obrigatório* | URL base (`https://matrix.org`). |
| `access_token` | *obrigatório* | Access token do usuário bot. |
| `user_id` | *vazio* | MXID completo do usuário bot. Opcional mas recomendado (supressão de eco das próprias mensagens). |
| `reply_header` | *vazio* | Prefixado em toda resposta enviada. |
| `allowlist` | `[]` | MXIDs cujas mensagens são tratadas. |

## Linha de comando

```sh
rousseau matrix \
  --homeserver-url https://matrix.org \
  --access-token syt_... \
  --user-id @rousseau-bot:matrix.org \
  --allow @alice:matrix.org
```

## Long-polling

`PollTimeout` tem padrão de 30 segundos. O cursor `since` de cada resposta do `/sync` fica armazenado em memória e é usado na próxima chamada, de modo que as mensagens nunca são reentregues durante o ciclo de vida do processo. Ao reiniciar, o daemon retrocede para o cursor mais antigo ainda vivo que o homeserver retorna — esta é a semântica normal do `sync` e corresponde a todo cliente Matrix.

## Convites para salas

O bot já precisa ser membro de qualquer sala em que deva responder. Convide-o a partir de um cliente Matrix normal. O rousseau não aceita convites automaticamente; entrar em salas está fora do escopo.

## Modos de falha

| Sintoma | Correção |
|---|---|
| 401 em `/sync` | Access token expirado ou invalidado. Faça login novamente. |
| Bot nunca vê uma mensagem | Confirme que o bot é membro da sala, não apenas convidado. |
| Loop de eco das próprias mensagens | Defina `user_id` na configuração para que o rousseau possa filtrar suas próprias mensagens. |
