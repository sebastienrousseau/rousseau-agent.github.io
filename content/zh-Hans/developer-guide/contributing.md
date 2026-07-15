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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "参与贡献"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "参与贡献"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "参与贡献"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "参与贡献"
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

## 基本规则

贡献接受来自受邀协作者。每个 PR 都以相同标准衡量：绿色 CI、下述代码规范、评审通过。绿色 CI 是必要但非充分条件。

权威源是仓库根目录的 [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md)。本页以文档站的语气镜像其内容。

## 开发环境

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # installs golangci-lint (v2) and govulncheck
make check      # vet + lint + race-tests + govulncheck
```

CI 中运行的每项检查都可通过 Makefile 在本地执行。若变更通过 `make check`，即会通过 CI。

## 提交规范

- **Conventional Commits** —— `feat:`、`fix:`、`refactor:`、`docs:`、`test:`、`chore:`、`ci:`、`perf:`。
- 主题行 ≤ 72 字符。正文解释 **为何**，而非做了什么。引用推动决策、issue 或事件。
- 不修改已发布的提交。新建一个提交；评审者更喜欢可 bisect 的序列。
- 若您配置了签名，请对提交签名。目前非必需，但对 release-tag 提交推荐。

## 代码规范

- 每个导出标识符都有以标识符名开头的 godoc 注释。
- 除非在 doc 注释中提供书面理由，否则不在导出 API 中使用 `interface{}` / `any`。
- `context.Context` 在每条 I/O 路径上传播。没有隐藏的全局变量或环境 logger；显式传递 `*slog.Logger`。
- 错误使用 `fmt.Errorf("...: %w", err)` 向上包装。哨兵错误进入 package 的 `errors.go`。在调用处优先 `errors.Is` / `errors.As`，避免字符串匹配。
- `main` 和测试辅助器之外不 panic。对运维者错误（重复注册、无效静态 schema）而 panic 的 `Must*` 变体，在有文档化理由时允许。
- 库代码中不使用 `fmt.Print*`。使用 `slog` 或 TUI model。`forbidigo` linter 强制执行。

## 测试规范

- 单元测试与代码同侧：`foo.go` → `foo_test.go`。
- 优先表驱动测试。停止性断言用 `require`，非停止性用 `assert`。
- 基于接口的测试注入优先于全局打补丁。每个 transport package 定义一个狭窄接口（`WSConn`、`IMAPClient`、`HTTPClient`、`Sender`），测试通过 fake 满足它。
- 覆盖率目标：纯业务逻辑 package 85%；总体 75%。
- Race 安全：`go test -race` 必须通过。若新并发代码引入非平凡的同步，需要一个 race 测试。
- 每个解析器都有 Fuzz 函数（`FuzzParseFoo` 与 `parseFoo` 同侧）。`make fuzz` 运行语料。

注入模式参见 [测试](/zh-Hans/developer-guide/testing/)。

## Pull request 流程

1. 对 `main` 打开 PR。若 `main` 移动到您身下，使用 rebase（不要 merge）。
2. 每个 PR 都需要：
   - 描述中的理由（2–3 句，链接到底层决策）。
   - 绿色 CI：`vet`、`lint`、`test-race`（Linux + macOS）、`govulncheck`、`codeql`、`reproducible-build`、覆盖率底线。
   - 评审通过。
3. 只 squash merge。合并提交消息就是最终提交消息，作为一次原子变更登陆 `main`。
4. 若 PR 新增依赖，请在描述中说明理由。相较新增依赖，优先标准库；相较新增依赖，优先复用既有依赖。

## 评审者清单

评审者按顺序核实：

1. **必要性。** 变更是否必需？还是在没有推动性需求的情况下增加了抽象 / 特性面？
2. **范围。** 变更是否保持在其声明的目的内，还是打包了不相关的清理？
3. **边界完整性。** 变更是否尊重 `agent → 具体` 的依赖方向？参见 [架构](/zh-Hans/developer-guide/architecture/)。
4. **测试覆盖。** 新代码路径是否有覆盖？边缘情形是否被行使？
5. **错误处理。** 错误是否带上下文包装？清理路径是否诚实（带有 `//nolint:errcheck` 理由的 `_ =`，而非静默吞没）？
6. **Godoc + linter 干净。** 每个导出符号都有文档；lint 输出为 0 问题。
7. **安全。** 变更是否触及 `bash` 工具、审批策略、传输认证或容器姿态？若是，PR 描述是否标注？

## 文档贡献

文档位于独立仓库。当代码 PR 触及用户可见面（新 flag、新字段、新工具）时，同一 PR —— 或紧随其后的文档仓库 PR —— 必须更新受影响的页面。

- **CLI 变更** → [用户指南：CLI](/zh-Hans/user-guide/cli/) 与 [参考：CLI 命令](/zh-Hans/reference/cli-commands/)。
- **配置变更** → [配置](/zh-Hans/configuration/) 与 [参考：配置 schema](/zh-Hans/reference/config-schema/)。
- **新工具** → [用户指南：工具](/zh-Hans/user-guide/tools/)。
- **新传输** → `content/transports/<name>.md`。
- **新 provider** → `content/providers/<name>.md`。
- **行为变更** → [Changelog](/zh-Hans/changelog/)。

## Release 流程

Release 从 `main` 切出：

1. 更新 changelog 条目。
2. 在 release 提交上打标签 `vX.Y.Z`。
3. `release` 工作流通过 GoReleaser 构建，生成 CycloneDX SBOM，发布 checksums 的 cosign 签名，并生成 SLSA-3 溯源。
4. 消费者按 [安全](/zh-Hans/security/) 与 [安装](/zh-Hans/getting-started/installation/) 中的配方进行校验。

Rousseau 遵循 [语义化版本](/zh-Hans/getting-started/updating/)：patch 修复 bug，minor 非破坏性地添加特性，major 破坏 —— 始终附带迁移配方。

## 治理

`rousseau-agent` 是单一维护者项目。决策权归 `go.mod` 与 `LICENSE` 中登记的维护者。贡献者可通过 PR 讨论或发送邮件到 `sebastian.rousseau@gmail.com` 提出方向变更。

## 安全披露

**请勿为安全报告提交公开 issue。** 请按 [安全策略](/zh-Hans/security/) 发送邮件到 `sebastian.rousseau@gmail.com`。72 小时内确认。

## 下一步

- [架构](/zh-Hans/developer-guide/architecture/) —— 变更前先看地图。
- [测试](/zh-Hans/developer-guide/testing/) —— 评审者期望的模式。
- [安全](/zh-Hans/security/) —— 披露路径。
