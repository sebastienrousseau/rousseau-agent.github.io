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
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "Códigos de saída"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Códigos de saída"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Códigos de saída"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Códigos de saída"
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

## Códigos de saída

O CLI do rousseau é deliberadamente conservador — dois códigos de saída cobrem todos os caminhos.

| Código | Emitido por | Significado |
|---|---|---|
| 0 | `cmd/rousseau/main.go` via `cli.Execute` | Comando completado com sucesso. Daemons saem com 0 em shutdown gracioso (SIGINT / SIGTERM). |
| 1 | `cmd/rousseau/main.go` via `cli.Execute` | Comando falhou. A string de erro é impressa em stderr. Cada falha — erro de parse de config, falha de auth de provider, panic de transporte, erro de wiring de ferramenta — mapeia para este código. |

`rousseau doctor` segue a mesma convenção: sai com 0 quando toda checagem passa, sai com 1 quando qualquer checagem é `fail`. Warnings e linhas de nível info não afetam o código de saída.

Releases futuras podem dividir falhas em códigos distintos (config vs runtime vs rede). Hoje, trate qualquer saída não-zero como retryable mas exigindo inspeção de log.

## Tratamento de sinais

`cmd/rousseau/main.go` instala um signal handler que cancela o `context.Context` raiz em `SIGINT` e `SIGTERM`. Cada componente de longa vida (agent loop, transporte, cron scheduler, servidor MCP) honra o cancelamento de context, então o caminho de shutdown é:

1. `SIGINT` / `SIGTERM` recebido.
2. Context raiz é cancelado.
3. Transportes chamam `Stop()` em si mesmos, fazendo flush de mensagens em voo.
4. Cron scheduler para de aceitar novos disparos; disparos rodando completam.
5. `Close()` do session store é chamado via `defer`, fazendo checkpoint do WAL.
6. `Execute` retorna 0.

`SIGKILL` não pode ser capturado. Se o daemon leva `kill -9` no meio de um turno, o WAL do session store protege contra corrupção mas o turno em voo não é persistido. O próximo launch retoma do último estado salvo.

## Política de restart do systemd

Para a unidade Quadlet de referência:

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` reinicia em qualquer saída não-zero; combinado com a convenção de código de saída do rousseau isso significa: saída 0 (`SIGTERM` de `systemctl stop`) não reinicia, saída 1 sim.

Para daemons que batem em erros persistentes (config ruim, auth de provider errada), `on-failure` vai fazer thrash. Observe `journalctl` para a razão da falha antes de assumir que o loop de retry vai se recuperar.

## Semântica de probes Kubernetes

O rousseau não envia endpoint HTTP de liveness/readiness por design. Probes Kubernetes devem ser ou:

- Probes `exec` rodando `rousseau doctor --config /etc/rousseau/config.yaml` (retorna 0 em healthy, 1 em falha), ou
- Ausentes, com o pod contando com `restartPolicy: Always` e o próprio tratamento de erro do daemon.

`rousseau doctor` é barato (~50ms) então é uma boa liveness probe. Não use como readiness probe — um `fail` em `provider.claudecli.binary` não deveria tirar o pod de rotação se a falha não vai se autocorrigir.

## Erros tratados

Erros que produzem código de saída 1 pela superfície de erro do CLI incluem:

- **Falha de carregamento de config** — erro de parse YAML, campo desconhecido, tipo inválido.
- **Falha de auth de provider** — API key ausente, credenciais inválidas, região Bedrock / Vertex inválida.
- **Falha de startup de transporte** — token ausente, host IMAP/SMTP inalcançável, erro de protocolo whatsmeow.
- **Falha de abertura de store** — permissão negada em `~/.local/share/rousseau/`, disco cheio.
- **Falha de checagem de doctor** — qualquer linha `fail` faz doctor retornar saída 1.
- **Falha de parse de expressão cron** — `rousseau cron add` valida antes de persistir.

## Panics não tratados

`go test -race` roda em cada build de CI, então panics são extremamente raros. Quando acontecem, o runtime Go imprime o panic + stack trace em stderr e sai com um código não-zero do runtime — tipicamente 2, mas essa é uma convenção do Go e não algo que o rousseau controla.

Para produção, envolva o daemon em um supervisor que captura stderr em saída anormal e reporta o trace.

## Próximo

- [Guia do usuário: CLI](/pt-BR/user-guide/cli/) — cada comando.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — expor o sinal slog além do código de saída.
- [Solução de problemas](/pt-BR/troubleshooting/) — o que fazer quando o código de saída não é suficiente.
