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
changefreq: "monthly"
description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/quickstart/"
subtitle: "rousseau en cinq minutes : installer, configurer, converser, vérifier."
tags: "quickstart, install, provider, transport, supply-chain"
title: "Démarrage rapide"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Démarrage rapide"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Démarrage rapide"
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
twitter_description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Démarrage rapide"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## rousseau en 5 minutes

Rousseau est un binaire Go statique unique qui embarque une TUI Bubble Tea, un magasin de sessions SQLite à `~/.local/share/rousseau/sessions.db`, et neuf transports de messagerie (WhatsApp, Signal, Telegram, Slack, Discord, Matrix, iMessage, SMS, email). Aucun plan de contrôle SaaS, aucune télémétrie, aucun serveur de licence. Le LLM, c'est vous qui le fournissez.

Cette page vous guide de bout en bout :

- [ ] **1. Installer rousseau** — depuis les sources, `go install`, ou une release vérifiée par cosign.
- [ ] **2. Configurer votre LLM** — choisissez un provider (`claudecli` par défaut ; Anthropic, Bedrock, Vertex, ou tout endpoint compatible OpenAI).
- [ ] **3. Tenir votre première conversation** — `rousseau chat` dans votre terminal.
- [ ] **4. Ajouter un transport** — associer WhatsApp avec un JID autorisé.
- [ ] **5. Vérifier la chaîne d'approvisionnement** — vérifier avec cosign le fichier de sommes de contrôle, puis lire le SBOM CycloneDX et la provenance SLSA-3.

La plupart des opérateurs terminent en moins de dix minutes.

## 1. Installer rousseau

<aside class="admonition" data-type="tip"><span class="admonition-title">Recommandé</span><p><code>go install</code> est la voie la plus rapide si vous avez déjà Go 1.26+. En production, utilisez une release signée avec <code>cosign verify-blob</code> pour conserver les garanties de la chaîne d'approvisionnement.</p></aside>

<div class="tabs" data-tabs="qs-install">
  <div class="tab-list" role="tablist" aria-label="Install method">
    <button role="tab" aria-selected="true">go install</button>
    <button role="tab" aria-selected="false">From source</button>
    <button role="tab" aria-selected="false">Signed release</button>
    <button role="tab" aria-selected="false">Container</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
rousseau version
```

Le binaire embarque `modernc.org/sqlite` (voir `internal/state/sqlite/store.go`), donc aucune dépendance libc ou CGo à l'exécution. Fonctionne à l'identique sur macOS, Linux et Windows.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` exécute `go vet`, `golangci-lint`, `go test -race` et `govulncheck` — les mêmes portes que celles imposées par la CI.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Chaque release taguée publie une archive avec somme de contrôle, un SBOM CycloneDX, une attestation de provenance SLSA-3, et une signature cosign du fichier de sommes de contrôle :

```sh
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_linux_amd64.tar.gz
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt.sig

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt

sha256sum -c rousseau_0.6.0_checksums.txt --ignore-missing
tar -xzf rousseau_0.6.0_linux_amd64.tar.gz
sudo install -m 0755 rousseau /usr/local/bin/
```

<aside class="admonition" data-type="note"><span class="admonition-title">Note</span><p>L'identité <code>cosign</code> est limitée à l'OIDC de GitHub Actions de <code>sebastienrousseau/rousseau-agent</code>. Voir <a href="/fr/security/">Sécurité</a> pour la racine de confiance.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau est livré avec un `Dockerfile` compatible Podman à `docker/Dockerfile` et une unité Quadlet systemd à `docker/rousseau-agent.container`. Une image publiée sur ghcr.io est prévue dans la feuille de route ; en attendant, construisez-la localement :

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Voir [Déploiement](/fr/deployment/) pour l'unité Quadlet de référence avec une posture d'exécution durcie (rootless, `DropCapability=all`, `NoNewPrivileges=true`, seccomp).

  </div>
</div>

### Prérequis spécifiques à l'OS

<div class="tabs" data-tabs="qs-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
brew install go@1.26
# For the container path:
brew install podman
podman machine init && podman machine start
```

Pour le provider `claudecli` par défaut, installez Claude Code depuis https://claude.ai/download et exécutez `claude login` une fois.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Installez Go 1.26+ via votre gestionnaire de paquets ou depuis https://go.dev/dl. Pour la voie conteneur, utilisez Podman rootless ≥ 5.x avec le mode réseau `pasta`.

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI (facultatif, pour le provider `claudecli`) : téléchargez depuis https://claude.ai/download.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau fonctionne nativement sur Windows via `go install`. Le déploiement conteneur de référence est limité à Linux ; sur Windows, utilisez WSL 2 pour la voie Podman.

```powershell
winget install GoLang.Go
# Or: choco install golang
```

Pour `claudecli`, installez Claude Code depuis https://claude.ai/download.

<aside class="admonition" data-type="warning"><span class="admonition-title">Note Windows</span><p>Certains paquets de transport appellent des sous-processus (<code>signal-cli</code>) ou ouvrent des chemins spécifiques à l'OS (<code>~/.local/share/</code>). Les transports <code>whatsapp</code>, <code>slack</code>, <code>discord</code>, <code>telegram</code>, <code>matrix</code>, <code>email</code>, <code>sms</code> sont tous multiplateformes. <code>signal</code> et <code>imessage</code> nécessitent leurs outils hôtes respectifs.</p></aside>

  </div>
</div>

## 2. Configurer votre LLM

La configuration se trouve à `~/.config/rousseau/config.yaml` (surchargeable avec `--config`) et chaque champ est défini dans `internal/config/config.go`. Le provider par défaut est `claudecli`, qui délègue à votre CLI `claude` locale afin qu'aucune clé API ne quitte votre machine.

### claudecli (par défaut, sans clés)

Si vous avez déjà Claude Code (`claude`) installé et authentifié, c'est terminé. Rousseau hérite de sa session OAuth :

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

Voir [Providers : claudecli](/fr/providers/claudecli/).

### API Anthropic

Anthropic direct. Utilise le SDK officiel `anthropic-sdk-go` dans `internal/llm/anthropic/client.go` :

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` est lue directement depuis l'environnement (voir `config.Load` dans `internal/config/config.go`) ; la clé n'a jamais besoin d'être présente sur le disque. Voir [Providers : Anthropic](/fr/providers/anthropic/).

### AWS Bedrock

Utilise la chaîne d'identifiants AWS standard (profil, IMDS, IRSA). La région et le modèle proviennent de `BedrockConfig` dans `internal/config/config.go` :

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

Aucune clé API dans `config.yaml`. Voir [Providers : Bedrock](/fr/providers/bedrock/).

### Google Vertex AI

Anthropic sur Vertex ; lit un fichier JSON de compte de service. Champs de configuration définis dans `VertexConfig` :

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

Voir [Providers : Vertex](/fr/providers/vertex/).

### Compatible OpenAI (OpenRouter, Ollama, vLLM, LM Studio)

Les noms de providers `openai`, `openrouter` et `ollama` partagent `OpenAIConfig`. Les URL de base pour OpenRouter et Ollama ont des valeurs par défaut dans `setDefaults` (`https://openrouter.ai/api/v1` et `http://localhost:11434/v1`) ; tout le reste atterrit dans le bloc `openai` avec un `base_url` explicite :

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

Voir [Providers : Compatible OpenAI](/fr/providers/openai-compatible/) et [Guides : vLLM auto-hébergé](/fr/guides/self-hosted-vllm/).

## 3. Tenir votre première conversation

```sh
rousseau chat
```

Vous verrez une TUI Bubble Tea (`internal/tui/model.go`) :

- Un **viewport** en haut fait défiler la transcription. Le texte de l'assistant s'affiche en flux à mesure qu'il arrive.
- Une **zone de texte** en bas prend votre saisie. Appuyez sur `Entrée` pour envoyer, `Ctrl+C` pour quitter.
- Un **spinner** s'affiche pendant les tours du LLM ; un petit indicateur de streaming apparaît lorsque les tokens arrivent.
- Chaque tour est persisté dans SQLite à `~/.local/share/rousseau/sessions.db`. La journalisation WAL est activée par `Open()` dans `internal/state/sqlite/store.go`, donc vous pouvez exécuter en toute sécurité d'autres commandes rousseau (`rousseau session list`, `rousseau mcp`) sur la même base de données pendant que la TUI est ouverte.

Commencez par demander quelque chose de petit — par exemple « lister les fichiers sous `internal/tools/builtin` » — et rousseau appellera les outils intégrés `read`, `grep`, `edit`, `write` ou `bash` (`internal/tools/builtin/*.go`) selon les besoins. Voir [Guide utilisateur : TUI](/fr/user-guide/tui/) pour les raccourcis clavier et [Guide utilisateur : Outils](/fr/user-guide/tools/) pour les schémas.

Emplacement pour capture d'écran : la TUI affiche une barre de statut sur deux lignes (id de session et provider), le viewport avec les messages assistant + utilisateur teintés de couleur, et la zone de texte au focus en bas.

## 4. Ajouter un transport (WhatsApp)

WhatsApp est le transport de référence car l'appairage y est le plus strict. Tous les autres transports (`slack`, `discord`, `telegram`, `matrix`, `signal`, `sms`, `imessage`, `email`) suivent la même forme.

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Au premier lancement, `rousseau` affiche un QR code sur stdout. Scannez-le dans **WhatsApp > Paramètres > Appareils liés** sur votre téléphone. Le client whatsmeow (`internal/transport/whatsapp/client.go`) émet trois événements de log structurés :

- `whatsapp.qr_ready` — le QR a été rendu.
- `whatsapp.paired` — le téléphone a accepté le QR.
- `whatsapp.connected` — le websocket vers Meta est actif.

Les identifiants de l'appareil sont mis en cache à `~/.local/share/rousseau/whatsapp.db` (une base SQLite séparée, de sorte que réappairer un appareil ne touche pas l'historique des conversations). Le flag `--allow` fixe une allowlist de JID E.164 ; tout autre expéditeur est silencieusement rejeté par `router.transport.rejected`.

Rousseau utilise le protocole WhatsApp Web **non officiel**. Meta bannit occasionnellement les numéros exécutant des clients non officiels — ne l'exécutez pas sur un numéro dont vous dépendez. Voir [Transports : WhatsApp](/fr/transports/whatsapp/) pour l'analyse de risque.

## 5. Vérifier la chaîne d'approvisionnement

Chaque release taguée livre :

| Artefact | Objectif |
|---|---|
| `rousseau_<v>_checksums.txt` | SHA-256 de chaque archive de la release. |
| `rousseau_<v>_checksums.txt.sig` | Signature cosign (keyless, OIDC émise depuis GitHub Actions). |
| `rousseau_<v>_sbom.cdx.json` | SBOM CycloneDX 1.5 du graphe de modules Go. |
| `rousseau_<v>_provenance.intoto.jsonl` | Attestation de provenance SLSA-3. |

Vérifiez l'identité de la signature avant de faire confiance aux sommes de contrôle :

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

Le `--certificate-identity-regexp` fixe l'identité du signataire au dépôt rousseau-agent sous l'espace de noms de Sebastien. **Ne l'affaiblissez pas.** Une identité générique annule l'intérêt de la signature keyless.

Une fois la signature vérifiée, `sha256sum -c` prouve que le tarball téléchargé est bien celui que la CI a construit. Lisez le SBOM avec `cyclonedx-cli tree`, vérifiez la provenance SLSA-3 avec `slsa-verifier verify-artifact`, et seulement ensuite extrayez l'archive.

Voir [Sécurité](/fr/security/) pour l'ensemble des frontières de confiance et [Guides : Onboarding entreprise](/fr/guides/enterprise-onboarding/) pour la checklist de l'équipe plateforme.

## Dépannage

<aside class="admonition" data-type="tip"><span class="admonition-title">Premier arrêt recommandé</span><p>Exécutez <code>rousseau doctor</code> avant d'ouvrir un ticket. Il sollicite chaque sous-système — auth du provider, magasin d'état, identifiants de transport — et affiche des lignes structurées pass/warn/fail.</p></aside>

### `rousseau version` affiche « dev » après `go install`

Les valeurs `version`, `commit` et `buildDate` sont estampillées par la chaîne d'outils de release via `-ldflags` dans `internal/cli/root.go`. `go install` ignore ces flags, donc le binaire rapporte `dev / none / unknown`. Utilisez la voie de release signée si vous avez besoin d'une chaîne de version stable ; la chaîne `dev` est sans conséquence à l'exécution.

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` délègue au binaire `claude`. Soit vous mettez Claude Code dans votre `$PATH` (voir [Providers : claudecli](/fr/providers/claudecli/)), soit vous changez de provider — l'alternative la plus rapide est `provider: anthropic` avec `ANTHROPIC_API_KEY` exportée.

### Le QR WhatsApp s'affiche mais n'est jamais accepté

Trois causes courantes : (1) l'horloge du conteneur a un décalage supérieur à 30 secondes — le handshake WhatsApp est sensible au temps ; (2) un appairage partiellement complété a laissé `whatsapp.db` dans un état inutilisable — supprimez `~/.local/share/rousseau/whatsapp.db` et rescannez ; (3) Meta a invalidé le numéro — essayez un nouveau numéro de téléphone. Voir [Transports : WhatsApp](/fr/transports/whatsapp/).

### `cosign verify-blob` renvoie l'erreur « no matching signatures »

Le `--certificate-identity-regexp` doit correspondre au dépôt GitHub du signataire. Pour rousseau-agent, la valeur correcte est `sebastienrousseau/rousseau-agent`. Un wildcard annule l'intérêt de la signature keyless — ne l'affaiblissez pas. Si la regex est correcte, rafraîchissez la racine de confiance Sigstore avec `cosign initialize`.

### Chaque appel d'outil est refusé avec « denied by pattern policy »

Vous fonctionnez en mode `pattern` avec `default: deny` et aucune règle d'autorisation correspondante. Ajoutez une entrée d'autorisation pour l'outil, ou basculez `default: allow` et ajoutez plutôt des règles de refus ciblées. Voir [Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/) pour des exemples traités.

## Pages liées

- [Démarrage : Installation](/fr/getting-started/installation/) — chaque méthode d'installation avec la recette de vérification.
- [Démarrage : Premier transport](/fr/getting-started/first-transport/) — parcours de bout en bout WhatsApp/Slack/Discord.
- [Configuration](/fr/configuration/) — chaque bouton dans `~/.config/rousseau/config.yaml`.
- [Concepts](/fr/concepts/) — la boucle de l'agent, le magasin de sessions, MCP, cron, skills.
- [Dépannage](/fr/troubleshooting/) — le catalogue complet des modes de défaillance.

## Lectures complémentaires

- `README.md` — positionnement au niveau du dépôt et matrice des capacités.
- `SECURITY.md` — frontières de confiance et durcissement de la chaîne d'approvisionnement.
- `internal/config/config.go` — la struct de config faisant autorité.
- `internal/cli/root.go` — câblage de l'arborescence de commandes Cobra.

## Étapes suivantes

| Où aller | Pourquoi |
|---|---|
| [Configuration](/fr/configuration/) | Chaque bouton dans `~/.config/rousseau/config.yaml` avec les valeurs par défaut. |
| [Concepts](/fr/concepts/) | La boucle de l'agent, le magasin de sessions, MCP, cron, skills. |
| [Déploiement](/fr/deployment/) | Podman rootless + unité Quadlet systemd. |
| [Sécurité](/fr/security/) | Frontières de confiance, provenance SLSA-3, posture seccomp. |
| [Tutoriels](/fr/tutorials/) | Parcours complets de bout en bout. |
| [Référence](/fr/reference/cli-commands/) | Chaque flag CLI, code de sortie et champ de config. |
