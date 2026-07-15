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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "Seu primeiro transporte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Seu primeiro transporte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Seu primeiro transporte"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Seu primeiro transporte"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Como parear um transporte de chat com o daemon rousseau, colocar em allowlist o JID/user ID que o aciona, enviar uma primeira mensagem de teste e confirmar a resposta. O WhatsApp é o passo a passo canônico porque o pareamento é o mais rigoroso; as abas abaixo mostram os passos a passo paralelos para Slack e Discord.</p></aside>

## Escolha seu primeiro transporte

Cada transporte é um adaptador fino atrás da mesma interface `transport.Transport` — allowlisting, roteamento de sessão e entrega de cron são idênticos em todos eles. As diferenças são a UX de pareamento e o formato de identificador por transporte (JID, user ID, room ID). Escolha o que você conseguir parear mais rápido:

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

O WhatsApp é a referência — o mais difícil de parear, o mais fácil de testar (você já tem o app no seu telefone).

**Pré-requisitos:** seu telefone com WhatsApp, seu JID E.164 (ex.: `447900123456@s.whatsapp.net`).

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Escaneie o QR em **WhatsApp &gt; Configurações &gt; Dispositivos conectados &gt; Conectar um dispositivo**. Envie `hello` para si mesmo; o rousseau responde via WhatsApp. Veja abaixo o passo a passo completo.

<aside class="admonition" data-type="warning"><span class="admonition-title">Protocolo não oficial</span><p>O suporte a WhatsApp usa <code>whatsmeow</code> — um cliente reverso. A Meta ocasionalmente bane números que executam clientes não oficiais. Não execute isso em um número no qual você depende.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Pré-requisitos:** admin em um workspace Slack, um app criado em [api.slack.com/apps](https://api.slack.com/apps), Socket Mode habilitado.

1. Crie um app Slack, habilite **Socket Mode** em <em>Settings &gt; Socket Mode</em>.
2. Crie um **App-Level Token** com `connections:write` — este é o token `xapp-…`.
3. Em <em>OAuth &amp; Permissions</em>, adicione os escopos de bot `chat:write`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read`. Instale no workspace para obter o token de bot `xoxb-…`.
4. Em <em>Event Subscriptions</em>, inscreva-se em `message.im` (DMs) e em qualquer evento de canal que desejar.

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

Envie DM para o bot no Slack; o rousseau responde na mesma DM. Veja [Transportes: Slack](/pt-BR/transports/slack/) para o passo a passo completo com justificativa dos escopos OAuth.

<aside class="admonition" data-type="tip"><span class="admonition-title">Sem HTTP público</span><p>Socket Mode significa que o daemon se conecta de forma saída ao WebSocket do Slack. Você não precisa de um webhook público, ngrok ou ingress.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Pré-requisitos:** um aplicativo Discord em [discord.com/developers/applications](https://discord.com/developers/applications), um usuário bot, a **Message Content Intent** habilitada em <em>Bot</em>.

1. Crie um aplicativo, adicione um bot, copie o token do bot.
2. Em <em>Bot &gt; Privileged Gateway Intents</em>, habilite **Message Content Intent**. Sem isso, o texto da mensagem chega vazio.
3. Convide o bot via <em>OAuth2 &gt; URL Generator</em> — escopo `bot`, permissões `Send Messages`, `Read Message History`.

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

Envie DM para o bot; o rousseau responde. Veja [Transportes: Discord](/pt-BR/transports/discord/) para mergulho profundo em permissões e intents.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Pré-requisitos:** um bot Telegram do [@BotFather](https://t.me/BotFather).

1. Envie mensagem para `@BotFather`, `/newbot`, siga os prompts. Copie o token.
2. Fale com seu bot pelo menos uma vez para que o Telegram crie um chat.

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

O valor de `--allow` é o ID numérico de usuário do Telegram (não o username). Obtenha enviando mensagem para [@userinfobot](https://t.me/userinfobot).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Pré-requisitos:** `signal-cli` instalado e vinculado a uma conta Signal. Veja a [documentação do signal-cli](https://github.com/AsamK/signal-cli) para o fluxo de pareamento.

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

O rousseau gera `signal-cli` como um subprocesso (veja `internal/cli/signal.go`) e se comunica com ele via JSON-RPC. Veja [Transportes: Signal](/pt-BR/transports/signal/).

  </div>
</div>

## Por que o passo a passo do WhatsApp

O restante desta página usa o WhatsApp como o exemplo canônico — se você entender o padrão aqui, cada outro transporte é uma variação (colocar em allowlist um ID estável, executar uma UX de pareamento uma vez, enviar um teste, verificar a resposta). Pule para a página do transporte irmão se já tiver um token em mãos:

- [Slack](/pt-BR/transports/slack/) — tokens Socket Mode e event subscriptions.
- [Discord](/pt-BR/transports/discord/) — token do bot, intents, inteiros de permissão.
- [Telegram](/pt-BR/transports/telegram/) — token do BotFather.
- [Signal](/pt-BR/transports/signal/) — subprocesso signal-cli.
- [Matrix](/pt-BR/transports/matrix/) — URL do homeserver + access token.

## Pré-requisitos

- `rousseau` no `$PATH` (veja [Instalação](/pt-BR/getting-started/installation/)).
- Um provider funcional — o `claudecli` herdando a autenticação do Claude Code é o padrão; qualquer outro precisa ter sua configuração preenchida primeiro ([Configuração](/pt-BR/configuration/)).
- Seu telefone com WhatsApp instalado. Seu JID de telefone E.164 (ex.: `447900123456@s.whatsapp.net`).

## Passo 1 — Escolha o JID que acionará o daemon

O rousseau usa uma allowlist para restringir o handling de entrada a um conjunto fixo de JIDs. Cada outro remetente é silenciosamente descartado. Isso é crítico: sem uma allowlist, qualquer pessoa que saiba o número poderia acionar o agente.

Seu JID E.164 é seu número de telefone, apenas dígitos, seguido de `@s.whatsapp.net`:

```
447900123456@s.whatsapp.net
```

JIDs de grupo terminam em `@g.us`; o daemon também os suporta, mas comece com um JID pessoal.

## Passo 2 — Primeiro lançamento e pareamento

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

No primeiro lançamento, um código QR é impresso no stdout. Abra o WhatsApp no seu telefone, vá para **Configurações → Dispositivos conectados → Conectar um dispositivo** e escaneie o QR.

O daemon imprime algo como:

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

Depois que você escaneia, o whatsmeow persiste as credenciais do dispositivo em `whatsapp.db`. Lançamentos subsequentes conectam silenciosamente — sem mais QR.

## Passo 3 — Envie uma mensagem de teste

Do seu telefone, envie `hello` para si mesmo. O daemon loga o evento de entrada, faz dispatch ao agente e entrega a resposta de volta pelo WhatsApp com o header configurado:

```
💎 *Rousseau Agent*

Hello — what would you like to work on?
```

O header de resposta é configurável via `whatsapp.reply_header`. Defina-o como um único espaço para desabilitar o prefixo.

## Passo 4 — Configure um `config.yaml` para não precisar de flags longas

Crie `~/.config/rousseau/config.yaml`:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

Agora `rousseau whatsapp --allow 447900123456@s.whatsapp.net` pega o header automaticamente. Cada transporte lê seu bloco do mesmo arquivo — veja [Configuração](/pt-BR/configuration/) para a lista completa.

`bypassPermissions` é o padrão para daemons não-atendidos porque não há humano do outro lado do terminal para aprovar chamadas de tool interativamente. **Configure uma política de aprovação** ([Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/)) antes de apontar o daemon para qualquer coisa que você se importe.

## Passo 5 — Confirme ponta a ponta

Envie uma pergunta de codificação do seu telefone:

```
Read the file at /workspace/README.md and summarise it in 3 bullets.
```

O daemon executa uma chamada de tool `read`, alimenta o arquivo para o modelo e envia mensagem de volta com o resumo. Você acabou de fechar o loop:

- Telefone → WhatsApp → WebSocket do whatsmeow
- rousseau-agent → loop do agente → chamada de tool → chamada ao provider
- resposta → whatsmeow → WhatsApp → telefone

Nada cruzou o perímetro da sua rede exceto a chamada ao provider — e se o provider era `claudecli` na sua instalação local do Claude Code, nem isso.

## Verificando com `rousseau doctor`

```sh
rousseau doctor
```

Cada checagem para o caminho do WhatsApp é coberta:

- `provider.claudecli.binary`, `provider.claudecli.version` — o caminho LLM.
- `state.path`, `state.db_size`, `state.sessions` — armazenamento de sessão SQLite.
- `whatsapp.store`, `whatsapp.paired` — credenciais de dispositivo.
- `whatsapp.voice` — postura de transcrição de notas de voz.

Uma linha `fail` é um hard stop; uma linha `warn` vale investigar antes de subir para produção.

## Solução de problemas

### O código QR é impresso mas o telefone o rejeita

Três causas comuns. Primeiro, um pareamento anterior parcialmente concluído deixou `whatsapp.db` em um estado que o whatsmeow não pode reutilizar — delete `~/.local/share/rousseau/whatsapp.db` e escaneie novamente. Segundo, o relógio está desviado em mais de 30 segundos (comum em contêineres sem um cliente NTP funcional) — o handshake do WhatsApp é sensível ao tempo. Terceiro, uma versão mais antiga do `whatsmeow` pode perder uma atualização de protocolo da Meta; atualize o rousseau.

### Enviei uma mensagem, mas o daemon loga `router.transport.rejected`

Seu JID não corresponde à allowlist. O valor passado para `--allow` deve ser o JID do remetente exatamente como o WhatsApp o reporta (`447900123456@s.whatsapp.net`, sem `+`, sem espaços). Note que testar consigo mesmo funciona porque o rousseau substitui o próprio JID da conta pelo hash de privacidade LID (veja `internal/transport/whatsapp/resolve.go`).

### Nenhum código QR é impresso e o daemon sai com `no rows`

O store do whatsmeow nunca foi inicializado. Garanta que o diretório pai (`~/.local/share/rousseau/`) existe e é gravável. `rousseau doctor` reporta isso em `whatsapp.store`.

### O rousseau responde, mas a saída do modelo está vazia

Verifique `provider.claudecli.binary` e `provider.claudecli.version` no `rousseau doctor`. A causa mais comum de resposta vazia é uma invocação `claudecli` retornando `is_error: true` — o daemon loga o erro truncado no nível `warn`. Troque o provider para `anthropic` ou `bedrock` para isolar o subprocesso.

### Slack/Discord: "invalid_auth" ou "401 Unauthorized"

Para Slack, `xapp-…` (app token) e `xoxb-…` (bot token) são diferentes — misturá-los produz `invalid_auth`. Para Discord, o token exibido em <em>Bot &gt; Reset Token</em> é one-shot; se você o copiou uma vez e perdeu, deve resetar novamente.

## Páginas relacionadas

- [Transportes](/pt-BR/transports/) — cada transporte, seu protocolo de wire e seu formato de allowlist.
- [Guia do usuário: CLI](/pt-BR/user-guide/cli/) — cada comando e flag.
- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — a alavanca de segurança primária.
- [Implantação](/pt-BR/deployment/) — passe do `rousseau whatsapp` em primeiro plano para uma unidade systemd.
- [Modo voz](/pt-BR/user-guide/voice-mode/) — transforme notas de voz do WhatsApp em turnos do agente.

## Leitura complementar

- `internal/transport/whatsapp/client.go` — connect, QR, event pump.
- `internal/transport/whatsapp/resolve.go` — normalização LID/JID e tratamento de self-chat.
- `internal/cli/whatsapp.go` — wiring do CLI, DSN do store, seleção de transcritor.
- `internal/cli/slack.go`, `internal/cli/discord.go` — CLIs de transportes irmãos.
- `internal/transport/router.go` — imposição da allowlist.
