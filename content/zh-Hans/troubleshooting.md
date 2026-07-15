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
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/troubleshooting/"
subtitle: "常见故障模式及其修复方法。"
tags: "troubleshooting, support"
title: "故障排查"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "故障排查"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "故障排查"
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
twitter_description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "故障排查"
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

## WhatsApp：无法扫描二维码

症状：`rousseau whatsapp` 打印的二维码被手机 app 拒绝，或者配对对话框显示 "This device is not paired with WhatsApp."

修复：

1. **重建容器。** 如果你运行的是较旧镜像，`whatsmeow` 可能已发布协议更新。重建：
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **删除 `whatsapp.db`。** 部分完成的配对会让数据库处于 whatsmeow 无法复用的状态。删除后重新配对：
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **检查时钟偏差。** WhatsApp 的握手对时间敏感。若容器时钟偏差超过 30 秒，配对会静默失败。
   ```sh
   timedatectl status
   ```

## WhatsApp 重连循环

症状：日志显示每隔几秒反复出现 `whatsapp.connected` 后紧跟 `whatsapp.disconnected`。

修复：

1. **时钟偏差。** 同上。
2. **允许列表配置错误。** 每条入站消息都被作为未授权而丢弃；某些服务器在静默丢弃过多后会关闭 socket。使用 `--allow` 添加正确的 JID。
3. **Meta 侧封禁。** 若 WhatsApp 手机端显示 "This device has been logged out"，Meta 已使配对失效。使用新的二维码重新配对。若同一号码反复发生，请停止使用该号码。

## cosign verify-blob 失败

症状：

```
Error: no matching signatures
```

修复：

1. **certificate-identity 正则错误。** 该正则必须匹配签署发布的 GitHub 仓库。对于 rousseau-agent 发布，正确值为：
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   不要使用 `.*`——那会接受任何仓库的 cosign 签名。
2. **OIDC 发行方错误。** GitHub Actions 的 cosign 签名由 `https://token.actions.githubusercontent.com` 发行。其他 CI 提供方（GitLab、Buildkite）从不同的 URL 发行。
3. **签名文件错误。** 检查 `<version>_checksums.txt.sig` 与你正在验证的 `_checksums.txt` 相对应（而非来自另一次发布的过时副本）。
4. **Sigstore 信任根变更。** 使用 `cosign initialize` 刷新；信任根按缓慢节奏更新。

## 容器绑定挂载失败

症状：`podman play kube` 或 `systemctl --user start rousseau-agent.service` 因绑定挂载报 `permission denied`。

修复：

1. **SELinux 标签。** 每一行卷都必须以 `:Z`（共享用 `:z`）结尾，以便 Podman 应用正确的 SELinux 标签：
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z`（大写）是私有标签——适用于单容器挂载。`:z`（小写）在多个容器间共享标签。
2. **`keep-id` 映射。** 没有 `UserNS=keep-id`，容器 UID 1000 会被重映射到主机的 subuid 范围，无法写入主机拥有的文件。请确保 Quadlet 中包含：
   ```
   UserNS=keep-id
   ```
3. **目录缺失。** Podman 不会自动创建绑定挂载源。请先创建目录：
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## 定时任务未触发

症状：`rousseau cron list` 显示任务存在，但在预定时间未发生任何事。

修复：

1. **检查状态。** `rousseau status` 报告调度器活动。若调度器未运行，则托管它的守护进程未运行。
2. **时区。** 调度使用服务器本地时区。用 `timedatectl` 确认。若希望调度不受主机 locale 影响，可在 Quadlet 中设置 `TZ=UTC`。
3. **PollInterval 延迟。** 新任务会在 `PollInterval`（默认 60 秒）内生效。请等待一分钟。
4. **投递失败。** 任务已触发但投递失败。查看日志中的 `cron.delivery_failed`；目标格式因传输而异（参见 [/cron/](/zh-Hans/cron/)）。

## 审批策略拒绝一切

症状：每次工具调用都被 "denied by pattern policy" 拒绝，模型无法推进。

修复：

1. **缺少允许规则。** 在 `pattern` 模式下并设置 `default: deny` 时，每次工具调用都需要一条匹配的允许规则。为你希望放行的工具添加一条：
   ```yaml
   agent:
     approver:
       mode: pattern
       default: deny
       allow:
         - {tool: read, match: ".*"}
         - {tool: grep, match: ".*"}
         - {tool: edit, match: "^./workspace/.*"}
   ```
2. **deny 优先于 allow。** 对同一工具，`deny` 规则总是胜过 `allow` 规则。请检查你的拒绝列表是否意外过度匹配。
3. **提高默认值。** 对于有人值守的会话，`default: allow` 加上收紧的拒绝规则通常更实用：
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## 提供方返回 401

症状：agent 报错 `provider: unauthorized`。

修复：

1. **API 密钥错误。** 对于 Anthropic 直连提供方，请确认 `ANTHROPIC_API_KEY` 已导出或在 `~/.config/rousseau/config.yaml` 中设置。
2. **凭证链错误。** 对于 Bedrock，在容器内运行 `aws sts get-caller-identity` 确认 SDK 解析的主体。
3. **Vertex 服务账号。** 对于 Vertex 提供方，请确认 `vertex.credentials_file` 指向的文件在容器内可读，并授予 `roles/aiplatform.user`。

## 提供方返回 429

症状：agent 报错 `provider: rate limited`。

修复：

1. **降低 `max_tokens`。** 较短的完成能更快清空速率窗口。
2. **启用压缩。** 长文本会增加输入 token 压力；`agent.compression.enabled: true` 会折叠旧消息。
3. **等待。** rousseau 在 `Complete` 内部不重试；由调用方（聊天传输、定时调度器或 `rousseau chat`）决定是否重试及如何重试。

## `rousseau chat` 只显示空白 TUI

症状：Bubble Tea TUI 打开但没有光标、没有视口。

修复：

1. **TERM 环境。** rousseau 需要具备 ANSI 能力的终端。请设置 `TERM=xterm-256color`（或类似值）。
2. **stdin 被包装。** 在 `nohup` 或管道下运行会剥离终端。请交互式运行。

## Slack：启动时 `invalid_auth`

症状：`slack.starting` 之后立即出现 `invalid_auth`。

修复：

1. **令牌混用。** Rousseau 同时需要 `xapp-…`（应用级，`--app-token`）和 `xoxb-…`（机器人，`--bot-token`）。在期望机器人令牌处传入应用令牌会导致此错误。
2. **应用未安装。** 创建作用域后，请在 Slack 应用配置中点击 *Install to Workspace*。令牌仅在安装后有效。
3. **令牌已轮换。** 管理员可能手动轮换了 Slack 令牌。若你轮换了令牌，所有使用它的守护进程都必须以新值重启。

## Slack：机器人回复自己的消息（循环）

症状：rousseau 的出站消息触发了入站事件，守护进程随之回复，造成失控回复。

修复：

1. **设置 `bot_user_id`。** `--bot-user-id` 选项（或配置中的 `slack.bot_user_id`）让守护进程忽略该用户 ID 发送的消息。用 `curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test` 获取。
2. **验证事件过滤。** 传输默认忽略 `bot_message` 子类型，但配置不当的 Slack 应用可能绕过此机制。

## Discord：消息正文为空

症状：`discord.incoming from=... body=` —— 消息到达但没有内容。

修复：

1. **未启用 Message Content Intent。** 在 Discord 开发者门户的 <em>Bot &gt; Privileged Gateway Intents</em> 中打开 **Message Content Intent**。未启用时，Discord 会在 Gateway 事件中去除消息文本。
2. **缺少作用域。** 邀请 URL 必须授予机器人对所用频道/私聊的 `Read Message History` 与 `Send Messages`。

## Discord：`disallowed intents`

症状：启动时报错 `Discord returned 4014 disallowed intents`。

修复：

1. **特权 Intent。** 启用 *Message Content Intent*（见上）。即使你从未使用，只要请求而未获批，Discord 就会返回 4014。
2. **认证。** 加入 100+ 服务器的机器人必须经 Discord 认证才能使用特权 intent。请按开发者门户步骤操作。

## Telegram：`unauthorized`

症状：`telegram.starting` 后出现 `getUpdates: 401`。

修复：

1. **令牌错误。** BotFather 只会返回一次令牌——不要包含末尾的句点。令牌形如 `<bot_id>:<secret>`。
2. **令牌已吊销。** 在 BotFather 中执行 `/revoke` 会使当前令牌失效；重新获取一个。

## Email：`dial tcp: i/o timeout`

症状：IMAP 或 SMTP 连接始终不成功。

修复：

1. **端口错误。** IMAP 为 `993`（隐式 TLS）。SMTP 提交为 `587`（STARTTLS）或 `465`（隐式 TLS）。Rousseau 两端都使用隐式 TLS——仅支持 STARTTLS 的服务器目前不受支持。迁移方案参见 [传输：Email](/zh-Hans/transports/email/)。
2. **出站被阻。** 企业防火墙经常阻止出站 SMTP。在容器内使用 `openssl s_client -connect smtp.example.com:465` 测试。
3. **提供方要求应用密码。** Gmail、Fastmail 等在启用 2FA 时要求使用应用密码（而非账户密码）。请在提供方的安全设置中生成一个。

## Vertex：`permission denied on resource`

症状：`vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`。

修复：

1. **缺少角色。** 为调用 API 的服务账号或用户授予 `roles/aiplatform.user`。IAM 变更最多需要一分钟传播。
2. **项目错误。** 配置中的 `project` 必须与拥有配额的项目相同。若在另一个项目上计费，请使用 `gcloud auth application-default set-quota-project` 设定 quota-project。
3. **区域不匹配。** 请求区域必须支持该模型——Vertex Model Garden 会列出支持情况。

## Bedrock：`You don't have access to the model`

症状：`AccessDeniedException: You don't have access to the model with the specified model ID`。

修复：

1. **未申请模型访问权。** Bedrock 需要通过控制台明确申请模型访问（*Foundation models &gt; Model access*）。即使 IAM 允许 `InvokeModel`，此步骤仍必需。
2. **区域错误。** 模型可用性因区域而异。请查看 Bedrock 控制台。
3. **跨账号配置错误。** 若使用 AssumeRole，请确认目标角色的策略允许对精确模型 ARN 执行 `bedrock:InvokeModel`。

## Ollama：`context deadline exceeded`

症状：Ollama 仍在生成时 rousseau 超时。

修复：

1. **CPU 推理很慢。** 70B 模型在笔记本 CPU 上单轮可能耗时数分钟。请使用较小模型（`llama3.1:8b`）或 GPU 主机。
2. **超时继承。** rousseau 使用 SDK 默认 HTTP 超时。若你自行封装提供方，请将超时提升至至少 120 秒。

## 语音消息：未配置转录器

症状：`whatsapp.audio_ignored reason=transcriber_not_configured`。

修复：

1. **Whisper 未启用。** 在配置中设置 `whatsapp.voice.enabled: true` 并确保 `whisper` 二进制在 `PATH` 中（或将 `whatsapp.voice.binary` 设为绝对路径）。
2. **模型文件缺失。** 将 `whatsapp.voice.model_path` 设为明确的 `.bin` 文件。Whisper.cpp 模型需手动下载——配置指向它们的位置。

## 会话存储：`database is locked`

症状：WAL 写入者阻塞；请求超时。

修复：

1. **两个守护进程共用一个 DB。** SQLite 的 WAL 支持并发读者但仅允许一个写者。若你对同一 `state.path` 运行两个 rousseau 进程，其中一个会阻塞。请使用不同的状态路径。
2. **`busy_timeout` 过低。** DSN 设置为 `busy_timeout=15000`。在持续争用下可提高——但请先排查根因。
3. **过时的 WAL 文件。** 崩溃的写入者会留下被锁定的 `sessions.db-wal`。停止一切、删除 `sessions.db-wal` 和 `sessions.db-shm`、重启。

## MCP：Claude Desktop 看不到 rousseau 工具

症状：在 `claude_desktop_config.json` 中通过 `command: "rousseau"` 启动 rousseau，但没有工具出现。

修复：

1. **配置未保存。** Claude Desktop 在保存时热重载；如果你在运行实例中编辑了文件，请重启它。
2. **`command` 不在 PATH 中。** Claude Desktop 从自身环境启动子进程；`/usr/local/bin/rousseau` 可能不可见。请使用绝对路径。
3. **stderr 噪声。** rousseau 将结构化日志写入 stderr；日志过多会压垮宿主。对严格宿主运行 MCP 时请设置 `log.level: warn`。

## 技能：`skill loader: parse: yaml: line X`

症状：rousseau 启动时报 YAML 解析错误。

修复：

1. **frontmatter 格式错误。** 技能使用 `---` 分隔的 YAML frontmatter。请确保两条围栏均存在且没有制表符缩进。
2. **未加引号的冒号。** 值中的冒号（`description: this: that`）会被解析为嵌套 map。请给值加引号：`description: "this: that"`。

## `rousseau doctor` 报告 `warn`

症状：doctor 完成但出现琥珀色行。

修复：

1. **阅读理由。** 每条 warn 行都包含原因。常见的有：`whatsapp.paired=false`（从未链接）、`state.wal_size=large`（检查点滞后）、`provider.claudecli.model=unset`（使用 claude 的默认值）。
2. **warn 不是失败。** 守护进程仍会启动；该行只是提示有值得审查的地方。

## Kubernetes：pod 卡在 `CrashLoopBackOff`

症状：Deployment 始终未达到 Ready。

修复：

1. **查看日志。** `kubectl logs -p <pod>` 显示上一个容器的 stderr。十有八九是配置或凭证错误。
2. **缺少状态卷。** 若 `~/.local/share/rousseau` 没有 PVC，配对在重启后不会保留，守护进程可能在反复尝试重新配对时循环。
3. **IRSA / Workload Identity 配置错误。** 请确认服务账号注解匹配具有提供方权限的 IAM 角色。`kubectl exec` 进入 pod 并运行 `aws sts get-caller-identity`（Bedrock）或 `gcloud auth print-access-token`（Vertex）确认。

## nftables 规则集阻断了提供方出站

症状：应用出站规则后首次调用提供方时 `dial tcp: i/o timeout`。

修复：

1. **CIDR 已轮换。** 提供方 IP 范围会变化。请使用基于 DNS 的出站——由定时任务刷新的 ipset，或在连接时解析的出站代理。
2. **DNS 被阻。** 出站规则集必须允许到 DNS 解析器的 UDP/53（或 TCP/53）。

## 结构化日志缺字段

症状：`whatsapp.incoming` 只显示了 `from` 而没有其他属性。

修复：

1. **日志级别过高。** 部分字段仅在 `debug` 级别发出。请在配置中设置 `log.level: debug`。
2. **JSON 解析器吞掉字段。** 经过剥离未知字段的过滤器可能会丢弃 `elapsed`、`bytes` 等。请对照原始 stdout 验证。

## 相关页面

- [快速入门：第一个传输](/zh-Hans/getting-started/first-transport/)——端到端演练。
- [提供方](/zh-Hans/providers/)——按提供方的故障排查。
- [传输](/zh-Hans/transports/)——按传输的故障排查。
- [配置](/zh-Hans/configuration/)——每一项配置的权威来源。
- [安全](/zh-Hans/security/)——信任边界与审计轨迹。

## 延伸阅读

- `internal/cli/doctor.go`——doctor 实现。
- `internal/state/sqlite/store.go`——会话存储 DSN 与 WAL 处理。
- `internal/transport/router.go`——入站事件路由与允许列表。
- Slog 属性键参考——源码树中所有的 `.info()`/`.warn()`/`.error()`。
