# -*- coding: utf-8 -*-
"""Páginas do miolo do Planner 2027 (A5)."""
import datetime as dt
from reportlab.lib.units import mm
from common import (C, MESES, MESES_ABR, DIAS, DIAS_ABR, DIAS_1, month_grid, mini_calendar,
                    corner_botanical, sprig, flower, stars_row, feriados, datas_comemorativas,
                    fmt_range, nth_weekday)

M = mm

QUOTES = [
    "Todo começo carrega a força de uma escolha.",
    "Pequenos passos, todos os dias, constroem grandes caminhos.",
    "Floresça onde você plantou suas intenções.",
    "Organizar o tempo é cuidar de quem você quer se tornar.",
    "Gratidão transforma o que temos em suficiente.",
    "Metade do caminho: celebre o quanto você já andou.",
    "Descansar também faz parte do plano.",
    "Constância vale mais do que intensidade.",
    "Recomece quantas vezes forem necessárias.",
    "O que você prioriza hoje desenha o seu amanhã.",
    "Finalize com carinho o que você começou com coragem.",
    "Olhe para trás com orgulho e para frente com esperança.",
]


# ------------------------------------------------------------------ helpers
def fit_rows(h_avail, row_h, header=True, pad=1 * M):
    n = int((h_avail - pad) // row_h) - (1 if header else 0)
    return max(1, n)


def field(pg, x, y, w, label, lw=None, size=7.2):
    """Campo 'Label ________' numa linha. Retorna nada."""
    t = pg.t
    lw = lw or pg.text(0, -100, label, t.f_body_sb, size)  # largura do rótulo
    pg.text(x, y, label, t.f_body_sb, size, t.ink)
    pg.line(x + lw + 2 * M, y - 0.8 * M, x + w, y - 0.8 * M, t.line, 0.5)


def check_lines(pg, x, y_top, w, n, gap=6.4 * M, numbered=False):
    t = pg.t
    y = y_top
    for i in range(n):
        if numbered:
            pg.circle(x + 1.7 * M, y + 1.1 * M, 1.9 * M, fill=t.fill_header)
            pg.text(x + 1.7 * M, y + 0.2 * M, str(i + 1), t.f_body_b, 6, t.ink, align="center")
        else:
            pg.checkbox(x, y - 0.6 * M)
        pg.line(x + 5.2 * M, y - 0.8 * M, x + w, y - 0.8 * M, t.line_soft, 0.5)
        y -= gap
    return y


def table(pg, x, y_top, w, cols, rows, row_h=6.2 * M, header=True, zebra=False, head_size=6.6,
          dotted=False):
    """cols = [(label, width_fraction, align)], rows = número de linhas vazias ou lista de listas."""
    t = pg.t
    total_frac = sum(c[1] for c in cols)
    widths = [w * c[1] / total_frac for c in cols]
    y = y_top
    if header:
        pg.rect(x, y - row_h, w, row_h, fill=t.fill_header)
        cx = x
        for (label, frac, align), cw in zip(cols, widths):
            tx = cx + 1.8 * M if align == "left" else cx + cw / 2 if align == "center" else cx + cw - 1.8 * M
            pg.text(tx, y - row_h + 2.1 * M, label.upper() if t.deco == "minimal" else label,
                    t.f_body_sb, head_size, t.ink, align=align, tracking=0.4 if t.deco == "minimal" else 0)
            cx += cw
        y -= row_h
    n = rows if isinstance(rows, int) else len(rows)
    for r in range(n):
        if zebra and r % 2 == 1:
            pg.rect(x, y - row_h, w, row_h, fill=t.fill_soft)
        if not isinstance(rows, int):
            cx = x
            for (label, frac, align), cw, val in zip(cols, widths, rows[r]):
                tx = cx + 1.8 * M if align == "left" else cx + cw / 2 if align == "center" else cx + cw - 1.8 * M
                if val:
                    pg.text(tx, y - row_h + 2.0 * M, str(val), t.f_body, 7, t.ink, align=align)
                cx += cw
        pg.line(x, y - row_h, x + w, y - row_h, t.line_soft, 0.45, [0.6, 1.6] if dotted else None)
        y -= row_h
    # bordas verticais
    cx = x
    for cw in widths[:-1]:
        cx += cw
        pg.line(cx, y_top, cx, y, t.line_soft, 0.45)
    pg.rect(x, y, w, y_top - y, stroke=t.line, width=0.55)
    return y


def progress_segments(pg, x, y, w, n=10, h=3.2 * M, gap=0.8 * M):
    t = pg.t
    sw = (w - gap * (n - 1)) / n
    for i in range(n):
        pg.rect(x + i * (sw + gap), y, sw, h, stroke=t.line, fill="#FFFFFF", width=0.5,
                r=0.8 * M if t.deco == "botanical" else 0)


def circles_row(pg, x, y, n, r=1.6 * M, gap=None, labels=None, stroke=None):
    t = pg.t
    gap = gap or (r * 2 + 1.6 * M)
    for i in range(n):
        pg.circle(x + i * gap + r, y, r, stroke=stroke or t.line, width=0.55)
        if labels:
            pg.text(x + i * gap + r, y - r - 2.4 * M, labels[i], t.f_body, 5.2, t.ink_soft, align="center")


def deco_bottom(pg):
    """Decoração discreta no rodapé externo (só tema botânico)."""
    t = pg.t
    if t.deco != "botanical":
        return
    x = pg.x1 - 2 * M if pg.recto else pg.x0 + 2 * M
    sprig(pg.c, x, 8.5 * M, 16 * M, 160 if pg.recto else 20, "#C9D3C4", flip=pg.recto, leaves=5, stem_w=0.45)


# ------------------------------------------------------------------ páginas iniciais
def p_title(pg, year=2027):
    t, c = pg.t, pg.c
    W, H = pg.W, pg.H
    if t.deco == "botanical":
        corner_botanical(c, 8 * M, H - 8 * M, 46 * M, t, flip_y=True)
        corner_botanical(c, W - 8 * M, 8 * M, 46 * M, t, flip_x=True)
        pg.text(W / 2, H * 0.60, "Planner", t.f_script, 46, t.accent, align="center")
        pg.text(W / 2, H * 0.60 - 24 * M, str(year), t.f_title_b, 74, t.ink, align="center")
        pg.line(W / 2 - 22 * M, H * 0.60 - 30 * M, W / 2 + 22 * M, H * 0.60 - 30 * M, t.accent3, 0.8)
        pg.text(W / 2, H * 0.60 - 38 * M, "um ano para planejar com leveza", t.f_title_i, 10, t.ink_soft, align="center")
        pg.text(W / 2, H * 0.24, "este planner pertence a", t.f_body, 7.5, t.ink_soft, align="center")
        pg.line(W / 2 - 34 * M, H * 0.24 - 9 * M, W / 2 + 34 * M, H * 0.24 - 9 * M, t.line, 0.6)
    else:
        pg.rect(0, 0, W, H, fill="#FFFFFF")
        pg.rect(pg.x0, H - 40 * M, 14 * M, 1.4 * M, fill=t.accent)
        pg.text(pg.x0 - 1.5 * M, H * 0.50, str(year), "Montserrat-ExtraBold", 96, t.ink)
        pg.text(pg.x0, H * 0.50 - 12 * M, "PLANNER", t.f_title_b, 16, t.ink, tracking=7)
        pg.text(pg.x0, H * 0.50 - 20 * M, "planejamento anual · mensal · semanal", t.f_body, 7.6, t.ink_soft)
        pg.text(pg.x0, H * 0.22, "PERTENCE A", t.f_body_sb, 6.5, t.ink_soft, tracking=1.5)
        pg.line(pg.x0, H * 0.22 - 7 * M, pg.x1, H * 0.22 - 7 * M, t.ink, 0.7)
        pg.line(pg.x0, 12 * M, pg.x1, 12 * M, t.line, 0.6)


def p_dados(pg):
    t = pg.t
    y = pg.header("Dados pessoais", "informações importantes à mão", "person")
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0 + 70 * M, pg.w, y - pg.y0 - 70 * M, "Sobre mim", icon_name="person")
    labels = ["Nome", "Telefone", "E-mail", "Endereço", "Cidade / UF", "Instagram", "Data de nascimento",
              "Profissão"]
    yy = yi - 6 * M
    for lb in labels:
        field(pg, xi, yy, wi, lb, lw=30 * M)
        yy -= 10.5 * M
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, 66 * M, "Em caso de emergência", icon_name="medical_services")
    yy = yi - 6 * M
    for lb in ["Ligar para", "Telefone", "Tipo sanguíneo", "Alergias / medicamentos", "Plano de saúde"]:
        field(pg, xi, yy, wi, lb, lw=38 * M)
        yy -= 10.5 * M
    pg.footer("Dados pessoais")
    deco_bottom(pg)


def p_calendario(pg, year, hol, subtitle=None):
    t = pg.t
    y = pg.header(f"Calendário {year}", subtitle or "visão geral do ano", "calendar_today")
    cols, rows = 3, 4
    gw, gh = pg.w / cols, (y - pg.y0 - 7 * M) / rows
    for m in range(12):
        cx = pg.x0 + (m % cols) * gw
        cy = y - (m // cols) * gh
        mini_calendar(pg, cx + 2 * M, cy - 1 * M, gw - 4 * M, year, m + 1, hol, size=5.9, title_size=7.6)
    # legenda
    pg.circle(pg.x0 + 2 * M, pg.y0 + 2.4 * M, 1.6 * M, fill=t.fill_header)
    pg.text(pg.x0 + 5 * M, pg.y0 + 1.4 * M, "feriado nacional", t.f_body, 6.4, t.ink_soft)
    pg.footer(f"Calendário {year}")


def p_feriados(pg, year):
    t = pg.t
    y = pg.header(f"Feriados e datas {year}", "para programar o ano com antecedência", "event")
    hol = feriados(year)
    com = datas_comemorativas(year)
    colw = (pg.w - 4 * M) / 2
    # coluna esquerda: feriados + facultativos
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, colw, y - pg.y0, "Feriados nacionais", icon_name="flag")
    yy = yi - 4.5 * M
    for d, (name, kind) in sorted(hol.items()):
        if kind == "data":
            continue
        pg.text(xi, yy, f"{d.day:02d}/{d.month:02d}", t.f_body_b, 7, t.ink)
        pg.text(xi + 11 * M, yy, DIAS_ABR[d.weekday()], t.f_body, 6.2, t.ink_soft)
        lines = pg.wrap(name + (" (ponto facultativo)" if kind == "facultativo" else ""), t.f_body, 6.6, wi - 18 * M)
        for ln in lines:
            pg.text(xi + 18 * M, yy, ln, t.f_body, 6.6, t.ink if kind == "feriado" else t.ink_soft)
            yy -= 3.6 * M
        yy -= 3.3 * M
    yy -= 2 * M
    pg.text(xi, yy, "Feriados municipais e estaduais da minha cidade:", t.f_body_sb, 6.4, t.ink)
    yy -= 7 * M
    while yy > pg.y0 + 4 * M:
        pg.line(xi, yy, xi + wi, yy, t.line_soft, 0.45)
        yy -= 6.5 * M
    # coluna direita: datas comemorativas
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 4 * M, pg.y0, colw, y - pg.y0, "Datas comemorativas", icon_name="celebration")
    yy = yi - 4.5 * M
    for d, name in sorted(com.items()):
        pg.text(xi, yy, f"{d.day:02d}/{d.month:02d}", t.f_body_b, 7, t.ink)
        pg.text(xi + 11 * M, yy, DIAS_ABR[d.weekday()], t.f_body, 6.2, t.ink_soft)
        lines = pg.wrap(name, t.f_body, 6.6, wi - 18 * M)
        for ln in lines:
            pg.text(xi + 18 * M, yy, ln, t.f_body, 6.6, t.ink)
            yy -= 3.6 * M
        yy -= 3.3 * M
    pg.footer(f"Feriados {year}")


def p_datas_importantes(pg):
    t = pg.t
    y = pg.header("Datas importantes", "aniversários, comemorações e lembretes do ano", "cake")
    cols, rows = 3, 4
    gap = 3 * M
    gw = (pg.w - gap * (cols - 1)) / cols
    gh = (y - pg.y0 - gap * (rows - 1)) / rows
    for m in range(12):
        cx = pg.x0 + (m % cols) * (gw + gap)
        cy = y - (m // cols) * (gh + gap) - gh
        xi, yi, wi, hi = pg.box(cx, cy, gw, gh, MESES[m], title_size=7.6)
        pg.ruled(xi, yi - 4.6 * M, wi, int((hi - 3 * M) // (6.3 * M)), gap=6.3 * M)
    pg.footer("Datas importantes")


def p_metas(pg, year):
    t = pg.t
    y = pg.header(f"Metas {year}", "o que eu quero construir neste ano", "emoji_events")
    xi, yi, wi, hi = pg.box(pg.x0, y - 16 * M, pg.w, 16 * M, fill=t.fill_soft)
    pg.text(xi, yi - 4.5 * M, "Minha palavra do ano:", t.f_title_i if t.deco == "botanical" else t.f_body_sb, 9, t.ink)
    pg.line(xi + 40 * M, yi - 5.3 * M, xi + wi, yi - 5.3 * M, t.line, 0.6)
    areas = [("Pessoal", "self_improvement"), ("Carreira e estudos", "work"), ("Finanças", "savings"),
             ("Saúde e bem-estar", "spa"), ("Relacionamentos", "favorite"), ("Lazer e sonhos", "flight")]
    top = y - 20 * M
    gap = 3 * M
    gw = (pg.w - gap) / 2
    gh = (top - pg.y0 - 2 * gap) / 3
    for i, (name, ic) in enumerate(areas):
        cx = pg.x0 + (i % 2) * (gw + gap)
        cy = top - (i // 2) * (gh + gap) - gh
        xi, yi, wi, hi = pg.box(cx, cy, gw, gh, name, icon_name=ic)
        check_lines(pg, xi, yi - 4.6 * M, wi, int((hi - 2 * M) // (6.8 * M)), gap=6.8 * M)
    pg.footer(f"Metas {year}")


def p_ano_em_cores(pg, year):
    t = pg.t
    y = pg.header("Meu ano em cores", "pinte um quadradinho por dia conforme o seu humor", "palette")
    # legenda
    moods = ["ótimo", "bom", "normal", "cansativo", "difícil", "especial"]
    lx = pg.x0
    for i, md in enumerate(moods):
        pg.circle(lx + 2 * M, y - 3 * M, 1.9 * M, stroke=t.line, width=0.6)
        pg.text(lx + 5.2 * M, y - 3.9 * M, md, t.f_body, 6.4, t.ink)
        lx += pg.w / len(moods)
    top = y - 9 * M
    left_w = 8 * M
    gw = (pg.w - left_w) / 12
    gh = (top - pg.y0 - 6 * M) / 31
    for m in range(12):
        pg.text(pg.x0 + left_w + m * gw + gw / 2, top - 4.2 * M, MESES_ABR[m], t.f_body_sb, 5.6, t.ink, align="center")
    gy = top - 6 * M
    for d in range(31):
        yy = gy - d * gh
        pg.text(pg.x0 + left_w - 1.5 * M, yy - gh + 1.3 * M, str(d + 1), t.f_body, 5.4, t.ink_soft, align="right")
        for m in range(12):
            ndays = (dt.date(year + (1 if m == 11 else 0), 1 if m == 11 else m + 2, 1) - dt.date(year, m + 1, 1)).days
            if d < ndays:
                pg.rect(pg.x0 + left_w + m * gw, yy - gh, gw, gh, stroke=t.line_soft, width=0.45, fill="#FFFFFF")
            else:
                pg.rect(pg.x0 + left_w + m * gw, yy - gh, gw, gh, stroke=t.line_soft, width=0.45, fill=t.fill_soft)
    pg.footer("Meu ano em cores")


def p_saude(pg):
    t = pg.t
    y = pg.header("Minha saúde", "acompanhamento do ano", "monitor_heart")
    xi, yi, wi, hi = pg.box(pg.x0, y - 74 * M, pg.w, 74 * M, "Medidas e acompanhamento", icon_name="monitor_weight")
    cols = [("", 2.2, "left"), ("Jan", 1, "center"), ("Abr", 1, "center"), ("Jul", 1, "center"), ("Out", 1, "center")]
    rows = [["Peso", "", "", "", ""], ["Altura / IMC", "", "", "", ""], ["Cintura", "", "", "", ""],
            ["Quadril", "", "", "", ""], ["Pressão arterial", "", "", "", ""], ["Como me sinto (1–10)", "", "", "", ""]]
    table(pg, xi, yi - 1 * M, wi, cols, rows, row_h=8 * M)
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, y - pg.y0 - 78 * M, "Consultas", icon_name="medical_services")
    cols = [("Data", 1, "left"), ("Especialidade", 1.8, "left"), ("Profissional", 1.8, "left"), ("Retorno", 1, "left")]
    table(pg, xi, yi - 1 * M, wi, cols, fit_rows(hi, 7.2 * M), row_h=7.2 * M)
    pg.footer("Minha saúde")


def p_exames(pg):
    t = pg.t
    y = pg.header("Exames e cuidados", "para não perder nenhuma data", "vaccines")
    h1 = 64 * M
    xi, yi, wi, hi = pg.box(pg.x0, y - h1, pg.w, h1, "Exames", icon_name="biotech")
    table(pg, xi, yi - 1 * M, wi, [("Exame", 2, "left"), ("Data", 1, "left"), ("Resultado", 1.6, "left"), ("Próximo", 1, "left")], fit_rows(hi, 7 * M), row_h=7 * M)
    h2 = 54 * M
    xi, yi, wi, hi = pg.box(pg.x0, y - h1 - 4 * M - h2, pg.w, h2, "Medicamentos e vitaminas", icon_name="medication")
    table(pg, xi, yi - 1 * M, wi, [("Nome", 2, "left"), ("Dose", 1, "left"), ("Horário", 1, "left"), ("Período", 1.2, "left")], fit_rows(hi, 6.6 * M), row_h=6.6 * M)
    h3 = y - h1 - h2 - 8 * M - pg.y0
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, h3, "Vacinas", icon_name="vaccines")
    table(pg, xi, yi - 1 * M, wi, [("Vacina", 2, "left"), ("Data", 1, "left"), ("Dose", 1, "left"), ("Próxima", 1, "left")], fit_rows(hi, 6.6 * M), row_h=6.6 * M)
    pg.footer("Exames e cuidados")


def p_fin_ano(pg, year):
    t = pg.t
    y = pg.header("Visão financeira do ano", "resumo mês a mês", "account_balance_wallet")
    cols = [("Mês", 1.1, "left"), ("Receitas", 1.2, "left"), ("Despesas", 1.2, "left"), ("Economizei", 1.2, "left"), ("Saldo", 1.1, "left")]
    rows = [[MESES[m], "", "", "", ""] for m in range(12)] + [["Total", "", "", "", ""]]
    yb = table(pg, pg.x0, y, pg.w, cols, rows, row_h=8.6 * M, zebra=True)
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, yb - 4 * M - pg.y0, "Reserva de emergência", icon_name="savings", fill=t.fill_soft)
    field(pg, xi, yi - 5 * M, wi / 2 - 3 * M, "Meta:  R$", lw=16 * M)
    field(pg, xi + wi / 2, yi - 5 * M, wi / 2, "Tenho hoje:  R$", lw=24 * M)
    pg.text(xi, yi - 12.5 * M, "Progresso (cada bloco = 10%)", t.f_body, 6.4, t.ink_soft)
    progress_segments(pg, xi, yi - 18.5 * M, wi, 10, h=4 * M)
    pg.footer("Visão financeira")


def p_metas_fin(pg):
    t = pg.t
    y = pg.header("Metas financeiras", "sonhos com valor, prazo e plano", "savings")
    gap = 3.5 * M
    gw = (pg.w - gap) / 2
    gh = (y - pg.y0 - gap) / 2
    for i in range(4):
        cx = pg.x0 + (i % 2) * (gw + gap)
        cy = y - (i // 2) * (gh + gap) - gh
        xi, yi, wi, hi = pg.box(cx, cy, gw, gh, f"Meta {i + 1}", icon_name="flag")
        yy = yi - 5 * M
        for lb in ["O que", "Valor total  R$", "Prazo", "Guardar por mês  R$"]:
            field(pg, xi, yy, wi, lb, lw=pg.text(0, -100, lb, t.f_body_sb, 7.2))
            yy -= 9.5 * M
        pg.text(xi, yy - 1 * M, "Progresso", t.f_body, 6.4, t.ink_soft)
        progress_segments(pg, xi, yy - 7 * M, wi, 10, h=4 * M)
        pg.text(xi, yy - 11.5 * M, "0%", t.f_body, 5.4, t.ink_soft)
        pg.text(xi + wi, yy - 11.5 * M, "100%", t.f_body, 5.4, t.ink_soft, align="right")
        pg.text(xi, yy - 18 * M, "Primeiro passo:", t.f_body_sb, 6.6, t.ink)
        pg.line(xi + 22 * M, yy - 18.8 * M, xi + wi, yy - 18.8 * M, t.line, 0.5)
        pg.text(xi, yy - 26 * M, "Conquistei em:", t.f_body_sb, 6.6, t.ink)
        pg.line(xi + 22 * M, yy - 26.8 * M, xi + wi, yy - 26.8 * M, t.line, 0.5)
    pg.footer("Metas financeiras")


def p_acessos(pg):
    t = pg.t
    y = pg.header("Acessos e assinaturas", "serviços, logins e renovações", "key")
    cols = [("Serviço", 1.5, "left"), ("Login", 1.6, "left"), ("Dica de senha", 1.6, "left"), ("Valor", 0.9, "left"), ("Renova em", 1.0, "left")]
    yb = table(pg, pg.x0, y, pg.w, cols, 17, row_h=8.3 * M, zebra=True)
    pg.icon(pg.x0, pg.y0 + 1.6 * M, "lock", size=7, color=t.ink_soft)
    pg.text(pg.x0 + 4.5 * M, pg.y0 + 1.6 * M, "Dica de segurança: anote apenas pistas da senha, nunca a senha completa.", t.f_body, 6.2, t.ink_soft)
    pg.footer("Acessos e assinaturas")


def p_leituras(pg):
    t = pg.t
    y = pg.header("Minhas leituras", "livros do ano e minhas notas", "menu_book")
    cols = [("Título", 2.4, "left"), ("Autor", 1.6, "left"), ("Início", 0.8, "left"), ("Fim", 0.8, "left"), ("Nota", 1.3, "left")]
    total = sum(c[1] for c in cols)
    yb = table(pg, pg.x0, y, pg.w, cols, 18, row_h=8.2 * M, zebra=True)
    # estrelinhas vazias na coluna nota
    xstar = pg.x0 + pg.w * (sum(c[1] for c in cols[:-1]) / total) + 1.6 * M
    yy = y - 8.2 * M
    for r in range(18):
        yy -= 8.2 * M
        stars_row(pg, xstar, yy + 2.2 * M, 5, size=6.6)
    pg.footer("Minhas leituras")


def p_favoritos(pg):
    t = pg.t
    y = pg.header("Favoritos do ano", "para lembrar o que me fez bem", "favorite")
    items = [("Livros", "menu_book"), ("Filmes e séries", "movie"), ("Músicas e podcasts", "music_note"), ("Lugares e sabores", "restaurant")]
    gap = 3.5 * M
    gw = (pg.w - gap) / 2
    gh = (y - pg.y0 - gap) / 2
    for i, (name, ic) in enumerate(items):
        cx = pg.x0 + (i % 2) * (gw + gap)
        cy = y - (i // 2) * (gh + gap) - gh
        xi, yi, wi, hi = pg.box(cx, cy, gw, gh, name, icon_name=ic)
        pg.ruled(xi, yi - 5 * M, wi, 9, gap=7.6 * M)
    pg.footer("Favoritos do ano")


def p_lugares_quero(pg):
    t = pg.t
    y = pg.header("Lugares que quero conhecer", "a lista de sonhos de viagem", "flight")
    cols = [("", 0.35, "center"), ("Lugar", 2.2, "left"), ("Quando", 1, "left"), ("Com quem", 1.3, "left"), ("Preciso guardar", 1.2, "left")]
    yb = table(pg, pg.x0, y, pg.w, cols, 12, row_h=9 * M, zebra=True)
    xx = pg.x0 + pg.w * (0.35 / sum(c[1] for c in cols)) / 2 - 1.6 * M
    yy = y - 9 * M
    for r in range(12):
        yy -= 9 * M
        pg.checkbox(xx, yy + 2.9 * M)
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, yb - 4 * M - pg.y0, "Próxima viagem: o que preciso resolver", icon_name="luggage", fill=t.fill_soft)
    check_lines(pg, xi, yi - 4.5 * M, wi / 2 - 3 * M, 4, gap=6.6 * M)
    check_lines(pg, xi + wi / 2, yi - 4.5 * M, wi / 2, 4, gap=6.6 * M)
    pg.footer("Lugares que quero conhecer")


def p_lugares_visitados(pg):
    t = pg.t
    y = pg.header("Lugares já visitados", "memórias para guardar", "place")
    n = 7
    gh = (y - pg.y0) / n
    for i in range(n):
        cy = y - (i + 1) * gh
        pg.rect(pg.x0, cy + 1.2 * M, pg.w, gh - 2.4 * M, stroke=t.line, width=0.55, r=2 * M if t.deco == "botanical" else 0)
        pg.icon(pg.x0 + 2.5 * M, cy + gh - 7.2 * M, "place", size=8)
        field(pg, pg.x0 + 7.5 * M, cy + gh - 7 * M, pg.w * 0.55, "Lugar", lw=10 * M)
        field(pg, pg.x0 + pg.w * 0.66, cy + gh - 7 * M, pg.w * 0.34 - 3 * M, "Data", lw=8 * M)
        pg.text(pg.x0 + 2.5 * M, cy + gh - 13.5 * M, "Melhor lembrança:", t.f_body_sb, 6.8, t.ink)
        pg.line(pg.x0 + 2.5 * M, cy + gh - 19.5 * M, pg.x1 - 2.5 * M, cy + gh - 19.5 * M, t.line_soft, 0.5)
    pg.footer("Lugares já visitados")


def p_projetos(pg):
    t = pg.t
    y = pg.header("Projetos e planos", "do sonho à execução", "lightbulb")
    gap = 3.5 * M
    gw = (pg.w - gap) / 2
    gh = (y - pg.y0 - gap) / 2
    for i in range(4):
        cx = pg.x0 + (i % 2) * (gw + gap)
        cy = y - (i // 2) * (gh + gap) - gh
        xi, yi, wi, hi = pg.box(cx, cy, gw, gh, f"Projeto {i + 1}", icon_name="rocket_launch")
        yy = yi - 5 * M
        field(pg, xi, yy, wi, "Nome", lw=10 * M)
        yy -= 9 * M
        pg.text(xi, yy, "Objetivo", t.f_body_sb, 7.2, t.ink)
        yy -= 6 * M
        pg.ruled(xi, yy, wi, 2, gap=6.5 * M)
        yy -= 10 * M
        pg.text(xi, yy, "Passos", t.f_body_sb, 7.2, t.ink)
        yy -= 5.5 * M
        yy = check_lines(pg, xi, yy, wi, 4, gap=6.4 * M)
        field(pg, xi, yy - 1 * M, wi, "Prazo", lw=10 * M)
    pg.footer("Projetos e planos")


def p_desejos(pg):
    t = pg.t
    y = pg.header("Lista de desejos", "com prioridade, para comprar com consciência", "shopping_bag")
    cols = [("", 0.35, "center"), ("Item", 2.4, "left"), ("Valor", 1, "left"), ("Prioridade", 1.1, "center"), ("Comprei em", 1, "left")]
    total = sum(c[1] for c in cols)
    yb = table(pg, pg.x0, y, pg.w, cols, 17, row_h=8.6 * M, zebra=True)
    xx = pg.x0 + pg.w * (0.35 / total) / 2 - 1.6 * M
    xp = pg.x0 + pg.w * (sum(c[1] for c in cols[:3]) / total) + pg.w * (1.1 / total) / 2
    yy = y - 8.6 * M
    for r in range(17):
        yy -= 8.6 * M
        pg.checkbox(xx, yy + 2.7 * M)
        circles_row(pg, xp - 6.6 * M, yy + 4.3 * M, 3, r=1.3 * M, gap=4.6 * M)
    pg.text(pg.x0, pg.y0 + 1.6 * M, "Prioridade: pinte 1, 2 ou 3 bolinhas · Regra dos 7 dias: anote, espere uma semana e decida com calma.", t.f_body, 6, t.ink_soft)
    pg.footer("Lista de desejos")


def p_rotina(pg):
    t = pg.t
    y = pg.header("Minha rotina ideal", "o dia que eu quero viver com mais frequência", "wb_sunny")
    cols = [("Manhã", "wb_sunny", ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00"]),
            ("Tarde", "wb_twilight", ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]),
            ("Noite", "bedtime", ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"])]
    gap = 3 * M
    gw = (pg.w - 2 * gap) / 3
    bh = y - pg.y0 - 46 * M
    for i, (name, ic, slots) in enumerate(cols):
        cx = pg.x0 + i * (gw + gap)
        xi, yi, wi, hi = pg.box(cx, y - bh, gw, bh, name, icon_name=ic)
        yy = yi - 6 * M
        step = (hi - 6 * M) / (len(slots) * 2)
        for s in slots:
            pg.text(xi, yy, s, t.f_body_sb, 6.4, t.ink_soft)
            pg.line(xi + 9 * M, yy - 0.8 * M, xi + wi, yy - 0.8 * M, t.line_soft, 0.5)
            yy -= step
            pg.line(xi + 9 * M, yy - 0.8 * M, xi + wi, yy - 0.8 * M, t.line_soft, 0.5, [0.6, 1.6])
            yy -= step
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, 42 * M, "Rituais de autocuidado que quero manter", icon_name="spa", fill=t.fill_soft)
    check_lines(pg, xi, yi - 4.5 * M, wi / 2 - 3 * M, 4, gap=7 * M)
    check_lines(pg, xi + wi / 2, yi - 4.5 * M, wi / 2, 4, gap=7 * M)
    pg.footer("Rotina ideal")


# ------------------------------------------------------------------ páginas mensais
def m_abertura(pg, year, m, hol):
    t, c = pg.t, pg.c
    pg.month_tab(m - 1)
    W, H = pg.W, pg.H
    name = MESES[m - 1]
    if t.deco == "botanical":
        corner_botanical(c, W - 12 * M, 10 * M, 52 * M, t, flip_x=True)
        pg.text(pg.x0, H - 52 * M, name, t.f_script, 52, t.accent)
        pg.text(pg.x0 + 1 * M, H - 62 * M, f"{m:02d} · {year}", t.f_title_i, 12, t.ink_soft)
        pg.line(pg.x0, H - 67 * M, pg.x0 + 50 * M, H - 67 * M, t.accent3, 0.8)
        pg.para(pg.x0, H - 78 * M, f"“{QUOTES[m - 1]}”", 78 * M, t.f_title_i, 10.5, 15, t.ink)
    else:
        pg.text(pg.x0 - 1 * M, H - 60 * M, f"{m:02d}", "Montserrat-ExtraBold", 92, t.fill_header)
        pg.text(pg.x0, H - 72 * M, name.upper(), t.f_title_b, 22, t.ink, tracking=3)
        pg.text(pg.x0, H - 79 * M, str(year), t.f_body, 9, t.ink_soft, tracking=2)
        pg.rect(pg.x0, H - 84 * M, 12 * M, 1 * M, fill=t.accent)
        pg.para(pg.x0, H - 93 * M, f"“{QUOTES[m - 1]}”", 80 * M, t.f_title, 10, 14.5, t.ink)
    mini_calendar(pg, pg.x0, H - 112 * M, 56 * M, year, m, hol, size=6.2, title_size=8)
    if t.deco == "minimal":
        xi, yi, wi, hi = pg.box(pg.x0 + 62 * M, H - 180 * M, pg.x1 - pg.x0 - 62 * M, 68 * M, "Destaques do mês", icon_name="star")
        check_lines(pg, xi, yi - 4.6 * M, wi, 8, gap=7 * M)
    yy = H - 150 * M
    xi, yi, wi, hi = pg.box(pg.x0, yy - 30 * M, (56 if t.deco == "minimal" else 72) * M, 30 * M, "Intenção do mês", icon_name="auto_awesome")
    pg.ruled(xi, yi - 5 * M, wi, 3, gap=7 * M)
    field(pg, pg.x0, yy - 42 * M, 72 * M, "Palavra do mês", lw=24 * M)
    pg.footer(name)


def m_plan1(pg, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Planejamento mensal", f"{MESES[m - 1]} · parte 1", "event_note")
    xi, yi, wi, hi = pg.box(pg.x0, y - 20 * M, pg.w, 20 * M, "Foco do mês", icon_name="center_focus_strong", fill=t.fill_soft)
    pg.ruled(xi, yi - 5 * M, wi, 2, gap=6.5 * M, color=t.line)
    top = y - 24 * M
    xi, yi, wi, hi = pg.box(pg.x0, top - 30 * M, pg.w, 30 * M, "Top 3 prioridades", icon_name="emoji_events")
    check_lines(pg, xi, yi - 4.6 * M, wi, 3, gap=7 * M, numbered=True)
    top -= 34 * M
    colw = (pg.w - 3.5 * M) / 2
    bh = top - pg.y0 - 36 * M
    xi, yi, wi, hi = pg.box(pg.x0, top - bh, colw, bh, "Datas importantes", icon_name="event")
    yy = yi - 5.2 * M
    for i in range(8):
        pg.rect(xi, yy - 1.2 * M, 7 * M, 4.6 * M, stroke=t.line, width=0.5, r=0.8 * M if t.deco == "botanical" else 0)
        pg.line(xi + 9 * M, yy - 0.8 * M, xi + wi, yy - 0.8 * M, t.line_soft, 0.5)
        yy -= 7.2 * M
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3.5 * M, top - bh, colw, bh, "Não posso esquecer", icon_name="push_pin")
    check_lines(pg, xi, yi - 5 * M, wi, 8, gap=7.2 * M)
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, 32 * M, "Metas do mês", icon_name="flag")
    check_lines(pg, xi, yi - 4.6 * M, wi / 2 - 3 * M, 3, gap=7 * M)
    check_lines(pg, xi + wi / 2, yi - 4.6 * M, wi / 2, 3, gap=7 * M)
    pg.footer(MESES[m - 1])


def m_plan2(pg, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Planejamento mensal", f"{MESES[m - 1]} · parte 2", "event_note")
    # check-in áreas da vida
    bh = 58 * M
    xi, yi, wi, hi = pg.box(pg.x0, y - bh, pg.w, bh, "Check-in das áreas da vida (1 a 10)", icon_name="donut_small")
    areas = ["Saúde", "Família", "Amor", "Amigos", "Carreira", "Finanças", "Lazer", "Espiritualidade", "Estudos", "Autocuidado"]
    colw = wi / 2
    for i, a in enumerate(areas):
        cx = xi + (i % 2) * colw
        cy = yi - 5 * M - (i // 2) * 9.4 * M
        pg.text(cx, cy - 0.5 * M, a, t.f_body_sb, 6.8, t.ink)
        circles_row(pg, cx + 24 * M, cy + 0.6 * M, 10, r=1.35 * M, gap=3.4 * M)
    top = y - bh - 4 * M
    colw2 = (pg.w - 3.5 * M) / 2
    h2 = 40 * M
    xi, yi, wi, hi = pg.box(pg.x0, top - h2, colw2, h2, "Hábitos que quero fortalecer", icon_name="eco")
    check_lines(pg, xi, yi - 4.6 * M, wi, 4, gap=7 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw2 + 3.5 * M, top - h2, colw2, h2, "Cuidados comigo", icon_name="spa")
    check_lines(pg, xi, yi - 4.6 * M, wi, 4, gap=7 * M)
    top -= h2 + 4 * M
    h3 = top - pg.y0
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, colw2, h3, "Como quero me sentir", icon_name="mood", fill=t.fill_soft)
    pg.ruled(xi, yi - 5 * M, wi, 3, gap=7.5 * M, color=t.line)
    xi, yi, wi, hi = pg.box(pg.x0 + colw2 + 3.5 * M, pg.y0, colw2, h3, "Wishlist do mês", icon_name="shopping_bag")
    yy = yi - 5 * M
    for i in range(3):
        pg.checkbox(xi, yy - 0.6 * M)
        pg.line(xi + 5 * M, yy - 0.8 * M, xi + wi - 16 * M, yy - 0.8 * M, t.line_soft, 0.5)
        pg.text(xi + wi - 15 * M, yy, "R$", t.f_body, 6.4, t.ink_soft)
        pg.line(xi + wi - 10 * M, yy - 0.8 * M, xi + wi, yy - 0.8 * M, t.line_soft, 0.5)
        yy -= 7.5 * M
    pg.footer(MESES[m - 1])


def _cal_cells(pg, year, m, hol, first_col, ncols, x, top, colw, rows_h, notes=False):
    t = pg.t
    grid = month_grid(year, m)
    com = datas_comemorativas(year)
    # cabeçalho dias
    for i in range(ncols):
        wd = first_col + i
        cx = x + i * colw
        pg.rect(cx, top - 6 * M, colw, 6 * M, fill=t.fill_header)
        pg.text(cx + colw / 2, top - 4.1 * M, DIAS[wd].upper() if t.deco == "minimal" else DIAS[wd],
                t.f_body_sb, 6.6, t.ink, align="center", tracking=0.5 if t.deco == "minimal" else 0)
    gy = top - 6 * M
    for r, row in enumerate(grid):
        cy = gy - (r + 1) * rows_h
        for i in range(ncols):
            wd = first_col + i
            d = row[wd]
            cx = x + i * colw
            weekend = wd >= 5
            fill = t.fill_soft if weekend else "#FFFFFF"
            pg.rect(cx, cy, colw, rows_h, fill=fill, stroke=t.line_soft, width=0.45)
            inmonth = d.month == m
            pg.text(cx + 1.6 * M, cy + rows_h - 4.2 * M, str(d.day), t.f_body_b if inmonth else t.f_body,
                    7.4 if inmonth else 6.4, t.ink if inmonth else t.line)
            if inmonth:
                info = hol.get(d)
                label = None
                if info and info[1] != "data":
                    label = info[0]
                elif d in com:
                    label = com[d]
                if label:
                    lines = pg.wrap(label, t.f_body, 4.9, colw - 3 * M)[:2]
                    yy = cy + rows_h - 7.6 * M
                    for ln in lines:
                        pg.text(cx + 1.6 * M, yy, ln, t.f_body, 4.9, t.accent if t.deco == "botanical" else t.ink_soft)
                        yy -= 2.6 * M
    if notes:
        cx = x + ncols * colw
        pg.rect(cx, top - 6 * M, colw, 6 * M, fill=t.fill_header)
        pg.text(cx + colw / 2, top - 4.1 * M, "NOTAS" if t.deco == "minimal" else "Notas", t.f_body_sb, 6.6, t.ink,
                align="center", tracking=0.5 if t.deco == "minimal" else 0)
        for r in range(6):
            cy = gy - (r + 1) * rows_h
            pg.rect(cx, cy, colw, rows_h, stroke=t.line_soft, width=0.45)
            yy = cy + rows_h - 6 * M
            while yy > cy + 2 * M:
                pg.line(cx + 1.5 * M, yy, cx + colw - 1.5 * M, yy, t.line_soft, 0.4, [0.6, 1.6])
                yy -= 5 * M


def m_cal_left(pg, year, m, hol):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header(MESES[m - 1], f"calendário · {year}", "calendar_month")
    colw = pg.w / 4
    rows_h = (y - pg.y0 - 6 * M) / 6
    _cal_cells(pg, year, m, hol, 0, 4, pg.x0, y, colw, rows_h)
    pg.footer(MESES[m - 1])


def m_cal_right(pg, year, m, hol):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Visão do mês", f"{MESES[m - 1]} · {year}", "calendar_month")
    colw = pg.w / 4
    rows_h = (y - pg.y0 - 6 * M) / 6
    _cal_cells(pg, year, m, hol, 4, 3, pg.x0, y, colw, rows_h, notes=True)
    pg.footer(MESES[m - 1])


def m_financas(pg, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Controle financeiro", f"{MESES[m - 1]}", "account_balance_wallet")
    colw = (pg.w - 3 * M) / 2
    xi, yi, wi, hi = pg.box(pg.x0, y - 12 * M, colw, 12 * M, fill=t.fill_soft)
    field(pg, xi, yi - 4 * M, wi, "Meta de economia  R$", lw=32 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3 * M, y - 12 * M, colw, 12 * M, fill=t.fill_soft)
    field(pg, xi, yi - 4 * M, wi, "Saldo inicial  R$", lw=26 * M)
    gap = 3 * M
    resumo_h = 11 * M
    top = y - 12 * M - gap
    avail = top - (pg.y0 + resumo_h + gap)
    rh = 5.9 * M
    # alturas: receitas (3 linhas), fixas (8), variáveis (restante)
    def box_h(nrows):
        return 6.2 * M + 5 * M + 1 * M + rh * (nrows + 1)
    h1 = box_h(3)
    h2 = box_h(8)
    h3 = avail - h1 - h2 - 2 * gap
    xi, yi, wi, hi = pg.box(pg.x0, top - h1, pg.w, h1, "Receitas", icon_name="trending_up")
    table(pg, xi, yi - 0.5 * M, wi, [("Descrição", 3, "left"), ("Data", 1, "left"), ("Valor", 1.2, "left")], 3, row_h=rh, head_size=6)
    top -= h1 + gap
    xi, yi, wi, hi = pg.box(pg.x0, top - h2, pg.w, h2, "Despesas fixas", icon_name="home")
    table(pg, xi, yi - 0.5 * M, wi, [("Descrição", 3, "left"), ("Venc.", 0.9, "left"), ("Valor", 1.2, "left"), ("Pago", 0.6, "center")], 8, row_h=rh, head_size=6)
    top -= h2 + gap
    xi, yi, wi, hi = pg.box(pg.x0, top - h3, pg.w, h3, "Despesas variáveis", icon_name="shopping_cart")
    table(pg, xi, yi - 0.5 * M, wi, [("Descrição", 3, "left"), ("Data", 0.9, "left"), ("Valor", 1.2, "left"), ("Categoria", 1.2, "left")], fit_rows(hi, rh), row_h=rh, head_size=6)
    # resumo
    yb = pg.y0
    pg.rect(pg.x0, yb, pg.w, resumo_h, fill=t.fill_header if t.deco == "botanical" else t.accent,
            r=2.2 * M if t.deco == "botanical" else 0)
    col = t.ink if t.deco == "botanical" else "#FFFFFF"
    lab = ["Receitas", "Despesas", "Economizei", "Saldo final"]
    cw = pg.w / 4
    for i, lb in enumerate(lab):
        pg.text(pg.x0 + i * cw + 2.5 * M, yb + 7 * M, lb, t.f_body_sb, 6.2, col)
        pg.text(pg.x0 + i * cw + 2.5 * M, yb + 2.6 * M, "R$", t.f_body, 6.2, col)
        pg.line(pg.x0 + i * cw + 7.5 * M, yb + 2.2 * M, pg.x0 + (i + 1) * cw - 3 * M, yb + 2.2 * M, col, 0.5)
    pg.footer(MESES[m - 1])


def m_habitos(pg, year, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Hábitos do mês", f"{MESES[m - 1]} · escreva até 8 hábitos e marque cada dia", "task_alt")
    ndays = (dt.date(year + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1) - dt.date(year, m, 1)).days
    head_h = 18 * M
    nh = 8
    day_w, wd_w = 7 * M, 5.5 * M
    hab_w = (pg.w - day_w - wd_w) / nh
    row_h = (y - head_h - pg.y0 - 6 * M) / 31
    # cabeçalho rotacionado (linhas para escrever)
    for i in range(nh):
        cx = pg.x0 + day_w + wd_w + i * hab_w
        pg.rect(cx, y - head_h, hab_w, head_h, fill=t.fill_header, stroke=t.line_soft, width=0.45)
        pg.line(cx + hab_w * 0.62, y - head_h + 2 * M, cx + hab_w * 0.62, y - 2 * M, t.line, 0.5)
    pg.text(pg.x0 + (day_w + wd_w) / 2, y - head_h + 2.4 * M, "dia", t.f_body_sb, 6, t.ink_soft, align="center")
    gy = y - head_h
    for d in range(31):
        cy = gy - (d + 1) * row_h
        date = dt.date(year, m, d + 1) if d < ndays else None
        weekend = date is not None and date.weekday() >= 5
        if d < ndays:
            pg.rect(pg.x0, cy, day_w + wd_w, row_h, fill=t.fill_soft if weekend else "#FFFFFF", stroke=t.line_soft, width=0.45)
            pg.text(pg.x0 + day_w - 1.2 * M, cy + row_h * 0.28, str(d + 1), t.f_body_sb, 6.2, t.ink, align="right")
            pg.text(pg.x0 + day_w + wd_w / 2, cy + row_h * 0.28, DIAS_1[date.weekday()], t.f_body, 5.6, t.ink_soft, align="center")
        for i in range(nh):
            cx = pg.x0 + day_w + wd_w + i * hab_w
            if d < ndays:
                pg.rect(cx, cy, hab_w, row_h, fill=t.fill_soft if weekend else "#FFFFFF", stroke=t.line_soft, width=0.45)
                if t.deco == "botanical":
                    pg.circle(cx + hab_w / 2, cy + row_h / 2, 1.25 * M, stroke=t.line, width=0.45)
                else:
                    pg.rect(cx + hab_w / 2 - 1.2 * M, cy + row_h / 2 - 1.2 * M, 2.4 * M, 2.4 * M, stroke=t.line, width=0.45)
            else:
                pg.rect(cx, cy, hab_w, row_h, fill=t.fill_soft, stroke=t.line_soft, width=0.45)
    # total
    cy = gy - 31 * row_h - 6 * M
    pg.text(pg.x0 + day_w + wd_w - 1.5 * M, cy + 1.8 * M, "total", t.f_body_sb, 6, t.ink_soft, align="right")
    for i in range(nh):
        cx = pg.x0 + day_w + wd_w + i * hab_w
        pg.rect(cx, cy, hab_w, 6 * M, stroke=t.line, width=0.5)
    pg.footer(MESES[m - 1])


def m_bemestar(pg, year, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Bem-estar do mês", f"{MESES[m - 1]} · água, sono, movimento e humor", "spa")
    ndays = (dt.date(year + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1) - dt.date(year, m, 1)).days
    last = "Ciclo" if t.deco == "botanical" else "Energia"
    cols = [("Dia", 7 * M, "day"), ("", 5 * M, "wd"), ("Água (copos)", 34 * M, "water"), ("Sono (h)", 13 * M, "line"),
            ("Exercício", 15 * M, "check"), ("Humor", 13 * M, "mood"), (last, 13 * M, "mood"), ("Notas", 0, "line")]
    fixed = sum(c[1] for c in cols)
    cols[-1] = ("Notas", pg.w - fixed, "line")
    head_h = 7 * M
    row_h = (y - head_h - pg.y0) / 31
    cx = pg.x0
    for label, w, kind in cols:
        pg.rect(cx, y - head_h, w, head_h, fill=t.fill_header, stroke=t.line_soft, width=0.45)
        if kind == "water":
            pg.icon(cx + 2 * M, y - head_h + 2.1 * M, "water_drop", size=7, color=t.accent if t.deco == "botanical" else t.ink)
            pg.text(cx + 6.5 * M, y - head_h + 2.3 * M, label, t.f_body_sb, 5.9, t.ink)
        elif label:
            pg.text(cx + w / 2, y - head_h + 2.3 * M, label, t.f_body_sb, 5.9, t.ink, align="center")
        cx += w
    gy = y - head_h
    for d in range(ndays):
        cy = gy - (d + 1) * row_h
        date = dt.date(year, m, d + 1)
        weekend = date.weekday() >= 5
        cx = pg.x0
        for label, w, kind in cols:
            pg.rect(cx, cy, w, row_h, fill=t.fill_soft if weekend else "#FFFFFF", stroke=t.line_soft, width=0.4)
            if kind == "day":
                pg.text(cx + w - 1.5 * M, cy + row_h * 0.28, str(d + 1), t.f_body_sb, 6, t.ink, align="right")
            elif kind == "wd":
                pg.text(cx + w / 2, cy + row_h * 0.28, DIAS_1[date.weekday()], t.f_body, 5.4, t.ink_soft, align="center")
            elif kind == "water":
                for k in range(8):
                    pg.circle(cx + 2.6 * M + k * 4.1 * M, cy + row_h / 2, 1.15 * M, stroke=t.line, width=0.4)
            elif kind == "check":
                pg.rect(cx + w / 2 - 1.3 * M, cy + row_h / 2 - 1.3 * M, 2.6 * M, 2.6 * M, stroke=t.line, width=0.45,
                        r=0.5 * M if t.deco == "botanical" else 0)
            elif kind == "mood":
                pg.circle(cx + w / 2, cy + row_h / 2, 1.5 * M, stroke=t.line, width=0.45)
            cx += w
    pg.footer(MESES[m - 1])


def m_lista(pg, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Lista do mês", f"{MESES[m - 1]} · tarefas, compras e ideias", "checklist")
    colw = (pg.w - 3.5 * M) / 2
    h1 = 104 * M
    xi, yi, wi, hi = pg.box(pg.x0, y - h1, colw, h1, "Tarefas", icon_name="task_alt")
    check_lines(pg, xi, yi - 4.6 * M, wi, 14, gap=6.6 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3.5 * M, y - h1, colw, h1, "Tarefas", icon_name="task_alt")
    check_lines(pg, xi, yi - 4.6 * M, wi, 14, gap=6.6 * M)
    top = y - h1 - 3.5 * M
    h2 = top - pg.y0
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, colw, h2, "Compras", icon_name="shopping_cart")
    check_lines(pg, xi, yi - 4.6 * M, wi, 7, gap=6.6 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3.5 * M, pg.y0, colw, h2, "Ideias e anotações", icon_name="lightbulb")
    pg.dotgrid(xi, yi - hi + 1 * M, wi, hi - 3 * M, step=4.5 * M)
    pg.footer(MESES[m - 1])


def m_revisao(pg, m):
    t = pg.t
    pg.month_tab(m - 1)
    y = pg.header("Revisão do mês", f"{MESES[m - 1]} · olhar para trás com carinho", "rate_review")
    colw = (pg.w - 3.5 * M) / 2
    h1 = 46 * M
    xi, yi, wi, hi = pg.box(pg.x0, y - h1, colw, h1, "O que deu certo", icon_name="thumb_up")
    pg.ruled(xi, yi - 5 * M, wi, 5, gap=7 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3.5 * M, y - h1, colw, h1, "O que posso melhorar", icon_name="trending_up")
    pg.ruled(xi, yi - 5 * M, wi, 5, gap=7 * M)
    top = y - h1 - 3.5 * M
    xi, yi, wi, hi = pg.box(pg.x0, top - h1, colw, h1, "Melhores momentos", icon_name="photo_camera")
    pg.ruled(xi, yi - 5 * M, wi, 5, gap=7 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3.5 * M, top - h1, colw, h1, "Sou grata por", icon_name="favorite")
    pg.ruled(xi, yi - 5 * M, wi, 5, gap=7 * M)
    top -= h1 + 3.5 * M
    h3 = 24 * M
    xi, yi, wi, hi = pg.box(pg.x0, top - h3, pg.w, h3, "Balanço", icon_name="insights", fill=t.fill_soft)
    pg.text(xi, yi - 4.5 * M, "Metas concluídas", t.f_body_sb, 6.8, t.ink)
    circles_row(pg, xi + 28 * M, yi - 3.4 * M, 10, r=1.6 * M, gap=4.4 * M)
    pg.text(xi, yi - 12.5 * M, "Nota do mês", t.f_body_sb, 6.8, t.ink)
    stars_row(pg, xi + 28 * M, yi - 13.3 * M, 5, size=9)
    pg.text(xi + wi * 0.62, yi - 4.5 * M, "Economizei  R$", t.f_body_sb, 6.8, t.ink)
    pg.line(xi + wi * 0.62 + 24 * M, yi - 5.3 * M, xi + wi, yi - 5.3 * M, t.line, 0.5)
    pg.text(xi + wi * 0.62, yi - 12.5 * M, "Li / aprendi", t.f_body_sb, 6.8, t.ink)
    pg.line(xi + wi * 0.62 + 20 * M, yi - 13.3 * M, xi + wi, yi - 13.3 * M, t.line, 0.5)
    top -= h3 + 3.5 * M
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, top - pg.y0, "Mensagem para o próximo mês", icon_name="mail")
    pg.ruled(xi, yi - 5 * M, wi, max(1, int((hi - 4 * M) // (7 * M))), gap=7 * M)
    pg.footer(MESES[m - 1])


# ------------------------------------------------------------------ semana
def _day_block(pg, x, y_top, w, h, date, hol, lines_gap=6.6 * M):
    t = pg.t
    info = hol.get(date)
    com = datas_comemorativas(date.year).get(date)
    hb = 7.2 * M
    r = 2 * M if t.deco == "botanical" else 0
    pg.rect(x, y_top - h, w, h, stroke=t.line, width=0.55, r=r)
    weekend = date.weekday() >= 5
    # faixa do cabeçalho do dia
    pg.c.saveState()
    p = pg.c.beginPath()
    p.roundRect(x, y_top - h, w, h, r)
    pg.c.clipPath(p, stroke=0, fill=0)
    pg.rect(x, y_top - hb, w, hb, fill=t.fill_header if not weekend or t.deco == "minimal" else "#F6E7E7")
    pg.c.restoreState()
    pg.line(x, y_top - hb, x + w, y_top - hb, t.line, 0.55)
    # número + nome
    pg.text(x + 2.5 * M, y_top - hb + 1.7 * M, f"{date.day:02d}", t.f_title_b, 12.5, t.ink)
    pg.text(x + 11.5 * M, y_top - hb + 2.3 * M, DIAS[date.weekday()] if t.deco == "botanical" else DIAS[date.weekday()].upper(),
            t.f_title_i if t.deco == "botanical" else t.f_body_sb, 8 if t.deco == "botanical" else 6.8, t.ink,
            tracking=0.8 if t.deco == "minimal" else 0)
    label = None
    if info and info[1] != "data":
        label = info[0] + (" · ponto facultativo" if info[1] == "facultativo" else "")
    elif com:
        label = com
    if label:
        pg.text(x + w - 2.2 * M, y_top - hb + 2.4 * M, label, t.f_body, 5.6,
                t.accent if t.deco == "botanical" else t.ink_soft, align="right")
    # linhas
    yy = y_top - hb - lines_gap
    while yy > y_top - h + 1.5 * M:
        pg.line(x + 2.5 * M, yy, x + w - 2.5 * M, yy, t.line_soft, 0.45)
        yy -= lines_gap


def w_left(pg, week, hol, month_idx):
    t = pg.t
    n, a, b = week
    pg.month_tab(month_idx)
    y = pg.header(f"Semana {n}", fmt_range(a, b), "date_range")
    # mini calendário do mês de referência no canto do cabeçalho (apenas tema minimal: fica no lado direito)
    gap = 2.5 * M
    bh = (y - pg.y0 - 3 * gap) / 4
    for i in range(4):
        d = a + dt.timedelta(days=i)
        _day_block(pg, pg.x0, y - i * (bh + gap), pg.w, bh, d, hol)
    pg.footer(f"Semana {n}")


def w_right(pg, week, hol, month_idx):
    t = pg.t
    n, a, b = week
    pg.month_tab(month_idx)
    y = pg.header(MESES[month_idx], f"semana {n} · {fmt_range(a, b)}", "date_range")
    gap = 2.5 * M
    total = y - pg.y0
    bottom_h = 75 * M
    avail = total - bottom_h - 3 * gap
    hf = avail * 0.40
    hs = avail * 0.30
    _day_block(pg, pg.x0, y, pg.w, hf, a + dt.timedelta(days=4), hol)
    _day_block(pg, pg.x0, y - hf - gap, pg.w, hs, a + dt.timedelta(days=5), hol)
    _day_block(pg, pg.x0, y - hf - hs - 2 * gap, pg.w, hs, a + dt.timedelta(days=6), hol)
    top = pg.y0 + bottom_h
    colw = (pg.w - 3 * M) / 2
    # coluna esquerda
    h1 = 27 * M
    xi, yi, wi, hi = pg.box(pg.x0, top - h1, colw, h1, "Essencial da semana", icon_name="star")
    check_lines(pg, xi, yi - 4.3 * M, wi, 3, gap=6.3 * M, numbered=True)
    h2 = bottom_h - h1 - 2.5 * M
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, colw, h2, "Pendências", icon_name="push_pin")
    check_lines(pg, xi, yi - 4.3 * M, wi, int((hi - 2 * M) // (6.3 * M)), gap=6.3 * M)
    # coluna direita
    xr = pg.x0 + colw + 3 * M
    h3 = 17 * M
    xi, yi, wi, hi = pg.box(xr, top - h3, colw, h3, "Foco", icon_name="center_focus_strong", fill=t.fill_soft)
    pg.ruled(xi, yi - 4.5 * M, wi, 2, gap=6 * M, color=t.line)
    h4 = 33 * M
    xi, yi, wi, hi = pg.box(xr, top - h3 - 2.5 * M - h4, colw, h4, "Bem-estar", icon_name="spa")
    tracks = [("água", "water_drop"), ("sono", "bedtime"), ("exercício", "fitness_center"), ("leitura", "menu_book")]
    yy = yi - 4.2 * M
    for lb, ic in tracks:
        pg.icon(xi, yy - 0.3 * M, ic, size=6.5, color=t.accent if t.deco == "botanical" else t.ink_soft)
        pg.text(xi + 4 * M, yy, lb, t.f_body, 6, t.ink)
        circles_row(pg, xi + 19 * M, yy + 0.9 * M, 7, r=1.25 * M, gap=4.4 * M)
        yy -= 5.6 * M
    xx = xi + 19 * M
    for i, dd in enumerate(DIAS_1):
        pg.text(xx + i * 4.4 * M + 1.25 * M, yy + 1.6 * M, dd, t.f_body, 4.8, t.ink_soft, align="center")
    h5 = bottom_h - h3 - h4 - 5 * M
    xi, yi, wi, hi = pg.box(xr, pg.y0, colw, h5, "Observações", icon_name="edit")
    pg.ruled(xi, yi - 4.5 * M, wi, max(1, int((hi - 2 * M) // (6 * M))), gap=6 * M)
    pg.footer(f"Semana {n}")


# ------------------------------------------------------------------ finais
def p_retrospectiva(pg, year):
    t = pg.t
    y = pg.header(f"Retrospectiva {year}", "fechamento do ano", "auto_awesome")
    colw = (pg.w - 3.5 * M) / 2
    h1 = 50 * M
    for i, (name, ic) in enumerate([("Minhas conquistas", "emoji_events"), ("Maiores aprendizados", "school"),
                                    ("Momentos inesquecíveis", "photo_camera"), ("Pessoas que fizeram diferença", "people")]):
        cx = pg.x0 + (i % 2) * (colw + 3.5 * M)
        cy = y - (i // 2) * (h1 + 3.5 * M) - h1
        xi, yi, wi, hi = pg.box(cx, cy, colw, h1, name, icon_name=ic)
        pg.ruled(xi, yi - 5 * M, wi, 5, gap=7.6 * M)
    top = y - 2 * h1 - 7 * M
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, top - pg.y0, "Balanço do ano", icon_name="insights", fill=t.fill_soft)
    pg.text(xi, yi - 5 * M, "Nota do ano", t.f_body_sb, 7, t.ink)
    stars_row(pg, xi + 24 * M, yi - 5.8 * M, 5, size=10)
    field(pg, xi, yi - 14 * M, wi, f"{year} em uma palavra", lw=30 * M)
    field(pg, xi, yi - 23 * M, wi, "Metas concluídas", lw=28 * M)
    field(pg, xi, yi - 32 * M, wi, "O que eu levo comigo", lw=32 * M)
    pg.footer(f"Retrospectiva {year}")


def p_proximo_ano(pg, year):
    t = pg.t
    y = pg.header(f"Planejando {year + 1}", "primeiras ideias para o próximo ano", "flag")
    colw = (pg.w - 3.5 * M) / 2
    h1 = 60 * M
    xi, yi, wi, hi = pg.box(pg.x0, y - h1, colw, h1, "O que quero manter", icon_name="favorite")
    pg.ruled(xi, yi - 5 * M, wi, 6, gap=7.6 * M)
    xi, yi, wi, hi = pg.box(pg.x0 + colw + 3.5 * M, y - h1, colw, h1, "O que quero mudar", icon_name="sync")
    pg.ruled(xi, yi - 5 * M, wi, 6, gap=7.6 * M)
    top = y - h1 - 3.5 * M
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0 + 20 * M, pg.w, top - pg.y0 - 20 * M, f"Metas para {year + 1}", icon_name="emoji_events")
    check_lines(pg, xi, yi - 5 * M, wi / 2 - 3 * M, int((hi - 3 * M) // (7.2 * M)), gap=7.2 * M)
    check_lines(pg, xi + wi / 2, yi - 5 * M, wi / 2, int((hi - 3 * M) // (7.2 * M)), gap=7.2 * M)
    xi, yi, wi, hi = pg.box(pg.x0, pg.y0, pg.w, 16 * M, fill=t.fill_soft)
    field(pg, xi, yi - 4.5 * M, wi, f"Minha palavra para {year + 1}", lw=38 * M)
    pg.footer(f"Planejando {year + 1}")


def p_contatos(pg):
    t = pg.t
    y = pg.header("Contatos", "pessoas e serviços importantes", "contacts")
    table(pg, pg.x0, y, pg.w, [("Nome", 1.6, "left"), ("Telefone", 1.1, "left"), ("E-mail / @", 1.5, "left")], 18, row_h=8.6 * M, zebra=True)
    pg.footer("Contatos")


def p_notas_pautada(pg):
    t = pg.t
    y = pg.header("Anotações", None, "edit", small=True)
    pg.ruled(pg.x0, y - 2 * M, pg.w, int((y - pg.y0) // (7 * M)), gap=7 * M)
    pg.footer("Anotações")


def p_notas_pontilhada(pg):
    t = pg.t
    y = pg.header("Anotações", None, "edit", small=True)
    pg.dotgrid(pg.x0, pg.y0, pg.w, y - pg.y0 - 2 * M, step=5 * M)
    pg.footer("Anotações")


def p_produzido_por(pg):
    t, c = pg.t, pg.c
    W, H = pg.W, pg.H
    if t.deco == "botanical":
        corner_botanical(c, W - 10 * M, H - 10 * M, 40 * M, t, flip_x=True, flip_y=True)
        corner_botanical(c, 10 * M, 10 * M, 40 * M, t)
    xi, yi, wi, hi = pg.box(pg.x0 + 8 * M, H / 2 - 32 * M, pg.w - 16 * M, 64 * M, fill="#FFFFFF")
    pg.text(W / 2, H / 2 + 20 * M, "Este planner foi produzido com carinho por", t.f_title_i if t.deco == "botanical" else t.f_body, 9, t.ink, align="center")
    pg.line(W / 2 - 36 * M, H / 2 + 9 * M, W / 2 + 36 * M, H / 2 + 9 * M, t.line, 0.6)
    pg.text(W / 2, H / 2 + 2 * M, "@", t.f_body_sb, 9, t.ink_soft, align="center")
    pg.line(W / 2 - 36 * M, H / 2 - 4 * M, W / 2 + 36 * M, H / 2 - 4 * M, t.line, 0.6)
    pg.text(W / 2, H / 2 - 12 * M, "Produção artesanal · feito à mão, página por página", t.f_body, 6.8, t.ink_soft, align="center")
    pg.text(W / 2, H / 2 - 22 * M, "Encomendas e personalizações:", t.f_body_sb, 6.8, t.ink, align="center")
    pg.line(W / 2 - 30 * M, H / 2 - 28 * M, W / 2 + 30 * M, H / 2 - 28 * M, t.line, 0.6)
