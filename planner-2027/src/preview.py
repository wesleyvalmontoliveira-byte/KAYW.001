# -*- coding: utf-8 -*-
"""Renderiza páginas de um PDF para PNG (conferência visual / imagens de divulgação).
Uso: python preview.py arquivo.pdf 1,2,3 saida.png [--dpi 80] [--spread]
--spread: junta as páginas lado a lado (pares à esquerda, ímpares à direita)."""
import sys, argparse
import pymupdf
from PIL import Image


def render(pdf, pages, out, dpi=80, spread=False, cols=None):
    doc = pymupdf.open(pdf)
    imgs = []
    for p in pages:
        pix = doc[p - 1].get_pixmap(dpi=dpi)
        imgs.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    if spread or cols:
        n = len(imgs)
        cols = cols or n
        rows = (n + cols - 1) // cols
        w, h = imgs[0].size
        gap = 6
        sheet = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * h + (rows + 1) * gap), (120, 120, 120))
        for i, im in enumerate(imgs):
            r, c_ = divmod(i, cols)
            sheet.paste(im, (gap + c_ * (w + gap), gap + r * (h + gap)))
        sheet.save(out)
    else:
        imgs[0].save(out)
    print("ok", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("pages"); ap.add_argument("out")
    ap.add_argument("--dpi", type=int, default=80); ap.add_argument("--spread", action="store_true")
    ap.add_argument("--cols", type=int, default=None)
    a = ap.parse_args()
    render(a.pdf, [int(x) for x in a.pages.split(",")], a.out, a.dpi, a.spread, a.cols)
