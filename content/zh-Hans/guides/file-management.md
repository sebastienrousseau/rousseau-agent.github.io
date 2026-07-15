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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "指南：文件管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：文件管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：文件管理"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：文件管理"
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

## 两个工具

两个工具会改动文件系统：

- [`write`](/zh-Hans/reference/tool-schemas/#write) —— 整文件覆盖。`internal/tools/builtin/write.go` 以模式 `0o644` 写入，并 `MkdirAll(dir, 0o755)`。
- [`edit`](/zh-Hans/reference/tool-schemas/#edit) —— 在现有文件中做一次精确字符串替换。`internal/tools/builtin/edit.go`。

两者都需要**绝对路径**（它们会调用 `filepath.IsAbs`）。两者都没有原子交换的伎俩 —— 直接使用 `os.WriteFile`。

## 容器看世界的视角

`docker/rousseau-agent.container` 的参考 Quadlet 单元把三个主机目录挂载到容器中：

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

主机上没有其他东西可见。从容器内部看，一个针对 `/workspace/repos/foo/main.go` 的 `edit` 工具调用在主机上解析到 `~/team-rousseau-workspace/repos/foo/main.go`。

### `:Z` —— SELinux 标签

每条 `Volume=` 上的 `:Z` flag 告诉 Podman 用**容器私有**的 SELinux MCS 类别重标该挂载。如果没有它，在启用 SELinux enforcing 模式的系统上：

- 读取大多数时候仍然可用（`container_file_t` 广泛可读）。
- 写入以 `EACCES` 失败，审计日志中出现 `avc: denied { write }`。

如果您把 flag 换成 `:z`（小写），Podman 会用**共享**类别重标 —— 对多个容器用户共享的主机更安全，但不是默认。

在没有 SELinux 的系统（Debian、非加固 Ubuntu）上，`:Z` 是静默 no-op。

### `UserNS=keep-id` —— UID 映射

容器以 UID/GID 1000 运行。没有用户命名空间映射时，rootless Podman 会把 1000 重映射到 subuid 范围（通常是 `100000+`），从容器内写入的文件在主机上会属于那个映射后的 UID —— 对运维来说无法使用。

`UserNS=keep-id` 把容器 UID 1000 映射到主机用户的 UID（在参考设置中也是 1000）。写入 `/workspace` 内的文件最终在主机上属于 `seb:seb` —— 正是您想要的。

如果您的主机用户不是 UID 1000，映射仍然有效；`keep-id` 使用调用用户的实际 UID。

## 编辑 `/workspace` 之外

由于 bind mount 是容器对主机文件系统的唯一视图，针对 `/etc/nginx/nginx.conf` 的 `write` 或 `edit` 会以 path-not-found 错误失败 —— 该路径在容器内根本不存在。这是**特性**：意味着运维的审批策略可以信任容器边界。

如果您确实需要守护进程触碰一个不同的主机路径：

1. **首选：** 向 Quadlet 单元添加一条新的 `Volume=` 行。做最不宽容的选择：`:ro` 表示只读，`:Z` 表示私有 SELinux 标签。
2. **不要**在容器外运行 rousseau 来绕过边界 —— 您会丢失 seccomp、drop-caps 与只读根文件系统。

## 在容器之外编辑

如果您在主机上直接运行 rousseau（无容器），工具针对守护进程的进程视图操作 —— 默认情况下包括用户 HOME 下的一切。审批器是唯一的隔离层。pattern 模式 + `default: deny` 的配方见 [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/)。

## `write` vs `edit` —— 何时用哪个

| 场景 | 使用 |
|---|---|
| 创建新文件。 | `write`。 |
| 整体重写文件。 | `write`。 |
| 更改大文件的某一节。 | `edit`。当 `old_string` 不唯一时安全失败。 |
| 在文件内重命名一个符号。 | 多次带逐渐更多周围上下文的 `edit` 调用，或者一次带完整重写内容的 `write`。不要使用 `edit` 走 `replace_all` 风格的语义 —— 该工具拒绝。 |

`edit` 上精确唯一性的约束是有意的。它直接借用了 Claude Code 的 Edit 工具。在 `internal/tools/builtin/edit.go` 中搜索解释原因的注释块。

## 常见失败模式

| 症状 | 原因 | 修复 |
|---|---|---|
| `edit: path must be absolute, got "…"` | 模型传了相对路径。 | 在审批器中拒绝或重写；要求模型使用绝对路径。 |
| `edit: old_string not found in …` | 文件在模型上次读取后被改动，或者模型幻觉出了周围上下文。 | 模型通常会重新读取并重试。 |
| `edit: old_string is not unique in … (found 3 occurrences)` | 相同字符串出现多次。 | 模型必须提供更多周围行来消歧。 |
| `write: permission denied` | SELinux 标签不匹配或 UID 映射错误。 | 核实卷上的 `:Z` 与容器上的 `UserNS=keep-id`。 |
| `read: does not look like UTF-8 text` | 文件前 512 字节包含 NUL 字节（`read.go` 中的 `isLikelyText`）。 | 在审批器层拒绝二进制读取；如需鉴别，使用带 `file` 的 `bash` 工具。 |

## 大规模重写之前的备份

工具不会创建 `.bak` 副本。对于高风险变更，教模型先写到一个同级路径，用 `bash` diff，然后交换。或者，把一切放在一个 git 分支上运行 —— rousseau 完全把 `git` 排除在自己的执行路径之外，所以任何版本化都通过您正常的工作流发生。

## 相关

- [参考：工具 schema](/zh-Hans/reference/tool-schemas/) —— 精确输入 schema。
- [用户指南：工具](/zh-Hans/user-guide/tools/)。
- [部署](/zh-Hans/deployment/) —— 定义 bind mount 的 Quadlet 单元。
- [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 把写入锚定到某个目录树。
