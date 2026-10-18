// Medición anónima de visitas de Visión Alfa: sin cookies y sin datos personales.
(function () {
  try {
    if (localStorage.getItem("va-panel-k")) return; // no contar las visitas de Flor
  } catch (e) {}
  var URL_FN = "https://futhqkqfjuuemhcxzakn.supabase.co/functions/v1/visita";
  var CLAVE = "sb_publishable_x20gCAkWL2NsZG84wiWgGQ_hlchdMOF";
  var sesion;
  try {
    sesion = sessionStorage.getItem("va-s");
    if (!sesion) { sesion = Math.random().toString(36).slice(2, 12); sessionStorage.setItem("va-s", sesion); }
  } catch (e) { sesion = Math.random().toString(36).slice(2, 12); }

  function origen() {
    var q = new URLSearchParams(location.search), utm = (q.get("utm_source") || "").toLowerCase();
    var r = ""; try { r = document.referrer ? new URL(document.referrer).hostname : ""; } catch (e) {}
    var t = utm || r;
    if (!t || r === location.hostname) return utm || (r === location.hostname ? "interno" : "directo");
    if (/instagram|ig\b/.test(t)) return "instagram";
    if (/facebook|fb\b/.test(t)) return "facebook";
    if (/whatsapp|wa\.me/.test(t)) return "whatsapp";
    if (/google/.test(t)) return "google";
    if (/mercadopago|mercadolibre/.test(t)) return "mercadopago";
    if (/tiktok/.test(t)) return "tiktok";
    return t.replace(/^www\./, "").slice(0, 40);
  }
  var pagina = (location.pathname.split("/").pop() || "index.html").replace(".html", "") || "index";
  var disp = Math.min(screen.width, innerWidth) <= 760 ? "celular" : "compu";

  function enviar(evento, detalle) {
    try {
      fetch(URL_FN, {
        method: "POST", keepalive: true,
        headers: { "Content-Type": "application/json", apikey: CLAVE },
        body: JSON.stringify({ evento: evento, pagina: pagina, origen: evento === "vista" ? origen() : null, dispositivo: disp, sesion: sesion, detalle: detalle || null }),
      }).catch(function () {});
    } catch (e) {}
  }
  enviar("vista");

  // Clics importantes: comprar, reservar, la nube, equipo, recursos gratis, WhatsApp
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a,button"); if (!a) return;
    var d = null, href = a.getAttribute("href") || "";
    if (a.dataset.comprar) d = "comprar:" + a.dataset.comprar;
    else if (a.closest(".nube-caja") && !a.classList.contains("nube-x")) d = "nube";
    else if (/agenda\.html/.test(href)) d = "reservar:" + ((href.match(/servicio=([a-z0-9-]+)/) || [])[1] || "asesoria");
    else if (/equipo\.html/.test(href)) d = "equipo";
    else if (/recursos\.html|cv\.html/.test(href)) d = "gratis";
    else if (/wa\.me|whatsapp/.test(href)) d = "whatsapp";
    if (d) enviar("clic", d);
  }, true);
})();
