---
name: analise-criativa
description: >-
  Gera análise criativa semanal de Meta Ads em PowerPoint (visão de anúncio):
  competitividade, atratividade (CTR, hook rate, hold, ThruPlay) e conversão
  (funil pageview → carrinho → compra), classifica campeões, hipóteses do que
  funcionou e pedidos de novos ads a partir do DNA. Use when the user asks for
  análise criativa, relatório de criativos, deck de ads, PPT de criativos,
  campeões de Facebook/Meta, or pedido de novos anúncios.
---

# Análise criativa (Meta Ads → PPT)

Deck para o **cliente**, apresentado pelo especialista. Tom direto, em português. Visão de **anúncio**. Não reabre o FUP. Não mistura Google neste relatório.

Antes de montar números, leia [metricas.md](metricas.md). Fontes: [fontes.md](fontes.md). Exemplo bom vs ruim: [exemplo.md](exemplo.md). Schema do JSON: [schema.md](schema.md).

## Quando usar

Pedido de análise criativa, relatório de criativos da terça, deck/PPT de ads, campeões de Facebook, o que funcionou na peça, ou pedido de novos anúncios para nutrir a conta.

## Recorte

- **Só Meta Ads.** Google replica os campeões de Facebook a cada 14 dias — uma linha na capa, sem seção Google.
- **W-1** = última semana fechada (seg–dom, `America/Sao_Paulo`). Comparar com **W-2** na leitura e nos campeões.
- Unidade: **anúncio** (nome / ad). Se o mesmo vídeo estiver em vários ads, o DNA agrupa no texto do campeão; a tabela continua no ad.
- **Piso de gasto:** entra só anúncio com gasto **> R$ 15** em W-1. R$ 15,00 ou menos fica de fora da análise (ruído). Anotar quantos saíram, por campanha (`below_floor`).
- **Análise por campanha.** Ad só compete com peer da **mesma** campanha. Não ranquear a conta inteira numa tabela só.
- Dentro da campanha: ordenar por valor gasto (maior primeiro), ficar com os **top 10**. Essa lista trava: as três etapas usam **os mesmos 10, na mesma ordem**.
- **Campanhas ativas na capa:** campanha Meta distinta com gasto > 0 em W-1. O quadro mostra o **total**. A tabela lista até 8, por gasto. Pausada sem gasto não entra. Campanha só com ads ≤ R$ 15 ainda pode aparecer na capa, sem slides de dados.
- Sem amostra inventada. Sem `#DIV/0!`. Sem dado = “—”.

## Por que 3 telas de dados (não 1 tabela)

PPT 16:9 não cabe competitividade + atratividade + conversão numa grade só com nome de anúncio legível. Uma tabela única vira fonte 8pt — inútil para cliente.

**Por campanha, três slides, mesmos anúncios, mesma ordem:**

1. Competitividade · [campanha]
2. Atratividade · [campanha]
3. Conversão · [campanha]

O olho acompanha a linha. Não paginar além do top 10. Não misturar campanhas na mesma página.

## Estrutura do PPT (obrigatória)

Nesta ordem:

1. **Capa** — conta, semana W-1 vs W-2, investimento Meta, ROAS, % da receita na peça líder, **campanhas ativas (total + lista)**. Nota: Google fora deste deck.
2. **Leitura** — 2–4 frases em linguagem de cliente. Três caixas: segue performando / perdeu força / sai de linha.
3. **Por campanha** — 1 página de Competitividade + 1 de Atratividade + 1 de Conversão (top 10, mesma ordem). Depois, se houver, o slide do campeão **dessa** campanha.
4. **Pedido · DNA** — variações com a campanha no pedido: copia 1 coisa, muda 1 variável. Critério de leitura.
5. **Pedido · ideias novas** — 1–2 apostas com teto, explícitas como teste. Fecha com o que **não** pedimos nesta semana.

Não entregar JSON solto no lugar do PPT. Não entregar Doc. A entrega é o `.pptx`.

## Linguagem (cliente)

| Interno | No slide |
|---|---|
| Campeão | Segue performando |
| Saturado | Perdeu força |
| Promessa | Ainda cedo |
| Matar | Sai de linha |

Saturação só aparece se **frequência subiu e CTR/hook caiu** juntos. “O criativo morreu” no slide é erro. Hipótese ≠ fato.

Não usar jargão de leilão (Advantage+, CPM de leilão, sessão cega) no corpo. Se precisar, uma nota de rodapé.

## Como classificar

- **Segue performando** — competitividade ok + atratividade acima da mediana da **campanha** + CPA/ROAS melhor que o canal, com amostra.
- **Ainda cedo** — sinal bom, gasto baixo demais para cravar. Não escalar.
- **Perdeu força** — frequência alta **e** queda de hook/CTR vs W-2.
- **Sai de linha** — competitividade cara + atratividade ruim + conversão ruim, com amostra.

Máximo **3 slides de campeão** no deck. Campeão é da campanha (não da conta). Priorizar ROAS/CPA com gasto material **dentro da campanha**. DNA só desses.

## Pedido de novos ads

Nutrir a conta. Não é “fazer criativo”.

- **DNA (obrigatório):** cada linha traz a **campanha**, copia 1 coisa do campeão e muda 1 variável. Recorte, quantidade, critério (5 dias ou piso de gasto).
- **Ideias novas (1–2):** teto de verba. Marcadas como teste. Não substituem o DNA.
- **O que não pedir** nesta semana — sempre no último slide.
- Máximo 5 pedidos no total (DNA + novas). Se 1 ad concentrar 50%+ da receita, prioridade 1 é variação do líder.

## Como produzir

1. Ler [metricas.md](metricas.md) e [fontes.md](fontes.md).
2. Pegar a tabela de anúncios (planilha colada, CSV, ou o que o usuário mandar). Não inventar linha.
3. Classificar. Escolher até 3 campeões. Escrever hipóteses e pedidos.
4. Gravar JSON no schema de [schema.md](schema.md) (ex.: `/tmp/analise-criativa.json`).
5. Gerar o PPT:

```bash
~/.cursor/skills/analise-criativa/scripts/run.sh \
  /tmp/analise-criativa.json \
  ~/Downloads/analise-criativa-{conta}-W1-{data}.pptx
```

O `run.sh` cria um venv local e instala `python-pptx` na primeira vez. Não usar o Python do sistema.

6. Abrir o arquivo e conferir o checklist. Entregar o caminho do `.pptx`.

## Checklist antes de entregar

- [ ] Só Meta; Google só na nota da capa
- [ ] Capa com total de campanhas ativas (gasto em W-1) e a lista
- [ ] Só ads com gasto > R$ 15; por campanha; top 10 por gasto
- [ ] 3 telas por campanha, mesmas linhas, mesma ordem
- [ ] Atratividade tem hook / hold 50% / ThruPlay (vídeo) ou “—”
- [ ] Clique = clique de link
- [ ] Conversão tem pageview, C.C/carrinho e compras (volume, taxa vs etapa anterior, CPA)
- [ ] Sem compra → “—”, não #DIV/0!
- [ ] ≤ 3 slides de campeão, cada um com hipótese do que funcionou
- [ ] Pedido DNA + 1–2 ideias novas + o que não pedir
- [ ] Arquivo `.pptx` gerado pelo script, não HTML
