/* =====================================================================
   주식 AI 실험실 — stock_lab.js
   ===================================================================== */

// ── 상수 ──────────────────────────────────────────────────────────────
const FEATURE_NAMES = {
  ret:       "당일 수익률",
  ret_5:     "5일 수익률",
  ma5:       "5일 이동평균",
  ma20:      "20일 이동평균",
  vol_ratio: "거래량 비율",
};

const MODEL_INFO = {
  logistic: { name: "로지스틱 회귀",    emoji: "📏", desc: "직선으로 구분 · 해석 쉬움",       color: "blue" },
  rf:       { name: "랜덤 포레스트",    emoji: "🌲", desc: "여러 트리의 다수결",               color: "green" },
  nn:       { name: "신경망",           emoji: "🧠", desc: "뇌 구조 흉내 · 복잡 패턴",        color: "purple" },
  gbm:      { name: "그래디언트 부스팅", emoji: "🚀", desc: "실수 보완하며 점점 발전",         color: "orange" },
};

const COLORS = {
  blue:   { btn: "bg-blue-900/40 hover:bg-blue-800/50 border-blue-800/60 text-blue-300",   sel: "bg-blue-600/20 border-blue-500 text-white" },
  green:  { btn: "bg-green-900/40 hover:bg-green-800/50 border-green-800/60 text-green-300", sel: "bg-green-600/20 border-green-500 text-white" },
  purple: { btn: "bg-purple-900/40 hover:bg-purple-800/50 border-purple-800/60 text-purple-300", sel: "bg-purple-600/20 border-purple-500 text-white" },
  orange: { btn: "bg-orange-900/40 hover:bg-orange-800/50 border-orange-800/60 text-orange-300", sel: "bg-orange-600/20 border-orange-500 text-white" },
};

// 삼성전자 샘플 (60 거래일, 2024-01-02 기준)
const SAMPLE_DATA = {
  samsung: { basePrice: 74000, baseVol: 12000000, vol: 0.012 },
  kakao:   { basePrice: 52000, baseVol: 6000000,  vol: 0.018 },
  naver:   { basePrice: 210000, baseVol: 3000000, vol: 0.010 },
};

const PAGE_QUERY = new URLSearchParams(window.location.search);
const LAB_PRESETS = {
  chapter06: {
    title: "chapter06 · 로지스틱 회귀 웹앱 실습",
    desc: "확률 기반 분류 흐름을 확인할 수 있도록 로지스틱 회귀와 삼성전자 샘플을 미리 준비했어요.",
    model: "logistic",
    sample: "samsung",
  },
  chapter08: {
    title: "chapter08 · 랜덤포레스트 웹앱 실습",
    desc: "트리 기반 앙상블 결과를 바로 비교할 수 있도록 랜덤포레스트와 삼성전자 샘플을 불러왔어요.",
    model: "rf",
    sample: "samsung",
  },
  chapter10: {
    title: "chapter10 · 평가 지표 웹앱 실습",
    desc: "정확도, AUC, 정밀도, 수익률을 한 화면에서 읽을 수 있도록 기본 샘플을 준비했어요.",
    model: "rf",
    sample: "samsung",
  },
  chapter21: {
    title: "chapter21 · 신경망 웹앱 실습",
    desc: "신경망(MLP) 모델이 실제 주가 입력을 어떻게 해석하는지 바로 체험할 수 있어요.",
    model: "nn",
    sample: "samsung",
  },
  chapter107: {
    title: "chapter107 · 백테스트 지표 웹앱 실습",
    desc: "포트폴리오 곡선과 전략 수익률을 함께 읽으며 성과지표를 연결해보세요.",
    model: "rf",
    sample: "samsung",
  },
  chapter112: {
    title: "chapter112 · 미니 프로젝트 웹앱 실습",
    desc: "같은 데이터에서 여러 모델을 바꿔가며 전체 파이프라인을 비교할 수 있어요.",
    model: "rf",
    sample: "samsung",
  },
};

// ── 상태 ──────────────────────────────────────────────────────────────
let selectedModel    = "rf";
let lastResult       = null;
let portfolioChart   = null;
let importanceChart  = null;

// ── 초기화 ────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  buildModelButtons();
  initGrid(10);
  applyPresetFromQuery();
  setupEventListeners();
  checkOllama();
});

// ── 모델 버튼 생성 ────────────────────────────────────────────────────
function buildModelButtons() {
  const container = document.getElementById("model-buttons");
  container.innerHTML = "";
  Object.entries(MODEL_INFO).forEach(([key, info]) => {
    const btn = document.createElement("button");
    btn.dataset.model = key;
    btn.className = `model-btn flex items-start gap-2 p-3 rounded-xl border-2 transition text-left ${
      key === selectedModel
        ? COLORS[info.color].sel
        : COLORS[info.color].btn
    }`;
    btn.innerHTML = `
      <span class="text-xl flex-none mt-0.5">${info.emoji}</span>
      <span>
        <span class="block font-semibold text-sm">${info.name}</span>
        <span class="block text-xs opacity-70 mt-0.5">${info.desc}</span>
      </span>`;
    btn.addEventListener("click", () => selectModel(key));
    container.appendChild(btn);
  });
}

function selectModel(key) {
  selectedModel = key;
  document.querySelectorAll(".model-btn").forEach(btn => {
    const k     = btn.dataset.model;
    const info  = MODEL_INFO[k];
    const isSelected = k === key;
    btn.className = `model-btn flex items-start gap-2 p-3 rounded-xl border-2 transition text-left ${
      isSelected ? COLORS[info.color].sel : COLORS[info.color].btn
    }`;
  });
}

function applyPresetFromQuery() {
  const preset = LAB_PRESETS[PAGE_QUERY.get("chapter")] || {};
  const model  = PAGE_QUERY.get("model") || preset.model;
  const sample = PAGE_QUERY.get("sample") || preset.sample;
  const title  = preset.title || PAGE_QUERY.get("title");
  const desc   = preset.desc || PAGE_QUERY.get("desc");

  if (model && MODEL_INFO[model]) selectModel(model);
  if (sample && SAMPLE_DATA[sample]) loadSample(sample);

  if (title || desc) {
    const banner = document.getElementById("chapter-lab-banner");
    document.getElementById("chapter-lab-title").textContent = title || "웹앱 실습 프리셋";
    document.getElementById("chapter-lab-desc").textContent  = desc || "";
    banner.classList.remove("hidden");
  }
}

// ── 그리드 관리 ───────────────────────────────────────────────────────
function initGrid(count = 10) {
  document.getElementById("data-grid").innerHTML = "";
  for (let i = 0; i < count; i++) addGridRow();
}

function addGridRow(date = "", close = "", volume = "") {
  const tbody  = document.getElementById("data-grid");
  const rowNum = tbody.querySelectorAll("tr").length + 1;
  const tr     = document.createElement("tr");
  tr.className = "border-b border-slate-800/80 hover:bg-slate-800/20 group";
  tr.innerHTML = `
    <td class="w-7 px-2 py-0.5 text-center text-slate-600 text-xs select-none border-r border-slate-800">${rowNum}</td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="date" value="${date}" class="grid-input" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${close}" placeholder="60000" class="grid-input" min="0" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${volume}" placeholder="10000000" class="grid-input" min="0" tabindex="0"/>
    </td>
    <td class="w-7 px-1 py-0.5 text-center">
      <button onclick="removeGridRow(this)"
        class="opacity-0 group-hover:opacity-100 text-slate-600 hover:text-red-400 text-base leading-none transition">×</button>
    </td>`;
  tbody.appendChild(tr);
  updateRowCount();
  return tr;
}

function removeGridRow(btn) {
  const rows = document.querySelectorAll("#data-grid tr");
  if (rows.length <= 1) return;
  btn.closest("tr").remove();
  renumberGrid();
  updateRowCount();
}

function renumberGrid() {
  document.querySelectorAll("#data-grid tr").forEach((tr, i) => {
    tr.querySelector("td:first-child").textContent = i + 1;
  });
}

function clearGrid() {
  document.getElementById("data-grid").innerHTML = "";
  initGrid(10);
}

function updateRowCount() {
  const n = document.querySelectorAll("#data-grid tr").length;
  document.getElementById("row-count").textContent = `${n}행`;
}

function getGridData() {
  const rows = [];
  document.querySelectorAll("#data-grid tr").forEach(tr => {
    const inputs  = tr.querySelectorAll("input");
    const date    = inputs[0].value.trim();
    const close   = parseFloat(inputs[1].value);
    const volume  = parseFloat(inputs[2].value);
    if (date && !isNaN(close) && !isNaN(volume) && close > 0 && volume > 0) {
      rows.push({ date, close, volume });
    }
  });
  return rows;
}

// ── 샘플 데이터 ───────────────────────────────────────────────────────
function loadSample(stockKey) {
  const cfg   = SAMPLE_DATA[stockKey];
  if (!cfg) return;
  const data  = generateSampleData(cfg.basePrice, cfg.baseVol, cfg.vol, 60);
  const tbody = document.getElementById("data-grid");
  tbody.innerHTML = "";
  data.forEach(r => addGridRow(r.date, r.close, r.volume));
  updateRowCount();
}

function generateSampleData(basePrice, baseVol, volatility, days) {
  const data   = [];
  let price    = basePrice;
  const start  = new Date("2024-01-02");
  const rng    = mulberry32(42);

  for (let i = 0; i < days; i++) {
    // 영업일 계산 (간단히 주말 포함)
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    const dateStr = d.toISOString().split("T")[0];

    const change = (rng() - 0.48) * volatility;
    price        = Math.max(price * (1 + change), basePrice * 0.4);
    const vol    = Math.round(baseVol * (0.5 + rng() * 1.5));
    data.push({ date: dateStr, close: Math.round(price), volume: vol });
  }
  return data;
}

// 재현 가능한 간단한 난수 생성기 (Mulberry32)
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = t + Math.imul(t ^ (t >>> 7), 61 | t) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ── CSV 불러오기 ──────────────────────────────────────────────────────
function setupEventListeners() {
  // CSV
  document.getElementById("csv-upload").addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      const lines  = ev.target.result.trim().split("\n");
      const tbody  = document.getElementById("data-grid");
      tbody.innerHTML = "";
      let loaded   = 0;
      lines.forEach((line, i) => {
        if (i === 0 && isNaN(parseFloat(line.split(",")[1]))) return; // 헤더 스킵
        const parts = line.split(",");
        if (parts.length >= 3) {
          addGridRow(parts[0].trim(), parts[1].trim(), parts[2].trim());
          loaded++;
        }
      });
      updateRowCount();
      if (loaded === 0) alert("CSV 파싱 실패. 헤더: date,close,volume 형식인지 확인하세요.");
    };
    reader.readAsText(file);
    this.value = "";
  });

  // 분석 버튼
  document.getElementById("analyze-btn").addEventListener("click", runAnalysis);

  // 챗봇 전송
  document.getElementById("chat-send").addEventListener("click", () => {
    const input = document.getElementById("chat-input");
    const msg   = input.value.trim();
    if (msg) sendChat(msg);
  });
  document.getElementById("chat-input").addEventListener("keydown", e => {
    if (e.key === "Enter") {
      const msg = e.target.value.trim();
      if (msg) sendChat(msg);
    }
  });

  // 빠른 질문 칩
  document.querySelectorAll(".quick-q").forEach(btn => {
    btn.addEventListener("click", () => sendChat(btn.textContent.trim()));
  });
}

// ── 분석 실행 ─────────────────────────────────────────────────────────
async function runAnalysis() {
  const rows = getGridData();
  if (rows.length < 25) {
    showAlert(`유효한 행이 ${rows.length}개입니다. 최소 25행 이상 필요해요.`);
    return;
  }

  const btn     = document.getElementById("analyze-btn");
  const btnText = document.getElementById("analyze-btn-text");
  btn.disabled  = true;
  btnText.textContent = "분석 중…";

  try {
    const resp = await fetch("/api/stock/analyze", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ rows, model: selectedModel }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: "서버 오류" }));
      throw new Error(err.detail || "분석 실패");
    }

    const result  = await resp.json();
    lastResult    = result;
    displayResults(result);

  } catch (err) {
    showAlert(`분석 오류: ${err.message}`);
  } finally {
    btn.disabled = false;
    btnText.textContent = "AI 분석 시작!";
  }
}

// ── 결과 표시 ─────────────────────────────────────────────────────────
function displayResults(r) {
  document.getElementById("result-placeholder").classList.add("hidden");

  // 헤더
  setVisible("result-header", true);
  const modelInfo = MODEL_INFO[r.model_key] || { emoji: "🤖" };
  document.getElementById("result-model-emoji").textContent = modelInfo.emoji;
  document.getElementById("result-model-name").textContent  = r.model_name;
  document.getElementById("result-data-info").textContent   = `학습 ${r.n_train}행 · 테스트 ${r.n_test}행`;

  // 지표 카드
  setVisible("metrics-cards", true);
  document.getElementById("metric-acc").textContent  = pct(r.accuracy);
  document.getElementById("metric-auc").textContent  = r.auc.toFixed(3);
  document.getElementById("metric-prec").textContent = pct(r.precision);
  colorize("metric-acc",  r.accuracy  >= 0.55 ? "text-green-400"  : "text-yellow-400");
  colorize("metric-auc",  r.auc       >= 0.55 ? "text-blue-400"   : "text-yellow-400");
  colorize("metric-prec", r.precision >= 0.55 ? "text-purple-400" : "text-yellow-400");

  // 수익률 카드
  setVisible("return-cards", true);
  const portEl = document.getElementById("metric-port");
  const bhEl   = document.getElementById("metric-bh");
  portEl.textContent = signedPct(r.portfolio_return);
  bhEl.textContent   = signedPct(r.buyhold_return);
  portEl.className   = `text-xl font-bold ${r.portfolio_return > r.buyhold_return ? "text-green-400" : r.portfolio_return > 0 ? "text-yellow-400" : "text-red-400"}`;

  // 차트들
  setVisible("portfolio-card",   true);
  setVisible("importance-card",  true);
  setVisible("signals-card",     true);

  drawPortfolioChart(r.portfolio, r.buyhold, r.model_name);
  drawImportanceChart(r.feature_importance);
  drawSignalsTable(r.signals);

  // 챗봇 초기 메시지
  clearChat();
  const bestFeat = Object.entries(r.feature_importance).sort((a, b) => b[1] - a[1])[0];
  const bestName = bestFeat ? (FEATURE_NAMES[bestFeat[0]] || bestFeat[0]) : "";
  addChatBubble("ai",
    `${r.model_name} 분석 완료! ` +
    `정확도 ${pct(r.accuracy)}, AUC ${r.auc.toFixed(3)}. ` +
    (bestName ? `가장 중요한 요소는 "${bestName}"이었어요. ` : "") +
    `전략 수익률 ${signedPct(r.portfolio_return)}. 궁금한 점을 질문해보세요!`
  );
}

// ── 차트 ──────────────────────────────────────────────────────────────
function drawPortfolioChart(portfolio, buyhold, modelName) {
  if (portfolioChart) { portfolioChart.destroy(); portfolioChart = null; }
  const ctx    = document.getElementById("portfolio-chart").getContext("2d");
  const labels = portfolio.map((_, i) => `${i}일`);

  portfolioChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label:           modelName,
          data:            portfolio,
          borderColor:     "#6366f1",
          backgroundColor: "rgba(99,102,241,0.08)",
          tension:         0.3,
          fill:            true,
          pointRadius:     0,
          borderWidth:     2,
        },
        {
          label:       "전량 보유",
          data:        buyhold,
          borderColor: "#64748b",
          borderDash:  [5, 4],
          tension:     0.3,
          pointRadius: 0,
          borderWidth: 1.5,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { color: "#94a3b8", font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.dataset.label}: ${(ctx.raw * 100 - 100).toFixed(2)}%`,
          },
        },
      },
      scales: {
        x: { ticks: { color: "#64748b", font: { size: 10 }, maxTicksLimit: 8 }, grid: { color: "#1e293b" } },
        y: { ticks: { color: "#64748b", font: { size: 10 }, callback: v => `${(v * 100 - 100).toFixed(1)}%` }, grid: { color: "#1e293b" } },
      },
    },
  });
}

function drawImportanceChart(featImp) {
  if (importanceChart) { importanceChart.destroy(); importanceChart = null; }
  const ctx    = document.getElementById("importance-chart").getContext("2d");
  const sorted = Object.entries(featImp).sort((a, b) => b[1] - a[1]);
  const labels = sorted.map(([k]) => FEATURE_NAMES[k] || k);
  const values = sorted.map(([, v]) => v);
  const maxVal = Math.max(...values, 0.001);

  importanceChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label:           "중요도",
        data:            values,
        backgroundColor: values.map(v => v === maxVal ? "rgba(99,102,241,0.7)" : "rgba(51,65,85,0.7)"),
        borderColor:     values.map(v => v === maxVal ? "#6366f1" : "#475569"),
        borderWidth:     1,
        borderRadius:    4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#64748b", font: { size: 10 } }, grid: { color: "#1e293b" } },
        y: { ticks: { color: "#94a3b8", font: { size: 11 } } },
      },
    },
  });
}

function drawSignalsTable(signals) {
  const tbody = document.getElementById("signals-tbody");
  tbody.innerHTML = "";
  signals.forEach(s => {
    const tr  = document.createElement("tr");
    tr.className = "border-b border-slate-700/40";
    const signalClass  = s.signal === "매수"
      ? "bg-green-900/50 text-green-300 border border-green-800/50"
      : "bg-slate-700/50 text-slate-400";
    const actualClass  = s.actual === "상승" ? "text-green-400" : "text-red-400";
    const correctIcon  = s.correct ? "✓" : "✗";
    const correctClass = s.correct ? "text-green-400" : "text-red-400";
    tr.innerHTML = `
      <td class="py-1.5 pr-3 text-slate-400">${s.date}</td>
      <td class="py-1.5 pr-3 text-right font-mono">${s.close.toLocaleString()}</td>
      <td class="py-1.5 pr-3 text-center">
        <span class="px-2 py-0.5 rounded-full text-xs ${signalClass}">${s.signal}</span>
      </td>
      <td class="py-1.5 pr-3 text-center font-mono">${s.prob}%</td>
      <td class="py-1.5 pr-3 text-center ${actualClass}">${s.actual}</td>
      <td class="py-1.5 text-center font-bold ${correctClass}">${correctIcon}</td>`;
    tbody.appendChild(tr);
  });
}

// ── 챗봇 ──────────────────────────────────────────────────────────────
function clearChat() {
  document.getElementById("chat-history").innerHTML = "";
}

function addChatBubble(role, text) {
  const history = document.getElementById("chat-history");
  const wrap    = document.createElement("div");
  wrap.className = `flex ${role === "user" ? "justify-end" : "justify-start"}`;
  const bubble   = document.createElement("div");
  bubble.className = `max-w-xs px-3 py-2 text-xs leading-relaxed ${
    role === "user" ? "chat-bubble-user text-white" : "chat-bubble-ai text-slate-200"
  }`;
  bubble.textContent = text;
  wrap.appendChild(bubble);
  history.appendChild(wrap);
  history.scrollTop = history.scrollHeight;
}

let chatTyping = null;

async function sendChat(message) {
  if (!message) return;
  if (!lastResult) {
    addChatBubble("ai", "먼저 AI 분석을 실행해주세요!");
    return;
  }

  document.getElementById("chat-input").value = "";
  addChatBubble("user", message);

  // 타이핑 표시
  const history = document.getElementById("chat-history");
  chatTyping    = document.createElement("div");
  chatTyping.className = "flex justify-start";
  chatTyping.innerHTML = `<div class="chat-bubble-ai px-3 py-2 text-xs text-slate-500">🤖 생각 중…</div>`;
  history.appendChild(chatTyping);
  history.scrollTop = history.scrollHeight;

  try {
    const resp = await fetch("/api/chat", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ message, context: lastResult }),
    });
    chatTyping.remove();
    chatTyping = null;

    if (resp.ok) {
      const data = await resp.json();
      addChatBubble("ai", data.response);
    } else {
      addChatBubble("ai", "응답을 가져올 수 없습니다.");
    }
  } catch {
    if (chatTyping) { chatTyping.remove(); chatTyping = null; }
    addChatBubble("ai", "연결 오류가 발생했습니다.");
  }
}

// ── Ollama 상태 확인 ──────────────────────────────────────────────────
async function checkOllama() {
  try {
    const resp = await fetch("/api/ollama/status");
    const data = await resp.json();
    updateOllamaBadge(data.status === "online", data.models || []);
  } catch {
    updateOllamaBadge(false, []);
  }
}

function updateOllamaBadge(online, models) {
  const dot   = document.getElementById("ollama-dot");
  const label = document.getElementById("ollama-label");
  const badge = document.getElementById("ollama-badge");
  const chatBadge = document.getElementById("ollama-chat-badge");

  if (online) {
    dot.className   = "w-1.5 h-1.5 rounded-full bg-green-400 inline-block";
    label.textContent = `Ollama 연결됨 ${models.length > 0 ? `(${models[0]})` : ""}`;
    badge.className   = badge.className.replace("text-slate-400", "text-green-300").replace("border-slate-700", "border-green-800/50");
    chatBadge.textContent = "AI 설명 사용 가능";
    chatBadge.className = "text-xs px-2 py-0.5 rounded-full bg-green-900/30 text-green-400 border border-green-800/50";
  } else {
    dot.className   = "w-1.5 h-1.5 rounded-full bg-yellow-500 inline-block";
    label.textContent = "Ollama 오프라인";
    chatBadge.textContent = "규칙 기반 설명 모드";
    chatBadge.className = "text-xs px-2 py-0.5 rounded-full bg-yellow-900/30 text-yellow-500 border border-yellow-800/50";
  }
}

// ── 유틸 ──────────────────────────────────────────────────────────────
function setVisible(id, show) {
  document.getElementById(id).classList.toggle("hidden", !show);
}

function colorize(id, cls) {
  const el = document.getElementById(id);
  el.className = el.className.replace(/text-\w+-\d+/g, "").trim() + " " + cls;
}

function pct(v) { return `${(v * 100).toFixed(1)}%`; }

function signedPct(v) { return `${v >= 0 ? "+" : ""}${v.toFixed(2)}%`; }

function showAlert(msg) {
  alert(msg);
}
