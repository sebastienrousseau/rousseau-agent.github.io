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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "Transporte WhatsApp"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte WhatsApp"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte WhatsApp"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte WhatsApp"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Como o transporte WhatsApp pareia com seu telefone, as regras de normalização LID vs phone-JID, o fluxo de transcrição de notas de voz, downloads de mídia, padrões regex de allowlist e os modos de falha que pegam operadores de primeira vez. Leia <code>internal/transport/whatsapp/client.go</code>, <code>resolve.go</code> e <code>dispatch.go</code> junto a esta página.</p></aside>

## Visão geral

O transporte WhatsApp (`internal/transport/whatsapp/`) é apoiado por `go.mau.fi/whatsmeow` — um cliente multi-dispositivo WhatsApp Web reversamente-engenheirado. A Meta considera isso um cliente não oficial; não execute isso em um número pessoal do qual você depende para qualquer coisa importante.

A criptografia ponta a ponta do protocolo Signal é preservada (o whatsmeow usa o mesmo protocolo que o app móvel do WhatsApp). O daemon mantém as credenciais de dispositivo em um arquivo SQLite separado do store de sessões, então um relink de dispositivo não afeta o histórico de conversas.

<aside class="admonition" data-type="caution"><span class="admonition-title">Protocolo não oficial</span><p>A Meta ocasionalmente bane números que executam clientes não oficiais. Mesmo que você cumpra os rate limits do WhatsApp e se comporte com responsabilidade, um número de telefone usado com <code>whatsmeow</code> pode ser banido sem aviso. Use um número dedicado, não um pessoal.</p></aside>

## Pareamento

Primeiro lançamento:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Um código QR é impresso no stdout via `mdp/qrterminal/v3`. Escaneie-o com o app WhatsApp do telefone (**Configurações → Dispositivos conectados → Conectar um dispositivo**). O estado de pareamento é escrito em `whatsapp.db` no diretório de estado (tipicamente `~/.local/share/rousseau/whatsapp.db`).

Lançamentos subsequentes reutilizam o dispositivo pareado silenciosamente. Se o QR reaparecer, o pareamento foi revogado pelo lado do telefone — delete `whatsapp.db` e pareie novamente.

## Allowlist

`--allow` restringe o handling de entrada. Múltiplas flags acumulam:

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

O valor é um **JID** do WhatsApp — o número de telefone E.164 (sem `+`) seguido de `@s.whatsapp.net`. JIDs de grupo (`<id>@g.us`) também são suportados.

Uma allowlist vazia aceita qualquer remetente. Para um daemon de transporte de chat você sempre quer pelo menos uma entrada.

## Normalização LID vs phone-JID

O WhatsApp usa dois formatos de identificador para um usuário:

| Formato | Exemplo | Significado |
|---|---|---|
| Phone JID | `447900123456@s.whatsapp.net` | O número de telefone E.164, sem `+`, seguido de `@s.whatsapp.net`. Estável ao longo do tempo; expõe o número de telefone. |
| LID | `1234567890@lid` | Location-Independent ID — uma string de aparência aleatória que não revela o número de telefone. Também estável, mas não diretamente linkável a um número. |
| Sufixo de dispositivo | `447900123456:5@s.whatsapp.net` | Qualquer JID pode carregar um sufixo de device-address (`:N`). O WhatsApp reporta mensagens com o dispositivo específico que as enviou. |

O handler de entrada do rousseau (`ResolveInbound` em `internal/transport/whatsapp/resolve.go`) normaliza cada evento para uma forma canônica antes do dispatch:

1. **Remove o sufixo de dispositivo.** `447900:5@s.whatsapp.net` vira `447900@s.whatsapp.net`. Isso permite que allowlists escritas como JIDs de usuário simples correspondam independentemente de qual dispositivo linkado enviou a mensagem.
2. **Substitui LID pelo phone JID do titular da conta em self-chat.** Quando o titular da conta é o remetente (`IsFromMe=true`), o WhatsApp reporta o remetente como o LID da conta (um hash de privacidade), não o phone JID. O rousseau substitui pelo próprio JID da conta para que operadores possam colocar `<phone>@s.whatsapp.net` na allowlist e ter o teste de self-chat roteando corretamente.
3. **Descarta remetentes não-parseáveis.** Campos `User` ou `Server` vazios — descobertos pelo `FuzzResolveInbound` — não podem ser roteados com segurança. A mensagem é silenciosamente pulada em vez de ser passada ao handler como um From mal-formado.

### Armadilha do self-chat

Quando você envia uma mensagem para si mesmo no WhatsApp (para testar o bot), o campo do remetente chega como seu LID. Se você colocou seu phone JID na allowlist, a busca ingênua falharia. A substituição do rousseau — `if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }` — corrige isso.

### Prevenção de loop

`IsFromMe=true` também dispara para mensagens enviadas por *este* dispositivo linkado (respostas de saída do rousseau ecoando de volta). O transporte as descarta quando o ID do dispositivo corresponde:

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

Mensagens dos *outros* dispositivos linkados da conta (ex.: o telefone primário testando "envie mensagem para si mesmo") carregam `IsFromMe=true`, mas um ID de dispositivo diferente — essas são tratadas normalmente.

## Padrões regex de allowlist

A flag `--allow` recebe strings exatas, não regexes — o rousseau realiza uma checagem de igualdade case-insensitive em `router.go`. Se você quer correspondência por padrão, use o arquivo de configuração com modo `pattern` (o mesmo das políticas de aprovação):

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

Para grupos (`<hash>@g.us`), adicione-os da mesma forma. Para permitir todos de um determinado código de país, você precisaria de uma implementação customizada de `Router.Allow` — o enforcer embutido não faz prefix matching por design.

<aside class="admonition" data-type="warning"><span class="admonition-title">Allowlist vazia</span><p>Uma allowlist vazia aceita qualquer remetente. Não execute um transporte de chat sem allowlist em um número público — qualquer pessoa que saiba o número se torna um operador do seu agente.</p></aside>

## Cabeçalho de resposta

Cada mensagem de saída é prefixada com um cabeçalho para que o remetente saiba com qual bot está falando. O padrão:

```
💎 *Rousseau Agent*

<message body>
```

O WhatsApp renderiza `*text*` como negrito. Sobrescreva na configuração:

```yaml
whatsapp:
  reply_header: "🤖 *Coding bot*\n\n"
```

Defina como um único espaço `" "` para desabilitar o prefixo completamente.

## Transcrição de notas de voz

Notas de voz recebidas são transcritas via `whisper.cpp` quando o operador opta por isso. Desligado por padrão porque requer o CLI `whisper` instalado.

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| Campo | Efeito |
|---|---|
| `enabled` | Toggle. Quando desligado, mensagens de áudio são logadas e puladas. |
| `binary` | Executável do Whisper CLI. Vazio usa `whisper` como padrão. |
| `model` | Passado para `--model` (`base.en`, `small`, `medium`). |
| `model_path` | Caminho `.bin` explícito. Tem precedência sobre `model`. |
| `language` | Passado para `--language`. Vazio detecta automaticamente. |
| `extra_args` | Anexado a cada invocação. |

O texto transcrito é entregue ao agente como se o usuário o tivesse digitado.

## Implantação em contêiner

A unidade Quadlet Podman de referência (`docker/rousseau-agent.container`) monta o diretório de estado como leitura-gravação para que o pareamento sobreviva a restarts:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` dá ao contêiner uma stack somente-egresso rootless. O whatsmeow não precisa de capabilities elevadas; `DropCapability=all` é seguro.

## Fluxo de transcrição de notas de voz

Quando uma nota de voz chega, o resolver padrão retorna `SkipEmptyText` (sem conteúdo de texto). O `Dispatch` detecta isso especificamente para mensagens de áudio e — se um `Transcriber` estiver configurado — prossegue por este caminho:

```
Inbound audio message
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • Logs whatsapp.audio_downloaded on success
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • Returns plain-text transcription
  │     • Logs whatsapp.transcribed with duration
  │
  └── Re-enter handleTextMessage with the transcription as `Body`
```

Se nenhum transcritor estiver configurado, o daemon loga `whatsapp.audio_ignored reason=transcriber_not_configured` e descarta a mensagem. Notas de voz nunca disparam uma resposta de "silêncio" — uma entrada vazia produz uma saída vazia.

## Downloads de mídia

A interface `Downloader` é pequena de propósito:

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

Atualmente apenas o download de áudio está conectado. Downloads de imagem e vídeo estão no roadmap — chegam como `waProto.ImageMessage` / `VideoMessage` e precisariam de uma interface `DownloadableMedia` correspondente. Acompanhe [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) para o plano.

## Indicadores de digitação

O handler envolve cada resposta em chamadas `SendPresence(Composing, Paused)` para que o remetente veja o indicador "…está digitando" enquanto o modelo pensa. Ambas as chamadas têm timeout de 5 segundos e são best-effort — uma falha de presence nunca bloqueia a própria resposta.

## Modos de falha

| Sintoma | Correção |
|---|---|
| QR reimprime a cada restart | O pareamento foi revogado pelo telefone; delete `whatsapp.db` e refaça o pareamento. |
| Loop de reconexão do WhatsApp | Verifique desvio de relógio contra `pool.ntp.org` — o handshake do whatsmeow é sensível ao tempo. |
| Mensagens de entrada ignoradas | Verifique se o remetente está na lista `--allow`; verifique logs por `router.transport.rejected`. |
| A Meta bane o número | Não execute em um número pessoal. O protocolo é não oficial. |
| Self-chat "hello" não é roteado | Self-chat usa LID; o rousseau substitui pelo phone JID para casar com allowlist. Verifique se `ownID` está inicializado — o daemon loga `whatsapp.connected` quando está. |
| Notas de voz silenciosamente descartadas | Ou `whatsapp.voice.enabled: false` ou o binário `whisper` está ausente. Linha de log: `whatsapp.audio_ignored`. |
| Cada resposta volta para mim duas vezes | A prevenção de loop está desligada. Garanta que você está executando uma build recente; a correção chegou em `ResolveInbound` no início do rollout multi-device do whatsmeow. |

## Solução de problemas

### O QR é impresso, mas o app do telefone o rejeita

Três causas comuns: (1) um pareamento anterior parcialmente concluído deixou `whatsapp.db` em um estado que o whatsmeow não pode reutilizar — delete o arquivo e escaneie novamente; (2) o relógio está desviado por mais de 30 segundos (comum em contêineres sem NTP) — verifique com `timedatectl status`; (3) uma versão mais antiga do `whatsmeow` pode perder uma atualização de protocolo da Meta.

### `whatsapp.connected` depois `whatsapp.disconnected` em loop

Desvio de relógio, ou a Meta invalidou o pareamento. Verifique eventos `whatsapp.logged_out` no log — esse é o sinal definitivo.

### Notas de voz chegam mas nunca são transcritas

O binário do transcritor não é resolvível. Verifique `whatsapp.voice.binary` e `whatsapp.voice.model_path` — ambos devem apontar para arquivos reais (ou `binary` deve estar no `PATH`).

### Regex de allowlist não casa

A allowlist do rousseau é exact-string, não regex. Para casar com uma faixa de remetentes, liste cada um explicitamente ou adicione um router customizado.

### Cabeçalho de resposta aparece como caracteres `*` literais

O cliente do destinatário não renderiza Markdown do WhatsApp. Isso é uma questão de renderização no lado do cliente; use texto puro se seus destinatários estão em clientes mais antigos.

## Páginas relacionadas

- [Começando: Seu primeiro transporte](/pt-BR/getting-started/first-transport/) — passo a passo de ponta a ponta.
- [Guia do usuário: Modo voz](/pt-BR/user-guide/voice-mode/) — mergulho profundo em notas de voz.
- [Configuração](/pt-BR/configuration/) — o bloco de configuração `whatsapp`.
- [Transportes](/pt-BR/transports/) — os outros oito transportes.
- [Implantação](/pt-BR/deployment/) — executando WhatsApp em um contêiner Podman.

## Leitura complementar

- `internal/transport/whatsapp/client.go` — connect, pareamento QR, event pump.
- `internal/transport/whatsapp/resolve.go` — normalização LID/JID e tratamento de self-chat.
- `internal/transport/whatsapp/dispatch.go` — dispatch de mensagem de entrada com branching para nota de voz.
- `internal/transport/whatsapp/whisper.go` — transcritor whisper-cpp de referência.
- `internal/cli/whatsapp.go` — wiring do CLI, DSN do store, seleção de transcritor.
