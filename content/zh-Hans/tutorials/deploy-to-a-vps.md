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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "教程：部署到 VPS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "教程：部署到 VPS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "教程：部署到 VPS"
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
twitter_description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "教程：部署到 VPS"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 您将构建什么

一台全新的 Ubuntu 24.04 VPS，在 rootless Podman 容器下运行 rousseau-agent WhatsApp 守护进程，由位于 `docker/rousseau-agent.container` 的 systemd Quadlet 单元驱动。只读根文件系统、所有能力放弃、`NoNewPrivileges=true`、开启 seccomp。零入站网络端口。

预计时间：45 分钟。

## 先决条件

- 一台 Ubuntu 24.04（或 Debian 12+ / Fedora 40+）VPS。1 GB RAM、20 GB 磁盘就足够了。
- 到具有 sudo 权限的非 root 用户的 SSH 密钥访问。
- 您的 Anthropic API key，或愿意运行 `claudecli` —— `claudecli` 需要在 VPS 上安装带活跃 OAuth 会话的 `claude`，在无头服务器上这很别扭。Anthropic direct 或 Bedrock 是务实之选。

## 第 1 步：基础 OS 设置

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# rootless podman 需要为用户提供 subuid/subgid 范围
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

创建服务用户及其 systemd 用户会话：

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # 无人登录时也保持用户服务运行
```

## 第 2 步：转移源代码

`docker/rousseau-agent.container` 的 Quadlet 单元会构建一个本地镜像。在 VPS 上：

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

`Dockerfile` 生成一个静态 Go 二进制（`CGO_ENABLED=0`），把它复制到一个最小基础镜像中，并以 UID 1000 运行。基础镜像讨论见 [部署](/zh-Hans/deployment/)。

## 第 3 步：播种配置

Rousseau 读取 `~/.config/rousseau/config.yaml`。在主机上创建 —— Quadlet 单元把容器的 `$HOME` bind-mount 回主机。

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/config.yaml <<'YAML'
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

whatsapp:
  reply_header: "*rousseau*\n\n"

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

log:
  level: info
  format: json
YAML
chown -R rousseau:rousseau /home/rousseau/.config
```

把 Anthropic API key 存在 systemd 环境文件中 —— 绝不要放在 `config.yaml` 中：

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

从 Quadlet 单元中引用它 —— 见下一步。

## 第 4 步：安装 Quadlet 单元

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

针对您的 JID 与 secret 文件进行编辑：

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

重载并启动：

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## 第 5 步：首次配对

WhatsApp 桥接首次需要打印 QR 码。附加：

```sh
podman logs -f rousseau-agent
# 用您的手机扫描 QR：WhatsApp > 设置 > 已连接设备
```

预期日志序列（来自 `internal/transport/whatsapp/client.go`）：

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

设备凭据持久化到 `/home/rousseau/.local/share/rousseau/whatsapp.db`。后续重启会跳过 QR。

## 第 6 步：核实

```sh
podman exec rousseau-agent rousseau status
```

退出码 0 表示守护进程健康。任何非零都是红旗 —— 见 [参考：退出码](/zh-Hans/reference/exit-codes/)。

从允许列表中的手机向自己发送一条测试消息。结构化日志显示：

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## 第 7 步：加固评审

Quadlet 单元已经强制：

- `ReadOnly=true` + `Tmpfs=/tmp` —— 运行时无镜像变更。
- `DropCapability=all` —— Go 二进制不需要提升的能力。
- `NoNewPrivileges=true` —— 子进程无法获得特权。
- `SeccompProfile=/usr/share/containers/seccomp.json` —— 内核级 syscall 过滤器。
- `Network=pasta` —— rootless 网络栈，默认拦截入站。
- `UserNS=keep-id` —— bind-mount 的文件在两侧的属主如预期。

如果您想要最紧的姿态，把守护进程包裹在只出站的防火墙（nftables 或 Cloudflare Zero-Trust）中，只允许 Anthropic + Meta 实际解析到的 CDN 地址段。清单见 [指南：企业接入](/zh-Hans/guides/enterprise-onboarding/)。

## 第 8 步：备份

整个持久化状态就是一个目录：`/home/rousseau/.local/share/rousseau/`。用 `restic` 或 `borg` 每晚备份。

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

SQLite 数据库可以安全地热快照，因为 `internal/state/sqlite/store.go` 中的 `Open()` 启用了 WAL journaling。

## 相关

- [部署](/zh-Hans/deployment/) —— 完整 Quadlet 单元参考。
- [指南：生产部署](/zh-Hans/guides/production-deployment/) —— 日志转运、滚动重启。
- [指南：企业接入](/zh-Hans/guides/enterprise-onboarding/) —— SBOM 校验、seccomp 审计。
- [安全](/zh-Hans/security/) —— 信任边界。
