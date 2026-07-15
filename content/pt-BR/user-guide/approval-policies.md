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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "Políticas de aprovação"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Políticas de aprovação"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Políticas de aprovação"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Políticas de aprovação"
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

## O contrato

Cada tool call passa por `Approver.Approve(ctx, ApprovalRequest)` antes de ser executada. A interface vive em `internal/agent/approver.go`:

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` é chamado sincronamente no hot path; implementações devem retornar rapidamente ou honrar o cancelamento de `ctx`.

Um `DecisionDeny` com uma razão não vazia expõe a razão de volta para o modelo como um erro `tool_result`. O modelo pode então se adaptar (tipicamente pedindo esclarecimento ao operador) em vez de falhar silenciosamente. Essa é uma decisão de design deliberada — negações silenciosas produzem comportamento pior que anotadas.

## Três modos distribuídos

### `allow_all`

Cada tool call roda. Esse é o comportamento baseline quando nenhum approver é configurado.

```yaml
agent:
  approver:
    mode: allow_all
```

Use quando:

- `rousseau chat` interativo com o provider `claudecli` (o Claude Code está fazendo suas próprias aprovações por call).
- Smoke tests de desenvolvimento em que você quer ver exatamente o que o modelo faria.

### `deny_all`

Bloqueia toda tool call com uma única string de razão.

```yaml
agent:
  approver:
    mode: deny_all
    reason: "denied by policy for this deployment"
```

Use quando:

- Fazendo smoke test do wiring do approver.
- Uma postura de inspeção de primeira leitura onde você quer ver o que o modelo *teria* tentado, sem deixá-lo agir.

### `pattern`

Regras de allow / deny por regex, por ferramenta. **Deny vence allow.** Requests não correspondidos caem no `default` (`allow` ou `deny`).

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # safe-by-default; unlisted requests are blocked
    reason: "denied by pattern policy"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## Semântica de regras

Cada `PatternRule` tem dois campos:

| Campo | Significado |
|---|---|
| `tool` | Nome da ferramenta (`read`, `write`, `edit`, `grep`, `bash`, ou qualquer ferramenta customizada). Vazio bate em toda ferramenta. |
| `match` | Regex Go RE2 contra a entrada JSON bruta que o modelo produziu. Vazio bate em toda entrada. |

**Ordem de match:**

1. Cada regra de deny é testada contra o request. Primeiro match → deny.
2. Cada regra de allow é testada. Primeiro match → allow.
3. Cai para `default`. `default` vazio é tratado como `deny` — safe-by-default.

Deny sempre vence porque a disposição mais segura é preferida. Um operador adicionando um bloco `allow` amplo nunca consegue destrancar acidentalmente uma categoria que ele havia negado.

## Match contra JSON bruto

A regex de `match` roda contra a **entrada JSON bruta** que o modelo emitiu, não contra campos parseados. Isso tem duas consequências:

1. **Você faz match contra a forma JSON.** Para uma call `bash`, isso se parece com `{"command":"ls /tmp"}`. Faça match com `"command":\s*"ls\s`.
2. **Você pode fazer match em qualquer campo.** A ferramenta `edit` recebe `{"path":"/x","old_string":"...","new_string":"..."}`; você pode fazer match em `path`, em `old_string`, ou em ambos.

Escape caracteres relevantes ao JSON com cuidado:

- Aspas duplas são literais no JSON bruto — faça match com `\"` na sua regex se usar strings YAML com aspas duplas.
- Barras invertidas requerem duplicação em YAML: `\\` no arquivo YAML se torna `\` na regex compilada.

## Patterns de matcher trabalhados

### Restringir edits a uma árvore de diretório

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### Whitelist de comandos shell seguros

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### Negar comandos destrutivos independentemente de allow

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### Negar escritas em diretórios do sistema

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## O campo `Default`

`default: deny` é a disposição mais segura e o valor recomendado para qualquer daemon sem supervisão. `default: allow` inverte o modelo — cada call não listada roda, e regras `deny` viram a alavanca primária.

Quando usar `default: allow`:

- O daemon está rodando dentro de um contêiner fortemente travado ([Implantação](/pt-BR/deployment/)) e o contêiner é sua fronteira primária.
- Você está experimentando e quer ver o comportamento do modelo antes de decidir o que bloquear.

Em todo o resto, prefira `default: deny`.

## O campo `Reason`

`reason` é a string retornada ao modelo em cada negação (ou fallback de `default: deny`). Vazio cai para `denied by pattern policy` (ou `denied by policy` para `deny_all`).

Definir uma razão útil melhora a recuperação do modelo — em vez de `denied by pattern policy`, tente `denied — this deployment only allows reads inside /workspace; ask the operator to widen the scope` e observe o modelo responder com um esclarecimento acionável.

## Interação com `claudecli`

Quando `provider: claudecli`, o Claude Code está rodando as tool calls, e seu próprio permission-mode (`bypassPermissions`, `plan`, `default`) também controla cada ação. Comportamento efetivo é a interseção: **ambos** o approver do rousseau e o approver do Claude Code precisam permitir a call para que ela rode.

Prefira manter ambos alinhados:

- Sem supervisão: `bypassPermissions` no Claude Code, `mode: pattern` + `default: deny` no rousseau.
- Inspeção somente leitura: `plan` no Claude Code, `mode: pattern` permitindo só `read`/`grep` no rousseau. Veja [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/).

## Trilha de auditoria

Cada decisão do approver é emitida via slog:

| Evento | Significado |
|---|---|
| `tool.execute` (INFO) | Call aprovada, executando. |
| `tool.denied` (WARN) | Call bloqueada. Inclui nome da ferramenta e razão. |
| `tool.error` (WARN) | Call rodou mas falhou. |

Veja [Guias: Observabilidade](/pt-BR/guides/observability/) para receitas de pipeline.

## Approvers customizados

Qualquer tipo que satisfaça `Approver` funciona. Conecte o seu ao embutir o agent loop:

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // Consult an external policy engine, prompt the operator, ...
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

A interface é deliberadamente minimalista (`Approve` é o único método) para que integrar com um policy engine externo (OPA, Cedar, ou um engine de regras sob medida) seja um pequeno adapter.

## Solução de problemas

### Toda call negada mesmo com um allow correspondente

Deny vence allow. `PatternApprover.Approve` em `internal/agent/approver.go` linha 152 itera regras de deny primeiro. Procure pela string `reason` exata nos logs `tool.denied`.

### Erro de compilação de regex no início

`PatternApprover` compila regexes preguiçosamente no primeiro `Approve`. Um erro de compilação resulta em `DecisionDeny` com razão `approver: pattern compile: <err>`. Teste regexes em [regex101.com](https://regex101.com) com o flavor Go.

### `mode: pattern` mas `default:` é ignorado

Apenas `allow` e `deny` são valores válidos para `default:`. Valores vazios ou desconhecidos caem para `DecisionDeny` (padrão seguro) e não imprimem warning.

### Regra de allow bate no JSON literalmente

A regex roda contra o JSON bruto de entrada da tool call. Para bater em um campo `path`, escape aspas: `"\"path\":\"/workspace/"`.

### Calls negadas não aparecem nos logs

Aparecem — como `tool.denied` em nível `warn`. Se você filtra por nível, garanta que `warn` está incluído.

## Páginas relacionadas

- [Guias: Auditoria + Políticas de Aprovação](/pt-BR/guides/audit-approval-policies/) — exemplo trabalhado com trilha de auditoria slog.
- [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/) — a postura de inspeção.
- [Guia do usuário: Tools](/pt-BR/user-guide/tools/) — as ferramentas que o approver controla.
- [Segurança](/pt-BR/security/) — visão geral de fronteiras de confiança.
- [Agent loop](/pt-BR/agent-loop/) — onde o approver é chamado.

## Leitura adicional

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — a matriz de teste.
- `internal/cli/approver.go` — tradução config → approver.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
