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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "Transporte de correo"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte de correo"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte de correo"
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
twitter_title: "Transporte de correo"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>El recorrido de contraseña de aplicación de Gmail, cómo configurar el transporte para Fastmail / Google Workspace / un servidor de correo autoalojado, la ruta de migración desde servidores solo STARTTLS y la contrapartida entre renderizado plano y HTML. Lee <code>internal/transport/email/client.go</code> junto a esta página.</p></aside>

## Descripción general

El transporte de correo (`internal/transport/email/`) es un par: **IMAP entrante** (vía `github.com/emersion/go-imap/v2`) y **SMTP saliente** (vía `net/smtp` de la biblioteca estándar de Go).

Sondea INBOX buscando mensajes `UNSEEN`, los marca como `SEEN` tras entregarlos al handler, y responde vía `net/smtp.SendMail`.

## Postura TLS

**Ambos extremos son TLS completo.** El transporte usa `imapclient.DialTLS` del lado IMAP y `smtp.SendMail` con `PlainAuth` sobre una conexión ya envuelta en TLS del lado SMTP. Los servidores IMAP o SMTP solo con STARTTLS **no están soportados actualmente** — el servicio se niega a enviar credenciales en texto plano sobre un socket sin cifrar.

Puertos TLS estándar:

- IMAP: `993`
- Envío SMTP: `465` (TLS implícito) — TLS completo. **No `587` a menos que tu proveedor también haga TLS implícito en 587.**

Algunos proveedores (Google Workspace, Fastmail) aceptan envío SMTP en `465` con TLS implícito. Verifica tu proveedor antes de configurar.

## Configuración

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

| Campo | Por defecto | Efecto |
|---|---|---|
| `imap_addr` | *requerido* | `host:port` para IMAP con TLS. |
| `imap_username` | *requerido* | Nombre de usuario IMAP. |
| `imap_password` | *requerido* | Contraseña IMAP. |
| `mailbox` | `INBOX` | Buzón a sondear. |
| `poll_interval` | `30s` | Con qué frecuencia buscar correo UNSEEN. |
| `smtp_addr` | *requerido* | `host:port` para envío SMTP. |
| `smtp_username` | *requerido* | Nombre de usuario SMTP. |
| `smtp_password` | *requerido* | Contraseña SMTP. |
| `from` | *requerido* | Dirección `From` del envelope y del encabezado. |
| `reply_header` | *vacío* | Antepuesto al cuerpo de cada mensaje saliente. |

## Línea de comandos

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

## Forma del mensaje saliente

Las respuestas cumplen con RFC 5322. rousseau escribe:

```
From: bot@example.com
To: sender@example.com
Subject: Re: <inbound subject>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 es incondicional. La salida HTML está fuera del alcance; no hay motor de plantillas cableado.

## Forma del mensaje entrante

Los mensajes `UNSEEN` se parsean en un `IncomingMessage` con:

- `From` = la dirección del header `From` parseada.
- `Body` = las partes `text/plain` concatenadas.
- `At` = el `INTERNALDATE` de IMAP.

Los adjuntos, `text/html` y las imágenes inline se ignoran.

## Elección del buzón

`mailbox: "INBOX"` es el valor por defecto. Apunta a una etiqueta de Gmail (`"[Gmail]/etiqueta"`) o a una carpeta de Fastmail para un filtrado más fino — cualquier cosa que el servidor IMAP exponga funciona.

## Configuración específica por proveedor

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">Autoalojado</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Recorrido de contraseña de aplicación de Gmail.** Las contraseñas regulares de Gmail no autenticarán sobre IMAP/SMTP cuando 2FA está activado. Genera una contraseña de aplicación:

1. Visita https://myaccount.google.com/security. Confirma que **Verificación en dos pasos** esté activada.
2. Haz clic en **Contraseñas de aplicaciones** (solo visible con 2FA habilitado).
3. Nombra la app "rousseau-agent", genera. Copia la contraseña de 16 caracteres (los espacios son opcionales).

Configuración:

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

<aside class="admonition" data-type="warning"><span class="admonition-title">Bloqueo de administrador de Google Workspace</span><p>Algunos administradores de Workspace deshabilitan las contraseñas de aplicaciones a nivel de organización. Si <em>Contraseñas de aplicaciones</em> no aparece en tu página de seguridad, pide al administrador que permita "Acceso a apps menos seguras" o configure OAuth — rousseau aún no admite OAuth de Gmail (hoja de ruta).</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Fastmail admite contraseñas de aplicaciones en *Settings &gt; Password &amp; Security &gt; App passwords*. Crea una contraseña con alcance *Mail (IMAP/POP/SMTP)*:

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

Microsoft 365 ha deprecado la autenticación básica (usuario + contraseña) para la mayoría de tenants. Rousseau aún no admite Modern Auth / OAuth (hoja de ruta). Opciones:

1. Habilitar *SMTP autenticado* por buzón en el centro de administración de M365 (posible en algunos tenants).
2. Usar un relay: ejecuta rousseau contra un IMAP+SMTP autoalojado que reenvíe a través de M365 vía SMTP con una contraseña de aplicación.
3. Espera a que aterrice el soporte de OAuth.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Cualquier servidor de correo autoalojado que hable IMAP sobre TLS en 993 y envío SMTP sobre TLS implícito en 465 funciona sin configuración. Postfix + Dovecot con `smtpd_tls_wrappermode=yes` en el puerto 465 es una configuración clásica.

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

Si tu servidor es solo STARTTLS (envío SMTP puerto 587), rousseau se negará a autenticar — el transporte no envía credenciales en texto plano. Consulta la sección de migración a continuación.

  </div>
</div>

## Migrar desde servidores solo STARTTLS

Rousseau usa TLS implícito tanto en IMAP (993) como en SMTP (465). Si tu infraestructura de correo existente solo ofrece STARTTLS en 143 (IMAP) o 587 (envío SMTP), tienes tres opciones:

1. **Habilita TLS implícito en tu servidor.** Postfix admite `smtpd_tls_wrappermode=yes` enlazado al puerto 465. Dovecot admite el servicio `imaps` en el puerto 993 sin configuración.
2. **Frontea el servidor con un proxy que termine TLS.** `stunnel` puede aceptar TLS implícito en 465 y reenviar como STARTTLS en 587.
3. **Espera al soporte de STARTTLS.** Elemento de hoja de ruta; consulta `docs/GAP_ANALYSIS_2026.md`.

## Renderizado plano vs HTML

La salida es `text/plain; charset=utf-8`. Sin plantilla HTML. Esto es deliberado — el texto plano se renderiza universalmente, no incrusta píxeles de seguimiento y nunca se rompe en un cliente de correo solo de texto. Si quieres salida HTML, envuelve el transporte y reescribe `SendMail`:

```go
// Transporte personalizado que emite multipart/alternative.
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... construir mensaje multipart/alternative, llamar a net/smtp.SendMail ...
}
```

El núcleo de rousseau se mantiene en texto plano; el HTML es una preocupación del llamador.

## Modos de fallo

| Síntoma | Corrección |
|---|---|
| Errores en `imapclient.DialTLS` | Confirma que el puerto 993 está abierto en saliente, el certificado TLS es válido. |
| `SMTP AUTH failed` | `PlainAuth` requiere que el hostname del servidor de auth coincida con `smtp_addr`. Los proveedores con balanceadores de carga pueden presentar un nombre distinto. |
| Los mensajes nunca se marcan como SEEN | El handler devolvió un error. Arregla el problema subyacente; rousseau no reintenta indefinidamente. |
| Respuestas duplicadas | Dos instancias de rousseau en el mismo buzón; solo una debería ejecutarse. |
| `AUTHENTICATE failed: Application-specific password required` | Gmail con 2FA activado, y se usó la contraseña de cuenta en lugar de una contraseña de aplicación. Consulta el recorrido de Gmail más arriba. |

## Solución de problemas

### `dial tcp: connect: connection refused`

Puerto incorrecto. Asegúrate de que `imap_addr` use `:993` (no `:143`) y `smtp_addr` use `:465` (no `:587` para servidores solo STARTTLS).

### El bot responde a spam

Cualquier mensaje en INBOX con `UNSEEN` se procesa. Filtra spam a nivel de buzón (reglas del lado del servidor, filtro de spam de Gmail) o configura un `mailbox:` distinto de INBOX y enruta el correo a él con una regla del lado del servidor.

### `SendMail` tiene éxito pero el mensaje nunca llega

Revisa el log de correo del servidor SMTP. Causas comunes: fallo de firma DKIM (el dominio `From:` no coincide con un dominio que tu servidor puede firmar), discrepancia de DNS reverso, el SPF del dominio receptor bloquea tu IP.

### El Unicode en el cuerpo del mensaje se renderiza como `?????`

Algo en el camino eliminó UTF-8. Verifica que `Content-Type: text/plain; charset=utf-8` esté en el mensaje enviado (rousseau siempre lo establece) y que ningún relay esté transcodificando.

### El sondeo tarda segundos incluso tras cambiar la configuración

`poll_interval` solo se relee al arrancar el servicio. Reinicia para tomar el nuevo valor.

## Páginas relacionadas

- [Primeros pasos: Tu primer transporte](/es/getting-started/first-transport/) — recorrido de principio a fin.
- [Configuración](/es/configuration/) — el bloque de configuración `email`.
- [Transportes](/es/transports/) — transportes hermanos.
- [Despliegue](/es/deployment/) — ejecutar Email en un contenedor Podman.
- [Cron](/es/cron/) — envía resúmenes programados vía correo.

## Lectura adicional

- `internal/transport/email/client.go` — sondeo IMAP, envío SMTP, parseo de mensajes.
- `internal/cli/email.go` — cableado de CLI.
- `internal/config/config.go` — struct `EmailConfig`.
- [Documentación de emersion/go-imap](https://github.com/emersion/go-imap) — la biblioteca IMAP.
