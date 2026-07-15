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
description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/quickstart/"
subtitle: "rousseau em cinco minutos: instalar, configurar, conversar, verificar."
tags: "quickstart, install, provider, transport, supply-chain"
title: "Início rápido"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Início rápido"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Início rápido"
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
twitter_description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Início rápido"
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

## rousseau em 5 minutos

Rousseau é um único binário Go estático que vem com uma TUI Bubble Tea, um armazenamento de sessão SQLite em `~/.local/share/rousseau/sessions.db` e nove transportes de chat (WhatsApp, Signal, Telegram, Slack, Discord, Matrix, iMessage, SMS, email). Sem plano de controle SaaS, sem telemetria, sem servidor de licenças. Você fornece o LLM.

Esta página o leva do início ao fim:

- [ ] **1. Instalar rousseau** — do código-fonte, `go install` ou de uma release verificada por cosign.
- [ ] **2. Configurar seu LLM** — escolha um provider (`claudecli` por padrão; Anthropic, Bedrock, Vertex ou qualquer endpoint compatível com OpenAI).
- [ ] **3. Ter sua primeira conversa** — `rousseau chat` no seu terminal.
- [ ] **4. Adicionar um transporte** — parear WhatsApp com um JID permitido.
- [ ] **5. Verificar a cadeia de suprimentos** — verificar com cosign o arquivo de checksums, depois ler o SBOM CycloneDX e a proveniência SLSA-3.

A maioria dos operadores termina em menos de dez minutos.

## 1. Instalar rousseau

<aside class="admonition" data-type="tip"><span class="admonition-title">Recomendado</span><p><code>go install</code> é o caminho mais rápido se você já tem Go 1.26+. Para produção, use uma release assinada com <code>cosign verify-blob</code> para manter as garantias da cadeia de suprimentos.</p></aside>

<div class="tabs" data-tabs="qs-install">
  <div class="tab-list" role="tablist" aria-label="Método de instalação">
    <button role="tab" aria-selected="true">go install</button>
    <button role="tab" aria-selected="false">A partir do código-fonte</button>
    <button role="tab" aria-selected="false">Release assinada</button>
    <button role="tab" aria-selected="false">Contêiner</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
rousseau version
```

O binário embute `modernc.org/sqlite` (veja `internal/state/sqlite/store.go`), portanto não há dependência de libc ou CGo em tempo de execução. Funciona de forma idêntica em macOS, Linux e Windows.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` executa `go vet`, `golangci-lint`, `go test -race` e `govulncheck` — os mesmos gates que a CI aplica.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Cada release marcada publica um arquivo com checksum, um SBOM CycloneDX, uma atestação de proveniência SLSA-3 e uma assinatura cosign sobre o arquivo de checksums:

```sh
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_linux_amd64.tar.gz
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt.sig

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt

sha256sum -c rousseau_0.6.0_checksums.txt --ignore-missing
tar -xzf rousseau_0.6.0_linux_amd64.tar.gz
sudo install -m 0755 rousseau /usr/local/bin/
```

<aside class="admonition" data-type="note"><span class="admonition-title">Nota</span><p>A identidade <code>cosign</code> está restrita ao OIDC do GitHub Actions de <code>sebastienrousseau/rousseau-agent</code>. Veja <a href="/pt-BR/security/">Segurança</a> para a raiz de confiança.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau vem com um `Dockerfile` amigável ao Podman em `docker/Dockerfile` e uma unidade Quadlet do systemd em `docker/rousseau-agent.container`. Uma imagem publicada em ghcr.io está no roadmap; enquanto isso, faça o build localmente:

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Veja [Implantação](/pt-BR/deployment/) para a unidade Quadlet de referência com postura de runtime endurecida (rootless, `DropCapability=all`, `NoNewPrivileges=true`, seccomp).

  </div>
</div>

### Pré-requisitos específicos do SO

<div class="tabs" data-tabs="qs-os">
  <div class="tab-list" role="tablist" aria-label="Sistema operacional">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
brew install go@1.26
# For the container path:
brew install podman
podman machine init && podman machine start
```

Para o provider `claudecli` padrão, instale o Claude Code em https://claude.ai/download e execute `claude login` uma vez.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Instale Go 1.26+ pelo seu gerenciador de pacotes ou em https://go.dev/dl. Para o caminho de container, use Podman rootless ≥ 5.x com modo de rede `pasta`.

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI (opcional, para o provider `claudecli`): baixe em https://claude.ai/download.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau roda nativamente no Windows via `go install`. A implantação de referência por container é apenas para Linux; no Windows, use WSL 2 para o caminho Podman.

```powershell
winget install GoLang.Go
# Or: choco install golang
```

Para `claudecli`, instale o Claude Code em https://claude.ai/download.

<aside class="admonition" data-type="warning"><span class="admonition-title">Nota sobre Windows</span><p>Alguns pacotes de transporte chamam subprocessos (<code>signal-cli</code>) ou abrem caminhos específicos do SO (<code>~/.local/share/</code>). Os transportes <code>whatsapp</code>, <code>slack</code>, <code>discord</code>, <code>telegram</code>, <code>matrix</code>, <code>email</code>, <code>sms</code> são todos multiplataforma. <code>signal</code> e <code>imessage</code> requerem suas respectivas ferramentas de host.</p></aside>

  </div>
</div>

## 2. Configurar seu LLM

A configuração fica em `~/.config/rousseau/config.yaml` (sobrescrevível com `--config`) e cada campo é definido em `internal/config/config.go`. O provider padrão é `claudecli`, que delega para sua CLI `claude` local, de modo que nenhuma chave de API sai do seu laptop.

### claudecli (padrão, sem chaves)

Se você já tem Claude Code (`claude`) instalado e autenticado, está pronto. Rousseau herda sua sessão OAuth:

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

Veja [Providers: claudecli](/pt-BR/providers/claudecli/).

### API da Anthropic

Anthropic direto. Usa o SDK oficial `anthropic-sdk-go` em `internal/llm/anthropic/client.go`:

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` é lida diretamente do ambiente (veja `config.Load` em `internal/config/config.go`); a chave nunca precisa estar em disco. Veja [Providers: Anthropic](/pt-BR/providers/anthropic/).

### AWS Bedrock

Usa a cadeia padrão de credenciais AWS (perfil, IMDS, IRSA). Região e modelo vêm de `BedrockConfig` em `internal/config/config.go`:

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

Nenhuma chave de API em `config.yaml`. Veja [Providers: Bedrock](/pt-BR/providers/bedrock/).

### Google Vertex AI

Anthropic no Vertex; lê um arquivo JSON de conta de serviço. Campos de configuração definidos em `VertexConfig`:

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

Veja [Providers: Vertex](/pt-BR/providers/vertex/).

### Compatível com OpenAI (OpenRouter, Ollama, vLLM, LM Studio)

Os nomes de provider `openai`, `openrouter` e `ollama` compartilham `OpenAIConfig`. URLs base para OpenRouter e Ollama têm padrões em `setDefaults` (`https://openrouter.ai/api/v1` e `http://localhost:11434/v1`); qualquer outra coisa cai no bloco `openai` com um `base_url` explícito:

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

Veja [Providers: Compatível com OpenAI](/pt-BR/providers/openai-compatible/) e [Guias: vLLM auto-hospedado](/pt-BR/guides/self-hosted-vllm/).

## 3. Ter sua primeira conversa

```sh
rousseau chat
```

Você verá uma TUI Bubble Tea (`internal/tui/model.go`):

- Um **viewport** no topo rola a transcrição. O texto do assistente é transmitido conforme chega.
- Uma **área de texto** na parte inferior recebe sua entrada. Pressione `Enter` para enviar, `Ctrl+C` para sair.
- Um **spinner** aparece durante os turnos do LLM; um pequeno indicador de streaming aparece enquanto os tokens chegam.
- Cada turno é persistido em SQLite em `~/.local/share/rousseau/sessions.db`. O journaling WAL é habilitado por `Open()` em `internal/state/sqlite/store.go`, então você pode executar com segurança outros comandos rousseau (`rousseau session list`, `rousseau mcp`) contra o mesmo banco de dados enquanto a TUI está aberta.

Comece pedindo algo pequeno — por exemplo, "liste os arquivos em `internal/tools/builtin`" — e rousseau chamará as ferramentas embutidas `read`, `grep`, `edit`, `write` ou `bash` (`internal/tools/builtin/*.go`) conforme necessário. Veja [Guia do usuário: TUI](/pt-BR/user-guide/tui/) para os atalhos de teclado e [Guia do usuário: Ferramentas](/pt-BR/user-guide/tools/) para os esquemas.

Placeholder de captura de tela: a TUI mostra uma barra de status de duas linhas (id de sessão e provider), o viewport com mensagens do assistente + usuário tingidas em cor e a área de texto em foco na parte inferior.

## 4. Adicionar um transporte (WhatsApp)

WhatsApp é o transporte de referência porque o pareamento é o mais rigoroso. Todos os outros transportes (`slack`, `discord`, `telegram`, `matrix`, `signal`, `sms`, `imessage`, `email`) seguem a mesma forma.

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

No primeiro lançamento, `rousseau` imprime um QR code em stdout. Escaneie-o em **WhatsApp > Configurações > Aparelhos conectados** no seu telefone. O cliente whatsmeow (`internal/transport/whatsapp/client.go`) emite três eventos de log estruturados:

- `whatsapp.qr_ready` — QR foi renderizado.
- `whatsapp.paired` — telefone aceitou o QR.
- `whatsapp.connected` — websocket para a Meta está ativo.

As credenciais do dispositivo são armazenadas em cache em `~/.local/share/rousseau/whatsapp.db` (um banco de dados SQLite separado, então religar um dispositivo não afeta o histórico de conversas). O flag `--allow` fixa uma allowlist de JIDs E.164; qualquer outro remetente é silenciosamente descartado por `router.transport.rejected`.

Rousseau usa o protocolo **não oficial** do WhatsApp Web. A Meta ocasionalmente bane números que executam clientes não oficiais — não execute isso em um número do qual você depende. Veja [Transportes: WhatsApp](/pt-BR/transports/whatsapp/) para a análise de risco.

## 5. Verificar a cadeia de suprimentos

Cada release marcada entrega:

| Artefato | Propósito |
|---|---|
| `rousseau_<v>_checksums.txt` | SHA-256 de cada arquivo na release. |
| `rousseau_<v>_checksums.txt.sig` | Assinatura cosign (keyless, emitida por OIDC do GitHub Actions). |
| `rousseau_<v>_sbom.cdx.json` | SBOM CycloneDX 1.5 do grafo de módulos Go. |
| `rousseau_<v>_provenance.intoto.jsonl` | Atestação de proveniência SLSA-3. |

Verifique a identidade da assinatura antes de confiar nos checksums:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

O `--certificate-identity-regexp` fixa a identidade do signatário ao repositório rousseau-agent sob o namespace do Sebastien. **Não o enfraqueça.** Uma identidade curinga anula o propósito da assinatura keyless.

Uma vez que a assinatura é verificada, `sha256sum -c` prova que o tarball que você baixou é aquele que a CI construiu. Leia o SBOM com `cyclonedx-cli tree`, verifique a proveniência SLSA-3 com `slsa-verifier verify-artifact` e só então extraia o arquivo.

Veja [Segurança](/pt-BR/security/) para os limites de confiança completos e [Guias: Onboarding empresarial](/pt-BR/guides/enterprise-onboarding/) para o checklist da equipe de plataforma.

## Solução de problemas

<aside class="admonition" data-type="tip"><span class="admonition-title">Primeira parada recomendada</span><p>Execute <code>rousseau doctor</code> antes de abrir uma issue. Ele exercita cada subsistema — auth do provider, armazenamento de estado, credenciais de transporte — e imprime linhas estruturadas pass/warn/fail.</p></aside>

### `rousseau version` imprime "dev" após `go install`

Os valores `version`, `commit` e `buildDate` são carimbados pela toolchain de release via `-ldflags` em `internal/cli/root.go`. `go install` ignora essas flags, então o binário reporta `dev / none / unknown`. Use o caminho de release assinada se precisar de uma string de versão estável; a string `dev` é inofensiva em tempo de execução.

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` delega para o binário `claude`. Ou coloque o Claude Code no seu `$PATH` (veja [Providers: claudecli](/pt-BR/providers/claudecli/)) ou troque de provider — a alternativa mais rápida é `provider: anthropic` com `ANTHROPIC_API_KEY` exportada.

### QR do WhatsApp é exibido mas nunca aceito

Três causas comuns: (1) o relógio do container está desajustado em mais de 30 segundos — o handshake do WhatsApp é sensível ao tempo; (2) um pareamento parcialmente concluído deixou `whatsapp.db` em um estado inutilizável — apague `~/.local/share/rousseau/whatsapp.db` e escaneie novamente; (3) a Meta invalidou o número — tente um número de telefone novo. Veja [Transportes: WhatsApp](/pt-BR/transports/whatsapp/).

### `cosign verify-blob` retorna erro "no matching signatures"

O `--certificate-identity-regexp` deve corresponder ao repositório GitHub do signatário. Para rousseau-agent, o valor correto é `sebastienrousseau/rousseau-agent`. Um curinga anula o propósito da assinatura keyless — não o enfraqueça. Se a regex estiver correta, atualize a raiz de confiança do Sigstore com `cosign initialize`.

### Cada chamada de ferramenta é negada com "denied by pattern policy"

Você está rodando no modo `pattern` com `default: deny` e nenhuma regra de permissão correspondente. Adicione uma entrada de permissão para a ferramenta, ou inverta para `default: allow` e adicione regras de negação estreitas. Veja [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) para exemplos trabalhados.

## Páginas relacionadas

- [Primeiros passos: Instalação](/pt-BR/getting-started/installation/) — cada método de instalação com a receita de verificação.
- [Primeiros passos: Primeiro transporte](/pt-BR/getting-started/first-transport/) — walkthrough de ponta a ponta de WhatsApp/Slack/Discord.
- [Configuração](/pt-BR/configuration/) — cada parâmetro em `~/.config/rousseau/config.yaml`.
- [Conceitos](/pt-BR/concepts/) — o loop do agente, o armazenamento de sessão, MCP, cron, skills.
- [Solução de problemas](/pt-BR/troubleshooting/) — o catálogo completo de modos de falha.

## Leitura adicional

- `README.md` — posicionamento no nível do repositório e matriz de capacidades.
- `SECURITY.md` — limites de confiança e endurecimento da cadeia de suprimentos.
- `internal/config/config.go` — a struct de configuração autoritativa.
- `internal/cli/root.go` — cabeamento da árvore de comandos Cobra.

## Próximos passos

| Para onde ir | Por quê |
|---|---|
| [Configuração](/pt-BR/configuration/) | Cada parâmetro em `~/.config/rousseau/config.yaml` com padrões. |
| [Conceitos](/pt-BR/concepts/) | O loop do agente, o armazenamento de sessão, MCP, cron, skills. |
| [Implantação](/pt-BR/deployment/) | Podman rootless + unidade Quadlet do systemd. |
| [Segurança](/pt-BR/security/) | Limites de confiança, proveniência SLSA-3, postura seccomp. |
| [Tutoriais](/pt-BR/tutorials/) | Walkthroughs completos de ponta a ponta. |
| [Referência](/pt-BR/reference/cli-commands/) | Cada flag da CLI, código de saída e campo de configuração. |
