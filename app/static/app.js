const $ = (id) => document.getElementById(id);

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || res.statusText);
  return data;
}

// ---- статус конфигурации ----
(async () => {
  try {
    const h = await api("/api/health");
    const parts = [];
    parts.push(h.anthropic_configured ? "Claude ✓" : "Claude ✗ (нет ключа)");
    parts.push(h.snov_configured ? "Snov.io ✓" : "Snov.io ✗ (нет ключей)");
    $("status").textContent = parts.join("  ·  ") + `  ·  ${h.model}`;
  } catch {
    $("status").textContent = "сервер недоступен";
  }
})();

let currentCopy = null;

// ---- 1. генерация ----
$("btnGen").onclick = async () => {
  const btn = $("btnGen");
  btn.disabled = true; btn.textContent = "⏳ Claude пишет…";
  try {
    const brief = {
      product: $("product").value,
      audience: $("audience").value,
      goal: $("goal").value,
      tone: $("tone").value,
      language: $("language").value,
      sender_name: $("sender_name").value,
      num_followups: parseInt($("num_followups").value || "2", 10),
      extra_notes: $("extra_notes").value,
    };
    currentCopy = await api("/api/generate-copy", {
      method: "POST",
      body: JSON.stringify(brief),
    });
    renderDraft(currentCopy);
    $("draftCard").classList.remove("hidden");
    $("prospectsCard").classList.remove("hidden");
    $("launchCard").classList.remove("hidden");
  } catch (e) {
    alert("Ошибка: " + e.message);
  } finally {
    btn.disabled = false; btn.textContent = "✨ Сгенерировать черновик";
  }
};

function renderDraft(copy) {
  const subs = $("subjects");
  subs.innerHTML = "";
  copy.subject_variants.forEach((s) => {
    const span = document.createElement("span");
    span.className = "pill";
    span.textContent = s;
    subs.appendChild(span);
  });
  const stepsEl = $("steps");
  stepsEl.innerHTML = "";
  copy.steps.forEach((st, i) => {
    const div = document.createElement("div");
    div.className = "step";
    div.innerHTML = `
      <div class="meta">Шаг ${st.step} · задержка ${st.delay_days} дн.</div>
      <label>Тема</label>
      <input data-k="subject" data-i="${i}" value="${escapeAttr(st.subject)}" />
      <label>Текст</label>
      <textarea data-k="body" data-i="${i}">${escapeHtml(st.body)}</textarea>`;
    stepsEl.appendChild(div);
  });
  // правки синхронизируем обратно в currentCopy
  stepsEl.querySelectorAll("[data-k]").forEach((el) => {
    el.oninput = () => {
      currentCopy.steps[+el.dataset.i][el.dataset.k] = el.value;
    };
  });
}

// ---- 3. проспекты ----
$("btnProspects").onclick = async () => {
  const btn = $("btnProspects");
  btn.disabled = true;
  try {
    const prospects = parseCsv($("prospects_csv").value);
    if (!prospects.length) throw new Error("Нет получателей в CSV.");
    const out = await api("/api/prospects", {
      method: "POST",
      body: JSON.stringify({ list_name: $("list_name").value, prospects }),
    });
    show("prospectsOut", out);
    if (out.list_id) $("launch_list_id").value = out.list_id;
  } catch (e) {
    alert("Ошибка: " + e.message);
  } finally {
    btn.disabled = false;
  }
};

// ---- 4. запуск ----
$("btnLaunch").onclick = async () => {
  const btn = $("btnLaunch");
  btn.disabled = true;
  try {
    const body = {
      campaign_id: parseInt($("campaign_id").value, 10),
      list_id: $("launch_list_id").value ? parseInt($("launch_list_id").value, 10) : null,
      prospects: [],
    };
    const out = await api("/api/launch", { method: "POST", body: JSON.stringify(body) });
    show("launchOut", out);
  } catch (e) {
    alert("Ошибка: " + e.message);
  } finally {
    btn.disabled = false;
  }
};

$("btnAnalytics").onclick = async () => {
  try {
    const id = parseInt($("campaign_id").value, 10);
    show("launchOut", await api(`/api/analytics/${id}`));
  } catch (e) {
    alert("Ошибка: " + e.message);
  }
};

// ---- утилиты ----
function parseCsv(text) {
  return text
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean)
    .map((line) => {
      const [email, first_name = "", last_name = "", company = "", position = ""] =
        line.split(",").map((x) => x.trim());
      return { email, first_name, last_name, company, position };
    });
}
function show(id, data) {
  const el = $(id);
  el.textContent = JSON.stringify(data, null, 2);
  el.classList.remove("hidden");
}
function escapeHtml(s) {
  return (s || "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}
function escapeAttr(s) {
  return (s || "").replace(/"/g, "&quot;");
}
