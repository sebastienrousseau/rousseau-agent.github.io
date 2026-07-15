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
description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "Référence : magasin de sessions"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence : magasin de sessions"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Référence : magasin de sessions"
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
twitter_description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence : magasin de sessions"
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

## Emplacement et pilote

Le magasin de sessions est une base SQLite unique à `state.path` (défaut : `~/.local/share/rousseau/sessions.db`, voir `internal/config/config.go` `setDefaults`).

Rousseau utilise `modernc.org/sqlite` — un pilote SQLite pur Go. Il n'y a **aucune dépendance CGO ou libsqlite3**. Le binaire Go dans `bin/rousseau` est entièrement statique.

`Open()` dans `internal/state/sqlite/store.go` applique quatre pragmas à chaque ouverture :

| PRAGMA | Objectif |
|---|---|
| `journal_mode=WAL` | Write-ahead logging. Autorise les lecteurs concurrents, permet des sauvegardes à chaud sûres. |
| `foreign_keys=ON` | Garantie d'intégrité standard. |
| `busy_timeout=15000` | Attente de 15 secondes en cas de contention de verrou — critique dès que plusieurs transports écrivent en parallèle. |
| — | `EnsureSearch` s'exécute ensuite pour installer le schéma FTS5. |

Le magasin est ouvert une fois par processus. Plusieurs démons pointant vers le même fichier DB sont supportés grâce à la combinaison busy-timeout + WAL — le pont WhatsApp, `rousseau mcp` et `rousseau session list` peuvent partager le fichier en toute sécurité.

## Tour du schéma

### Table : `sessions`

Définie dans `internal/state/sqlite/schema.sql` :

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    payload        TEXT NOT NULL,        -- JSON blob of the full agent.Session
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
    ON sessions(updated_at DESC);
```

**Forme du payload.** La colonne `payload` stocke le JSON complet de `agent.Session` — rôles, blocs de contenu, blocs tool-use et tool-result, horodatages. Voir `Save`/`Load` dans `internal/state/sqlite/store.go`. Garder toute la session comme un seul blob JSON rend les migrations de schéma rares ; les requêtes sur les internes passent par l'index FTS5 ci-dessous.

**Les horodatages** sont ISO-8601 avec précision milliseconde (`2006-01-02T15:04:05.000Z` en syntaxe de temps Go), UTC.

**Ordonnancement.** `idx_sessions_updated_at` alimente `List` et `RecentSessions` (tous deux dans `store.go` / `search.go`).

### Table virtuelle : `sessions_fts` (FTS5)

Installée par `searchSchema` dans `internal/state/sqlite/search.go` :

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

Trois écritures pilotées par triggers la maintiennent cohérente avec `sessions` :

- `sessions_fts_ai` — après INSERT sur `sessions`, miroir de la ligne.
- `sessions_fts_au` — après UPDATE, suppression + réinsertion.
- `sessions_fts_ad` — après DELETE, suppression de la ligne FTS.

**Backfill.** `EnsureSearch` exécute un `LEFT JOIN` à chaque `Open()` pour insérer les lignes `sessions` que l'index FTS ne contient pas déjà. Cela rend l'index sûr à ajouter à une base existante — pas de migration manuelle.

**Tokenisation.** `porter unicode61` — stemmer Porter + casefolding Unicode. Insensible à la casse, gère la morphologie anglaise (`retry`/`retries`/`retried`).

**Classement.** `Search()` ordonne par `bm25(sessions_fts)` (plus bas = plus pertinent). `SearchHit.Rank` l'expose.

**Syntaxe de requête.** Passée à FTS5 verbatim. Voir [Tutoriel : exposer les outils via MCP](/fr/tutorials/expose-tools-via-mcp/) pour l'aide-mémoire opérateur.

### Table : `jid_sessions`

Persiste les correspondances émetteur-plateforme → identifiant de session ; installée par `NewJIDMap` dans `internal/state/sqlite/jidmap.go` :

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

Chaque transport longue durée utilise la JID map pour que le même numéro de téléphone, utilisateur Matrix ou utilisateur Slack reprenne la même conversation entre redémarrages. `Router.Handle` (`internal/transport/router.go`) la consulte en entrée ; `Put` l'écrit après `Save`.

L'espace JID est spécifique au transport — `447900123456@s.whatsapp.net` pour WhatsApp, `@user:matrix.org` pour Matrix, `U01ABC…` pour Slack. Le transport est responsable de la canonisation.

### Table : `cron_jobs`

Installée par `NewCronStore` dans `internal/state/sqlite/cron.go` :

```sql
CREATE TABLE IF NOT EXISTS cron_jobs (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    cron_expr   TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    deliver_to  TEXT NOT NULL,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL,
    last_run_at TEXT
);
```

`UNIQUE(name)` empêche les doublons. `rousseau cron add/list/remove/enable/disable` (depuis `internal/cli/cron.go`) font tous des allers-retours via cette table. Le planificateur dans `internal/cron/scheduler.go` la réconcilie à chaque `poll_interval`. MCP l'expose en lecture seule via `rousseau_cron_list`.

## Posture de concurrence

- **WAL** autorise un nombre illimité de lecteurs concurrents à côté d'un unique writer.
- **`busy_timeout=15000`** signifie qu'un writer qui rencontre de la contention attend jusqu'à 15 s plutôt que d'échouer rapidement. En pratique, le pont WhatsApp tient le rôle de writer tandis que `rousseau mcp` et `rousseau session list` sont des visiteurs en lecture seule.
- Le magasin n'est pas conçu pour la concurrence inter-machines. Deux hôtes écrivant dans le même fichier via NFS est un comportement indéfini — utilisez un unique writer et rsync la DB ailleurs pour des réplicas en lecture.

## Sauvegarde

L'approche la plus sûre est un `.backup` sqlite3 à chaud :

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` utilise l'API de sauvegarde en ligne de SQLite et fonctionne pendant que le primaire est en écriture. Les snapshots `restic` / `borg` sur le fichier brut sont également sûrs grâce au WAL — la sauvegarde obtient un snapshot cohérent au moment où le fichier est lu.

Le fichier `whatsapp.db` (identifiants d'appareil whatsmeow) est une base séparée ; sauvegardez-le de la même façon si vous voulez éviter de ré-appairer après une restauration.

## Reconstruire l'index FTS

Si l'index FTS5 se désynchronise (extrêmement rare — les triggers le maintiennent cohérent), reconstruisez-le :

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

L'`EnsureSearch` de rousseau ne défera pas cela ; les triggers reprennent simplement depuis un état propre.

## Voir aussi

- [Concepts](/fr/concepts/) — où se situe le magasin dans l'architecture globale.
- [Guide utilisateur : Compression + Rappel](/fr/user-guide/compression-recall/) — comment l'index FTS est exposé au modèle.
- [MCP : outils exposés](/fr/mcp/exposed-tools/) — la surface en lecture seule sur ce schéma.
- [Guides : gestion des espaces de travail](/fr/guides/managing-workspaces/) — partager / partitionner le magasin entre machines.
