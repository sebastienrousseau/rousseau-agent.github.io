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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "Guia: auditoria + políticas de aprovação"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: auditoria + políticas de aprovação"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia: auditoria + políticas de aprovação"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: auditoria + políticas de aprovação"
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

## O problema

Um daemon de transporte de chat sem supervisão não tem um humano no terminal para aprovar tool calls em tempo real. Se o modelo quiser executar `rm -rf /workspace/*`, algo precisa detê-lo. O approver em modo `pattern` do rousseau é essa alavanca.

A ameaça não é o modelo ficar rebelde — é uma instrução comprometida ou desalinhada chegando ao daemon pelo canal de transporte. Uma política em modo pattern com fallback `default: deny` torna o risco limitado e auditável.

## Modos do approver

Três modos embutidos são distribuídos (veja `internal/agent/approver.go`):

| Modo | Comportamento | Quando usar |
|---|---|---|
| `allow_all` | Toda tool call roda. | `rousseau chat` interativo em que o provider `claudecli` está fazendo suas próprias aprovações. |
| `deny_all` | Toda tool call é bloqueada. Motivos de negação são expostos ao modelo como erros de `tool_result` para que ele possa se adaptar. | Postura de inspeção somente leitura; smoke tests. |
| `pattern` | Regras de allow / deny por regex, por ferramenta. **Deny vence allow.** Requests não correspondidos caem no `default`. | Qualquer daemon sem supervisão em produção. |

## Config trabalhada

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Read-side tools: no restriction inside the workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edit inside /workspace only.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Write inside /workspace only.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell commands: whitelist of safe read-side utilities plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute deny rules override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

Duas propriedades importantes decorrem de `PatternApprover.Approve`:

1. **Deny vence.** Cada regra de deny é checada antes de qualquer regra de allow. Isso é mais seguro do que o inverso: um operador que adiciona um allow abrangente nunca consegue destrancar acidentalmente uma categoria que ele achava estar negada.
2. **Não correspondida → deny.** Com `default: deny`, qualquer tool call que o operador esqueceu de enumerar é bloqueada. Essa é a disposição safe-by-default; se você quer o oposto, defina `default: allow`.

## Lendo a trilha de auditoria

Cada tool call e cada negação é emitida pelo logger slog:

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

O daemon usa `slog` com nível e formato configuráveis (`log.level`, `log.format`). Para produção, prefira `format: json` para que ferramentas downstream (Loki, Vector, Datadog) façam parse limpo. Veja [Guias: Observabilidade](/pt-BR/guides/observability/) para a receita de pipeline.

Cada negação carrega uma chave estruturada estável:

- `tool.denied` — a tool call foi bloqueada. Campos: `name` (identificador da ferramenta), `reason` (de `PatternApprover.DenyReason` ou o fallback embutido).
- `tool.execute` — a tool call rodou. Campos: `name`, `id` (o ID de call emitido pelo modelo, para correlação).
- `tool.error` — a ferramenta rodou mas falhou. Campos: `name`, `err`.

Um filtro `slog` em `tool.denied` te dá a visão de auditoria "tentativas bloqueadas" que a maioria dos frameworks de compliance pede.

## Testando a política

`internal/agent/approver_test.go` na árvore de código exercita o `PatternApprover` com uma matriz ampla. Para fazer um smoke-test das suas próprias regras:

```sh
rousseau chat
> Run `rm -rf /tmp/foo` for me.
```

O modelo tentará a tool call `bash`. O daemon loga `tool.denied` e retorna a string `reason` ao modelo, que geralmente vai pivotar ("I can't run that — could you tell me what you were trying to do?").

Para a matriz de teste de referência, veja `internal/agent/approver_test.go` — as mesmas formas de regra são exercitadas lá.

## Adicionando um override manual

Às vezes um operador quer aprovar manualmente uma única call perigosa. O padrão mais simples:

1. Defina `mode: allow_all` em `rousseau chat` (TUI interativa). O provider `claudecli` cuida dos seus próprios prompts de aprovação por call.
2. Mantenha `mode: pattern` em todo daemon sem supervisão.

Hoje não há UI de aprovação interativa por call nos transportes de chat — a história de segurança é inteiramente regex + slog.

## O que a política não faz

- **Não faz sandbox da ferramenta.** Uma call de `bash` que sobrevive ao approver roda com o UID do daemon e sua visibilidade de filesystem. Coloque um contêiner rootless ([Implantação](/pt-BR/deployment/)) por baixo.
- **Não faz rate-limit.** Dez calls de `bash` permitidas por segundo são permitidas. Se você precisa de rate limiting, envolva o registry de ferramentas.
- **Não audita chamadas de rede outbound.** Se uma invocação de `bash` faz um curl para fora, o approver não verá a URL — apenas a string inicial `command` do `bash`. Negue `curl` e `wget` diretamente no nível de pattern.

## Padrões comuns

### Restringindo edição a uma árvore de diretórios

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### Auditor somente leitura

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

Combinado com `provider.claudecli.permission_mode: plan`, isso produz uma postura de inspeção somente leitura — veja [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/).

### Fluxos git-first

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## Cinco conjuntos de regras de referência

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Conjunto de regras de referência">
    <button role="tab" aria-selected="true">Laptop de dev</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">Produção</button>
    <button role="tab" aria-selected="false">Bot de on-call</button>
    <button role="tab" aria-selected="false">Somente leitura</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Laptop de dev.** Permissivo por padrão, nega o que é de fato perigoso. Assume um terminal supervisionado.

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Staging.** Lista de allow explícita para o workspace, nega tudo fora dele. Adequado para um daemon de staging compartilhado com raio de impacto limitado.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Produção.** Deny-first. Cada comando permitido é explicitamente enumerado. Adequado para um daemon de produção que responde perguntas voltadas ao cliente.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Layered denies just in case.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Bot de on-call.** Pode consultar monitoramento, seguir logs, mas não reiniciar serviços nem editar código. Adequado para um helper de resposta a incidentes exposto no Slack.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Auditor somente leitura.** Sem escritas, sem shell. Adequado para um bot de code review ou um daemon que explica docs.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

Combine com `provider.claudecli.permission_mode: plan` e `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` para reforço com cinto e suspensórios — o modelo literalmente não consegue solicitar outras ferramentas.

  </div>
</div>

## Solução de problemas

### Toda call é negada mesmo com regras de allow

Deny vence allow. Verifique se alguma das suas regras de deny está batendo sem intenção. A linha de log `tool.denied name=<X> reason=<Y>` inclui o motivo exato.

### Erro de compilação de regex de pattern

O `PatternApprover` compila regras preguiçosamente no primeiro uso. Um erro de compilação vira um `DecisionDeny` com razão `approver: pattern compile: <err>`. Corrija a regex; regex101.com com o flavor Go selecionado é seu amigo.

### Regex bate no JSON literalmente, não semanticamente

A regex de `match` roda contra o JSON bruto de entrada da tool call. Escape aspas e barras invertidas apropriadamente: `"\"path\":\"/workspace/"` bate no campo `path` de uma call `edit` ou `write`.

### `deny_all` não está bloqueando nada

Confirme `mode: deny_all` (não `mode: deny`). Os modos válidos são `allow_all`, `deny_all`, `pattern`. `allow` e `deny` sozinhos são tratados como aliases das variantes `_all`, mas strings exatas são mais seguras.

### Regra de allow para `bash` nunca bate

A entrada de `bash` é JSON como `{"command":"ls -la"}`. Faça o match contra esse literal JSON, não apenas contra a string do comando shell. Use um pattern como `^\\{\"command\":\"ls`.

## Páginas relacionadas

- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — referência mais profunda e exemplos trabalhados.
- [Guia do usuário: Tools](/pt-BR/user-guide/tools/) — schema de cada ferramenta embutida.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — expor a trilha de auditoria.
- [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/) — reforço com cinto e suspensórios.
- [Segurança](/pt-BR/security/) — visão geral do modelo de confiança.

## Leitura adicional

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — matriz de teste.
- `internal/cli/approver.go` — tradução config → approver.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
