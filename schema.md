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
`champion` ou `champions`: opcional, por campanha. No máximo 3 slides de campeão no deck inteiro.
`dna_requests` + `new_ideas` ≤ 5 no total.
