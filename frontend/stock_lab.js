/* =====================================================================
   주식 AI 실험실 — stock_lab.js
   ===================================================================== */

// ── 상수 ──────────────────────────────────────────────────────────────
const FEATURE_NAMES = {
  ret:       "당일 수익률",
  ret_5:     "5일 수익률",
  ma5_gap:   "5일 이동평균 괴리",
  ma20_gap:  "20일 이동평균 괴리",
  vol_ratio: "거래량 비율",
  range_pct: "고저 범위",
  body_pct:  "캔들 몸통 비율",
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
  chapter04: {
    title: "docs/04 · 부스팅 웹앱 실습",
    desc: "그래디언트 부스팅(GBM)으로 앞 모델의 실수를 뒤 모델이 고치는 흐름을 직접 실행해볼 수 있어요.",
    model: "gbm",
    sample: "samsung",
  },
  chapter09: {
    title: "chapter09 · 군집화 개념 웹앱 실습",
    desc: "지도학습, 비지도학습, 레이블, K-Means 군집화를 작은 데이터셋으로 직접 비교해볼 수 있어요.",
    sample: "samsung",
    concept: "clustering",
  },
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
    neuron: "cost",
  },
  chapter107: {
    title: "chapter107 · 백테스트 지표 웹앱 실습",
    desc: "포트폴리오 곡선과 전략 수익률을 함께 읽으며 성과지표를 연결해보세요.",
    model: "rf",
    sample: "samsung",
  },
  chapter112: {
    title: "chapter112 · 미니 프로젝트 웹앱 실습",
    desc: "KRX 티커(.KS/.KQ)로 준비한 CSV를 올려 같은 데이터에서 여러 모델을 비교해보세요.",
    model: "rf",
    sample: "samsung",
  },
};

const CONCEPT_MODE_INFO = {
  supervised: {
    label: "지도학습",
    title: "지도학습: 정답을 보면서 배우기",
    summary: "지도학습은 입력 데이터와 함께 정답 레이블을 같이 보여주고 학습하는 방식입니다. 아래 표에서 마지막 열이 바로 정답입니다.",
    tip: "회귀와 분류는 대표적인 지도학습입니다. 즉, '얼마다?' 또는 '무엇인가?'를 정답과 함께 배우는 문제예요.",
    badges: ["정답 있음", "레이블 사용", "예측 문제"],
    chartCaption: "초록/빨강 점은 이미 정답이 붙어 있는 데이터입니다. 모델은 이런 데이터를 보고 규칙을 배웁니다.",
  },
  unsupervised: {
    label: "비지도학습",
    title: "비지도학습: 정답 없이 구조 찾기",
    summary: "비지도학습은 정답 레이블 없이 시작합니다. 그래서 컴퓨터는 '무엇이 비슷한가?'를 먼저 살펴보며 무리나 패턴을 찾습니다.",
    tip: "군집화는 비지도학습의 대표 예시입니다. 정답 맞히기보다 데이터 지도를 그리는 느낌에 가깝습니다.",
    badges: ["정답 없음", "패턴 탐색", "무리 찾기"],
    chartCaption: "모든 점을 같은 색으로 보면 정답은 보이지 않습니다. 지금은 '비슷한 점이 어디 모여 있나?'만 보는 단계예요.",
  },
  label: {
    label: "레이블",
    title: "레이블: 데이터에 붙은 정답 이름표",
    summary: "레이블은 데이터 한 줄마다 붙는 정답 이름표입니다. 지도학습에서는 이 열을 보고 모델이 '이 입력이면 어떤 답인가'를 배웁니다.",
    tip: "예를 들어 '상승/하락'은 분류용 레이블이고, '내일 종가' 같은 숫자는 회귀용 정답이라고 생각하면 쉽습니다.",
    badges: ["정답 열", "이름표", "지도학습 핵심"],
    chartCaption: "차트에서는 점 색이 레이블 역할을 합니다. 표에서는 마지막 열이 레이블이라는 점에 집중해보세요.",
  },
  clustering: {
    label: "군집화",
    title: "군집화: 비슷한 점끼리 자동으로 묶기",
    summary: "군집화는 정답 레이블 없이 비슷한 데이터끼리 묶는 방법입니다. 아래 슬라이더로 K를 바꾸면 같은 데이터도 다른 방식으로 그룹이 나뉩니다.",
    tip: "K가 작으면 큰 무리 몇 개로, K가 크면 더 잘게 나뉩니다. 군집화 결과는 정답이라기보다 해석의 출발점입니다.",
    badges: ["K-Means", "비지도학습", "자동 그룹화"],
    chartCaption: "군집화는 정답을 맞히지 않습니다. 대신 가까운 점끼리 묶어 '이 데이터는 몇 개 무리로 보이는가?'를 보여줍니다.",
  },
};

const CONCEPT_POINTS = [
  { name: "A전자", ret5: 7.4, vol: 8.2, label: "상승" },
  { name: "B반도체", ret5: 6.5, vol: 7.4, label: "상승" },
  { name: "C플랫폼", ret5: 5.8, vol: 6.9, label: "상승" },
  { name: "D소프트", ret5: 4.9, vol: 6.1, label: "상승" },
  { name: "E보험", ret5: 1.8, vol: 2.8, label: "상승" },
  { name: "F은행", ret5: 1.1, vol: 2.1, label: "상승" },
  { name: "G유틸", ret5: -0.6, vol: 1.9, label: "하락" },
  { name: "H통신", ret5: -1.0, vol: 2.4, label: "하락" },
  { name: "I바이오", ret5: -5.3, vol: 8.0, label: "하락" },
  { name: "J게임", ret5: -4.7, vol: 8.6, label: "하락" },
  { name: "K2차전지", ret5: -3.9, vol: 6.8, label: "하락" },
  { name: "L화학", ret5: -3.1, vol: 6.0, label: "하락" },
];

const CONCEPT_CLUSTER_COLORS = ["#6366f1", "#10b981", "#f59e0b", "#ec4899"];

const NEURON_FOCUS_INFO = {
  weighted_sum: {
    label: "가중합",
    title: "가중합: 입력마다 중요도를 곱해서 더한 값",
    summary: "가중합은 뉴런이 가장 먼저 만드는 점수입니다. 각 입력에 가중치를 곱한 뒤 모두 더해서 '현재 입력이 얼마나 강한가?'를 계산합니다.",
    tip: "가중치가 크면 그 입력을 더 중요하게 본다는 뜻입니다. 같은 입력이라도 가중치가 달라지면 결과가 크게 달라집니다.",
  },
  bias: {
    label: "편향",
    title: "편향: 판단 기준을 옮기는 보정값",
    summary: "편향은 가중합에 마지막으로 더하는 값입니다. 편향이 있으면 같은 가중합이라도 더 쉽게 상승 쪽 또는 하락 쪽으로 기울 수 있습니다.",
    tip: "편향은 '기본 점수' 같은 역할을 합니다. 입력이 같아도 편향이 바뀌면 최종 판단이 달라질 수 있어요.",
  },
  sigmoid: {
    label: "시그모이드",
    title: "시그모이드: z를 0~1 사이 값으로 바꾸는 함수",
    summary: "시그모이드 함수는 선형변환 결과 z를 0과 1 사이 값으로 바꿔줍니다. 그래서 분류 문제에서 확률처럼 읽기 쉬운 출력이 됩니다.",
    tip: "z가 크면 1에 가까워지고, z가 작으면 0에 가까워집니다. z=0이면 시그모이드 값은 0.5입니다.",
  },
  activation: {
    label: "활성화 함수",
    title: "활성화 함수: 뉴런 출력 모양을 바꾸는 함수",
    summary: "활성화 함수는 선형변환 결과를 다음 층에 넘기기 전에 모양을 바꿔주는 함수입니다. 신경망이 복잡한 비선형 패턴을 배우게 해주는 핵심 역할입니다.",
    tip: "이 실습은 sigmoid를 사용하지만, 실제 은닉층에서는 ReLU나 tanh도 자주 사용합니다.",
  },
  error: {
    label: "오차",
    title: "오차: 예측과 정답의 차이",
    summary: "오차는 예측값이 실제 정답과 얼마나 다른지 보여주는 값입니다. 부호는 방향을, 크기는 얼마나 틀렸는지를 알려줍니다.",
    tip: "예측이 정답보다 작으면 음수, 크면 양수입니다. 역전파는 이 오차를 바탕으로 가중치를 수정합니다.",
  },
  cost: {
    label: "비용",
    title: "비용: 오차를 한 숫자로 요약한 값",
    summary: "비용은 오차를 바탕으로 모델이 전체적으로 얼마나 틀렸는지 나타내는 값입니다. 학습은 보통 이 비용을 줄이는 방향으로 진행됩니다.",
    tip: "이 실습에서는 가장 단순한 제곱 오차 예시를 보여줍니다. 실제 분류 문제에서는 크로스 엔트로피 같은 손실도 자주 씁니다.",
  },
};

// ── 상태 ──────────────────────────────────────────────────────────────
let selectedModel    = "rf";
let lastResult       = null;
let portfolioChart   = null;
let importanceChart  = null;
let candleChart      = null;
let labNNViz         = null;
let conceptChart     = null;
let conceptMode      = "supervised";
let neuronChart      = null;
let neuronFocus      = "weighted_sum";
let currentAssetLabel = "직접 입력 OHLCV";

// ── 초기화 ────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  buildModelButtons();
  initGrid(10);
  initConceptLab();
  initNeuronLab();
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
  const chapterKey = PAGE_QUERY.get("chapter");
  const preset = chapterKey && Object.prototype.hasOwnProperty.call(LAB_PRESETS, chapterKey)
    ? LAB_PRESETS[chapterKey]
    : {};
  const assistant = PAGE_QUERY.get("assistant");
  const company = PAGE_QUERY.get("company");
  const question = PAGE_QUERY.get("query");
  const model  = PAGE_QUERY.get("model") || preset.model;
  const sample = PAGE_QUERY.get("sample") || preset.sample;
  const dataset = PAGE_QUERY.get("dataset");
  const concept = PAGE_QUERY.get("concept") || preset.concept;
  const neuron = PAGE_QUERY.get("neuron") || preset.neuron;
  let title  = preset.title || PAGE_QUERY.get("title");
  let desc   = preset.desc || PAGE_QUERY.get("desc");

  if (assistant && company) {
    title = title || `AI 길잡이 · ${company} 분석 실습`;
    desc = desc || `${company} 관련 질문 "${question || ''}"을(를) 바탕으로 신호와 확률을 먼저 살펴볼 수 있는 실습 화면으로 들어왔어요.`;
  }

  if (model && MODEL_INFO[model]) selectModel(model);
  if (dataset) {
    loadBuiltinDataset(dataset);
  } else if (sample && SAMPLE_DATA[sample]) {
    loadSample(sample);
  }
  if (concept && CONCEPT_MODE_INFO[concept]) setConceptMode(concept);
  if (neuron && NEURON_FOCUS_INFO[neuron]) setNeuronFocus(neuron);

  if (title || desc) {
    const banner = document.getElementById("chapter-lab-banner");
    document.getElementById("chapter-lab-title").textContent = title || "웹앱 실습 프리셋";
    document.getElementById("chapter-lab-desc").textContent  = desc || "";
    banner.classList.remove("hidden");
  }
}

// ── 개념 실습 ─────────────────────────────────────────────────────────
function initConceptLab() {
  buildConceptModeButtons();

  const kInput = document.getElementById("concept-k");
  const kValue = document.getElementById("concept-k-value");
  const runBtn = document.getElementById("concept-run-btn");

  kInput.addEventListener("input", () => {
    kValue.textContent = kInput.value;
    if (conceptMode === "clustering") renderConceptLab();
  });
  runBtn.addEventListener("click", () => renderConceptLab());

  renderConceptLab();
}

function buildConceptModeButtons() {
  const wrap = document.getElementById("concept-mode-buttons");
  wrap.innerHTML = "";

  Object.entries(CONCEPT_MODE_INFO).forEach(([key, info]) => {
    const btn = document.createElement("button");
    btn.dataset.conceptMode = key;
    btn.className = "concept-mode-btn px-3 py-1.5 rounded-full border text-xs font-semibold transition";
    btn.textContent = info.label;
    btn.addEventListener("click", () => setConceptMode(key));
    wrap.appendChild(btn);
  });

  updateConceptModeButtons();
}

function setConceptMode(mode) {
  if (!CONCEPT_MODE_INFO[mode]) return;
  conceptMode = mode;
  updateConceptModeButtons();
  renderConceptLab();
}

function updateConceptModeButtons() {
  document.querySelectorAll(".concept-mode-btn").forEach(btn => {
    const active = btn.dataset.conceptMode === conceptMode;
    btn.className = `concept-mode-btn px-3 py-1.5 rounded-full border text-xs font-semibold transition ${
      active
        ? "bg-indigo-600/20 border-indigo-500 text-indigo-200"
        : "bg-slate-900 border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
    }`;
  });
}

function renderConceptLab() {
  const info = CONCEPT_MODE_INFO[conceptMode];
  const isClustering = conceptMode === "clustering";
  const k = parseInt(document.getElementById("concept-k").value, 10);
  const clustered = isClustering ? runMiniKMeans(CONCEPT_POINTS, k) : [];

  document.getElementById("concept-title").textContent = info.title;
  document.getElementById("concept-summary").textContent = info.summary;
  document.getElementById("concept-tip").textContent = info.tip;
  document.getElementById("concept-chart-caption").textContent = info.chartCaption;
  document.getElementById("concept-k-wrap").style.display = isClustering ? "flex" : "none";
  document.getElementById("concept-target-header").textContent =
    conceptMode === "label" ? "레이블 = 정답" : isClustering ? "군집 결과" : "레이블";
  document.getElementById("concept-k-value").textContent = String(k);

  const badgeWrap = document.getElementById("concept-badges");
  const badges = isClustering ? [...info.badges, `K=${k}`] : info.badges;
  badgeWrap.innerHTML = badges.map(text => (
    `<span class="px-2.5 py-1 rounded-full bg-slate-900 border border-slate-700 text-[11px] text-slate-300">${text}</span>`
  )).join("");

  renderConceptTable(clustered);
  renderConceptChart(clustered);
}

function renderConceptTable(clustered) {
  const tbody = document.getElementById("concept-table-body");
  tbody.innerHTML = "";

  CONCEPT_POINTS.forEach((point, idx) => {
    const tr = document.createElement("tr");
    tr.className = "border-b border-slate-800/70";

    let targetHtml = `<span class="text-slate-600">?</span>`;
    if (conceptMode === "supervised") {
      targetHtml = `<span class="px-2 py-0.5 rounded-full text-[11px] ${
        point.label === "상승"
          ? "bg-emerald-900/40 text-emerald-300 border border-emerald-800/50"
          : "bg-rose-900/40 text-rose-300 border border-rose-800/50"
      }">${point.label}</span>`;
    } else if (conceptMode === "label") {
      targetHtml = `<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold ${
        point.label === "상승"
          ? "bg-sky-900/40 text-sky-300 border border-sky-800/50"
          : "bg-violet-900/40 text-violet-300 border border-violet-800/50"
      }">${point.label} = 정답</span>`;
    } else if (conceptMode === "unsupervised") {
      targetHtml = `<span class="text-slate-500">숨김</span>`;
    } else if (conceptMode === "clustering") {
      const cluster = clustered[idx];
      const color = CONCEPT_CLUSTER_COLORS[cluster % CONCEPT_CLUSTER_COLORS.length];
      targetHtml = `<span class="px-2 py-0.5 rounded-full text-[11px] border" style="color:${color}; border-color:${color}55; background:${color}18">군집 ${cluster + 1}</span>`;
    }

    tr.innerHTML = `
      <td class="py-1.5 pr-3 text-slate-300">${point.name}</td>
      <td class="py-1.5 pr-3 text-right font-mono text-slate-400">${signedPct(point.ret5)}</td>
      <td class="py-1.5 pr-3 text-right font-mono text-slate-400">${point.vol.toFixed(1)}</td>
      <td class="py-1.5 text-center">${targetHtml}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderConceptChart(clustered) {
  if (conceptChart) {
    conceptChart.destroy();
    conceptChart = null;
  }

  const ctx = document.getElementById("concept-chart").getContext("2d");
  const datasets = getConceptDatasets(clustered);

  conceptChart = new Chart(ctx, {
    type: "scatter",
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: "#94a3b8", font: { size: 11 } },
        },
        tooltip: {
          callbacks: {
            label(context) {
              const raw = context.raw;
              const pieces = [
                raw.name,
                `수익률 ${signedPct(raw.x)}`,
                `변동성 ${raw.y.toFixed(1)}`,
              ];
              if (conceptMode === "clustering" && typeof raw.cluster === "number") {
                pieces.push(`군집 ${raw.cluster + 1}`);
              } else if (conceptMode !== "unsupervised") {
                pieces.push(`레이블 ${raw.label}`);
              }
              return pieces.join(" · ");
            },
          },
        },
      },
      scales: {
        x: {
          title: { display: true, text: "최근 5일 수익률 (%)", color: "#64748b" },
          ticks: {
            color: "#64748b",
            callback: (value) => `${value}%`,
          },
          grid: { color: "#1e293b" },
        },
        y: {
          title: { display: true, text: "변동성", color: "#64748b" },
          ticks: { color: "#64748b" },
          grid: { color: "#1e293b" },
        },
      },
    },
  });
}

function getConceptDatasets(clustered) {
  if (conceptMode === "supervised" || conceptMode === "label") {
    return [
      {
        label: "상승 레이블",
        data: CONCEPT_POINTS.filter(point => point.label === "상승").map(point => ({
          x: point.ret5, y: point.vol, name: point.name, label: point.label,
        })),
        backgroundColor: "rgba(16,185,129,0.8)",
        borderColor: "#10b981",
        pointRadius: 6,
      },
      {
        label: "하락 레이블",
        data: CONCEPT_POINTS.filter(point => point.label === "하락").map(point => ({
          x: point.ret5, y: point.vol, name: point.name, label: point.label,
        })),
        backgroundColor: "rgba(244,63,94,0.8)",
        borderColor: "#f43f5e",
        pointRadius: 6,
      },
    ];
  }

  if (conceptMode === "unsupervised") {
    return [
      {
        label: "레이블 숨김 데이터",
        data: CONCEPT_POINTS.map(point => ({
          x: point.ret5, y: point.vol, name: point.name, label: point.label,
        })),
        backgroundColor: "rgba(148,163,184,0.8)",
        borderColor: "#94a3b8",
        pointRadius: 6,
      },
    ];
  }

  const datasets = [];
  const k = Math.max(...clustered) + 1;
  for (let clusterId = 0; clusterId < k; clusterId++) {
    const color = CONCEPT_CLUSTER_COLORS[clusterId % CONCEPT_CLUSTER_COLORS.length];
    datasets.push({
      label: `군집 ${clusterId + 1}`,
      data: CONCEPT_POINTS
        .map((point, idx) => ({ point, idx }))
        .filter(item => clustered[item.idx] === clusterId)
        .map(({ point }) => ({
          x: point.ret5, y: point.vol, name: point.name, label: point.label, cluster: clusterId,
        })),
      backgroundColor: `${color}cc`,
      borderColor: color,
      pointRadius: 6,
    });
  }
  return datasets;
}

function runMiniKMeans(points, k, maxIter = 20) {
  const coords = points.map(point => [point.ret5, point.vol]);
  const sortedIndices = coords
    .map((coord, idx) => ({ idx, score: coord[0] + coord[1] }))
    .sort((a, b) => a.score - b.score)
    .map(item => item.idx);

  const seeds = [];
  for (let i = 0; i < k; i++) {
    const pick = sortedIndices[Math.round((i * (sortedIndices.length - 1)) / Math.max(k - 1, 1))];
    seeds.push([...coords[pick]]);
  }

  let centers = seeds;
  let assigned = new Array(points.length).fill(0);

  for (let iter = 0; iter < maxIter; iter++) {
    let changed = false;

    assigned = coords.map((coord, idx) => {
      let bestCluster = 0;
      let bestDist = Infinity;
      centers.forEach((center, centerIdx) => {
        const dist = euclideanDistance(coord, center);
        if (dist < bestDist) {
          bestDist = dist;
          bestCluster = centerIdx;
        }
      });
      if (assigned[idx] !== bestCluster) changed = true;
      return bestCluster;
    });

    const nextCenters = centers.map((center, centerIdx) => {
      const members = coords.filter((_, idx) => assigned[idx] === centerIdx);
      if (!members.length) return center;
      const avgX = members.reduce((sum, item) => sum + item[0], 0) / members.length;
      const avgY = members.reduce((sum, item) => sum + item[1], 0) / members.length;
      return [avgX, avgY];
    });

    centers = nextCenters;
    if (!changed) break;
  }

  return assigned;
}

function euclideanDistance(a, b) {
  const dx = a[0] - b[0];
  const dy = a[1] - b[1];
  return Math.sqrt(dx * dx + dy * dy);
}

// ── 뉴런 계산 미니 실습 ───────────────────────────────────────────────
function initNeuronLab() {
  buildNeuronFocusButtons();

  const ids = ["neuron-x1", "neuron-x2", "neuron-w1", "neuron-w2", "neuron-bias", "neuron-target"];
  ids.forEach(id => {
    document.getElementById(id).addEventListener("input", renderNeuronLab);
  });

  document.getElementById("neuron-preset-up").addEventListener("click", () => {
    setNeuronInputs({ x1: 0.8, x2: 0.3, w1: 0.6, w2: 0.2, bias: -0.1, target: 1 });
  });
  document.getElementById("neuron-preset-flat").addEventListener("click", () => {
    setNeuronInputs({ x1: 0.4, x2: 0.4, w1: 0.3, w2: 0.2, bias: 0.0, target: 1 });
  });
  document.getElementById("neuron-preset-miss").addEventListener("click", () => {
    setNeuronInputs({ x1: 0.2, x2: 0.1, w1: -0.8, w2: -0.5, bias: -0.4, target: 1 });
  });

  renderNeuronLab();
}

function buildNeuronFocusButtons() {
  const wrap = document.getElementById("neuron-focus-buttons");
  wrap.innerHTML = "";

  Object.entries(NEURON_FOCUS_INFO).forEach(([key, info]) => {
    const btn = document.createElement("button");
    btn.dataset.neuronFocus = key;
    btn.className = "neuron-focus-btn px-3 py-1.5 rounded-full border text-xs font-semibold transition";
    btn.textContent = info.label;
    btn.addEventListener("click", () => setNeuronFocus(key));
    wrap.appendChild(btn);
  });

  updateNeuronFocusButtons();
}

function setNeuronFocus(key) {
  if (!NEURON_FOCUS_INFO[key]) return;
  neuronFocus = key;
  updateNeuronFocusButtons();
  renderNeuronLab();
}

function updateNeuronFocusButtons() {
  document.querySelectorAll(".neuron-focus-btn").forEach(btn => {
    const active = btn.dataset.neuronFocus === neuronFocus;
    btn.className = `neuron-focus-btn px-3 py-1.5 rounded-full border text-xs font-semibold transition ${
      active
        ? "bg-violet-600/20 border-violet-500 text-violet-200"
        : "bg-slate-900 border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
    }`;
  });
}

function setNeuronInputs({ x1, x2, w1, w2, bias, target }) {
  document.getElementById("neuron-x1").value = x1;
  document.getElementById("neuron-x2").value = x2;
  document.getElementById("neuron-w1").value = w1;
  document.getElementById("neuron-w2").value = w2;
  document.getElementById("neuron-bias").value = bias;
  document.getElementById("neuron-target").value = target;
  renderNeuronLab();
}

function getNeuronInputs() {
  const x1 = parseFloat(document.getElementById("neuron-x1").value) || 0;
  const x2 = parseFloat(document.getElementById("neuron-x2").value) || 0;
  const w1 = parseFloat(document.getElementById("neuron-w1").value) || 0;
  const w2 = parseFloat(document.getElementById("neuron-w2").value) || 0;
  const bias = parseFloat(document.getElementById("neuron-bias").value) || 0;
  const rawTarget = parseFloat(document.getElementById("neuron-target").value);
  const target = rawTarget >= 0.5 ? 1 : 0;
  document.getElementById("neuron-target").value = target;
  return { x1, x2, w1, w2, bias, target };
}

function sigmoid(value) {
  return 1 / (1 + Math.exp(-value));
}

function renderNeuronLab() {
  const { x1, x2, w1, w2, bias, target } = getNeuronInputs();
  const inputVector = [x1, x2];
  const wx1 = x1 * w1;
  const wx2 = x2 * w2;
  const weightedSum = wx1 + wx2;
  const z = weightedSum + bias;
  const pred = sigmoid(z);
  const error = pred - target;
  const cost = (error * error) / 2;

  document.getElementById("neuron-weighted-sum").textContent = formatNeuronNumber(weightedSum);
  document.getElementById("neuron-z").textContent = formatNeuronNumber(z);
  document.getElementById("neuron-pred").textContent = formatNeuronNumber(pred);
  document.getElementById("neuron-error").textContent = formatSignedNeuronNumber(error);
  document.getElementById("neuron-cost").textContent = formatNeuronNumber(cost);

  const info = NEURON_FOCUS_INFO[neuronFocus];
  document.getElementById("neuron-focus-title").textContent = info.title;
  document.getElementById("neuron-focus-summary").textContent = info.summary;
  document.getElementById("neuron-tip").textContent = info.tip;
  document.getElementById("neuron-formula-text").textContent =
    getNeuronFormulaText({ inputVector, x1, x2, w1, w2, bias, target, wx1, wx2, weightedSum, z, pred, error, cost });
  document.getElementById("neuron-chart-caption").textContent =
    getNeuronChartCaption({ weightedSum, bias, pred, target, error, cost });

  renderNeuronChart({ wx1, wx2, weightedSum, bias, z, pred, target, error, cost });
}

function getNeuronFormulaText(values) {
  const { inputVector, x1, x2, w1, w2, bias, target, wx1, wx2, weightedSum, z, pred, error, cost } = values;
  if (neuronFocus === "weighted_sum") {
    return `가중합 = (${x1} × ${w1}) + (${x2} × ${w2}) = ${formatNeuronNumber(wx1)} + ${formatNeuronNumber(wx2)} = ${formatNeuronNumber(weightedSum)}`;
  }
  if (neuronFocus === "bias") {
    return `z = 가중합 + 편향 = ${formatNeuronNumber(weightedSum)} + (${bias}) = ${formatNeuronNumber(z)}`;
  }
  if (neuronFocus === "sigmoid") {
    return `sigmoid(z) = 1 / (1 + e^(-z)) = 1 / (1 + e^(-${formatNeuronNumber(z)})) = ${formatNeuronNumber(pred)}`;
  }
  if (neuronFocus === "activation") {
    return `입력 벡터 ${JSON.stringify(inputVector)} → 선형변환 점수 z=${formatNeuronNumber(z)} → 활성화 함수 sigmoid(z)=${formatNeuronNumber(pred)}`;
  }
  if (neuronFocus === "error") {
    return `오차 = 예측 - 정답 = ${formatNeuronNumber(pred)} - ${target} = ${formatSignedNeuronNumber(error)}`;
  }
  return `비용 = (오차²) / 2 = (${formatSignedNeuronNumber(error)}²) / 2 = ${formatNeuronNumber(cost)}`;
}

function getNeuronChartCaption({ weightedSum, bias, pred, target, error, cost }) {
  if (neuronFocus === "weighted_sum") {
    return `두 입력의 기여를 더하면 가중합 ${formatNeuronNumber(weightedSum)}가 됩니다.`;
  }
  if (neuronFocus === "bias") {
    return `가중합 ${formatNeuronNumber(weightedSum)}에 편향 ${formatSignedNeuronNumber(bias)}를 더해 z=${formatNeuronNumber(weightedSum + bias)}가 됩니다.`;
  }
  if (neuronFocus === "sigmoid") {
    return `선형변환 결과 z=${formatNeuronNumber(weightedSum + bias)}를 sigmoid에 넣으면 예측값 ${formatNeuronNumber(pred)}가 됩니다.`;
  }
  if (neuronFocus === "activation") {
    return `활성화 함수는 z=${formatNeuronNumber(weightedSum + bias)}를 바로 쓰지 않고 예측값 ${formatNeuronNumber(pred)}처럼 해석하기 쉬운 값으로 바꿉니다.`;
  }
  if (neuronFocus === "error") {
    return `예측 ${formatNeuronNumber(pred)}와 정답 ${target}의 차이가 오차 ${formatSignedNeuronNumber(error)}입니다.`;
  }
  return `오차가 ${formatSignedNeuronNumber(error)}이므로 비용은 ${formatNeuronNumber(cost)}입니다. 학습은 이 값을 줄이는 방향으로 진행됩니다.`;
}

function renderNeuronChart(values) {
  if (neuronChart) {
    neuronChart.destroy();
    neuronChart = null;
  }

  const ctx = document.getElementById("neuron-chart").getContext("2d");
  const config = getNeuronChartConfig(values);
  neuronChart = new Chart(ctx, config);
}

function getNeuronChartConfig(values) {
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label(context) {
            return ` ${context.label}: ${formatNeuronNumber(context.raw)}`;
          },
        },
      },
    },
    scales: {
      x: { ticks: { color: "#94a3b8", font: { size: 11 } }, grid: { color: "#1e293b" } },
      y: { ticks: { color: "#64748b", font: { size: 10 } }, grid: { color: "#1e293b" } },
    },
  };

  if (neuronFocus === "weighted_sum") {
    return {
      type: "bar",
      data: {
        labels: ["x1*w1", "x2*w2", "가중합"],
        datasets: [{
          data: [values.wx1, values.wx2, values.weightedSum],
          backgroundColor: ["rgba(16,185,129,0.75)", "rgba(59,130,246,0.75)", "rgba(168,85,247,0.8)"],
          borderColor: ["#10b981", "#3b82f6", "#a855f7"],
          borderWidth: 1,
          borderRadius: 6,
        }],
      },
      options: commonOptions,
    };
  }

  if (neuronFocus === "bias") {
    return {
      type: "bar",
      data: {
        labels: ["가중합", "편향", "z"],
        datasets: [{
          data: [values.weightedSum, values.bias, values.z],
          backgroundColor: ["rgba(168,85,247,0.8)", "rgba(245,158,11,0.8)", "rgba(14,165,233,0.8)"],
          borderColor: ["#a855f7", "#f59e0b", "#0ea5e9"],
          borderWidth: 1,
          borderRadius: 6,
        }],
      },
      options: commonOptions,
    };
  }

  if (neuronFocus === "error") {
    return {
      type: "bar",
      data: {
        labels: ["예측", "정답", "오차"],
        datasets: [{
          data: [values.pred, values.target, values.error],
          backgroundColor: ["rgba(139,92,246,0.8)", "rgba(34,197,94,0.8)", "rgba(245,158,11,0.8)"],
          borderColor: ["#8b5cf6", "#22c55e", "#f59e0b"],
          borderWidth: 1,
          borderRadius: 6,
        }],
      },
      options: commonOptions,
    };
  }

  if (neuronFocus === "sigmoid" || neuronFocus === "activation") {
    return {
      type: "bar",
      data: {
        labels: ["선형변환 z", "sigmoid(z)"],
        datasets: [{
          data: [values.z, values.pred],
          backgroundColor: ["rgba(14,165,233,0.8)", "rgba(139,92,246,0.8)"],
          borderColor: ["#0ea5e9", "#8b5cf6"],
          borderWidth: 1,
          borderRadius: 6,
        }],
      },
      options: commonOptions,
    };
  }

  return {
    type: "bar",
    data: {
      labels: ["|오차|", "비용"],
      datasets: [{
        data: [Math.abs(values.error), values.cost],
        backgroundColor: ["rgba(251,191,36,0.8)", "rgba(244,63,94,0.8)"],
        borderColor: ["#fbbf24", "#f43f5e"],
        borderWidth: 1,
        borderRadius: 6,
      }],
    },
    options: commonOptions,
  };
}

function formatNeuronNumber(value) {
  return Number(value).toFixed(4);
}

function formatSignedNeuronNumber(value) {
  const num = Number(value);
  return `${num >= 0 ? "+" : ""}${num.toFixed(4)}`;
}

// ── 그리드 관리 ───────────────────────────────────────────────────────
function initGrid(count = 10) {
  document.getElementById("data-grid").innerHTML = "";
  for (let i = 0; i < count; i++) addGridRow();
}

function normalizeOHLCRow(row = {}) {
  const close = Number(row.close ?? 0);
  const open = row.open ?? close;
  const high = row.high ?? Math.max(open, close);
  const low = row.low ?? Math.min(open, close);
  return {
    date: row.date || "",
    open: Number.isFinite(Number(open)) ? Number(open) : "",
    high: Number.isFinite(Number(high)) ? Number(high) : "",
    low: Number.isFinite(Number(low)) ? Number(low) : "",
    close: Number.isFinite(close) ? close : "",
    volume: Number.isFinite(Number(row.volume)) ? Number(row.volume) : "",
  };
}

function addGridRow(row = {}) {
  const normalized = normalizeOHLCRow(typeof row === "object" ? row : {});
  const tbody  = document.getElementById("data-grid");
  const rowNum = tbody.querySelectorAll("tr").length + 1;
  const tr     = document.createElement("tr");
  tr.className = "border-b border-slate-800/80 hover:bg-slate-800/20 group";
  tr.innerHTML = `
    <td class="w-7 px-2 py-0.5 text-center text-slate-600 text-xs select-none border-r border-slate-800">${rowNum}</td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="date" value="${normalized.date}" class="grid-input" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${normalized.open}" placeholder="59800" class="grid-input" min="0" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${normalized.high}" placeholder="60300" class="grid-input" min="0" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${normalized.low}" placeholder="59200" class="grid-input" min="0" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${normalized.close}" placeholder="60000" class="grid-input" min="0" tabindex="0"/>
    </td>
    <td class="px-1 py-0.5 border-r border-slate-800">
      <input type="number" value="${normalized.volume}" placeholder="10000000" class="grid-input" min="0" tabindex="0"/>
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
  currentAssetLabel = "직접 입력 OHLCV";
  setBuiltinDatasetNote("");
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
    const open    = parseFloat(inputs[1].value);
    const high    = parseFloat(inputs[2].value);
    const low     = parseFloat(inputs[3].value);
    const close   = parseFloat(inputs[4].value);
    const volume  = parseFloat(inputs[5].value);
    if (
      date &&
      !isNaN(open) &&
      !isNaN(high) &&
      !isNaN(low) &&
      !isNaN(close) &&
      !isNaN(volume) &&
      open > 0 &&
      high > 0 &&
      low > 0 &&
      close > 0 &&
      volume > 0
    ) {
      rows.push({
        date,
        open: Math.min(open, high),
        high: Math.max(open, high, close, low),
        low: Math.min(open, low, close),
        close,
        volume,
      });
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
  data.forEach(r => addGridRow(r));
  updateRowCount();
  currentAssetLabel = ({ samsung: "삼성전자", kakao: "카카오", naver: "NAVER" }[stockKey]) || "샘플 종목";
  setBuiltinDatasetNote("");
}

function fillRandomGrid() {
  const presets = [
    { basePrice: 18500, baseVol: 850000, vol: 0.026, days: 40, label: "소형 성장주" },
    { basePrice: 74200, baseVol: 6400000, vol: 0.014, days: 48, label: "대형 우량주" },
    { basePrice: 128000, baseVol: 2900000, vol: 0.019, days: 52, label: "중형 모멘텀주" },
    { basePrice: 392000, baseVol: 1200000, vol: 0.022, days: 44, label: "고가 변동성주" },
  ];
  const preset = presets[Math.floor(Math.random() * presets.length)];
  const seed = Math.floor(Date.now() % 100000);
  const data = generateSampleData(preset.basePrice, preset.baseVol, preset.vol, preset.days, seed);
  const tbody = document.getElementById("data-grid");
  tbody.innerHTML = "";
  data.forEach(r => addGridRow(r));
  updateRowCount();
  currentAssetLabel = preset.label;
  setBuiltinDatasetNote(`랜덤 채우기 완료. ${preset.label} 느낌의 임의 주가 데이터 ${data.length}행을 생성했어요.`);
}

async function loadBuiltinDataset(datasetId) {
  try {
    const resp = await fetch(`/api/datasets/${datasetId}/adapted/stock-lab`);
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.detail || "데이터셋을 불러오지 못했습니다.");

    const tbody = document.getElementById("data-grid");
    tbody.innerHTML = "";
    (data.rows || []).forEach(r => addGridRow(r));
    updateRowCount();
    currentAssetLabel = data.title || "내장 데이터셋";
    setBuiltinDatasetNote(`내장 CSV '${data.title}' 로드 완료. ${data.note}`);
  } catch (err) {
    showAlert(`내장 데이터셋 로드 오류: ${err.message}`);
  }
}

function setBuiltinDatasetNote(message) {
  const el = document.getElementById("builtin-dataset-note");
  if (!el) return;
  if (!message) {
    el.classList.add("hidden");
    el.textContent = "";
    return;
  }
  el.textContent = message;
  el.classList.remove("hidden");
}

function generateSampleData(basePrice, baseVol, volatility, days, seed = 42) {
  const data   = [];
  let price    = basePrice;
  const start  = new Date("2026-01-02");
  const rng    = mulberry32(seed);

  for (let i = 0; i < days; i++) {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    while (d.getDay() === 0 || d.getDay() === 6) {
      d.setDate(d.getDate() + 1);
    }
    const dateStr = d.toISOString().split("T")[0];

    const drift = 0.0008 + (rng() - 0.5) * 0.0012;
    const season = Math.sin(i / 6) * volatility * 0.35;
    const change = drift + season + (rng() - 0.48) * volatility;
    const prevPrice = price;
    price        = Math.max(price * (1 + change), basePrice * 0.45);
    const volBoost = 1 + Math.abs(change) * 14;
    const vol    = Math.round(baseVol * (0.55 + rng() * 1.2) * volBoost);
    const open = prevPrice * (1 + (rng() - 0.5) * volatility * 0.35);
    const close = price;
    const high = Math.max(open, close) * (1 + rng() * volatility * 0.55);
    const low = Math.min(open, close) * (1 - rng() * volatility * 0.55);
    data.push({
      date: dateStr,
      open: Math.round(open),
      high: Math.round(high),
      low: Math.round(low),
      close: Math.round(close),
      volume: vol,
    });
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
      let headerMap = null;
      lines.forEach((line, i) => {
        const parts = line.split(",").map(part => part.trim());
        if (i === 0) {
          const maybeHeader = parts.map(part => part.toLowerCase());
          if (maybeHeader.includes("date")) {
            headerMap = maybeHeader;
            return;
          }
        }

        let row = null;
        if (headerMap) {
          const getVal = (name) => parts[headerMap.indexOf(name)];
          row = {
            date: getVal("date"),
            open: getVal("open"),
            high: getVal("high"),
            low: getVal("low"),
            close: getVal("close"),
            volume: getVal("volume"),
          };
        } else if (parts.length >= 6) {
          row = {
            date: parts[0],
            open: parts[1],
            high: parts[2],
            low: parts[3],
            close: parts[4],
            volume: parts[5],
          };
        } else if (parts.length >= 3) {
          row = {
            date: parts[0],
            close: parts[1],
            volume: parts[2],
          };
        }

        if (row && row.date && row.close && row.volume) {
          addGridRow(row);
          loaded++;
        }
      });
      updateRowCount();
      if (loaded > 0) {
        currentAssetLabel = file.name.replace(/\.csv$/i, "");
        setBuiltinDatasetNote(`CSV '${file.name}' 로드 완료. OHLC가 없던 행은 close 기준으로 자동 보정했어요.`);
      } else {
        alert("CSV 파싱 실패. 헤더가 date,open,high,low,close,volume 또는 date,close,volume 형식인지 확인하세요.");
      }
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
  document.getElementById("result-asset-name").textContent  = currentAssetLabel;
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
  setVisible("candle-card",      true);
  setVisible("explanation-card", true);
  setVisible("portfolio-card",   true);
  setVisible("importance-card",  true);
  setVisible("signals-card",     true);

  drawCandleChart(r.candles || [], r);
  drawPredictionExplanation(r);
  drawPortfolioChart(r.portfolio, r.buyhold, r.model_name);
  drawImportanceChart(r.feature_importance);
  drawSignalsTable(r.signals);

  // ── 신경망 시각화 패널 ──
  if (r.nn_viz && r.model_key === "nn") {
    setVisible("nnviz-card", true);
    labNNViz = mountNNViz("labnnviz", "nn-viz-canvas-lab", r.nn_viz);
  } else {
    setVisible("nnviz-card", false);
    labNNViz = null;
  }

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
function drawCandleChart(candles, result) {
  if (candleChart) { candleChart.destroy(); candleChart = null; }
  if (!candles.length) return;

  const ctx = document.getElementById("candle-chart").getContext("2d");
  const candleData = candles.map(item => ({
    x: item.date,
    o: item.open,
    h: item.high,
    l: item.low,
    c: item.close,
  }));
  const predictionPoint = {
    x: result.predicted_next_date,
    y: result.predicted_next_close,
  };

  candleChart = new Chart(ctx, {
    data: {
      datasets: [
        {
          type: "candlestick",
          label: `${currentAssetLabel} OHLCV`,
          data: candleData,
          color: {
            up: "#22c55e",
            down: "#ef4444",
            unchanged: "#94a3b8",
          },
          borderColor: {
            up: "#22c55e",
            down: "#ef4444",
            unchanged: "#94a3b8",
          },
        },
        {
          type: "scatter",
          label: "내일 예상 종가",
          data: [predictionPoint],
          parsing: false,
          backgroundColor: "#facc15",
          borderColor: "#fde047",
          pointRadius: 8,
          pointHoverRadius: 10,
          pointBorderWidth: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "nearest", intersect: false },
      plugins: {
        legend: {
          labels: { color: "#94a3b8", font: { size: 11 } },
        },
        tooltip: {
          callbacks: {
            label(context) {
              if (context.dataset.type === "scatter") {
                return ` 내일 예상 종가: ${Math.round(context.raw.y).toLocaleString()}원`;
              }
              const raw = context.raw;
              return ` 시:${Math.round(raw.o).toLocaleString()} 고:${Math.round(raw.h).toLocaleString()} 저:${Math.round(raw.l).toLocaleString()} 종:${Math.round(raw.c).toLocaleString()}`;
            },
          },
        },
      },
      scales: {
        x: {
          type: "time",
          time: { unit: "day", tooltipFormat: "yyyy-LL-dd" },
          ticks: { color: "#64748b", font: { size: 10 }, maxTicksLimit: 8 },
          grid: { color: "#1e293b" },
        },
        y: {
          ticks: {
            color: "#64748b",
            font: { size: 10 },
            callback: value => `${Math.round(value).toLocaleString()}`,
          },
          grid: { color: "#1e293b" },
        },
      },
    },
  });

  document.getElementById("next-date-badge").textContent = result.predicted_next_date;
  document.getElementById("candle-caption").textContent =
    `${currentAssetLabel}의 최근 ${candles.length}개 OHLCV 캔들을 표시했습니다. 마지막 종가 ${Math.round(result.last_close).toLocaleString()}원 대비 `
    + `내일 예상 종가는 ${Math.round(result.predicted_next_close).toLocaleString()}원(${signedPct(result.predicted_move_pct)})로 추정했습니다.`;
}

function drawPredictionExplanation(r) {
  const ds = r.dataset_summary || {};
  const method = r.method_summary || {};
  const reg = r.regression_metrics || {};
  const prediction = r.prediction_summary || {};
  const topFeatures = (method.top_features || []).join(", ");

  document.getElementById("prediction-signal-badge").textContent = prediction.signal || "예측 요약";
  document.getElementById("dataset-range-text").textContent =
    `${ds.start_date || "-"} ~ ${ds.end_date || "-"} 구간의 ${ds.rows || 0}행 OHLCV를 사용했습니다. 시간 순서를 유지한 채 학습 ${ds.train_rows || 0}행, 테스트 ${ds.test_rows || 0}행으로 나눴습니다.`;
  document.getElementById("model-method-text").textContent =
    `${method.classification || "-"} ${method.regression || ""} ${method.reason || ""}`.trim();
  document.getElementById("prediction-reason-text").textContent =
    `${prediction.basis || "-"}${topFeatures ? ` 특히 ${topFeatures} 신호를 더 많이 참고했습니다.` : ""}`;
  document.getElementById("last-close-text").textContent =
    `${Math.round(r.last_close || 0).toLocaleString()}원`;
  document.getElementById("next-close-text").textContent =
    `${Math.round(r.predicted_next_close || 0).toLocaleString()}원 (${signedPct(r.predicted_move_pct || 0)})`;
  document.getElementById("regression-metrics-text").textContent =
    `MAE ${Math.round(reg.mae || 0).toLocaleString()}원 · RMSE ${Math.round(reg.rmse || 0).toLocaleString()}원 · R² ${(reg.r2 ?? 0).toFixed(3)}`;
}

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
