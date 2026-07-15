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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/deployment/"
subtitle: "Podman rootless com Quadlet do systemd, mais uma nota sobre Kubernetes."
tags: "deployment, operations, container, systemd"
title: "Implantação"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Implantação"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Implantação"
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
twitter_description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Implantação"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>As três topologias de implantação suportadas pelo rousseau — Podman rootless + Quadlet (referência), Docker puro e Kubernetes — além de gerenciamento de segredos via Vault, AWS Secrets Manager e GCP Secret Manager. Fonte da verdade para o Quadlet de referência: <code>docker/rousseau-agent.container</code>.</p></aside>

## Postura de referência

A implantação de referência é um contêiner Podman rootless gerenciado por uma unidade Quadlet do systemd — um nó, sem dependência de Kubernetes, sobrevive a reboots, não requer privilégios de root.

Fonte da verdade: `docker/rousseau-agent.container` no repositório rousseau-agent.

## Escolha uma topologia

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

A implantação de referência. Rootless, endurecida, sobrevive a reboots, sem necessidade de orquestrador.

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

Veja a unidade Quadlet completa e sua justificativa mais abaixo nesta página.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose é um formato familiar, mas não impõe a postura de segurança que o Quadlet impõe — você precisa definir cada flag de hardening à mão:

```yaml
services:
  rousseau:
    image: rousseau-agent:local
    read_only: true
    cap_drop: [ALL]
    security_opt:
      - no-new-privileges:true
      - seccomp:default
    user: "1000:1000"
    tmpfs:
      - /tmp:size=64m,mode=1777
    volumes:
      - ${HOME}/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
      - ${HOME}/.claude:/home/rousseau/.claude:rw,Z
      - ${HOME}/team-rousseau-workspace:/workspace:rw,Z
    environment:
      HOME: /home/rousseau
    restart: unless-stopped
    command: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Docker com root</span><p>O daemon Docker clássico executa como root. Mesmo com <code>user: "1000:1000"</code>, o daemon tem as capabilities do dono do socket Docker. Prefira Docker rootless ou Podman.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes precisa de um Deployment + PVC. Veja o manifesto abaixo, além de [Guias: Implantação em Kubernetes](/pt-BR/guides/kubernetes-deployment/) para um exemplo completo de Helm chart.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: rousseau-agent, namespace: agents }
spec:
  replicas: 1
  strategy: { type: Recreate }
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: rousseau
          image: ghcr.io/sebastienrousseau/rousseau-agent:v0.6.0
          args: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: { drop: [ALL] }
            readOnlyRootFilesystem: true
          volumeMounts:
            - { name: state, mountPath: /home/rousseau/.local/share/rousseau }
            - { name: tmp,   mountPath: /tmp }
      volumes:
        - name: state
          persistentVolumeClaim: { claimName: rousseau-state }
        - name: tmp
          emptyDir: { medium: Memory, sizeLimit: 64Mi }
```

  </div>
</div>

## Gerenciamento de segredos

Nunca coloque chaves de API ou tokens no `config.yaml`. Carregue-os em runtime a partir de um backend de segredos:

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">systemd credentials</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Use `vault agent` para renderizar variáveis de ambiente em um arquivo que o rousseau lê. Modelo de exemplo:

```
{{- with secret "kv/rousseau/anthropic" }}
ANTHROPIC_API_KEY={{ .Data.data.api_key }}
{{- end }}
```

Systemd:

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/vault-agent -config=/etc/vault/agent.hcl
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Use `aws secretsmanager` para buscar a chave em um arquivo de env no boot:

```sh
aws secretsmanager get-secret-value \
  --secret-id rousseau/anthropic \
  --query SecretString --output text | \
  jq -r '"ANTHROPIC_API_KEY=\(.api_key)"' > /run/rousseau/env
```

Systemd:

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/fetch-secrets.sh
```

Combine com IRSA no EKS para que o SDK resolva credenciais de forma transparente — sem necessidade de chaves AWS estáticas no host.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Use `gcloud secrets versions access`:

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

Ou, em Kubernetes, use o [driver CSI do Secret Manager](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component) para montar segredos como arquivos.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Credenciais do systemd (disponíveis no systemd 250+) carregam segredos em memória no início da unidade:

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

O daemon lê `$CREDENTIALS_DIRECTORY/anthropic_key` no início. Sem gravações em disco além do armazenamento (criptografado) de credenciais.

  </div>
</div>

## Compile a imagem

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Build multi-stage. Estágio 1: `golang:1.26-alpine` compila o binário estático (`CGO_ENABLED=0`). Estágio 2: `node:22-alpine` fornece o subprocesso `claude` CLI. A imagem de runtime tem ~550 MB; a camada Node existe apenas para que o provider opcional `claudecli` tenha um lar.

Se você usar um provider diferente (Anthropic direto, Bedrock, Vertex, compatível com OpenAI), pode remover o runtime Node e encolher a imagem.

## Instale a unidade Quadlet

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Habilite no boot com `systemctl --user enable rousseau-agent.service` após confirmar que o lingering está ativo (`loginctl enable-linger $USER`).

## Postura de runtime — cada configuração do Quadlet

| Configuração | Valor | Justificativa |
|---|---|---|
| `Network=pasta` | Stack de rede rootless | `slirp4netns` foi removido de versões recentes do Podman; pasta é mais rápido em kernels modernos e bloqueia entradas do host por padrão. |
| `UserNS=keep-id` | Container UID 1000 → host UID 1000 | Arquivos com bind mount mantêm a propriedade do host; o processo do contêiner pode escrever em arquivos de propriedade do host. |
| `ReadOnly=true` | Filesystem raiz somente leitura | O daemon nunca deveria mutar a imagem em runtime. Qualquer coisa gravável vive em um bind mount ou no tmpfs. |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | Scratch gravável | Para qualquer coisa que precise de um arquivo temporário em runtime (raro). |
| `DropCapability=all` | Todas as capabilities removidas | O binário Go não precisa de capabilities elevadas — TCP de saída não requer `CAP_NET_BIND_SERVICE` ou similar. |
| `NoNewPrivileges=true` | Bit `no_new_privs` ativado | Bloqueia escalada setuid dentro do contêiner. |
| `SeccompProfile=/usr/share/containers/seccomp.json` | Filtro seccomp padrão | Gating de syscalls no nível do kernel além das capabilities removidas. |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | Bind mount do estado | Sessões, pareamento do WhatsApp, jobs cron, mapa de JID, índice FTS5. `:Z` define o rótulo SELinux. |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | Autenticação do `claude` CLI | Relevante apenas quando o provider `claudecli` está ativo. O `claude` atualiza OAuth em cache no lugar. |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | Workspace | Apenas o workspace é visível de dentro do contêiner. Nada mais do host é montado. |
| `Environment=HOME=/home/rousseau` | Define `$HOME` | Consumido pelo Viper, pelo `claude` CLI e pelo resolvedor de diretório de estado. |
| `AutoUpdate=disabled` | Podman não faz auto-update | Atualizações são feitas pelo operador em uma cadência de release, não silenciosamente. |

## Linha `Exec=`

O Quadlet vem com:

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

Substitua pelo transporte de sua escolha e sua allowlist. Múltiplos transportes tipicamente rodam em unidades Quadlet separadas — uma imagem, um binário, várias unidades — para que uma falha em um transporte não derrube os outros.

## Kubernetes / OpenShift

O `rousseau` é um daemon de binário único; um `Deployment` mínimo + `PersistentVolumeClaim` para o diretório de estado é suficiente:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
spec:
  replicas: 1
  strategy:
    type: Recreate           # do not run two daemons against one state DB
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile: {type: RuntimeDefault}
      containers:
        - name: rousseau
          image: registry.example.com/rousseau-agent:v1.0.0
          args: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: {drop: [ALL]}
            readOnlyRootFilesystem: true
          volumeMounts:
            - {name: state, mountPath: /home/rousseau/.local/share/rousseau}
            - {name: tmp,   mountPath: /tmp}
      volumes:
        - name: state
          persistentVolumeClaim: {claimName: rousseau-state}
        - name: tmp
          emptyDir: {medium: Memory, sizeLimit: 64Mi}
```

Como não há superfície HTTP de entrada, **nenhum `Service` ou `Ingress` é necessário** para transportes com WebSocket de saída (Slack, Discord, WhatsApp, Matrix). Somente um transporte no estilo webhook precisaria de um `Service`, e o rousseau não entrega nenhum por padrão.

A estratégia `Recreate` é deliberada — o arquivo de estado SQLite não é projetado para dois escritores concorrentes. Se você precisar de HA, execute um daemon por transporte e confie no próprio estado do transporte (Slack Socket Mode, Discord Gateway) para a semântica de reconexão.

## Destino de logs do systemd

O Quadlet herda a configuração do journal do systemd. `journalctl --user -u rousseau-agent.service` lê os logs. Para agregação de logs, use um sidecar journal-to-Loki / journal-to-Fluent-Bit; não canalize o formato de log do rousseau diretamente para o disco (o rousseau não faz log-rotation).

Configure o rousseau para emitir JSON para que os agregadores possam analisá-lo:

```yaml
log:
  level: info
  format: json
```

## Bloqueio de egresso com nftables (opcional)

`docker/nftables.rules.example` na árvore de código-fonte entrega um template para hardening de egresso no nível do kernel — descarta tudo exceto os ranges do WhatsApp Web da Meta, Anthropic (atrás do CloudFront, então use filtro baseado em domínio) e Signal. Sobreponha isso ao namespace do contêiner para a postura mais rígida. Veja [segurança](/pt-BR/security/) para o raciocínio.

## Helm chart (roadmap)

Um Helm chart first-party está no roadmap. Até que ele seja lançado, os manifestos acima são suficientes para uma implantação mínima. Acompanhe [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) para o progresso.

Esboço do `values.yaml` (para revisão de usuários potenciais):

```yaml
image:
  repository: ghcr.io/sebastienrousseau/rousseau-agent
  tag: v0.6.0
transport:
  name: whatsapp
  args: ["--allow", "447900123456@s.whatsapp.net"]
provider:
  name: anthropic
  # api_key sourced from a Secret
persistence:
  size: 4Gi
  storageClass: fast-ssd
resources:
  requests: { cpu: "100m", memory: "128Mi" }
  limits:   { cpu: "1",    memory: "512Mi" }
networkPolicy:
  enabled: true
  # egress: allowed CIDRs list
```

## Solução de problemas

### `podman play kube` falha com `permission denied` em um bind mount

Rótulo SELinux ausente. Todo volume deve terminar com `:Z` (ou `:z` para compartilhado). Veja [Solução de problemas: Contêiner falha ao fazer bind mount](/pt-BR/troubleshooting/#container-fails-to-bind-mount).

### Pod do Kubernetes em CrashLoopBackOff na primeira inicialização

O volume de estado não foi pré-criado, ou sua propriedade não corresponde ao UID 1000. Adicione um initContainer para fazer `chown` no volume:

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` não encontra a unidade Quadlet

`daemon-reload` não foi executado, ou o arquivo de unidade tem um typo. Confirme com `systemctl --user cat rousseau-agent.service` — o Quadlet gera a unidade dinamicamente, então cat é a ferramenta de depuração mais rápida.

### Após reboot, o daemon não inicia

Habilite lingering: `loginctl enable-linger $USER`. Sem lingering, o user manager do systemd sai no logout e não é reiniciado até o próximo login.

### Dois daemons se atrapalharam e o banco de estado está corrompido

Nunca execute dois daemons contra o mesmo `state.path`. Se ocorrer corrupção, faça backup do arquivo, `rm sessions.db{,-wal,-shm}`, reinicie. O histórico de sessão é perdido; o pareamento sobrevive se `whatsapp.db` for separado (é por padrão).

## Páginas relacionadas

- [Guias: Implantação em Kubernetes](/pt-BR/guides/kubernetes-deployment/) — Helm chart completo e exemplo de NetworkPolicy.
- [Guias: Implantação em produção](/pt-BR/guides/production-deployment/) — o checklist de produção.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — logs e métricas.
- [Segurança](/pt-BR/security/) — limites de confiança, seccomp, egresso.
- [Configuração](/pt-BR/configuration/) — todos os ajustes.

## Leitura complementar

- `docker/Dockerfile` — o build multi-stage.
- `docker/rousseau-agent.container` — a unidade Quadlet.
- `docker/example-nftables.rules` — conjunto de regras de egresso de exemplo.
- `Makefile` — automação de build.
- Docs do systemd: [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html).
