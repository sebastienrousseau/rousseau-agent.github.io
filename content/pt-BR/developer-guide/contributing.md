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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "Contribuir"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contribuir"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Contribuir"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contribuir"
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

## Regras básicas

Contribuições aceitas de colaboradores convidados. Cada PR é submetido à mesma barra: CI verde, padrões de código abaixo, aprovação do revisor. CI verde é necessário mas não suficiente.

A fonte autoritativa é o [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) na raiz do repo. Esta página o espelha na voz do docs-site.

## Ambiente de desenvolvimento

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # installs golangci-lint (v2) and govulncheck
make check      # vet + lint + race-tests + govulncheck
```

Cada checagem que roda no CI está disponível localmente pelo Makefile. Se uma mudança passa em `make check`, ela passará no CI.

## Padrões de commit

- **Conventional Commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`, `perf:`.
- Subject line ≤ 72 caracteres. O corpo explica **por que**, não o quê. Referencie a decisão, issue ou incidente motivador.
- Não faça amend em commits publicados. Crie um novo commit; o revisor prefere uma série que possa fazer bisect.
- Assine seus commits se você tiver signing configurado. Não é obrigatório atualmente, mas recomendado para commits de release-tag.

## Padrões de código

- Cada identificador exportado tem um comentário godoc começando com o nome do identificador.
- Sem `interface{}` / `any` em APIs exportadas sem justificativa escrita no comentário de doc.
- `context.Context` propaga por cada caminho de I/O. Sem globais escondidos ou loggers ambientes; passe `*slog.Logger` explicitamente.
- Erros embrulham para cima com `fmt.Errorf("...: %w", err)`. Erros sentinela vão no `errors.go` do pacote. Prefira `errors.Is` / `errors.As` nos call sites em vez de string matching.
- Sem panics fora de `main` e test helpers. Variantes `Must*` que fazem panic em erro de operador (registro duplicado, schema estático inválido) são permitidas com racionalização documentada.
- Sem `fmt.Print*` em código de biblioteca. Use `slog` ou um modelo TUI. O linter `forbidigo` reforça isso.

## Padrões de teste

- Testes unitários vivem ao lado do código: `foo.go` → `foo_test.go`.
- Testes table-driven preferidos. Use `require` para assertions que param, `assert` para as que não param.
- Injeção de teste baseada em interface em vez de patching global. Cada pacote de transporte define uma interface estreita (`WSConn`, `IMAPClient`, `HTTPClient`, `Sender`) que testes satisfazem com fakes.
- Alvo de cobertura: 85% para pacotes puros de lógica de negócio; 75% geral.
- Race-safe: `go test -race` deve passar. Novo código concorrente precisa de um race test se introduz sincronização não trivial.
- Funções fuzz para cada parser (`FuzzParseFoo` ao lado de `parseFoo`). `make fuzz` roda o corpus.

Veja [Testing](/pt-BR/developer-guide/testing/) para o padrão de injeção.

## Processo de pull request

1. Abra o PR contra `main`. Rebase (não faça merge) se `main` se mover debaixo de você.
2. Cada PR requer:
   - Uma racionalização na descrição (2–3 sentenças linkando para a decisão subjacente).
   - CI verde: `vet`, `lint`, `test-race` em Linux + macOS, `govulncheck`, `codeql`, `reproducible-build`, floor de cobertura.
   - Aprovação do revisor.
3. Apenas squash merges. A mensagem de commit de merge é a mensagem final de commit e chega em `main` como uma mudança atômica.
4. Se o PR adiciona uma nova dependência, note a justificativa na descrição. Prefira a standard library em vez de adicionar uma dependência; prefira uma dependência existente a adicionar uma nova.

## Checklist do revisor

Revisores verificam, em ordem:

1. **Necessidade.** A mudança é necessária, ou adiciona abstração / superfície de feature sem um requisito motivador?
2. **Escopo.** A mudança fica dentro do propósito declarado, ou combina limpezas não relacionadas?
3. **Integridade de fronteira.** A mudança respeita a direção de dependência `agent → concrete`? Veja [Arquitetura](/pt-BR/developer-guide/architecture/).
4. **Cobertura de testes.** Novos caminhos de código estão cobertos? Casos de borda são exercitados?
5. **Tratamento de erros.** Erros são embrulhados com contexto? Os caminhos de cleanup são honestos (`_ =` com uma justificativa `//nolint:errcheck`, não silenciosamente engolidos)?
6. **Godoc + linter limpo.** Cada símbolo exportado documentado; saída do lint é 0 issues.
7. **Segurança.** A mudança toca a ferramenta `bash`, política de aprovação, auth de transporte ou postura de contêiner? Se sim, a descrição do PR sinaliza isso?

## Contribuições de documentação

A documentação vive em um repositório separado. Quando um PR de código toca superfície visível ao usuário (uma nova flag, um novo campo, uma nova ferramenta), o mesmo PR — ou um PR imediato de follow-up no repo de docs — deve atualizar as páginas afetadas.

- **Mudança de CLI** → [Guia do usuário: CLI](/pt-BR/user-guide/cli/) e [Referência: Comandos CLI](/pt-BR/reference/cli-commands/).
- **Mudança de config** → [Configuração](/pt-BR/configuration/) e [Referência: Schema de config](/pt-BR/reference/config-schema/).
- **Nova ferramenta** → [Guia do usuário: Tools](/pt-BR/user-guide/tools/).
- **Novo transporte** → `content/transports/<name>.md`.
- **Novo provider** → `content/providers/<name>.md`.
- **Mudança comportamental** → [Changelog](/pt-BR/changelog/).

## Processo de release

Releases são cortadas de `main`:

1. Atualize entradas do changelog.
2. Marque como `vX.Y.Z` no commit de release.
3. O workflow `release` builda via GoReleaser, gera um SBOM CycloneDX, publica uma assinatura cosign dos checksums e gera provenance SLSA-3.
4. Consumidores verificam pela receita em [Segurança](/pt-BR/security/) e [Instalação](/pt-BR/getting-started/installation/).

O rousseau segue [Semantic Versioning](/pt-BR/getting-started/updating/): patch corrige bugs, minor adiciona features de forma não-quebradora, major quebra — sempre com uma receita de migração.

## Governança

`rousseau-agent` é um projeto de mantenedor único. A autoridade de decisão fica com o mantenedor registrado em `go.mod` e `LICENSE`. Contribuidores propõem mudanças de direção via discussão de PR ou por email para `sebastian.rousseau@gmail.com`.

## Disclosures de segurança

**Não abra uma issue pública para um report de segurança.** Envie email para `sebastian.rousseau@gmail.com` conforme a [Política de segurança](/pt-BR/security/). Reconhecimento em até 72 horas.

## Próximo

- [Arquitetura](/pt-BR/developer-guide/architecture/) — o mapa antes de você mudá-lo.
- [Testing](/pt-BR/developer-guide/testing/) — o padrão que o revisor espera.
- [Segurança](/pt-BR/security/) — o caminho de disclosure.
