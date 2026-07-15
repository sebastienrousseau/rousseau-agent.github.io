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
hreflang: "zh-Hans"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "zh-Hans"
locale: "zh_CN"
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
permalink: "https://docs.rousseau-agent.dev/zh-Hans/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "升级"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "升级"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "升级"
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
twitter_title: "升级"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 版本策略

Rousseau 遵循 [Semantic Versioning](https://semver.org)：

| 版本变动 | 变化内容 |
|---|---|
| Patch（`0.1.2 → 0.1.3`） | Bug 修复、安全修复、依赖升级。无配置或落盘格式变更。 |
| Minor（`0.1.x → 0.2.0`） | 新功能。配置新增始终非破坏性；若字段被移除，别名回退至少覆盖一个次要版本。 |
| Major（`0.x → 1.0`） | 破坏性变更。需要在 [changelog](/zh-Hans/changelog/) 中提供已记录的迁移配方。 |

[SECURITY.md 策略](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) 表述明确：只有 `main` 与最近的打标签 release 会接收安全修复。没有长期支持分支。

## 按安装路径的更新方法

### 已签名的 release 归档

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

校验不是可选项。每次 release 都会附带全新的 cosign 签名；跳过校验会瓦解供应链姿态。

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

要固定一个精确 tag：

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

如果您想让新二进制优先生效，`$GOBIN`（通常为 `~/go/bin`）需要在 `$PATH` 中排在 `/usr/local/bin` 之前。

### 容器镜像

在镜像引用上滚动 tag，然后重启 systemd 服务。如果您使用参考 Quadlet 单元：

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

在关注供应链的部署中，固定到 `:latest` 是不安全的 —— 始终固定一个不可变的 tag（`:v0.4.2`），并对照 release notes 校验镜像 digest。

### 从源代码

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # 在本地运行完整的 CI 门禁
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` 与 CI 强制的 18-linter + race + govulncheck 门禁完全一致 —— 本地运行通过即保证可复现构建任务也会通过。

## 配置迁移

每个次要版本的配置 schema 变更都记录在 [changelog](/zh-Hans/changelog/) 中。Viper 的默认值可让旧键在一个次要周期内继续工作；适用如下模式：

- **新增键**：获得一个保留原行为的默认值。无需操作。
- **键重命名**：旧键别名保留一个次要版本。命中别名时会记录一条警告。
- **键移除**：加载时抛出快速失败错误。changelog 会命名替代项。

要用新二进制对配置进行 dry-run：

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` 会走查每个运行时依赖与每个配置选项；`fail` 行会准确指出哪个键需要关注。

## 会话存储兼容性

`~/.local/share/rousseau/sessions.db` 使用带版本 schema 的 SQLite。schema 迁移是累加的且幂等 —— 守护进程在启动时执行 `CREATE TABLE IF NOT EXISTS` 和 `ALTER TABLE ADD COLUMN`。一旦新 schema 已运行，**绝不要** 跨次要版本降级；SQLite 不会自动移除列，但应用代码假定它们存在。

如果您需要清空重来：

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

守护进程会在下次启动时重新创建存储。WhatsApp 设备凭据独立保存在 `whatsapp.db`，因此重置会话存储不会强制重新配对。

## WhatsApp 存储兼容性

`whatsapp.db`（whatsmeow 的设备存储）与会话存储分离，正是为了让会话 schema 迁移不会破坏 WhatsApp 配对。如果 whatsmeow 自身在 rousseau 升级时改变了落盘格式，changelog 会加以标注，恢复路径为：删除 `whatsapp.db`、重启、重新扫描 QR。

## 回滚

- **已签名 release 归档 / `go install`**：使用同样的配方重装先前 tag。
- **容器**：将镜像 tag 改回并重启。
- **从源代码**：`git checkout <old-tag> && make build`。

只要旧版本的会话存储 schema 是新版本所写内容的超集，回滚就是安全的。实践中，单一次要序列内始终成立，跨相邻次要版本通常也成立。主版本升级会附带迁移配方，并在 changelog 中提供明确的回滚免责声明。

## 下一步

- [Changelog](/zh-Hans/changelog/) —— release 逐一的分解。
- [故障排除](/zh-Hans/troubleshooting/) —— 若 `rousseau doctor` 出现 `fail` 行。
