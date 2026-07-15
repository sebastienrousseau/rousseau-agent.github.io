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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "Caso de uso: setor regulado"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Caso de uso: setor regulado"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Caso de uso: setor regulado"
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
twitter_description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Caso de uso: setor regulado"
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

## A história

Você é um engenheiro de plataforma em um banco de porte médio. A área de compliance diz que qualquer assistente de codificação usado pelos seus engenheiros deve:

1. Rodar dentro das contas AWS do banco, não em um control plane SaaS.
2. Rotear o tráfego do modelo por um provider com o qual o banco tem contrato e trilha de auditoria (Bedrock).
3. Ter uma postura documentada de supply chain (SLSA-3, SBOM, verificação de assinatura).
4. Aplicar políticas de aprovação com uma trilha de auditoria legível por máquina.
5. Não exfiltrar código fonte para terceiros.

O posicionamento do rousseau se encaixa em cada um desses requisitos. Você o roda como um `Deployment` Kubernetes no cluster EKS do time de plataforma, dirigindo um transporte Slack Socket Mode no canal de engenharia.

O rollout de engenharia é sem novidades — um `Deployment`, um `Secret`, um `ConfigMap`, um `PersistentVolumeClaim`. A história é o que acontece quando o auditor chega.

## A auditoria

Um auditor externo faz quatro perguntas.

**P1: Para onde vai o tráfego do modelo?**

Você aponta para `internal/llm/bedrock/`. O provider usa a cadeia padrão de credenciais AWS (via IRSA no EKS), então as credenciais são tokens STS de vida curta. O tráfego nunca sai da sua conta AWS.

**P2: Como você verifica o binário que está rodando?**

Você mostra o `docker/Dockerfile` — um build multi-stage com base `golang:1.26-alpine` fixada — e o script `release-verify.sh` que o time de SRE roda durante a promoção de imagem:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

Você acrescenta: a provenance SLSA-3 é atestada via GitHub Actions OIDC. O log de transparência Sigstore é um trust anchor público.

**P3: Como você impede o modelo de mutar produção?**

Você aponta para a config `agent.approver`:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|git log|go test|go build) "}
    deny:
      - {tool: bash, match: "rm -rf|sudo|curl|wget|chmod|chown"}
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|exec)"}
      - {tool: bash, match: "aws (s3 rm|iam|kms delete)"}
      - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
      - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

Deny vence allow. Não correspondido → deny. Cada decisão é logada como um evento slog estruturado (`tool.execute`, `tool.denied`) e encaminhada ao tenant Datadog do banco via um daemonset Vector.

**P4: Onde é armazenado o código fonte que uma sessão referencia?**

Você explica: o estado da sessão vive em um PVC lastreado por EBS com criptografia em repouso. O contexto do modelo fica dentro da sessão comprimida (veja [Compressão + Recall](/pt-BR/user-guide/compression-recall/)). O índice de recall FTS5 roda no mesmo PVC. Nada vai para `agentskills.io` ou qualquer URL externa — [Skills](/pt-BR/skills/) são carregadas de um diretório bind-mountado, não de um registry hospedado.

O auditor pergunta de acompanhamento: "E o próprio modelo?" Você explica que o Bedrock é a fronteira do modelo; qualquer coisa que o Bedrock faça com prompts é governada pelo contrato existente do banco com a AWS.

## O que isso requer

### O manifesto

Veja [Guias: Implantação Kubernetes](/pt-BR/guides/kubernetes-deployment/) para o manifesto completo. Desvios-chave para este caso de uso:

- **Namespace `pod-security.kubernetes.io/enforce: restricted`.**
- **IRSA** para credenciais Bedrock — sem chaves AWS de vida longa em secrets.
- **NetworkPolicy** permitindo egress somente para endpoints regionais Bedrock e Slack WSS.
- **Daemonset Vector** enviando saída slog para o Datadog com o campo `msg` parseado como uma facet.

### A config

```yaml
provider: bedrock

bedrock:
  region: eu-west-1
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  max_tokens: 4096

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  compression:
    enabled: true
    trigger_messages: 40
    keep_recent: 6
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow: [...as above...]
    deny:  [...as above...]

slack:
  app_token: xapp-<from-Secret>
  bot_token: xoxb-<from-Secret>
  allowlist:
    - U012ABC   # platform team on-call
    - U012DEF   # platform team lead
```

### A história de auditoria

Cada tool call é uma linha slog. Cada negação é outra. O monitor do Datadog em `msg:tool.denied` alerta o SOC. Semanalmente, o time de plataforma extrai um relatório:

```
# LogQL / Datadog / whichever
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

O relatório vai para o drive de compliance. Como o schema slog é estável ([Observabilidade](/pt-BR/guides/observability/)), o parsing não quebra entre upgrades do rousseau.

## O que o auditor pode não perguntar mas deveria

- **Builds reproduzíveis.** O CI do rousseau inclui um job `reproducible-build` que verifica saída bit-idêntica em checkouts limpos. Você pode reconstruir independentemente a partir de um source com tag e comparar SHA-256.
- **Pinning de dependências.** `go.mod` fixa versões exatas; `go.sum` é congelado. O Dependabot abre updates como PRs revisáveis, não bumps silenciosos.
- **`govulncheck` em cada commit.** Qualquer vulnerabilidade conhecida que alcance um símbolo importado falha o CI.
- Análise estática **CodeQL** em cada commit.

Tudo o acima está em [Segurança](/pt-BR/security/) — a gaveta de arquivos de compliance já existe.

## A fronteira out-of-tenant

O Bedrock é a fronteira. O tráfego para `bedrock-runtime.eu-west-1.amazonaws.com` sai do pod mas fica dentro da AWS. O diagrama de fluxo de dados do banco mostra uma seta do pod para o Bedrock; não existem outras setas de outbound para essa implantação (Slack Socket Mode é WSS de outbound para `wss-primary.slack.com`, que é documentado como um egress permitido separado).

## Páginas relacionadas

- [Guias: Implantação Kubernetes](/pt-BR/guides/kubernetes-deployment/) — os manifestos.
- [Guias: Auditoria + Políticas de Aprovação](/pt-BR/guides/audit-approval-policies/) — a história de compliance.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — o pipeline slog.
- [Provider Bedrock](/pt-BR/providers/bedrock/) — cadeia de credenciais e comportamento de região.
- [Segurança](/pt-BR/security/) — modelo de confiança e controles de supply chain.
