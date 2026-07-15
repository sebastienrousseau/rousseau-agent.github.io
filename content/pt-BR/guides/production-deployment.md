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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "Guia: implantação em produção"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: implantação em produção"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: implantação em produção"
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
twitter_description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: implantação em produção"
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

## Leia isso depois

A unidade Quadlet de referência em `docker/rousseau-agent.container` cobre a história de "como rodar o rousseau". Este guia cobre o que você adiciona ao redor antes de chamar de produção: logs, backups, health e higiene de processo.

## Envio de logs

O rousseau escreve logs estruturados para stderr via `log/slog` (`internal/cli/root.go`). Quando você o roda sob systemd, esse stderr vai para o journal. Opções para enviar para fora do host:

| Ferramenta | Encaixe | Notas |
|---|---|---|
| Vector (`vector.dev`) | Melhor padrão. | Fonte `journald` + um filtro descartando DEBUG. Envie para Loki, Datadog, S3, o que for. |
| Promtail + Loki | Se você já roda Grafana. | A fonte `journal` do Loki funciona diretamente contra `journalctl -o json`. |
| Datadog Agent | Se Datadog é o padrão da org. | O agent DD tem um tail journald. JSON estruturado parseia nativamente. |
| Fluent Bit | Alternativa de footprint pequeno. | Defina `log.format: json` em `config.yaml`; o input `systemd` do Fluent Bit parseia. |

Configure `log.format: json` (`internal/config/config.go` `LogConfig.Format`) incondicionalmente em produção. Saída em texto é desenhada para `less`, não para parsing de máquina.

Veja [Guias: Observabilidade](/pt-BR/guides/observability/) para uma receita completa de pipeline Loki.

## Backup do session store

O diretório de estado `~/.local/share/rousseau/` é o único estado durável do rousseau. Faça backup dele todas as noites.

Duas abordagens:

**1. SQLite `.backup` (recomendado).**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` usa a API online do SQLite — seguro mesmo com o daemon escrevendo. Veja [Referência: Session store](/pt-BR/reference/session-store/).

**2. Snapshot de filesystem.**

Como o journaling WAL está ligado (`Open()` em `internal/state/sqlite/store.go`), `restic` e `borg` podem snapshotar os arquivos brutos com o daemon rodando. WAL garante uma imagem consistente point-in-time.

Não:

- Copie o arquivo `.db` com `cp` com o daemon rodando a menos que você também copie `-wal` e `-shm`.
- Armazene backups no mesmo disco.
- Pule o arquivo de credenciais de device do WhatsApp — perdê-lo significa re-escanear o QR.

## Health checks

`rousseau status` (`internal/cli/status.go`) sai com 0 se saudável, não-zero em problema. Use como probe de health do systemd:

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

Para um probe mais rico, roteirize uma checagem que:

1. Roda `rousseau status`.
2. Confirma que a última escrita do session store foi recente (`stat sessions.db -c %Y` comparado com now).
3. Checa o uptime do contêiner via `podman inspect`.

O rousseau não expõe um `/healthz` HTTP. Se sua plataforma requer um (readiness probes do Kubernetes), veja [Guias: Implantação Kubernetes](/pt-BR/guides/kubernetes-deployment/) — você envolve o rousseau em um pequeno sidecar amigável a `curl`.

## Restart rolling

Como o estado é um único arquivo SQLite, o daemon é genuinamente single-instance. Um restart rolling é: pare, substitua a imagem, inicie. Nenhum warm-up necessário.

```sh
podman pull localhost/rousseau-agent:local     # or rebuild locally
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

Sequência de log esperada (de `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

Se o daemon não emitir `whatsapp.connected` dentro de ~15 segundos, faça rollback.

## Múltiplos transportes em um host

Você pode querer o mesmo session store compartilhado por WhatsApp e Slack. Duas formas:

- **Múltiplas unidades Quadlet** — uma para cada transporte, cada uma apontando para o mesmo `state.path`. WAL + `busy_timeout` (veja `Open()` em `internal/state/sqlite/store.go`) torna escritores concorrentes seguros.
- **Um binário, um transporte por invocação.** Os comandos de transporte do rousseau são single-transport (`whatsapp`, `slack`, `signal`, …). Para rodar dois transportes você roda dois processos.

## Mudanças de configuração com zero-downtime

O rousseau não faz hot-reload de `config.yaml`. Mudanças de config requerem restart. `SIGHUP` não é conectado para reload.

Workflow prático:

1. Edite `~/.config/rousseau/config.yaml`.
2. `systemctl --user restart rousseau-agent`.
3. Verifique dos logs.

Para a maioria dos transportes a reconexão é rápida (~1-3 segundos). A pausa principal é no WhatsApp, onde whatsmeow reestabelece o websocket.

## Retenção de log

Retenção de `journald` é definida por `SystemMaxUse=` em `/etc/systemd/journald.conf`. Para uma implantação amigável a auditoria, envie logs para fora do host e defina o journald para uma retenção mais curta no disco local (por exemplo, 7 dias) para que a trilha de auditoria viva em Loki/S3, não em um filesystem que um intruso poderia rotacionar.

## Ciclo de vida de imagem de contêiner

Reconstrua a imagem em cada release do rousseau que você quer adotar:

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

A linha Quadlet `AutoUpdate=disabled` (em `docker/rousseau-agent.container`) impede que `podman auto-update` toque no contêiner. Você controla a cadência de update.

## Relacionado

- [Implantação](/pt-BR/deployment/) — a unidade Quadlet de referência.
- [Tutorial: Deploy a um VPS](/pt-BR/tutorials/deploy-to-a-vps/) — exemplo trabalhado.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — pipeline de log.
- [Guias: Onboarding Corporativo](/pt-BR/guides/enterprise-onboarding/) — checklist completo.
