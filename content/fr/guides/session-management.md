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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "Guide : gestion des sessions"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : gestion des sessions"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : gestion des sessions"
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
twitter_description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : gestion des sessions"
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

## Cycle de vie d'une session

Une session est une valeur `agent.Session` persistée comme ligne de la table `sessions` (`internal/state/sqlite/schema.sql`). Elle a un `id`, un `title`, une tranche ordonnée chronologiquement de valeurs `Message`, et des horodatages. Une fois créée, elle existe jusqu'à ce que vous la supprimiez.

Les sessions sont créées à la demande par chaque point d'entrée :

- `rousseau chat` — une session par session TUI (une nouvelle à chaque invocation `chat` ; il faudrait construire un sélecteur de session pour en réutiliser une existante).
- Chaque transport (`whatsapp`, `slack`, …) — une session par JID, via la table JID (`internal/state/sqlite/jidmap.go`).
- `rousseau cron` — chaque déclenchement est une session one-shot bornée à cette exécution.

## Énumérer

```sh
rousseau session list --limit 10
```

Sortie (depuis `newSessionListCmd` dans `internal/cli/session.go`) :

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` renvoie un nombre illimité de lignes.

## Rechercher

FTS5 sur chaque message enregistré :

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # préfixe
```

La commande enveloppe `Store.Search` (`internal/state/sqlite/search.go`) avec `SearchOptions{Limit: N}`. Le classement est BM25 ; les extraits sont tronqués à ~200 caractères.

## Afficher

```sh
rousseau session show <session-id>
```

Affiche la transcription complète avec des marqueurs `→ tool_use(name, input)` et `← tool_result` entre les messages assistants. Utile pour auditer la session d'un démon non-supervisé.

## Supprimer

```sh
rousseau session delete <session-id> --yes
```

Le flag `--yes` est requis (`newSessionDeleteCmd`). La suppression cascade via les triggers FTS5 afin que l'index de recall reste cohérent.

## Déclenchement de la compression

Quand `agent.compression.enabled: true` dans `config.yaml`, le `LLMCompressor` (`internal/agent/compressor.go`) vérifie deux conditions avant chaque tour :

- `len(s.Messages) >= trigger_messages` (60 par défaut).
- `len(s.Messages) > keep_recent` (8 par défaut).

Si les deux sont vraies, le compresseur résume la tranche la plus ancienne en un unique message utilisateur synthétique préfixé du marqueur `[rousseau-compressed]`, puis garde tels quels les `keep_recent` derniers messages. La session réécrite remplace l'originale en mémoire et est persistée au prochain `Store.Save`.

Une deuxième compression sur une session déjà compressée est sautée sauf si la session a atteint plus de `2 * trigger_messages` — cela borne une croissance galopante sans payer pour re-résumer à chaque tour.

Ligne de log :

```
INFO agent.compressed messages=68
```

## Restauration

Les sessions se restaurent automatiquement. Le routeur de transport (`internal/transport/router.go`) recherche la cartographie JID → id de session à l'entrée, puis `Store.Load` désérialise la charge utile JSON en une `agent.Session`. Aucune étape manuelle.

Si une cartographie est périmée — l'id de session existe dans `jid_sessions` mais pas dans `sessions` — vous verrez `router.stale_mapping` (WARN), et le routeur crée une session neuve. Artefact hérité d'une suppression partielle ; sans risque à ignorer.

## Restauration manuelle depuis une sauvegarde

Pour restaurer l'ensemble du magasin de sessions depuis un snapshot `.backup` :

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

Les fichiers `-wal` et `-shm` doivent être supprimés à côté du primaire ; SQLite les reconstruit à la prochaine ouverture.

## Suppression en masse par âge

Il n'existe pas de CLI intégrée « supprimer les sessions de plus de X ». Supprimez via SQLite :

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Les triggers FTS5 maintiennent la cohérence de l'index de recall.

## Préserver la confidentialité

Comme le contenu de session est stocké en clair dans un blob JSON, traitez `sessions.db` comme sensible. Options :

- **Chiffrement au niveau système de fichiers.** LUKS sous Linux, FileVault sous macOS.
- **Sauvegardes chiffrées.** `restic` et `borg` chiffrent tous deux au repos.
- **Suppression à la fin pour les sessions one-shot.** Pour les démons pilotés par cron, un hook post-run pourrait faire `rousseau session delete` sur l'id de la session qui vient de se terminer. Non intégré aujourd'hui ; voir [Guides: Enterprise Onboarding](/fr/guides/enterprise-onboarding/) pour la revue.

## Référence complète des commandes `rousseau session`

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Session subcommand">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Liste les sessions, plus récentes d'abord :

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

Colonnes : `ID`, `Title`, `Messages`, `UpdatedAt`. Le flag `--json` émet un objet par ligne pour les consommateurs scriptés.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Affiche la transcription complète d'une session :

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` affiche le JSON tel que stocké (utile pour le débogage). Sans `--raw`, les appels d'outils s'affichent comme `→ tool_use(name, input)` et les résultats comme `← tool_result`.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Recherche plein texte sur chaque session :

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

Utilise l'index FTS5 (voir `internal/state/sqlite/`). Les résultats sont classés par pertinence et incluent un extrait avec les termes correspondants mis en évidence.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Supprime une session et ses entrées FTS5 :

```sh
rousseau session delete <session-id> --yes
```

Le flag `--yes` est requis — pas de confirmation interactive. La suppression cascade via les triggers SQL pour maintenir la cohérence de l'index de recall.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Exporte une session en JSON :

```sh
rousseau session export <session-id> > session.json
```

Le format exporté correspond au blob JSON sur disque ; la ré-importation n'est pas encore supportée (feuille de route).

  </div>
</div>

## Dépannage

### `session not found`

L'ID que vous avez passé n'existe pas. Sensible à la casse. Utilisez `rousseau session list` pour voir les IDs valides.

### La recherche FTS5 ne renvoie rien

L'index peut être obsolète sur des sessions héritées importées avant que FTS5 ne soit câblé. Reconstruisez en exécutant toute opération de mutation de contenu (une suppression déclenche une réindexation), ou réindexez manuellement via SQLite.

### `database is locked` en lecture

Un autre démon tient un verrou d'écriture WAL. Utilisez un DSN en lecture seule (`?mode=ro`) si vous n'avez besoin que de lire.

### Le magasin de sessions grossit trop vite

Activez la compression (`agent.compression.enabled: true`) et exécutez périodiquement `VACUUM` sur le fichier SQLite pour récupérer de l'espace.

### La restauration depuis une sauvegarde produit un état périmé

Assurez-vous d'avoir supprimé `-wal` et `-shm` avant de démarrer le démon. SQLite rejouera le WAL si `-wal` est présent, annulant potentiellement votre restauration.

## Pages liées

- [Reference: Session store](/fr/reference/session-store/) — schéma et DDL.
- [Guides: Managing workspaces](/fr/guides/managing-workspaces/) — magasins par workspace.
- [Guides: Context management](/fr/guides/context-management/) — comment la compression décide ce qu'elle garde.
- [User Guide: CLI](/fr/user-guide/cli/) — signatures des commandes.
- [User Guide: Compression &amp; Recall](/fr/user-guide/compression-recall/) — internes du compresseur et du recall FTS5.

## Lecture complémentaire

- `internal/cli/session.go` — câblage CLI.
- `internal/state/sqlite/store.go` — DSN, WAL, index.
- `internal/agent/session.go` — la structure `Session`.
- `internal/agent/compressor.go` — `LLMCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall`.
