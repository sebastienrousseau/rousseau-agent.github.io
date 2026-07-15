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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "Tutorial: implantar em um VPS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: implantar em um VPS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: implantar em um VPS"
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
twitter_description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: implantar em um VPS"
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

## O que você constrói

Um VPS Ubuntu 24.04 recém-provisionado rodando o daemon WhatsApp do rousseau-agent sob um contêiner Podman rootless, dirigido pela unidade Quadlet do systemd em `docker/rousseau-agent.container`. Filesystem raiz somente leitura, todas as capabilities descartadas, `NoNewPrivileges=true`, seccomp ligado. Zero portas de rede de entrada.

Tempo estimado: 45 minutos.

## Pré-requisitos

- Um VPS com Ubuntu 24.04 (ou Debian 12+ / Fedora 40+). 1 GB de RAM, 20 GB de disco é suficiente.
- Acesso SSH por chave a um usuário não-root com sudo.
- Sua chave de API da Anthropic ou disposição para rodar `claudecli` — o `claudecli` precisa do `claude` instalado no VPS com uma sessão OAuth ativa, o que é inconveniente em um servidor headless. Anthropic direct ou Bedrock é a escolha prática.

## Passo 1: setup do SO base

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# rootless podman needs subuid/subgid ranges for the user
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

Crie o usuário de serviço e sua sessão systemd de usuário:

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # keeps user services running when nobody is logged in
```

## Passo 2: transferir o código-fonte

A unidade Quadlet em `docker/rousseau-agent.container` compila uma imagem local. No VPS:

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

O `Dockerfile` produz um binário Go estático (`CGO_ENABLED=0`), copia-o para uma base mínima e roda como UID 1000. Veja [Implantação](/pt-BR/deployment/) para a discussão sobre a imagem base.

## Passo 3: semear a configuração

O rousseau lê `~/.config/rousseau/config.yaml`. Crie-o no host — a unidade Quadlet faz bind-mount do `$HOME` do contêiner de volta ao host.

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/config.yaml <<'YAML'
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

whatsapp:
  reply_header: "*rousseau*\n\n"

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

log:
  level: info
  format: json
YAML
chown -R rousseau:rousseau /home/rousseau/.config
```

Guarde a chave da API da Anthropic em um arquivo de ambiente do systemd — nunca no `config.yaml`:

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

Referencie-o a partir da unidade Quadlet — veja o próximo passo.

## Passo 4: instalar a unidade Quadlet

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

Edite para o seu JID e arquivo de segredos:

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

Recarregue e inicie:

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## Passo 5: primeiro pareamento

O bridge do WhatsApp precisa imprimir um QR code na primeira vez. Anexe:

```sh
podman logs -f rousseau-agent
# scan the QR from your phone: WhatsApp > Settings > Linked devices
```

Sequência de log esperada (de `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

As credenciais do dispositivo persistem em `/home/rousseau/.local/share/rousseau/whatsapp.db`. Reinícios subsequentes pulam o QR.

## Passo 6: verificar

```sh
podman exec rousseau-agent rousseau status
```

Código de saída 0 significa que o daemon está saudável. Qualquer não-zero é um alerta vermelho — veja [Referência: Códigos de saída](/pt-BR/reference/exit-codes/).

Envie a si mesmo uma mensagem de teste do telefone na allowlist. Os logs estruturados mostram:

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## Passo 7: revisão de endurecimento

A unidade Quadlet já aplica:

- `ReadOnly=true` + `Tmpfs=/tmp` — sem mutação de imagem em runtime.
- `DropCapability=all` — o binário Go não precisa de caps elevadas.
- `NoNewPrivileges=true` — processos filhos não podem ganhar privilégios.
- `SeccompProfile=/usr/share/containers/seccomp.json` — filtro de syscalls no kernel.
- `Network=pasta` — stack de rede rootless, bloqueia inbound por padrão.
- `UserNS=keep-id` — arquivos bind-mounted com dono como esperado em ambos os lados.

Se você quer a postura mais estrita, envolva o daemon em um firewall apenas outbound (nftables ou Cloudflare Zero-Trust) que só permite os ranges de CDN que Anthropic + Meta realmente resolvem. Veja [Guias: Onboarding empresarial](/pt-BR/guides/enterprise-onboarding/) para o checklist.

## Passo 8: backup

Todo o estado persistente é um único diretório: `/home/rousseau/.local/share/rousseau/`. Faça `restic` ou `borg` dele todas as noites.

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

Os bancos SQLite podem ser snapshotados ao vivo com segurança porque o journaling WAL é habilitado por `Open()` em `internal/state/sqlite/store.go`.

## Relacionados

- [Implantação](/pt-BR/deployment/) — referência completa da unidade Quadlet.
- [Guias: Implantação em produção](/pt-BR/guides/production-deployment/) — envio de logs, restarts em rolling.
- [Guias: Onboarding empresarial](/pt-BR/guides/enterprise-onboarding/) — verificação de SBOM, auditoria seccomp.
- [Segurança](/pt-BR/security/) — limites de confiança.
