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
      var slug = btn.getAttribute("data-slug");
      if (!slug) {
        btn.disabled = false;
        return;
      }
      window.location.href = api + "/checkout/" + encodeURIComponent(slug);
    });
  });
});
