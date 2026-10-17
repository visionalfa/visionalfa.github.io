// Conexión de la web con el sistema de ventas (inicio de sesión, compras y lectura).
(function () {
  var URL_SUPABASE = "https://futhqkqfjuuemhcxzakn.supabase.co";
  var CLAVE_PUBLICA = "sb_publishable_x20gCAkWL2NsZG84wiWgGQ_hlchdMOF";

  var sb = window.supabase.createClient(URL_SUPABASE, CLAVE_PUBLICA, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: "implicit" },
  });

  async function sesion() {
    var r = await sb.auth.getSession();
    return r.data.session;
  }

  async function llamar(funcion, opciones) {
    opciones = opciones || {};
    var s = await sesion();
    var headers = { "Content-Type": "application/json", apikey: CLAVE_PUBLICA };
    if (s) headers.Authorization = "Bearer " + s.access_token;
    var r = await fetch(URL_SUPABASE + "/functions/v1/" + funcion + (opciones.query || ""), {
      method: opciones.method || "GET",
      headers: headers,
      body: opciones.body ? JSON.stringify(opciones.body) : undefined,
    });
    var datos = await r.json().catch(function () { return {}; });
    if (!r.ok) {
      var error = new Error(datos.error || "Algo salió mal. Probá de nuevo en unos minutos.");
      error.status = r.status;
      throw error;
    }
    return datos;
  }

  async function comprar(producto) {
    var s = await sesion();
    if (!s) {
      location.href = "cuenta.html?comprar=" + encodeURIComponent(producto);
      return;
    }
    var datos = await llamar("checkout", { method: "POST", body: { producto: producto } });
    location.href = datos.url;
  }

  function aviso(texto) {
    var caja = document.getElementById("va-aviso");
    if (!caja) {
      caja = document.createElement("div");
      caja.id = "va-aviso";
      caja.setAttribute("role", "status");
      caja.style.cssText =
        "position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);" +
        "max-width:calc(100% - 32px);background:#16231B;color:#F4F3EE;padding:14px 20px;border-radius:14px;" +
        "font:500 15px/1.4 'Instrument Sans',system-ui,sans-serif;box-shadow:0 12px 30px rgba(0,0,0,.25);z-index:50";
      document.body.appendChild(caja);
    }
    caja.textContent = texto;
    caja.hidden = false;
    clearTimeout(caja._t);
    caja._t = setTimeout(function () { caja.hidden = true; }, 6000);
  }

  // Cualquier botón con data-comprar="id-del-producto" inicia la compra.
  document.addEventListener("click", function (e) {
    var boton = e.target.closest("[data-comprar]");
    if (!boton) return;
    e.preventDefault();
    if (boton.getAttribute("aria-busy") === "true") return;
    var texto = boton.textContent;
    boton.setAttribute("aria-busy", "true");
    boton.textContent = "Un momento…";
    comprar(boton.dataset.comprar).catch(function (err) {
      boton.textContent = texto;
      boton.removeAttribute("aria-busy");
      aviso(err.message);
    });
  });

  window.VA = { sb: sb, sesion: sesion, llamar: llamar, comprar: comprar, aviso: aviso };
})();
