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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "Compressão + recall"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Compressão + recall"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Compressão + recall"
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
twitter_title: "Compressão + recall"
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

## Dois problemas, dois mecanismos

- Uma única sessão longa pode ultrapassar a janela de contexto do modelo. A **compressão** colapsa mensagens antigas em um bloco de resumo para que o loop continue funcionando.
- Uma nova sessão sobre um tópico relacionado perde o valor das conversas anteriores. O **recall** consulta o índice FTS5 entre sessões e insere trechos no system prompt.

A compressão edita a sessão atual no local. O recall nunca edita — ele anexa contexto ao system prompt do turno atual.

## Compressão

`internal/agent/compressor.go` implementa um sumarizador apoiado em LLM. O loop do agente o consulta no início de cada `Turn`:

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

Se a sessão for curta, nada acontece. Quando a contagem de mensagens ultrapassa `trigger_messages`, o compressor:

1. Isola o final da sessão — as `keep_recent` mensagens mais recentes — e as preserva na íntegra.
2. Envia tudo o que é mais antigo ao provedor com um prompt de sumarização.
3. Substitui o bloco mais antigo por uma única mensagem sintética `RoleSystem` contendo o resumo.
4. Marca a sessão para que o bloco de resumo fique no prefixo elegível para prompt cache já na próxima chamada ao provedor.

O loop então prossegue com a lista de mensagens menor. Você nunca vê a emenda.

### Habilitando a compressão

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # zero → default 60
    keep_recent: 8            # zero → default 8
    prompt: ""                # zero → sensible default
```

| Campo | Padrão | Significado |
|---|---|---|
| `enabled` | `false` | Desligado por padrão. |
| `trigger_messages` | 60 | Contagem de mensagens acima da qual a compressão dispara. |
| `keep_recent` | 8 | Quantas mensagens recentes preservar na íntegra. |
| `prompt` | embutido | Sobrescreve a instrução de sumarização. |

### Quando deixar desligado

A compressão usa uma ida e volta ao provedor por disparo. Em uma conta `claudecli` no plano por assinatura, essa viagem é gratuita — habilite à vontade. Em uma API paga por token, cada disparo tem um custo, então aumente `trigger_messages` ou mantenha desabilitado para sessões curtas.

### Quando deixar ligado

- Daemons de chat de longa duração em que uma thread de WhatsApp cresce ao longo de semanas.
- Prompts agendados por cron cujas respostas alimentam um prompt subsequente.
- Provedores auto-hospedados em que o custo por token é zero.

### Semântica preservada durante a compressão

- Pares tool-use / tool-result nunca são divididos. Se um `tool_use` está na região comprimida e seu `tool_result` está na região preservada, ambos são colapsados no resumo.
- O compressor nunca reescreve o turno de usuário em andamento.
- O prompt caching (marcadores `cache_control` em `internal/llm/anthropic`) é colocado no bloco de resumo, para que a próxima chamada o leia do cache.

## Recall

`internal/state/sqlite/` mantém uma tabela virtual FTS5 indexando cada mensagem. Um `RecallProvider` executa uma consulta contra essa tabela e retorna um apêndice para o system prompt.

### A interface

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

O loop do agente chama isto uma vez por iteração. Quando retorna texto não vazio, o texto é anexado ao system prompt base daquela iteração.

### O provider padrão

`internal/agent/recall.go` traz uma heurística que:

1. Extrai tokens relevantes da última mensagem de usuário na sessão atual.
2. Executa `MATCH` contra o índice FTS5 para esses tokens em outras sessões.
3. Formata os N melhores trechos como um bloco `Previously in another session:`.
4. Limita o apêndice para que nunca exceda um orçamento de caracteres configurado.

### Habilitando o recall

O recall é conectado na construção do agente. Veja `internal/cli/chat.go` e `internal/cli/*.go` para saber como cada transporte o conecta. Ao embutir no seu próprio código:

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### Interação com o approver

O recall lê do armazenamento de sessões; nunca dispara uma chamada de ferramenta. O approver não é consultado. Os próprios conteúdos do store são o limite de confiança.

### Busca em sessões pelo CLI

O recall é uma feature voltada à máquina. Para humanos, o mesmo índice FTS5 alimenta:

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

Mesmo motor de consulta, mesmos resultados, menos o re-ranking pelo LLM que um `RecallProvider` mais completo pode acrescentar.

## Interação com skills

Skills ([Skills](/pt-BR/skills/)) e recall ambos adicionam conteúdo ao system prompt. Eles são compostos em uma ordem fixa:

1. System prompt base (de `agent.system_prompt` ou o padrão).
2. Apêndice de skills (se houver).
3. Apêndice de recall (se houver).

Tudo é separado por duas quebras de linha. Se nada precisa ser adicionado, o prompt base passa inalterado.

## Semântica do bloco de resumo

A mensagem sintética de resumo é emitida com `RoleSystem`. Não é uma mensagem de usuário nem de assistente, então nunca aparece em `rousseau session show` como um turno de conversa — aparece como metadado `[compressed summary]`.

Se você retomar uma sessão comprimida com `rousseau chat --session <id>`, o resumo é preservado. Deletar o bloco de resumo via uma hipotética edição de schema é inseguro: o modelo pode referenciar fatos conhecidos apenas por meio dele.

## Verificando se a compressão está disparando

```
INFO agent.compressed messages=12
```

`messages` é o novo comprimento da sessão depois que o bloco de resumo substituiu o prefixo comprimido. Um `WARN agent.compress_failed err=...` significa que o provedor de sumarização deu erro; o loop continuou contra a sessão não comprimida.

## Ressalvas

- Compressão é lossy. O resumo é texto gerado por modelo; detalhes importantes podem ser descartados. Para trilhas de auditoria, mantenha a sessão completa no store — a compressão só afeta o que o modelo vê, não o que o SQLite persiste.
- O recall exige a extensão FTS5 do SQLite. `modernc.org/sqlite` a compila por padrão; se você trocar a implementação do store, garanta que FTS5 esteja disponível.
- Ambas as features assumem texto UTF-8. Transcrições de mensagens de voz (veja [Voice mode](/pt-BR/user-guide/voice-mode/)) contam como mensagens de usuário normais depois de transcritas.

## Próximo

- [Conceitos](/pt-BR/concepts/) — visão geral do loop do agente.
- [Configuração](/pt-BR/configuration/) — cada botão de `agent.compression.*`.
- [Skills](/pt-BR/skills/) — a terceira entrada do system prompt.
