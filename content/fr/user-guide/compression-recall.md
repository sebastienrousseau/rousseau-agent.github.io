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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "Compression + rappel"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Compression + rappel"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Compression + rappel"
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
twitter_description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Compression + rappel"
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

## Deux problèmes, deux mécanismes

- Une longue session unique peut dépasser la fenêtre de contexte du modèle. La **compression** replie les messages anciens en un bloc de résumé pour que la boucle continue de fonctionner.
- Une nouvelle session sur un sujet apparenté perd la valeur des conversations antérieures. Le **rappel** (recall) interroge l'index FTS5 sur l'ensemble des sessions et insère des extraits dans le prompt système.

La compression modifie la session courante sur place. Le rappel ne modifie jamais — il ajoute du contexte au prompt système pour le tour courant.

## Compression

`internal/agent/compressor.go` implémente un résumeur adossé au LLM. La boucle d'agent le consulte au début de chaque `Turn` :

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

Si la session est courte, il ne se passe rien. Une fois que le nombre de messages franchit `trigger_messages`, le compresseur :

1. Isole la queue de la session — les `keep_recent` messages les plus récents — et les préserve verbatim.
2. Envoie tout ce qui est plus ancien au fournisseur avec un prompt de résumé.
3. Remplace le bloc plus ancien par un unique message `RoleSystem` synthétique contenant le résumé.
4. Marque la session pour que le bloc de résumé se retrouve dans le préfixe éligible au cache de prompt lors du prochain appel au fournisseur.

La boucle continue ensuite contre la liste de messages plus courte. L'utilisateur ne voit jamais la couture.

### Activer la compression

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # zéro → défaut 60
    keep_recent: 8            # zéro → défaut 8
    prompt: ""                # zéro → défaut raisonnable
```

| Champ | Défaut | Signification |
|---|---|---|
| `enabled` | `false` | Désactivé par défaut. |
| `trigger_messages` | 60 | Nombre de messages au-dessus duquel la compression se déclenche. |
| `keep_recent` | 8 | Combien de messages récents préserver verbatim. |
| `prompt` | intégré | Surcharge l'instruction de résumé. |

### Quand la laisser désactivée

La compression consomme un aller-retour fournisseur par déclenchement. Sur un compte `claudecli` avec abonnement, ce trajet est gratuit — activez librement. Sur une API tarifée au jeton, chaque déclenchement a un coût, donc augmentez `trigger_messages` ou laissez-la désactivée pour les sessions courtes.

### Quand la laisser active

- Démons de transport chat longue durée où un fil WhatsApp grandit sur des semaines.
- Prompts planifiés par cron dont les réponses alimentent un prompt de suivi.
- Fournisseurs auto-hébergés où le coût par jeton est nul.

### Sémantique préservée à travers la compression

- Les paires tool-use / tool-result ne sont jamais séparées. Si un `tool_use` est dans la région compressée et son `tool_result` dans la région préservée, les deux sont repliés dans le résumé.
- Le compresseur ne réécrit jamais le tour utilisateur en cours de vol.
- La mise en cache de prompt (marqueurs `cache_control` d'`internal/llm/anthropic`) est placée sur le bloc de résumé afin que le prochain appel le lise depuis le cache.

## Rappel

`internal/state/sqlite/` maintient une table virtuelle FTS5 indexant chaque message. Un `RecallProvider` exécute une requête contre cette table et renvoie un appendice de prompt système.

### L'interface

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

La boucle d'agent l'appelle une fois par itération. Quand elle retourne du texte non vide, ce texte est ajouté au prompt système de base pour cette itération.

### Le fournisseur par défaut

`internal/agent/recall.go` livre une heuristique qui :

1. Extrait les jetons saillants du dernier message utilisateur de la session courante.
2. Exécute `MATCH` sur l'index FTS5 pour ces jetons à travers les autres sessions.
3. Formate les N meilleurs extraits en un bloc `Previously in another session:`.
4. Borne l'appendice pour qu'il n'excède jamais un budget en caractères configuré.

### Activer le rappel

Le rappel est câblé à la construction de l'agent. Voir `internal/cli/chat.go` et `internal/cli/*.go` pour la façon dont chaque transport le câble. Dans votre propre intégration :

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### Interaction avec l'approbateur

Le rappel lit depuis le magasin de sessions ; il ne déclenche jamais d'appel d'outil. L'approbateur n'est pas consulté. Le contenu du magasin lui-même constitue la frontière de confiance.

### Recherche de session depuis la CLI

Le rappel est une fonctionnalité orientée machine. Pour les humains, le même index FTS5 alimente :

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

Même moteur de requête, mêmes résultats, moins le re-ranking LLM qu'un vrai RecallProvider peut ajouter.

## Interaction avec les skills

Les skills ([Skills](/fr/skills/)) et le rappel ajoutent tous deux au prompt système. Ils sont composés dans un ordre fixe :

1. Prompt système de base (depuis `agent.system_prompt` ou le défaut).
2. Appendice des skills (le cas échéant).
3. Appendice de rappel (le cas échéant).

Tout est séparé par deux retours à la ligne. Si rien n'a besoin d'être ajouté, le prompt de base passe inchangé.

## Sémantique du bloc de résumé

Le message de résumé synthétique est émis avec `RoleSystem`. Ce n'est ni un message utilisateur ni un message assistant, donc il n'apparaît jamais dans `rousseau session show` comme un tour conversationnel — il apparaît comme métadonnée `[compressed summary]`.

Si vous reprenez une session compressée avec `rousseau chat --session <id>`, le résumé est préservé. Supprimer le bloc de résumé via une hypothétique édition de schéma n'est pas sûr : le modèle peut référencer des faits uniquement connus à travers lui.

## Vérifier que la compression se déclenche

```
INFO agent.compressed messages=12
```

`messages` est la nouvelle longueur de session après que le bloc de résumé a remplacé le préfixe compressé. Un `WARN agent.compress_failed err=...` signifie que le fournisseur de résumé a erré ; la boucle a continué contre la session non compressée.

## Précautions

- La compression est destructrice. Le résumé est du texte généré par modèle ; des détails importants peuvent être perdus. Pour les pistes d'audit, conservez la session complète dans le magasin — la compression n'affecte que ce que le modèle voit, pas ce que SQLite persiste.
- Le rappel nécessite l'extension SQLite FTS5. `modernc.org/sqlite` l'intègre par défaut ; si vous remplacez l'implémentation du magasin, assurez-vous que FTS5 est disponible.
- Les deux fonctionnalités supposent du texte UTF-8. Les transcriptions de notes vocales (voir [Mode vocal](/fr/user-guide/voice-mode/)) comptent comme des messages utilisateur ordinaires une fois transcrites.

## Suite

- [Concepts](/fr/concepts/) — vue d'ensemble de la boucle d'agent.
- [Configuration](/fr/configuration/) — chaque bouton `agent.compression.*`.
- [Skills](/fr/skills/) — la troisième entrée de prompt système.
