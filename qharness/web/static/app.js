const status = document.getElementById("status");
const result = document.getElementById("result");
const prompt = document.getElementById("prompt");
const strategy = document.getElementById("strategy");
const send = document.getElementById("send");

async function checkHealth() {
  try {
    const r = await fetch("/health");
    const j = await r.json();
    status.textContent = j.status === "ok" ? "在线" : "异常";
    status.className = "pill";
  } catch (e) {
    status.textContent = "离线";
    status.className = "pill";
  }
}

send.addEventListener("click", async () => {
  const text = prompt.value.trim();
  if (!text) return;
  result.textContent = "运行中…";
  try {
    const r = await fetch("/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: "qharness", messages: [{ role: "user", content: text }], strategy: strategy.value }),
    });
    const j = await r.json();
    result.textContent = j.choices?.[0]?.message?.content ?? JSON.stringify(j, null, 2);
  } catch (e) {
    result.textContent = "请求失败：" + e.message;
  }
});

checkHealth();
