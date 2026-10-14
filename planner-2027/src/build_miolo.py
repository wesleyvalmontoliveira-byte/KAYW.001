# -*- coding: utf-8 -*-
"""
Gera o miolo do Planner 2027 (A5, datado, seg-dom) em PDF vetorial.
Uso: python build_miolo.py [delicada|neutra|all] [--ano 2027]
"""
import os, sys, argparse
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from common import (register_fonts, THEMES, Page, A5_W, A5_H, feriados, weeks_by_month, OUT_DIR, MESES)
import pages as P


def build(theme_key, year=2027, out=None):
    register_fonts()
    t = THEMES[theme_key]
    out = out or os.path.join(OUT_DIR, "miolo", f"Planner-2027-Miolo-A5-{t.name}.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    c = canvas.Canvas(out, pagesize=(A5_W, A5_H))
    c.setTitle(f"Planner {year} — Miolo A5 — versão {t.name}")
    c.setAuthor("Kit Planner 2027 · arquivo digital para encadernação")
    c.setSubject("Planner datado 2027, semana de segunda a domingo, A5")
    hol = feriados(year)
    wbm = weeks_by_month(year)
    state = {"n": 0}

    def page(fn, *args, **kw):
        state["n"] += 1
        pg = Page(c, t, state["n"])
        fn(pg, *args, **kw)
        c.showPage()
        return state["n"]

    def need_parity(odd):
        """Garante que a PRÓXIMA página seja ímpar (recto) ou par (verso), inserindo anotações."""
        while ((state["n"] + 1) % 2 == 1) != odd:
            page(P.p_notas_pontilhada)

    # ---- abertura (20 páginas)
    page(P.p_title, year)                 # 1 recto
    page(P.p_dados)                       # 2
    page(P.p_calendario, year, hol)       # 3
    page(P.p_calendario, year + 1, feriados(year + 1), "para já programar o ano seguinte")  # 4
    page(P.p_feriados, year)              # 5
    page(P.p_datas_importantes)           # 6
    page(P.p_metas, year)                 # 7
    page(P.p_ano_em_cores, year)          # 8
    page(P.p_saude)                       # 9
    page(P.p_exames)                      # 10
    page(P.p_fin_ano, year)               # 11
    page(P.p_metas_fin)                   # 12
    page(P.p_acessos)                     # 13
    page(P.p_leituras)                    # 14
    page(P.p_favoritos)                   # 15
    page(P.p_lugares_quero)               # 16
    page(P.p_lugares_visitados)           # 17
    page(P.p_projetos)                    # 18
    page(P.p_desejos)                     # 19
    page(P.p_rotina)                      # 20

    # ---- meses
    for m in range(1, 13):
        need_parity(odd=True)
        page(P.m_abertura, year, m, hol)      # recto
        page(P.m_plan1, m)                    # verso
        page(P.m_plan2, m)                    # recto
        page(P.m_cal_left, year, m, hol)      # verso
        page(P.m_cal_right, year, m, hol)     # recto
        page(P.m_financas, m)                 # verso
        page(P.m_habitos, year, m)            # recto
        page(P.m_bemestar, year, m)           # verso
        page(P.m_lista, m)                    # recto
        for wk in wbm[m]:
            need_parity(odd=False)
            page(P.w_left, wk, hol, m - 1)    # verso
            page(P.w_right, wk, hol, m - 1)   # recto
        page(P.m_revisao, m)                  # verso

    # ---- fechamento
    need_parity(odd=True)
    page(P.p_retrospectiva, year)
    page(P.p_proximo_ano, year)
    page(P.p_contatos)
    page(P.p_notas_pautada)
    page(P.p_notas_pautada)
    page(P.p_notas_pontilhada)
    page(P.p_notas_pontilhada)
    need_parity(odd=False)
    page(P.p_produzido_por)
    c.save()
    print(f"ok {out} — {state['n']} páginas")
    return out, state["n"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("theme", nargs="?", default="all")
    ap.add_argument("--ano", type=int, default=2027)
    a = ap.parse_args()
    keys = list(THEMES) if a.theme == "all" else [a.theme]
    for k in keys:
        build(k, a.ano)
