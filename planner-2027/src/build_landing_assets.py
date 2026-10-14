# -*- coding: utf-8 -*-
"""
Gera as imagens usadas pela landing page (vendas/landing/img/):
  - páginas do miolo (Delicada e Neutra) renderizadas individualmente e em spreads
  - extras (divisórias, guardas, adesivos), guia, capas em destaque
  - cópias dos mockups e da imagem Open Graph
Todas as imagens saem sem metadados (EXIF/ICC/XMP).
"""
import os, shutil
import pymupdf
from PIL import Image, ImageDraw

from common import OUT_DIR
from build_mockups import render, CAPAS_PDF, MIOLO

LANDING = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "vendas", "landing"))
IMG = os.path.join(LANDING, "img")
os.makedirs(IMG, exist_ok=True)

EXTRAS = os.path.join(OUT_DIR, "extras")
GUIA = os.path.join(OUT_DIR, "bonus", "Guia-da-Encadernadora-Planner-2027.pdf")
CAPA_PRODUTO = os.path.normpath(os.path.join(LANDING, "..", "capa-produto"))


def save(im, name, q=84):
    """Salva JPEG limpo (sem metadados)."""
    if im.mode != "RGB":
        im = im.convert("RGB")
    path = os.path.join(IMG, name)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
    b = open(path, "rb").read()
    for m in (b"Exif", b"http://ns.adobe.com/xap", b"ICC_PROFILE"):
        assert m not in b, (name, m)
    print(f"ok {name} ({im.width}x{im.height}, {os.path.getsize(path)//1024} KB)")


def page(pdf, pno, width, trim=False):
    """Página renderizada em RGB com `width` px de largura (pno 1-based)."""
    im = render(pdf, pno - 1, dpi=200, trim_bleed=trim)
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)


def framed(im, border=(226, 218, 212)):
    """Fio fino ao redor da página (simula a folha)."""
    out = Image.new("RGB", (im.width + 2, im.height + 2), border)
    out.paste(im, (1, 1))
    return out


def spread(pdf, left, right, width=1400):
    """Duas páginas lado a lado com vinco central suave."""
    half = width // 2
    a, b = page(pdf, left, half), page(pdf, right, half)
    out = Image.new("RGB", (width, a.height), (255, 255, 255))
    out.paste(a, (0, 0)); out.paste(b, (half, 0))
    d = ImageDraw.Draw(out, "RGBA")
    for i in range(14):  # sombra do vinco
        alpha = int(38 * (1 - i / 14))
        d.line((half - i, 0, half - i, out.height), fill=(60, 40, 35, alpha))
        d.line((half + i, 0, half + i, out.height), fill=(60, 40, 35, alpha))
    return framed(out)


def main():
    D, N = MIOLO["Delicada"], MIOLO["Neutra"]

    # --- galeria "por dentro, página a página" (Delicada) ---
    singles = [
        (1, "pg-d-01-abertura", "Abertura"),
        (2, "pg-d-02-dados-pessoais", "Dados pessoais"),
        (3, "pg-d-03-calendario-2027", "Calendário 2027"),
        (5, "pg-d-05-feriados", "Feriados 2027"),
        (7, "pg-d-07-metas", "Metas 2027"),
        (8, "pg-d-08-ano-em-cores", "Meu ano em cores"),
        (11, "pg-d-11-visao-financeira", "Visão financeira do ano"),
        (12, "pg-d-12-metas-financeiras", "Metas financeiras"),
        (21, "pg-d-21-abertura-mes", "Abertura do mês"),
        (22, "pg-d-22-planejamento-mensal", "Planejamento mensal"),
        (26, "pg-d-26-controle-financeiro", "Controle financeiro"),
        (27, "pg-d-27-habitos", "Hábitos do mês"),
        (28, "pg-d-28-bem-estar", "Bem-estar"),
        (29, "pg-d-29-lista-do-mes", "Lista do mês"),
        (40, "pg-d-40-revisao", "Revisão do mês"),
        (250, "pg-d-250-anotacoes", "Anotações"),
        (254, "pg-d-254-colofao", "Página da artesã"),
    ]
    for pno, name, _ in singles:
        save(framed(page(D, pno, 760)), f"{name}.jpg")

    save(spread(D, 24, 25), "sp-d-calendario-mensal.jpg")
    save(spread(D, 30, 31), "sp-d-semana.jpg")
    save(spread(N, 24, 25), "sp-n-calendario-mensal.jpg")
    save(spread(N, 30, 31), "sp-n-semana.jpg")
    save(spread(N, 26, 27), "sp-n-financas-habitos.jpg")
    save(framed(page(N, 21, 760)), "pg-n-21-abertura-mes.jpg")
    save(framed(page(N, 7, 760)), "pg-n-07-metas.jpg")

    # --- extras ---
    save(framed(page(os.path.join(EXTRAS, "Divisorias-2027-12-meses-A5-Delicada.pdf"), 1, 760)), "ex-divisoria-delicada.jpg")
    save(framed(page(os.path.join(EXTRAS, "Divisorias-2027-12-meses-A5-Neutra.pdf"), 1, 760)), "ex-divisoria-neutra.jpg")
    save(framed(page(os.path.join(EXTRAS, "Guardas-2027-8-padroes-A5.pdf"), 1, 760)), "ex-guarda-1.jpg")
    save(framed(page(os.path.join(EXTRAS, "Guardas-2027-8-padroes-A5.pdf"), 3, 760)), "ex-guarda-3.jpg")
    save(framed(page(os.path.join(EXTRAS, "Adesivos-2027-2-folhas-A4-Delicada.pdf"), 1, 900)), "ex-adesivos-delicada.jpg")
    save(framed(page(os.path.join(EXTRAS, "Adesivos-2027-2-folhas-A4-Neutra.pdf"), 1, 900)), "ex-adesivos-neutra.jpg")

    # --- guia ---
    g = pymupdf.open(GUIA)
    for pno in (1, 4, 6):
        if pno <= g.page_count:
            save(framed(page(GUIA, pno, 760)), f"guia-p{pno}.jpg")

    # --- capas em destaque (sem sangria) ---
    for n in (1, 7, 11, 16, 23, 28):
        save(page(CAPAS_PDF, 2 * n - 1, 600, trim=True), f"capa-{n:02d}.jpg", q=86)

    # --- cópias ---
    for f in ("mockup-capa-11-ceu-estrelado.jpg", "mockup-capa-23-terracota.jpg", "mockup-miolo-neutra-semana.jpg"):
        shutil.copy(os.path.join(OUT_DIR, "mockups", f), os.path.join(IMG, f))
    shutil.copy(os.path.join(CAPA_PRODUTO, "capa-atelie-planner-2027-1200x628.jpg"), os.path.join(IMG, "og-1200x628.jpg"))
    shutil.copy(os.path.join(CAPA_PRODUTO, "capa-atelie-planner-2027-1080x1080.jpg"), os.path.join(IMG, "capa-produto-1080.jpg"))
    print("copiados mockups + OG")


if __name__ == "__main__":
    main()
