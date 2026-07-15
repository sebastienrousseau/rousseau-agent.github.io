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
description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
keywords: "update, upgrade, go install, container tag, config migration, minor version"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "Atualização"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Atualização"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Atualização"
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
twitter_description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Atualização"
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

## Política de versionamento

O rousseau segue [Semantic Versioning](https://semver.org):

| Bump | O que muda |
|---|---|
| Patch (`0.1.2 → 0.1.3`) | Correções de bugs, correções de segurança, bumps de dependência. Sem mudanças de config ou formato em disco. |
| Minor (`0.1.x → 0.2.0`) | Novas features. Adições de config são sempre não quebradoras; se um campo for removido, um fallback com alias cobre pelo menos uma versão minor. |
| Major (`0.x → 1.0`) | Mudanças quebradoras. Requer uma receita de migração documentada no [changelog](/pt-BR/changelog/). |

A [política em SECURITY.md](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) é explícita: apenas `main` e a release com tag mais recente recebem correções de segurança. Não há branch de suporte de longo prazo.

## Método de atualização por caminho de instalação

### Arquivo de release assinada

```sh
VERSION=<new-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

Verificação não é opcional. Cada release traz uma nova assinatura cosign; pular a checagem anula a postura de cadeia de suprimentos.

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Para fixar uma tag exata:

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

`$GOBIN` (tipicamente `~/go/bin`) precisa estar no `$PATH` antes de `/usr/local/bin` se você quiser que o binário novo tenha precedência.

### Imagem de contêiner

Mude a tag da referência da imagem e reinicie o serviço systemd. Se você usa a unidade Quadlet de referência:

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Fixar em `:latest` é inseguro em uma implantação consciente da cadeia de suprimentos — sempre fixe uma tag imutável (`:v0.4.2`) e verifique o digest da imagem contra as notas de release.

### A partir do código-fonte

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # runs the full CI gate locally
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` é o mesmo gate de 18 linters + race + govulncheck que o CI impõe — uma passagem local garante que o job de build reprodutível também passará.

## Migração de config

Mudanças de schema de config são documentadas no [changelog](/pt-BR/changelog/) para cada versão minor. Os defaults do Viper mantêm chaves antigas funcionando por um ciclo minor; o padrão a seguir se aplica:

- **Chave nova adicionada**: recebe um default que preserva o comportamento anterior. Nenhuma ação necessária.
- **Chave renomeada**: a chave antiga tem alias por uma versão minor. Um warning é logado quando o alias é acessado.
- **Chave removida**: um erro de fail-fast é emitido no load. O changelog nomeia o substituto.

Para fazer um dry-run de uma config contra um binário novo:

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` percorre cada dependência de runtime e cada escolha de config; uma linha `fail` mostra exatamente qual chave precisa de atenção.

## Compatibilidade do session-store

`~/.local/share/rousseau/sessions.db` usa SQLite com schema versionado. Migrações de schema são aditivas e idempotentes — o daemon executa `CREATE TABLE IF NOT EXISTS` e `ALTER TABLE ADD COLUMN` no startup. **Nunca faça downgrade** através de uma versão minor depois que o novo schema já rodou; o SQLite não remove colunas automaticamente, mas o código de aplicação assume a presença delas.

Se você precisa de uma base limpa:

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

O daemon recria o store no próximo start. As credenciais de dispositivo do WhatsApp são armazenadas separadamente em `whatsapp.db`, então um reset do session-store não força repareamento.

## Compatibilidade do WhatsApp store

`whatsapp.db` (o device store do whatsmeow) é separado do session store precisamente para que uma migração de schema de sessão não inutilize o pareamento do WhatsApp. Se o próprio whatsmeow muda o formato em disco em um upgrade do rousseau, o changelog sinaliza e o caminho de recuperação é: deletar `whatsapp.db`, reiniciar, re-escanear o QR.

## Rollback

- **Arquivo de release assinada / `go install`**: reinstale a tag anterior usando a mesma receita.
- **Contêiner**: mude a tag da imagem de volta e reinicie.
- **A partir do código-fonte**: `git checkout <old-tag> && make build`.

Rollbacks são seguros enquanto o schema do session-store na versão mais antiga for um superset do que a versão mais nova escreveu. Na prática isso é sempre verdade dentro de uma mesma série minor e geralmente verdade entre minors adjacentes. Upgrades major trazem uma receita de migração com um aviso explícito de rollback no changelog.

## Próximo

- [Changelog](/pt-BR/changelog/) — detalhamento release a release.
- [Solução de problemas](/pt-BR/troubleshooting/) — se `rousseau doctor` mostrar uma linha `fail`.
