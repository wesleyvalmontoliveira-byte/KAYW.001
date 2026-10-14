# -*- coding: utf-8 -*-
"""
Extras do kit: guardas (A5), divisórias de meses com aba (A5) e adesivos (A4).
Uso: python build_extras.py
"""
import os, random
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, A5
from reportlab.pdfbase import pdfmetrics
from common import register_fonts, C, icon, sprig, flower, OUT_DIR, DELICADA, NEUTRA, MESES, MESES_ABR, DIAS_ABR
import build_capas as bc

register_fonts()
M = mm
A5W, A5H = A5
A4W, A4H = A4

FRASES_MES = ["Todo começo carrega a força de uma escolha.", "Pequenos passos também constroem grandes anos.",
              "Floresça no seu tempo.", "Constância vale mais que intensidade.", "Cuide de quem você está se tornando.",
              "Metade do ano: celebre o caminho.", "Recomeçar também é avançar.", "Descanse sem culpa, avance sem pressa.",
              "Colha o que você plantou com carinho.", "Faça do simples o seu melhor.", "Gratidão transforma o olhar.",
              "Feche o ano com orgulho de quem você foi."]


def dashed_cut(c, x, y, w, h, r=2 * M):
    c.saveState(); c.setStrokeColor(C("#C9C9C9")); c.setLineWidth(0.3); c.setDash([1.5, 1.5])
    c.roundRect(x, y, w, h, r, stroke=1, fill=0); c.restoreState()


def ctext(c, x, y, s, font, size, color, align="center"):
    c.setFont(font, size); c.setFillColor(C(color))
    if align == "center":
        c.drawCentredString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


# ------------------------------------------------------------------ GUARDAS (A5, 8 padrões)
def guardas():
    out = os.path.join(OUT_DIR, "extras", "Guardas-2027-8-padroes-A5.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    c = canvas.Canvas(out, pagesize=A5)
    c.setTitle("Guardas Planner 2027 — 8 padrões A5 (imprimir em papel 120–180 g)")
    rnd = random.Random(7)
    pads = [
        lambda: bc.fundo_poa(c, rnd, base="#F4DEDE", dot="#FFFFFF", step=8 * M, r=1.3 * M),
        lambda: bc.fundo_jardim(c, rnd),
        lambda: bc.fundo_vichy(c, rnd, base="#FFFFFF", tone="#E8CBCC", step=7 * M),
        lambda: bc.fundo_coracoes(c, rnd),
        lambda: bc.fundo_grid(c, rnd, base="#FAFAF8", line="#DCDCD6", step=6 * M),
        lambda: bc.fundo_carvao_dots(c, rnd),
        lambda: bc.fundo_diagonais(c, rnd),
        lambda: bc.fundo_linho(c, rnd),
    ]
    for fn in pads:
        fn(); c.showPage()
    c.save(); print("ok", out)


# ------------------------------------------------------------------ DIVISÓRIAS (A5, 12 meses, aba na borda externa)
def divisorias(t):
    out = os.path.join(OUT_DIR, "extras", f"Divisorias-2027-12-meses-A5-{t.name}.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    c = canvas.Canvas(out, pagesize=A5)
    c.setTitle(f"Divisórias de meses 2027 — {t.name} — A5 com aba (imprimir em papel 180–250 g)")
    rnd = random.Random(11)
    delic = t.deco != "minimal"
    for m in range(12):
        # fundo
        if delic:
            c.setFillColor(C("#FBF6F4")); c.rect(0, 0, A5W, A5H, stroke=0, fill=1)
            for i in range(14):
                sprig(c, rnd.uniform(0, A5W), rnd.uniform(0, A5H), rnd.uniform(14, 24) * M, rnd.uniform(0, 360),
                      rnd.choice(["#B8C6B2", "#CBD6C6"]), flip=rnd.random() < 0.5, leaves=6, stem_w=0.5)
            for i in range(6):
                flower(c, rnd.uniform(0, A5W), rnd.uniform(0, A5H), rnd.uniform(2, 3) * M, "#F2C4C8", "#E8D3A8")
        else:
            c.setFillColor(C("#F5F5F2")); c.rect(0, 0, A5W, A5H, stroke=0, fill=1)
            c.setStrokeColor(C("#E1E1DC")); c.setLineWidth(0.35)
            x = 0
            while x < A5W:
                c.line(x, 0, x, A5H); x += 8 * M
            y = 0
            while y < A5H:
                c.line(0, y, A5W, y); y += 8 * M
        # placa central
        bc.plate(c, A5W / 2 - 46 * M, A5H / 2 - 36 * M, 92 * M, 72 * M, alpha=0.92, r=4 * M if delic else 0)
        if delic:
            ctext(c, A5W / 2, A5H / 2 + 12 * M, f"{m + 1:02d}", "PlayfairDisplay-Regular", 54, t.accent)
            ctext(c, A5W / 2, A5H / 2 - 2 * M, MESES[m], "GreatVibes-Regular", 30, t.ink)
            c.setStrokeColor(C(t.accent)); c.setLineWidth(0.6)
            c.line(A5W / 2 - 16 * M, A5H / 2 - 7 * M, A5W / 2 + 16 * M, A5H / 2 - 7 * M)
            flower(c, A5W / 2, A5H / 2 - 7 * M, 2 * M, "#E7B9BB", "#D9B88A")
            ctext(c, A5W / 2, A5H / 2 - 15 * M, FRASES_MES[m], "PlayfairDisplay-Italic", 7.5, t.ink_soft)
            ctext(c, A5W / 2, A5H / 2 - 27 * M, "2027", "Nunito-Regular", 8, t.ink_soft)
        else:
            ctext(c, A5W / 2, A5H / 2 + 10 * M, f"{m + 1:02d}", "Montserrat-ExtraBold", 56, t.ink)
            bc.tracking_text(c, A5W / 2, A5H / 2 - 4 * M, MESES[m].upper(), "Montserrat-Medium", 15, t.ink, 4)
            c.setFillColor(C(t.ink)); c.rect(A5W / 2 - 6 * M, A5H / 2 - 9 * M, 12 * M, 0.9 * M, stroke=0, fill=1)
            ctext(c, A5W / 2, A5H / 2 - 17 * M, FRASES_MES[m], "Inter-Regular", 7.2, t.ink_soft)
            ctext(c, A5W / 2, A5H / 2 - 28 * M, "2027", "Inter-Regular", 8, t.ink_soft)
        # aba (direita, em cascata) — a artesã recorta ao redor para ficar saliente, ou mantém dentro da página
        tab_h = (A5H - 2 * 12 * M) / 12
        ty = A5H - 12 * M - (m + 1) * tab_h
        c.setFillColor(C(t.accent if delic else t.ink))
        c.roundRect(A5W - 11 * M, ty + 1 * M, 11 * M + 2, tab_h - 2 * M, 1.5 * M, stroke=0, fill=1)
        c.saveState(); c.translate(A5W - 5 * M, ty + tab_h / 2); c.rotate(-90)
        ctext(c, 0, -1.6 * M, MESES_ABR[m], "Montserrat-Bold" if not delic else "Nunito-Bold", 7, "#FFFFFF")
        c.restoreState()
        c.showPage()
    c.save(); print("ok", out)


# ------------------------------------------------------------------ ADESIVOS (A4, 2 folhas por tema)
LABELS = ["Importante", "Urgente", "Pagar", "Reunião", "Consulta", "Prova", "Aniversário", "Viagem", "Lembrete",
          "Feriado", "Folga", "Treino", "Autocuidado", "Meta batida", "Não esquecer", "Prazo final", "Hoje",
          "Prioridade", "Compras", "Encontro", "Trabalho", "Estudos", "Família", "Pausa"]
LABEL_ICONS = ["priority_high", "bolt", "payments", "work", "medical_services", "school", "cake", "flight", "push_pin",
               "celebration", "beach_access", "fitness_center", "spa", "emoji_events", "warning", "alarm", "wb_sunny",
               "star", "shopping_cart", "favorite", "work", "menu_book", "home", "local_cafe"]
ICONS = ["favorite", "star", "water_drop", "bed", "fitness_center", "menu_book", "cake", "flight", "local_cafe",
         "account_balance_wallet", "event", "check", "alarm", "pets", "restaurant", "shopping_cart", "spa",
         "directions_run", "local_hospital", "school", "work", "home", "phone", "mail", "music_note", "movie", "brush",
         "lightbulb", "flag", "savings", "celebration", "self_improvement", "local_florist", "wb_sunny", "nightlight",
         "edit", "push_pin", "bolt", "emoji_events", "card_giftcard", "directions_car", "hotel", "eco", "checklist",
         "local_mall"]
LABELS2 = ["Dentista", "Médico", "Academia", "Salão", "Escola", "Igreja", "Fatura", "Aluguel", "Luz", "Água",
           "Internet", "Mercado", "Farmácia", "Carro", "Pet", "Faxina", "Entrega", "Correios", "Live", "Postar",
           "Aula", "Terapia", "Visita", "Festa"]
HABITOS = [("water_drop", "beber água"), ("bed", "dormir cedo"), ("fitness_center", "treino"), ("menu_book", "leitura"),
           ("self_improvement", "meditação"), ("directions_run", "caminhada"), ("local_florist", "sem açúcar"),
           ("medical_services", "vitaminas"), ("savings", "guardar dinheiro"), ("phone", "menos tela"),
           ("edit", "diário"), ("wb_sunny", "sol da manhã")]
FRASES = ["Eu consigo!", "Dia de me cuidar", "Respira fundo", "Foco total", "Feito!", "Semana top",
          "Pausa para o café", "Dia de pagamento", "Hora de celebrar", "Pequenos passos", "Boa semana!", "Hoje é dia de…",
          "Orgulho de mim", "Não desista", "Um dia de cada vez", "Gratidão"]


def adesivos(t):
    delic = t.deco != "minimal"
    out = os.path.join(OUT_DIR, "extras", f"Adesivos-2027-2-folhas-A4-{t.name}.pdf")
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(f"Adesivos Planner 2027 — {t.name} — 2 folhas A4 (papel adesivo fosco)")
    pal = ["#F4DEDE", "#E8CBCC", "#D6E0D2", "#F2E6D8", "#E9E3F1", "#FBEAD8"] if delic else \
          ["#ECECE7", "#E1E1DC", "#D9D5CC", "#C8B9A6", "#A3A89A", "#F5F5F2"]
    ink = t.ink
    f_bold = "Nunito-Bold" if delic else "Montserrat-Bold"
    f_reg = "Nunito-Regular" if delic else "Inter-Regular"
    f_script = "GreatVibes-Regular" if delic else "Montserrat-Medium"
    mx, top = 12 * M, A4H - 14 * M

    def sheet_title(s, sub):
        ctext(c, mx, top + 2 * M, s, f_bold, 9, ink, align="left")
        ctext(c, A4W - mx, top + 2 * M, sub, f_reg, 6.5, t.ink_soft, align="right")
        c.setStrokeColor(C(t.line)); c.setLineWidth(0.4); c.line(mx, top, A4W - mx, top)

    # ---------- folha 1: abas de meses + rótulos + dias
    sheet_title("Folha 1 · Abas de meses, rótulos e dias da semana",
                "imprima em papel adesivo fosco A4 · recorte pelas linhas pontilhadas")
    y = top - 6 * M
    # abas de meses (2 linhas de 6)
    w, h, gap = 29 * M, 11 * M, 2.4 * M
    for i in range(12):
        col, row = i % 6, i // 6
        x = mx + col * (w + gap); yy = y - h - row * (h + gap)
        c.setFillColor(C(pal[i % len(pal)])); c.roundRect(x, yy, w, h, 2 * M, stroke=0, fill=1)
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2)
        ctext(c, x + w / 2, yy + h / 2 - 1.2 * M, MESES[i], f_bold, 8.5, ink)
    y = y - 2 * (h + gap) - 4 * M
    # rótulos (4 colunas x 6)
    w, h = 43 * M, 9.5 * M
    for i, lab in enumerate(LABELS):
        col, row = i % 4, i // 4
        x = mx + col * (w + gap); yy = y - h - row * (h + gap)
        c.setFillColor(C("#FFFFFF")); c.setStrokeColor(C(t.accent if delic else ink)); c.setLineWidth(0.6)
        c.roundRect(x, yy, w, h, 1.8 * M, stroke=1, fill=1)
        c.setFillColor(C(pal[i % len(pal)])); c.roundRect(x, yy, 9 * M, h, 1.8 * M, stroke=0, fill=1)
        c.rect(x + 6 * M, yy, 3 * M, h, stroke=0, fill=1)
        c.setFont("MaterialIcons-Regular", 10); c.setFillColor(C(ink)); c.drawCentredString(x + 4.5 * M, yy + h / 2 - 1.6 * M, icon(LABEL_ICONS[i]))
        ctext(c, x + 11 * M, yy + h / 2 - 1.2 * M, lab, f_bold, 8, ink, align="left")
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2)
    y = y - 6 * (h + gap) - 4 * M
    # dias da semana (7) + "semana N" vazios (5)
    w, h = 20 * M, 9 * M
    for i in range(7):
        x = mx + i * (w + gap); yy = y - h
        c.setFillColor(C(ink if not delic else t.accent)); c.roundRect(x, yy, w, h, 1.5 * M, stroke=0, fill=1)
        ctext(c, x + w / 2, yy + h / 2 - 1.2 * M, DIAS_ABR[i].upper(), f_bold, 8, "#FFFFFF")
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2)
    y = y - h - 4 * M
    # flags "mês" vazias para personalizar (6)
    w, h = 29 * M, 12 * M
    for i in range(6):
        x = mx + i * (w + gap); yy = y - h
        c.setFillColor(C(pal[(i + 2) % len(pal)])); c.roundRect(x, yy, w, h, 2 * M, stroke=0, fill=1)
        c.setStrokeColor(C("#FFFFFF")); c.setLineWidth(0.5); c.line(x + 4 * M, yy + 4 * M, x + w - 4 * M, yy + 4 * M)
        ctext(c, x + w / 2, yy + h - 4 * M, "escreva aqui", f_reg, 5.5, t.ink_soft)
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2)
    y = y - h - 4 * M
    # faixas decorativas (washi) 3 linhas
    for i in range(3):
        yy = y - (i + 1) * 9 * M
        wdt = A4W - 2 * mx
        if delic:
            if i == 0:
                bc.fundo_poa.__wrapped__ if False else None
                c.setFillColor(C(pal[0])); c.rect(mx, yy, wdt, 7 * M, stroke=0, fill=1)
                c.setFillColor(C("#FFFFFF"))
                xx = mx + 3 * M
                while xx < mx + wdt:
                    c.circle(xx, yy + 3.5 * M, 1.2 * M, stroke=0, fill=1); xx += 6 * M
            elif i == 1:
                c.setFillColor(C("#FFFFFF")); c.rect(mx, yy, wdt, 7 * M, stroke=0, fill=1)
                xx = mx
                while xx < mx + wdt:
                    sprig(c, xx, yy + 2 * M, 10 * M, 15, "#9FB09A", leaves=5, stem_w=0.5); xx += 14 * M
            else:
                c.setFillColor(C(pal[2])); c.rect(mx, yy, wdt, 7 * M, stroke=0, fill=1)
                xx = mx + 4 * M
                while xx < mx + wdt:
                    bc.heart(c, xx, yy + 3.5 * M, 1.4 * M, "#C98B8F"); xx += 8 * M
        else:
            if i == 0:
                c.setFillColor(C(ink)); c.rect(mx, yy, wdt, 7 * M, stroke=0, fill=1)
                xx = mx
                c.setFillColor(C("#FFFFFF"))
                while xx < mx + wdt:
                    c.rect(xx, yy, 3 * M, 7 * M, stroke=0, fill=1); xx += 6 * M
            elif i == 1:
                c.setFillColor(C(pal[3])); c.rect(mx, yy, wdt, 7 * M, stroke=0, fill=1)
                c.setFillColor(C("#FFFFFF"))
                xx = mx + 3 * M
                while xx < mx + wdt:
                    c.circle(xx, yy + 3.5 * M, 0.7 * M, stroke=0, fill=1); xx += 4 * M
            else:
                c.setFillColor(C(pal[4])); c.rect(mx, yy, wdt, 7 * M, stroke=0, fill=1)
                c.setStrokeColor(C("#FFFFFF")); c.setLineWidth(0.8)
                xx = mx
                while xx < mx + wdt:
                    c.line(xx, yy, xx + 7 * M, yy + 7 * M); xx += 5 * M
        dashed_cut(c, mx - 1, yy - 1, wdt + 2, 7 * M + 2, r=0)
    y = y - 3 * 9 * M - 4 * M
    # rótulos preenchidos (compromissos e contas) 6 colunas x 4
    w, h = 28.5 * M, 8.5 * M
    for i, lab in enumerate(LABELS2):
        col, row = i % 6, i // 6
        x = mx + col * (w + gap); yy = y - h - row * (h + gap)
        c.setFillColor(C(pal[(i + row) % len(pal)])); c.roundRect(x, yy, w, h, 1.6 * M, stroke=0, fill=1)
        ctext(c, x + w / 2, yy + h / 2 - 1.1 * M, lab, f_bold, 7.2, ink)
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2)
    y = y - 4 * (h + gap) - 4 * M
    # mini-etiquetas "pago" / "feito" / "ok" redondas (14)
    d = 10 * M
    tags = ["PAGO", "FEITO", "OK", "TOP", "URGENTE", "HOJE", "META", "PAGO", "FEITO", "OK", "TOP", "URGENTE", "HOJE", "META"]
    for i, tg in enumerate(tags):
        x = mx + i * (d + 3.3 * M) + d / 2; yy = y - d / 2
        c.setFillColor(C(ink if not delic else t.accent) if i % 2 == 0 else C(pal[i % len(pal)]))
        c.circle(x, yy, d / 2, stroke=0, fill=1)
        ctext(c, x, yy - 1 * M, tg, f_bold, 4.8, "#FFFFFF" if i % 2 == 0 else ink)
        c.saveState(); c.setStrokeColor(C("#C9C9C9")); c.setLineWidth(0.3); c.setDash([1.5, 1.5])
        c.circle(x, yy, d / 2 + 1, stroke=1, fill=0); c.restoreState()
    c.showPage()

    # ---------- folha 2: ícones + frases + formas
    sheet_title("Folha 2 · Ícones, frases e formas", "imprima em papel adesivo fosco A4 · recorte pelas linhas pontilhadas")
    y = top - 6 * M
    d, gap = 13 * M, 2.6 * M
    per_row = 12
    for i, name in enumerate(ICONS[:48]):
        col, row = i % per_row, i // per_row
        x = mx + col * (d + gap) + d / 2; yy = y - d / 2 - row * (d + gap)
        c.setFillColor(C(pal[i % len(pal)])); c.circle(x, yy, d / 2, stroke=0, fill=1)
        c.setFont("MaterialIcons-Regular", 15); c.setFillColor(C(ink)); c.drawCentredString(x, yy - 2 * M, icon(name))
        c.saveState(); c.setStrokeColor(C("#C9C9C9")); c.setLineWidth(0.3); c.setDash([1.5, 1.5])
        c.circle(x, yy, d / 2 + 1, stroke=1, fill=0); c.restoreState()
    rows = (min(len(ICONS), 48) + per_row - 1) // per_row
    y = y - rows * (d + gap) - 4 * M
    # frases (4 colunas x 4)
    w, h = 43 * M, 13 * M
    for i, fr in enumerate(FRASES):
        col, row = i % 4, i // 4
        x = mx + col * (w + gap); yy = y - h - row * (h + gap)
        c.setFillColor(C(pal[(i + 1) % len(pal)] if i % 2 else "#FFFFFF"))
        c.setStrokeColor(C(t.accent if delic else ink)); c.setLineWidth(0.6)
        c.roundRect(x, yy, w, h, 2.5 * M if delic else 0, stroke=1, fill=1)
        ctext(c, x + w / 2, yy + h / 2 - 2 * M, fr, f_script, 15 if delic else 9, ink)
        if delic:
            flower(c, x + w - 5 * M, yy + h - 4 * M, 1.6 * M, "#E7B9BB", "#D9B88A")
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2)
    y = y - 4 * (h + gap) - 4 * M
    # formas pequenas: corações, estrelas, checks, setas (4 linhas de 14)
    s = 9 * M
    for row in range(4):
        for col in range(14):
            x = mx + col * (s + 3.5 * M) + s / 2; yy = y - s / 2 - row * (s + 3.5 * M)
            color = pal[(row * 2 + col) % len(pal)]
            if row == 0:
                bc.heart(c, x, yy, 2.6 * M, t.accent if delic else ink)
            elif row == 1:
                bc.star4(c, x, yy, 3.4 * M, "#D9B88A" if delic else "#C8B9A6")
            elif row == 2:
                c.setFillColor(C(color)); c.circle(x, yy, s / 2, stroke=0, fill=1)
                c.setFont("MaterialIcons-Regular", 12); c.setFillColor(C(ink)); c.drawCentredString(x, yy - 1.6 * M, icon("check"))
            else:
                c.setFillColor(C(color)); c.roundRect(x - s / 2, yy - s / 2, s, s, 1.5 * M, stroke=0, fill=1)
                c.setFont("MaterialIcons-Regular", 12); c.setFillColor(C(ink)); c.drawCentredString(x, yy - 1.6 * M, icon(["arrow_forward", "flag", "favorite_border", "star_border"][col % 4]))
            c.saveState(); c.setStrokeColor(C("#C9C9C9")); c.setLineWidth(0.3); c.setDash([1.5, 1.5])
            c.circle(x, yy, s / 2 + 1, stroke=1, fill=0); c.restoreState()
    y = y - 4 * (s + 3.5 * M) - 4 * M
    # chips de hábitos (ícone + palavra) 4 colunas x 3
    w, h = 43 * M, 9 * M
    for i, (ic, lab) in enumerate(HABITOS):
        col, row = i % 4, i // 4
        x = mx + col * (w + gap); yy = y - h - row * (h + gap)
        c.setFillColor(C(pal[(i + 2) % len(pal)])); c.roundRect(x, yy, w, h, 4.5 * M if delic else 1.5 * M, stroke=0, fill=1)
        c.setFont("MaterialIcons-Regular", 10); c.setFillColor(C(ink)); c.drawCentredString(x + 6 * M, yy + h / 2 - 1.6 * M, icon(ic))
        ctext(c, x + 11 * M, yy + h / 2 - 1.2 * M, lab, f_bold, 7.5, ink, align="left")
        dashed_cut(c, x - 1, yy - 1, w + 2, h + 2, r=4.5 * M if delic else 1.5 * M)
    y = y - 3 * (h + gap) - 4 * M
    # contagem regressiva 1–15 + "dia D"
    d = 10 * M
    for i in range(16):
        x = mx + i * (d + 2.4 * M) + d / 2; yy = y - d / 2
        c.setFillColor(C("#FFFFFF")); c.setStrokeColor(C(t.accent if delic else ink)); c.setLineWidth(0.6)
        c.circle(x, yy, d / 2, stroke=1, fill=1)
        ctext(c, x, yy - 1.3 * M, str(15 - i) if i < 15 else "D", f_bold, 8, ink)
        c.saveState(); c.setStrokeColor(C("#C9C9C9")); c.setLineWidth(0.3); c.setDash([1.5, 1.5])
        c.circle(x, yy, d / 2 + 1, stroke=1, fill=0); c.restoreState()
    ctext(c, mx, y - d - 4 * M, "contagem regressiva · cole um por dia até o grande dia", f_reg, 6, t.ink_soft, align="left")
    c.showPage()
    c.save(); print("ok", out)


if __name__ == "__main__":
    guardas()
    for t in (DELICADA, NEUTRA):
        divisorias(t)
        adesivos(t)
