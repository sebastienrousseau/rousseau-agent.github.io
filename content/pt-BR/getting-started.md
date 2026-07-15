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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/getting-started/"
subtitle: "Instale o rousseau-agent e chegue ao seu primeiro transporte."
tags: "install, quickstart, getting-started"
title: "Começando"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Começando"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Começando"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Começando"
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

## Para quem é isto

- **Desenvolvedores individuais** que querem um assistente de codificação executando em seu próprio laptop e acionando o `claude` CLI já existente. Sem chaves de API passando pela configuração do rousseau, sem broker de nuvem no meio.
- **Operadores de plataforma** executando um agente de codificação compartilhado para uma equipe atrás de um perímetro corporativo. O Rousseau é um único binário Go estático em um contêiner Podman rootless com capabilities removidas — implantável ao lado de qualquer outro serviço systemd.
- **Revisores de segurança** avaliando um agente antes da adoção. Proveniência SLSA-3, checksums de release assinados com cosign, SBOM CycloneDX, builds reproduzíveis, e cada limite de confiança está documentado em [Segurança](/pt-BR/security/).

## O caminho mais rápido

1. **Se você já tem o `claude` CLI instalado e autenticado,** o início mais rápido é `rousseau chat` com o provider padrão `claudecli` — a autenticação é herdada, não há chaves a serem canalizadas. Continue com [Primeira execução](#first-run) abaixo.
2. **Se você quer um caminho direto de API com sua própria chave,** defina `ANTHROPIC_API_KEY` e altere `provider: anthropic` em `~/.config/rousseau/config.yaml`. Veja [Provedor Anthropic](/pt-BR/providers/anthropic/).
3. **Se você está numa empresa com AWS Bedrock ou Google Vertex,** escolha o provider correspondente — [Bedrock](/pt-BR/providers/bedrock/) usa a cadeia de credenciais padrão da AWS; [Vertex](/pt-BR/providers/vertex/) lê um JSON de service-account. Nenhum segredo fica no arquivo de configuração do rousseau.
4. **Se você está isolado da internet ou quer inferência totalmente auto-hospedada,** aponte o rousseau para um endpoint compatível com OpenAI — Ollama, vLLM, LM Studio ou qualquer camada de compatibilidade. Veja [Provedor compatível com OpenAI](/pt-BR/providers/openai-compatible/).

## O que você terá ao final

- Um binário `rousseau` no `$PATH` verificado contra uma assinatura cosign (caminho de release) ou compilado a partir do código-fonte (`make check` executa o mesmo gate de 18 linters + race + govulncheck que o CI impõe).
- Um TUI `rousseau chat` funcional com o provider escolhido.
- Um armazenamento de sessões SQLite em `~/.local/share/rousseau/sessions.db` — cada turno é persistido, com recall entre sessões disponível via FTS5.
- Opcionalmente: um transporte de chat ao vivo (WhatsApp, Slack, Signal, ...) acessível do seu telefone.

## Prefere assistir?

Um screencast curto do fluxo abaixo está no roadmap. Até lá, toda a cerimônia cabe nesta página — a maioria dos operadores termina em menos de dez minutos.

## Requisitos do sistema

| Requisito | Versão | Notas |
|---|---|---|
| Toolchain Go | 1.26+ | `CGO_ENABLED=0`; o binário é totalmente estático. |
| Container runtime | Podman 4.4+ | A implantação de referência usa Podman rootless + uma unidade Quadlet do systemd. Docker funciona, mas Quadlet é específico do Podman. |
| `claude` CLI | latest | Somente ao usar o provider padrão `claudecli`. |
| `signal-cli` | 0.13+ | Somente ao usar o transporte Signal. |
| Servidor BlueBubbles | 1.9+ | Somente ao usar o transporte iMessage (host macOS necessário). |
| `whisper.cpp` | 1.5+ | Somente se você habilitar a transcrição de notas de voz do WhatsApp. |

## Instalação

### A partir do código-fonte

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` executa vet, `golangci-lint`, `go test -race` e `govulncheck` — os mesmos gates que o CI impõe.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

O binário incorpora `modernc.org/sqlite`, então não há dependência de libc ou CGo em runtime.

### A partir de uma release assinada

Toda release com tag publica um arquivo com checksums, um SBOM CycloneDX, uma atestação de proveniência SLSA-3 e uma assinatura cosign do arquivo de checksum. Sempre verifique antes de executar:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

A regex de certificate-identity é o que fixa a identidade do assinante; não a enfraqueça.

## Primeira execução

### Chat no terminal

```sh
rousseau chat
```

TUI Bubble Tea. Enter para enviar, `Ctrl+C` para sair. O provider padrão é `claudecli`, que herda a autenticação da sua instalação local do Claude Code; nenhuma chave de API é canalizada através da configuração do rousseau.

O histórico de sessão é persistido em `~/.local/share/rousseau/sessions.db` (SQLite com journaling WAL e FTS5 para recall entre sessões).

### Primeiro transporte de chat

WhatsApp é o transporte de referência (a UX de pareamento é a mais rigorosa). Pareie na primeira execução escaneando o QR do seu telefone:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

O JID E.164 (`<digits>@s.whatsapp.net`) restringe o tratamento de entrada; qualquer outro remetente é silenciosamente descartado. O estado de pareamento é armazenado em `whatsapp.db` junto ao armazenamento de sessões.

Outros transportes seguem o mesmo formato:

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

Cada `rousseau <transport> --help` lista suas flags. Os padrões vêm de `~/.config/rousseau/config.yaml`.

## Onde o estado é armazenado

| Caminho | Finalidade |
|---|---|
| `~/.config/rousseau/config.yaml` | Arquivo de configuração no nível do usuário (Viper). |
| `~/.local/share/rousseau/sessions.db` | Sessões, jobs cron, mapa de JID, índice de recall FTS5. |
| `~/.local/share/rousseau/whatsapp.db` | Credenciais de dispositivo do Whatsmeow (mantidas separadas para que um relink de dispositivo não afete conversas). |
| `~/.claude/` | Tokens OAuth do `claude` CLI, apenas ao usar o provider `claudecli`. |

## Próximos passos

- [Conceitos](/pt-BR/concepts/) — o loop do agente, o armazenamento de sessões, MCP, cron, skills.
- [Configuração](/pt-BR/configuration/) — todos os ajustes.
- [Implantação](/pt-BR/deployment/) — como executar o daemon sob systemd.
