#!/usr/bin/env python3
"""Gera o PPT 16:9 da análise criativa a partir do JSON da skill."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.45)

INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x5C, 0x5C, 0x5C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RULE = RGBColor(0xDD, 0xDD, 0xDD)
ROW = RGBColor(0xF7, 0xF7, 0xF7)

HEADER = {
    "competitiveness": RGBColor(0x1A, 0x1A, 0x1A),
    "attractiveness": RGBColor(0x4A, 0x4A, 0x4A),
    "conversion": RGBColor(0x2F, 0x3A, 0x32),
}

ROWS_PER_SLIDE = 10


def dash(value) -> str:
    if value is None:
        return "—"
    text = str(value).strip()
    return text if text else "—"


def set_run(run, *, size=14, bold=False, color=INK, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_text(slide, l, t, w, h, text, *, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color)
    return box


def add_act(slide, act: str, title: str):
    add_text(slide, MARGIN, Inches(0.22), Inches(12.4), Inches(0.28), act, size=11, color=MUTED)
    add_text(slide, MARGIN, Inches(0.42), Inches(12.4), Inches(0.42), title, size=22, bold=True)


def fill_cell(cell, text, *, size=11, bold=False, fill=None, color=INK, align=PP_ALIGN.CENTER):
    cell.text = ""
    if fill is not None:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
    else:
        cell.fill.background()
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = dash(text)
    set_run(run, size=size, bold=bold, color=color)
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for edge in ("lnL", "lnR", "lnT", "lnB"):
        existing = tcPr.find(qn(f"a:{edge}"))
        if existing is not None:
            tcPr.remove(existing)
        ln = tcPr.makeelement(qn(f"a:{edge}"), {})
        ln.set("w", str(Emu(6350)))
        srgb = ln.makeelement(qn("a:solidFill"), {})
        srgb_clr = srgb.makeelement(qn("a:srgbClr"), {"val": "DDDDDD"})
        srgb.append(srgb_clr)
        ln.append(srgb)
        tcPr.append(ln)


def add_table(slide, headers, rows, *, left, top, width, height, header_fill):
    table_shape = slide.shapes.add_table(1 + len(rows), len(headers), left, top, width, height)
    table = table_shape.table
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        fill_cell(cell, header, size=10, bold=True, fill=header_fill, color=WHITE, align=PP_ALIGN.CENTER)
    for r, row in enumerate(rows, start=1):
        bg = WHITE if r % 2 else ROW
        for c, value in enumerate(row):
            align = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.RIGHT
            fill_cell(table.cell(r, c), value, size=10, fill=bg, color=INK, align=align)
    return table


def chunk(items, n):
    for i in range(0, len(items), n):
        yield i // n, items[i : i + n]


def blank_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    return slide


def cover(prs, data):
    slide = blank_slide(prs)
    add_text(slide, MARGIN, Inches(1.8), Inches(12), Inches(0.35), "Análise criativa · Meta Ads", size=14, color=MUTED)
    add_text(slide, MARGIN, Inches(2.15), Inches(12), Inches(0.7), data["client"], size=36, bold=True)
    add_text(
        slide,
        MARGIN,
        Inches(2.9),
        Inches(12),
        Inches(0.4),
        f"Semana {data['week_label']}  ·  comparado com {data['week_compare']}",
        size=16,
        color=MUTED,
    )
    add_text(
        slide,
        MARGIN,
        Inches(3.4),
        Inches(12),
        Inches(0.4),
        "Visão de anúncio. O que performou, o que cansou, o que pedimos agora.",
        size=14,
    )

    kpis = [
        (data.get("spend", "—"), "Investimento Meta"),
        (data.get("roas", "—"), "ROAS da semana"),
        (data.get("concentration", "—"), "Receita na peça líder"),
    ]
    for i, (value, label) in enumerate(kpis):
        left = MARGIN + Inches(i * 4.1)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(4.3), Inches(3.8), Inches(1.35))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0xF3, 0xF3, 0xF3)
        shape.line.color.rgb = RULE
        add_text(slide, left + Inches(0.2), Inches(4.45), Inches(3.4), Inches(0.55), value, size=24, bold=True)
        add_text(slide, left + Inches(0.2), Inches(5.05), Inches(3.4), Inches(0.4), label, size=12, color=MUTED)

    add_text(
        slide,
        MARGIN,
        Inches(6.85),
        Inches(12.4),
        Inches(0.35),
        "Google Ads não entra neste relatório. A cada 14 dias replicamos os campeões de Facebook no Demand Gen.",
        size=11,
        color=MUTED,
    )


def reading(prs, data):
    slide = blank_slide(prs)
    add_act(slide, "2 · Dados", "O que a semana mostrou")
    add_text(slide, MARGIN, Inches(1.0), Inches(12.4), Inches(1.1), data.get("reading", ""), size=16)

    buckets = data.get("buckets") or {}
    labels = [
        ("Segue performando", buckets.get("performing") or []),
        ("Perdeu força", buckets.get("weak") or []),
        ("Sai de linha", buckets.get("kill") or []),
    ]
    for i, (title, items) in enumerate(labels):
        left = MARGIN + Inches(i * 4.2)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(2.3), Inches(4.0), Inches(4.4))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0xF7, 0xF7, 0xF7)
        shape.line.color.rgb = RULE
        add_text(slide, left + Inches(0.2), Inches(2.45), Inches(3.6), Inches(0.4), title, size=16, bold=True)
        body = "\n".join(f"· {item}" for item in items) or "—"
        add_text(slide, left + Inches(0.2), Inches(2.95), Inches(3.6), Inches(3.5), body, size=13)


def data_block(prs, data, kind: str):
    specs = {
        "competitiveness": {
            "act": "2 · Dados",
            "title": "Competitividade",
            "subtitle": "O anúncio está barato ou caro para aparecer?",
            "headers": ["Anúncio", "Alcance", "Impressões", "Frequência", "CPM", "Valor gasto"],
            "keys": ["reach", "impressions", "frequency", "cpm", "spend"],
            "fill": HEADER["competitiveness"],
        },
        "attractiveness": {
            "act": "2 · Dados",
            "title": "Atratividade",
            "subtitle": "Parou no feed e clicou? Hook / hold / ThruPlay só em vídeo.",
            "headers": ["Anúncio", "Cliques", "CTR", "CPC", "Hook rate", "Hold 50%", "ThruPlay"],
            "keys": ["clicks", "ctr", "cpc", "hook", "hold", "thruplay"],
            "fill": HEADER["attractiveness"],
        },
        "conversion": {
            "act": "2 · Dados",
            "title": "Conversão",
            "subtitle": "Funil: pageview → carrinho → compra. Taxa vs etapa anterior.",
            "headers": [
                "Anúncio",
                "Pageview",
                "Tx PV",
                "C.C",
                "Tx carrinho",
                "CPA carrinho",
                "Compras",
                "Tx compras",
                "Receita",
                "CPA",
                "ROAS",
            ],
            "keys": [
                "pageview",
                "tx_pv",
                "cart",
                "tx_cart",
                "cpa_cart",
                "purchases",
                "tx_purchases",
                "revenue",
                "cpa",
                "roas",
            ],
            "fill": HEADER["conversion"],
        },
    }
    spec = specs[kind]
    ads = data.get("ads") or []
    pages = list(chunk(ads, ROWS_PER_SLIDE)) or [(0, [])]
    total = len(pages)

    for page_i, group in pages:
        slide = blank_slide(prs)
        suffix = f"  ({page_i + 1}/{total})" if total > 1 else ""
        add_act(slide, spec["act"], spec["title"] + suffix)
        add_text(slide, MARGIN, Inches(0.88), Inches(12.4), Inches(0.32), spec["subtitle"], size=12, color=MUTED)

        rows = []
        for ad in group:
            block = ad.get(kind) or {}
            row = [dash(ad.get("name"))]
            for key in spec["keys"]:
                row.append(dash(block.get(key)))
            rows.append(row)

        add_table(
            slide,
            spec["headers"],
            rows,
            left=MARGIN,
            top=Inches(1.25),
            width=Inches(12.4),
            height=Inches(5.7),
            header_fill=spec["fill"],
        )


def champion(prs, item, index, total):
    slide = blank_slide(prs)
    add_act(slide, "3 · Criativos", f"Campeão {index} de {total}")
    add_text(slide, MARGIN, Inches(0.95), Inches(12.4), Inches(0.45), item.get("name", ""), size=26, bold=True)
    add_text(slide, MARGIN, Inches(1.4), Inches(12.4), Inches(0.35), item.get("meta", ""), size=13, color=MUTED)

    stats = (item.get("stats") or [])[:4]
    for i, stat in enumerate(stats):
        left = MARGIN + Inches(i * 3.2)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.9), Inches(3.05), Inches(1.25))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0xF3, 0xF3, 0xF3)
        shape.line.color.rgb = RULE
        add_text(slide, left + Inches(0.15), Inches(2.0), Inches(2.75), Inches(0.5), dash(stat.get("value")), size=22, bold=True)
        add_text(slide, left + Inches(0.15), Inches(2.5), Inches(2.75), Inches(0.5), dash(stat.get("label")), size=11, color=MUTED)

    add_text(slide, MARGIN, Inches(3.35), Inches(12.4), Inches(0.35), "O que funcionou", size=16, bold=True)
    worked = item.get("worked") or []
    add_text(
        slide,
        MARGIN,
        Inches(3.75),
        Inches(12.4),
        Inches(1.5),
        "\n".join(f"· {line}" for line in worked) or "—",
        size=14,
    )

    hypo = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, MARGIN, Inches(5.4), Inches(12.4), Inches(1.55))
    hypo.fill.solid()
    hypo.fill.fore_color.rgb = RGBColor(0xEE, 0xF3, 0xF0)
    hypo.line.color.rgb = RGBColor(0x2F, 0x3A, 0x32)
    add_text(slide, MARGIN + Inches(0.25), Inches(5.5), Inches(11.9), Inches(0.3), "Hipótese", size=12, bold=True, color=RGBColor(0x2F, 0x3A, 0x32))
    add_text(slide, MARGIN + Inches(0.25), Inches(5.85), Inches(11.9), Inches(0.95), dash(item.get("hypothesis")), size=14)


def dna_slide(prs, data):
    slide = blank_slide(prs)
    add_act(slide, "4 · Pedido", "Mais anúncios a partir do DNA que já funciona")
    add_text(
        slide,
        MARGIN,
        Inches(0.95),
        Inches(12.4),
        Inches(0.4),
        "Copiar uma coisa do campeão. Trocar uma coisa. Sem mudar oferta nesta leva.",
        size=13,
        color=MUTED,
    )
    reqs = data.get("dna_requests") or []
    rows = [
        [dash(r.get("name")), dash(r.get("copy")), dash(r.get("change")), dash(r.get("qty")), dash(r.get("criteria"))]
        for r in reqs
    ] or [["—", "—", "—", "—", "—"]]
    add_table(
        slide,
        ["Pedido", "Copia", "Muda", "Qtde", "Como sabemos que funcionou"],
        rows,
        left=MARGIN,
        top=Inches(1.45),
        width=Inches(12.4),
        height=Inches(5.4),
        header_fill=HEADER["competitiveness"],
    )


def ideas_slide(prs, data):
    slide = blank_slide(prs)
    add_act(slide, "4 · Pedido", "Ideias novas — teste, não campeão")
    ideas = data.get("new_ideas") or []
    for i, idea in enumerate(ideas[:2]):
        left = MARGIN + Inches(i * 6.3)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.15), Inches(6.05), Inches(3.15))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0xF7, 0xF7, 0xF7)
        shape.line.color.rgb = RULE
        add_text(slide, left + Inches(0.25), Inches(1.3), Inches(5.55), Inches(0.45), dash(idea.get("name")), size=16, bold=True)
        add_text(slide, left + Inches(0.25), Inches(1.85), Inches(5.55), Inches(1.3), dash(idea.get("why")), size=13)
        add_text(slide, left + Inches(0.25), Inches(3.3), Inches(5.55), Inches(0.7), dash(idea.get("cap")), size=12, color=MUTED)

    add_text(slide, MARGIN, Inches(4.5), Inches(12.4), Inches(0.35), "O que não pedimos nesta semana", size=16, bold=True)
    do_not = data.get("do_not") or []
    add_text(
        slide,
        MARGIN,
        Inches(4.95),
        Inches(12.4),
        Inches(1.6),
        "\n".join(f"· {line}" for line in do_not) or "—",
        size=14,
    )
    add_text(
        slide,
        MARGIN,
        Inches(6.85),
        Inches(12.4),
        Inches(0.3),
        "Próximo passo interno: Google replica os campeões desta lista daqui a 14 dias.",
        size=11,
        color=MUTED,
    )


def build(data: dict, output: Path) -> Path:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    cover(prs, data)
    reading(prs, data)
    data_block(prs, data, "competitiveness")
    data_block(prs, data, "attractiveness")
    data_block(prs, data, "conversion")
    champions = data.get("champions") or []
    for i, item in enumerate(champions[:3], start=1):
        champion(prs, item, i, min(len(champions), 3))
    dna_slide(prs, data)
    ideas_slide(prs, data)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))
    return output


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("uso: build_pptx.py <input.json> [saida.pptx]", file=sys.stderr)
        return 2
    source = Path(argv[0]).expanduser()
    dest = Path(argv[1]).expanduser() if len(argv) > 1 else Path.cwd() / "analise-criativa.pptx"
    data = json.loads(source.read_text(encoding="utf-8"))
    path = build(data, dest)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
