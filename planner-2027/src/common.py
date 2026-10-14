# -*- coding: utf-8 -*-
"""
Base compartilhada do gerador do Kit Planner 2027.
Temas, fontes, primitivas de desenho (reportlab) e utilitários de datas.
"""
import os, math, random, calendar, datetime as dt
from dataclasses import dataclass
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.units import mm

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "produto"))

A5_W, A5_H = 148 * mm, 210 * mm
A4_W, A4_H = 210 * mm, 297 * mm

# ----------------------------------------------------------------- fontes
_registered = False
ICON = {}


def register_fonts():
    global _registered
    if _registered:
        return
    for f in os.listdir(FONT_DIR):
        if f.lower().endswith(".ttf"):
            pdfmetrics.registerFont(TTFont(f[:-4], os.path.join(FONT_DIR, f)))
    with open(os.path.join(FONT_DIR, "MaterialIcons-Regular.codepoints")) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) == 2:
                ICON[parts[0]] = chr(int(parts[1], 16))
    _registered = True


def icon(name, fallback="circle"):
    return ICON.get(name) or ICON.get(fallback, "")


# ----------------------------------------------------------------- temas
@dataclass
class Theme:
    key: str
    name: str
    ink: str
    ink_soft: str
    line: str
    line_soft: str
    fill_soft: str
    fill_header: str
    accent: str
    accent2: str
    accent3: str
    tab_fill: str
    tab_ink: str
    f_title: str
    f_title_b: str
    f_title_i: str
    f_script: str
    f_body: str
    f_body_b: str
    f_body_sb: str
    f_body_l: str
    deco: str
    palette: tuple  # cores de apoio para capas/adesivos


DELICADA = Theme(
    key="delicada", name="Delicada",
    ink="#4A4442", ink_soft="#8F8583", line="#CDBDBA", line_soft="#EADFDC",
    fill_soft="#FBF4F2", fill_header="#F4DEDE", accent="#C98B8F", accent2="#9FB09A",
    accent3="#D9B88A", tab_fill="#E8CBCC", tab_ink="#7A4F52",
    f_title="PlayfairDisplay-Regular", f_title_b="PlayfairDisplay-Bold",
    f_title_i="PlayfairDisplay-Italic", f_script="GreatVibes-Regular",
    f_body="Nunito-Regular", f_body_b="Nunito-Bold", f_body_sb="Nunito-SemiBold",
    f_body_l="Nunito-Light", deco="botanical",
    palette=("#F4DEDE", "#E8CBCC", "#C98B8F", "#9FB09A", "#D6E0D2", "#D9B88A",
             "#F2E6D8", "#D8D0E6", "#B9A6C9", "#F7C8B8", "#E9A08F", "#A8C3D1"),
)

NEUTRA = Theme(
    key="neutra", name="Neutra",
    ink="#262626", ink_soft="#7D7D7A", line="#BDBDB8", line_soft="#E4E4E0",
    fill_soft="#F5F5F2", fill_header="#ECECE7", accent="#2E2E2E", accent2="#A3A89A",
    accent3="#C8B9A6", tab_fill="#DADAD4", tab_ink="#2E2E2E",
    f_title="Montserrat-Medium", f_title_b="Montserrat-Bold",
    f_title_i="Montserrat-SemiBold", f_script="Montserrat-ExtraBold",
    f_body="Inter-Regular", f_body_b="Inter-Bold", f_body_sb="Inter-SemiBold",
    f_body_l="Inter-Regular", deco="minimal",
    palette=("#ECECE7", "#DADAD4", "#2E2E2E", "#A3A89A", "#C8B9A6", "#8C8C86",
             "#F5F5F2", "#B7B7B0", "#50504C", "#D9CBB8", "#9AA3A8", "#6E7B73"),
)

THEMES = {"delicada": DELICADA, "neutra": NEUTRA}


def C(h):
    return HexColor(h)


# ----------------------------------------------------------------- datas
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
         "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
MESES_ABR = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
DIAS_ABR = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
DIAS_1 = ["S", "T", "Q", "Q", "S", "S", "D"]


def easter(year):
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def nth_weekday(year, month, weekday, n):
    """n-ésimo dia da semana (0=seg) do mês."""
    d = dt.date(year, month, 1)
    off = (weekday - d.weekday()) % 7
    return d + dt.timedelta(days=off + 7 * (n - 1))


def feriados(year):
    """Feriados nacionais (lei) + pontos facultativos usuais. Retorna {date: (nome, tipo)}."""
    e = easter(year)
    f = {
        dt.date(year, 1, 1): ("Confraternização Universal", "feriado"),
        e - dt.timedelta(days=48): ("Carnaval", "facultativo"),
        e - dt.timedelta(days=47): ("Carnaval", "facultativo"),
        e - dt.timedelta(days=46): ("Quarta-feira de Cinzas", "facultativo"),
        e - dt.timedelta(days=2): ("Sexta-feira Santa", "feriado"),
        e: ("Páscoa", "data"),
        dt.date(year, 4, 21): ("Tiradentes", "feriado"),
        dt.date(year, 5, 1): ("Dia do Trabalho", "feriado"),
        e + dt.timedelta(days=60): ("Corpus Christi", "facultativo"),
        dt.date(year, 9, 7): ("Independência do Brasil", "feriado"),
        dt.date(year, 10, 12): ("Nossa Senhora Aparecida", "feriado"),
        dt.date(year, 11, 2): ("Finados", "feriado"),
        dt.date(year, 11, 15): ("Proclamação da República", "feriado"),
        dt.date(year, 11, 20): ("Dia da Consciência Negra", "feriado"),
        dt.date(year, 12, 25): ("Natal", "feriado"),
    }
    return f


def datas_comemorativas(year):
    e = easter(year)
    d = {
        dt.date(year, 3, 8): "Dia Internacional da Mulher",
        dt.date(year, 3, 15): "Dia do Consumidor",
        e: "Páscoa",
        dt.date(year, 4, 18): "Dia Nacional do Livro Infantil",
        nth_weekday(year, 5, 6, 2): "Dia das Mães",
        dt.date(year, 6, 12): "Dia dos Namorados",
        dt.date(year, 6, 24): "São João",
        dt.date(year, 7, 20): "Dia do Amigo",
        nth_weekday(year, 8, 6, 2): "Dia dos Pais",
        dt.date(year, 9, 21): "Dia da Árvore / início da primavera (22)",
        dt.date(year, 10, 12): "Dia das Crianças",
        dt.date(year, 10, 15): "Dia do Professor",
        dt.date(year, 10, 31): "Halloween",
        nth_weekday(year, 11, 4, 4): "Black Friday",
        dt.date(year, 12, 24): "Véspera de Natal",
        dt.date(year, 12, 25): "Natal",
        dt.date(year, 12, 31): "Réveillon",
    }
    return d


def weeks_of_year(year):
    """Lista de (segunda, domingo) de todas as semanas que tocam o ano, seg-dom."""
    first = dt.date(year, 1, 1)
    start = first - dt.timedelta(days=first.weekday())
    last = dt.date(year, 12, 31)
    weeks = []
    while start <= last:
        weeks.append((start, start + dt.timedelta(days=6)))
        start += dt.timedelta(days=7)
    return weeks


def weeks_by_month(year):
    """Atribui cada semana a um mês: 1ª semana -> janeiro, última -> dezembro,
    demais pela regra da quinta-feira."""
    weeks = weeks_of_year(year)
    out = {m: [] for m in range(1, 13)}
    for i, (a, b) in enumerate(weeks):
        if i == 0:
            m = 1
        elif i == len(weeks) - 1:
            m = 12
        else:
            thu = a + dt.timedelta(days=3)
            m = thu.month if thu.year == year else (1 if thu.year < year else 12)
        out[m].append((i + 1, a, b))
    return out


def month_grid(year, month):
    """6 linhas x 7 colunas (seg..dom) com dates (inclui dias de meses vizinhos)."""
    first = dt.date(year, month, 1)
    start = first - dt.timedelta(days=first.weekday())
    rows = []
    d = start
    for r in range(6):
        row = []
        for c in range(7):
            row.append(d)
            d += dt.timedelta(days=1)
        rows.append(row)
    return rows


def fmt_range(a, b):
    if a.month == b.month:
        return f"{a.day:02d} a {b.day:02d} de {MESES[a.month-1].lower()}"
    return f"{a.day:02d} {MESES_ABR[a.month-1].lower()} a {b.day:02d} {MESES_ABR[b.month-1].lower()}"


# ----------------------------------------------------------------- primitivas
class Page:
    """Contexto de uma página A5 com margens espelhadas."""

    def __init__(self, c, theme, number, size=(A5_W, A5_H), m_out=9 * mm, m_in=14 * mm,
                 m_top=10 * mm, m_bot=10 * mm):
        self.c = c
        self.t = theme
        self.n = number
        self.W, self.H = size
        self.recto = (number % 2 == 1)  # página ímpar = direita
        # margem interna (lombada) fica à esquerda na recto, à direita na verso
        self.x0 = m_in if self.recto else m_out
        self.x1 = self.W - (m_out if self.recto else m_in)
        self.y0 = m_bot
        self.y1 = self.H - m_top
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0

    # --- texto
    def text(self, x, y, s, font=None, size=9, color=None, align="left", tracking=0):
        c = self.c
        c.setFont(font or self.t.f_body, size)
        c.setFillColor(C(color or self.t.ink))
        if tracking:
            # desenha letra a letra com espaçamento
            total = sum(pdfmetrics.stringWidth(ch, font or self.t.f_body, size) for ch in s) + tracking * (len(s) - 1)
            if align == "center":
                x = x - total / 2
            elif align == "right":
                x = x - total
            for ch in s:
                c.drawString(x, y, ch)
                x += pdfmetrics.stringWidth(ch, font or self.t.f_body, size) + tracking
            return total
        if align == "center":
            c.drawCentredString(x, y, s)
        elif align == "right":
            c.drawRightString(x, y, s)
        else:
            c.drawString(x, y, s)
        return pdfmetrics.stringWidth(s, font or self.t.f_body, size)

    def icon(self, x, y, name, size=9, color=None, align="left"):
        self.text(x, y, icon(name), font="MaterialIcons-Regular", size=size,
                  color=color or self.t.accent, align=align)

    def wrap(self, s, font, size, width):
        words, lines, cur = s.split(), [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(test, font, size) <= width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, width, font=None, size=9, leading=None, color=None, align="left"):
        font = font or self.t.f_body
        leading = leading or size * 1.35
        for ln in self.wrap(s, font, size, width):
            self.text(x if align != "center" else x + width / 2, y, ln, font, size, color, align)
            y -= leading
        return y

    def vtext(self, x, y, s, font=None, size=8, color=None, angle=90):
        c = self.c
        c.saveState()
        c.translate(x, y)
        c.rotate(angle)
        c.setFont(font or self.t.f_body, size)
        c.setFillColor(C(color or self.t.ink))
        c.drawString(0, 0, s)
        c.restoreState()

    # --- formas
    def line(self, x0, y0, x1, y1, color=None, width=0.5, dash=None):
        c = self.c
        c.setStrokeColor(C(color or self.t.line))
        c.setLineWidth(width)
        c.setDash(dash or [])
        c.line(x0, y0, x1, y1)
        c.setDash([])

    def rect(self, x, y, w, h, fill=None, stroke=None, width=0.5, r=0):
        c = self.c
        if fill:
            c.setFillColor(C(fill))
        if stroke:
            c.setStrokeColor(C(stroke))
            c.setLineWidth(width)
        if r:
            c.roundRect(x, y, w, h, r, stroke=1 if stroke else 0, fill=1 if fill else 0)
        else:
            c.rect(x, y, w, h, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def circle(self, x, y, r, fill=None, stroke=None, width=0.5):
        c = self.c
        if fill:
            c.setFillColor(C(fill))
        if stroke:
            c.setStrokeColor(C(stroke))
            c.setLineWidth(width)
        c.circle(x, y, r, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def checkbox(self, x, y, s=3.2 * mm, r=0.6 * mm):
        t = self.t
        if t.deco == "botanical":
            self.rect(x, y, s, s, stroke=t.line, width=0.6, r=r)
        else:
            self.rect(x, y, s, s, stroke=t.ink_soft, width=0.6)

    def ruled(self, x, y_top, w, n, gap=7 * mm, color=None, width=0.45, dotted=False):
        """n linhas horizontais a partir de y_top descendo."""
        y = y_top
        for i in range(n):
            self.line(x, y, x + w, y, color or self.t.line_soft, width, [0.6, 1.6] if dotted else None)
            y -= gap
        return y

    def dotgrid(self, x, y, w, h, step=5 * mm, color=None, r=0.35):
        c = self.c
        c.setFillColor(C(color or self.t.line))
        nx, ny = int(w // step), int(h // step)
        ox = x + (w - nx * step) / 2
        oy = y + (h - ny * step) / 2
        for i in range(nx + 1):
            for j in range(ny + 1):
                c.circle(ox + i * step, oy + j * step, r, stroke=0, fill=1)

    def box(self, x, y, w, h, title=None, fill=None, stroke=None, r=None, title_size=8.2,
            icon_name=None, title_h=None):
        """Caixa com título. Retorna (x_in, y_top_in, w_in, h_in)."""
        t = self.t
        r = (2.2 * mm if t.deco == "botanical" else 0) if r is None else r
        self.rect(x, y, w, h, fill=fill or "#FFFFFF", stroke=stroke or t.line, width=0.55, r=r)
        th = title_h or (6.2 * mm if title else 0)
        if title:
            if t.deco == "botanical":
                self.c.saveState()
                p = self.c.beginPath()
                p.roundRect(x, y + h - th, w, th, r)
                self.c.clipPath(p, stroke=0, fill=0)
                self.rect(x, y + h - th - r, w, th + r, fill=fill_title(t), stroke=None, r=0)
                self.c.restoreState()
                self.line(x, y + h - th, x + w, y + h - th, t.line, 0.55)
                tx = x + 2.5 * mm
                if icon_name:
                    self.icon(tx, y + h - th + 1.8 * mm, icon_name, size=8, color=t.accent)
                    tx += 4.6 * mm
                self.text(tx, y + h - th + 1.9 * mm, title, t.f_title_i, title_size, t.ink)
            else:
                self.rect(x, y + h - th, w, th, fill=t.fill_header, stroke=None)
                self.line(x, y + h - th, x + w, y + h - th, t.line, 0.55)
                tx = x + 2.5 * mm
                if icon_name:
                    self.icon(tx, y + h - th + 1.8 * mm, icon_name, size=8, color=t.ink)
                    tx += 4.6 * mm
                self.text(tx, y + h - th + 2.0 * mm, title.upper(), t.f_body_sb, title_size - 1, t.ink, tracking=0.6)
        pad = 2.5 * mm
        return x + pad, y + h - th - pad, w - 2 * pad, h - th - 2 * pad

    # --- cabeçalho / rodapé
    def header(self, title, subtitle=None, icon_name=None, small=False):
        t = self.t
        y = self.y1
        if t.deco == "botanical":
            self.text(self.x0, y - 7.5 * mm, title, t.f_title_i, 15 if not small else 12.5, t.ink)
            if subtitle:
                self.text(self.x0, y - 12.3 * mm, subtitle, t.f_body, 7.6, t.ink_soft)
            self.line(self.x0, y - 14.5 * mm, self.x1, y - 14.5 * mm, t.line, 0.6)
            # raminho na ponta direita da linha do cabeçalho
            sprig(self.c, self.x1 - 1 * mm, y - 9 * mm, 20 * mm, 180, t.accent2, flip=False)
        else:
            self.text(self.x0, y - 7.2 * mm, title.upper(), t.f_title_b, 11.5 if not small else 10, t.ink, tracking=1.4)
            if subtitle:
                self.text(self.x1, y - 7.2 * mm, subtitle, t.f_body, 7.4, t.ink_soft, align="right")
            self.rect(self.x0, y - 10.4 * mm, 10 * mm, 0.9 * mm, fill=t.accent)
            self.line(self.x0, y - 14.5 * mm, self.x1, y - 14.5 * mm, t.line, 0.6)
        return y - 18 * mm  # topo da área de conteúdo

    def footer(self, label=""):
        t = self.t
        y = 5.2 * mm
        self.text(self.x1 if self.recto else self.x0, y, str(self.n), t.f_body, 6.5, t.ink_soft,
                  align="right" if self.recto else "left")
        if label:
            self.text(self.x0 if self.recto else self.x1, y, label, t.f_body_l if t.deco == "botanical" else t.f_body,
                      6.5, t.ink_soft, align="left" if self.recto else "right")

    def month_tab(self, month_idx):
        """Aba lateral externa com os 12 meses, mês atual destacado."""
        t = self.t
        tab_h = 12.5 * mm
        tab_w = 4.2 * mm
        top = self.H - 22 * mm
        x = self.W - tab_w if self.recto else 0
        for i in range(12):
            y = top - i * (tab_h + 1.2 * mm) - tab_h
            cur = (i == month_idx)
            fill = t.accent if cur else t.tab_fill
            if t.deco == "botanical" and cur:
                fill = t.accent
            self.rect(x, y, tab_w, tab_h, fill=fill)
            col = "#FFFFFF" if cur else t.tab_ink
            self.vtext(x + tab_w / 2 + 1.0 * mm, y + 2.2 * mm, MESES_ABR[i], t.f_body_sb, 5.6, col, 90)


def fill_title(t):
    return t.fill_header


# ----------------------------------------------------------------- decoração
def leaf(c, x, y, L, w, angle, color, alpha=1.0):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setFillColor(C(color))
    c.setFillAlpha(alpha)
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(L * 0.3, w, L * 0.75, w, L, 0)
    p.curveTo(L * 0.75, -w, L * 0.3, -w, 0, 0)
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def sprig(c, x, y, length, angle, color, flip=False, leaves=7, stem_w=0.5):
    """Raminho botânico: haste curva com folhas alternadas."""
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setStrokeColor(C(color))
    c.setLineWidth(stem_w)
    p = c.beginPath()
    p.moveTo(0, 0)
    bend = length * 0.18 * (-1 if flip else 1)
    p.curveTo(length * 0.35, bend * 0.6, length * 0.7, bend, length, bend * 0.4)
    c.drawPath(p, stroke=1, fill=0)
    for i in range(leaves):
        tt = 0.12 + i * (0.8 / max(1, leaves - 1))
        # ponto na curva (bezier cúbica)
        x0, y0 = 0, 0
        x1, y1 = length * 0.35, bend * 0.6
        x2, y2 = length * 0.7, bend
        x3, y3 = length, bend * 0.4
        u = 1 - tt
        px = u**3 * x0 + 3 * u**2 * tt * x1 + 3 * u * tt**2 * x2 + tt**3 * x3
        py = u**3 * y0 + 3 * u**2 * tt * y1 + 3 * u * tt**2 * y2 + tt**3 * y3
        size = length * (0.22 - 0.012 * i)
        side = 1 if i % 2 == 0 else -1
        leaf(c, px, py, size, size * 0.28, 42 * side + (12 if flip else -12), color, 0.95)
    c.restoreState()


def flower(c, x, y, r, petal_color, center_color, petals=5, alpha=1.0):
    c.saveState()
    c.translate(x, y)
    for i in range(petals):
        c.saveState()
        c.rotate(i * 360 / petals)
        c.setFillColor(C(petal_color))
        c.setFillAlpha(alpha)
        c.ellipse(-r * 0.32, r * 0.25, r * 0.32, r * 1.05, stroke=0, fill=1)
        c.restoreState()
    c.setFillColor(C(center_color))
    c.circle(0, 0, r * 0.26, stroke=0, fill=1)
    c.restoreState()


def corner_botanical(c, x, y, size, t, flip_x=False, flip_y=False):
    """Composição de raminhos + flor para cantos de capa/abertura."""
    c.saveState()
    c.translate(x, y)
    c.scale(-1 if flip_x else 1, -1 if flip_y else 1)
    sprig(c, 0, 0, size, 58, t.accent2, leaves=8, stem_w=0.7)
    sprig(c, 0, 0, size * 0.8, 18, t.accent2, flip=True, leaves=6, stem_w=0.6)
    sprig(c, 0, 0, size * 0.65, 95, "#B8C6B2", leaves=5, stem_w=0.5)
    flower(c, size * 0.42, size * 0.33, size * 0.08, t.accent, t.accent3)
    flower(c, size * 0.16, size * 0.52, size * 0.055, "#E7B9BB", t.accent3)
    c.setFillColor(C(t.accent3))
    for (dx, dy) in [(0.55, 0.62), (0.7, 0.2), (0.3, 0.75)]:
        c.circle(size * dx, size * dy, size * 0.012, stroke=0, fill=1)
    c.restoreState()


def stars_row(pg, x, y, n=5, size=8, color=None):
    for i in range(n):
        pg.icon(x + i * (size * 1.15), y, "star_border", size=size, color=color or pg.t.ink_soft)


def mini_calendar(pg, x, y_top, w, year, month, hol=None, title_font=None, size=5.6, today_marks=None, title_size=7.2):
    """Mini calendário mensal (seg-dom). y_top = topo. Retorna altura usada."""
    t = pg.t
    hol = hol or {}
    cols = 7
    cw = w / cols
    rh = size * 1.75
    pg.text(x + w / 2, y_top - title_size, MESES[month - 1], title_font or (t.f_title_i if t.deco == "botanical" else t.f_body_sb),
            title_size, t.ink, align="center")
    yy = y_top - title_size - rh * 0.95
    for i, d in enumerate(DIAS_1):
        pg.text(x + cw * i + cw / 2, yy, d, t.f_body_sb, size - 0.4, t.ink_soft, align="center")
    yy -= rh
    for row in month_grid(year, month):
        if all(d.month != month for d in row):
            continue
        for i, d in enumerate(row):
            if d.month != month:
                continue
            cx = x + cw * i + cw / 2
            info = hol.get(d)
            if info and info[1] == "feriado":
                pg.circle(cx, yy + size * 0.33, size * 0.78, fill=t.fill_header if t.deco == "botanical" else t.fill_header)
            col = t.ink if i < 6 else t.accent if t.deco == "botanical" else t.ink_soft
            pg.text(cx, yy, str(d.day), t.f_body if i < 6 else t.f_body_b, size, col, align="center")
        yy -= rh
    return y_top - yy
