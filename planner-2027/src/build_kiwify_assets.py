# -*- coding: utf-8 -*-
"""
Assets para publicar na Kiwify: pacotes ZIP do entregável (por módulo da área de membros),
capa vertical da área de membros, banner e capas dos módulos — tudo sem metadados.
Uso: python build_kiwify_assets.py
"""
import os, io, zipfile, textwrap
import pymupdf
from PIL import Image, ImageDraw
from common import register_fonts, OUT_DIR
from build_mockups import render, font, shadow, with_rings, CAPAS_PDF, MIOLO
from build_capa_produto import gradient_bg, botanical_overlay, save_clean, INK, ACC, SOFT, SAGE

register_fonts()
ROOT = os.path.normpath(os.path.join(OUT_DIR, ".."))
KW = os.path.join(ROOT, "vendas", "kiwify")
IMG = os.path.join(KW, "imagens"); ZIPS = os.path.join(KW, "entregaveis")
for d in (IMG, ZIPS):
    os.makedirs(d, exist_ok=True)

LICENCA = """ATELIÊ PLANNER 2027 — LICENÇA DE USO
=====================================
VOCÊ PODE: imprimir e vender planners, agendas e cadernos FÍSICOS feitos com estes arquivos,
em quantidade ilimitada, com a sua marca; personalizar as capas (nome, logo, frases);
usar os mockups na sua divulgação.

VOCÊ NÃO PODE: vender, doar, compartilhar ou publicar os arquivos digitais (PDF/PNG), inteiros
ou em partes; vender o miolo como produto digital; alegar autoria dos designs.

Fontes: Google Fonts (SIL Open Font License) · Ícones: Material Icons (Apache 2.0).
Suporte: responda o e-mail de entrega ou chame no WhatsApp informado na área de membros.
"""

MODULOS = [
    # (num, título, subtítulo, pasta(s) do produto, nome do zip, imagem de referência)
    ("01", "Comece por aqui", "licença, estrutura dos arquivos e como imprimir", None, None, "kit"),
    ("02", "Miolos A5 e A4", "Delicada e Neutra · 254 páginas · 2 pág./folha", ["miolo", "miolo-a4-2pp"], "02-Miolos-A5-e-A4-2pp.zip", "spread"),
    ("03", "30 Capas", "PDF com sangria, A4 com marcas e PNG 300 dpi", ["capas"], "03-Capas-30-modelos-PDF-e-PNG.zip", "cover"),
    ("04", "Divisórias, guardas e adesivos", "24 divisórias · 8 guardas · 300+ adesivos", ["extras"], "04-Divisorias-Guardas-Adesivos.zip", "stickers"),
    ("05", "Mockups e divulgação", "10 imagens prontas + catálogo das capas", ["mockups"], "05-Mockups-e-Divulgacao.zip", "mock"),
    ("06", "Bônus: Guia da Encadernadora", "impressão, wire-o, custos, preço e vendas", ["bonus"], "06-Bonus-Guia-da-Encadernadora.zip", "guide"),
]


def make_zips():
    for num, titulo, sub, pastas, zname, _ in MODULOS:
        if not pastas:
            continue
        path = os.path.join(ZIPS, zname)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            z.writestr("LEIA-ME.txt", f"ATELIÊ PLANNER 2027 — Módulo {num}: {titulo}\n{sub}\n\n" + LICENCA)
            for pasta in pastas:
                base = os.path.join(OUT_DIR, pasta)
                for root, _, files in os.walk(base):
                    for f in sorted(files):
                        full = os.path.join(root, f)
                        z.write(full, os.path.join(pasta, os.path.relpath(full, base)))
        print(f"ok {path} ({os.path.getsize(path)/1e6:.1f} MB)")
    # pacote único (opcional)
    path = os.path.join(ZIPS, "00-Atelie-Planner-2027-COMPLETO.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("LEIA-ME.txt", "ATELIÊ PLANNER 2027 — pacote completo\n\n" + LICENCA)
        for root, _, files in os.walk(OUT_DIR):
            for f in sorted(files):
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, OUT_DIR))
    print(f"ok {path} ({os.path.getsize(path)/1e6:.1f} MB)")
    with open(os.path.join(ZIPS, "LICENCA-DE-USO.txt"), "w") as fh:
        fh.write(LICENCA)


def thumb(kind, h):
    """Miniatura RGBA (com sombra) do conteúdo de cada módulo."""
    if kind == "cover":
        cov = render(CAPAS_PDF, 0, dpi=120, trim_bleed=True)
        obj = with_rings(cov.resize((int(cov.width * h / cov.height), h), Image.LANCZOS))
    elif kind == "spread":
        L = render(MIOLO["Delicada"], 29, dpi=90); R = render(MIOLO["Delicada"], 30, dpi=90)
        obj = Image.new("RGBA", (L.width * 2 + 8, L.height), (0, 0, 0, 0))
        obj.alpha_composite(L.convert("RGBA"), (0, 0)); obj.alpha_composite(R.convert("RGBA"), (L.width + 8, 0))
        obj = obj.resize((int(obj.width * h / obj.height), h), Image.LANCZOS)
    elif kind == "stickers":
        obj = render(os.path.join(OUT_DIR, "extras", "Adesivos-2027-2-folhas-A4-Delicada.pdf"), 0, dpi=80).convert("RGBA")
        obj = obj.resize((int(obj.width * h / obj.height), h), Image.LANCZOS)
    elif kind == "guide":
        obj = render(os.path.join(OUT_DIR, "bonus", "Guia-da-Encadernadora-Planner-2027.pdf"), 0, dpi=80).convert("RGBA")
        obj = obj.resize((int(obj.width * h / obj.height), h), Image.LANCZOS)
    elif kind == "mock":
        obj = Image.open(os.path.join(OUT_DIR, "mockups", "mockup-capa-23-terracota.jpg")).convert("RGBA")
        obj = obj.resize((int(obj.width * h / obj.height), h), Image.LANCZOS)
    else:  # kit
        obj = Image.open(os.path.join(OUT_DIR, "mockups", "kit-completo-visao-geral.jpg")).convert("RGBA")
        obj = obj.resize((int(obj.width * h / obj.height), h), Image.LANCZOS)
    sh, pad = shadow(obj.size, blur=16, alpha=90)
    out = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 0)); out.alpha_composite(obj, (pad - 8, pad - 12))
    return out


def card_modulo(num, titulo, sub, kind, w=600, h=900):
    im = gradient_bg(w, h)
    deco = botanical_overlay(w, h, int(w * 0.34))
    deco.putalpha(deco.getchannel("A").point(lambda a: int(a * 0.7)))
    im.alpha_composite(deco)
    d = ImageDraw.Draw(im)
    d.text((40, 36), "ATELIÊ PLANNER 2027", font=font("Nunito-Bold.ttf", 20), fill=SOFT)
    d.text((40, 70), num, font=font("PlayfairDisplay-Bold.ttf", 120), fill=ACC)
    y = 215
    f_t = font("PlayfairDisplay-Bold.ttf", 44)
    lines, cur = [], ""
    for wd in titulo.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f_t) <= w - 80:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    for ln in lines:
        d.text((40, y), ln, font=f_t, fill=INK); y += 52
    d.rectangle((40, y + 8, 96, y + 11), fill=ACC); y += 26
    for ln in textwrap.wrap(sub, 38):
        d.text((40, y), ln, font=font("Nunito-Regular.ttf", 22), fill=SOFT); y += 30
    th = thumb(kind, 420 if kind in ("cover", "guide", "stickers") else 300)
    th = th.rotate(-5, resample=Image.BICUBIC, expand=True)
    x = (w - th.width) // 2 + 20
    im.alpha_composite(th, (x, h - th.height + 40))
    return im.convert("RGB")


def capa_area(w=1200, h=1800):
    im = gradient_bg(w, h)
    deco = botanical_overlay(w, h, int(w * 0.3))
    im.alpha_composite(deco)
    d = ImageDraw.Draw(im)
    d.text((w // 2, 170), "Ateliê", font=font("GreatVibes-Regular.ttf", 190), fill=ACC, anchor="ms")
    d.text((w // 2, 310), "Planner 2027", font=font("PlayfairDisplay-Bold.ttf", 118), fill=INK, anchor="ms")
    d.rectangle((w // 2 - 36, 340, w // 2 + 36, 345), fill=ACC)
    d.text((w // 2, 400), "kit completo pronto para imprimir,", font=font("Nunito-Regular.ttf", 36), fill=SOFT, anchor="ms")
    d.text((w // 2, 448), "encadernar e vender", font=font("Nunito-Regular.ttf", 36), fill=SOFT, anchor="ms")
    c01 = thumb("cover", 800)
    cov16 = render(CAPAS_PDF, 30, dpi=120, trim_bleed=True)
    cov16 = with_rings(cov16.resize((int(cov16.width * 740 / cov16.height), 740), Image.LANCZOS))
    sh, pad = shadow(cov16.size, blur=16, alpha=90)
    o16 = Image.new("RGBA", sh.size, (0, 0, 0, 0)); o16.alpha_composite(sh, (0, 0)); o16.alpha_composite(cov16, (pad - 8, pad - 12))
    im.alpha_composite(o16.rotate(7, resample=Image.BICUBIC, expand=True), (540, 540))
    im.alpha_composite(c01.rotate(-4, resample=Image.BICUBIC, expand=True), (130, 600))
    f_b = font("Nunito-Bold.ttf", 28)
    y = 1660
    for b in ("2 miolos A5 · 30 capas · divisórias · adesivos", "mockups · Guia da Encadernadora · licença comercial"):
        d.text((w // 2, y), b, font=f_b, fill=INK, anchor="ms"); y += 44
    return im.convert("RGB")


def banner(w=1920, h=640):
    im = gradient_bg(w, h)
    deco = botanical_overlay(w, h, int(h * 0.55))
    im.alpha_composite(deco)
    d = ImageDraw.Draw(im)
    d.text((120, 200), "Ateliê", font=font("GreatVibes-Regular.ttf", 150), fill=ACC, anchor="ls")
    d.text((120, 320), "Planner 2027", font=font("PlayfairDisplay-Bold.ttf", 100), fill=INK, anchor="ls")
    d.text((124, 380), "Bem-vinda à sua área de membros! Baixe os arquivos por módulo", font=font("Nunito-Regular.ttf", 30), fill=SOFT, anchor="ls")
    d.text((124, 420), "e comece pelo Guia da Encadernadora.", font=font("Nunito-Regular.ttf", 30), fill=SOFT, anchor="ls")
    d.text((124, 472), "licença comercial · suporte por e-mail e WhatsApp", font=font("Nunito-Bold.ttf", 26), fill=SAGE, anchor="ls")
    kit = Image.open(os.path.join(OUT_DIR, "mockups", "kit-completo-visao-geral.jpg")).convert("RGBA")
    kit = kit.resize((int(kit.width * 470 / kit.height), 470), Image.LANCZOS)
    sh, pad = shadow(kit.size, blur=16, alpha=90)
    o = Image.new("RGBA", sh.size, (0, 0, 0, 0)); o.alpha_composite(sh, (0, 0)); o.alpha_composite(kit, (pad - 8, pad - 12))
    o = o.rotate(-3, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(o, (w - o.width + 30, (h - o.height) // 2 + 10))
    return im.convert("RGB")


if __name__ == "__main__":
    make_zips()
    save_clean(capa_area(), os.path.join(IMG, "capa-area-de-membros-1200x1800.jpg"))
    save_clean(banner(), os.path.join(IMG, "banner-area-de-membros-1920x640.jpg"))
    for num, titulo, sub, _, _, kind in MODULOS:
        slug = ["comece-por-aqui", "miolos-a5-e-a4", "30-capas", "divisorias-guardas-e-adesivos", "mockups-e-divulgacao", "bonus-guia"][int(num) - 1]
        save_clean(card_modulo(num, titulo, sub, kind), os.path.join(IMG, f"modulo-{num}-{slug}-600x900.jpg"))
