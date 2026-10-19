// Cartelito de actividad REAL de la web: compras confirmadas por Mercado Pago (anónimas)
// y números de visitas medidos. Si no hay nada real para mostrar, no aparece.
(function () {
  var URL_FN = "https://futhqkqfjuuemhcxzakn.supabase.co/functions/v1/actividad";
  var CLAVE = "sb_publishable_x20gCAkWL2NsZG84wiWgGQ_hlchdMOF";
  var MAX_POR_VISITA = 3, ESPERA_INICIAL = 9000, VISIBLE = 6500, ENTRE = 22000;
  try { if (sessionStorage.getItem("va-act-off")) return; } catch (e) {}

  function hace(min) {
    if (min < 60) return "hace " + min + (min === 1 ? " minuto" : " minutos");
    var h = Math.round(min / 60);
    if (h < 24) return "hace " + h + (h === 1 ? " hora" : " horas");
    var d = Math.round(h / 24);
    return "hace " + d + (d === 1 ? " día" : " días");
  }

  function mensajes(j) {
    var m = [];
    (j.compras || []).slice(0, 4).forEach(function (c) {
      m.push({ ico: "📘", txt: "Alguien compró <b></b>", dato: c.producto, sub: hace(c.hace) });
    });
    if (j.testsSemana) m.push({ ico: "🧭", txt: j.testsSemana + " personas hicieron el <b></b> esta semana", dato: "test de competencias", sub: "Es gratis · 3 minutos", href: "perfil.html" });
    if (j.visitantesHoy) m.push({ ico: "👀", txt: j.visitantesHoy + " personas visitaron la web hoy", sub: "Visión Alfa" });
    return m;
  }

  function armar() {
    var css = document.createElement("style");
    css.textContent =
      ".act{position:fixed;left:16px;bottom:16px;z-index:55;max-width:min(340px,calc(100vw - 32px));display:flex;align-items:center;gap:12px;" +
      "background:#fff;color:#16231B;border:1px solid #DAD8CF;border-radius:16px;padding:12px 40px 12px 14px;box-shadow:0 12px 30px rgba(22,35,27,.18);" +
      "font:500 14.5px/1.35 'Instrument Sans',system-ui,sans-serif;text-decoration:none;transform:translateY(140%);opacity:0;transition:transform .45s cubic-bezier(.2,.8,.2,1),opacity .45s}" +
      ".act.ver{transform:none;opacity:1}" +
      ".act-ico{flex:none;width:38px;height:38px;border-radius:50%;background:#F4F3EE;display:flex;align-items:center;justify-content:center;font-size:19px}" +
      ".act b{color:#1F3D2B}.act small{display:block;color:#6B7069;font-size:12.5px;margin-top:2px}" +
      ".act-x{position:absolute;top:4px;right:4px;width:32px;height:32px;border:0;background:none;color:#6B7069;font-size:18px;cursor:pointer;border-radius:50%}" +
      "@media (prefers-reduced-motion:reduce){.act{transition:opacity .2s;transform:none}}";
    document.head.appendChild(css);
    var caja = document.createElement("div");
    caja.className = "act"; caja.setAttribute("role", "status"); caja.setAttribute("aria-live", "polite");
    document.body.appendChild(caja);
    return caja;
  }

  function mostrar(caja, m, alTerminar) {
    caja.innerHTML = "";
    var cuerpo = document.createElement(m.href ? "a" : "div");
    if (m.href) { cuerpo.href = m.href; cuerpo.style.cssText = "color:inherit;text-decoration:none;display:flex;align-items:center;gap:12px"; }
    else cuerpo.style.cssText = "display:flex;align-items:center;gap:12px";
    var ico = document.createElement("span"); ico.className = "act-ico"; ico.textContent = m.ico;
    var t = document.createElement("span");
    var linea = document.createElement("span"); linea.innerHTML = m.txt; // plantilla fija, sin datos externos
    var b = linea.querySelector("b"); if (b) b.textContent = m.dato || "";
    var s = document.createElement("small"); s.textContent = m.sub || "";
    t.appendChild(linea); t.appendChild(s);
    cuerpo.appendChild(ico); cuerpo.appendChild(t); caja.appendChild(cuerpo);
    var x = document.createElement("button"); x.type = "button"; x.className = "act-x"; x.setAttribute("aria-label", "Cerrar"); x.textContent = "×";
    x.addEventListener("click", function () {
      caja.classList.remove("ver"); try { sessionStorage.setItem("va-act-off", "1"); } catch (e) {}
      alTerminar(true);
    });
    caja.appendChild(x);
    requestAnimationFrame(function () { caja.classList.add("ver"); });
    setTimeout(function () { caja.classList.remove("ver"); alTerminar(false); }, VISIBLE);
  }

  function iniciar() {
    fetch(URL_FN, { headers: { apikey: CLAVE } }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (!j) return;
      var lista = mensajes(j);
      if (!lista.length) return;
      var caja = armar(), i = 0, terminado = false;
      function siguiente() {
        if (terminado || i >= Math.min(MAX_POR_VISITA, lista.length) || document.hidden) return;
        mostrar(caja, lista[i++], function (cerrado) {
          if (cerrado) { terminado = true; return; }
          setTimeout(siguiente, ENTRE);
        });
      }
      setTimeout(siguiente, ESPERA_INICIAL);
    }).catch(function () {});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
