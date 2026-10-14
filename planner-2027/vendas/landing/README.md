# Landing page — Ateliê Planner 2027

Página de vendas estática (HTML + CSS + JS puro, sem build). Funciona em qualquer hospedagem.

## Arquivos
| Arquivo | O que é |
|---|---|
| `index.html` | página de vendas completa |
| `obrigado.html` | página de obrigado (use como "Página de obrigado" na Kiwify) |
| `termos.html`, `privacidade.html` | termos de uso/licença e política de privacidade (exigidos pela Meta Ads e pela Kiwify) |
| `assets/config.js` | **único arquivo que você precisa editar** (links, WhatsApp, e-mail, preços, pixel, data do lançamento) |
| `assets/style.css`, `assets/app.js` | visual e comportamento (contador, galeria, calculadora, CTA fixo) |
| `img/` | imagens (renderizadas direto dos PDFs do kit + 2 fotos ilustrativas geradas por IA, sem metadados) |

## 1. Configure (`assets/config.js`)
```js
checkoutUrl: "https://pay.kiwify.com.br/XXXXXX", // link da oferta (Produto → Ofertas → copiar link)
whatsapp: "5599985298576",                       // 55 + DDD + número
email: "suporte....@gmail.com",
offerEnd: "2026-10-20T23:59:59-03:00",           // fim do lançamento; depois disso a página mostra R$ 47 sozinha
pixelId: "123456789012345",                      // Pixel da Meta (opcional)
```
- Enquanto `checkoutUrl` estiver vazio, todos os botões rolam até a seção de preço.
- Parâmetros `utm_*`, `fbclid`, `src` e `sck` da URL são repassados ao checkout automaticamente.
- Com `pixelId` preenchido a página dispara `PageView`, `ViewContent` (galeria), `InitiateCheckout` (clique em comprar) e `Contact` (WhatsApp). O evento `Purchase` deve vir da Kiwify (aba Pixels + API de conversões) para não duplicar.

## 2. Publique (escolha uma)
1. **Netlify Drop** (grátis, 1 minuto): acesse app.netlify.com/drop e arraste a pasta `landing` inteira. Você recebe um link `https://nome.netlify.app`.
2. **Vercel**: `vercel deploy` dentro da pasta, ou arraste no painel.
3. **Hospedagem própria / Hostinger**: envie a pasta por FTP para `public_html/planner2027/`.
4. **GitHub Pages** (já configurado neste repositório, branch `main`): a página fica em `https://wesleyvalmontoliveira-byte.github.io/KAYW.001/planner-2027/vendas/landing/`. O arquivo `_config.yml` na raiz impede que produto, ZIPs e documentos internos sejam publicados no site.

O `og:image`, `og:url` e `canonical` do `index.html` já apontam para o endereço do GitHub Pages; se mudar de domínio, atualize-os.

## 3. Conecte à Kiwify
- Produto → **URL da página de vendas**: cole o link publicado.
- Produto → **Página de obrigado**: `https://seu-link/obrigado.html`.
- Produto → **Ofertas**: copie o link da oferta e cole em `checkoutUrl`.

## 4. Substituições recomendadas antes de escalar anúncios
- Troque as 2 fotos ilustrativas (`img/foto-atelie-*.jpg`, geradas por IA) por fotos reais do seu ateliê ou dos planners montados.
- Depois das primeiras vendas, adicione depoimentos reais (prints de WhatsApp) — a página não traz depoimentos inventados de propósito.
- Preencha `businessName`/`businessDoc` no `config.js` para aparecer no rodapé e nos termos.

## Regenerar imagens das páginas
```bash
cd planner-2027/src && python3 build_landing_assets.py
```
