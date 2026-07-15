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
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/troubleshooting/"
subtitle: "Modos comuns de falha e como resolvê-los."
tags: "troubleshooting, support"
title: "Solução de problemas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Solução de problemas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Solução de problemas"
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
twitter_description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Solução de problemas"
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

## WhatsApp: QR não é escaneado

Sintoma: `rousseau whatsapp` imprime um QR que o app do telefone rejeita, ou o diálogo de pareamento diz "Este dispositivo não está pareado com o WhatsApp."

Correções:

1. **Recompile o contêiner.** Se você está executando uma imagem mais antiga, o `whatsmeow` pode ter recebido uma atualização de protocolo. Recompile:
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **Delete o `whatsapp.db`.** Um pareamento parcialmente concluído deixa o banco em um estado que o whatsmeow não pode reutilizar. Delete-o e refaça o pareamento:
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **Verifique o desvio de relógio.** O handshake do WhatsApp é sensível ao tempo. Se o relógio do contêiner estiver desviado por mais de 30 segundos, o pareamento falha silenciosamente.
   ```sh
   timedatectl status
   ```

## Loop de reconexão do WhatsApp

Sintoma: logs mostram `whatsapp.connected` seguido de `whatsapp.disconnected` repetidamente a cada poucos segundos.

Correções:

1. **Desvio de relógio.** Mesma correção acima.
2. **Allowlist mal configurada.** Cada mensagem de entrada é descartada como não autorizada; alguns servidores fecham o socket após muitos descartes silenciosos. Adicione os JIDs corretos com `--allow`.
3. **Banimento pela Meta.** Se o app móvel do WhatsApp mostrar "Este dispositivo foi desconectado", a Meta invalidou o pareamento. Refaça o pareamento a partir de um QR novo. Se acontecer repetidamente no mesmo número, pare de usar aquele número.

## cosign verify-blob falha

Sintoma:

```
Error: no matching signatures
```

Correções:

1. **Regex de certificate-identity errada.** A regex deve casar com o repositório GitHub que assinou a release. Para releases do rousseau-agent o valor correto é:
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   Não use `.*` — isso aceitaria uma assinatura cosign de qualquer repositório.
2. **Emissor OIDC errado.** Assinaturas cosign do GitHub Actions são emitidas por `https://token.actions.githubusercontent.com`. Outros providers de CI (GitLab, Buildkite) emitem a partir de URLs diferentes.
3. **Arquivo de assinatura errado.** Verifique se `<version>_checksums.txt.sig` corresponde ao `_checksums.txt` que você está verificando (não uma cópia obsoleta de uma release diferente).
4. **Trust root do Sigstore mudou.** Atualize com `cosign initialize`; o trust root é atualizado em uma rotação lenta.

## Contêiner falha ao fazer bind mount

Sintoma: `podman play kube` ou `systemctl --user start rousseau-agent.service` falha com `permission denied` em um bind mount.

Correções:

1. **Rótulo SELinux.** Cada linha de volume deve terminar com `:Z` (ou `:z` para compartilhado) para que o Podman aplique o rótulo SELinux correto:
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z` (maiúsculo) é o rótulo privado — apropriado para mounts de contêiner único. `:z` (minúsculo) compartilha o rótulo entre contêineres.
2. **Mapeamento `keep-id`.** Sem `UserNS=keep-id`, o UID 1000 do contêiner é remapeado no range subuid do host e não pode escrever em arquivos de propriedade do host. Garanta que o Quadlet tenha:
   ```
   UserNS=keep-id
   ```
3. **Diretório ausente.** O Podman não cria automaticamente as origens de bind mount. Crie o diretório primeiro:
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## Job de cron não dispara

Sintoma: `rousseau cron list` mostra o job, mas nada acontece no horário agendado.

Correções:

1. **Verifique o status.** `rousseau status` reporta a atividade do scheduler. Se o scheduler não está rodando, o daemon que o hospeda não está rodando.
2. **Fuso horário.** Schedules usam o fuso horário local do servidor. Confirme com `timedatectl`. Defina `TZ=UTC` no Quadlet se quiser scheduling determinístico independentemente do locale do host.
3. **Atraso do PollInterval.** Novos jobs entram em atividade dentro de `PollInterval` (padrão 60s). Espere um minuto.
4. **Falha na entrega.** O job disparou mas a entrega falhou. Verifique logs por `cron.delivery_failed`; o formato de destino é específico do transporte (veja [/cron/](/pt-BR/cron/)).

## Política de aprovação rejeitando tudo

Sintoma: cada chamada de tool é negada com "denied by pattern policy" e o modelo recusa a progredir.

Correções:

1. **Regra allow ausente.** No modo `pattern` com `default: deny`, cada chamada de tool precisa de uma regra de allow correspondente. Adicione uma para as tools que deseja permitir:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: deny
       allow:
         - {tool: read, match: ".*"}
         - {tool: grep, match: ".*"}
         - {tool: edit, match: "^./workspace/.*"}
   ```
2. **Deny prevalece sobre allow.** Uma regra `deny` sempre prevalece sobre uma regra `allow` para a mesma tool. Revise sua deny list em busca de over-matches acidentais.
3. **Eleve o padrão.** Para sessões atendidas, `default: allow` com regras deny apertadas costuma ser mais viável:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## Provider retorna 401

Sintoma: o agente erra com `provider: unauthorized`.

Correções:

1. **Chave de API errada.** Para o provider direto da Anthropic, verifique se `ANTHROPIC_API_KEY` está exportada ou definida em `~/.config/rousseau/config.yaml`.
2. **Cadeia de credenciais errada.** Para Bedrock, execute `aws sts get-caller-identity` de dentro do contêiner para confirmar qual principal o SDK resolve.
3. **Service account do Vertex.** Para o provider Vertex, confirme que o arquivo em `vertex.credentials_file` é legível dentro do contêiner e concede `roles/aiplatform.user`.

## Provider retorna 429

Sintoma: o agente erra com `provider: rate limited`.

Correções:

1. **Reduza `max_tokens`.** Completions mais curtas liberam a janela de rate mais rápido.
2. **Habilite a compressão.** Transcrições longas aumentam a pressão nos tokens de entrada; `agent.compression.enabled: true` colapsa mensagens antigas.
3. **Espere passar.** O rousseau não retenta dentro de `Complete`; o caller (transporte de chat, scheduler de cron ou `rousseau chat`) decide se e como retentar.

## `rousseau chat` mostra apenas um TUI em branco

Sintoma: o TUI Bubble Tea abre mas sem cursor, sem viewport.

Correções:

1. **Ambiente TERM.** O rousseau requer um terminal ANSI-capaz. Defina `TERM=xterm-256color` (ou similar).
2. **stdin envolvido.** Rodar sob `nohup` ou um pipe remove o terminal. Execute interativamente.

## Slack: `invalid_auth` no início

Sintoma: `slack.starting` imediatamente seguido de `invalid_auth`.

Correções:

1. **Token errado misturado.** O rousseau precisa de ambos `xapp-…` (app-level, `--app-token`) e `xoxb-…` (bot, `--bot-token`). Passar um app token onde um bot token é esperado produz esse erro.
2. **App não instalado.** Depois de criar os escopos, clique em *Install to Workspace* na configuração do app Slack. Tokens só são válidos após a instalação.
3. **Token rotacionado.** Tokens Slack podem ser rotacionados manualmente por um admin. Se você rotacionou um, todos os daemons que o usam devem ser reiniciados com o novo valor.

## Slack: bot responde às próprias mensagens (loop)

Sintoma: a mensagem de saída do rousseau dispara um evento de entrada ao qual o daemon responde, causando respostas descontroladas.

Correções:

1. **Defina `bot_user_id`.** A flag `--bot-user-id` (ou `slack.bot_user_id` na config) diz ao daemon para ignorar mensagens enviadas por aquele user ID. Recupere-o com `curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test`.
2. **Verifique o filtro de eventos.** O transporte ignora subtipos `bot_message` por padrão, mas um app Slack mal configurado pode contornar isso.

## Discord: texto da mensagem chega vazio

Sintoma: `discord.incoming from=... body=` — mensagens chegam mas sem conteúdo.

Correções:

1. **Message Content Intent desabilitado.** No Discord Developer Portal em <em>Bot &gt; Privileged Gateway Intents</em>, ative **Message Content Intent**. Sem isso, o Discord remove o texto da mensagem dos eventos do Gateway.
2. **Escopos ausentes.** A URL de convite deve ter concedido ao bot `Read Message History` e `Send Messages` para o canal/DM que você está usando.

## Discord: `disallowed intents`

Sintoma: erros de inicialização com `Discord returned 4014 disallowed intents`.

Correções:

1. **Intents privilegiadas.** Habilite *Message Content Intent* (veja acima). Mesmo que você nunca peça, o Discord retorna 4014 se você solicitar sem aprovação.
2. **Verificação.** Bots em 100+ servidores devem ser verificados pelo Discord para usar intents privilegiadas. Siga o passo a passo do developer portal.

## Telegram: `unauthorized`

Sintoma: `telegram.starting` seguido de `getUpdates: 401`.

Correções:

1. **Token errado.** O BotFather retorna o token uma vez — não inclua o ponto final. O token tem a forma `<bot_id>:<secret>`.
2. **Token revogado.** `/revoke` no BotFather invalida o token atual; obtenha um novo.

## Email: `dial tcp: i/o timeout`

Sintoma: a conexão IMAP ou SMTP nunca completa.

Correções:

1. **Porta errada.** IMAP é `993` (TLS implícito). Submissão SMTP é `587` (STARTTLS) ou `465` (TLS implícito). O rousseau usa TLS implícito em ambos — servidores só-STARTTLS ainda não são suportados. Veja [Transportes: Email](/pt-BR/transports/email/) para a migração.
2. **Egresso bloqueado.** Firewalls corporativos frequentemente bloqueiam SMTP de saída. Teste com `openssl s_client -connect smtp.example.com:465` de dentro do contêiner.
3. **Provider requer app password.** Gmail, Fastmail e similares requerem uma app password (não sua senha da conta) quando 2FA está habilitado. Gere uma nas configurações de segurança do provider.

## Vertex: `permission denied on resource`

Sintoma: `vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`.

Correções:

1. **Role ausente.** Conceda `roles/aiplatform.user` ao service account ou usuário que chama a API. Mudanças de IAM levam até um minuto para propagar.
2. **Projeto errado.** O `project` na configuração deve corresponder ao projeto que possui a cota. Se o billing está em um projeto diferente, use quota-project via `gcloud auth application-default set-quota-project`.
3. **Incompatibilidade de região.** O modelo deve estar disponível na região solicitada — o Vertex Model Garden lista isso.

## Bedrock: `You don't have access to the model`

Sintoma: `AccessDeniedException: You don't have access to the model with the specified model ID`.

Correções:

1. **Acesso ao modelo não solicitado.** O Bedrock requer solicitação explícita de acesso ao modelo via console (*Foundation models &gt; Model access*). Mesmo com o IAM permitindo `InvokeModel`, esse passo é necessário.
2. **Região errada.** A disponibilidade do modelo é regional. Verifique o console do Bedrock.
3. **Má configuração cross-account.** Se estiver usando AssumeRole, verifique se a política do role de destino permite `bedrock:InvokeModel` no ARN exato do modelo.

## Ollama: `context deadline exceeded`

Sintoma: o rousseau expira enquanto o Ollama ainda está gerando.

Correções:

1. **Inferência em CPU é lenta.** Um modelo 70B em CPU de laptop pode levar minutos por turno. Use um modelo menor (`llama3.1:8b`) ou um host com GPU.
2. **Herança de timeout.** O rousseau usa o timeout HTTP padrão do SDK. Se você envelopa o provider você mesmo, estenda o timeout para pelo menos 120 s.

## Notas de voz: transcritor não configurado

Sintoma: `whatsapp.audio_ignored reason=transcriber_not_configured`.

Correções:

1. **Whisper desabilitado.** Defina `whatsapp.voice.enabled: true` na configuração e garanta que o binário `whisper` está no `PATH` (ou defina `whatsapp.voice.binary` para um caminho absoluto).
2. **Arquivo de modelo ausente.** Defina `whatsapp.voice.model_path` para um arquivo `.bin` explícito. Modelos do Whisper.cpp são baixados manualmente — a configuração aponta para onde eles vivem.

## Armazenamento de sessão: `database is locked`

Sintoma: o writer WAL bloqueia; requisições expiram.

Correções:

1. **Dois daemons, um DB.** SQLite com WAL suporta leitores concorrentes mas apenas um escritor. Se você executar dois processos rousseau contra o mesmo `state.path`, um vai bloquear. Use paths de estado diferentes.
2. **`busy_timeout` muito baixo.** O DSN define `busy_timeout=15000`. Sob contenção sustentada, aumente-o — mas investigue a causa raiz primeiro.
3. **Arquivo WAL obsoleto.** Um writer que travou pode deixar `sessions.db-wal` travado. Pare tudo, delete `sessions.db-wal` e `sessions.db-shm`, reinicie.

## MCP: Claude Desktop não vê as tools do rousseau

Sintoma: rousseau lançado via `command: "rousseau"` em `claude_desktop_config.json`, mas nenhuma tool aparece.

Correções:

1. **Configuração não salva.** O Claude Desktop faz hot-reload no save; se você editou o arquivo em uma instância rodando, reinicie-a.
2. **`command` não está no PATH.** O Claude Desktop lança subprocessos a partir de seu próprio ambiente; `/usr/local/bin/rousseau` pode não estar visível. Use um caminho absoluto.
3. **Ruído no stderr.** O rousseau escreve logs estruturados no stderr; um logger muito verboso pode sobrecarregar o host. Defina `log.level: warn` ao executar MCP contra um host restrito.

## Skills: `skill loader: parse: yaml: line X`

Sintoma: o rousseau erra na inicialização com um erro de parse YAML.

Correções:

1. **Frontmatter mal-formado.** Skills usam frontmatter YAML delimitado por `---`. Garanta que ambas as cercas estejam presentes e não haja indentação por tabs.
2. **Dois-pontos sem aspas.** Um dois-pontos dentro de um valor (`description: this: that`) é interpretado como um mapa aninhado. Coloque o valor entre aspas: `description: "this: that"`.

## `rousseau doctor` reporta `warn`

Sintoma: o doctor completa mas com linhas em âmbar.

Correções:

1. **Leia o motivo.** Cada linha warn inclui um motivo. Comuns: `whatsapp.paired=false` (nunca linkado), `state.wal_size=large` (checkpoint atrasado), `provider.claudecli.model=unset` (usando o padrão do claude).
2. **Warns não são falhas.** O daemon vai iniciar; a linha está sinalizando algo que vale revisar.

## Kubernetes: pod preso em `CrashLoopBackOff`

Sintoma: o deployment nunca chega a Ready.

Correções:

1. **Leia os logs.** `kubectl logs -p <pod>` mostra o stderr do contêiner anterior. Nove em cada dez vezes é um erro de configuração ou credencial.
2. **Volume de estado ausente.** Sem um PVC para `~/.local/share/rousseau`, o pareamento não sobrevive ao restart e o daemon pode entrar em loop tentando refazer o pareamento.
3. **Má configuração de IRSA / Workload Identity.** Verifique se a annotation do service account casa com um IAM role que tem permissões de provider. Faça `kubectl exec` no pod e execute `aws sts get-caller-identity` (Bedrock) ou `gcloud auth print-access-token` (Vertex) para confirmar.

## Conjunto de regras nftables bloqueia egresso do provider

Sintoma: `dial tcp: i/o timeout` na primeira chamada ao provider após aplicar um conjunto de regras de egresso.

Correções:

1. **CIDR rotacionado.** Ranges de IP de providers mudam. Use egresso baseado em DNS via um ipset que atualiza em cron, ou use um proxy de egresso que resolve no momento da conexão.
2. **DNS bloqueado.** O conjunto de regras de egresso deve permitir UDP/53 (ou TCP/53) ao seu resolvedor DNS.

## Logs estruturados sem campos

Sintoma: `whatsapp.incoming` aparece com `from` e nenhum outro atributo.

Correções:

1. **Nível de log muito alto.** Alguns campos só são emitidos em `debug`. Defina `log.level: debug` na configuração.
2. **Parser JSON removendo campos.** Passar por um filtro que remove campos desconhecidos pode descartar `elapsed`, `bytes`, etc. Verifique contra stdout bruto.

## Páginas relacionadas

- [Começando: Seu primeiro transporte](/pt-BR/getting-started/first-transport/) — passo a passo de ponta a ponta.
- [Providers](/pt-BR/providers/) — solução de problemas por provider.
- [Transportes](/pt-BR/transports/) — solução de problemas por transporte.
- [Configuração](/pt-BR/configuration/) — a fonte da verdade para cada ajuste.
- [Segurança](/pt-BR/security/) — limites de confiança e trilha de auditoria.

## Leitura complementar

- `internal/cli/doctor.go` — a implementação do doctor.
- `internal/state/sqlite/store.go` — DSN do armazenamento de sessão e handling do WAL.
- `internal/transport/router.go` — roteamento de eventos de entrada e allowlist.
- Referência de chaves de atributos do slog — cada `.info()`/`.warn()`/`.error()` na árvore de código-fonte.
