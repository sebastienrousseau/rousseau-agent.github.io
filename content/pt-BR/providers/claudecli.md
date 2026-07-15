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
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "Provedor claudecli"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Provedor claudecli"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Provedor claudecli"
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
twitter_title: "Provedor claudecli"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Como o provider <code>claudecli</code> herda autenticação do Claude Code instalado localmente, a matriz completa de <code>PermissionMode</code>, a semântica de correlação de sessão, aliases de modelo, e quando preferir isto sobre a API direta da Anthropic. Leia <code>internal/llm/claudecli/client.go</code> junto a esta página para a verdade absoluta.</p></aside>

## Quando usar o claudecli

O `claudecli` executa o CLI `claude` (Claude Code) como um subprocesso. Ele é o **provider padrão** e a escolha certa quando:

- Você já tem o Claude Code instalado e autenticado localmente.
- Você quer reutilizar uma conta Claude Code em nível de subscrição em vez de canalizar chaves de API.
- Você quer que o modelo rode dentro do próprio loop de tool-use do `claude` (seus recursos de edição de arquivo, thinking e plan mode ficam intactos).
- Você quer zero material secreto no arquivo de configuração do rousseau.

O trade-off: o `Registry` de tools do rousseau **não** é invocado para este provider — o `claude` roda suas próprias tools dentro do subprocesso. Objetos de resposta voltam como uma única mensagem de texto de fim de turno. Se você precisa que o rousseau limite `bash`/`edit`/`write` através da política de aprovação, use `anthropic`, `bedrock`, `vertex` ou um provider compatível com OpenAI.

## Herança de autenticação

O CLI `claude` mantém autenticação em três lugares:

| Localização | Conteúdo |
|---|---|
| `~/.claude/` | Tokens OAuth (subscrição), saída de helper de chave de API, configuração do workspace. |
| Keychain do sistema | No macOS, o `claude` pode cachear refresh tokens no login keychain. |
| Env `ANTHROPIC_API_KEY` | Se definida, o `claude` a usa em modo de chave de API em vez de OAuth. |

O `claudecli` nunca lê estes diretamente. Cada invocação é `exec.CommandContext(binary, args...)` — o subprocesso herda o ambiente e o diretório home do pai, e consulta suas próprias credenciais. Isso é o que o torna "zero-config" para operadores individuais.

<aside class="admonition" data-type="tip"><span class="admonition-title">Binds do contêiner</span><p>Ao executar o rousseau em um contêiner, faça bind-mount de <code>~/.claude</code> como leitura-gravação no contêiner para que o <code>claude</code> possa atualizar tokens OAuth cacheados no lugar:</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

O rótulo `Z` é crítico em hosts SELinux; veja [Implantação](/pt-BR/deployment/) para a unidade Quadlet completa.

## Configuração

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

| Campo | Padrão | Efeito |
|---|---|---|
| `binary` | `claude` | Executável resolvido no `$PATH`. Aponte para um caminho absoluto se você tem múltiplas versões do `claude`. |
| `model` | *vazio* | Passado como `--model <value>`. Vazio usa o padrão do `claude`. |
| `permission_mode` | *vazio* | Passado como `--permission-mode <value>`. Veja a tabela abaixo. |
| `extra_args` | `[]` | Antepostos antes de `-p <prompt>` em cada invocação. |

Cada campo mapeia para `ClaudeCLIConfig` em `internal/config/config.go`. A linha de comando do subprocesso montada a cada turno é:

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Parsing do STDOUT</span><p>O rousseau espera que o <code>claude</code> emita um envelope JSON no stdout. Se você envelopa o <code>claude</code> em um shell script (para auditoria, redação ou rate-limiting) o wrapper deve encaminhar o stdout sem modificação. O parser tolera uma linha de log inicial antes do primeiro <code>{</code> — veja <code>parseResult</code> em <code>internal/llm/claudecli/client.go</code> — mas lixo após o envelope JSON causará falha.</p></aside>

## Matriz de PermissionMode

A flag `PermissionMode` espelha o próprio `--permission-mode` do `claude`. O subprocesso impõe o valor; o rousseau não faz dupla checagem.

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">Atendido</button>
    <button role="tab" aria-selected="false">Não-atendido</button>
    <button role="tab" aria-selected="false">Somente leitura</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Sessões TUI interativas onde um humano está no terminal e pode aprovar chamadas de tool.

| Modo | Comportamento |
|---|---|
| `default` | O Claude Code pede confirmação interativamente para cada chamada de tool. Melhor para sessões exploratórias. |
| `acceptEdits` | Edições de arquivo prosseguem sem pedir; outras tools ainda pedem. Bom quando você confia na superfície de edição. |
| `auto` | Automático baseado na tool. Use quando quer que a heurística embutida do claude decida. |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Transportes de chat (WhatsApp, Slack, Discord, Signal, …) não têm humano no terminal para responder aos prompts.

| Modo | Comportamento |
|---|---|
| `bypassPermissions` | Cada chamada de tool roda sem pedir. Aceita o raio de impacto total. |
| `dontAsk` | Alias tratado de forma semelhante ao bypass. |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

O CLI define `bypassPermissions` automaticamente para daemons não-atendidos se o operador não especificou um — veja `setUnattendedPermissionDefault` em `internal/cli`.

<aside class="admonition" data-type="caution"><span class="admonition-title">Raio de impacto</span><p><code>bypassPermissions</code> dá ao modelo acesso direto ao <code>bash</code> com os privilégios do daemon. Combine com (a) um contêiner endurecido, (b) uma allowlist e (c) um approver em modo pattern no lado do rousseau — ou use um provider que não seja <code>claudecli</code>, que permite ao rousseau impor approvals antes de a tool executar.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Modo de exploração para refactors grandes ou revisões de código onde você não quer nenhuma gravação.

| Modo | Comportamento |
|---|---|
| `plan` | Modo planejador. Reads e grep são permitidos; writes são inibidos. |

```yaml
claudecli:
  permission_mode: plan
```

Pareie com o modo somente leitura do próprio rousseau (veja [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/)) para uma imposição em cinta e suspensório.

  </div>
</div>

## Correlação de sessão

O `claudecli` mantém o estado da conversa dentro do subprocesso. O rousseau correlaciona seus próprios IDs de sessão com os do `claude` via duas flags:

- `claude -p --session-id <uuid>` cria uma nova sessão. Se o UUID já existe, o `claude` erra com `already in use`.
- `claude -p --resume <uuid>` retoma uma sessão existente. Se desconhecida, o `claude` erra.

O rousseau escolhe a flag usando um `SessionCache` em memória (`InMemorySessionCache` por padrão). Em um cache miss em cold-start onde o `claude` já tem estado de uma execução anterior do rousseau, o provider tenta otimisticamente `--session-id`, captura o erro `already in use` e retenta com `--resume`. Veja o comentário em `(*Provider).Complete` em `internal/llm/claudecli/client.go`.

Callers que embutem o provider podem trocar por um cache persistente via `provider.WithCache(store)` — o store `state.sqlite` implementa a mesma interface e sobrevive a restarts do daemon, evitando o roundtrip de cold-start no primeiro turno após um reboot.

## Aliases de modelo

Os aliases de modelo do `claude` são honrados pelo subprocesso sem alteração:

| Alias | Aponta para |
|---|---|
| `sonnet` | O modelo padrão atual do tier Sonnet. |
| `opus` | O modelo padrão atual do tier Opus. |
| `haiku` | O modelo padrão atual do tier Haiku. |

Para reprodutibilidade entre restarts do daemon (benchmarks de skill, jobs cron, execuções em batch), fixe um ID de modelo exato:

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">Aliases seguem as releases</span><p>Aliases mudam quando a Anthropic entrega um novo modelo. O alias <code>sonnet</code> em julho de 2026 não aponta para os mesmos pesos para os quais o alias <code>sonnet</code> apontava em abril de 2026. Se seu workflow depende de um comportamento específico, fixe o ID exato.</p></aside>

## Combinando com skills

O `claudecli` envia o system prompt via `--system-prompt` na criação da sessão. O `claude` o honra literalmente e ignora valores subsequentes de `--system-prompt` em `--resume` — o que corresponde a como o rousseau o usa. A saída do `SkillsProvider` é inserida antes da invocação:

```
<agent.SystemPrompt>

<skill 1 markdown>

<skill 2 markdown>

<RecallProvider appendix>
```

Veja `internal/agent/agent.go` `systemPrompt()`. Skills funcionam de forma idêntica em cada provider; a mecânica da composição acontece em `agent.Agent`, não no provider.

<aside class="admonition" data-type="tip"><span class="admonition-title">Prompt caching</span><p>O provider direto da Anthropic marca o system prompt para o cache efêmero de prompt (veja <code>internal/llm/anthropic/cache.go</code>). O <code>claudecli</code> não — o <code>claude</code> possui seu próprio cache internamente. Se você quer economias mensuráveis no prompt-cache, use <code>provider: anthropic</code>.</p></aside>

## Armadilhas

- **Sem portabilidade entre providers.** Uma sessão criada contra o `claudecli` não é portável para `anthropic` — o estado do lado do modelo vive dentro do `claude`. Trocar de providers no meio força uma nova sessão.
- **O registry de tools não é invocado.** `bash`, `edit`, `write`, `grep`, `read` são executados pelo `claude`, não pelo `rousseau`. O `agent.Approver` do rousseau não pode limitar essas chamadas. Use um provider que não seja `claudecli` se precisar de imposição de approval no lado do rousseau.
- **Escopo de `--add-dir`.** Por padrão, o `claude` recusa a ler fora de seu próprio workspace. Passe `--add-dir /workspace` (ou onde seu código-fonte vive) via `extra_args` para expandir. Combine com a política de aprovação do rousseau no nível do transporte se você quer compensar a perda de controle.
- **Streaming.** O `claudecli` usa `claude -p --output-format json` (não-streaming). O caminho de streaming em `internal/llm/claudecli/stream.go` lê `--output-format stream-json`; opte usando `StreamingProvider` de uma integração embutida.
- **Vazamento de ambiente.** O subprocesso herda cada variável de ambiente do pai. Se `ANTHROPIC_API_KEY` está definida no ambiente do rousseau, o `claude` a preferirá sobre o OAuth cacheado. Isso geralmente é fine, mas muda o billing.

## Solução de problemas

### `claudecli: run: exec: "claude": executable file not found in $PATH`

O `claude` não está no `PATH` (ou a imagem do contêiner não o entrega). Duas correções:

1. Defina `claudecli.binary` para um caminho absoluto.
2. Adicione o Claude Code à camada de runtime do contêiner — o `docker/Dockerfile` de referência usa `node:22-alpine` por essa razão.

### `claudecli: model error: session id already in use`

Você está executando dois processos rousseau contra o mesmo session ID contra a mesma instalação do `claude`, ou o cache em memória descartou uma sessão da qual o `claude` ainda se lembra. A retentativa otimista descrita acima trata o segundo caso; o primeiro significa que você tem daemons concorrentes se atrapalhando.

### `claudecli: no JSON in output`

O `claude` imprimiu não-JSON no stdout, ou saiu antes de emitir o envelope. Causas comuns: uma chave de API inválida no lado do Claude Code, uma versão do `claude` que antecede `--output-format json`, ou um shell wrapper escrevendo marcadores de progresso. Execute `claude -p --output-format json 'hello'` diretamente para isolar.

### A resposta corta no meio da frase

A saída do `claude` é limitada por `--max-turns` e seu próprio budget interno de tokens. O rousseau não define `--max-turns`; se você o define via `extra_args`, aumente-o. Para gerações longas, considere um provider de API direta onde você controla `MaxTokens` a partir de `internal/llm/anthropic/client.go`.

### O plano de subscrição tem rate-limit mas a API está bem

O CLI `claude` em um plano de subscrição tem limites ocultos por-conversa e por-janela. Se você os atingir, mude para `provider: anthropic` com uma chave de API — a API direta tem limites explícitos e publicados (veja [Guias: Rate limits](/pt-BR/guides/rate-limits/)).

## Páginas relacionadas

- [Providers: Anthropic](/pt-BR/providers/anthropic/) — API direta com prompt caching e streaming.
- [Providers: Bedrock](/pt-BR/providers/bedrock/) — Claude gerenciado pela AWS.
- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — como limitar chamadas de tool na camada rousseau.
- [Skills](/pt-BR/skills/) — como o apêndice do system-prompt é composto.
- [Configuração](/pt-BR/configuration/) — o bloco `claudecli` em contexto.

## Leitura complementar

- `internal/llm/claudecli/client.go` — invocação de subprocesso, correlação de sessão, parsing de JSON.
- `internal/llm/claudecli/stream.go` — variante de streaming usando `--output-format stream-json`.
- `internal/config/config.go` — struct `ClaudeCLIConfig`.
- `internal/cli/root.go` — como `setUnattendedPermissionDefault` escolhe `bypassPermissions` para transportes de chat.
