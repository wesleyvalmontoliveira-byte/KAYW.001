# -*- coding: utf-8 -*-
"""
Bônus: Guia da Encadernadora (A4, PDF) — como imprimir, montar, precificar e vender o Planner 2027.
Uso: python build_guia.py
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether,
                ListFlowable, ListItem)
from common import register_fonts, C, sprig, flower, corner_botanical, OUT_DIR, DELICADA

register_fonts()
T = DELICADA
W, H = A4
OUT = os.path.join(OUT_DIR, "bonus", "Guia-da-Encadernadora-Planner-2027.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

INK, SOFT, ACC, SAGE, GOLD, FILL = T.ink, T.ink_soft, T.accent, T.accent2, T.accent3, T.fill_header

st = {
  "h1": ParagraphStyle("h1", fontName="PlayfairDisplay-Regular", fontSize=22, leading=27, textColor=C(INK), spaceAfter=3 * mm),
  "sub": ParagraphStyle("sub", fontName="Nunito-Regular", fontSize=9.5, leading=13, textColor=C(SOFT), spaceAfter=6 * mm),
  "h2": ParagraphStyle("h2", fontName="PlayfairDisplay-Regular", fontSize=13.5, leading=17, textColor=C(ACC), spaceBefore=5 * mm, spaceAfter=2 * mm),
  "p": ParagraphStyle("p", fontName="Nunito-Regular", fontSize=9.6, leading=14, textColor=C(INK), spaceAfter=2.2 * mm),
  "small": ParagraphStyle("small", fontName="Nunito-Regular", fontSize=8, leading=11, textColor=C(SOFT)),
  "b": ParagraphStyle("b", fontName="Nunito-Bold", fontSize=9.6, leading=14, textColor=C(INK)),
  "li": ParagraphStyle("li", fontName="Nunito-Regular", fontSize=9.6, leading=13.5, textColor=C(INK)),
  "call": ParagraphStyle("call", fontName="Nunito-Regular", fontSize=9.4, leading=13.5, textColor=C(INK)),
  "th": ParagraphStyle("th", fontName="Nunito-Bold", fontSize=8.2, leading=10.5, textColor=C(INK)),
  "td": ParagraphStyle("td", fontName="Nunito-Regular", fontSize=8.4, leading=11, textColor=C(INK)),
  "center": ParagraphStyle("center", fontName="Nunito-Regular", fontSize=10, leading=14, textColor=C(INK), alignment=TA_CENTER),
}


def P(txt, s="p"):
  return Paragraph(txt, st[s])


def bullets(items, s="li"):
  return ListFlowable([ListItem(Paragraph(i, st[s]), leftIndent=5 * mm, value="•") for i in items],
            bulletType="bullet", start="•", bulletFontName="Nunito-Bold", bulletFontSize=9,
            bulletColor=C(ACC), leftIndent=6 * mm, spaceAfter=2.5 * mm)


def numbered(items, s="li"):
  return ListFlowable([ListItem(Paragraph(i, st[s]), leftIndent=6 * mm) for i in items], bulletType="1",
            bulletFontName="Nunito-Bold", bulletFontSize=9, bulletColor=C(ACC), leftIndent=7 * mm,
            spaceAfter=2.5 * mm)


def table(data, widths, header=True, zebra=True, align_right_cols=()):
  rows = [[Paragraph(str(c), st["th" if (header and i == 0) else "td"]) for c in r] for i, r in enumerate(data)]
  t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
  style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.2 * mm),
       ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm), ("LEFTPADDING", (0, 0), (-1, -1), 2.5 * mm),
       ("LINEBELOW", (0, 0), (-1, -1), 0.3, C(T.line)), ("BOX", (0, 0), (-1, -1), 0.5, C(T.line))]
  if header:
    style += [("BACKGROUND", (0, 0), (-1, 0), C(FILL))]
  if zebra:
    for i in range(1, len(rows)):
      if i % 2 == 0:
        style.append(("BACKGROUND", (0, i), (-1, i), C(T.fill_soft)))
  t.setStyle(TableStyle(style))
  t.spaceAfter = 4 * mm
  return t


def callout(txt, title="Dica"):
  inner = Table([[Paragraph(f"<b>{title}</b> — {txt}", st["call"])]], colWidths=[W - 2 * 20 * mm - 6 * mm])
  inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C(T.fill_soft)), ("BOX", (0, 0), (-1, -1), 0.6, C(ACC)),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm)]))
  inner.spaceBefore = 2 * mm; inner.spaceAfter = 4 * mm
  return inner


def check_list(items):
  from common import icon
  rows = [[Paragraph(icon("check_box_outline_blank"), ParagraphStyle("ck", fontName="MaterialIcons-Regular", fontSize=11, textColor=C(ACC))), Paragraph(i, st["li"])] for i in items]
  t = Table(rows, colWidths=[8 * mm, W - 40 * mm - 8 * mm])
  t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6 * mm),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6 * mm), ("LINEBELOW", (0, 0), (-1, -1), 0.3, C(T.line_soft))]))
  t.spaceAfter = 4 * mm
  return t


# ------------------------------------------------------------------ decoração das páginas
def on_cover(c, doc):
  c.saveState()
  c.setFillColor(C("#FBF6F4")); c.rect(0, 0, W, H, stroke=0, fill=1)
  corner_botanical(c, 0, H, 70 * mm, T, flip_x=False, flip_y=True)
  corner_botanical(c, W, 0, 70 * mm, T, flip_x=True, flip_y=False)
  c.setFillColor(C("#FFFFFF")); c.roundRect(30 * mm, 95 * mm, W - 60 * mm, 110 * mm, 5 * mm, stroke=0, fill=1)
  c.setFont("GreatVibes-Regular", 34); c.setFillColor(C(ACC)); c.drawCentredString(W / 2, 178 * mm, "Bônus exclusivo")
  c.setFont("PlayfairDisplay-Regular", 30); c.setFillColor(C(INK)); c.drawCentredString(W / 2, 160 * mm, "Guia da Encadernadora")
  c.setFont("Nunito-Regular", 11.5); c.setFillColor(C(SOFT))
  c.drawCentredString(W / 2, 148 * mm, "Como imprimir, montar, precificar e vender o seu Planner 2027")
  c.setStrokeColor(C(ACC)); c.setLineWidth(0.7); c.line(W / 2 - 20 * mm, 140 * mm, W / 2 + 20 * mm, 140 * mm)
  flower(c, W / 2, 140 * mm, 2.4 * mm, "#E7B9BB", "#D9B88A")
  c.setFont("Nunito-Regular", 9.5); c.setFillColor(C(INK))
  for i, s in enumerate(["impressão do miolo e das capas · wire-o e acabamentos",
              "planilha de custos e preço de venda · fotos, legendas e scripts",
              "calendário de vendas · checklist de produção · licença de uso"]):
    c.drawCentredString(W / 2, 128 * mm - i * 6 * mm, s)
  c.setFont("Nunito-Regular", 8); c.setFillColor(C(SOFT)); c.drawCentredString(W / 2, 104 * mm, "Kit Planner 2027 · arquivos digitais para encadernação artesanal")
  c.restoreState()


def on_page(c, doc):
  c.saveState()
  c.setStrokeColor(C(T.line)); c.setLineWidth(0.4); c.line(20 * mm, H - 16 * mm, W - 20 * mm, H - 16 * mm)
  sprig(c, W - 20 * mm, H - 14.5 * mm, 16 * mm, 180, SAGE, leaves=6, stem_w=0.5)
  c.setFont("Nunito-Regular", 7.5); c.setFillColor(C(SOFT))
  c.drawString(20 * mm, H - 14 * mm, "GUIA DA ENCADERNADORA · PLANNER 2027")
  c.line(20 * mm, 14 * mm, W - 20 * mm, 14 * mm)
  c.drawString(20 * mm, 9.5 * mm, "Kit Planner 2027 · uso pessoal e comercial de produtos impressos · proibida a revenda dos arquivos")
  c.drawRightString(W - 20 * mm, 9.5 * mm, str(doc.page))
  c.restoreState()


# ------------------------------------------------------------------ conteúdo
def story():
  S = [Spacer(1, 10), PageBreak()]
  # 1 — bem-vinda / o que recebeu
  S += [P("Bem-vinda ao seu kit", "h1"), P("Tudo o que está nesta pasta foi pensado para você produzir planners lindos, com acabamento profissional, sem depender de designer. Guarde este guia por perto: ele responde as dúvidas mais comuns da produção.", "sub")]
  S += [P("O que você recebeu", "h2")]
  S += [table([
    ["Pasta / arquivo", "O que é", "Como usar"],
    ["miolo/ Planner-2027-Miolo-A5-Delicada.pdf", "Miolo completo, 254 páginas A5, tema Delicada (rosé, serifada, botânica)", "Imprimir direto em A5 (frente e verso) ou enviar para gráfica"],
    ["miolo/ Planner-2027-Miolo-A5-Neutra.pdf", "Mesmo conteúdo no tema Neutra (minimalista, preto/areia)", "Idem"],
    ["miolo-a4-2pp/ ...virar-borda-CURTA / LONGA.pdf", "Miolo imposto 2 páginas por folha A4 (64 folhas), para cortar ao meio e empilhar", "Impressoras domésticas A4 — veja o capítulo de impressão"],
    ["capas/ Capas-2027-30-modelos-A5-com-sangria.pdf", "30 capas + contracapas, 148×210 mm com 3 mm de sangria", "Gráfica (papel 250–300 g, laminação fosca)"],
    ["capas/ Capas-2027-30-modelos-A4-com-marcas-de-corte.pdf", "As mesmas capas centralizadas em A4 com marcas de corte", "Impressão caseira ou em copiadora"],
    ["capas/ png-300dpi/", "PNG de cada capa e contracapa em 300 dpi", "Personalizar com nome no Canva / Photopea"],
    ["extras/ Divisorias-2027-12-meses-A5-*.pdf", "12 divisórias de meses com aba (uma por tema)", "Papel 180–250 g, inserir antes da abertura de cada mês"],
    ["extras/ Guardas-2027-8-padroes-A5.pdf", "8 guardas estampadas", "Papel 120–180 g, 1 após a capa e 1 antes da contracapa"],
    ["extras/ Adesivos-2027-2-folhas-A4-*.pdf", "2 folhas de adesivos por tema (abas, rótulos, ícones, frases)", "Papel adesivo fosco A4 + recorte"],
    ["mockups/", "Imagens prontas para divulgar (capas, miolo aberto, catálogo das 30 capas)", "Instagram, WhatsApp, Elo7, Shopee"],
    ["bonus/ (este guia)", "Guia da Encadernadora", "Ler antes de produzir o primeiro planner"],
  ], [52 * mm, 66 * mm, 52 * mm])]
  S += [callout("os PDFs do miolo são vetoriais: imprimem nítidos em qualquer tamanho. Se a gráfica pedir, eles podem ser redimensionados proporcionalmente (ex.: A6) sem perda de qualidade.", "Importante")]
  S += [PageBreak()]

  # 2 — impressão do miolo
  S += [P("Imprimindo o miolo", "h1"), P("Dois caminhos: imprimir direto em folhas A5 (mais simples) ou em A4 com duas páginas por folha (mais barato por folha e aceito em qualquer impressora doméstica).", "sub")]
  S += [P("Opção A · papel A5, frente e verso", "h2")]
  S += [numbered(["Abra <b>Planner-2027-Miolo-A5-Delicada.pdf</b> (ou Neutra) no Adobe Reader ou no navegador.",
          "Papel: <b>A5 (148 × 210 mm)</b>. Escala: <b>Tamanho real / 100%</b> (nunca “ajustar à página”).",
          "Frente e verso: ative e escolha <b>virar na borda longa</b> (a borda longa de uma folha A5 em pé é a lateral — é como um livro).",
          "Imprima primeiro um teste com as páginas 1 a 4 e confira se o verso ficou alinhado e na posição correta.",
          "Imprima o restante. O arquivo já tem 254 páginas (127 folhas), com a abertura de cada mês sempre em página ímpar (lado direito)."])]
  S += [P("Opção B · papel A4, 2 páginas por folha (corte e empilhe)", "h2")]
  S += [P("Use os arquivos da pasta <b>miolo-a4-2pp/</b>. Eles já vêm impostos no sistema “corte e empilhe”: você imprime as 64 folhas frente e verso, corta a pilha ao meio e coloca a metade da esquerda sobre a metade da direita — pronto, as 256 páginas ficam em ordem (as 2 últimas são em branco e podem ser usadas como notas).")]
  S += [table([
    ["Sua impressora vira as folhas…", "Use este arquivo", "Configuração de frente e verso"],
    ["pela lateral, como um livro (o mais comum em impressoras com duplex automático quando a página é paisagem)", "…virar-borda-CURTA.pdf", "Frente e verso · virar na borda CURTA"],
    ["por cima, como um calendário", "…virar-borda-LONGA.pdf", "Frente e verso · virar na borda LONGA"],
    ["impressora sem duplex", "qualquer um dos dois", "Imprima só as páginas ímpares, recoloque a pilha e imprima as pares (faça um teste com 2 folhas antes)"],
  ], [68 * mm, 44 * mm, 58 * mm])]
  S += [callout("não sabe qual é o seu caso? Imprima apenas as folhas 1 e 2 de cada arquivo (são 2 folhas A4) e veja em qual delas a página 2 fica atrás da página 1 na posição certa. Depois use só esse arquivo.", "Teste de 2 folhas")]
  S += [P("Papel e tinta", "h2")]
  S += [bullets(["<b>Sulfite 75 g</b>: mais barato, bom para teste. <b>Sulfite 90 g</b> ou <b>pólen bold 90 g</b>: toque premium, menos transparência, canetas não vazam — é o que recomendamos para venda.",
          "Os tons do miolo são claros de propósito: gastam pouca tinta/toner e ficam elegantes mesmo em impressoras simples. Em laser, use modo “qualidade”; em jato de tinta, papel <i>matte</i> deixa o resultado mais bonito.",
          "Em gráfica rápida, peça: <b>“miolo A5, 254 páginas, 4×4 cores (ou 1×1 se quiser mais barato), sulfite 90 g, sem acabamento — vou encadernar”</b>. Envie o arquivo A5 (a gráfica faz a própria imposição)."])]
  S += [PageBreak()]

  # 3 — capas
  S += [P("Imprimindo as capas", "h1"), P("As 30 capas foram criadas em 148 × 210 mm com 3 mm de sangria em cada lado (arquivo final 154 × 216 mm). A sangria evita filetes brancos na borda depois do corte.", "sub")]
  S += [P("Materiais que funcionam bem", "h2")]
  S += [table([
    ["Material", "Gramatura", "Acabamento", "Observação"],
    ["Papel couché fosco", "250–300 g", "Laminação BOPP fosca (ou brilho)", "Padrão profissional; cores fiéis"],
    ["Cartão triplex / supremo", "250–300 g", "Laminação ou verniz", "Mais rígido, ótimo com acetato por cima"],
    ["Papel fotográfico fosco", "200–230 g", "Sem laminação (ou plástico adesivo)", "Impressão caseira em jato de tinta"],
    ["Papelão cinza 1–1,5 mm (capa dura)", "—", "Encapar com a capa impressa em 150–180 g", "Mais trabalhoso, maior valor percebido"],
  ], [40 * mm, 24 * mm, 50 * mm, 56 * mm])]
  S += [P("Qual arquivo usar", "h2")]
  S += [bullets(["<b>Gráfica</b>: envie <b>Capas-2027-30-modelos-A5-com-sangria.pdf</b> e indique as páginas (ex.: capa 05 = páginas 9 e 10). Peça “4×4, 300 g, laminação fosca, corte no formato final 148 × 210 mm”.",
          "<b>Em casa / copiadora</b>: use <b>Capas-2027-30-modelos-A4-com-marcas-de-corte.pdf</b>; imprima a frente (página ímpar) e o verso (página par) e corte pelas marcas com estilete e régua de metal.",
          "<b>Personalizar com nome</b>: abra o PNG em 300 dpi no Canva (Criar design → Tamanho personalizado → 154 × 216 mm), insira a imagem, adicione o texto e baixe em “PDF para impressão” com marcas de corte e sangria."])]
  S += [callout("as fontes das capas são Playfair Display, Great Vibes (delicadas) e Montserrat (neutras) — todas gratuitas no Canva. Assim o nome do cliente combina com o restante do design.", "Fontes")]
  S += [P("Furação e cantos", "h2")]
  S += [bullets(["Fure capa, guardas, divisórias e miolo juntos, em pequenas pilhas, para os furos ficarem alinhados.",
          "Arredonde os cantos externos (cantoneira 5–8 mm): o planner ganha acabamento de loja e resiste melhor ao uso.",
          "Opcional: capa de acetato 0,3 mm na frente e papelão cinza atrás — a combinação favorita das clientes para planners de mesa."])]
  S += [PageBreak()]

  # 4 — montagem wire-o
  S += [P("Montagem e encadernação", "h1"), P("Ordem recomendada e tamanhos de wire-o para o miolo completo (127 folhas A5 em sulfite 90 g ≈ 14 mm de bloco).", "sub")]
  S += [P("Ordem de montagem", "h2")]
  S += [numbered(["Capa da frente (laminada) — opcional acetato por cima.", "Guarda estampada (papel 120–180 g).",
          "Páginas iniciais do miolo (páginas 1 a 20).", "Divisória de Janeiro + páginas de Janeiro; repita para cada mês (a divisória entra sempre antes da página de abertura do mês).",
          "Páginas finais (retrospectiva, contatos, notas).", "Guarda estampada + contracapa (verso da capa escolhida ou papelão)."])]
  S += [P("Tamanho do wire-o (valores aproximados — confirme com seu fornecedor)", "h2")]
  S += [table([
    ["Bloco (folhas de 75–90 g)", "Wire-o", "Passo", "Serve para"],
    ["até 60 folhas (≈ 7 mm)", "3/8\" (9,5 mm)", "3:1", "cadernetas e mini planners"],
    ["até 100 folhas (≈ 11 mm)", "1/2\" (12,7 mm)", "3:1", "miolo reduzido / semestral"],
    ["até 120 folhas (≈ 13 mm)", "5/8\" (15,9 mm)", "3:1", "miolo completo em 75 g, sem divisórias"],
    ["até 150 folhas (≈ 16 mm)", "3/4\" (19,1 mm)", "3:1 ou 2:1", "miolo completo + divisórias + guardas (recomendado)"],
    ["até 180 folhas (≈ 20 mm)", "7/8\" (22,2 mm)", "2:1", "miolo + capa dura + extras"],
    ["até 220 folhas (≈ 25 mm)", "1\" (25,4 mm)", "2:1", "dois miolos ou papel mais grosso"],
  ], [50 * mm, 32 * mm, 22 * mm, 66 * mm])]
  S += [bullets(["Regra prática: o diâmetro do wire-o deve ser cerca de <b>20–25 % maior</b> que a espessura total do bloco (miolo + capas + extras) para o planner abrir e girar 360°.",
          "Passo 3:1 (3 anéis por polegada) = anéis menores e visual mais fino, ideal até 3/4\". Passo 2:1 = anéis maiores para blocos grossos. A furadeira deve ser do mesmo passo do wire-o.",
          "Alternativas: <b>espiral plástica</b> (mais barata), <b>garras plásticas</b>, <b>encadernação com discos</b> (permite trocar páginas) e <b>costura copta</b> para um produto artesanal premium."])]
  S += [callout("feche o wire-o com o lado da emenda voltado para dentro da contracapa e aperte apenas o suficiente para formar um círculo — anéis ovais rasgam o furo com o tempo.", "Acabamento")]
  S += [PageBreak()]

  # 5 — custos e preço
  S += [P("Custos e preço de venda", "h1"), P("Exemplo realista para 1 planner completo produzido em casa (impressora laser colorida) e com capa feita em gráfica. Ajuste os valores para a sua cidade e fornecedores.", "sub")]
  S += [table([
    ["Item", "Quantidade", "Custo unitário", "Subtotal"],
    ["Sulfite 90 g A4 (2 págs. por folha)", "64 folhas", "R$ 0,06", "R$ 3,84"],
    ["Toner / tinta (miolo, páginas claras)", "254 páginas", "R$ 0,05", "R$ 12,70"],
    ["Capa + contracapa 300 g laminadas (gráfica)", "1 jogo", "R$ 6,00", "R$ 6,00"],
    ["Guardas (2) + divisórias (12) em papel 180 g", "14 folhas", "R$ 0,35", "R$ 4,90"],
    ["Wire-o 3/4\" + furação", "1 un.", "R$ 2,50", "R$ 2,50"],
    ["Folha de adesivos (opcional, 1 de 2)", "1 folha A4", "R$ 2,80", "R$ 2,80"],
    ["Embalagem (saco kraft/celofane + tag)", "1 un.", "R$ 1,80", "R$ 1,80"],
    ["Custo de materiais", "", "", "R$ 34,54"],
    ["Mão de obra (≈ 40 min a R$ 25/h)", "", "", "R$ 16,70"],
    ["Custo total de produção", "", "", "R$ 51,24"],
  ], [78 * mm, 30 * mm, 30 * mm, 32 * mm])]
  S += [P("Sugestão de preços", "h2")]
  S += [table([
    ["Versão", "O que inclui", "Preço sugerido", "Margem sobre materiais"],
    ["Essencial", "miolo + capa laminada + wire-o", "R$ 89 a R$ 99", "≈ 2,6×"],
    ["Completa", "+ divisórias, guardas, adesivos e nome na capa", "R$ 119 a R$ 139", "≈ 3,4×"],
    ["Premium", "capa dura/acetato, elástico, caneta e caixa", "R$ 159 a R$ 189", "≈ 4×"],
  ], [26 * mm, 72 * mm, 36 * mm, 36 * mm])]
  S += [bullets(["Fórmula simples: <b>preço = (materiais + mão de obra) × 1,8 a 2,2</b>, já cobrindo taxas de plataforma (Shopee/Elo7 ≈ 12–20 %), embalagem de envio e imprevistos.",
          "Venda a “Completa” como padrão e a “Essencial” como opção econômica: a maioria escolhe a do meio.",
          "Em pedidos de 5+ unidades (empresas, escolas, igrejas), ofereça 10 % de desconto — o custo por unidade cai com a impressão em lote.",
          "Com o kit você recupera o investimento no <b>primeiro planner vendido</b>; a partir do segundo, o arquivo é lucro puro."])]
  S += [PageBreak()]

  # 6 — fotos e divulgação
  S += [P("Fotos, legendas e divulgação", "h1"), P("Use os mockups da pasta <b>mockups/</b> para começar hoje e substitua por fotos reais assim que montar o primeiro exemplar.", "sub")]
  S += [P("Fotos reais que vendem", "h2")]
  S += [bullets(["Luz natural de janela, nunca flash. Fundo neutro (mesa de madeira clara, tecido linho, papel kraft).",
          "Os 5 ângulos: capa fechada de frente · planner aberto na semana · detalhe do wire-o e dos adesivos · pilha com várias capas · nas mãos de alguém (escala e desejo).",
          "Mostre a página sendo usada: caneta, uma anotação à mão, uma xícara. Planner cheio vende mais que planner vazio.",
          "Grave um vídeo de 15 s folheando o miolo — é o conteúdo que mais gera perguntas no direct."])]
  S += [P("Legendas prontas (copie e ajuste)", "h2")]
  S += [table([
    ["Objetivo", "Legenda"],
    ["Lançamento / pré-venda", "Abri a pré-venda do Planner 2027! Miolo completo com planejamento anual, mensal e semanal + controle financeiro e hábitos, em 2 estilos e 30 capas pra escolher. Lote limitado, entrega em dezembro. Chama no direct pra garantir o seu "],
    ["Prova social", "Olha o carinho que ficou o planner da @cliente Capa Jardim Sage com nome, divisórias e adesivos. Quer o seu personalizado? Só mandar “QUERO 2027”."],
    ["Urgência", "Últimas 5 unidades do lote de dezembro! Depois disso, só em janeiro. Quem já organizou 2027? "],
    ["Educativo", "Por que planner físico? Escrever à mão aumenta a memória e a sensação de controle. Por isso o miolo tem revisão mensal, metas e espaço de bem-estar toda semana "],
  ], [34 * mm, 136 * mm])]
  S += [P("Hashtags: #planner2027 #planner #agenda2027 #papelariapersonalizada #encadernacaoartesanal #planneramor #organizacao #planejamento2027 #presentecriativo", "small")]
  S += [PageBreak()]

  # 7 — vendas e scripts
  S += [P("Como vender: pré-venda, lotes e scripts", "h1"), P("O segredo do planner é vender antes de produzir. Pré-venda com lote pequeno gera caixa, evita estoque parado e cria urgência real.", "sub")]
  S += [P("Modelo de pré-venda em 4 passos", "h2")]
  S += [numbered(["<b>Anuncie um lote</b> (ex.: 20 unidades) com data de entrega (ex.: 10 de dezembro) e prazo para fechar (7 dias).",
          "<b>Sinal de 50 %</b> no pedido (Pix) e o restante na entrega. Registre tudo em uma lista: nome, capa, tema do miolo, nome na capa, extras.",
          "<b>Produza em lote</b>: imprima todos os miolos de uma vez, depois todas as capas, depois fure e monte. Economiza horas.",
          "<b>Entregue com foto</b>: peça para a cliente marcar você. Cada entrega vira novo conteúdo e novos pedidos."])]
  S += [P("Script de WhatsApp", "h2")]
  S += [table([
    ["Momento", "Mensagem"],
    ["Abertura", "Oi, [nome]! Vi que você curtiu o Planner 2027. Ele tem 254 páginas em A5: calendário anual, planejamento de cada mês, semanas completas com espaço pra hábitos e bem-estar, controle financeiro e muito mais. Você prefere o estilo Delicado (rosé) ou Neutro (preto e areia)?"],
    ["Objeção de preço", "Entendo! Ele custa R$ 119 na versão completa, mas vem com capa laminada, nome personalizado, divisórias de meses, guardas e adesivos — tudo montado à mão. Posso parcelar em 2× ou você pode garantir a versão Essencial por R$ 89 "],
    ["Fechamento", "Perfeito! Pra reservar o seu: me manda a capa escolhida (mando o catálogo com 30 opções), o nome pra personalizar e o Pix do sinal de R$ 60. Entrego até 10/12, certinho pra começar o ano organizada "],
    ["Pós-venda", "[nome], seu planner ficou pronto! Te mando a foto? Ah, e se você gostou, tenho um cupom de R$ 10 pra uma amiga que quiser o dela também."],
  ], [30 * mm, 140 * mm])]
  S += [P("Onde vender", "h2")]
  S += [bullets(["<b>Instagram + WhatsApp</b>: canal principal; use os mockups no feed e stories com enquetes de capas.",
          "<b>Elo7 e Shopee</b>: cadastre o produto como “Planner 2027 personalizado A5 wire-o” com as fotos do catálogo; o Elo7 tem público que busca papelaria artesanal.",
          "<b>Feiras, escolas e empresas</b>: kits de 10+ com logo na capa (use os PNGs e insira a logo no Canva).",
          "<b>Bazares de fim de ano</b>: leve 10 prontos com as capas mais pedidas (Jardim Sage, Preto Essencial, Terracota, Céu Estrelado)."])]
  S += [PageBreak()]

  # 8 — calendário + checklist
  S += [P("Calendário de vendas 2026 → 2027", "h1"), P("Planner tem três picos de venda. Planeje a produção para chegar com estoque em cada um deles.", "sub")]
  S += [table([
    ["Quando", "O que fazer", "Meta sugerida"],
    ["Outubro", "Montar 2 amostras físicas, fotografar, publicar catálogo de capas, abrir pré-venda lote 1", "10–20 pedidos"],
    ["Novembro", "Produzir lote 1; Black Friday (26/11) com brinde (adesivos) em vez de desconto; abrir lote 2 para Natal", "20–30 pedidos"],
    ["1 a 15 de dezembro", "Entregas do lote 1 e 2; conteúdo de unboxing; kits presente com caneta", "entregas + 10 pedidos extras"],
    ["16 a 31 de dezembro", "Lote “virada de ano” (pronta-entrega com 4 capas campeãs)", "10 unidades à pronta-entrega"],
    ["Janeiro", "Segunda onda: “ainda dá tempo de organizar 2027”; campanha para quem ganhou Pix de Natal", "15–20 pedidos"],
    ["Fevereiro", "Volta às aulas: versão para professoras e estudantes (capa + nome + adesivos escolares)", "10–15 pedidos"],
    ["Março em diante", "Planner semestral (imprima só de julho a dezembro), cadernos e agendas com as mesmas capas", "recorrência"],
  ], [34 * mm, 100 * mm], ) if False else table([
    ["Quando", "O que fazer", "Meta sugerida"],
    ["Outubro", "Montar 2 amostras físicas, fotografar, publicar catálogo de capas, abrir pré-venda lote 1", "10–20 pedidos"],
    ["Novembro", "Produzir lote 1; Black Friday (26/11) com brinde (adesivos) em vez de desconto; abrir lote 2 para Natal", "20–30 pedidos"],
    ["1 a 15 de dezembro", "Entregas do lote 1 e 2; conteúdo de unboxing; kits presente com caneta", "entregas + 10 extras"],
    ["16 a 31 de dezembro", "Lote “virada de ano” (pronta-entrega com 4 capas campeãs)", "10 à pronta-entrega"],
    ["Janeiro", "Segunda onda: “ainda dá tempo de organizar 2027”; campanha para quem ganhou Pix de Natal", "15–20 pedidos"],
    ["Fevereiro", "Volta às aulas: versão para professoras e estudantes (capa + nome + adesivos escolares)", "10–15 pedidos"],
    ["Março em diante", "Planner semestral (imprima só de julho a dezembro), cadernos e agendas com as mesmas capas", "recorrência"],
  ], [34 * mm, 100 * mm, 36 * mm])]
  S += [P("Checklist de produção (por pedido)", "h2")]
  S += [check_list(["Pedido anotado: capa, tema do miolo, nome na capa, extras, prazo e sinal recebido",
           "Miolo impresso e conferido (teste de 4 páginas antes do lote)", "Capa + contracapa impressas, laminadas e cortadas na medida",
           "Guardas e divisórias impressas e posicionadas antes de cada mês", "Furação alinhada (capa, guardas, miolo e divisórias juntos)",
           "Wire-o do tamanho certo, fechado redondo", "Cantos arredondados e limpeza final", "Adesivos recortados e embalagem com tag",
           "Foto do produto pronto enviada para a cliente (e salva para o portfólio)", "Pedido de avaliação / indicação enviado 3 dias após a entrega"])]
  S += [PageBreak()]

  # 9 — licença e FAQ
  S += [P("Licença de uso e perguntas frequentes", "h1"), P("Leia com atenção: a licença protege você e o trabalho de quem criou os arquivos.", "sub")]
  S += [P("O que você pode fazer", "h2")]
  S += [bullets(["Imprimir e vender planners, agendas e cadernos <b>físicos</b> produzidos com estes arquivos, em quantidade ilimitada, com a sua marca.",
          "Personalizar as capas (nome, logo, frases) e combinar miolos, capas e extras como quiser.",
          "Usar os mockups e o catálogo em redes sociais, marketplaces e materiais impressos de divulgação."])]
  S += [P("O que você não pode fazer", "h2")]
  S += [bullets(["Vender, doar, compartilhar ou disponibilizar os arquivos digitais (PDF/PNG), inteiros ou em partes, inclusive em grupos.",
          "Vender o miolo como produto digital (“arquivo editável”, “PDF para imprimir em casa”).",
          "Registrar ou alegar autoria dos designs."])]
  S += [P("Perguntas frequentes", "h2")]
  S += [table([
    ["Pergunta", "Resposta"],
    ["Os arquivos são editáveis?", "Os miolos não (são PDFs fechados para manter o padrão de impressão). As capas vêm em PNG para personalização com nome/logo no Canva ou similar."],
    ["Posso imprimir em outro tamanho?", "Sim: ao imprimir, use “ajustar à área imprimível” para A6 ou o PDF escala proporcionalmente. Para A4 completo, imprima o A5 com escala 141 %."],
    ["O planner começa em que dia?", "A primeira semana vai de 28/12/2026 a 03/01/2027 (segunda a domingo); são 53 semanas até 02/01/2028. Feriados nacionais e datas comemorativas de 2027 já estão marcados."],
    ["Posso trocar a ordem das páginas?", "Sim, no Adobe Acrobat ou em sites como ilovepdf.com (organizar páginas). Mantenha a abertura de cada mês em página ímpar para os meses começarem à direita."],
    ["A gráfica pediu CMYK/perfil de cor.", "Os arquivos estão em RGB com cores suaves; gráficas digitais convertem automaticamente. Se quiser cores exatas, peça uma prova impressa de 2 páginas antes do lote."],
    ["Recebo atualizações?", "Correções de erros são enviadas sem custo para quem comprou. Novas versões (2028, outros tamanhos) terão condições especiais para clientes."],
  ], [48 * mm, 122 * mm])]
  S += [Spacer(1, 6 * mm), P("Bons negócios e um 2027 cheio de planners entregues com orgulho! ", "center")]
  return S


def build():
  doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=24 * mm, bottomMargin=20 * mm,
              title="Guia da Encadernadora · Planner 2027", author="Kit Planner 2027", subject="Bônus: impressão, montagem, preço e vendas")
  doc.build(story(), onFirstPage=on_cover, onLaterPages=on_page)
  print("ok", OUT)


if __name__ == "__main__":
  build()
