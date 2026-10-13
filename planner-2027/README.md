# Kit Planner 2027 — produto digital low-ticket (análise → produto → vendas)

Projeto completo gerado a partir da análise de um anúncio ativo na **Biblioteca de Anúncios da Meta**:
pesquisa do produto, recriação de um kit **melhor e mais completo** (PDFs com design visual) e o plano de vendas.

| Pasta | Conteúdo |
|---|---|
| `analise/relatorio-meta-ads.md` | Relatório da pesquisa: anúncio escolhido (início **17/09/2026**, há 26 dias), concorrentes, preços, estrutura da oferta e **sugestão de preço** |
| `produto/` | **O produto pronto** (ver abaixo) — 20 MB de PDFs/PNGs/JPGs |
| `src/` | Código Python que gera tudo (`build_all.sh` na raiz regenera o kit em ~30 s) |
| `vendas/` | Estratégia de vendas, copies/roteiros de anúncios Meta e **landing page** pronta (`vendas/landing/index.html`) |

## O produto (`produto/`)

```
produto/
├── miolo/            Planner-2027-Miolo-A5-Delicada.pdf   (254 páginas, A5, vetorial)
│                     Planner-2027-Miolo-A5-Neutra.pdf     (254 páginas, A5, vetorial)
├── miolo-a4-2pp/     4 PDFs: miolo imposto "2 páginas por folha" A4 (64 folhas), corte-e-empilhe,
│                     variantes para frente-e-verso virando na borda CURTA ou LONGA
├── capas/            Capas-2027-30-modelos-A5-com-sangria.pdf  (60 páginas: 30 capas + contracapas, 154×216 mm)
│                     Capas-2027-30-modelos-A4-com-marcas-de-corte.pdf
│                     png-300dpi/  (60 PNGs para personalizar com nome no Canva)
├── extras/           Divisorias-2027-12-meses-A5-{Delicada,Neutra}.pdf · Guardas-2027-8-padroes-A5.pdf
│                     Adesivos-2027-2-folhas-A4-{Delicada,Neutra}.pdf (300+ adesivos)
├── mockups/          10 imagens de divulgação (capas com wire-o, miolo aberto, catálogo das 30 capas, visão do kit)
└── bonus/            Guia-da-Encadernadora-Planner-2027.pdf (10 páginas: impressão, wire-o, custos, preço, legendas, scripts)
```

**Estrutura do miolo (254 páginas):** título · dados pessoais · calendários 2027 e 2028 · feriados · datas importantes · metas · ano em cores · saúde · exames · visão financeira · metas financeiras · acessos · leituras · favoritos · lugares · projetos · desejos · rotina → para cada mês: abertura (sempre em página ímpar) · planejamento (2 pág.) · calendário em página dupla · controle financeiro · hábitos 31×8 · bem-estar · lista · semanas em página dupla (53 semanas, 28/12/2026 → 02/01/2028) · revisão do mês → retrospectiva · próximo ano · contatos · notas · créditos.
Feriados nacionais 2027 (Carnaval 08–09/02, Sexta-feira Santa 26/03, Corpus Christi 27/05 etc.) e datas comemorativas já marcados.

## Preço sugerido

- **Lançamento (7 dias): R$ 27,90** → **preço cheio R$ 47,00**
- Order bump R$ 9,90 · upsell R$ 37,00 (Kit Professora) · ticket médio esperado ≈ R$ 35 (lançamento) / R$ 54 (cheio)
- Justificativa e comparação com concorrentes (R$ 3 a R$ 69,90) em `analise/relatorio-meta-ads.md`.

## Como regenerar

```bash
pip install reportlab pillow pymupdf pypdf
./build_all.sh            # ou, em src/: python3 build_miolo.py all && python3 build_capas.py ...
python3 src/preview.py produto/miolo/Planner-2027-Miolo-A5-Delicada.pdf 1,21,24,25 /tmp/p.png --dpi 70
```

Scripts: `build_miolo.py` (miolos, `--ano` para outros anos), `impose_a4.py`, `build_capas.py`, `build_extras.py`, `build_mockups.py`, `build_guia.py`, `preview.py`.

## Fontes e licenças

Fontes em `src/fonts/` (Google Fonts, licença SIL Open Font License 1.1 — uso comercial permitido, inclusive embutidas em PDF):
Playfair Display, Nunito, Montserrat, Inter, Great Vibes, Caveat, DM Serif Display, Poppins.
Ícones: Material Icons (Apache License 2.0). Toda a arte (padrões, raminhos, flores, capas) é vetorial e gerada pelo código — sem imagens de terceiros.
