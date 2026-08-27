// Proxy spre api.scriucutolk.md — păstrează URL-ul vechi /api/submit-contact
const API =
  process.env.CONTACT_API_URL || "https://api.scriucutolk.md/api/contact";

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { name, _replyto, email, message } = req.body || {};
    const response = await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        email: email || _replyto,
        _replyto,
        message,
      }),
    });

    const data = await response.json().catch(() => ({}));
    return res.status(response.status).json(data);
  } catch (error) {
    console.error("contact proxy", error);
    return res.status(502).json({
      error: "PROXY_FAILED",
      message: "Nu am putut trimite mesajul. Încearcă din nou.",
    });
  }
};
