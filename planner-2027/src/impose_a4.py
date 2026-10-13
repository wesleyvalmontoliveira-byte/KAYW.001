# -*- coding: utf-8 -*-
"""
Imposição "2 páginas por folha" (A4 paisagem, corte ao meio e empilhe) a partir do miolo A5.
Gera duas variantes de frente-e-verso: virar na borda CURTA (como livro) e na borda LONGA (como calendário).
Uso: python impose_a4.py produto/miolo/Planner-2027-Miolo-A5-Delicada.pdf [...]
"""
import os, sys
import pymupdf

MM = 72 / 25.4
A4W, A4H = 297 * MM, 210 * MM
A5W, A5H = 148 * MM, 210 * MM


def impose(src, out, flip="curta"):
    sd = pymupdf.open(src)
    n = sd.page_count
    pad = (-n) % 4
    total = n + pad
    half = total // 2
    sheets = total // 4
    od = pymupdf.open()

    def place(page, idx, x):
        if idx <= n:
            page.show_pdf_page(pymupdf.Rect(x, 0, x + A5W, A5H), sd, idx - 1)

    def sheet(left, right):
        page = od.new_page(width=A4W, height=A4H)
        place(page, left, 0.25 * MM)
        place(page, right, A4W / 2 + 0.25 * MM)
        # marcas de corte no centro
        x = A4W / 2
        sh = page.new_shape()
        sh.draw_line((x, 0), (x, 4 * MM))
        sh.draw_line((x, A4H - 4 * MM), (x, A4H))
        sh.finish(color=(0.55, 0.55, 0.55), width=0.3)
        sh.draw_line((x, 6 * MM), (x, A4H - 6 * MM))
        sh.finish(color=(0.80, 0.80, 0.80), width=0.3, dashes="[1 3] 0")
        sh.commit()

    for i in range(sheets):
        f_l, f_r = 2 * i + 1, half + 2 * i + 1
        sheet(f_l, f_r)
        if flip == "curta":   # virar como livro: o verso da metade esquerda cai na direita
            sheet(half + 2 * i + 2, 2 * i + 2)
        else:                 # virar como calendário: metade esquerda continua à esquerda
            sheet(2 * i + 2, half + 2 * i + 2)
    od.set_metadata({"title": os.path.basename(out).replace(".pdf", ""),
                     "subject": f"Imprimir em A4 paisagem, frente e verso, virar na borda {flip.upper()}. "
                                f"Depois corte as folhas ao meio e coloque a pilha da esquerda sobre a da direita.",
                     "author": "Kit Planner 2027 · arquivo digital para encadernação"})
    od.save(out, garbage=4, deflate=True)
    print(f"ok {out} — {sheets} folhas A4 ({total} páginas A5, {pad} em branco no final)")


if __name__ == "__main__":
    for src in sys.argv[1:]:
        base = os.path.basename(src).replace("Miolo-A5", "Miolo-A4-2pp").replace(".pdf", "")
        d = os.path.normpath(os.path.join(os.path.dirname(src), "..", "miolo-a4-2pp"))
        os.makedirs(d, exist_ok=True)
        impose(src, os.path.join(d, base + "-virar-borda-CURTA.pdf"), "curta")
        impose(src, os.path.join(d, base + "-virar-borda-LONGA.pdf"), "longa")
