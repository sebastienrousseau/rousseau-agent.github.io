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
description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "Segurança"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Segurança"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Segurança"
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
twitter_description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Segurança"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>O modelo de ameaças do rousseau em prosa e em diagrama ASCII, os limites críticos (política de aprovação, isolamento do contêiner, cadeia de suprimentos), o filtro seccomp de referência e como apertá-lo ainda mais, a política de egresso de rede e a trilha de auditoria que aparece no <code>slog</code>. Cruze com <code>SECURITY.md</code> na árvore de código-fonte e com <code>docker/rousseau-agent.container</code> para a verdade absoluta.</p></aside>

## Diagrama do modelo de ameaças

```
                          ┌──────────────────────────────────┐
                          │        Chat transport user       │
                          │   (WhatsApp / Slack / Discord)   │
                          └──────────────────┬───────────────┘
                                             │ E2EE (WhatsApp)
                                             │ TLS   (Slack / Discord / …)
                        ─────────────────────┴─────────────────────
                                             │
                                             ▼
      ┌─────────────── rousseau-agent container ────────────────┐
      │                                                          │
      │   ┌─────────────┐    inbound     ┌──────────────────┐   │
      │   │  Transport  │ ───────────▶   │  Router          │   │
      │   │  adapter    │                │  + allowlist     │   │
      │   └─────────────┘                └────────┬─────────┘   │
      │                                           │             │
      │                                           ▼             │
      │                                   ┌─────────────┐       │
      │                                   │   Agent     │       │
      │                                   │  Turn loop  │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │                            approver     │              │
      │                          ◀───────────────┤              │
      │                                          ▼              │
      │                                   ┌─────────────┐       │
      │                                   │  Registry   │       │
      │                                   │ read/edit/  │       │
      │                                   │ bash/…      │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │  ROOTFS  ReadOnly=true  ─────────────────┤              │
      │  CAPS    DropCapability=all              │              │
      │  UID     1000, keep-id                   │              │
      │  SECCOMP default filter                  │              │
      │                                          │              │
      │            outbound TLS                  ▼              │
      └──────────────────┬───────────────────────┬──────────────┘
                         │                       │
                         ▼                       ▼
                ┌────────────────┐    ┌─────────────────────┐
                │  LLM provider  │    │  bind mounts        │
                │  (Anthropic /  │    │  ~/.local/share/    │
                │   Bedrock /    │    │    rousseau/  RW    │
                │   Vertex / …)  │    │  workspace/   RW    │
                └────────────────┘    │  ~/.claude/   RW    │
                                      └─────────────────────┘
```

Tudo dentro da caixa do contêiner está sob controle do rousseau. O ingresso do transporte de chat chega já criptografado E2EE (WhatsApp) ou criptografado com TLS (Slack, Discord, Matrix, Telegram, Email, SMS). O egresso para o provider LLM é TLS. Bind mounts são o único acesso do daemon ao filesystem do host.

## Modelo de confiança — o que está no escopo

O `rousseau-agent` é um **daemon local, container-native**. Três limites críticos:

### 1. O shell do usuário

A tool embutida `bash` executa comandos arbitrários com os privilégios do usuário. **Este é o limite de segurança primário.** Cada chamada de tool é exibida antes da execução e está sujeita à política de aprovação configurada (`allow_all`, `deny_all` ou modo `pattern` com regras regex de allow / deny por tool e um padrão configurável).

Operadores executando daemons não-atendidos (transportes de chat) **devem** ou:

- impor o modo `pattern` com `default: deny` e regras explícitas de allow, ou
- aceitar a postura `bypassPermissions` com entendimento explícito da exposição.

Não há meio-termo em que o modelo se auto-limita. Se o daemon pode executar shell e é acessível a partir de um transporte de chat, os usuários com acesso podem, em princípio, controlar o shell.

### 2. Isolamento do contêiner

A implantação de referência é um contêiner Podman rootless com:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- Filtro seccomp padrão (`/usr/share/containers/seccomp.json`)
- UID não-root 1000
- Mapeamento de user-namespace `keep-id`
- `Network=pasta` (rootless, sem entrada-do-host por padrão)

Apenas o bind mount do workspace, o diretório de estado e `~/.claude` são visíveis de dentro do contêiner. Veja [/deployment/](/pt-BR/deployment/).

### 3. Cadeia de suprimentos

Cada commit executa `govulncheck` e CodeQL. Cada release entrega:

- **Proveniência SLSA Nível 3** via `slsa-framework/slsa-github-generator`, assinada através do OIDC do GitHub Actions.
- **Assinatura cosign** no arquivo de checksum, verificável contra o log de transparência do Sigstore.
- **SBOM CycloneDX JSON.**
- **Atestação de build reproduzível** — um job dedicado do CI verifica saída bit-idêntica a partir de um checkout novo.

## Modelo de confiança — o que está fora do escopo

- **Saída maliciosa do modelo.** O operador é responsável por revisar as chamadas de tool antes de aprová-las. Políticas de aprovação tornam isso menos propenso a erros; não eliminam a necessidade de julgamento humano.
- **Toolchain Go, runtime de contêiner ou OS do host comprometidos.** Um ambiente de build confiável é assumido.
- **Acesso físico à máquina.**
- **Ataques contra o próprio provider LLM.** Vulnerabilidades do provider são responsabilidade do provider.

## Controles da cadeia de suprimentos

| Controle | Implementação |
|---|---|
| Fixação de dependências diretas | Versões exatas em `go.mod`; resolução transitiva congelada em `go.sum`. |
| Varredura de vulnerabilidades | `govulncheck ./...` em cada build do CI. Builds falham em qualquer vulnerabilidade conhecida que atinja um símbolo importado. |
| Análise estática | `golangci-lint` v2 (18 linters) + GitHub CodeQL (Go). |
| Atualizações de dependências | Dependabot para `gomod` e `github-actions`, cadência semanal. |
| Proveniência de build | SLSA Nível 3 via `slsa-framework/slsa-github-generator`; atestada através do OIDC do GitHub Actions e publicada no log de transparência do Sigstore. |
| Assinatura de release | Checksums de release são assinados com cosign (keyless, via OIDC do GitHub Actions). |
| Software bill of materials | SBOM CycloneDX JSON anexado a cada artefato de release. |
| Builds reproduzíveis | Job dedicado `reproducible-build` do CI verifica saída bit-idêntica. |

Arquivos de workflow do CI ficam em `.github/workflows/` na árvore de código-fonte: `ci.yml`, `codeql.yml`, `slsa.yml`, `release.yml`, `reproducible-build.yml`.

## Verificando uma release

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

As duas flags que fixam a identidade:

- `--certificate-identity-regexp` casa com o repositório GitHub que emite o certificado de assinatura. Nunca amplie isso para `.*`; é o que impede a assinatura cosign de outro repositório de validar contra seu arquivo de checksum.
- `--certificate-oidc-issuer` fixa o emissor OIDC no GitHub Actions.

A entrada do log de transparência do Sigstore pode ser consultada separadamente em https://search.sigstore.dev/.

## Controles de runtime

Cada configuração abaixo está definida na unidade Quadlet de referência e pertence a qualquer baseline de operador de contêiner:

- **Usuário não-root (UID 1000)** — sem privilégio para escalar para root dentro do contêiner.
- **`ReadOnly=true`** — a imagem não é gravável em runtime; o binário não pode mutar a si mesmo ou suas dependências.
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`** — o único local gravável fora dos bind mounts.
- **`DropCapability=all`** — nenhum bit `CAP_*` definido. TCP de saída não requer nenhum.
- **`NoNewPrivileges=true`** — bloqueia escalada setuid.
- **Filtro seccomp padrão** — gating de syscalls no nível do kernel.
- **`Network=pasta`** — stack de rede rootless; sem entrada do host por padrão.
- **Sem portas publicadas** — nenhum `PublishPort=` no Quadlet. Não há superfície HTTP de entrada a publicar.

## Inventário de criptografia

| Uso | Implementação |
|---|---|
| TLS para endpoints LLM / transporte | Biblioteca padrão Go `crypto/tls` com o trust store do sistema. |
| WhatsApp | `whatsmeow` (protocolo Signal). |
| Matrix | API client-server sobre HTTPS. |
| SMTP (transporte de email) | Biblioteca padrão Go `net/smtp` com `PlainAuth` sobre TLS. |
| Armazenamento de sessão em repouso | **Não criptografado na camada de aplicação.** Operadores que requerem criptografia em repouso devem montar o diretório de estado em um filesystem criptografado (LUKS, FileVault). |

Nenhuma primitiva criptográfica personalizada é implementada neste projeto.

## Divulgação

Reporte privadamente para **sebastian.rousseau@gmail.com**. **Não** abra uma issue pública para reports que afetem a segurança.

Inclua:

- Descrição concisa e vetor CVSS 3.1.
- Componente afetado (caminho do arquivo + faixa de linhas, ou caminho de módulo de dependência).
- Detalhes do ambiente (`rousseau version`, versão do Go, OS, runtime de contêiner).
- Reprodução mínima — idealmente um teste que falhe.

### Compromissos de resposta

| Evento | SLA |
|---|---|
| Confirmação do report | ≤ 72 horas |
| Decisão de triagem (aceitar / recusar / precisar-de-info) | ≤ 7 dias |
| Correção entregue para **Crítico** (CVSS ≥ 9.0) | ≤ 14 dias |
| Correção entregue para **Alto** (7.0–8.9) | ≤ 30 dias |
| Correção entregue para **Médio / Baixo** | agendada em uma release rotineira |
| Divulgação pública (coordenada) | após a release da correção |

## Versões suportadas

Apenas a branch `main` e a release taggada mais recente recebem correções de segurança. Não há branches de suporte de longo prazo.

## Detalhamento do filtro seccomp

A unidade Quadlet de referência usa o perfil seccomp padrão do Podman em `/usr/share/containers/seccomp.json`. Ele bloqueia cerca de 70 syscalls que nenhuma invocação correta do rousseau precisa, incluindo:

| Família de syscall | Bloqueado | Justificativa |
|---|---|---|
| Keyring do kernel (`add_key`, `keyctl`, `request_key`) | sim | O rousseau não toca no keyring do kernel. |
| Gerenciamento de mount (`mount`, `umount`, `pivot_root`, `chroot`) | sim | Sem mudanças dinâmicas de mount em runtime. |
| Módulos do kernel (`init_module`, `finit_module`, `delete_module`) | sim | O daemon não pode carregar módulos do kernel. |
| Jogos de namespace (`setns`, `unshare` com certas flags) | filtrado | Impede escape do contêiner via troca de namespace. |
| Primitivas de debug (`ptrace`, `process_vm_readv`, `process_vm_writev`) | sim | O rousseau não se conecta a outros processos. |
| BPF (`bpf`) | sim | Sem programas eBPF de dentro do contêiner. |
| Reboot (`reboot`, `kexec_*`) | sim | Contêiner não tem razão legítima para reiniciar o host. |
| Mudanças de relógio (`clock_settime`, `adjtimex`) | sim | O tempo é gerenciado pelo host. |

O perfil padrão permite syscalls suficientes para a biblioteca padrão, o driver SQLite (`modernc.org/sqlite`), o cliente whatsmeow e os SDKs OpenAI/Anthropic. Se você precisar apertar mais — ex.: remover `personality` porque nunca emula outras ABIs — copie o perfil padrão, remova a syscall e referencie a cópia via `SeccompProfile=/path/to/profile.json` no Quadlet.

<aside class="admonition" data-type="caution"><span class="admonition-title">Teste de perfil mais rígido</span><p>Cada ajuste de seccomp precisa de cobertura no seu smoke test — uma syscall que você não sabia que o rousseau precisava fará com que uma completion ou transporte falhe em runtime. Teste com um round-trip real de chat antes de subir para produção.</p></aside>

## Política de egresso de rede

Por padrão, o contêiner não tem ingresso e egresso irrestrito (`Network=pasta`). Para implantações de alta segurança, adicione um conjunto de regras nftables que permita apenas os domínios que o rousseau precisa:

```
# /etc/nftables.d/rousseau.nft — example only, adjust to your provider
table inet rousseau_out {
    chain output {
        type filter hook output priority 0; policy drop;

        # LLM providers
        ip daddr { 3.5.0.0/16, 15.230.0.0/16 } tcp dport 443 accept  # Anthropic + Bedrock
        ip daddr { 34.107.0.0/16 } tcp dport 443 accept              # Vertex

        # Chat transports
        ip daddr { 157.240.0.0/16 } tcp dport 443 accept             # Meta (WhatsApp)
        ip daddr { 3.208.0.0/16 } tcp dport 443 accept               # Slack

        # DNS
        udp dport 53 accept
        tcp dport 53 accept

        # NTP
        udp dport 123 accept
    }
}
```

Ranges de CIDR mudam — trate o acima como scaffolding. O ponto é que o egresso do rousseau é finito e enumerável; o exemplo `docker/example-nftables.rules` no código-fonte é um conjunto de regras inicial.

## Trilha de auditoria via slog

Cada evento relevante para segurança é logado via `log/slog` do Go em nível JSON estruturado (`log.format: json`). Os eventos que você deve monitorar em produção:

| Evento | Nível | Origem | O que ele diz |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | Qual tool o modelo pediu para executar, em qual sessão. |
| `tool.denied` | warn | `internal/agent/agent.go` | Um approver negou uma chamada; contém a string de motivo. |
| `tool.error` | warn | `internal/agent/agent.go` | A tool executou mas retornou um erro. |
| `router.transport.rejected` | info | `internal/transport/router.go` | Uma mensagem de entrada falhou na allowlist. |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | A Meta invalidou o pareamento. |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | Um handler de tool MCP retornou um erro. |
| `cron.delivery_failed` | warn | `internal/cron/` | A entrega do transporte de um job agendado deu erro. |

Alimente o stream JSON para Loki / Datadog / Splunk / um pipeline Vector; veja [Guias: Observabilidade](/pt-BR/guides/observability/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Nomenclatura de campos</span><p>Chaves de atributos do slog têm namespace por ponto (<code>whatsapp.connected</code>, não <code>event=whatsapp_connected</code>). Consulte com a chave bruta em qualquer ferramenta de log que você use.</p></aside>

## Solução de problemas

### Contêiner recusa a iniciar com `mount: permission denied`

Incompatibilidade de rótulo SELinux. Garanta que cada linha de bind mount termine com `:Z` (rótulo privado) ou `:z` (compartilhado). Sem um rótulo, o processo do contêiner não pode ler/gravar arquivos que foram rotulados pelo host.

### Seccomp está matando uma syscall que preciso

Podman imprime `syscall X blocked` no journal. Reproduza com `strace -f -e trace=X` fora do contêiner para confirmar o que precisa da chamada. Se for legítima, copie o perfil seccomp padrão, adicione a syscall à allow-list e referencie o perfil via `SeccompProfile=`.

### `cosign verify-blob` mostra "certificate identity does not match"

Sua `--certificate-identity-regexp` está errada. Use `sebastienrousseau/rousseau-agent`. Qualquer regex mais frouxa (`.*`, `.+`) derrota o propósito da assinatura keyless.

### Egresso do provider falha sob restrições do nftables

Seu conjunto de regras não inclui o range de IP atual do provider. Providers rotacionam CIDRs. Use egresso baseado em DNS com um ipset que resolve em um cron, ou use um proxy de egresso que resolve nomes no momento da conexão.

### Nada no slog quando espero eventos de auditoria

Nível de log muito alto. Defina `log.level: info` (ou `debug` para detalhes no nível do wire) e confirme que o daemon realmente inicia uma nova sessão — `slog.Default()` é usado antes de a configuração carregar, então mensagens de boot inicial vão para stderr em forma de texto independentemente.

## Páginas relacionadas

- [Implantação](/pt-BR/deployment/) — a unidade Quadlet de referência.
- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — a alavanca de segurança primária.
- [Guias: Prompt Injection](/pt-BR/guides/prompt-injection/) — ataques que vêm através da saída do modelo.
- [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/) — como executar um daemon "olhar, não tocar".
- [Guias: Observabilidade](/pt-BR/guides/observability/) — pipeline slog + Loki / Datadog.

## Leitura complementar

- `SECURITY.md` — o documento canônico de política.
- `docker/rousseau-agent.container` — a unidade Quadlet de referência.
- `docker/example-nftables.rules` — conjunto de regras de egresso de exemplo.
- `internal/agent/agent.go` — onde os eventos `tool.execute` e `tool.denied` são emitidos.
- `internal/agent/approver.go` — implementações de política de aprovação.
