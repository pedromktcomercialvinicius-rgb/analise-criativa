#!/usr/bin/env python3
"""Gera o PPT 16:9 da análise criativa a partir do JSON da skill."""

from __future__ import annotations

import json
import struct
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

TOP_ADS = 10
MIN_SPEND_BRL = 15  # exclusivo: gasto > R$ 15


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


def add_table(slide, headers, rows, *, left, top, width, height, header_fill, highlight_rows=None):
    table_shape = slide.shapes.add_table(1 + len(rows), len(headers), left, top, width, height)
    table = table_shape.table
    winners = set(highlight_rows or [])
    win_bg = RGBColor(0xEE, 0xF3, 0xF0)
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        fill_cell(cell, header, size=10, bold=True, fill=header_fill, color=WHITE, align=PP_ALIGN.CENTER)
    for r, row in enumerate(rows, start=1):
        winner = r in winners
        bg = win_bg if winner else (WHITE if r % 2 else ROW)
        for c, value in enumerate(row):
            align = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.RIGHT
            fill_cell(
                table.cell(r, c),
                value,
                size=10,
                bold=winner and c == 0,
                fill=bg,
                color=INK,
                align=align,
            )
    return table


def blank_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    return slide


def parse_campaigns(data):
    raw = data.get("active_campaigns")
    if not raw:
        raw = data.get("campaigns") or []
    rows = []
    for item in raw:
        if isinstance(item, str):
            name = item.strip()
            if name:
                rows.append((name, "—"))
            continue
        if isinstance(item, dict):
            name = dash(item.get("name"))
            if name == "—":
                continue
            rows.append((name, dash(item.get("spend"))))
    return rows


def cover(prs, data):
    slide = blank_slide(prs)
    campaigns = parse_campaigns(data)
    total = len(campaigns)

    add_text(slide, MARGIN, Inches(0.28), Inches(12.4), Inches(0.28), "Análise criativa · Meta Ads", size=14, color=MUTED)
    add_text(slide, MARGIN, Inches(0.52), Inches(12.4), Inches(0.55), data["client"], size=28, bold=True)
    add_text(
        slide,
        MARGIN,
        Inches(1.08),
        Inches(12.4),
        Inches(0.32),
        f"Semana {data['week_label']}  ·  comparado com {data['week_compare']}",
        size=14,
        color=MUTED,
    )
    add_text(
        slide,
        MARGIN,
        Inches(1.4),
        Inches(12.4),
        Inches(0.3),
        "Visão de anúncio. O que performou, o que cansou, o que pedimos agora.",
        size=13,
    )

    kpis = [
        (data.get("spend", "—"), "Investimento Meta"),
        (data.get("roas", "—"), "ROAS da semana"),
        (data.get("concentration", "—"), "Receita na peça líder"),
        (str(total), "Campanhas ativas"),
    ]
    for i, (value, label) in enumerate(kpis):
        left = MARGIN + Inches(i * 3.15)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.85), Inches(3.0), Inches(1.05))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0xF3, 0xF3, 0xF3)
        shape.line.color.rgb = RULE
        add_text(slide, left + Inches(0.15), Inches(1.95), Inches(2.7), Inches(0.45), value, size=20, bold=True)
        add_text(slide, left + Inches(0.15), Inches(2.4), Inches(2.7), Inches(0.35), label, size=11, color=MUTED)

    add_text(slide, MARGIN, Inches(3.1), Inches(12.4), Inches(0.32), f"Campanhas ativas · {total}", size=16, bold=True)
    add_text(
        slide,
        MARGIN,
        Inches(3.4),
        Inches(12.4),
        Inches(0.28),
        "Campanha com gasto em W-1. O número do quadro é o total, mesmo se a tabela mostrar só as 8 de maior gasto.",
        size=11,
        color=MUTED,
    )

    shown = campaigns[:8]
    extra = total - len(shown)
    rows = [[name, spend] for name, spend in shown] or [["—", "—"]]
    if extra > 0:
        rows.append([f"+{extra} campanha(s) fora desta lista", "—"])

    add_table(
        slide,
        ["Campanha", "Gasto W-1"],
        rows,
        left=MARGIN,
        top=Inches(3.75),
        width=Inches(12.4),
        height=Inches(2.95),
        header_fill=HEADER["competitiveness"],
    )

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


def data_block(prs, ads, kind: str, *, campaign: str, extra: str = "", winner=None):
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
    locked = ads[:TOP_ADS]
    winner = winner or {}
    winner_name = dash(winner.get("name"))
    winner_why = dash(winner.get("why"))
    slide = blank_slide(prs)
    add_act(slide, spec["act"], f"{spec['title']} · {campaign}")
    add_text(
        slide,
        MARGIN,
        Inches(0.86),
        Inches(12.4),
        Inches(0.28),
        f"{spec['subtitle']} Top {TOP_ADS} com gasto > R$ {MIN_SPEND_BRL}. Mesma ordem nas três etapas.{extra}",
        size=11,
        color=MUTED,
    )
    if winner_name != "—":
        callout = f"Campeão desta etapa: {winner_name}"
        if winner_why != "—":
            callout = f"{callout}  ·  {winner_why}"
    else:
        callout = "Campeão desta etapa: — (sem amostra para coroar)"
    add_text(slide, MARGIN, Inches(1.12), Inches(12.4), Inches(0.3), callout, size=14, bold=True)

    rows = []
    highlight = []
    for i, ad in enumerate(locked):
        block = ad.get(kind) or {}
        name = dash(ad.get("name"))
        is_winner = winner_name != "—" and name == winner_name
        if is_winner:
            name = f"★ {name}"
            highlight.append(i + 1)
        row = [name]
        for key in spec["keys"]:
            row.append(dash(block.get(key)))
        rows.append(row)
    if not rows:
        rows = [["—"] + ["—"] * (len(spec["headers"]) - 1)]

    add_table(
        slide,
        spec["headers"],
        rows,
        left=MARGIN,
        top=Inches(1.46),
        width=Inches(12.4),
        height=Inches(5.4),
        header_fill=spec["fill"],
        highlight_rows=highlight,
    )


def campaign_champions(camp):
    items = []
    if camp.get("champion"):
        items.append(camp["champion"])
    items.extend(camp.get("champions") or [])
    return items


def campaign_sections(prs, data):
    campaigns = data.get("campaigns") or []
    if not campaigns and data.get("ads"):
        campaigns = [{"name": "Conta", "ads": data.get("ads") or [], "champions": data.get("champions") or []}]

    shown = 0
    for camp in campaigns:
        name = dash(camp.get("name"))
        ads = camp.get("ads") or []
        below = camp.get("below_floor")
        extra = ""
        if below:
            extra = f" {below} ads com R$ {MIN_SPEND_BRL} ou menos, fora desta análise."
        winners = camp.get("stage_winners") or {}
        for kind in ("competitiveness", "attractiveness", "conversion"):
            data_block(prs, ads, kind, campaign=name, extra=extra, winner=winners.get(kind))
        for champ in campaign_champions(camp):
            if shown >= 3:
                break
            champion(prs, champ, campaign=name)
            shown += 1

    if shown == 0:
        for item in (data.get("champions") or [])[:3]:
            champion(prs, item, campaign="Conta")


def resolve_file(value) -> Path | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if path.exists():
        return path
    skill_root = Path(__file__).resolve().parent.parent
    for base in (Path.cwd(), skill_root, skill_root / "scripts"):
        candidate = (base / raw).resolve()
        if candidate.exists():
            return candidate
    return None


def png_size(path: Path):
    data = path.read_bytes()[:24]
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    return None


def place_creative(slide, creative: dict):
    box_l, box_t = MARGIN, Inches(0.95)
    box_w, box_h = Inches(2.85), Inches(5.05)
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, box_l, box_t, box_w, box_h)
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(0xF3, 0xF3, 0xF3)
    frame.line.color.rgb = RULE

    kind = dash(creative.get("kind")).lower()
    media = resolve_file(creative.get("file") or creative.get("poster") or creative.get("image"))
    video = resolve_file(creative.get("video"))
    duration = dash(creative.get("duration"))

    if media:
        pad = Inches(0.08)
        inner_w = box_w - pad * 2
        inner_h = box_h - Inches(0.42)
        size = png_size(media)
        pic_w, pic_h = inner_w, inner_h
        if size:
            iw, ih = size
            scale = min(inner_w / iw, inner_h / ih)
            pic_w, pic_h = int(iw * scale), int(ih * scale)
        left = box_l + pad + (inner_w - pic_w) // 2
        top = box_t + pad
        picture = slide.shapes.add_picture(str(media), left, top, pic_w, pic_h)
        if video:
            try:
                picture.click_action.hyperlink.address = video.resolve().as_uri()
            except Exception:
                pass
    else:
        add_text(
            slide,
            box_l + Inches(0.12),
            box_t + Inches(2.1),
            box_w - Inches(0.24),
            Inches(1.2),
            "Peça não baixada",
            size=12,
            color=MUTED,
            align=PP_ALIGN.CENTER,
        )

    if kind.startswith("video"):
        label = f"▶  Vídeo {duration}" if duration != "—" else "▶  Vídeo"
    elif kind.startswith("carousel"):
        label = "Carrossel · card 1"
    elif kind.startswith("image") or kind.startswith("est"):
        label = "Imagem"
    else:
        label = "Peça"
    add_text(
        slide,
        box_l + Inches(0.1),
        box_t + box_h - Inches(0.38),
        box_w - Inches(0.2),
        Inches(0.32),
        label,
        size=11,
        color=MUTED,
        align=PP_ALIGN.CENTER,
    )


def champion(prs, item, *, campaign: str):
    slide = blank_slide(prs)
    add_act(slide, "3 · Criativos", f"Campeão · {campaign}")
    creative = item.get("creative") or {}
    place_creative(slide, creative)

    left = Inches(3.5)
    width = Inches(9.35)
    add_text(slide, left, Inches(0.95), width, Inches(0.4), item.get("name", ""), size=22, bold=True)
    add_text(slide, left, Inches(1.32), width, Inches(0.28), dash(item.get("meta")), size=12, color=MUTED)

    stats = (item.get("stats") or [])[:4]
    for i, stat in enumerate(stats):
        x = left + Inches(i * 2.35)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.65), Inches(2.25), Inches(0.85))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0xF3, 0xF3, 0xF3)
        shape.line.color.rgb = RULE
        add_text(slide, x + Inches(0.1), Inches(1.7), Inches(2.05), Inches(0.4), dash(stat.get("value")), size=16, bold=True)
        add_text(slide, x + Inches(0.1), Inches(2.1), Inches(2.05), Inches(0.3), dash(stat.get("label")), size=10, color=MUTED)

    script = item.get("script") or {}
    angle = dash(item.get("angle"))
    script_lines = [
        f"Gancho: {dash(script.get('hook'))}",
        f"Miolo: {dash(script.get('body'))}",
        f"CTA / tela: {dash(script.get('cta') or script.get('on_screen'))}",
        f"Ângulo: {angle}",
    ]
    add_text(slide, left, Inches(2.6), width, Inches(0.28), "Roteiro e ângulo", size=13, bold=True)
    add_text(slide, left, Inches(2.88), width, Inches(0.95), "\n".join(script_lines), size=12)

    retention = item.get("retention") or {}
    add_text(slide, left, Inches(3.85), width, Inches(0.28), "Retenção — até onde ficou", size=13, bold=True)
    add_table(
        slide,
        ["3s", "25%", "50%", "75%", "Fim", "Tempo médio"],
        [[
            dash(retention.get("hook")),
            dash(retention.get("p25")),
            dash(retention.get("p50")),
            dash(retention.get("p75")),
            dash(retention.get("p100") or retention.get("thruplay")),
            dash(retention.get("avg_time")),
        ]],
        left=left,
        top=Inches(4.15),
        width=width,
        height=Inches(0.7),
        header_fill=HEADER["attractiveness"],
    )
    add_text(slide, left, Inches(4.88), width, Inches(0.35), dash(retention.get("drop")), size=12, color=MUTED)

    add_text(slide, left, Inches(5.22), width, Inches(0.26), "O que funcionou", size=13, bold=True)
    worked = item.get("worked") or []
    add_text(
        slide,
        left,
        Inches(5.46),
        width,
        Inches(0.7),
        "\n".join(f"· {line}" for line in worked) or "—",
        size=12,
    )

    hypo = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(6.2), width, Inches(0.9))
    hypo.fill.solid()
    hypo.fill.fore_color.rgb = RGBColor(0xEE, 0xF3, 0xF0)
    hypo.line.color.rgb = RGBColor(0x2F, 0x3A, 0x32)
    add_text(slide, left + Inches(0.15), Inches(6.25), width - Inches(0.3), Inches(0.22), "Hipótese", size=11, bold=True, color=RGBColor(0x2F, 0x3A, 0x32))
    add_text(slide, left + Inches(0.15), Inches(6.48), width - Inches(0.3), Inches(0.55), dash(item.get("hypothesis")), size=12)


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
        [
            dash(r.get("campaign") or r.get("name")),
            dash(r.get("name")),
            dash(r.get("copy")),
            dash(r.get("change")),
            dash(r.get("qty")),
            dash(r.get("criteria")),
        ]
        for r in reqs
    ] or [["—", "—", "—", "—", "—", "—"]]
    add_table(
        slide,
        ["Campanha", "Pedido", "Copia", "Muda", "Qtde", "Como sabemos que funcionou"],
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
    campaign_sections(prs, data)
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
