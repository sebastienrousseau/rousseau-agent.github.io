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
description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "Transporte de e-mail"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte de e-mail"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte de e-mail"
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
twitter_description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte de e-mail"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>O passo a passo de app-password do Gmail, como configurar o transporte para Fastmail / Google Workspace / um servidor de e-mail auto-hospedado, o caminho de migração a partir de servidores só-STARTTLS e o trade-off de renderização plain-vs-HTML. Leia <code>internal/transport/email/client.go</code> junto a esta página.</p></aside>

## Visão geral

O transporte de email (`internal/transport/email/`) é um par: **IMAP de entrada** (via `github.com/emersion/go-imap/v2`) e **SMTP de saída** (via `net/smtp` da biblioteca padrão do Go).

Ele faz polling na INBOX por mensagens `UNSEEN`, marca-as como `SEEN` após handoff para o handler e responde via `net/smtp.SendMail`.

## Postura TLS

**Ambas as pontas usam TLS completo.** O transporte usa `imapclient.DialTLS` no lado IMAP e `smtp.SendMail` com `PlainAuth` sobre uma conexão já envelopada em TLS no lado SMTP. Servidores IMAP ou SMTP só-STARTTLS **não são suportados atualmente** — o daemon recusa enviar credenciais em texto simples sobre um socket sem criptografia.

Portas TLS padrão:

- IMAP: `993`
- Submissão SMTP: `465` (TLS implícito) — TLS completo. **Não `587` a menos que seu provider também faça TLS implícito em 587.**

Alguns providers (Google Workspace, Fastmail) aceitam submissão SMTP em `465` com TLS implícito. Verifique seu provider antes de configurar.

## Configuração

```yaml
email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  mailbox: "INBOX"
  poll_interval: "30s"

  smtp_addr: "smtp.example.com:465"
  smtp_username: "bot@example.com"
  smtp_password: "..."

  from: "bot@example.com"
  reply_header: ""
```

| Campo | Padrão | Efeito |
|---|---|---|
| `imap_addr` | *obrigatório* | `host:port` para IMAP TLS. |
| `imap_username` | *obrigatório* | Usuário IMAP. |
| `imap_password` | *obrigatório* | Senha IMAP. |
| `mailbox` | `INBOX` | Caixa de correio para polling. |
| `poll_interval` | `30s` | Frequência de busca por e-mails UNSEEN. |
| `smtp_addr` | *obrigatório* | `host:port` para submissão SMTP. |
| `smtp_username` | *obrigatório* | Usuário SMTP. |
| `smtp_password` | *obrigatório* | Senha SMTP. |
| `from` | *obrigatório* | Endereço `From` do envelope + cabeçalho. |
| `reply_header` | *vazio* | Anteposto ao corpo de cada mensagem de saída. |

## Linha de comando

```sh
rousseau email \
  --imap-addr imap.example.com:993 \
  --imap-username bot@example.com \
  --imap-password ... \
  --smtp-addr smtp.example.com:465 \
  --smtp-username bot@example.com \
  --smtp-password ... \
  --from bot@example.com
```

## Formato da mensagem de saída

Respostas estão em conformidade com RFC 5322. O rousseau escreve:

```
From: bot@example.com
To: sender@example.com
Subject: Re: <inbound subject>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 é incondicional. Saída HTML está fora do escopo; não há template engine conectado.

## Formato da mensagem de entrada

Mensagens `UNSEEN` são parseadas em uma `IncomingMessage` com:

- `From` = o endereço do cabeçalho `From` parseado.
- `Body` = as partes `text/plain` concatenadas.
- `At` = o `INTERNALDATE` do IMAP.

Anexos, `text/html` e imagens inline são ignorados.

## Escolha da caixa de correio

`mailbox: "INBOX"` é o padrão. Aponte para uma label do Gmail (`"[Gmail]/label"`) ou uma pasta do Fastmail para filtragem mais fina — qualquer coisa que o servidor IMAP exponha funciona.

## Configuração específica por provider

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">Auto-hospedado</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Passo a passo de app password do Gmail.** Senhas normais do Gmail não autenticarão via IMAP/SMTP quando 2FA está ativado. Gere uma app password:

1. Visite https://myaccount.google.com/security. Confirme que **Verificação em duas etapas** está ativa.
2. Clique em **Senhas de app** (visível somente com 2FA habilitado).
3. Nomeie o app como "rousseau-agent", gere. Copie a senha de 16 caracteres (espaços opcionais).

Configuração:

```yaml
email:
  imap_addr: imap.gmail.com:993
  imap_username: your.address@gmail.com
  imap_password: "aaaa bbbb cccc dddd"

  smtp_addr: smtp.gmail.com:465
  smtp_username: your.address@gmail.com
  smtp_password: "aaaa bbbb cccc dddd"

  from: your.address@gmail.com
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Bloqueio administrativo do Google Workspace</span><p>Alguns admins do Workspace desabilitam app passwords no nível da organização. Se <em>App passwords</em> está ausente da sua página de segurança, peça ao seu admin para permitir "Less secure app access" ou configurar OAuth — o rousseau ainda não suporta OAuth do Gmail (roadmap).</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O Fastmail suporta app passwords em *Settings &gt; Password &amp; Security &gt; App passwords*. Crie uma senha escopada para *Mail (IMAP/POP/SMTP)*:

```yaml
email:
  imap_addr: imap.fastmail.com:993
  imap_username: your.address@fastmail.com
  imap_password: "..."

  smtp_addr: smtp.fastmail.com:465
  smtp_username: your.address@fastmail.com
  smtp_password: "..."

  from: your.address@fastmail.com
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O Microsoft 365 depreciou a autenticação básica (username + senha) para a maioria dos tenants. O rousseau ainda não suporta Modern Auth / OAuth (roadmap). Opções:

1. Habilite *Authenticated SMTP* por caixa de correio no centro de admin do M365 (possível em alguns tenants).
2. Use um relay: execute o rousseau contra um IMAP+SMTP auto-hospedado que encaminha através do M365 via SMTP com uma app password.
3. Espere o suporte a OAuth chegar.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Qualquer servidor de e-mail auto-hospedado que fale IMAP sobre TLS em 993 e submissão SMTP sobre TLS implícito em 465 funciona out of the box. Postfix + Dovecot com `smtpd_tls_wrappermode=yes` na porta 465 é uma configuração clássica.

```yaml
email:
  imap_addr: mail.internal:993
  imap_username: rousseau
  imap_password: "..."

  smtp_addr: mail.internal:465
  smtp_username: rousseau
  smtp_password: "..."

  from: rousseau@internal
```

Se seu servidor é só-STARTTLS (submissão SMTP na porta 587), o rousseau recusará a autenticar — o transporte não envia credenciais em texto simples. Veja a seção de migração abaixo.

  </div>
</div>

## Migrando de servidores só-STARTTLS

O rousseau usa TLS implícito em ambos IMAP (993) e SMTP (465). Se sua infraestrutura de e-mail existente oferece apenas STARTTLS em 143 (IMAP) ou 587 (submissão SMTP), você tem três opções:

1. **Habilite TLS implícito no seu servidor.** O Postfix suporta `smtpd_tls_wrappermode=yes` vinculado à porta 465. O Dovecot suporta o serviço `imaps` na porta 993 out of the box.
2. **Coloque um proxy que termina TLS na frente do servidor.** O `stunnel` pode aceitar TLS implícito em 465 e encaminhar como STARTTLS em 587.
3. **Espere o suporte a STARTTLS.** Item do roadmap; veja `docs/GAP_ANALYSIS_2026.md`.

## Renderização plain vs HTML

A saída é `text/plain; charset=utf-8`. Sem template HTML. Isso é deliberado — texto puro é universalmente renderizado, não embute pixels de rastreamento e nunca quebra em um cliente de e-mail somente-texto. Se você quer saída HTML, envelope o transporte e reescreva `SendMail`:

```go
// Custom transport that emits multipart/alternative.
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... construct multipart/alternative message, call net/smtp.SendMail ...
}
```

O core do rousseau permanece plain-text; HTML é uma preocupação do caller.

## Modos de falha

| Sintoma | Correção |
|---|---|
| Erros de `imapclient.DialTLS` | Confirme que a porta 993 está aberta para saída, o certificado TLS é válido. |
| `SMTP AUTH failed` | `PlainAuth` requer que o hostname do servidor de autenticação corresponda a `smtp_addr`. Providers com load balancers podem apresentar um nome diferente. |
| Mensagens nunca marcadas como SEEN | O handler retornou um erro. Corrija o problema subjacente; o rousseau não retenta indefinidamente. |
| Respostas duplicadas | Duas instâncias do rousseau na mesma caixa de correio; apenas uma deve rodar. |
| `AUTHENTICATE failed: Application-specific password required` | Gmail com 2FA ativado, e a senha da conta foi usada em vez de uma app password. Veja o passo a passo do Gmail acima. |

## Solução de problemas

### `dial tcp: connect: connection refused`

Porta errada. Garanta que `imap_addr` usa `:993` (não `:143`) e `smtp_addr` usa `:465` (não `:587` para servidores só-STARTTLS).

### O bot responde ao spam

Qualquer mensagem no INBOX com `UNSEEN` é tratada. Filtre spam no nível da caixa de correio (regras server-side, filtro de spam do Gmail) ou configure um `mailbox:` diferente de INBOX e roteie e-mails para ele com uma regra server-side.

### `SendMail` tem sucesso mas a mensagem nunca chega

Verifique o log de e-mail do servidor SMTP. Causas comuns: falha na assinatura DKIM (o domínio `From:` não corresponde a um domínio que seu servidor pode assinar), incompatibilidade de DNS reverso, o SPF do domínio receptor bloqueia seu IP.

### Unicode no corpo da mensagem renderiza como `?????`

Algo ao longo do caminho removeu UTF-8. Verifique que `Content-Type: text/plain; charset=utf-8` está na mensagem enviada (o rousseau sempre o define) e que nenhum relay está transcodificando.

### O polling leva segundos mesmo após mudança de configuração

`poll_interval` só é relido no início do daemon. Reinicie para pegar o novo valor.

## Páginas relacionadas

- [Começando: Seu primeiro transporte](/pt-BR/getting-started/first-transport/) — passo a passo de ponta a ponta.
- [Configuração](/pt-BR/configuration/) — o bloco de configuração `email`.
- [Transportes](/pt-BR/transports/) — transportes irmãos.
- [Implantação](/pt-BR/deployment/) — executando Email em um contêiner Podman.
- [Cron](/pt-BR/cron/) — envie digests agendados por email.

## Leitura complementar

- `internal/transport/email/client.go` — polling IMAP, envio SMTP, parsing de mensagens.
- `internal/cli/email.go` — wiring do CLI.
- `internal/config/config.go` — struct `EmailConfig`.
- [Docs do emersion/go-imap](https://github.com/emersion/go-imap) — a biblioteca IMAP.
