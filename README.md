# Análise criativa

Skill para montar o **deck semanal de criativos Meta Ads** em PowerPoint: competitividade, atratividade (com hook rate) e conversão, depois campeões e pedido de novos anúncios.

## O que faz

- PPT 16:9 para o cliente (especialista apresenta)
- Só Meta; Google replica campeões a cada 14 dias (fora deste deck)
- Anúncio com gasto **> R$ 15** na semana; top 10 **por campanha**
- 3 telas de dados por campanha (mesmos ads, mesma ordem)
- Até 3 slides de campeão: peça na tela (imagem ou vídeo/frame), roteiro, ângulo, retenção, hipótese
- Pedido = DNA do campeão + 1–2 ideias novas

## Instalar

### Cursor

```bash
git clone https://github.com/pedromktcomercialvinicius-rgb/analise-criativa.git ~/.cursor/skills/analise-criativa
chmod +x ~/.cursor/skills/analise-criativa/scripts/run.sh
```

Ou, num projeto:

```bash
git clone https://github.com/pedromktcomercialvinicius-rgb/analise-criativa.git .cursor/skills/analise-criativa
```

Na primeira geração o `run.sh` cria um venv e instala `python-pptx`. Depois peça: “faz a análise criativa da [conta]”.

### Claude Code / Codex / outras IAs com Agent Skills

Clone a pasta para o diretório de skills da ferramenta (ex.: `~/.claude/skills/analise-criativa`) ou anexe os arquivos `.md` no chat.

O contrato da skill é o `SKILL.md`. As outras IAs não “puxam o GitHub sozinhas”: elas precisam da pasta no projeto ou dos arquivos colados/anexados.

## Arquivos

| Arquivo | Função |
|---|---|
| `SKILL.md` | Ordem do deck, regras, como gerar o PPT |
| `metricas.md` | Fórmulas dos 3 blocos |
| `fontes.md` | De onde vem o dado (planilha até o banco existir) |
| `meta-mcp.md` | Como o MCP da Meta baixa a peça, assiste e lê a retenção |
| `schema.md` | JSON que o script espera |
| `exemplo.md` | Bom vs ruim |
| `scripts/run.sh` | Cria venv e gera o `.pptx` |
| `scripts/build_pptx.py` | Monta os slides |
| `scripts/exemplo.json` | Fixture para testar o script |
