# Estratégia de vendas — Kit Planner 2027 (arquivos para encadernação)

> Produto: kit digital low-ticket para artesãs/encadernadoras produzirem e venderem planners 2027 impressos.
> Modelo validado pelo anúncio analisado na Biblioteca de Anúncios da Meta (Nayara Oliveira Papelaria Criativa, ativo desde 17/09/2026, R$ 39,90).
> Preço-base: **R$ 47,00** · lançamento **R$ 27,90** (7 dias) · bump R$ 9,90 · upsell R$ 37,00.

---

## 1. Posicionamento

| | Concorrente analisado | **Nosso kit** |
|---|---|---|
| Promessa | "Planner 2027 para artesãs" (foco no arquivo) | **"Produza e venda planners 2027 sem designer"** (foco no lucro da artesã) |
| Miolos | 2 (delicada/neutra), não editáveis | 2 (Delicada/Neutra), 254 páginas, datados, com feriados 2027 — **+ versão A4 2 pág./folha** nas 2 opções de frente-e-verso |
| Capas | 30 PNG + Canva | 30 em **PDF com sangria + PNG 300 dpi** (gráfica e caseira) |
| Extras | guardas, mockups, adesivos, 2 bônus | guardas, **24 divisórias com aba**, 4 folhas de adesivos (300+), 10 mockups + catálogo |
| Bônus | não detalhado | **Guia da Encadernadora** (impressão, wire-o, planilha de custo, preço, legendas, scripts, calendário) |
| Preço | R$ 39,90 | R$ 47 (lançamento R$ 27,90) |

**Big idea do funil:** "o kit se paga no primeiro planner vendido" — a artesã compra um ativo de produção, não um PDF.

**Diferencial de mensagem:** ninguém no nicho ensina a *vender* o planner pronto. Nosso bônus resolve a dor seguinte ("comprei o arquivo e agora?"), o que aumenta a conversão e reduz reembolso.

---

## 2. Oferta e escada de preços

| Etapa | Item | Preço | Papel |
|---|---|---|---|
| Front-end | Kit Planner 2027 completo | **R$ 27,90** (lançamento, 7 dias) → R$ 47,00 | aquisição; margem para pagar tráfego |
| Order bump (checkout) | "Pacote Presente": 10 tags de presente + 3 cartões "para você" + 2 folhas extras de adesivos sazonais (Natal/Ano-novo) | **R$ 9,90** | +ticket com custo zero (gerar com os mesmos scripts) |
| Upsell 1 (pós-compra) | Kit Professora 2027 (miolo com horário de aulas, diário de classe, planejamento bimestral) + 10 capas escolares | **R$ 37,00** | expansão de catálogo para o mesmo público |
| Downsell | Só as 30 capas + Guia | R$ 17,00 | recupera quem recusou o upsell |
| Back-end (fev/27) | Miolo Semestral jul–dez 2027 + Agenda 2028 em pré-venda | R$ 27–47 | recorrência anual |

**Ticket médio esperado:** lançamento ≈ R$ 35 (27,90 + 25 % bump + 12 % upsell); preço cheio ≈ R$ 54.

**Garantia:** 7 dias incondicional (padrão de plataforma). Produto digital entregue por e-mail (Kiwify, Hotmart, Kavoo ou Cakto — taxas 8–10 % + R$ 1–2,50 por venda).

---

## 3. Funil

```
Anúncio (Reels/Stories/Feed)  →  Landing (vendas/landing/index.html)  →  Checkout + bump  →  Upsell  →  Entrega por e-mail
          ↑                                                                                              ↓
   Remarketing 7 dias                                                                  Grupo WhatsApp de clientes
   (quem viu 50 % do vídeo / visitou a página)                                         (prova social, UGC, back-end)
```

**Página de vendas** (já pronta em `vendas/landing/`): hero com promessa + preço, "para quem é", 8 cards do kit, página a página, catálogo das 30 capas, **calculadora de lucro**, pilha de valor (R$ 284) vs. R$ 27,90, garantia, FAQ, CTA fixo no mobile, contador de 7 dias.

**Checkout:** 1 página, Pix em destaque (maior conversão no nicho), cartão até 6x, bump marcado como "sim, quero" com imagem.

**Pós-compra:** e-mail 1 (acesso + link do guia), e-mail 2 (dia 2: "imprima estas 4 páginas de teste"), e-mail 3 (dia 5: "poste sua primeira foto e marque a gente"), e-mail 4 (dia 10: upsell Kit Professora com desconto para quem não comprou).

---

## 4. Tráfego pago (Meta Ads)

### Estrutura de campanhas (fase de lançamento, 14 dias)

| Campanha | Objetivo | Público | Orçamento/dia | Criativos |
|---|---|---|---|---|
| C1 · Conversão (compra) — Advantage+ | Vendas | Aberto BR, mulheres 25–55 (Advantage+ audience, sem interesses) | R$ 60 | 3 vídeos + 2 carrosséis + 1 estático |
| C2 · Conversão — interesses | Vendas | Interesses: encadernação, papelaria personalizada, Silhouette Cameo, scrapbook, Elo7, "artesanato" + comportamento pequenas empresas | R$ 40 | mesmos criativos (comparar CPA com C1) |
| C3 · Remarketing | Vendas | Visitantes LP 7 d + ViewContent + 50 % do vídeo, excluindo compradores | R$ 20 | depoimento/prova + "últimas horas" + FAQ em vídeo |
| C4 · Engajamento (opcional) | Visualização de vídeo (ThruPlay) | Lookalike 1 % de compradores (após 50 vendas) | R$ 20 | vídeo folheando o miolo |

Total: **R$ 120–140/dia** ≈ R$ 1.800–2.000 na fase de lançamento (14 dias). Depois, manter R$ 60–80/dia no que der CPA ≤ R$ 18.

### Métricas-alvo (benchmarks do nicho low-ticket digital BR)

| Métrica | Alvo | Alerta |
|---|---|---|
| CPM | R$ 15–30 | > R$ 45 → trocar criativo/público |
| CTR (link) | ≥ 1,5 % | < 0,9 % → gancho fraco |
| Conversão da LP → checkout iniciado | ≥ 12 % | < 7 % → promessa/preço/velocidade |
| Checkout iniciado → compra | ≥ 35 % (Pix) | < 25 % → bump confuso, checkout lento |
| **CPA (custo por venda)** | **≤ R$ 15** em lançamento (R$ 27,90) · ≤ R$ 22 a R$ 47 | > R$ 25 → pausar conjunto |
| ROAS (com bump/upsell) | ≥ 2,2 | < 1,5 por 3 dias → otimizar |
| Reembolso | ≤ 3 % | > 6 % → revisar expectativa (editável? físico?) |

**Ponto de equilíbrio por venda (lançamento):** ticket médio R$ 35 − taxa plataforma (≈ R$ 4) = R$ 31 de margem bruta por pedido → CPA de R$ 15 deixa ~R$ 16 de lucro por venda; a R$ 47 cheio (ticket ≈ R$ 54), CPA de R$ 22 deixa ~R$ 27.

### Projeção (90 dias, cenário conservador)

| Fase | Investimento | Vendas | Receita (ticket médio) | Resultado |
|---|---|---|---|---|
| Lançamento (14 d, R$ 27,90) | R$ 2.000 | 140 | R$ 4.900 (R$ 35) | +R$ 2.400 após taxas |
| Perene out–dez (R$ 47) | R$ 5.000 | 230 | R$ 12.400 (R$ 54) | +R$ 6.300 |
| Jan–fev (volta às aulas / Kit Professora) | R$ 2.000 | 90 | R$ 4.900 | +R$ 2.400 |
| **Total** | **R$ 9.000** | **460** | **≈ R$ 22.000** | **≈ R$ 11.000 líquido** |

> Público potencial é grande: só a busca "atividades" na Biblioteca de Anúncios devolve ~6.300 anúncios ativos (professoras/artesãs comprando PDFs), e "planner 2027" ~700. O concorrente analisado está no ar há 26 dias com 2 anúncios ativos — sinal de que a oferta converte.

---

## 5. Criativos (ganchos testados no nicho)

**Formato vencedor:** vídeo vertical 15–30 s, mãos folheando o planner impresso (ou mockup animado), texto na tela, voz ou música. Ver roteiros completos em `vendas/anuncios-meta.md`.

Ganchos (primeiros 3 s):
1. "Você encaderna? Então pare de pagar designer para fazer miolo de planner."
2. "Quanto você cobra num planner 2027? Esse aqui custa R$ 35 pra produzir e vende a R$ 119."
3. "254 páginas prontas, datadas, com feriados — e 30 capas. Por menos que um almoço."
4. "O erro de quem vende planner: começar a produzir em dezembro."
5. "Não é PDF pra imprimir em casa e usar. É pra você *vender*."

Estáticos: catálogo das 30 capas (`produto/mockups/catalogo-30-capas.jpg`), mockup capa 01 e 16, "antes/depois" (miolo aberto).

Regra de teste: 6 criativos → 3 dias → manter os 2 com menor CPA → substituir os piores por variações do melhor gancho a cada 5 dias.

---

## 6. Orgânico e comunidade (custo zero)

- **Instagram/TikTok** (3 posts/semana): reels folheando o miolo; "monte comigo" (time-lapse da encadernação); carrossel "quanto custa produzir um planner"; enquete de capas nos stories.
- **Pinterest**: 30 pins (uma capa por pin) linkando para a LP — tráfego de cauda longa até março.
- **Grupos de Facebook** de encadernação/papelaria (regras permitindo): post de valor "tabela de wire-o por número de folhas" (trecho do guia) + link na bio.
- **Elo7/Shopee** como vitrine: anunciar o kit digital a R$ 47 (sem desconto) — reforça o preço-âncora e capta busca orgânica.
- **Afiliadas** (plataforma): 40 % de comissão para artesãs influenciadoras do nicho — elas já têm a audiência exata.
- **Grupo de clientes no WhatsApp**: UGC (fotos dos planners montados) vira prova social para os anúncios de remarketing.

---

## 7. Calendário de lançamento

| Data | Ação |
|---|---|
| D-7 a D-1 | Conta de anúncios + pixel + domínio da LP; cadastrar produto, bump e upsell; gravar 3 vídeos; aquecer perfil com 5 posts |
| **D0 (ter)** | Abrir lançamento R$ 27,90 — C1 + C2 ligadas às 6h; stories ao vivo montando o planner |
| D+2 | Primeira otimização: pausar criativos com CTR < 0,9 %; ligar C3 (remarketing) |
| D+4 | E-mail/WhatsApp "metade do prazo"; carrossel com fotos de clientes |
| D+6 | "Últimas 24 h" em todos os canais; subir orçamento 30 % no melhor conjunto |
| **D+7** | Vira para R$ 47; manter campanhas com CPA ≤ R$ 22 |
| Nov (Black Friday 26/11) | Reabrir R$ 27,90 por 72 h + bump de brinde; lançar Kit Professora |
| Dez 1–20 | Mensagem "ainda dá tempo: imprima em casa em 1 dia" (versão A4) |
| Jan | Campanha "volta às aulas" (upsell) + pré-venda do Semestral |

---

## 8. KPIs semanais (planilha simples)

| Semana | Investimento | Cliques | Visitas LP | Checkouts | Vendas | Bump % | Upsell % | Receita | CPA | ROAS | Reembolsos |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | |
| 2 | | | | | | | | | | | |

Decisões automáticas: CPA > R$ 25 por 3 dias → pausar; ROAS > 3 por 3 dias → +20 % orçamento/dia; taxa de bump < 15 % → trocar imagem/texto do bump.

---

## 9. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Pirataria/compartilhamento dos arquivos | marca d'água invisível por comprador (nome no rodapé via plataforma), licença clara, preço baixo reduz incentivo |
| Expectativa de "editável" | FAQ e anúncio deixam claro: miolos fechados, capas PNG personalizáveis |
| Sazonalidade (cai em fevereiro) | back-end: Semestral, Agenda 2028, Kit Professora, cadernos com as mesmas capas |
| Dependência de Meta Ads | Pinterest + afiliadas + marketplaces como canais perenes |

---

## 10. Checklist de implementação

- [ ] Plataforma (Kiwify/Hotmart/Kavoo): produto, bump R$ 9,90, upsell R$ 37, e-mails de entrega
- [ ] Zipar `produto/` em 3 pacotes (miolos · capas · extras+bônus) e anexar na área de membros
- [ ] Publicar `vendas/landing/index.html` (Netlify/Vercel/hosting) com domínio próprio e pixel da Meta
- [ ] Trocar `href="#checkout"` pelo link real do checkout; ajustar data do contador
- [ ] Criar Business Manager, pixel, eventos (ViewContent, InitiateCheckout, Purchase) e API de conversões da plataforma
- [ ] Gravar 3 vídeos + 2 carrosséis + 1 estático (roteiros em `anuncios-meta.md`)
- [ ] Montar 2 exemplares físicos para fotos reais e para o vídeo de folhear
- [ ] Abrir grupo de clientes no WhatsApp e preparar as 4 mensagens de pós-venda
