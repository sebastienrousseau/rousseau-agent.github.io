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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "Tutorial: endurecer o approver"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: endurecer o approver"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: endurecer o approver"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: endurecer o approver"
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

## O que você constrói

Um daemon rousseau que começou rodando o provider `claudecli` em modo `bypassPermissions` (o padrão sem supervisão) acaba sob um approver rousseau-agent em modo `pattern` com `default: deny`. Cada tool call é ou explicitamente allowlistada ou bloqueada; cada negação produz um evento slog `tool.denied` que você pode auditar.

Tempo estimado: 30 minutos para um passe adequado de regras com testes.

## Pré-requisitos

- Rousseau instalado com qualquer bridge de transporte rodando (WhatsApp, Slack, Signal — qualquer coisa sem supervisão).
- Familiaridade básica com regex do Go — regras do approver são regexes Go RE2 sobre o JSON de entrada da ferramenta.

## Onde o approver vive

Duas camadas independentes podem aprovar tool calls:

1. **O próprio permission mode do provider.** O provider `claudecli` (`internal/llm/claudecli/client.go`) delega para `claude --permission-mode`. Valores documentados em `ClaudeCLIConfig.PermissionMode` (`internal/config/config.go`): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Daemons sem supervisão fixam `bypassPermissions` em `setUnattendedPermissionDefault`.
2. **O próprio approver do rousseau.** Configurado sob `agent.approver` (`internal/config/config.go` `ApproverConfig`; implementação em `internal/agent/approver.go`). Três modos: `allow_all`, `deny_all`, `pattern`. **Deny vence allow, e calls não correspondidas caem no `default`.**

Para um daemon sem supervisão, o approver do rousseau é a mitigação que você configura à mão. O próprio modo do `claudecli` é o cinto de segurança.

## Passo 1: auditoria baseline

Antes de escrever regras, rode algumas sessões realistas com `mode: allow_all` e `log.format: json`. Cada tool call emite `tool.execute` (`internal/agent/agent.go`):

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Você agora tem uma distribuição empírica de quais ferramentas o agente usa e contra quais caminhos. Essa é a semente para a allowlist.

## Passo 2: rascunhe uma política pattern

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # Read side: unrestricted within the daemon's filesystem view.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Editing pinned to /workspace.
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell: whitelist of read-only utilities plus git status/diff/log.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute denies override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

Implante e observe o stream slog. Os eventos relevantes (`internal/agent/agent.go`):

- `tool.execute` — a call rodou. Campos: `name`, `id`.
- `tool.denied` — o approver bloqueou. Campos: `name`, `reason`.
- `tool.error` — rodou e falhou. Campos: `name`, `err`.

## Passo 3: itere

O primeiro dia expõe falsos positivos: tool calls legítimas que o approver bloqueou. Faça grep neles:

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Cada `tool.denied` recorrente merece uma decisão:

- **Genuinamente necessário** — estenda a regra de allow. Prefira estreita (path fixado) a ampla (regex aberta).
- **Não necessário** — deixe negado. O modelo vai pivotar para uma abordagem diferente.

Não enfraqueça `default: deny`. Essa é a propriedade que torna uma ferramenta não lembrada segura.

## Passo 4: excerto de audit-log

Uma execução de produção com um prompt desconhecido ficou assim:

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

O único `tool.denied` aqui foi `bash: "curl https://…"`. A regra de deny pegou, o modelo degradou para `read` + `grep`, e a resposta ainda foi entregue.

## Passo 5: consolide

Uma vez que a taxa de falso positivo se estabilize, congele a config, faça commit em source control (segredos excluídos — veja [Guias: Onboarding Corporativo](/pt-BR/guides/enterprise-onboarding/)), e coloque um code review na frente de mudanças de config. `internal/agent/approver_test.go` na árvore de código é seu modelo de como escrever testes contra o ruleset — copie a forma para um pacote interno se você quer que o CI pegue uma política quebrada.

## O que a política ainda não faz

Mesmo com as regras pattern mais apertadas:

- **Sem sandbox.** Uma call `bash` permitida ainda roda com o UID e a visibilidade de filesystem do daemon. Coloque um contêiner rootless ([Implantação](/pt-BR/deployment/)) por baixo.
- **Sem rate limiting.** Dez calls permitidas por segundo são todas permitidas. Envolva o registry de ferramentas se você precisa disso.
- **Sem auditoria de rede outbound.** O approver vê a string inicial `command` do `bash`, não o que ele faz curl. Negue `curl` e `wget` diretamente — as regras de deny de amostra fazem isso.

Veja [Guias: Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) para a discussão mais profunda.

## Relacionado

- [Guia do usuário: Políticas de Aprovação](/pt-BR/user-guide/approval-policies/) — referência para cada modo.
- [Guia do usuário: Tools](/pt-BR/user-guide/tools/) — schemas de ferramentas, úteis para escrever regex.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — envie `tool.denied` para Loki/Datadog.
- [Referência: Logs](/pt-BR/reference/logs/) — cada mensagem slog conhecida.
