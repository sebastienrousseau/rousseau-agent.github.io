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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "Guia: gestão de arquivos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: gestão de arquivos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: gestão de arquivos"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: gestão de arquivos"
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

## As duas ferramentas

Duas ferramentas alteram o filesystem:

- [`write`](/pt-BR/reference/tool-schemas/#write) — sobrescrita de arquivo inteiro. `internal/tools/builtin/write.go` escreve com modo `0o644` e `MkdirAll(dir, 0o755)`.
- [`edit`](/pt-BR/reference/tool-schemas/#edit) — substituição única de string exata dentro de um arquivo existente. `internal/tools/builtin/edit.go`.

Ambas exigem um **caminho absoluto** (chamam `filepath.IsAbs`). Nenhuma delas faz atomic-swap — usam `os.WriteFile` diretamente.

## A visão de mundo do contêiner

A unidade Quadlet de referência em `docker/rousseau-agent.container` monta três diretórios do host dentro do contêiner:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

Nada mais no host é visível. De dentro do contêiner, uma tool call `edit` contra `/workspace/repos/foo/main.go` resolve para `~/team-rousseau-workspace/repos/foo/main.go` no host.

### `:Z` — o rótulo SELinux

A flag `:Z` em cada `Volume=` diz ao Podman para re-rotular o mount com uma categoria SELinux MCS **privada ao contêiner**. Sem ela, em um sistema com SELinux em modo enforcing:

- Leituras ainda funcionam na maior parte do tempo (`container_file_t` é amplamente legível).
- Escritas falham com `EACCES` e `avc: denied { write }` no log de auditoria.

Se você troca a flag para `:z` (minúsculo), o Podman re-rotula com uma categoria **compartilhada** — mais seguro para hosts compartilhados entre múltiplos usuários de contêiner, mas não é o padrão.

Em sistemas sem SELinux (Debian, Ubuntu sem endurecimento), `:Z` é um no-op silencioso.

### `UserNS=keep-id` — mapeamento de UID

O contêiner roda como UID/GID 1000. Sem mapeamento de user namespace, o Podman rootless remapearia 1000 para o intervalo subuid (tipicamente `100000+`), e arquivos escritos de dentro do contêiner seriam donos daquele UID mapeado no host — inutilizáveis para o operador.

`UserNS=keep-id` mapeia o UID 1000 do contêiner para o UID do usuário do host (também 1000 no setup de referência). Arquivos escritos dentro de `/workspace` acabam pertencendo a `seb:seb` no host — exatamente o que você quer.

Se seu usuário de host não for UID 1000, o mapeamento ainda funciona; `keep-id` usa o UID real do usuário invocador.

## Editar fora de `/workspace`

Como os bind mounts são a única visão do contêiner sobre o filesystem do host, um `write` ou `edit` contra `/etc/nginx/nginx.conf` vai falhar com um erro de caminho não encontrado — o caminho simplesmente não existe dentro do contêiner. Isso é uma **feature**: significa que a política de approver do operador pode confiar no limite do contêiner.

Se você realmente precisa que o daemon toque um caminho diferente do host:

1. **Preferido:** adicione uma nova linha `Volume=` à unidade Quadlet. Faça a escolha menos permissiva: `:ro` para somente leitura, `:Z` para rotulação SELinux privada.
2. **Não** rode o rousseau fora do contêiner para burlar o limite — você perde seccomp, drop-caps e o filesystem raiz somente leitura.

## Editar fora do contêiner

Se você roda o rousseau diretamente no host (sem contêiner), as ferramentas operam contra a visão do processo do daemon — tudo sob a HOME do usuário por padrão. O approver é a única camada de contenção. Veja [Guias: Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) para a receita de modo pattern + `default: deny`.

## `write` vs `edit` — quando usar qual

| Situação | Use |
|---|---|
| Criar um arquivo novo. | `write`. |
| Reescrever um arquivo inteiro. | `write`. |
| Mudar uma seção de um arquivo grande. | `edit`. Ele falha com segurança quando `old_string` não é único. |
| Renomear um símbolo em todo o arquivo. | Múltiplas calls `edit` com contexto ao redor progressivamente maior, ou um único `write` com o conteúdo completo reescrito. Não use `edit` com semântica estilo `replace_all` — a ferramenta recusa. |

A restrição de unicidade exata em `edit` é deliberada. Ela empresta diretamente da Edit tool do Claude Code. Procure em `internal/tools/builtin/edit.go` pelo bloco de comentário que explica o porquê.

## Modos comuns de falha

| Sintoma | Causa | Correção |
|---|---|---|
| `edit: path must be absolute, got "…"` | O modelo passou um caminho relativo. | Rejeite ou reescreva no approver; peça ao modelo para usar caminhos absolutos. |
| `edit: old_string not found in …` | O arquivo mudou desde a última leitura do modelo, ou o modelo alucinou o contexto ao redor. | O modelo tipicamente vai reler e tentar de novo. |
| `edit: old_string is not unique in … (found 3 occurrences)` | A mesma string aparece múltiplas vezes. | O modelo deve fornecer mais linhas ao redor para desambiguar. |
| `write: permission denied` | Rótulo SELinux incompatível ou mapeamento de UID errado. | Verifique `:Z` no volume e `UserNS=keep-id` no contêiner. |
| `read: does not look like UTF-8 text` | O arquivo contém bytes NUL nos primeiros 512 bytes (`isLikelyText` em `read.go`). | Recuse leituras binárias no nível do approver; use a ferramenta `bash` com `file` se precisar identificar. |

## Backups antes de grandes reescritas

As ferramentas não criam cópias `.bak`. Para mudanças de alto risco, ensine o modelo a escrever em um caminho irmão primeiro, dar `bash` diff nele e então trocar. Como alternativa, faça tudo passar por uma branch git — o rousseau deixa `git` completamente fora do seu caminho de execução, então o versionamento acontece pelo seu fluxo normal.

## Relacionados

- [Referência: Schemas de tool](/pt-BR/reference/tool-schemas/) — schemas exatos de entrada.
- [Guia do usuário: Tools](/pt-BR/user-guide/tools/).
- [Implantação](/pt-BR/deployment/) — a unidade Quadlet que define os bind mounts.
- [Guias: Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — fixando escritas a uma árvore de diretórios.
