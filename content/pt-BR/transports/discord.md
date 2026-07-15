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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Transporte Discord"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Discord"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Discord"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Discord"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Um passo a passo do Discord Developer Portal, quais intents do Gateway o rousseau precisa e por quê, o cálculo do bitmask de permissões explicado, e os modos de falha para configurações incorretas comuns. Leia <code>internal/transport/discord/client.go</code> junto com esta página.</p></aside>

## Visão geral

O transporte Discord (`internal/transport/discord/`) fala diretamente com o protocolo Discord Gateway v10 — sem SDK de terceiros. WebSocket para entrada (`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`); REST para saída (`POST /channels/{id}/messages`).

## Pré-requisitos

1. **Um Discord Application com usuário Bot.** Crie em https://discord.com/developers/applications → **New Application** → aba **Bot** → **Add Bot**.
2. **Um token de bot** (aba Bot → **Reset Token** → copie o token — você só o vê uma vez).
3. **Intent Message Content habilitada** (aba Bot → **Privileged Gateway Intents**). Sem isso, o Gateway remove o texto da mensagem de cada evento e o rousseau verá corpos vazios.
4. **O bot convidado para pelo menos um servidor** (ou DMs habilitadas). Gere a URL de convite em **OAuth2 → URL Generator** com o escopo `bot` e as permissões `Send Messages` + `Read Message History`.

## Configuração

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| Campo | Padrão | Efeito |
|---|---|---|
| `token` | *obrigatório* | Token do bot do Developer Portal. |
| `reply_header` | *vazio* | Prefixado em toda resposta enviada. |
| `allowlist` | `[]` | IDs de usuário do Discord cujas mensagens são tratadas. |

## Linha de comando

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Intents do Gateway

O rousseau solicita três intents (`internal/transport/discord/client.go`):

| Intent | Bit | Finalidade |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | Mensagens em canais de servidor. |
| `DIRECT_MESSAGES` | `1 << 12` | DMs para o bot. |
| `MESSAGE_CONTENT` | `1 << 15` | Preenche o campo `content`. **Deve estar habilitada no portal.** |

Sem a intent Message Content, os eventos `MESSAGE_CREATE` chegam com `content` vazio e o rousseau registrará `discord.empty_body`.

## Heartbeat

O transporte honra o `heartbeat_interval` do Gateway vindo do opcode Hello, enviando Heartbeat + monitorando `heartbeat_ack`. ACKs perdidos fecham o socket e permitem que o systemd reinicie o processo.

## Cabeçalho de resposta

O Discord renderiza `**texto**` como negrito e não exige nenhum formato específico de cabeçalho. Sobrescreva conforme necessário:

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## Calculadora de bits de permissão

O Discord usa um bitmask para codificar as permissões de canal de um bot. Cada permissão é uma potência de 2. Comuns para o rousseau:

| Permissão | Bit |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

Para conceder várias permissões, faça OR entre os bits e cole o inteiro resultante no parâmetro `permissions=` do OAuth2 URL Generator:

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">Auxiliar do portal</span><p>O <em>OAuth2 URL Generator</em> do developer portal permite marcar checkboxes de permissão e calcula o inteiro para você. Salve a URL gerada nos favoritos — ela permite que administradores de servidor convidem o bot para qualquer servidor Discord.</p></aside>

## Ciclo de vida do Gateway

O Gateway é stateful:

```
Client                        Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat every N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (a user typed)
  │   ─── (rousseau handles + POSTs reply)
  │
  │   ◀── Disconnect (code 4009: session timed out)
  │   ─── RESUME (session_id) or re-IDENTIFY
```

O cliente monitora `heartbeat_ack`. Se um ack for perdido, o socket fecha e o processo termina — o systemd ou o runtime do contêiner reinicia.

## Modos de falha

| Sintoma | Correção |
|---|---|
| Bot vê mensagens vazias | Habilite a intent Message Content no developer portal. |
| Gateway fecha com código 4004 | Token inválido. Regere. |
| Bot não consegue ver nenhum canal | Confirme que o convite OAuth2 incluiu o escopo `bot`. |
| 403 no envio | O bot não tem permissão `Send Messages` naquele canal. |
| Código 4014 no Identify | Solicitou uma intent para a qual seu app não foi aprovado (geralmente Message Content em um bot com 100+ servidores). Verifique seu bot. |
| Código 4009 (sessão expirou) | Normal após ociosidade prolongada. O Rousseau reconecta de forma transparente. |

## Solução de problemas

### Gateway 4013 (Invalid Intents)

Você está solicitando um bit de intent que não existe. Isso geralmente significa um descompasso entre as constantes de intent da biblioteca cliente e o mapa atual de intents do Discord. O rousseau monta o bitmask de intents em `internal/transport/discord/client.go`; atualize para a última versão se você vir 4013 após uma mudança de API do Discord.

### Bot recebe eventos, mas não responde

Descompasso da allowlist. O valor de `--allow` deve ser o ID numérico do usuário Discord (não o username, não o nome de exibição). Recupere-o no Discord: habilite Developer Mode em *User Settings &gt; Advanced*, depois clique com o botão direito num usuário &gt; *Copy User ID*.

### DMs funcionam, mas canais de guild não

Falta a intent `GUILD_MESSAGES`, ou o bot não foi convidado para a guild. As permissões de guild são separadas das permissões de DM — o bot precisa ter permissão `Read Messages` para o canal.

### `429 Too Many Requests` no envio

O Discord impõe um rate limit global de 50 req/s por bot, além de limites por canal. Sob carga sustentada, o rousseau atualmente não tenta novamente — o chamador precisa fazer backoff. Veja [Guias: Rate limits](/pt-BR/guides/rate-limits/).

### O status online do bot oscila

O Discord considera um bot offline após ~40s sem heartbeat. A linha de log `discord.heartbeat_missed` indica problema de rede ou daemon com CPU insuficiente. Verifique se o contêiner tem CPU suficiente alocada.

## Páginas relacionadas

- [Primeiros passos: Primeiro transporte](/pt-BR/getting-started/first-transport/) — passo a passo de ponta a ponta.
- [Configuração](/pt-BR/configuration/) — o bloco de configuração `discord`.
- [Transportes](/pt-BR/transports/) — transportes similares.
- [Guias: Auditoria &amp; Políticas de Aprovação](/pt-BR/guides/audit-approval-policies/) — política para servidores Discord.
- [Implantação](/pt-BR/deployment/) — executando o Discord em um contêiner Podman.

## Leitura adicional

- `internal/transport/discord/client.go` — conexão do Gateway, heartbeat, event pump.
- `internal/cli/discord.go` — integração da CLI.
- `internal/transport/router.go` — aplicação da allowlist.
- [Documentação da API do Discord: Gateway](https://discord.com/developers/docs/topics/gateway).
- [Documentação da API do Discord: Permissions](https://discord.com/developers/docs/topics/permissions).
