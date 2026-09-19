# Fontes de dados

Este relatório é **Meta Ads, nível anúncio, W-1**.

## Neste projeto (GrowthOS)

Ainda **não há dados de ads no banco**. Não consultar Lovable Cloud, não inventar extração, não puxar o FUP de outra base e fingir que é criativo.

Até existir tabela no Supabase:

1. Usar a planilha / CSV / print que o usuário mandar.
2. Mapear colunas para [metricas.md](metricas.md).
3. Se faltar hook, hold, ThruPlay ou pageview, a célula é “—” e a capa/leitura declara o buraco. Não estimar.

Quando o Supabase deste app tiver fato diário de anúncio, este arquivo aponta a tabela. Até lá, a fonte é o arquivo da semana.

## O que o arquivo precisa ter

Mínimo para competitividade: anúncio, alcance, impressões, gasto.

Mínimo para atratividade: cliques de link (ou cliques, se só isso vier — declarar).

Mínimo para conversão: compras, receita. Sem isso não há campeão de retorno.

Desejável: frequência (ou alcance para calcular), CPM (ou calcular), CTR/CPC (ou calcular), video 3s / p50 / ThruPlay, pageview, add to cart.

## Google e GA4

- **Google:** fora do deck semanal. Nota na capa: replica campeões de Meta a cada 14 dias.
- **GA4:** não ranqueia anúncio salvo `utm_content` com o nome da peça. Não misturar compra GA com compra Meta na mesma coluna.

## Recorte de anúncio

Uma linha = um anúncio da semana com gasto **> R$ 15**. Ads com R$ 15 ou menos não entram na tabela (contam em `below_floor` da campanha). Não misturar conjunto com ad.

**Capa — campanhas ativas:** nomes distintos de campanha Meta com gasto > 0 em W-1. Ordenar por gasto. O total do quadro = quantidade dessas campanhas.

**Dados — por campanha:** cada campanha vira um bloco de 3 slides. Comparar só ads daquela campanha. Top 10 por gasto, ordem travada nas três etapas.
