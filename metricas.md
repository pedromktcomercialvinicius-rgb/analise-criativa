# Métricas canônicas — análise criativa

Fórmulas usam **totais da semana** (não média das médias). Clique = **clique de link**. Sem dado ou divisão por zero = “—”.

Recorte da tabela: gasto **> R$ 15**, **por campanha**, top 10 por gasto. Mediana e “acima do mix” = peers da mesma campanha.

## Campeão da etapa

Nas três telas de dados, coroar **um** ad da campanha:

- Competitividade → menor CPM
- Atratividade → maior CTR de link
- Conversão → maior ROAS com compra (sem compra = sem campeão)

O número vai no `why` (“CPM R$ 19,78”, “CTR 2,10%”, “ROAS 4,80x”).

## Competitividade

O anúncio está barato ou caro para aparecer?

| Indicador | Fórmula |
|---|---|
| Alcance | soma |
| Impressões | soma |
| Frequência | impressões ÷ alcance |
| CPM | valor gasto ÷ impressões × 1.000 |
| Valor gasto | soma |

## Atratividade

Parou no feed e clicou? Vídeo sem 3s = “—” em hook/hold/ThruPlay. Estático e carrossel sem vídeo = “—” nessas três.

| Indicador | Fórmula | Lê o quê |
|---|---|---|
| Cliques | cliques de link | volume de saída do feed |
| CTR | cliques de link ÷ impressões | quis clicar? |
| CPC | valor gasto ÷ cliques de link | o clique está caro? |
| Hook rate | visualizações 3s ÷ impressões | parou no 1º segundo? |
| Hold 50% | visualizações 50% ÷ visualizações 3s | segurou o meio? |
| ThruPlay | ThruPlay ÷ impressões | foi até o fim? |

Não usar clique total no lugar de clique de link.

**Leitura cruzada**

- Hook baixo → gancho/thumb. Pedido de abertura, não de landing.
- Hook ok + hold baixo → miolo fraco.
- Hook/hold ok + CTR baixo → CTA.
- CTR ok + conversão ruim → não é peça de feed; olhar Conversão.

## Conversão

O clique vira dinheiro? Cada etapa: **volume, taxa vs etapa anterior, CPA**.

| Indicador | Fórmula |
|---|---|
| Pageview | landing page views |
| Tx PV | pageview ÷ cliques de link |
| CPA pageview | gasto ÷ pageview (só no slide de campeão, se couber) |
| C.C | add to cart (mesmo sentido do Excel: evento de carrinho) |
| Tx carrinho | C.C ÷ pageview |
| CPA carrinho | gasto ÷ C.C |
| Compras | compras da plataforma |
| Tx compras | compras ÷ C.C |
| Receita | valor de conversão |
| CPA | gasto ÷ compras |
| ROAS | receita ÷ gasto |

Se pageview não existir na extração, tx carrinho = C.C ÷ cliques, e a nota do slide declara isso. Não zerar.

Taxa vs impressão (como o 0,08% do Excel antigo) **não** entra no PPT — esconde o gargalo.

C.C, tx carrinho e CPA carrinho ficam **neste bloco**, não em Atratividade. Carrinho já é intenção no site.

## Campeão (slide)

Além do W-1, mostrar W-2 quando existir: hook, CTR, frequência, ROAS. Sem W-2 = “—”.

O slide **mostra a peça**: imagem no estático; no vídeo, o frame (e o mp4 no JSON para o agente ter assistido). Sem arquivo local, o quadro da peça fica vazio — não usar print genérico.

### Retenção (só vídeo)

Até onde o usuário ficou? Taxa = views daquele marco ÷ impressões, salvo hold.

| Indicador | Campo Meta | Fórmula | Lê o quê |
|---|---|---|---|
| Hook 3s | `actions` video_view | views 3s ÷ impressões | parou no gancho? |
| 25% | `video_p25_watched_actions` | p25 ÷ impressões | passou da abertura? |
| Hold 50% | `video_p50_watched_actions` | p50 ÷ views 3s | segurou o miolo? |
| 75% | `video_p75_watched_actions` | p75 ÷ impressões | chegou perto do CTA? |
| Fim / ThruPlay | `video_p100` ou `video_thruplay_watched_actions` | ÷ impressões | foi até o fim? |
| Tempo médio | `video_avg_time_watched_actions` | segundos | quanto ficou, em média |

**Curva** (`video_play_curve_actions`): % dos plays em cada segundo (0–14 = segundo a segundo). A **queda** é o maior tombo consecutivo ainda dentro da duração. Escrever o segundo **e** a cena (“no 6s some o rosto”). Sem cruzar curva × frame, não afirmar onde perdeu gente.

Estático / carrossel sem vídeo: todas essas células = “—”.
