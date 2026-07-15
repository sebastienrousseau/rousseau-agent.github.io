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
changefreq: "weekly"
description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/skills/"
subtitle: "Arquivos de skill em Markdown compatíveis com agentskills.io."
tags: "skills, reference"
title: "Skills"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Skills"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Skills"
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
twitter_description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Skills"
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

## Formato de skill

Uma skill é um arquivo Markdown com um cabeçalho front-matter YAML opcional. O formato é deliberadamente próximo da convenção [agentskills.io](https://agentskills.io) para que os arquivos sejam portáveis para outras ferramentas.

Exemplo — `~/.local/share/rousseau/skills/git-rebase.md`:

```markdown
---
name: git-rebase
description: Guide the user through an interactive rebase safely.
triggers:
  - rebase
  - git rebase
  - squash
  - autosquash
---
When helping with a git rebase, first verify the current HEAD is
pushed to a remote branch. Prefer `git rebase -i --autosquash`
when the user has fixup commits. Never force-push to `main`.
```

## Campos do front-matter

| Campo | Tipo | Efeito |
|---|---|---|
| `name` | string | Deve casar `^[a-z][a-z0-9-]*$`. Exibido por `rousseau skills list`. |
| `description` | string | Resumo em uma linha. |
| `triggers` | `[]string` | Substrings case-insensitive. Se qualquer uma aparecer na mensagem do usuário, a skill ativa. Vazio significa que a skill nunca ativa automaticamente. |

Tudo após o `---` de fechamento é o corpo da skill, literal.

## Descoberta

O loader varre `agent.skills_dir` por arquivos `*.md` (não recursivo). Um diretório ausente não é erro — Load retorna `nil`. Subdiretórios são ignorados.

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## Ativação

A cada turn do usuário, `SkillsProvider.SystemAppendix(session)` inspeciona a mensagem mais recente do usuário e casa os `triggers` de cada skill (case-insensitive). Cada match é concatenado (na ordem de carregamento) e inserido no system prompt daquele turn.

Skills com `triggers` vazios nunca ativam automaticamente, mas podem ser incluídas programaticamente por chamadores que embutem a biblioteca.

## CLI

```sh
# Lista as skills descobertas.
rousseau skills list

# Mostra o conteúdo de uma única skill.
rousseau skills show git-rebase
```

## Restrições de design

- **Sem execução de código.** Skills são strings. Elas não podem executar scripts ou comandos de shell. Se você quer automação, conecte uma nova ferramenta via `Registry.Register`.
- **Sem versionamento.** O rousseau não rastreia versões de skills. Gerencie isso no git — espera-se que o `skills_dir` seja uma cópia de trabalho de um repositório.
- **Determinístico.** A mesma sessão + mensagem do usuário produz o mesmo apêndice. Não há LLM no loop.

## Escrevendo skills eficazes

- Mantenha o corpo curto (100–500 palavras). Cada ativação é prefixada ao system prompt daquele turn.
- Prefira frases imperativas ("Quando o usuário perguntar sobre X, faça Y") em vez de exposição.
- Use `triggers` para frases de alta precisão; triggers amplos ("code", "help") ativam em quase todo turn e afogam as outras skills.
- Teste na TUI (`rousseau chat`) antes de subir para um daemon de transporte de chat — a linha de log `agent.skills_activated` lista quais skills dispararam.
