/* Ateliê Planner 2027 — comportamento da landing (sem dependências) */
(function () {
  "use strict";
  var C = window.LP_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fmt = function (n) { try { return "R$ " + n.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); } catch (e) { return "R$ " + n.toFixed(2).replace(".", ","); } };

  /* ---------- Pixel da Meta ---------- */
  if (C.pixelId) {
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", C.pixelId);
    window.fbq("track", "PageView");
  }
  var track = function (ev, data) { if (window.fbq) { try { window.fbq("track", ev, data || {}); } catch (e) { } } };

  /* ---------- Oferta / preços / contador ---------- */
  var offerEnd = C.offerEnd ? new Date(C.offerEnd) : null;
  var state = { active: false };
  function applyOffer() {
    var now = new Date();
    state.active = !!(offerEnd && !isNaN(offerEnd) && offerEnd > now && C.priceLaunch < C.priceFull);
    var price = state.active ? C.priceLaunch : C.priceFull;
    $$("[data-price]").forEach(function (el) { el.textContent = fmt(price); });
    $$("[data-price-int]").forEach(function (el) { el.textContent = Math.floor(price); });
    $$("[data-price-cents]").forEach(function (el) { el.textContent = (Math.round(price * 100) % 100 + "").padStart(2, "0"); });
    $$("[data-price-full]").forEach(function (el) { el.textContent = fmt(C.priceFull); });
    $$("[data-installments]").forEach(function (el) { el.textContent = C.installmentsText || ""; });
    $$("[data-launch-only]").forEach(function (el) { el.hidden = !state.active; });
    $$("[data-full-only]").forEach(function (el) { el.hidden = state.active; });
    if (offerEnd && state.active) {
      var d = new Date(offerEnd);
      $$("[data-offer-date]").forEach(function (el) { el.textContent = d.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" }); });
    }
  }
  function tick() {
    if (!offerEnd || !state.active) return;
    var diff = offerEnd - new Date();
    if (diff <= 0) { applyOffer(); return; }
    var d = Math.floor(diff / 864e5), h = Math.floor(diff / 36e5) % 24, m = Math.floor(diff / 6e4) % 60, s = Math.floor(diff / 1e3) % 60;
    var p = function (x) { return (x < 10 ? "0" : "") + x; };
    var txt = (d > 0 ? d + "d " : "") + p(h) + ":" + p(m) + ":" + p(s);
    $$("[data-cd]").forEach(function (el) { el.textContent = txt; });
  }
  applyOffer(); tick(); setInterval(tick, 1000);

  /* ---------- Links: checkout, WhatsApp, e-mail, Instagram ---------- */
  var utm = "";
  try {
    var q = new URLSearchParams(location.search), keep = [];
    q.forEach(function (v, k) { if (/^(utm_|fbclid|src|sck)/i.test(k)) keep.push(encodeURIComponent(k) + "=" + encodeURIComponent(v)); });
    utm = keep.join("&");
  } catch (e) { }
  $$("a[data-checkout]").forEach(function (a) {
    if (C.checkoutUrl) {
      a.href = C.checkoutUrl + (utm ? (C.checkoutUrl.indexOf("?") > -1 ? "&" : "?") + utm : "");
      a.target = "_self";
    } else { a.href = "#checkout"; }
    a.addEventListener("click", function () { track("InitiateCheckout", { value: state.active ? C.priceLaunch : C.priceFull, currency: "BRL" }); });
  });
  var waHref = function (msg) { return "https://wa.me/" + (C.whatsapp || "") + "?text=" + encodeURIComponent(msg || C.whatsappMsg || ""); };
  $$("a[data-wa]").forEach(function (a) {
    a.href = waHref(a.getAttribute("data-msg"));
    a.target = "_blank"; a.rel = "noopener";
    a.addEventListener("click", function () { track("Contact"); });
  });
  $$("[data-wa-display]").forEach(function (el) { el.textContent = C.whatsappDisplay || C.whatsapp || ""; });
  $$("a[data-email]").forEach(function (a) { a.href = "mailto:" + C.email; a.textContent = C.email; });
  $$("[data-ig]").forEach(function (el) {
    if (C.instagram) { el.hidden = false; var a = el.tagName === "A" ? el : $("a", el); if (a) { a.href = "https://instagram.com/" + C.instagram; a.textContent = "@" + C.instagram; } }
    else { el.hidden = true; }
  });
  $$("[data-business]").forEach(function (el) { el.textContent = C.businessName || ""; });
  $$("[data-business-doc]").forEach(function (el) { el.textContent = C.businessDoc ? " · " + C.businessDoc : ""; });
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Galeria: filtros + lightbox ---------- */
  var figs = $$(".gallery figure");
  $$(".filters button").forEach(function (b) {
    b.addEventListener("click", function () {
      $$(".filters button").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      var f = b.getAttribute("data-f");
      figs.forEach(function (fg) { fg.hidden = !(f === "all" || fg.getAttribute("data-cat") === f); });
    });
  });
  var lb = $("#lb");
  if (lb && typeof lb.showModal === "function") {
    var lbImg = $("#lb-img"), lbCap = $("#lb-cap"), cur = 0;
    var visible = function () { return figs.filter(function (f) { return !f.hidden; }); };
    var show = function (i) {
      var v = visible(); if (!v.length) return;
      cur = (i + v.length) % v.length;
      var im = $("img", v[cur]);
      lbImg.src = im.getAttribute("data-full") || im.src; lbImg.alt = im.alt;
      lbCap.textContent = ($("figcaption", v[cur]) || {}).textContent || im.alt;
    };
    figs.forEach(function (f) { f.addEventListener("click", function () { show(visible().indexOf(f)); lb.showModal(); track("ViewContent", { content_name: "galeria" }); }); });
    $("#lb-prev").addEventListener("click", function () { show(cur - 1); });
    $("#lb-next").addEventListener("click", function () { show(cur + 1); });
    $("#lb-close").addEventListener("click", function () { lb.close(); });
    lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
    document.addEventListener("keydown", function (e) { if (!lb.open) return; if (e.key === "ArrowLeft") show(cur - 1); if (e.key === "ArrowRight") show(cur + 1); });
  }

  /* ---------- Calculadora ---------- */
  var qtd = $("#c-qtd"), preco = $("#c-preco"), custo = $("#c-custo");
  function calc() {
    if (!qtd) return;
    var q = +qtd.value, p = +preco.value, c = +custo.value || 0;
    var lucroU = Math.max(p - c, 0), mes = lucroU * q, ano = mes * 12;
    $("#o-qtd").textContent = q + (q === 1 ? " planner" : " planners");
    $("#o-preco").textContent = fmt(p);
    $("#r-unit").textContent = fmt(lucroU);
    $("#r-mes").textContent = fmt(mes);
    $("#r-ano").textContent = fmt(ano);
    var kit = state.active ? C.priceLaunch : C.priceFull;
    var n = lucroU > 0 ? Math.ceil(kit / lucroU) : 0;
    $("#r-pay").textContent = n > 0 ? (n === 1 ? "O kit se paga com 1 planner vendido." : "O kit se paga com " + n + " planners vendidos.") : "Ajuste o preço de venda acima do custo.";
  }
  if (qtd) { [qtd, preco, custo].forEach(function (i) { i.addEventListener("input", calc); }); calc(); }

  /* ---------- CTA fixo no mobile + animação de entrada ---------- */
  var sticky = $("#sticky"), hero = $("#hero"), offer = $("#checkout");
  if ("IntersectionObserver" in window) {
    var pastHero = false, offerVisible = false;
    var upd = function () { if (sticky) sticky.classList.toggle("show", pastHero && !offerVisible); };
    if (hero) new IntersectionObserver(function (es) { pastHero = !es[0].isIntersecting && es[0].boundingClientRect.top < 0; upd(); }, { threshold: 0 }).observe(hero);
    if (offer) new IntersectionObserver(function (es) { offerVisible = es[0].isIntersecting; upd(); }, { threshold: .15 }).observe(offer);
    var ro = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); ro.unobserve(e.target); } }); }, { threshold: .12, rootMargin: "0px 0px -40px 0px" });
    $$(".reveal").forEach(function (el) { ro.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("in"); }); }
})();
