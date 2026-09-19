# Schema do JSON → PPT

O script `scripts/build_pptx.py` lê um JSON e grava `.pptx`. Não pular campo obrigatório. String vazia vira “—”.

O agente filtra **antes** de gravar o JSON: gasto **> R$ 15**, agrupa por campanha, ordena por gasto, corta em 10. O script só usa os 10 primeiros de `campaigns[].ads` e mantém essa ordem nas três etapas.

```json
{
  "client": "Oficialnutri",
  "week_label": "07–13/09/2026",
  "week_compare": "31/08–06/09/2026",
  "spend": "R$ 45 mil",
  "roas": "3,21x",
  "concentration": "40%",
  "active_campaigns": [
    { "name": "Advantage+ NC Regepepty", "spend": "R$ 39,2 mil" },
    { "name": "Advantage+ RC kit", "spend": "R$ 2,4 mil" }
  ],
  "reading": "2–4 frases. Fato e número. Linguagem de cliente.",
  "buckets": {
    "performing": ["Advantage+ NC · UGC Rotina 15s · ROAS 4,8x"],
    "weak": ["Advantage+ NC · Depoimento Ana 30s · freq. 3,4 e CTR −36%"],
    "kill": ["Advantage+ NC · Estático Off 20% · ROAS 0,8x"]
  },
  "campaigns": [
    {
      "name": "Advantage+ NC Regepepty",
      "spend": "R$ 39,2 mil",
      "below_floor": 2,
      "stage_winners": {
        "competitiveness": { "name": "UGC Rotina 15s", "why": "CPM R$ 19,78 — o mais barato para aparecer" },
        "attractiveness": { "name": "UGC Rotina 15s", "why": "CTR 1,82% · hook 38%" },
        "conversion": { "name": "UGC Rotina 15s", "why": "ROAS 4,80x · CPA R$ 205" }
      },
      "ads": [
        {
          "name": "UGC Rotina 15s",
          "tone": "performing",
          "competitiveness": {
            "reach": "410.000",
            "impressions": "920.000",
            "frequency": "2,2",
            "cpm": "R$ 19,78",
            "spend": "R$ 18.200"
          },
          "attractiveness": {
            "clicks": "16.750",
            "ctr": "1,82%",
            "cpc": "R$ 1,09",
            "hook": "38%",
            "hold": "18%",
            "thruplay": "9%"
          },
          "conversion": {
            "pageview": "4.850",
            "tx_pv": "29%",
            "cart": "612",
            "tx_cart": "12,6%",
            "cpa_cart": "R$ 29,74",
            "purchases": "89",
            "tx_purchases": "14,5%",
            "revenue": "R$ 87.360",
            "cpa": "R$ 205",
            "roas": "4,80x"
          }
        }
      ],
      "champion": {
        "name": "UGC Rotina 15s",
        "meta": "Novos clientes · kit 3 potes · 3 semanas no ar",
        "creative": {
          "kind": "video",
          "file": "scripts/fixtures/ugc-rotina.png",
          "video": "",
          "duration": "15s"
        },
        "script": {
          "hook": "“eu tomo isso todo dia antes do café”",
          "body": "Rotina de manhã, kit na pia, sem % na tela.",
          "cta": "kit 3 potes no fim, sem fala de desconto",
          "on_screen": "rosto + pote; oferta só no objeto"
        },
        "angle": "Hábito / prova de uso, não depoimento clínico.",
        "retention": {
          "hook": "38%",
          "p25": "28%",
          "p50": "18%",
          "p75": "12%",
          "p100": "9%",
          "avg_time": "4,2s",
          "drop": "Queda no 6s — some o rosto e entra o pote fechado."
        },
        "stats": [
          { "value": "4,8x", "label": "ROAS (4,6x na semana passada)" },
          { "value": "38%", "label": "Hook rate" },
          { "value": "1,82%", "label": "CTR de link" },
          { "value": "2,2", "label": "Frequência" }
        ],
        "worked": [
          "Formato: UGC vertical 15s, rotina de manhã.",
          "Gancho: hábito, não depoimento clínico.",
          "Oferta: kit na cena, sem % na tela."
        ],
        "hypothesis": "O que vende é prova de hábito em 15s. A próxima leva copia este DNA e troca uma variável."
      }
    }
  ],
  "dna_requests": [
    {
      "campaign": "Advantage+ NC Regepepty",
      "name": "Rotina 15s — gancho de noite",
      "copy": "Formato 15s + kit sem % na tela",
      "change": "Abertura: rotina noturna",
      "qty": "2 peças",
      "criteria": "Hook ≥ 35% e CPA no nível do líder, 5 dias ou R$ 2 mil"
    }
  ],
  "new_ideas": [
    {
      "name": "Antes/Depois 9:16 mais curto",
      "why": "Hook 41% no teste. Abrir no resultado, 8–10s.",
      "cap": "Teto R$ 3 mil. Só lemos parada e clique."
    }
  ],
  "do_not": [
    "Novo estático de desconto.",
    "Outro depoimento de 30s no mesmo público.",
    "Mudança de oferta na peça."
  ]
}
```

`tone` do anúncio: `performing` | `weak` | `early` | `kill` | `neutral`.
`campaigns[].ads`: já filtrados (gasto > R$ 15), ordenados por gasto, no máximo 10. Essa ordem é a ordem das três etapas.
`below_floor`: quantos ads da campanha ficaram de fora por gasto ≤ R$ 15.
`stage_winners`: obrigatório por campanha com tabela. `competitiveness` | `attractiveness` | `conversion` → `{ name, why }`. Sem amostra, omitir a chave (o slide escreve “—”).
`champion` ou `champions`: opcional, por campanha. No máximo 3 slides de campeão no deck inteiro.
`creative.kind`: `video` | `image` | `carousel`. `creative.file` = caminho local da imagem ou do poster. `creative.video` = mp4 local, se houver.
Campeão de vídeo sem `retention.drop` (segundo + cena) está incompleto.
`dna_requests` + `new_ideas` ≤ 5 no total.
