# -*- coding: utf-8 -*-
"""
Mockups programáticos (PIL): capas com wire-o e sombra, miolo aberto, catálogo das 30 capas e visão do kit.
Uso: python build_mockups.py
"""
import os, math
import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from common import OUT_DIR, FONT_DIR
from build_capas import CAPAS

CAPAS_PDF = os.path.join(OUT_DIR, "capas", "Capas-2027-30-modelos-A5-com-sangria.pdf")
MIOLO = {k: os.path.join(OUT_DIR, "miolo", f"Planner-2027-Miolo-A5-{k}.pdf") for k in ("Delicada", "Neutra")}
OUT = os.path.join(OUT_DIR, "mockups")
os.makedirs(OUT, exist_ok=True)
BLEED_FRAC = 3 / 154  # recorte da sangria


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def render(pdf, pno, dpi=110, trim_bleed=False):
    doc = pymupdf.open(pdf)
    pix = doc[pno].get_pixmap(dpi=dpi, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if trim_bleed:
        bx, by = int(im.width * BLEED_FRAC), int(im.height * 3 / 216)
        im = im.crop((bx, by, im.width - bx, im.height - by))
    return im


def background(w, h, c1=(246, 240, 234), c2=(226, 214, 204)):
    """Gradiente radial suave (centro claro, bordas mais escuras)."""
    rad = Image.radial_gradient("L").resize((int(w * 1.7), int(h * 1.7)), Image.BICUBIC)
    rad = rad.crop(((rad.width - w) // 2 - int(w * 0.08), (rad.height - h) // 2 - int(h * 0.1),
                    (rad.width - w) // 2 - int(w * 0.08) + w, (rad.height - h) // 2 - int(h * 0.1) + h))
    light = Image.new("RGB", (w, h), c1)
    dark = Image.new("RGB", (w, h), c2)
    return Image.composite(dark, light, rad)


def shadow(size, offset=(18, 28), blur=28, alpha=110):
    w, h = size
    pad = blur * 3
    sh = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + w, pad + h), radius=12, fill=(20, 15, 10, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    return sh, pad


def with_rings(cover, side="left", n=None, ring_color=(230, 230, 232), edge=(120, 120, 125)):
    """Adiciona anéis wire-o (duplo anel) e espessura de páginas atrás da capa."""
    w, h = cover.size
    margin_x = int(w * 0.06)
    canvas = Image.new("RGBA", (w + margin_x, h + int(h * 0.02)), (0, 0, 0, 0))
    # bloco de páginas (espessura) atrás
    for i, off in enumerate((10, 7, 4)):
        page = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        ImageDraw.Draw(page).rectangle((0, 0, w - 1, h - 1), outline=(215, 210, 205, 255))
        canvas.alpha_composite(page, (margin_x + off, off))
    cov = cover.convert("RGBA")
    # pequeno arredondamento de cantos externos
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.02), fill=255)
    cov.putalpha(mask)
    canvas.alpha_composite(cov, (margin_x, 0))
    # furos + anéis (wire-o visto de frente: pequenos laços horizontais)
    d = ImageDraw.Draw(canvas)
    n = n or 19
    step = h / (n + 1)
    hx = margin_x + int(w * 0.03)
    r_h = max(3, int(step * 0.2))
    lw = max(2, int(step * 0.11))
    for i in range(1, n + 1):
        cy = int(i * step)
        d.ellipse((hx - r_h, cy - r_h, hx + r_h, cy + r_h), fill=(40, 36, 34, 255))
        box = (hx - int(w * 0.07), cy - int(step * 0.30), hx + int(r_h * 0.6), cy + int(step * 0.30))
        d.ellipse(box, outline=(128, 128, 132, 255), width=lw)
        d.ellipse((box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1), outline=ring_color + (255,), width=max(1, lw // 2))
    return canvas


def perspective(img, tilt=0.06, rot=-5):
    """Leve rotação e distorção para dar sensação 3D."""
    w, h = img.size
    img = img.rotate(rot, resample=Image.BICUBIC, expand=True)
    w2, h2 = img.size
    dx = int(w2 * tilt)
    coeffs = find_coeffs([(0, 0), (w2, 0), (w2, h2), (0, h2)],
                         [(dx * 0.4, dx * 0.3), (w2 - dx * 0.2, 0), (w2, h2), (0, h2 - dx * 0.2)])
    return img.transform((w2, h2), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


def find_coeffs(pa, pb):
    """Coeficientes da transformação perspectiva (resolve sistema 8x8 por eliminação de Gauss, sem numpy)."""
    A, B = [], []
    for (x, y), (u, v) in zip(pa, pb):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    n = 8
    M = [row[:] + [b] for row, b in zip(A, B)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def paste_with_shadow(bg, obj, pos):
    sh, pad = shadow(obj.size)
    bg.alpha_composite(sh, (pos[0] - pad, pos[1] - pad))
    bg.alpha_composite(obj, pos)


def label(bg, text, pos, size=30, color=(70, 62, 58), fnt="Nunito-Regular.ttf", anchor="la"):
    ImageDraw.Draw(bg).text(pos, text, font=font(fnt, size), fill=color, anchor=anchor)


# ------------------------------------------------------------------ mockups
def mockup_capa(idx, out, bgcols=((246, 240, 234), (226, 214, 204))):
    W, H = 1600, 1200
    bg = background(W, H, *bgcols).convert("RGBA")
    cov = render(CAPAS_PDF, (idx - 1) * 2, dpi=120, trim_bleed=True)
    cov = cov.resize((int(cov.width * 0.95), int(cov.height * 0.95)))
    obj = with_rings(cov)
    obj = perspective(obj, tilt=0.04, rot=-4)
    paste_with_shadow(bg, obj, ((W - obj.width) // 2 + 40, (H - obj.height) // 2 + 10))
    name = CAPAS[idx - 1][0]
    label(bg, f"Capa {idx:02d} · {name}", (60, H - 70), 26, (110, 100, 94))
    label(bg, "Planner 2027 · A5 · wire-o", (W - 60, H - 70), 26, (110, 100, 94), anchor="ra")
    bg.convert("RGB").save(out, quality=86, optimize=True)
    print("ok", out)


def mockup_spread(theme, p_left, p_right, out, title):
    W, H = 1800, 1200
    bg = background(W, H, (240, 238, 234), (214, 210, 203)).convert("RGBA")
    L = render(MIOLO[theme], p_left - 1, dpi=120)
    R = render(MIOLO[theme], p_right - 1, dpi=120)
    scale = 0.92
    L = L.resize((int(L.width * scale), int(L.height * scale)))
    R = R.resize((int(R.width * scale), int(R.height * scale)))
    gap = 26
    spread = Image.new("RGBA", (L.width + R.width + gap, L.height + 8), (0, 0, 0, 0))
    # páginas de trás (espessura)
    for off in (8, 5):
        for x in (0, L.width + gap):
            pg = Image.new("RGBA", (L.width, L.height), (255, 255, 255, 255))
            ImageDraw.Draw(pg).rectangle((0, 0, L.width - 1, L.height - 1), outline=(215, 210, 205, 255))
            spread.alpha_composite(pg, (x + (off if x else -off), off))
    spread.alpha_composite(L.convert("RGBA"), (0, 0))
    spread.alpha_composite(R.convert("RGBA"), (L.width + gap, 0))
    # anéis no centro
    d = ImageDraw.Draw(spread)
    n = 19
    step = L.height / (n + 1)
    cx = L.width + gap // 2
    r_h = max(3, int(step * 0.2)); lw = max(2, int(step * 0.11))
    for i in range(1, n + 1):
        cy = int(i * step)
        for hx in (cx - gap // 2 - int(L.width * 0.03), cx + gap // 2 + int(L.width * 0.03)):
            d.ellipse((hx - r_h, cy - r_h, hx + r_h, cy + r_h), fill=(40, 36, 34, 255))
        box = (cx - gap // 2 - int(L.width * 0.03) - r_h, cy - int(step * 0.30), cx + gap // 2 + int(L.width * 0.03) + r_h, cy + int(step * 0.30))
        d.ellipse(box, outline=(128, 128, 132, 255), width=lw)
        d.ellipse((box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1), outline=(232, 232, 234, 255), width=max(1, lw // 2))
    spread = spread.rotate(-3, resample=Image.BICUBIC, expand=True)
    paste_with_shadow(bg, spread, ((W - spread.width) // 2, (H - spread.height) // 2 + 10))
    label(bg, title, (60, H - 70), 26, (110, 100, 94))
    label(bg, "Planner 2027 · miolo A5 · 254 páginas", (W - 60, H - 70), 26, (110, 100, 94), anchor="ra")
    bg.convert("RGB").save(out, quality=86, optimize=True)
    print("ok", out)


def catalogo(out):
    cols, rows = 6, 5
    tw = 230
    th = int(tw * 210 / 148)
    pad, top = 26, 150
    W = cols * (tw + pad) + pad
    H = top + rows * (th + pad + 34) + pad
    bg = Image.new("RGB", (W, H), (247, 244, 240))
    d = ImageDraw.Draw(bg)
    d.text((W // 2, 60), "30 capas prontas · Planner 2027", font=font("PlayfairDisplay-Bold.ttf", 46), fill=(60, 54, 50), anchor="mm")
    d.text((W // 2, 110), "15 delicadas + 15 neutras · A5 com sangria · PDF vetorial + PNG 300 dpi", font=font("Nunito-Regular.ttf", 22), fill=(120, 110, 104), anchor="mm")
    for i in range(30):
        c, r = i % cols, i // cols
        x = pad + c * (tw + pad); y = top + r * (th + pad + 34)
        im = render(CAPAS_PDF, i * 2, dpi=60, trim_bleed=True).resize((tw, th), Image.LANCZOS)
        sh, p = shadow((tw, th), offset=(6, 8), blur=10, alpha=80)
        bg.paste(sh, (x - p + 4, y - p + 6), sh)
        bg.paste(im, (x, y))
        d.rectangle((x, y, x + tw - 1, y + th - 1), outline=(220, 214, 208))
        d.text((x + tw // 2, y + th + 18), f"{i + 1:02d} · {CAPAS[i][0]}", font=font("Nunito-Regular.ttf", 17), fill=(90, 82, 78), anchor="mm")
    bg.save(out, quality=86, optimize=True)
    print("ok", out)


def kit_overview(out):
    W, H = 1800, 1200
    bg = background(W, H, (244, 238, 232), (222, 208, 200)).convert("RGBA")
    # 3 capas em leque (direita)
    for idx, rot, x, y in ((16, 8, 1250, 130), (2, 4, 1190, 105), (1, -2, 1120, 80)):
        cov = render(CAPAS_PDF, (idx - 1) * 2, dpi=88, trim_bleed=True)
        cov = with_rings(cov).rotate(rot, resample=Image.BICUBIC, expand=True)
        paste_with_shadow(bg, cov, (x, y))
    # miolo aberto (esquerda, em cima)
    L = render(MIOLO["Delicada"], 29, dpi=64); R = render(MIOLO["Delicada"], 30, dpi=64)
    spread = Image.new("RGBA", (L.width * 2 + 10, L.height), (0, 0, 0, 0))
    spread.alpha_composite(L.convert("RGBA"), (0, 0)); spread.alpha_composite(R.convert("RGBA"), (L.width + 10, 0))
    spread = spread.rotate(-4, resample=Image.BICUBIC, expand=True)
    paste_with_shadow(bg, spread, (90, 50))
    # adesivos e divisória (esquerda, embaixo)
    st = render(os.path.join(OUT_DIR, "extras", "Adesivos-2027-2-folhas-A4-Delicada.pdf"), 0, dpi=34).convert("RGBA")
    st = st.rotate(4, resample=Image.BICUBIC, expand=True)
    paste_with_shadow(bg, st, (150, 680))
    dv = render(os.path.join(OUT_DIR, "extras", "Divisorias-2027-12-meses-A5-Delicada.pdf"), 0, dpi=46).convert("RGBA")
    dv = dv.rotate(-6, resample=Image.BICUBIC, expand=True)
    paste_with_shadow(bg, dv, (560, 680))
    gd = render(os.path.join(OUT_DIR, "extras", "Guardas-2027-8-padroes-A5.pdf"), 0, dpi=46).convert("RGBA")
    gd = gd.rotate(5, resample=Image.BICUBIC, expand=True)
    paste_with_shadow(bg, gd, (860, 700))
    # textos
    d = ImageDraw.Draw(bg)
    d.rectangle((0, 1085, W, H), fill=(255, 255, 255, 170))
    d.text((W // 2, 1122), "Kit Planner 2027 · arquivos digitais prontos para imprimir e encadernar",
           font=font("PlayfairDisplay-Bold.ttf", 38), fill=(60, 54, 50), anchor="mm")
    d.text((W // 2, 1168), "2 miolos A5 (254 pág.) · 30 capas · divisórias · guardas · adesivos · mockups · guia da encadernadora",
           font=font("Nunito-Regular.ttf", 23), fill=(110, 100, 94), anchor="mm")
    bg.convert("RGB").save(out, quality=86, optimize=True)
    print("ok", out)


if __name__ == "__main__":
    mockup_capa(1, os.path.join(OUT, "mockup-capa-01-jardim-sage.jpg"))
    mockup_capa(11, os.path.join(OUT, "mockup-capa-11-ceu-estrelado.jpg"), ((236, 236, 240), (204, 204, 214)))
    mockup_capa(16, os.path.join(OUT, "mockup-capa-16-preto-essencial.jpg"), ((238, 236, 232), (210, 206, 200)))
    mockup_capa(23, os.path.join(OUT, "mockup-capa-23-terracota.jpg"), ((244, 236, 228), (222, 206, 192)))
    mockup_spread("Delicada", 30, 31, os.path.join(OUT, "mockup-miolo-delicada-semana.jpg"), "Miolo Delicada · planejamento semanal")
    mockup_spread("Delicada", 24, 25, os.path.join(OUT, "mockup-miolo-delicada-mensal.jpg"), "Miolo Delicada · calendário mensal")
    mockup_spread("Neutra", 26, 27, os.path.join(OUT, "mockup-miolo-neutra-financas-habitos.jpg"), "Miolo Neutra · finanças e hábitos")
    mockup_spread("Neutra", 30, 31, os.path.join(OUT, "mockup-miolo-neutra-semana.jpg"), "Miolo Neutra · planejamento semanal")
    catalogo(os.path.join(OUT, "catalogo-30-capas.jpg"))
    kit_overview(os.path.join(OUT, "kit-completo-visao-geral.jpg"))
