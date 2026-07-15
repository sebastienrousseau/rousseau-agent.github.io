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
changefreq: "monthly"
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "Fournisseur claudecli"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fournisseur claudecli"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fournisseur claudecli"
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
twitter_description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Fournisseur claudecli"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Comment le fournisseur <code>claudecli</code> hérite de l'authentification depuis votre Claude Code installé localement, la matrice complète de <code>PermissionMode</code>, la sémantique de corrélation de session, les alias de modèles, et quand le préférer à l'API Anthropic directe. Lisez <code>internal/llm/claudecli/client.go</code> en parallèle de cette page pour la source faisant foi.</p></aside>

## Quand utiliser claudecli

`claudecli` lance en sous-processus la CLI `claude` (Claude Code). C'est le **fournisseur par défaut** et le bon choix quand :

- Vous avez déjà Claude Code installé et authentifié localement.
- Vous voulez réutiliser un compte Claude Code d'abonnement plutôt que de plomber des clés API.
- Vous voulez que le modèle s'exécute dans la boucle tool-use propre à `claude` (ses fonctionnalités d'édition, de thinking et de plan mode restent intactes).
- Vous voulez zéro secret dans le fichier de configuration de rousseau.

Le compromis : le `Registry` d'outils de rousseau n'est **pas** invoqué pour ce fournisseur — `claude` exécute ses propres outils dans le sous-processus. Les objets de réponse reviennent comme un unique message texte de fin de tour. Si vous avez besoin que rousseau filtre `bash`/`edit`/`write` via la politique d'approbation, utilisez plutôt `anthropic`, `bedrock`, `vertex` ou un fournisseur compatible OpenAI.

## Héritage de l'authentification

La CLI `claude` conserve l'authentification à trois endroits :

| Emplacement | Contenu |
|---|---|
| `~/.claude/` | Jetons OAuth (abonnement), sortie de l'aide API-key, config workspace. |
| Trousseau système | Sous macOS, `claude` peut mettre en cache les refresh tokens dans le keychain de session. |
| Variable `ANTHROPIC_API_KEY` | Si positionnée, `claude` l'utilise en mode API-key plutôt que OAuth. |

`claudecli` ne lit jamais ces sources directement. Chaque invocation est un `exec.CommandContext(binary, args...)` — le sous-processus hérite de l'environnement et du répertoire personnel du parent, et va chercher ses propres credentials. C'est ce qui le rend « zéro config » pour les opérateurs individuels.

<aside class="admonition" data-type="tip"><span class="admonition-title">Montages conteneur</span><p>Quand vous exécutez rousseau dans un conteneur, bind-montez <code>~/.claude</code> en lecture-écriture dans le conteneur pour que <code>claude</code> puisse rafraîchir sur place ses tokens OAuth mis en cache :</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

Le label `Z` est critique sur les hôtes SELinux ; voir [Déploiement](/fr/deployment/) pour l'unité Quadlet complète.

## Configuration

```yaml
provider: claudecli

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args:
    - --add-dir
    - /workspace
```

| Champ | Défaut | Effet |
|---|---|---|
| `binary` | `claude` | Exécutable résolu via `$PATH`. Pointez vers un chemin absolu si vous avez plusieurs versions de `claude`. |
| `model` | *vide* | Transmis en `--model <valeur>`. Vide, utilise le défaut de `claude`. |
| `permission_mode` | *vide* | Transmis en `--permission-mode <valeur>`. Voir tableau plus bas. |
| `extra_args` | `[]` | Placé avant `-p <prompt>` à chaque invocation. |

Chaque champ correspond à `ClaudeCLIConfig` dans `internal/config/config.go`. La ligne de commande du sous-processus, assemblée à chaque tour, est :

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Parsing du STDOUT</span><p>Rousseau attend que <code>claude</code> émette une enveloppe JSON sur stdout. Si vous encapsulez <code>claude</code> dans un script shell (pour audit, expurgation ou rate-limit), le wrapper doit transférer stdout sans modification. Le parser tolère une ligne de log initiale avant le premier <code>{</code> — voir <code>parseResult</code> dans <code>internal/llm/claudecli/client.go</code> — mais tout déchet après l'enveloppe JSON provoquera un échec.</p></aside>

## Matrice PermissionMode

Le flag `PermissionMode` reflète le `--permission-mode` propre à `claude`. Le sous-processus applique la valeur ; rousseau ne double pas la vérification.

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">Supervisé</button>
    <button role="tab" aria-selected="false">Non supervisé</button>
    <button role="tab" aria-selected="false">Lecture seule</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Sessions TUI interactives où un humain est devant le terminal et peut approuver les appels d'outils.

| Mode | Comportement |
|---|---|
| `default` | Claude Code demande interactivement à chaque appel d'outil. Idéal pour les sessions exploratoires. |
| `acceptEdits` | Les éditions de fichier passent sans invite ; les autres outils continuent de demander. Bien lorsqu'on fait confiance à la surface d'édition. |
| `auto` | Automatique selon l'outil. À utiliser quand vous voulez laisser l'heuristique intégrée de claude décider. |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Les transports de chat (WhatsApp, Slack, Discord, Signal, …) n'ont personne au terminal pour répondre aux invites.

| Mode | Comportement |
|---|---|
| `bypassPermissions` | Chaque appel d'outil s'exécute sans invite. Accepte tout le rayon d'impact. |
| `dontAsk` | Alias traité comme bypass. |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

La CLI positionne automatiquement `bypassPermissions` pour les daemons non supervisés si l'opérateur n'a rien précisé — voir `setUnattendedPermissionDefault` dans `internal/cli`.

<aside class="admonition" data-type="caution"><span class="admonition-title">Rayon d'impact</span><p><code>bypassPermissions</code> donne au modèle un accès <code>bash</code> direct avec les privilèges du daemon. Combinez-le avec (a) un conteneur durci, (b) une allowlist et (c) un approver en mode pattern côté rousseau — ou utilisez un fournisseur autre que <code>claudecli</code> qui permette à rousseau d'appliquer les approbations avant l'exécution.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Mode exploration pour de gros refactors ou des revues de code sans écriture.

| Mode | Comportement |
|---|---|
| `plan` | Mode planneur. Les lectures et grep sont autorisés ; les écritures sont inhibées. |

```yaml
claudecli:
  permission_mode: plan
```

Associez-le au mode lecture seule propre à rousseau (voir [Guides : Mode lecture seule](/fr/guides/read-only-mode/)) pour un durcissement en ceinture-et-bretelles.

  </div>
</div>

## Corrélation de session

`claudecli` maintient l'état conversationnel dans le sous-processus. Rousseau corrèle ses propres identifiants de session avec ceux de `claude` via deux flags :

- `claude -p --session-id <uuid>` crée une nouvelle session. Si l'UUID existe déjà, `claude` renvoie `already in use`.
- `claude -p --resume <uuid>` reprend une session existante. Si inconnue, `claude` échoue.

Rousseau choisit le flag via un `SessionCache` en mémoire (`InMemorySessionCache` par défaut). Sur un cache miss à froid où `claude` conserve encore l'état d'une exécution précédente de rousseau, le provider tente optimiste `--session-id`, attrape l'erreur `already in use`, puis retente avec `--resume`. Voir le commentaire de `(*Provider).Complete` dans `internal/llm/claudecli/client.go`.

Les appelants qui embarquent le provider peuvent brancher un cache persistant via `provider.WithCache(store)` — le store `state.sqlite` implémente la même interface et survit aux redémarrages, évitant l'aller-retour à froid au premier tour après un redémarrage.

## Alias de modèles

Les alias de modèles de `claude` sont honorés tels quels par le sous-processus :

| Alias | Pointe vers |
|---|---|
| `sonnet` | Le modèle par défaut du tier Sonnet en vigueur. |
| `opus` | Le modèle par défaut du tier Opus en vigueur. |
| `haiku` | Le modèle par défaut du tier Haiku en vigueur. |

Pour la reproductibilité à travers les redémarrages de daemon (benchmarks de skills, jobs cron, batch), figez un identifiant de modèle exact :

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">Les alias suivent les releases</span><p>Les alias évoluent quand Anthropic livre un nouveau modèle. L'alias <code>sonnet</code> en juillet 2026 ne pointe pas vers les mêmes poids qu'en avril 2026. Si votre workflow dépend d'un comportement précis, figez l'ID exact.</p></aside>

## Combiner avec les skills

`claudecli` envoie le system prompt via `--system-prompt` à la création de session. `claude` l'honore tel quel et ignore les `--system-prompt` suivants sur `--resume` — ce qui correspond à l'usage qu'en fait rousseau. La sortie du `SkillsProvider` est insérée avant l'invocation :

```
<agent.SystemPrompt>

<skill 1 markdown>

<skill 2 markdown>

<RecallProvider appendix>
```

Voir `systemPrompt()` dans `internal/agent/agent.go`. Les skills fonctionnent à l'identique pour chaque fournisseur ; la mécanique de composition se fait dans `agent.Agent`, pas dans le provider.

<aside class="admonition" data-type="tip"><span class="admonition-title">Cache de prompt</span><p>Le fournisseur Anthropic direct marque le system prompt pour le cache de prompt éphémère (voir <code>internal/llm/anthropic/cache.go</code>). <code>claudecli</code> ne le fait pas — <code>claude</code> gère son propre cache en interne. Si vous voulez des gains mesurables de cache de prompt, utilisez <code>provider: anthropic</code>.</p></aside>

## Points de vigilance

- **Pas de portabilité inter-provider.** Une session créée contre `claudecli` n'est pas portable vers `anthropic` — l'état côté modèle vit à l'intérieur de `claude`. Basculer de provider en cours force une nouvelle session.
- **Le registre d'outils n'est pas invoqué.** `bash`, `edit`, `write`, `grep`, `read` sont exécutés par `claude`, pas par `rousseau`. L'`agent.Approver` de rousseau ne peut pas filtrer ces appels. Utilisez un provider autre que `claudecli` si vous avez besoin d'une application d'approbation côté rousseau.
- **Portée de `--add-dir`.** Par défaut, `claude` refuse de lire hors de son workspace. Passez `--add-dir /workspace` (ou l'emplacement de vos sources) via `extra_args` pour élargir. Combinez avec la politique d'approbation de rousseau au niveau du transport si vous voulez compenser la perte de contrôle.
- **Streaming.** `claudecli` utilise `claude -p --output-format json` (non-streaming). Le chemin streaming dans `internal/llm/claudecli/stream.go` lit `--output-format stream-json` ; activez-le via `StreamingProvider` depuis une intégration embarquée.
- **Fuite d'environnement.** Le sous-processus hérite de toute variable d'environnement du parent. Si `ANTHROPIC_API_KEY` est positionnée dans l'environnement de rousseau, `claude` la préférera à l'OAuth en cache. C'est généralement acceptable, mais cela change la facturation.

## Dépannage

### `claudecli: run: exec: "claude": executable file not found in $PATH`

`claude` n'est pas sur `PATH` (ou l'image conteneur ne l'embarque pas). Deux correctifs :

1. Renseignez `claudecli.binary` avec un chemin absolu.
2. Ajoutez Claude Code à la couche de runtime du conteneur — le `docker/Dockerfile` de référence utilise `node:22-alpine` pour cette raison.

### `claudecli: model error: session id already in use`

Vous avez deux processus rousseau sur le même identifiant de session contre la même installation `claude`, ou le cache mémoire a perdu une session que `claude` mémorise encore. Le retry optimiste décrit plus haut couvre le deuxième cas ; le premier signifie que des daemons concurrents se marchent dessus.

### `claudecli: no JSON in output`

`claude` a émis du non-JSON sur stdout, ou s'est terminé avant l'enveloppe. Causes fréquentes : clé API invalide côté Claude Code, version de `claude` antérieure à `--output-format json`, ou wrapper shell écrivant des marqueurs de progression. Exécutez `claude -p --output-format json 'hello'` directement pour isoler.

### La réponse est coupée en pleine phrase

La sortie de `claude` est plafonnée par `--max-turns` et son budget interne de tokens. Rousseau ne positionne pas `--max-turns` ; si vous le faites via `extra_args`, augmentez-le. Pour de longues générations, envisagez un provider API direct où vous contrôlez `MaxTokens` depuis `internal/llm/anthropic/client.go`.

### Plan par abonnement rate-limité alors que l'API est fluide

La CLI `claude` en plan d'abonnement possède des limites cachées par conversation et par fenêtre. Si vous les atteignez, basculez sur `provider: anthropic` avec une clé API — l'API directe expose des limites explicites, publiées (voir [Guides : Limites de débit](/fr/guides/rate-limits/)).

## Pages liées

- [Fournisseurs : Anthropic](/fr/providers/anthropic/) — API directe avec cache de prompt et streaming.
- [Fournisseurs : Bedrock](/fr/providers/bedrock/) — Claude géré par AWS.
- [Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/) — comment filtrer les appels d'outils à la couche rousseau.
- [Skills](/fr/skills/) — comment est composé l'appendice du system prompt.
- [Configuration](/fr/configuration/) — la section `claudecli` en contexte.

## Pour aller plus loin

- `internal/llm/claudecli/client.go` — invocation du sous-processus, corrélation de session, parsing JSON.
- `internal/llm/claudecli/stream.go` — variante streaming en `--output-format stream-json`.
- `internal/config/config.go` — struct `ClaudeCLIConfig`.
- `internal/cli/root.go` — comment `setUnattendedPermissionDefault` choisit `bypassPermissions` pour les transports de chat.
