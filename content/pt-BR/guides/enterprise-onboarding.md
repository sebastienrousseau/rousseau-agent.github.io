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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "Guia: onboarding empresarial"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: onboarding empresarial"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: onboarding empresarial"
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
twitter_description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: onboarding empresarial"
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

## Para quem é

Um time de plataforma avaliando o rousseau-agent antes que ele chegue perto de produção. Responde à pergunta "o que precisamos aprovar?". Cada item faz referência cruzada a uma coisa concreta específica que o rousseau envia para que a aprovação seja objetiva, não estética.

## Checklist

### 1. Supply chain

- [ ] **SBOM.** Confirme que cada release publica `rousseau_<v>_sbom.cdx.json` (CycloneDX 1.5). Importe no seu SCA scanner. Acionável: rode `cyclonedx-cli tree` contra o SBOM e faça grep por exceções de licença que sua org bane.
- [ ] **Provenance SLSA-3.** Cada release publica `rousseau_<v>_provenance.intoto.jsonl`. Verifique com `slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …`.
- [ ] **Trust root cosign.** Fixe o regex de identidade de certificado: `sebastienrousseau/rousseau-agent`. Cache a receita de verificação de checksum na sua ferramenta de bootstrap; veja [Quickstart](/pt-BR/quickstart/) passo 5.
- [ ] **Build reproduzível.** `make check` roda `go test -race` mais `govulncheck`. Configure uma varredura periódica de vulnerabilidade da versão que você está rodando.

### 2. Endurecimento de runtime

- [ ] **Contêiner rootless.** `docker/rousseau-agent.container` roda a unidade Quadlet sob um usuário sem privilégio dedicado com `loginctl enable-linger`. Confirme que seu host está configurado do mesmo jeito.
- [ ] **Todas as caps descartadas.** `DropCapability=all`. `podman inspect | jq '.[0].EffectiveCaps'` deve mostrar `[]`.
- [ ] **`NoNewPrivileges=true`.** Impede processos filhos de ganhar privilégios.
- [ ] **Filesystem raiz somente leitura.** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`.
- [ ] **Perfil Seccomp.** `SeccompProfile=/usr/share/containers/seccomp.json`. Audite contra o baseline do seu host.
- [ ] **Mapeamento de user namespace.** `UserNS=keep-id`. Confirma que arquivos bind-mountados têm ownership correto em ambos os lados.

### 3. Postura de rede

- [ ] **Sem inbound.** O rousseau tem zero superfície HTTP. `ss -tanp | grep rousseau` mostra sockets somente outbound.
- [ ] **Allowlist de egress.** Coloque nftables ou Cloudflare Zero-Trust fora do contêiner. Permita apenas:
  - O provider de LLM (`api.anthropic.com`, `bedrock-runtime.<region>.amazonaws.com`, `us-east1-aiplatform.googleapis.com`, etc.).
  - O transporte (`web.whatsapp.com`, `mtproto.telegram.org`, homeserver matrix, Slack `wss-*`).
- [ ] **Resolver DNS travado.** Opcionalmente rode um `unbound` em um contêiner adjacente que só resolve os nomes na allowlist.

### 4. Política de aprovação

- [ ] **`mode: pattern` para cada daemon sem supervisão.** Verifique `agent.approver.mode: pattern` na config para cada serviço de transporte.
- [ ] **`default: deny`.** Nenhuma call não correspondida passa.
- [ ] **Lista de deny para `bash`.** `rm\s+-rf`, `sudo`, `curl`, `wget`, `chmod`, `chown`, `nc`, `ncat`. Veja [Tutorial: Endurecer o approver](/pt-BR/tutorials/harden-approver-policy/).
- [ ] **Pin de path para `write` / `edit`.** Regex restringe escritas a `/workspace/...`.
- [ ] **Config em source control.** O YAML do approver é código — revise em PR.

### 5. Manejo de segredos

- [ ] **Sem API keys em `config.yaml`.** Armazene segredos em um `EnvironmentFile=` de `systemd` (`chmod 0600`) ou no secret manager da org.
- [ ] **`ANTHROPIC_API_KEY` piped via env.** `config.Load` (`internal/config/config.go`) o pega.
- [ ] **IRSA do Bedrock / ADC do Vertex.** Prefira federation de identidade a API keys de longa duração.
- [ ] **Cadência de rotação.** 90 dias ou o que sua política demandar. O rousseau não cacheia credenciais — uma chave rotacionada é pega no próximo restart do daemon.

### 6. Dados em repouso

- [ ] **Criptografia de `sessions.db`.** Criptografia de disco inteiro (LUKS no Linux, FileVault no macOS, volumes EBS-encrypted na AWS). O rousseau não implementa criptografia em nível de aplicação no session store.
- [ ] **Backups criptografados.** Restic ou borg ambos criptografam em repouso com uma chave que você controla.
- [ ] **Política de retenção.** Bulk-delete de sessões mais velhas que `N` dias — veja [Guias: Gerenciamento de sessão](/pt-BR/guides/session-management/) para o SQL.
- [ ] **Manejo do JID map.** A tabela `jid_sessions` mapeia números de telefone para session IDs. Trate como PII.

### 7. Logs e auditoria

- [ ] **`log.format: json`.** Saída parseable por máquina.
- [ ] **Envio de log para fora do host.** Vector / Promtail / Datadog. Veja [Guias: Observabilidade](/pt-BR/guides/observability/).
- [ ] **Retenção.** 90 dias mínimo em cold storage. A trilha de auditoria do rousseau é inteiramente em slog; você a torna durável.
- [ ] **Alerta em `tool.denied`.** Alerte em qualquer negação — pode ser benigna ou uma tentativa de injection.
- [ ] **Alerta em `whatsapp.logged_out`.** Quebra de política da Meta significa que a conta está fora de ação.

### 8. Gestão de mudança

- [ ] **Mudanças de config são código.** Revisadas em PR, versionadas em git.
- [ ] **Bumps de imagem são deliberados.** `AutoUpdate=disabled` na unidade Quadlet é intencional.
- [ ] **Plano de rollback.** Mantenha a imagem anterior tagged e disponível. `podman tag localhost/rousseau-agent:local rousseau-agent:previous` antes de cada build.

### 9. Resposta a incidentes

- [ ] **Escala de on-call.** Alguém pode rodar `systemctl --user stop rousseau-agent` dentro do seu SLO de MTTR.
- [ ] **Playbook de comprometimento.** Passos para: revogar a API key de LLM, revogar o token de transporte (por exemplo, re-instalação do bot Slack), snapshotar o session store, imagear o filesystem do contêiner, desvincular device do WhatsApp.
- [ ] **Canal de disclosure de segurança.** Leia `SECURITY.md` no repo do rousseau-agent para o endereço de disclosure coordenado.
- [ ] **SLO para correções de segurança.** Track de CVEs contra a versão fixada do rousseau. `govulncheck` em `make check` pega issues conhecidos da stdlib do Go e de dependências.

### 10. Mapeamento de compliance

- [ ] **Evidência SOC 2.** Provenance SLSA-3 + cosign + SBOM cobre CC7.1 (operações de sistema). Logs do approver cobrem CC7.2.
- [ ] **ISO 27001 A.12 Operations Security.** Políticas de aprovação + escopo de workspace + audit logs.
- [ ] **OWASP LLM Top-10.** O rousseau não atesta o LLM Top-10 hoje — isso é um item de roadmap. Documente seus controles compensatórios (approver + contêiner) na sua auditoria.

## Template de sign-off

Abaixo está um template leve que seu time de plataforma pode copiar para um runbook:

```
Rousseau-agent deployment sign-off
=================================
Version: <tag>            (verified via cosign / SLSA verifier)
Provider: <anthropic|bedrock|vertex|openai>
Transports enabled: <list>
Approver mode: pattern
Approver default: deny
Log destination: <Loki / Datadog / etc>
Backup destination: <s3://... / restic repo>
On-call: <team>
Security disclosure: <internal address>
```

## Relacionado

- [Segurança](/pt-BR/security/) — as fronteiras de confiança que este checklist protege.
- [Implantação](/pt-BR/deployment/) — a unidade Quadlet.
- [Tutorial: Deploy a um VPS](/pt-BR/tutorials/deploy-to-a-vps/) — exemplo trabalhado.
- [Guias: Implantação de produção](/pt-BR/guides/production-deployment/) — específicos operacionais.
