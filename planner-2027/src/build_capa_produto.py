# -*- coding: utf-8 -*-
"""
Capa do produto (imagem de vitrine para Kiwify/Hotmart/Kavoo, anúncios e redes) em 4 formatos,
salvas SEM metadados (sem EXIF, ICC, XMP ou chunks de texto).
Uso: python build_capa_produto.py
"""
import os, io
import pymupdf
from PIL import Image, ImageDraw, ImageFilter
from reportlab.pdfgen import canvas
from common import register_fonts, corner_botanical, flower, sprig, DELICADA, OUT_DIR
from build_mockups import render, with_rings, shadow, font, CAPAS_PDF, MIOLO

register_fonts()
NOME = "Ateliê"
NOME2 = "Planner 2027"
SUB = "Kit completo pronto para imprimir, encadernar e vender"
BADGES = ["2 miolos A5 · 254 páginas datadas", "30 capas + contracapas (PDF e PNG)",
          "divisórias, guardas e 300+ adesivos", "bônus: Guia da Encadernadora"]
RODAPE = "licença comercial · acesso imediato · garantia de 7 dias"
INK, ACC, SOFT, SAGE = (74, 68, 66), (169, 110, 114), (138, 128, 124), (159, 176, 154)
OUT = os.path.join(OUT_DIR, "..", "vendas", "capa-produto")
os.makedirs(OUT, exist_ok=True)


def gradient_bg(w, h, c1=(252, 247, 244), c2=(236, 218, 214)):
    rad = Image.radial_gradient("L").resize((int(w * 1.8), int(h * 1.8)), Image.BICUBIC)
    x0 = (rad.width - w) // 2 - int(w * 0.15); y0 = (rad.height - h) // 2 - int(h * 0.15)
    rad = rad.crop((x0, y0, x0 + w, y0 + h))
    return Image.composite(Image.new("RGB", (w, h), c2), Image.new("RGB", (w, h), c1), rad).convert("RGBA")


def botanical_overlay(w, h, size):
    """Raminhos e flores vetoriais (reportlab) rasterizados com transparência."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    corner_botanical(c, w, h, size, DELICADA, flip_x=True, flip_y=True)
    corner_botanical(c, 0, 0, size * 0.85, DELICADA, flip_x=False, flip_y=False)
    c.save(); buf.seek(0)
    doc = pymupdf.open(stream=buf.read(), filetype="pdf")
    pix = doc[0].get_pixmap(dpi=72, alpha=True)
    return Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)


def obj_cover(idx, height, rot):
    cov = render(CAPAS_PDF, (idx - 1) * 2, dpi=150, trim_bleed=True)
    cov = cov.resize((int(cov.width * height / cov.height), height), Image.LANCZOS)
    obj = with_rings(cov)
    sh, pad = shadow(obj.size, blur=22, alpha=95)
    out = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 0)); out.alpha_composite(obj, (pad - 14, pad - 20))
    return out.rotate(rot, resample=Image.BICUBIC, expand=True)


def obj_spread(width, rot):
    L = render(MIOLO["Delicada"], 29, dpi=100); R = render(MIOLO["Delicada"], 30, dpi=100)
    sp = Image.new("RGBA", (L.width * 2 + 10, L.height), (0, 0, 0, 0))
    sp.alpha_composite(L.convert("RGBA"), (0, 0)); sp.alpha_composite(R.convert("RGBA"), (L.width + 10, 0))
    sp = sp.resize((width, int(sp.height * width / sp.width)), Image.LANCZOS)
    sh, pad = shadow(sp.size, blur=18, alpha=90)
    out = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 0)); out.alpha_composite(sp, (pad - 10, pad - 14))
    return out.rotate(rot, resample=Image.BICUBIC, expand=True)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines


def title_block(im, x, y, col_w, scale=1.0, center=False):
    d = ImageDraw.Draw(im)
    f_script = font("GreatVibes-Regular.ttf", int(118 * scale))
    f_title = font("PlayfairDisplay-Bold.ttf", int(84 * scale))
    f_sub = font("Nunito-Regular.ttf", int(30 * scale))
    f_badge = font("Nunito-Bold.ttf", int(24 * scale))
    f_foot = font("Nunito-Regular.ttf", int(21 * scale))
    anchor = "ma" if center else "la"
    cx = x + col_w // 2 if center else x
    d.text((cx, y), NOME, font=f_script, fill=ACC, anchor=anchor)
    y += int(118 * scale)
    d.text((cx, y), NOME2, font=f_title, fill=INK, anchor=anchor)
    y += int(112 * scale)
    # linha + flor
    lx = cx - int(28 * scale) if center else x
    d.rectangle((lx, y, lx + int(56 * scale), y + int(3 * scale)), fill=ACC)
    y += int(22 * scale)
    for ln in wrap(d, SUB, f_sub, col_w):
        d.text((cx, y), ln, font=f_sub, fill=SOFT, anchor=anchor); y += int(40 * scale)
    y += int(16 * scale)
    bh = int(46 * scale); gap = int(12 * scale)
    for b in BADGES:
        tw = d.textlength(b, font=f_badge); bw = int(tw + 60 * scale)
        bx = cx - bw // 2 if center else x
        d.rounded_rectangle((bx, y, bx + bw, y + bh), radius=bh // 2, fill=(255, 255, 255, 225), outline=ACC + (255,), width=max(1, int(2 * scale)))
        d.ellipse((bx + int(16 * scale), y + bh // 2 - int(6 * scale), bx + int(28 * scale), y + bh // 2 + int(6 * scale)), fill=SAGE)
        d.text((bx + int(40 * scale), y + bh // 2), b, font=f_badge, fill=INK, anchor="lm")
        y += bh + gap
    y += int(10 * scale)
    d.text((cx, y), RODAPE, font=f_foot, fill=SOFT, anchor=anchor)
    return y


def compose(w, h, layout):
    im = gradient_bg(w, h)
    deco = botanical_overlay(w, h, int(min(w, h) * 0.26))
    deco.putalpha(deco.getchannel("A").point(lambda a: int(a * 0.75)))
    im.alpha_composite(deco)
    if layout == "square":      # 1080x1080
        c16 = obj_cover(16, 470, 7); c01 = obj_cover(1, 530, -4); sp = obj_spread(370, -6)
        im.alpha_composite(c16, (610, 80)); im.alpha_composite(c01, (515, 150)); im.alpha_composite(sp, (560, 730))
        title_block(im, 64, 70, 470)
    elif layout == "vertical":  # 1080x1350
        title_block(im, 90, 80, 900, scale=1.0, center=True)
        c16 = obj_cover(16, 440, 7); c01 = obj_cover(1, 480, -4); sp = obj_spread(480, -5)
        im.alpha_composite(c16, (560, 650)); im.alpha_composite(c01, (430, 690)); im.alpha_composite(sp, (30, 860))
    elif layout == "wide":      # 1200x628
        c16 = obj_cover(16, 330, 7); c01 = obj_cover(1, 370, -4); sp = obj_spread(300, -6)
        im.alpha_composite(c16, (820, 20)); im.alpha_composite(c01, (720, 60)); im.alpha_composite(sp, (560, 355))
        title_block(im, 56, 30, 520, scale=0.82)
    elif layout == "banner":    # 1920x1080
        c16 = obj_cover(16, 600, 7); c01 = obj_cover(1, 660, -4); sp = obj_spread(540, -6)
        im.alpha_composite(c16, (1340, 60)); im.alpha_composite(c01, (1170, 120)); im.alpha_composite(sp, (960, 640))
        title_block(im, 120, 110, 760, scale=1.25)
    return im.convert("RGB")


def save_clean(im, path):
    """Grava sem nenhum metadado: recria a imagem a partir dos pixels e salva sem EXIF/ICC/XMP/texto."""
    clean = Image.frombytes(im.mode, im.size, im.tobytes())
    if path.lower().endswith(".png"):
        clean.save(path, "PNG", optimize=True)
    else:
        clean.save(path, "JPEG", quality=92, optimize=True, progressive=True, subsampling=0)
    # verificação
    chk = Image.open(path)
    meta = {k: v for k, v in chk.info.items() if k not in ("jfif", "jfif_version", "jfif_unit", "jfif_density", "dpi", "progressive", "progression")}
    assert not chk.getexif() and not meta, f"metadados encontrados em {path}: {meta}"
    print(f"ok {path} ({chk.width}x{chk.height}, sem metadados)")


if __name__ == "__main__":
    slug = "atelie-planner-2027"
    save_clean(compose(1080, 1080, "square"), os.path.join(OUT, f"capa-{slug}-1080x1080.jpg"))
    save_clean(compose(1080, 1080, "square"), os.path.join(OUT, f"capa-{slug}-1080x1080.png"))
    save_clean(compose(1080, 1350, "vertical"), os.path.join(OUT, f"capa-{slug}-1080x1350.jpg"))
    save_clean(compose(1200, 628, "wide"), os.path.join(OUT, f"capa-{slug}-1200x628.jpg"))
    save_clean(compose(1920, 1080, "banner"), os.path.join(OUT, f"capa-{slug}-1920x1080.jpg"))
