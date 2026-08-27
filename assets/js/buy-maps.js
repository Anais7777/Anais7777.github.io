document.addEventListener("DOMContentLoaded", function () {
  var api =
    location.hostname === "localhost" || location.hostname === "127.0.0.1"
      ? "http://localhost:3000"
      : "https://api.scriucutolk.md";

  document.querySelectorAll(".buy-maps").forEach(function (box) {
    var btn = box.querySelector(".buy-maps-btn");
    var err = box.querySelector(".buy-maps-error");
    if (!btn || btn.dataset.buyMapsBound) return;
    btn.dataset.buyMapsBound = "1";

    btn.addEventListener("click", async function () {
      btn.disabled = true;
      if (err) err.style.display = "none";
      try {
        var res = await fetch(api + "/api/checkout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ slug: btn.getAttribute("data-slug") }),
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.message || "Checkout indisponibil");
        window.location.href = data.approvalUrl;
      } catch (e) {
        if (err) {
          err.textContent = e.message || "Nu am putut porni plata.";
          err.style.display = "block";
        }
        btn.disabled = false;
      }
    });
  });
});
