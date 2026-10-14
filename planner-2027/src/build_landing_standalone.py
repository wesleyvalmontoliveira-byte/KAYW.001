# -*- coding: utf-8 -*-
"""
Gera uma versão da landing em UM ÚNICO arquivo HTML (CSS, JS, fontes e imagens embutidos),
para abrir offline em qualquer computador/celular sem servidor:
    vendas/landing/atelie-planner-2027-landing-completa.html
Termos e privacidade entram como janelas (dialog) dentro do mesmo arquivo.
"""
import os, re, base64, io, mimetypes
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
LANDING = os.path.normpath(os.path.join(HERE, "..", "vendas", "landing"))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(LANDING, "atelie-planner-2027-landing-completa.html")

UNICODES = "U+0020-007E,U+00A0-00FF,U+0100-017F,U+2013-2014,U+2018-201D,U+2022,U+2026,U+2033,U+00D7,U+2039-203A"
FONT_FACES = [  # (arquivo, family, weight, style)
    ("PlayfairDisplay-Regular.ttf", "Playfair Display", 400, "normal"),
    ("PlayfairDisplay-Bold.ttf", "Playfair Display", 700, "normal"),
    ("PlayfairDisplay-Italic.ttf", "Playfair Display", 400, "italic"),
    ("Nunito-Regular.ttf", "Nunito", 400, "normal"),
    ("Nunito-SemiBold.ttf", "Nunito", 600, "normal"),
    ("Nunito-Bold.ttf", "Nunito", 700, "normal"),
    ("Nunito-ExtraBold.ttf", "Nunito", 800, "normal"),
    ("GreatVibes-Regular.ttf", "Great Vibes", 400, "normal"),
]


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def font_face_css():
    css = []
    total = 0
    for fname, family, weight, style in FONT_FACES:
        font = TTFont(os.path.join(FONTS, fname))
        opts = subset.Options(flavor="woff2", hinting=False, desubroutinize=True, layout_features=["kern", "liga", "calt"])
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=subset.parse_unicodes(UNICODES))
        sub.subset(font)
        font.flavor = "woff2"
        buf = io.BytesIO(); font.save(buf); data = buf.getvalue(); total += len(data)
        css.append(f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};font-display:swap;"
                   f"src:url(data:font/woff2;base64,{base64.b64encode(data).decode()}) format('woff2')}}")
    print(f"fontes embutidas: {len(FONT_FACES)} ({total//1024} KB)")
    return "\n".join(css)


def inline_images(html):
    cache = {}
    def rep(m):
        attr, path = m.group(1), m.group(2)
        full = os.path.join(LANDING, path)
        if not os.path.exists(full):
            return m.group(0)
        if path not in cache:
            cache[path] = data_uri(full)
        return f'{attr}="{cache[path]}"'
    html = re.sub(r'(src|href)="(img/[^"]+)"', rep, html)
    html = re.sub(r'"(img/[^"]+)"', lambda m: '"' + cache.get(m.group(1), m.group(1)) + '"', html)  # JSON-LD / og
    print(f"imagens embutidas: {len(cache)}")
    return html


def doc_dialog(page, did, title):
    src = read(os.path.join(LANDING, page))
    body = re.search(r'<main class="page-simple">(.*?)</main>', src, re.S).group(1)
    body = re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S)
    return (f'<dialog class="doc" id="{did}"><div class="doc-box"><button class="lb-close doc-close" data-close="{did}" aria-label="Fechar">✕</button>'
            f'<h2>{title}</h2>{body}</div></dialog>')


def main():
    html = read(os.path.join(LANDING, "index.html"))
    css = read(os.path.join(LANDING, "assets", "style.css"))
    cfg = read(os.path.join(LANDING, "assets", "config.js"))
    app = read(os.path.join(LANDING, "assets", "app.js"))

    extra_css = """
dialog.doc{border:0;border-radius:22px;padding:0;max-width:min(94vw,820px);width:100%;background:#fff}
dialog.doc::backdrop{background:rgba(40,32,31,.7)}
.doc-box{position:relative;padding:40px 36px 36px;max-height:84vh;overflow:auto}
.doc-box h2{margin-top:0;font-size:1.7rem}
.doc-box h2+p{color:var(--ink-2)}
.doc-box ul,.doc-box p{color:var(--ink-2)}
.doc-close{top:12px;right:12px}
@media (max-width:600px){.doc-box{padding:30px 20px}}
"""
    # fontes locais no lugar do Google Fonts
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)
    html = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>\s*', "", html)
    html = html.replace('<link rel="stylesheet" href="assets/style.css">',
                        "<style>\n" + font_face_css() + "\n" + css + extra_css + "\n</style>")
    html = html.replace('<script src="assets/config.js"></script>', "<script>\n" + cfg + "\n</script>")
    html = html.replace('<script src="assets/app.js"></script>', "<script>\n" + app + "\n</script>")

    # termos e privacidade como janelas internas
    html = html.replace('<a href="termos.html">', '<a href="#termos" data-open="termos">')
    html = html.replace('<a href="privacidade.html">', '<a href="#privacidade" data-open="privacidade">')
    dialogs = doc_dialog("termos.html", "termos", "Termos de uso e licença") + doc_dialog("privacidade.html", "privacidade", "Política de privacidade")
    opener = """<script>
document.querySelectorAll("[data-open]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var d=document.getElementById(a.getAttribute("data-open"));if(d&&d.showModal){d.showModal();}});});
document.querySelectorAll("[data-close]").forEach(function(b){b.addEventListener("click",function(){document.getElementById(b.getAttribute("data-close")).close();});});
document.querySelectorAll("dialog.doc").forEach(function(d){d.addEventListener("click",function(e){if(e.target===d)d.close();});});
</script>"""
    html = html.replace("</body>", dialogs + "\n" + opener + "\n</body>")

    html = inline_images(html)
    html = html.replace("<title>", "<!-- Versão em arquivo único (offline). Para publicar, use a pasta landing/ completa. -->\n<title>", 1)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"ok {OUT} ({os.path.getsize(OUT)/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
