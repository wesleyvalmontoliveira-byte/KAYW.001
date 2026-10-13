# -*- coding: utf-8 -*-
"""
Gera 30 capas + contracapas (A5 com sangria de 3 mm = 154 x 216 mm), em PDF vetorial,
versão A4 com marcas de corte e PNG 300 dpi (para Canva/Photoshop).
Uso: python build_capas.py
"""
import os, math, random
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from common import register_fonts, C, sprig, flower, leaf, OUT_DIR, DELICADA, NEUTRA

BLEED = 3 * mm
W, H = 148 * mm + 2 * BLEED, 210 * mm + 2 * BLEED
TRIM = (BLEED, BLEED, W - BLEED, H - BLEED)
CX = W / 2

# ------------------------------------------------------------------ util

def bg(c, color):
    c.setFillColor(C(color))
    c.rect(0, 0, W, H, stroke=0, fill=1)


def plate(c, x, y, w, h, color="#FFFFFF", alpha=0.88, r=4 * mm, stroke=None):
    c.saveState()
    c.setFillColor(C(color))
    c.setFillAlpha(alpha)
    if stroke:
        c.setStrokeColor(C(stroke)); c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke else 0, fill=1)
    c.restoreState()


def tracking_text(c, x, y, s, font, size, color, tracking, align="center"):
    total = sum(pdfmetrics.stringWidth(ch, font, size) for ch in s) + tracking * (len(s) - 1)
    if align == "center":
        x -= total / 2
    elif align == "right":
        x -= total
    c.setFont(font, size); c.setFillColor(C(color))
    for ch in s:
        c.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, font, size) + tracking


def title_serif(c, y, ink, accent=None, script="Planner", tagline="planeje · realize · celebre", year="2027",
                size_year=66, size_script=40, x=None, align="center"):
    x = CX if x is None else x
    accent = accent or ink
    c.setFont("GreatVibes-Regular", size_script); c.setFillColor(C(accent))
    if align == "center":
        c.drawCentredString(x, y + 20 * mm, script)
    else:
        c.drawString(x, y + 20 * mm, script)
    c.setFont("PlayfairDisplay-Bold", size_year); c.setFillColor(C(ink))
    if align == "center":
        c.drawCentredString(x, y, year)
        c.setStrokeColor(C(accent)); c.setLineWidth(0.7)
        c.line(x - 18 * mm, y - 5 * mm, x + 18 * mm, y - 5 * mm)
        tracking_text(c, x, y - 11 * mm, tagline, "Nunito-Regular", 7.2, ink, 1.6)
    else:
        c.drawString(x, y, year)
        c.setStrokeColor(C(accent)); c.setLineWidth(0.7)
        c.line(x, y - 5 * mm, x + 36 * mm, y - 5 * mm)
        tracking_text(c, x, y - 11 * mm, tagline, "Nunito-Regular", 7.2, ink, 1.6, align="left")


def title_sans(c, y, ink, accent=None, tagline="PLANEJAMENTO ANUAL · MENSAL · SEMANAL", year="2027",
               size_year=78, x=None, align="center", outline=False, label="PLANNER"):
    x = CX if x is None else x
    accent = accent or ink
    c.setFillColor(C(ink))
    if outline:
        to = c.beginText()
        to.setTextRenderMode(1)
        c.setStrokeColor(C(ink)); c.setLineWidth(0.9)
        to.setFont("Montserrat-ExtraBold", size_year)
        wdt = pdfmetrics.stringWidth(year, "Montserrat-ExtraBold", size_year)
        to.setTextOrigin(x - wdt / 2 if align == "center" else x, y)
        to.textOut(year)
        c.drawText(to)
    else:
        c.setFont("Montserrat-ExtraBold", size_year)
        if align == "center":
            c.drawCentredString(x, y, year)
        else:
            c.drawString(x, y, year)
    c.setFillColor(C(accent))
    if align == "center":
        c.rect(x - 7 * mm, y - 6 * mm, 14 * mm, 1.1 * mm, stroke=0, fill=1)
        tracking_text(c, x, y - 14 * mm, label, "Montserrat-Bold", 14, ink, 6)
        tracking_text(c, x, y - 20.5 * mm, tagline, "Inter-Regular", 5.8, ink, 1.4)
    else:
        c.rect(x, y - 6 * mm, 14 * mm, 1.1 * mm, stroke=0, fill=1)
        tracking_text(c, x, y - 14 * mm, label, "Montserrat-Bold", 14, ink, 6, align="left")
        tracking_text(c, x, y - 20.5 * mm, tagline, "Inter-Regular", 5.8, ink, 1.4, align="left")


def heart(c, x, y, s, color, alpha=1.0, angle=0):
    c.saveState(); c.translate(x, y); c.rotate(angle); c.setFillColor(C(color)); c.setFillAlpha(alpha)
    p = c.beginPath()
    p.moveTo(0, -s)
    p.curveTo(-s * 1.6, s * 0.2, -s * 0.9, s * 1.3, 0, s * 0.45)
    p.curveTo(s * 0.9, s * 1.3, s * 1.6, s * 0.2, 0, -s)
    c.drawPath(p, stroke=0, fill=1); c.restoreState()


def star4(c, x, y, s, color, alpha=1.0):
    c.saveState(); c.translate(x, y); c.setFillColor(C(color)); c.setFillAlpha(alpha)
    p = c.beginPath()
    p.moveTo(0, s)
    for i in range(1, 8):
        a = i * math.pi / 4
        r = s if i % 2 == 0 else s * 0.3
        p.lineTo(r * math.sin(a), r * math.cos(a))
    p.close(); c.drawPath(p, stroke=0, fill=1); c.restoreState()


def poly(c, pts, color, alpha=1.0):
    c.saveState(); c.setFillColor(C(color)); c.setFillAlpha(alpha)
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close(); c.drawPath(p, stroke=0, fill=1); c.restoreState()


def gradient(c, top, bottom, steps=120):
    t, b = C(top), C(bottom)
    for i in range(steps):
        f = i / (steps - 1)
        col = (t.red + (b.red - t.red) * f, t.green + (b.green - t.green) * f, t.blue + (b.blue - t.blue) * f)
        c.setFillColorRGB(*col)
        y = H - (i + 1) * H / steps
        c.rect(0, y - 0.5, W, H / steps + 1, stroke=0, fill=1)


# ------------------------------------------------------------------ fundos (padrões)
def fundo_jardim(c, rnd):
    bg(c, "#F7F3EC")
    for i in range(26):
        x, y = rnd.uniform(-5 * mm, W + 5 * mm), rnd.uniform(-5 * mm, H + 5 * mm)
        sprig(c, x, y, rnd.uniform(16, 30) * mm, rnd.uniform(0, 360), rnd.choice(["#9FB09A", "#B8C6B2", "#8FA38A"]),
              flip=rnd.random() < 0.5, leaves=rnd.randint(5, 8), stem_w=0.55)
    for i in range(10):
        flower(c, rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(2.2, 3.6) * mm, "#E7B9BB", "#D9B88A", alpha=0.95)


def fundo_poa(c, rnd, base="#F4DEDE", dot="#FFFFFF", step=9 * mm, r=1.5 * mm):
    bg(c, base)
    c.setFillColor(C(dot))
    y = 0; row = 0
    while y < H + step:
        x = (step / 2 if row % 2 else 0)
        while x < W + step:
            c.circle(x, y, r, stroke=0, fill=1); x += step
        y += step * 0.87; row += 1


def fundo_cerejeira(c, rnd):
    bg(c, "#FBF1F2")
    for i in range(14):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        sprig(c, x, y, rnd.uniform(18, 28) * mm, rnd.uniform(0, 360), "#B8C6B2", flip=rnd.random() < 0.5, leaves=5, stem_w=0.5)
    for i in range(40):
        flower(c, rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.6, 4.2) * mm,
               rnd.choice(["#F2C4C8", "#E8A9B0", "#F7D7DA"]), "#D9B88A", alpha=0.95)


def fundo_lavanda(c, rnd):
    bg(c, "#ECE7F3")
    for i in range(22):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        sprig(c, x, y, rnd.uniform(14, 26) * mm, rnd.uniform(0, 360), rnd.choice(["#B9A6C9", "#A897BB"]),
              flip=rnd.random() < 0.5, leaves=6, stem_w=0.5)
    c.setFillColor(C("#D8D0E6"))
    for i in range(120):
        c.circle(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.4, 1.3) * mm, stroke=0, fill=1)


def fundo_listras(c, rnd, base="#FFFFFF", line="#F0E4E1", step=6 * mm, w=2.4 * mm, vertical=True):
    bg(c, base); c.setFillColor(C(line))
    p = 0
    while p < (W if vertical else H):
        if vertical:
            c.rect(p, 0, w, H, stroke=0, fill=1)
        else:
            c.rect(0, p, W, w, stroke=0, fill=1)
        p += step


def fundo_vichy(c, rnd, base="#FFFFFF", tone="#E8CBCC", step=8 * mm):
    bg(c, base)
    c.saveState(); c.setFillColor(C(tone)); c.setFillAlpha(0.55)
    x = 0
    while x < W:
        c.rect(x, 0, step / 2, H, stroke=0, fill=1); x += step
    y = 0
    while y < H:
        c.rect(0, y, W, step / 2, stroke=0, fill=1); y += step
    c.restoreState()


def fundo_arcos(c, rnd):
    bg(c, "#F2E6D8")
    cols = ["#C97B63", "#D9A48A", "#E9C7B2", "#F2E6D8", "#B9C7B4"]
    r = 150 * mm
    for i, col in enumerate(cols):
        c.setFillColor(C(col))
        rr = r - i * 24 * mm
        c.circle(CX, -40 * mm, rr, stroke=0, fill=1)


def fundo_ondas(c, rnd):
    bg(c, "#FBF4F2")
    cols = ["#F4DEDE", "#E8CBCC", "#D6E0D2", "#F2E6D8"]
    base_y = 95 * mm
    for i, col in enumerate(cols):
        c.setFillColor(C(col))
        yb = base_y - i * 22 * mm
        p = c.beginPath(); p.moveTo(-5, -5); p.lineTo(-5, yb)
        x = -5
        while x < W + 10:
            p.curveTo(x + 15 * mm, yb + 10 * mm, x + 25 * mm, yb - 10 * mm, x + 40 * mm, yb)
            x += 40 * mm
        p.lineTo(W + 5, -5); p.close(); c.drawPath(p, stroke=0, fill=1)


def fundo_terrazzo(c, rnd, base="#FBF7F2", cols=("#E8CBCC", "#C98B8F", "#9FB09A", "#D9B88A", "#D8D0E6", "#A8C3D1")):
    bg(c, base)
    for i in range(260):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        s = rnd.uniform(1.2, 4.5) * mm
        n = rnd.randint(3, 6)
        pts = []
        for k in range(n):
            a = 2 * math.pi * k / n + rnd.uniform(-0.3, 0.3)
            rr = s * rnd.uniform(0.6, 1.0)
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        poly(c, pts, rnd.choice(cols), alpha=0.9)


def fundo_por_do_sol(c, rnd):
    gradient(c, "#F7CDB9", "#E08F7B")
    c.setFillColor(C("#FBEAD8")); c.circle(CX, 168 * mm, 28 * mm, stroke=0, fill=1)
    c.setFillColor(C("#E9A08F"))
    for i in range(5):
        c.rect(0, 30 * mm + i * 6 * mm, W, 1.2 * mm, stroke=0, fill=1)


def fundo_estrelas(c, rnd):
    bg(c, "#2F2F4A")
    for i in range(220):
        c.setFillColor(C("#FFFFFF")); c.setFillAlpha(rnd.uniform(0.3, 0.95))
        c.circle(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.2, 0.9) * mm, stroke=0, fill=1)
    c.setFillAlpha(1)
    for i in range(26):
        star4(c, rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.6, 4) * mm, rnd.choice(["#F2D6A2", "#FFFFFF"]), 0.95)
    c.setStrokeColor(C("#5A5A80")); c.setLineWidth(0.3)
    for i in range(10):
        c.line(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0, W), rnd.uniform(0, H))


def fundo_coracoes(c, rnd):
    bg(c, "#FFFFFF")
    for i in range(90):
        heart(c, rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.4, 4) * mm,
              rnd.choice(["#F4DEDE", "#E8CBCC", "#C98B8F"]), alpha=0.9, angle=rnd.uniform(-25, 25))


def fundo_confete(c, rnd):
    bg(c, "#FDF9F4")
    cols = ["#F4DEDE", "#C98B8F", "#9FB09A", "#D9B88A", "#B9A6C9", "#A8C3D1", "#F7C8B8"]
    for i in range(170):
        c.saveState(); c.translate(rnd.uniform(0, W), rnd.uniform(0, H)); c.rotate(rnd.uniform(0, 180))
        c.setFillColor(C(rnd.choice(cols))); c.setFillAlpha(0.92)
        c.roundRect(-2 * mm, -0.8 * mm, 4 * mm, 1.6 * mm, 0.6 * mm, stroke=0, fill=1); c.restoreState()


def fundo_lineart(c, rnd):
    bg(c, "#FFFFFF")
    c.setStrokeColor(C("#9FB09A")); c.setLineWidth(0.6)
    for (x, y, L, a, fl) in [(-4 * mm, 10 * mm, 90 * mm, 52, False), (W + 4 * mm, H - 12 * mm, 90 * mm, 232, False),
                             (-2 * mm, H - 40 * mm, 60 * mm, -20, True), (W, 46 * mm, 60 * mm, 160, True)]:
        c.saveState(); c.translate(x, y); c.rotate(a)
        p = c.beginPath(); p.moveTo(0, 0); bend = L * 0.2 * (-1 if fl else 1)
        p.curveTo(L * 0.35, bend * 0.6, L * 0.7, bend, L, bend * 0.4); c.drawPath(p, stroke=1, fill=0)
        for i in range(9):
            tt = 0.1 + i * 0.1
            u = 1 - tt
            px = 3 * u * u * tt * L * 0.35 + 3 * u * tt * tt * L * 0.7 + tt ** 3 * L
            py = 3 * u * u * tt * bend * 0.6 + 3 * u * tt * tt * bend + tt ** 3 * bend * 0.4
            size = L * (0.2 - 0.012 * i); side = 1 if i % 2 == 0 else -1
            c.saveState(); c.translate(px, py); c.rotate(40 * side)
            q = c.beginPath(); q.moveTo(0, 0); q.curveTo(size * .3, size * .3, size * .75, size * .3, size, 0)
            q.curveTo(size * .75, -size * .3, size * .3, -size * .3, 0, 0); c.drawPath(q, stroke=1, fill=0)
            c.line(0, 0, size * 0.9, 0); c.restoreState()
        c.restoreState()


def fundo_marmore(c, rnd):
    bg(c, "#FBF6F4")
    for i in range(70):
        c.saveState(); c.setFillColor(C(rnd.choice(["#F4DEDE", "#E8CBCC", "#D9B88A", "#C9C3BE"]))); c.setFillAlpha(rnd.uniform(0.05, 0.14))
        c.translate(rnd.uniform(0, W), rnd.uniform(0, H)); c.rotate(rnd.uniform(-30, 30))
        rx, ry = rnd.uniform(30, 90) * mm, rnd.uniform(6, 22) * mm
        c.ellipse(-rx, -ry, rx, ry, stroke=0, fill=1); c.restoreState()
    c.setLineWidth(0.3)
    for i in range(10):
        c.setStrokeColor(C(rnd.choice(["#D9B88A", "#C9B7A8", "#E0C8C9"])))
        p = c.beginPath(); x, y = rnd.uniform(0, W), rnd.uniform(0, H); p.moveTo(x, y)
        for k in range(3):
            x2, y2 = x + rnd.uniform(-50, 50) * mm, y + rnd.uniform(-50, 50) * mm
            p.curveTo(x + rnd.uniform(-20, 20) * mm, y + rnd.uniform(-20, 20) * mm,
                      x2 + rnd.uniform(-20, 20) * mm, y2 + rnd.uniform(-20, 20) * mm, x2, y2)
            x, y = x2, y2
        c.drawPath(p, stroke=1, fill=0)


def fundo_solido(c, rnd, color):
    bg(c, color)


def fundo_grid(c, rnd, base="#FAFAF8", line="#E4E4E0", step=8 * mm):
    bg(c, base); c.setStrokeColor(C(line)); c.setLineWidth(0.35)
    x = BLEED
    while x < W:
        c.line(x, 0, x, H); x += step
    y = BLEED
    while y < H:
        c.line(0, y, W, y); y += step


def fundo_linho(c, rnd):
    bg(c, "#E8DFD2"); c.setStrokeColor(C("#DED3C4")); c.setLineWidth(0.3)
    y = 0
    while y < H:
        c.line(0, y, W, y); y += 1.2 * mm
    c.setStrokeColor(C("#E2D8CA"))
    x = 0
    while x < W:
        c.line(x, 0, x, H); x += 1.2 * mm


def fundo_blocos(c, rnd):
    bg(c, "#ECECE7"); c.setFillColor(C("#2E2E2E")); c.rect(0, 0, W, H * 0.42, stroke=0, fill=1)


def fundo_listras_bold(c, rnd):
    bg(c, "#FFFFFF"); c.setFillColor(C("#2E2E2E"))
    y = 0
    while y < H * 0.36:
        c.rect(0, y, W, 5 * mm, stroke=0, fill=1); y += 10 * mm


def fundo_memphis(c, rnd):
    bg(c, "#F5F5F2")
    c.setFillColor(C("#A3A89A")); c.circle(30 * mm, H - 30 * mm, 14 * mm, stroke=0, fill=1)
    c.setFillColor(C("#C8B9A6")); c.rect(16 * mm, 56 * mm, 20 * mm, 20 * mm, stroke=0, fill=1)
    c.setStrokeColor(C("#2E2E2E")); c.setLineWidth(1.2)
    p = c.beginPath(); x0, y0 = 16 * mm, 26 * mm; p.moveTo(x0, y0)
    for i in range(8):
        p.lineTo(x0 + (i + 1) * 6 * mm, y0 + (6 * mm if i % 2 == 0 else 0))
    c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(C("#2E2E2E"))
    for i in range(5):
        for j in range(5):
            c.circle(W - 40 * mm + i * 5 * mm, H - 50 * mm + j * 5 * mm, 0.8 * mm, stroke=0, fill=1)
    c.setFillColor(C("#A3A89A"))
    p = c.beginPath(); p.moveTo(W - 18 * mm, H - 70 * mm); p.lineTo(W - 18 * mm, H - 96 * mm); p.lineTo(W - 44 * mm, H - 96 * mm); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(C("#C8B9A6")); c.setLineWidth(1.4); c.arc(W - 66 * mm, 14 * mm, W - 16 * mm, 64 * mm, 0, 180)


def fundo_kraft(c, rnd):
    bg(c, "#B9946B")
    c.setFillColor(C("#A8845C"))
    for i in range(400):
        c.circle(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.15, 0.5) * mm, stroke=0, fill=1)
    c.setFillColor(C("#C7A47C"))
    for i in range(300):
        c.circle(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.15, 0.4) * mm, stroke=0, fill=1)


def fundo_carvao_dots(c, rnd):
    bg(c, "#2E2E2E"); c.setFillColor(C("#4A4A4A"))
    x = BLEED
    while x < W:
        y = BLEED
        while y < H:
            c.circle(x, y, 0.45 * mm, stroke=0, fill=1); y += 5 * mm
        x += 5 * mm


def fundo_meiotom(c, rnd):
    bg(c, "#FFFFFF"); c.setFillColor(C("#2E2E2E"))
    step = 5 * mm
    rows = int(H / step)
    for j in range(rows):
        f = max(0, 1 - j / (rows * 0.75))
        r = 0.2 * mm + f * 2.1 * mm
        if r < 0.25 * mm:
            continue
        x = step / 2 + (step / 2 if j % 2 else 0)
        while x < W:
            c.circle(x, j * step + step / 2, r, stroke=0, fill=1); x += step


def fundo_diagonais(c, rnd):
    bg(c, "#FAFAF8"); c.setStrokeColor(C("#D9D9D4")); c.setLineWidth(0.4)
    d = -H
    while d < W:
        c.line(d, 0, d + H, H); d += 5 * mm


def fundo_arquitetonico(c, rnd):
    bg(c, "#F5F5F2"); c.setLineWidth(0.5)
    for i in range(18):
        c.setStrokeColor(C(rnd.choice(["#B7B7B0", "#8C8C86", "#C8B9A6"])))
        x, y = rnd.uniform(-10 * mm, W), rnd.uniform(-10 * mm, H)
        c.rect(x, y, rnd.uniform(20, 70) * mm, rnd.uniform(20, 70) * mm, stroke=1, fill=0)


# ------------------------------------------------------------------ catálogo de capas
# (nome, tema, fundo, kwargs, estilo do título, cor do texto, cor de destaque, posição y, placa?)
CAPAS = [
    ("Jardim Sage", "D", fundo_jardim, {}, "serif", "#4A4442", "#C98B8F", 0.50, True),
    ("Rosé Poá", "D", fundo_poa, {}, "serif", "#7A4F52", "#C98B8F", 0.52, False),
    ("Flor de Cerejeira", "D", fundo_cerejeira, {}, "serif", "#5B4A4C", "#C98B8F", 0.50, True),
    ("Lavanda", "D", fundo_lavanda, {}, "serif", "#4F4660", "#8F7BA8", 0.52, True),
    ("Listras Cream", "D", fundo_listras, {}, "serif", "#4A4442", "#C98B8F", 0.52, True),
    ("Vichy Rosé", "D", fundo_vichy, {}, "serif", "#7A4F52", "#C98B8F", 0.52, True),
    ("Arcos Boho", "D", fundo_arcos, {}, "serif", "#5B3F35", "#C97B63", 0.70, False),
    ("Ondas Suaves", "D", fundo_ondas, {}, "serif", "#4A4442", "#C98B8F", 0.70, False),
    ("Terrazzo Pastel", "D", fundo_terrazzo, {}, "serif", "#4A4442", "#C98B8F", 0.52, True),
    ("Pôr do Sol", "D", fundo_por_do_sol, {}, "serif", "#FFFFFF", "#FBEAD8", 0.40, False),
    ("Céu Estrelado", "D", fundo_estrelas, {}, "serif", "#F7F3EC", "#F2D6A2", 0.52, False),
    ("Corações", "D", fundo_coracoes, {}, "serif", "#7A4F52", "#C98B8F", 0.52, True),
    ("Confete", "D", fundo_confete, {}, "serif", "#4A4442", "#C98B8F", 0.52, True),
    ("Folhagem Line Art", "D", fundo_lineart, {}, "serif", "#4A4442", "#9FB09A", 0.52, False),
    ("Mármore Rosé", "D", fundo_marmore, {}, "serif", "#4A4442", "#C98B8F", 0.52, False),
    ("Preto Essencial", "N", fundo_solido, {"color": "#1E1E1E"}, "sans", "#F5F5F2", "#C8B9A6", 0.52, False),
    ("Branco Tipográfico", "N", fundo_solido, {"color": "#FFFFFF"}, "sans-outline", "#1E1E1E", "#1E1E1E", 0.52, False),
    ("Grid Técnico", "N", fundo_grid, {}, "sans", "#1E1E1E", "#1E1E1E", 0.52, True),
    ("Linho Bege", "N", fundo_linho, {}, "sans", "#3B3630", "#8C7B66", 0.52, False),
    ("Blocos", "N", fundo_blocos, {}, "sans-split", "#1E1E1E", "#F5F5F2", 0.60, False),
    ("Listras Bold", "N", fundo_listras_bold, {}, "sans-left", "#1E1E1E", "#1E1E1E", 0.78, False),
    ("Oliva", "N", fundo_solido, {"color": "#6E7B73"}, "sans", "#F2EEE6", "#D9CBB8", 0.52, False),
    ("Terracota", "N", fundo_solido, {"color": "#B8694F"}, "sans-circle", "#3B2A24", "#F2E6D8", 0.52, False),
    ("Petróleo", "N", fundo_solido, {"color": "#243B47"}, "sans-lines", "#F5F5F2", "#C8B9A6", 0.52, False),
    ("Memphis Suave", "N", fundo_memphis, {}, "sans", "#1E1E1E", "#1E1E1E", 0.52, False),
    ("Kraft", "N", fundo_kraft, {}, "sans-stamp", "#3B2E22", "#3B2E22", 0.52, False),
    ("Carvão Dots", "N", fundo_carvao_dots, {}, "sans", "#F5F5F2", "#A3A89A", 0.52, False),
    ("Meio-tom", "N", fundo_meiotom, {}, "sans", "#1E1E1E", "#1E1E1E", 0.68, True),
    ("Diagonais", "N", fundo_diagonais, {}, "sans", "#1E1E1E", "#1E1E1E", 0.52, True),
    ("Arquitetônico", "N", fundo_arquitetonico, {}, "sans", "#1E1E1E", "#1E1E1E", 0.52, True),
]


def draw_front(c, cap, idx):
    name, tema, fn, kw, style, ink, acc, ypos, use_plate = cap
    rnd = random.Random(1000 + idx)
    fn(c, rnd, **kw)
    y = H * ypos
    if use_plate:
        if style == "serif":
            plate(c, CX - 44 * mm, y - 17 * mm, 88 * mm, 52 * mm, alpha=0.86)
        else:
            plate(c, CX - 44 * mm, y - 26 * mm, 88 * mm, 50 * mm, alpha=0.9, r=0)
    if style == "serif":
        title_serif(c, y, ink, acc)
    elif style == "sans":
        title_sans(c, y, ink, acc)
    elif style == "sans-outline":
        title_sans(c, y, ink, acc, outline=True, size_year=96)
    elif style == "sans-split":
        c.setFont("Montserrat-ExtraBold", 84); c.setFillColor(C("#1E1E1E")); c.drawCentredString(CX, H * 0.50, "2027")
        tracking_text(c, CX, H * 0.30, "PLANNER", "Montserrat-Bold", 16, "#F5F5F2", 7)
        tracking_text(c, CX, H * 0.30 - 7 * mm, "ANUAL · MENSAL · SEMANAL", "Inter-Regular", 6, "#C8B9A6", 1.6)
    elif style == "sans-left":
        title_sans(c, y, ink, acc, x=14 * mm, align="left", size_year=70)
    elif style == "sans-circle":
        c.setFillColor(C(acc)); c.circle(CX, y + 4 * mm, 44 * mm, stroke=0, fill=1)
        title_sans(c, y, ink, ink, size_year=64)
    elif style == "sans-lines":
        c.setStrokeColor(C(acc)); c.setLineWidth(0.5)
        for i in range(14):
            c.line(0, 14 * mm + i * 4 * mm, W, 14 * mm + i * 4 * mm)
        title_sans(c, y, ink, acc)
    elif style == "sans-stamp":
        plate(c, CX - 46 * mm, y - 28 * mm, 92 * mm, 60 * mm, color="#F5F0E6", alpha=1, r=3 * mm, stroke="#3B2E22")
        c.saveState(); c.setStrokeColor(C("#3B2E22")); c.setLineWidth(0.6); c.setDash([2, 2])
        c.roundRect(CX - 43 * mm, y - 25 * mm, 86 * mm, 54 * mm, 2 * mm, stroke=1, fill=0); c.restoreState()
        title_sans(c, y, ink, acc, size_year=64)
    # créditos discretos na sangria inferior? não — mantém limpo.


def draw_back(c, cap, idx):
    name, tema, fn, kw, style, ink, acc, ypos, use_plate = cap
    rnd = random.Random(1000 + idx)
    fn(c, rnd, **kw)
    # elemento central discreto
    if style == "serif":
        light = ink in ("#FFFFFF", "#F7F3EC")
        if not light:
            plate(c, CX - 26 * mm, H / 2 - 9 * mm, 52 * mm, 18 * mm, alpha=0.85)
        c.setFont("GreatVibes-Regular", 18); c.setFillColor(C(ink if light else acc))
        c.drawCentredString(CX, H / 2 - 1 * mm, "Planner 2027")
        flower(c, CX, H / 2 + 11 * mm, 2.2 * mm, "#E7B9BB" if not light else ink, "#D9B88A")
    else:
        if use_plate:
            plate(c, CX - 22 * mm, H / 2 - 7 * mm, 44 * mm, 14 * mm, alpha=0.9, r=0)
        col = ink if style not in ("sans-split",) else "#F5F5F2"
        if style == "sans-split":
            col = "#1E1E1E"
        if style == "sans-stamp":
            plate(c, CX - 24 * mm, H / 2 - 8 * mm, 48 * mm, 16 * mm, color="#F5F0E6", alpha=1, r=2 * mm, stroke="#3B2E22")
        tracking_text(c, CX, H / 2 - 2 * mm, "PLANNER 2027", "Montserrat-Bold", 8, col, 3)


def trim_marks(c, pdf_w, pdf_h, ox, oy):
    """Marcas de corte ao redor da área aparada, para a versão A4."""
    c.setStrokeColor(C("#555555")); c.setLineWidth(0.3)
    L = 4 * mm; g = 1.5 * mm
    x0, y0, x1, y1 = ox + BLEED, oy + BLEED, ox + W - BLEED, oy + H - BLEED
    for (x, y, dx, dy) in [(x0, y0, -1, -1), (x1, y0, 1, -1), (x0, y1, -1, 1), (x1, y1, 1, 1)]:
        c.line(x + dx * g, y, x + dx * (g + L), y)
        c.line(x, y + dy * g, x, y + dy * (g + L))


def build():
    register_fonts()
    out_dir = os.path.join(OUT_DIR, "capas")
    png_dir = os.path.join(out_dir, "png-300dpi")
    os.makedirs(png_dir, exist_ok=True)
    # 1) PDF com sangria (todas as capas, frente e verso alternados)
    pdf_all = os.path.join(out_dir, "Capas-2027-30-modelos-A5-com-sangria.pdf")
    c = canvas.Canvas(pdf_all, pagesize=(W, H))
    c.setTitle("Capas Planner 2027 — 30 modelos (frente e verso) — A5 + 3 mm de sangria")
    for i, cap in enumerate(CAPAS, 1):
        draw_front(c, cap, i); c.showPage()
        draw_back(c, cap, i); c.showPage()
    c.save()
    # 2) PDF A4 com marcas de corte (1 capa por página, frente e verso)
    from reportlab.lib.pagesizes import A4
    pdf_a4 = os.path.join(out_dir, "Capas-2027-30-modelos-A4-com-marcas-de-corte.pdf")
    c = canvas.Canvas(pdf_a4, pagesize=A4)
    c.setTitle("Capas Planner 2027 — A4 com marcas de corte (imprimir em papel 250–300 g)")
    ox, oy = (A4[0] - W) / 2, (A4[1] - H) / 2
    for i, cap in enumerate(CAPAS, 1):
        for side, fn in (("frente", draw_front), ("verso", draw_back)):
            c.saveState(); c.translate(ox, oy)
            p = c.beginPath(); p.rect(0, 0, W, H); c.clipPath(p, stroke=0, fill=0)
            fn(c, cap, i); c.restoreState()
            trim_marks(c, A4[0], A4[1], ox, oy)
            c.setFont("Inter-Regular", 7); c.setFillColor(C("#777777"))
            c.drawString(ox, oy - 6 * mm, f"Capa {i:02d} · {cap[0]} · {side} · 148 x 210 mm + 3 mm de sangria · cortar nas marcas")
            c.showPage()
    c.save()
    # 3) PNG 300 dpi (frente e verso)
    doc = pymupdf.open(pdf_all)
    for i, cap in enumerate(CAPAS, 1):
        slug = cap[0].lower().replace(" ", "-").replace("ô", "o").replace("é", "e").replace("á", "a").replace("ç", "c").replace("ã", "a").replace("ó", "o").replace("í", "i")
        for k, side in ((0, "frente"), (1, "verso")):
            pix = doc[(i - 1) * 2 + k].get_pixmap(dpi=300, alpha=False)
            pix.save(os.path.join(png_dir, f"Capa-{i:02d}-{slug}-{side}.png"))
    print("ok", pdf_all); print("ok", pdf_a4); print("ok", png_dir)


if __name__ == "__main__":
    build()
