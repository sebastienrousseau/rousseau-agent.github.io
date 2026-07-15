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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Transporte Signal"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Signal"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Signal"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Signal"
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

O transporte Signal (`internal/transport/signal/`) delega ao `signal-cli` (https://github.com/AsamK/signal-cli) em seu modo daemon JSON-RPC.

`signal-cli --output=json -a <account> jsonRpc` transmite JSON-RPC 2.0 pela stdin/stdout: requisições `send` de saída entregam mensagens; chegadas de entrada aparecem como notificações `receive`.

## Pré-requisitos

Duas coisas precisam estar prontas antes que o rousseau possa falar com o Signal:

1. **`signal-cli` no `$PATH`** (ou um valor `binary` explícito na configuração).
2. **Conta registrada / vinculada fora da banda.**

O registro de conta está deliberadamente fora do escopo do rousseau. Dois caminhos suportados (segundo a documentação do `signal-cli`):

- **Registrar um novo número.** `signal-cli register` inicia a verificação por SMS ou voz. Conclua com `signal-cli verify <code>`. O número acaba pertencendo ao daemon.
- **Vincular como dispositivo secundário.** `signal-cli link` imprime um URI `tsdevice://`; escaneie-o no aplicativo móvel Signal em **Configurações → Dispositivos Vinculados**. O número continua pertencendo ao telefone; o daemon atua como secundário.

Ambos os fluxos persistem o estado em `~/.local/share/signal-cli/`. Faça bind-mount desse diretório no contêiner se você implantar via Podman.

## Configuração

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| Campo | Padrão | Efeito |
|---|---|---|
| `binary` | `signal-cli` | Executável a ser invocado. |
| `account` | *obrigatório* | Número de telefone E.164 sob o qual o daemon opera. |
| `extra_args` | `[]` | Inseridos entre `-a <account>` e `jsonRpc`. Úteis para `--config <path>` e `--verbose`. |
| `reply_header` | *vazio* | Prefixado em toda resposta enviada. |
| `allowlist` | `[]` | Números E.164 cujas mensagens são tratadas. Vazio aceita todos os remetentes. |

## Linha de comando

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

As flags espelham o bloco de configuração. `--allow` pode ser repetido.

## Fluxo de mensagens

- **Entrada.** `signal-cli` emite uma notificação JSON-RPC `receive` para cada mensagem que chega. O rousseau faz o parse, descarta o que não está na allowlist e entrega o corpo ao `Handler`.
- **Saída.** O rousseau escreve uma requisição JSON-RPC `send` na stdin do `signal-cli`. Os ACKs de entrega chegam pelo mesmo canal.

## Timeouts

O transporte não impõe seu próprio timeout ao subprocesso. A camada de rede do próprio `signal-cli` gerencia reconexões ao servidor Signal. Se o processo terminar, o rousseau não o reiniciará — um `Restart=on-failure` do systemd (que o Quadlet de referência já define) reinicia todo o daemon rousseau, levando o `signal-cli` junto.

## Modos de falha

| Sintoma | Correção |
|---|---|
| `signal-cli` sai imediatamente | Conta não está registrada ou vinculada. Complete o registro fora da banda. |
| Notificações `receive` nunca chegam | Verifique se a conta não está vinculada em outro lugar consumindo a fila. |
| Erros de parse JSON | Confirme que sua versão do `signal-cli` é 0.13+. Versões anteriores usavam um envelope diferente. |
