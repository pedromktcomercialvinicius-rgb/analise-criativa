# Meta Ads MCP — puxar a peça e assistir o campeão

Este relatório **não fecha** sem o agente ter visto o criativo do campeão. Número sem peça é chute.

Use o **MCP de Meta Ads** se estiver ligado (Pipeboard, MCP oficial da Meta, ou outro). Os nomes das tools mudam; o que importa é a **intenção**. Esta skill é **só leitura**. Não criar, pausar, duplicar nem alterar orçamento.

Se o MCP não estiver autenticado, pare e peça o login. Sem MCP, o analista manda o arquivo da peça (jpg/png/mp4) — a análise visual continua obrigatória.

## Ordem (campeão, um de cada vez)

1. Achar o `ad_id` do campeão (não o conjunto, não a campanha).
2. Puxar o criativo.
3. Baixar a mídia **local**.
4. **Assistir / ler** a peça.
5. Puxar KPIs + curva de retenção de W-1 (e W-2 se existir).
6. Cruzar o que viu com o que o usuário fez. Só então escrever `worked`, `angle`, `script`, `retention.drop` e `hypothesis`.

Não inventar roteiro. Se não deu para abrir a mídia, o slide declara o buraco e a hipótese não fala de gancho visual.

## Tools (Pipeboard e equivalentes)

Mapear pelo que a tool faz. No Pipeboard:

| Intenção | Tool típica |
|---|---|
| Conta | `mcp_meta_ads_get_ad_accounts` |
| Ads da campanha | `mcp_meta_ads_get_ads` (`campaign_id`) |
| Detalhe do ad | `mcp_meta_ads_get_ad_details` |
| Copy + IDs da peça | `mcp_meta_ads_get_ad_creatives` |
| Ver a imagem | `mcp_meta_ads_get_ad_image` |
| KPIs e vídeo | `mcp_meta_ads_get_insights` no **ad** |

Outro MCP: mesma sequência (`get_ads` → `get_ad_creatives` / `get_creative_assets` → `get_insights` / `get_video_performance` → `get_video_sources`).

Insights no nível **ad**, recorte W-1 (`time_range` seg–dom BRT). Pedir campos extras de vídeo se a tool aceitar `fields`. Se não aceitar, usar o que vier e completar com Graph API (abaixo).

## Mídia

### Imagem / estático / card de carrossel

1. `get_ad_creatives` + `get_ad_image` (ou URL `thumbnail_url` / `image_url` / `permalink_url`).
2. Baixar para `/tmp/analise-criativa-media/{ad_id}.jpg`.
3. **Abrir o arquivo de imagem** (visão). Descrever: cena, pessoa, produto, texto na tela, oferta, CTA, fundo, “cara de anúncio” vs UGC.
4. `creative.kind` = `image` (ou `carousel`). `creative.file` = caminho local. Carrossel: baixar os cards; no slide vai o card 1; no roteiro listar a ordem.

### Vídeo

`get_ad_image` sozinho **não basta**. Precisa do arquivo.

1. No criativo: `video_id` (`object_story_spec.video_data.video_id` ou `video_id`).
2. Source + poster:

```
GET /{video-id}?fields=source,picture,length,title
```

Ou tool tipo `get_video_sources` / `meta_get_video_sources`. `source` expira — baixar na hora.

3. Gravar `/tmp/analise-criativa-media/{ad_id}.mp4` e o poster `{ad_id}-poster.jpg`.
4. Extrair frames (ffmpeg):

```bash
ffmpeg -y -ss 0 -i /tmp/analise-criativa-media/{ad_id}.mp4 -frames:v 1 /tmp/analise-criativa-media/{ad_id}-t0.jpg
ffmpeg -y -ss 3 -i /tmp/analise-criativa-media/{ad_id}.mp4 -frames:v 1 /tmp/analise-criativa-media/{ad_id}-t3.jpg
```

Mais dois: metade da duração e o último segundo (`-sseof -1`). Abrir **os quatro frames**. Se der para transcrever o áudio, transcrever. Se não der, o roteiro sai do que está na tela + copy do criativo (`title`, `body`, `message`).

5. `creative.kind` = `video`. `creative.file` = poster ou `t0`. `creative.video` = mp4. `creative.duration` = duração.

## KPIs de retenção (vídeo)

Pedir no insights do ad:

- `actions` (video_view = 3s)
- `video_continuous_2_sec_watched_actions`
- `video_p25_watched_actions`
- `video_p50_watched_actions`
- `video_p75_watched_actions`
- `video_p95_watched_actions`
- `video_p100_watched_actions`
- `video_thruplay_watched_actions`
- `video_avg_time_watched_actions`
- `video_play_curve_actions`

Fórmulas em [metricas.md](metricas.md).

`video_play_curve_actions[0].value` é a curva: índice 0–14 = segundos 0–14; 15–17 = 15–20s, 20–25s, 25–30s. Cada número = % dos plays que chegaram naquele ponto.

**Queda:** maior tombo entre dois pontos consecutivos **dentro da duração da peça**. Escrever em linguagem de cliente: “no 6s, quando some o rosto e entra o pote”. Cruzar o segundo da curva com o frame daquele segundo. Sem isso, não chutar o miolo.

Estático: retenção = “—”. Não fabricar hook/hold.

## O que a análise tem que amarrar

| Viu na peça | Confere no número |
|---|---|
| Gancho (1º segundo / thumb) | Hook 3s vs peers da campanha |
| Miolo (prova, rotina, fala) | Queda na curva; hold 50% |
| CTA / oferta na tela | CTR e, se o clique veio, conversão |
| Ângulo (hábito, dor, antes/depois, desconto) | Quem clica compra? CPA/ROAS |

`worked` cita **o que está na peça** + o KPI. Proibido “UGC funciona” sem dizer o gancho e o segundo da queda.

## Graph API se o MCP não baixar o vídeo

```
GET /{ad-id}?fields=id,name,creative{id,thumbnail_url,object_story_spec,asset_feed_spec,video_id,image_url}
GET /{ad-id}/insights?fields=spend,impressions,reach,frequency,cpm,ctr,inline_link_clicks,actions,action_values,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions,video_thruplay_watched_actions,video_avg_time_watched_actions,video_play_curve_actions,video_continuous_2_sec_watched_actions&time_range={since,until}
GET /{video-id}?fields=source,picture,length
```

`thumbnail_width` / `thumbnail_height` altos (ex.: 720×1280) quando pedir `thumbnail_url`.

## Caminhos no JSON

Tudo local, não URL da CDN (expira e o PPT quebra). Relativo à skill ou absoluto:

- `creative.file` — imagem ou poster
- `creative.video` — mp4 do campeão, se existir
