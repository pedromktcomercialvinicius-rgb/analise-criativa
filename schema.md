# Schema do JSON → PPT

O script `scripts/build_pptx.py` lê um JSON e grava `.pptx`. Não pular campo obrigatório. String vazia vira “—”.

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
    { "name": "Advantage+ RC kit", "spend": "R$ 2,4 mil" },
    { "name": "Teste NC Antes/Depois", "spend": "R$ 2,1 mil" },
    { "name": "Prospecting UGC testes", "spend": "R$ 1,4 mil" }
  ],
  "reading": "2–4 frases. Fato e número. Linguagem de cliente.",
  "buckets": {
    "performing": ["UGC Rotina 15s · ROAS 4,8x", "UGC Rotina v2 · ROAS 4,2x"],
    "weak": ["Depoimento Ana 30s · freq. 3,4 e CTR −36%"],
    "kill": ["Estático Off 20% · ROAS 0,8x"]
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
  "champions": [
    {
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
  ],
  "dna_requests": [
    {
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
`champions`: 1 a 3 itens. `dna_requests` + `new_ideas` ≤ 5 no total.
