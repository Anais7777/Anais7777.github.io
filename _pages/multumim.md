---
layout: page
title: Mulțumim
permalink: /multumim/
comments: false
---

<div id="pay-ok">
  <p class="mb-4">Plata e înregistrată. Dacă ai pus un email valid, colecția de locuri ajunge acolo în câteva minute — o deschizi direct în Google Maps.</p>
  <p>Dacă nu vezi mesajul, verifică folderul Spam. Poți scrie și din <a href="/contacte/">Contacte</a>.</p>
</div>
<div id="pay-err" style="display:none;">
  <p class="mb-4">Plata nu s-a confirmat. Nu s-a reținut nimic și nu s-a trimis colecția. Poți relua cumpărarea de pe pagina destinației.</p>
  <p>Dacă totuși ți s-au tăiat banii, scrie-mi din <a href="/contacte/">Contacte</a>.</p>
</div>
<p><a href="/">Înapoi la scriucutolk</a></p>
<script>
  (function () {
    var s = new URLSearchParams(location.search).get("status");
    if (s && s !== "ok") {
      var ok = document.getElementById("pay-ok");
      var err = document.getElementById("pay-err");
      if (ok) ok.style.display = "none";
      if (err) err.style.display = "block";
      document.title = "Plată eșuată";
    }
  })();
</script>
