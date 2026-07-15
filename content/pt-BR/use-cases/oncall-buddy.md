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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "Caso de uso: parceiro de plantão"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Caso de uso: parceiro de plantão"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Caso de uso: parceiro de plantão"
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
twitter_description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Caso de uso: parceiro de plantão"
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

## A história

São 3 da manhã. Seu pager dispara. O PagerDuty diz que o serviço checkout está retornando 502s. Você é um dos dois SREs em uma empresa pequena, seu co-lead está de férias, e chegar no laptop significa encontrar seus óculos, descer as escadas e destravar uma VPN. Antes de tudo isso, você quer uma primeira resposta: quais dashboards estão ruins, o que mudou nas últimas 24 horas, qual runbook se aplica.

O rousseau vive na ops box no seu closet. Ele tem credenciais somente leitura para sua stack de logging, kubectl somente leitura em um namespace e uma conexão Slack Socket Mode em `#incident-oncall`. Você toca na notificação da DM no seu celular:

> what changed in checkout in the last 24h?

O rousseau lê o git log do repo do serviço checkout, cruza contra seu deploy log (de um diretório bind-mountado) e responde:

> Two changes: PR #4821 (payment retry logic, deployed 21:14 UTC) and a Helm value bump on `checkout-web` at 22:03 UTC. The payment retry change is the more suspicious — it touches the same code path the current 502s originate from.

Você pergunta:

> pull the last 100 error lines from checkout-web

O rousseau roda `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous` sob seu kubeconfig somente leitura, e cola de volta as linhas salientes. Você vê um trace de null-pointer. Você responde por DM:

> revert PR #4821 in staging first — call me when it's confirmed green

O rousseau posta em `#incident-oncall` com um plano, abre um PR de revert contra staging e pinga de volta quando staging está verde. Você levanta e vai para seu laptop.

## O que isso requer

### O daemon

O rousseau roda como um contêiner Podman rootless na ops box:

- **Provider**: `bedrock` — sua empresa já tem um compromisso de gasto Bedrock; sem chaves de API por usuário.
- **Transporte**: Slack Socket Mode — sem superfície HTTP inbound, apenas WebSocket outbound.
- **Estado**: `~/.local/share/rousseau/sessions.db`, em um disco criptografado com LUKS.

### Config

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  profile: rousseau-oncall
  model: anthropic.claude-sonnet-4-6-20250101-v1:0

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  approver:
    mode: pattern
    default: deny
    reason: "read-only on-call posture — ask an operator to widen the scope"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(kubectl get|kubectl describe|kubectl logs|git log|git diff|git show|cat|grep|rg|head|tail|wc) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr (view|list|diff) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr create --draft "}   # allows opening a draft revert
    deny:
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|rollout undo|exec)"}
      - {tool: bash, match: "gh pr merge|gh pr close --delete-branch"}

slack:
  app_token: xapp-<...>
  bot_token: xoxb-<...>
  allowlist:
    - U012ABCXYZ    # your Slack user ID
    - U012DEFGHI    # your co-lead's Slack user ID
```

### Os bind mounts

- Checkouts de repos em `/workspace/repos/` (somente leitura).
- Deploy log em `/workspace/deploys/` (somente leitura).
- kubeconfig em `/home/rousseau/.kube/config` — montado somente leitura, service account tem cluster role somente leitura no namespace `checkout`.
- Credenciais AWS via IAM Role for Service Accounts (IRSA) se em EKS, ou via `~/.aws/` montado para on-prem.

### A unidade Quadlet systemd

O `docker/rousseau-agent.container` de referência com:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

Inicia no restart do host. Journal disponível via `journalctl --user -u rousseau-agent.service`.

## A postura de segurança

- **Allowlist do Slack** garante que só você e seu co-lead podem dirigir o daemon. Toda outra DM é silenciosamente descartada.
- **Approver pattern com `default: deny`** bloqueia qualquer coisa fora da whitelist. Se o modelo quer rodar `kubectl delete pod`, ele recebe um erro `tool_result` explicando o bloqueio e reroteia para um documento de plano.
- **Kubeconfig somente leitura + mounts de repo somente leitura** significam que o daemon *não pode* mutar produção mesmo se o approver falhasse aberto.
- **Cinto, suspensórios e um segundo cinto** — cada camada falha com segurança.

## O que o rousseau não faz aqui

- **Não te pageia.** O PagerDuty é a fonte da verdade sobre quem está on-call.
- **Não faz merge de PRs.** O approver bloqueia `gh pr merge`. O rousseau pode abrir um revert draft; um humano ainda tem que confirmar.
- **Não roda `kubectl exec`.** Qualquer comando que pudesse mutar o estado do cluster é negado.
- **Não aprende com o incidente.** Recall cross-session via FTS5 significa que o rousseau do próximo incidente vai achar palavras-chave da sessão de hoje; as conclusões semânticas ainda são trabalho do operador.

## O que você mudaria sob carga

Se dois pagers às 3 da manhã por mês virarem dois por semana:

- Considere promover mais matchers de `bash` para `allow` conforme você ganha confiança.
- Conecte a saída slog em [Loki](/pt-BR/guides/observability/) para que revisões post-mortem possam citar as tool calls exatas que o rousseau fez.
- Adicione [tarefas agendadas](/pt-BR/guides/scheduled-tasks/) para que o rousseau rode um digest noturno de incidentes abertos no seu Slack da manhã.

## Páginas relacionadas

- [Guias: Auditoria + Políticas de Aprovação](/pt-BR/guides/audit-approval-policies/) — a alavanca de segurança.
- [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/) — a postura mais estrita.
- [Transporte Slack](/pt-BR/transports/slack/) — wiring Socket Mode.
- [Provider Bedrock](/pt-BR/providers/bedrock/) — cadeia de auth.
