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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "Sécurité"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Sécurité"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Sécurité"
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
twitter_title: "Sécurité"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Le modèle de menace de rousseau en prose et sous forme de diagramme ASCII, les frontières porteuses (politique d'approbation, isolation conteneur, chaîne d'approvisionnement), le filtre seccomp de référence et comment le durcir davantage, la politique de trafic sortant réseau, et la piste d'audit qui atterrit dans <code>slog</code>. Recoupez avec <code>SECURITY.md</code> dans l'arbre source et <code>docker/rousseau-agent.container</code> pour la source faisant foi.</p></aside>

## Diagramme du modèle de menace

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

Tout ce qui se trouve dans le cadre du conteneur est sous contrôle de rousseau. L'entrée depuis le transport de chat arrive déjà chiffrée E2EE (WhatsApp) ou en TLS (Slack, Discord, Matrix, Telegram, Email, SMS). La sortie vers le fournisseur LLM est en TLS. Les bind mounts sont le seul accès du daemon au système de fichiers hôte.

## Modèle de confiance — ce qui est dans le périmètre

`rousseau-agent` est un **daemon local, natif conteneur**. Trois frontières porteuses :

### 1. Le shell de l'utilisateur

L'outil intégré `bash` exécute des commandes arbitraires avec les privilèges de l'utilisateur. **C'est la frontière de sécurité principale.** Chaque appel d'outil est présenté avant exécution et soumis à la politique d'approbation configurée (`allow_all`, `deny_all` ou mode `pattern` avec règles regex allow/deny par outil et défaut configurable).

Les opérateurs qui exécutent des daemons non supervisés (transports de chat) **doivent** soit :

- imposer le mode `pattern` avec `default: deny` et des règles allow explicites, soit
- accepter la posture `bypassPermissions` en pleine conscience de l'exposition.

Il n'existe aucun compromis dans lequel le modèle s'auto-régule. Si le daemon peut sortir en shell et qu'il est joignable depuis un transport de chat, les utilisateurs joignables peuvent, en principe, piloter le shell.

### 2. Isolation conteneur

Le déploiement de référence est un conteneur Podman rootless avec :

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- Filtre seccomp par défaut (`/usr/share/containers/seccomp.json`)
- UID non-root 1000
- Mapping user-namespace `keep-id`
- `Network=pasta` (rootless, aucune entrée depuis l'hôte par défaut)

Seuls le bind mount du workspace, le répertoire d'état et `~/.claude` sont visibles depuis l'intérieur du conteneur. Voir [/deployment/](/fr/deployment/).

### 3. Chaîne d'approvisionnement

Chaque commit exécute `govulncheck` et CodeQL. Chaque release livre :

- **Provenance SLSA niveau 3** via `slsa-framework/slsa-github-generator`, signée via l'OIDC de GitHub Actions.
- **Signature cosign** sur le fichier de checksums, vérifiable via le journal de transparence Sigstore.
- **SBOM CycloneDX JSON.**
- **Attestation de build reproductible** — un job CI dédié vérifie l'obtention d'une sortie bit-à-bit identique depuis un checkout neuf.

## Modèle de confiance — ce qui est hors périmètre

- **Sorties malveillantes du modèle.** L'opérateur est responsable de la revue des appels d'outils avant approbation. Les politiques d'approbation réduisent les erreurs ; elles n'éliminent pas la nécessité du jugement humain.
- **Toolchain Go, runtime conteneur ou OS hôte compromis.** Un environnement de build de confiance est présupposé.
- **Accès physique à la machine.**
- **Attaques contre le fournisseur LLM lui-même.** Les vulnérabilités du fournisseur relèvent de sa responsabilité.

## Contrôles supply chain

| Contrôle | Implémentation |
|---|---|
| Pinning des dépendances directes | Versions exactes dans `go.mod` ; résolution transitive figée dans `go.sum`. |
| Analyse de vulnérabilités | `govulncheck ./...` à chaque build CI. Les builds échouent en présence d'une vulnérabilité connue atteignant un symbole importé. |
| Analyse statique | `golangci-lint` v2 (18 linters) + GitHub CodeQL (Go). |
| Mises à jour de dépendances | Dependabot pour `gomod` et `github-actions`, cadence hebdomadaire. |
| Provenance de build | SLSA niveau 3 via `slsa-framework/slsa-github-generator` ; attestée via l'OIDC de GitHub Actions et publiée dans le journal de transparence Sigstore. |
| Signature de release | Les checksums de release sont signés avec cosign (sans clé, via l'OIDC GitHub Actions). |
| Nomenclature logicielle | SBOM CycloneDX JSON attaché à chaque artefact de release. |
| Builds reproductibles | Job CI dédié `reproducible-build` qui vérifie l'obtention d'une sortie bit-à-bit identique. |

Les workflows CI vivent sous `.github/workflows/` dans l'arbre source : `ci.yml`, `codeql.yml`, `slsa.yml`, `release.yml`, `reproducible-build.yml`.

## Vérifier une release

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

Les deux flags qui verrouillent l'identité :

- `--certificate-identity-regexp` correspond au dépôt GitHub qui a émis le certificat de signature. Ne l'élargissez jamais à `.*` ; c'est ce qui empêche qu'une signature cosign d'un autre dépôt valide votre fichier de checksums.
- `--certificate-oidc-issuer` verrouille l'émetteur OIDC sur GitHub Actions.

L'entrée du journal de transparence Sigstore peut être interrogée séparément sur https://search.sigstore.dev/.

## Contrôles d'exécution

Chaque réglage ci-dessous est positionné sur l'unité Quadlet de référence et devrait figurer au socle de tout opérateur de conteneur :

- **Utilisateur non-root (UID 1000)** — aucun privilège à élever pour devenir root dans le conteneur.
- **`ReadOnly=true`** — l'image n'est pas modifiable à l'exécution ; le binaire ne peut ni se modifier ni modifier ses dépendances.
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`** — le seul emplacement modifiable hors bind mounts.
- **`DropCapability=all`** — aucun bit `CAP_*` positionné. Le TCP sortant n'en requiert aucun.
- **`NoNewPrivileges=true`** — bloque l'élévation setuid.
- **Filtre seccomp par défaut** — filtrage des appels système au niveau noyau.
- **`Network=pasta`** — pile réseau rootless ; aucune entrée depuis l'hôte par défaut.
- **Aucun port publié** — pas de `PublishPort=` dans le Quadlet. Il n'y a aucune surface HTTP entrante à publier.

## Inventaire cryptographique

| Usage | Implémentation |
|---|---|
| TLS vers endpoints LLM / transports | Bibliothèque standard Go `crypto/tls` avec le magasin de confiance système. |
| WhatsApp | `whatsmeow` (protocole Signal). |
| Matrix | API client-serveur sur HTTPS. |
| SMTP (transport email) | Bibliothèque standard Go `net/smtp` avec `PlainAuth` sur TLS. |
| Magasin de sessions au repos | **Non chiffré au niveau applicatif.** Les opérateurs exigeant un chiffrement au repos doivent monter le répertoire d'état sur un système de fichiers chiffré (LUKS, FileVault). |

Aucune primitive cryptographique custom n'est implémentée dans ce projet.

## Divulgation

Signalez en privé à **sebastian.rousseau@gmail.com**. **N'ouvrez pas** d'issue publique pour des signalements de sécurité.

Incluez :

- Description concise et vecteur CVSS 3.1.
- Composant affecté (chemin de fichier + plage de lignes, ou chemin de module de dépendance).
- Détails d'environnement (`rousseau version`, version de Go, OS, runtime conteneur).
- Reproduction minimale — idéalement un test qui échoue.

### Engagements de réponse

| Événement | SLA |
|---|---|
| Accusé de réception du signalement | ≤ 72 heures |
| Décision de triage (accept / decline / besoin d'info) | ≤ 7 jours |
| Correctif livré pour **Critique** (CVSS ≥ 9.0) | ≤ 14 jours |
| Correctif livré pour **Élevée** (7.0–8.9) | ≤ 30 jours |
| Correctif livré pour **Moyenne / Faible** | planifié dans une release courante |
| Divulgation publique (coordonnée) | après release du correctif |

## Versions supportées

Seule la branche `main` et la release taggée la plus récente reçoivent des correctifs de sécurité. Il n'existe pas de branches LTS.

## Décomposition du filtre seccomp

L'unité Quadlet de référence utilise le profil seccomp par défaut de Podman à `/usr/share/containers/seccomp.json`. Il bloque environ 70 appels système dont aucune invocation correcte de rousseau n'a besoin, notamment :

| Famille de syscall | Bloqué | Justification |
|---|---|---|
| Keyring noyau (`add_key`, `keyctl`, `request_key`) | oui | rousseau ne touche pas au keyring noyau. |
| Gestion des mounts (`mount`, `umount`, `pivot_root`, `chroot`) | oui | Aucun changement de mount dynamique à l'exécution. |
| Modules noyau (`init_module`, `finit_module`, `delete_module`) | oui | Le daemon ne peut pas charger de modules noyau. |
| Manipulations de namespaces (`setns`, `unshare` avec certains flags) | filtré | Prévient l'évasion de conteneur via swap de namespace. |
| Primitives de debug (`ptrace`, `process_vm_readv`, `process_vm_writev`) | oui | Rousseau ne s'attache pas à d'autres processus. |
| BPF (`bpf`) | oui | Aucun programme eBPF depuis l'intérieur du conteneur. |
| Redémarrage (`reboot`, `kexec_*`) | oui | Le conteneur n'a aucune raison légitime de redémarrer l'hôte. |
| Changements d'horloge (`clock_settime`, `adjtimex`) | oui | L'heure est gérée par l'hôte. |

Le profil par défaut autorise assez d'appels système pour la bibliothèque standard, le driver SQLite (`modernc.org/sqlite`), le client whatsmeow et les SDK OpenAI/Anthropic. Pour durcir davantage — par ex. retirer `personality` parce que vous n'émulez jamais d'autres ABI — copiez le profil par défaut, supprimez l'appel système et référencez la copie via `SeccompProfile=/path/to/profile.json` dans le Quadlet.

<aside class="admonition" data-type="caution"><span class="admonition-title">Tester un profil plus strict</span><p>Chaque ajustement seccomp doit être couvert par votre smoke test — un appel système que vous ignoriez nécessaire fera échouer une complétion ou un transport à l'exécution. Testez avec un aller-retour de chat réel avant de déployer en production.</p></aside>

## Politique de trafic sortant réseau

Par défaut, le conteneur n'a aucune entrée et sortie non restreinte (`Network=pasta`). Pour les déploiements haute sécurité, ajoutez un jeu de règles nftables qui n'autorise que les domaines dont rousseau a besoin :

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

Les plages CIDR évoluent — traitez ce qui précède comme un squelette. L'important est que le trafic sortant de rousseau est fini et énumérable ; l'exemple `docker/example-nftables.rules` dans les sources sert de point de départ.

## Piste d'audit via slog

Chaque événement à portée de sécurité est journalisé via `log/slog` de Go au niveau JSON structuré (`log.format: json`). Les événements à surveiller en production :

| Événement | Niveau | Source | Ce qu'il indique |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | Quel outil le modèle a demandé d'exécuter, dans quelle session. |
| `tool.denied` | warn | `internal/agent/agent.go` | Un approver a refusé un appel ; contient la chaîne de motif. |
| `tool.error` | warn | `internal/agent/agent.go` | L'outil s'est exécuté mais a retourné une erreur. |
| `router.transport.rejected` | info | `internal/transport/router.go` | Un message entrant a échoué l'allowlist. |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | Meta a invalidé l'appairage. |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | Un handler d'outil MCP a retourné une erreur. |
| `cron.delivery_failed` | warn | `internal/cron/` | La livraison via transport d'un job planifié a échoué. |

Injectez le flux JSON dans Loki / Datadog / Splunk / un pipeline Vector ; voir [Guides : Observabilité](/fr/guides/observability/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Nommage des champs</span><p>Les clés d'attributs slog sont namespacées par point (<code>whatsapp.connected</code>, pas <code>event=whatsapp_connected</code>). Interrogez avec la clé brute dans l'outil de logs que vous utilisez.</p></aside>

## Dépannage

### Le conteneur refuse de démarrer avec `mount: permission denied`

Mauvais label SELinux. Assurez-vous que chaque ligne de bind-mount se termine par `:Z` (label privé) ou `:z` (partagé). Sans label, le processus conteneur ne peut ni lire ni écrire les fichiers étiquetés par l'hôte.

### Seccomp tue un appel système dont j'ai besoin

Podman affiche `syscall X blocked` dans le journal. Reproduisez avec `strace -f -e trace=X` hors du conteneur pour confirmer ce qui a besoin de l'appel. Si c'est légitime, copiez le profil seccomp par défaut, ajoutez l'appel à l'allow-list et référencez le profil via `SeccompProfile=`.

### `cosign verify-blob` affiche "certificate identity does not match"

Votre `--certificate-identity-regexp` est erroné. Utilisez `sebastienrousseau/rousseau-agent`. Toute regex plus laxiste (`.*`, `.+`) ruine l'intérêt de la signature sans clé.

### La sortie fournisseur échoue sous restrictions nftables

Votre jeu de règles n'inclut pas la plage IP actuelle du fournisseur. Les fournisseurs font tourner leurs CIDR. Utilisez un egress basé DNS avec un ipset résolu par cron, ou un proxy egress qui résout les noms au moment de la connexion.

### Rien dans slog alors que j'attends des événements d'audit

Niveau de log trop haut. Positionnez `log.level: info` (ou `debug` pour du détail au niveau wire) et confirmez que le daemon démarre bien une nouvelle session — `slog.Default()` est utilisé avant le chargement de la configuration, donc les messages de tout début de boot sortent sur stderr au format texte quoi qu'il arrive.

## Pages liées

- [Déploiement](/fr/deployment/) — l'unité Quadlet de référence.
- [Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/) — le levier de sécurité principal.
- [Guides : Injection de prompt](/fr/guides/prompt-injection/) — attaques qui passent par les sorties du modèle.
- [Guides : Mode lecture seule](/fr/guides/read-only-mode/) — comment faire tourner un daemon « on regarde, on ne touche pas ».
- [Guides : Observabilité](/fr/guides/observability/) — pipeline slog + Loki / Datadog.

## Pour aller plus loin

- `SECURITY.md` — le document de politique de référence.
- `docker/rousseau-agent.container` — l'unité Quadlet de référence.
- `docker/example-nftables.rules` — exemple de jeu de règles egress.
- `internal/agent/agent.go` — où sont émis les événements `tool.execute` et `tool.denied`.
- `internal/agent/approver.go` — implémentations des politiques d'approbation.
