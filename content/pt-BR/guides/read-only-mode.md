---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "Guia: modo somente leitura"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: modo somente leitura"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia: modo somente leitura"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: modo somente leitura"
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

## Cenário

Você quer que o rousseau inspecione um repositório, responda perguntas sobre ele e produza relatórios — mas ele não pode escrever, editar ou executar comandos shell destrutivos. Essa é a postura que você implantaria para uma auditoria de primeira leitura, uma inspeção de resposta a incidentes ou um walk-through de compliance.

Três camadas se empilham para tornar isso difícil:

1. **Política de aprovação** — negar toda ferramenta mutante.
2. **Modo de permissão do `claudecli`** — colocar o Claude Code em modo `plan` para que seu próprio approver nunca edite arquivos.
3. **Filesystem** — montar o workspace com bind-mount somente leitura.

Cinto, suspensórios e um segundo cinto. Qualquer uma das três falha com segurança.

## Camada 1 — Approver

A postura somente leitura mais simples usa o approver `pattern` com uma allowlist:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # No deny rules needed — default: deny catches everything else.
    # No edit, write, or unrestricted bash — the model can't reach them.
```

Uma variante ainda mais estrita usa `deny_all`, que bloqueia toda ferramenta incluindo `read` e `grep`:

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` só é útil como smoke test; o modelo não conseguirá fazer trabalho significativo.

## Camada 2 — Modo de permissão do `claudecli`

Quando o provider é `claudecli`, o próprio Claude Code está executando as tool calls. Definir `permission_mode: plan` faz o Claude Code recusar toda call de write ou edit na sua própria camada, mesmo que o approver do rousseau tivesse permitido:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

Valores válidos (veja `internal/config/config.go` e os docs do Claude Code): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. `plan` é o único valor que mantém consistentemente o Claude Code em postura somente leitura.

## Camada 3 — Filesystem

Monte o workspace somente leitura. Sob o Quadlet Podman de referência:

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

`ro` faz o mount ser somente leitura da perspectiva do contêiner; mesmo que um binário comprometido tentasse `open(2)` com `O_WRONLY`, o kernel retornaria `EROFS`.

Sob Kubernetes:

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

O session store (`~/.local/share/rousseau/`) ainda precisa ser gravável — o daemon faz append nele a cada turno. Mantenha esse mount `rw` e deixe apenas o workspace somente leitura.

## Postura dry-run

Não existe flag `--dry-run` no daemon. Se você quer que o modelo *planeje* mudanças sem executá-las, a combinação acima atinge o equivalente:

- O approver bloqueia toda ferramenta mutante → o modelo recebe um erro de `tool_result` explicando o bloqueio.
- O modo `plan` no `claudecli` impede o Claude Code de rodar suas próprias ferramentas destrutivas.
- Mounts somente leitura param qualquer coisa que vaze.

O modelo tipicamente responderá com um documento de plano em vez de um diff. Esse é o entregável de inspeção somente leitura.

## O que ainda funciona

- Toda call de `read` e `grep`.
- `bash` para utilidades read-side seguras que você enumerou.
- Persistência de sessão — o store SQLite ainda grava a conversa.
- Recall cross-session via FTS5, export MCP, skills — tudo somente leitura de qualquer forma.

## O que quebra (intencionalmente)

- `write` e `edit` — negados.
- Comandos de shell mutantes — negados.
- Jobs de cron cujo prompt implica em escrita de arquivos — o modelo tenta, é negado, responde com um plano.
- `rousseau init` — o CLI não é afetado pelo approver, mas ele escreve em `~/.config/rousseau/` fora do workspace. Rode antes de ativar o modo somente leitura.

## Testando a postura

```sh
rousseau chat
> Edit /workspace/README.md to add a footer.
```

Linha de log esperada:

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

Resposta esperada no chat: o modelo se desculpa, produz um plano ou um patch de diff como texto e pede ao operador para aplicá-lo.

Para a variante `deny_all`, toda tool call é bloqueada — o modelo não tem como inspecionar nada, então essa postura só é útil como smoke test.

## Combinando com outros transportes

As mesmas três camadas se aplicam a WhatsApp, Slack, Discord e todos os outros transportes. Como o approver roda dentro do agent loop, ele não se importa com qual transporte entregou o turno do usuário. Um agente Slack somente leitura está a um bloco `mode: pattern` de distância.

## Ressalvas

- A postura somente leitura é reforçada pelo approver do rousseau e pelo filesystem — **não** pelo LLM. Um modelo ainda pode emitir uma tool call `edit`; o approver silenciosamente a bloqueia, mas a tentativa é logada como `tool.denied`. Isso é intencional para que trilhas de auditoria registrem o que o modelo tentou, não apenas o que teve sucesso.
- Bind mounts somente leitura não protegem contra symlinks apontando para fora do mount. A postura Podman de referência descarta todas as capabilities, o que previne a maioria dos caminhos de escape, mas não confie apenas no mount.
- O modo `plan` do provider `claudecli` é o contrato do Claude Code, não do rousseau. Se o Claude Code mudar sua semântica de permission-mode, a postura somente leitura do rousseau herda essa mudança.

## Próximo

- [Guia do usuário: Políticas de Aprovação](/pt-BR/user-guide/approval-policies/) — referência mais profunda.
- [Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — a contraparte mutante.
- [Implantação](/pt-BR/deployment/) — flags de mount e contêiner.
