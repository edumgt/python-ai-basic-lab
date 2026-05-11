/* ═══════════════════════════════════════════════════════════════════
   AI/ML Lab — app.js
   기술스택: AG Grid · ApexCharts · Canvas · LocalStorage
═══════════════════════════════════════════════════════════════════ */

// ── DOM 단축 ──────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

// ══════════════════════════════════════════════════════════════════
//  LocalStorage 헬퍼
// ══════════════════════════════════════════════════════════════════
const LS = {
  KEY: 'ailab',
  get(sub, def = null) {
    try { return JSON.parse(localStorage.getItem(`${this.KEY}_${sub}`)) ?? def; }
    catch { return def; }
  },
  set(sub, val) {
    try { localStorage.setItem(`${this.KEY}_${sub}`, JSON.stringify(val)); }
    catch { /* quota exceeded */ }
  },
  // 히스토리: 최대 30건, 최신 순
  pushHistory(item) {
    const hist = this.get('history', []);
    hist.unshift({ id: Date.now(), ...item });
    this.set('history', hist.slice(0, 30));
  },
  getHistory() { return this.get('history', []); },
  clearHistory() { this.set('history', []); },
};

// ══════════════════════════════════════════════════════════════════
//  전역 상태
// ══════════════════════════════════════════════════════════════════
let currentChapterId = LS.get('lastChapter', null);
let currentMode      = 'chapter';   // 'chapter' | 'doc'
let allChapters      = [];
let allDocs          = [];
let chapterGridApi   = null;
let historyGridApi   = null;
let apexBarChart     = null;
let apexLineChart    = null;
let neuralAnim       = null;

// ══════════════════════════════════════════════════════════════════
//  사이드바 토글
// ══════════════════════════════════════════════════════════════════
const sidebarEl = $('sidebar');
const overlayEl = $('overlay');

function setSidebar(open) {
  sidebarEl.classList.toggle('-translate-x-full', !open);
  sidebarEl.classList.toggle('translate-x-0', open);
  $('icon-menu').classList.toggle('hidden', open);
  $('icon-close').classList.toggle('hidden', !open);
  overlayEl.classList.toggle('hidden', !open);
  LS.set('sidebarOpen', open);
}

$('sidebar-toggle').addEventListener('click', () => {
  setSidebar(sidebarEl.classList.contains('-translate-x-full'));
});
overlayEl.addEventListener('click', () => setSidebar(false));

// ══════════════════════════════════════════════════════════════════
//  모드 탭 (대시보드 | 챕터 | 문서)
// ══════════════════════════════════════════════════════════════════
const MODE_PANELS = { dashboard: 'mode-dashboard', grid: 'mode-grid', docs: 'mode-docs' };

function switchMode(mode) {
  $$('.mode-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.mode === mode);
  });
  Object.entries(MODE_PANELS).forEach(([k, id]) => {
    const el = $(id);
    el.classList.toggle('hidden', k !== mode);
    el.classList.toggle('flex', k === mode && (k === 'grid'));
    el.classList.toggle('flex-col', k === mode && (k === 'grid'));
  });
  if (mode === 'grid' && chapterGridApi) {
    setTimeout(() => chapterGridApi.sizeColumnsToFit(), 50);
  }
  LS.set('sidebarMode', mode);
}

$$('.mode-btn').forEach(btn =>
  btn.addEventListener('click', () => switchMode(btn.dataset.mode))
);

// ══════════════════════════════════════════════════════════════════
//  콘텐츠 탭 (소스 | 결과 | 설명 | 차트 | 히스토리)
// ══════════════════════════════════════════════════════════════════
function activateTab(name) {
  $$('.tab-btn').forEach(b => {
    const active = b.dataset.tab === name;
    b.classList.toggle('active', active);
    b.classList.toggle('border-indigo-500', active);
    b.classList.toggle('text-indigo-400', active);
    b.classList.toggle('border-transparent', !active);
    b.classList.toggle('text-slate-400', !active);
  });
  $$('.tab-panel').forEach(p => {
    p.classList.toggle('hidden', p.id !== `tab-${name}`);
  });
  // AG Grid 히스토리 탭 활성화 시 리프레시
  if (name === 'history' && historyGridApi) {
    setTimeout(() => historyGridApi.sizeColumnsToFit(), 50);
  }
}

$$('.tab-btn').forEach(btn =>
  btn.addEventListener('click', () => activateTab(btn.dataset.tab))
);

// ══════════════════════════════════════════════════════════════════
//  로딩 오버레이
// ══════════════════════════════════════════════════════════════════
function showLoading(msg = '처리 중…') {
  $('loading-msg').textContent = msg;
  $('loading-overlay').classList.remove('hidden');
}
function hideLoading() {
  $('loading-overlay').classList.add('hidden');
}

// ══════════════════════════════════════════════════════════════════
//  Canvas — 뉴럴 네트워크 애니메이션
// ══════════════════════════════════════════════════════════════════
function initCanvas() {
  const canvas = $('neuralCanvas');
  const ctx    = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const N = 28;
  const MAX_DIST = 80;

  const nodes = Array.from({ length: N }, () => ({
    x:  Math.random() * W,
    y:  Math.random() * H,
    vx: (Math.random() - 0.5) * 0.4,
    vy: (Math.random() - 0.5) * 0.4,
    r:  Math.random() * 2 + 1.5,
    pulse: 0,
  }));

  function frame() {
    ctx.clearRect(0, 0, W, H);

    // edges
    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const d  = Math.sqrt(dx * dx + dy * dy);
        if (d < MAX_DIST) {
          const alpha = (1 - d / MAX_DIST) * 0.25;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = `rgba(99,102,241,${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    // nodes
    nodes.forEach(n => {
      const pulse = n.pulse > 0 ? n.pulse : 0;
      n.pulse = Math.max(0, n.pulse - 0.04);
      const extra = pulse * 4;
      const grd = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r + extra + 2);
      grd.addColorStop(0, `rgba(129,140,248,${0.9 + pulse * 0.1})`);
      grd.addColorStop(1, 'rgba(99,102,241,0)');
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r + extra, 0, Math.PI * 2);
      ctx.fillStyle = grd;
      ctx.fill();

      // motion
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
    });

    neuralAnim = requestAnimationFrame(frame);
  }
  frame();

  // 실행 시 노드 펄스 효과
  window._pulseCanvas = () => {
    nodes.forEach(n => { n.pulse = Math.random() > 0.5 ? 1 : 0; });
    setTimeout(() => nodes.forEach(n => { n.pulse = 0; }), 800);
  };
}

// ══════════════════════════════════════════════════════════════════
//  AG Grid — 챕터 목록 그리드
// ══════════════════════════════════════════════════════════════════
function initChapterGrid(chapters) {
  const columnDefs = [
    {
      field: 'id',
      headerName: 'ID',
      width: 90,
      cellStyle: { color: '#818cf8', fontWeight: '600' },
      valueFormatter: p => p.value.replace('chapter', 'ch'),
    },
    { field: 'title',  headerName: '제목', flex: 2, minWidth: 120 },
    { field: 'topic',  headerName: '주제', flex: 1, minWidth: 80,
      cellStyle: { color: '#94a3b8' } },
    {
      field: 'has_run',
      headerName: '실행',
      width: 60,
      cellRenderer: p => p.value
        ? `<span class="text-emerald-400">✓</span>`
        : `<span class="text-slate-600">—</span>`,
    },
  ];

  const gridOptions = {
    columnDefs,
    rowData: chapters,
    rowSelection: 'single',
    animateRows: true,
    pagination: true,
    paginationPageSize: 20,
    suppressMovableColumns: true,
    defaultColDef: { sortable: true, resizable: true, filter: true },
    onRowClicked: e => {
      selectChapter(e.data.id);
      setSidebar(false);
    },
    getRowStyle: p => {
      if (p.data.id === currentChapterId)
        return { background: 'rgba(99,102,241,.18)' };
    },
  };

  const el = $('chapterGrid');
  agGrid.createGrid(el, gridOptions);
  // save ref
  chapterGridApi = el._agGrid || null;

  // grid-search 연동
  $('grid-search').addEventListener('input', e => {
    const q = e.target.value.toLowerCase();
    const filtered = chapters.filter(c =>
      c.id.includes(q) || (c.title || '').toLowerCase().includes(q) ||
      (c.topic || '').toLowerCase().includes(q)
    );
    // AG Grid rowData 갱신
    el.querySelector('.ag-root-wrapper')?._agGrid?.setGridOption?.('rowData', filtered);
  });
}

// ══════════════════════════════════════════════════════════════════
//  AG Grid — 히스토리 그리드
// ══════════════════════════════════════════════════════════════════
function initHistoryGrid() {
  const columnDefs = [
    {
      field: 'timestamp', headerName: '시간', width: 120,
      valueFormatter: p => p.value ? new Date(p.value).toLocaleTimeString('ko-KR') : '—',
      cellStyle: { color: '#64748b' },
    },
    {
      field: 'chapterId', headerName: '챕터', width: 90,
      cellStyle: { color: '#818cf8', fontWeight: '600' },
      valueFormatter: p => (p.value || '').replace('chapter', 'ch'),
    },
    { field: 'title', headerName: '제목', flex: 1, minWidth: 100 },
    {
      field: 'elapsed_ms', headerName: '실행(ms)', width: 90,
      cellStyle: { color: '#94a3b8', textAlign: 'right' },
      valueFormatter: p => p.value ? `${p.value}ms` : '—',
    },
    {
      field: 'status', headerName: '상태', width: 70,
      cellRenderer: p =>
        p.value === 'ok'
          ? `<span class="hist-success px-2 py-0.5 rounded-full text-[10px]">성공</span>`
          : `<span class="hist-error px-2 py-0.5 rounded-full text-[10px]">오류</span>`,
    },
    {
      field: 'summary', headerName: '요약', flex: 1, minWidth: 100,
      cellStyle: { color: '#64748b', fontSize: '11px' },
    },
  ];

  const gridOptions = {
    columnDefs,
    rowData: LS.getHistory(),
    animateRows: true,
    pagination: true,
    paginationPageSize: 15,
    suppressMovableColumns: true,
    defaultColDef: { sortable: true, resizable: true },
  };

  const el = $('historyGrid');
  historyGridApi = agGrid.createGrid(el, gridOptions);
}

function refreshHistoryGrid() {
  if (!historyGridApi) return;
  historyGridApi.setGridOption?.('rowData', LS.getHistory());
  updateHistoryBadge();
}

function updateHistoryBadge() {
  const hist = LS.getHistory();
  const badge = $('historyBadge');
  if (hist.length > 0) {
    badge.textContent = hist.length;
    badge.classList.remove('hidden');
  } else {
    badge.classList.add('hidden');
  }
}

// ══════════════════════════════════════════════════════════════════
//  ApexCharts — 결과 시각화
// ══════════════════════════════════════════════════════════════════
const APEX_COMMON = {
  chart:   { background: 'transparent', toolbar: { show: false } },
  theme:   { mode: 'dark' },
  grid:    { borderColor: '#1e293b' },
  tooltip: { theme: 'dark' },
};

function destroyApex() {
  if (apexBarChart)  { apexBarChart.destroy();  apexBarChart  = null; }
  if (apexLineChart) { apexLineChart.destroy(); apexLineChart = null; }
  $('apex-bar-wrap').classList.add('hidden');
  $('apex-line-wrap').classList.add('hidden');
  $('charts-placeholder').classList.remove('hidden');
}

function renderApexFromResult(result) {
  destroyApex();
  if (!result) return;

  // ── 숫자 스칼라 → 가로 막대 차트 ──────────────────
  const SKIP = new Set(['chapter', 'topic', 'n_train', 'n_test']);
  const numEntries = Object.entries(result).filter(([k, v]) =>
    !SKIP.has(k) && typeof v === 'number' && isFinite(v)
  );

  if (numEntries.length >= 2) {
    const labels = numEntries.map(([k]) => k);
    const values = numEntries.map(([, v]) => parseFloat(v.toFixed(4)));

    $('charts-placeholder').classList.add('hidden');
    $('apex-bar-wrap').classList.remove('hidden');

    apexBarChart = new ApexCharts($('apex-bar'), {
      ...APEX_COMMON,
      chart:  { ...APEX_COMMON.chart, type: 'bar', height: 220 },
      series: [{ name: '값', data: values }],
      xaxis:  { categories: labels, labels: { style: { colors: '#94a3b8', fontSize: '11px' } } },
      yaxis:  { labels: { style: { colors: '#64748b', fontSize: '11px' } } },
      colors: ['#6366f1'],
      plotOptions: { bar: { borderRadius: 4, distributed: true } },
      legend: { show: false },
      dataLabels: { enabled: true, style: { fontSize: '10px' } },
    });
    apexBarChart.render();
  }

  // ── 배열 시계열 → 라인 차트 ────────────────────────
  const SERIES_KEYS = ['portfolio', 'buyhold', 'returns', 'prices', 'pred'];
  const seriesList = [];
  const colors     = ['#6366f1', '#10b981', '#f59e0b', '#f43f5e', '#3b82f6'];

  SERIES_KEYS.forEach(k => {
    if (Array.isArray(result[k]) && result[k].length > 1) {
      seriesList.push({ name: k, data: result[k].slice(0, 200) });
    }
  });

  // 알 수 없는 배열 키도 포함
  Object.entries(result).forEach(([k, v]) => {
    if (!SERIES_KEYS.includes(k) && Array.isArray(v) && v.length > 1 &&
        typeof v[0] === 'number' && seriesList.length < 4) {
      seriesList.push({ name: k, data: v.slice(0, 200) });
    }
  });

  if (seriesList.length > 0) {
    $('charts-placeholder').classList.add('hidden');
    $('apex-line-wrap').classList.remove('hidden');

    apexLineChart = new ApexCharts($('apex-line'), {
      ...APEX_COMMON,
      chart:  { ...APEX_COMMON.chart, type: 'line', height: 260 },
      series: seriesList,
      stroke: { curve: 'smooth', width: 2 },
      xaxis:  { labels: { show: false } },
      yaxis:  { labels: { style: { colors: '#64748b', fontSize: '11px' },
                           formatter: v => typeof v === 'number' ? v.toFixed(3) : v } },
      colors: colors.slice(0, seriesList.length),
      legend: { labels: { colors: '#94a3b8' } },
      markers: { size: 0 },
    });
    apexLineChart.render();
  }
}

// ══════════════════════════════════════════════════════════════════
//  결과 카드 렌더링
// ══════════════════════════════════════════════════════════════════
function renderResultCard(key, value) {
  const card = document.createElement('div');
  card.className = 'flex items-start gap-3 bg-slate-800/60 border border-slate-700 rounded-lg px-3 py-2';

  const keyEl = document.createElement('span');
  keyEl.className = 'flex-none font-mono text-[11px] text-indigo-300 pt-0.5 min-w-[110px]';
  keyEl.textContent = key;
  card.appendChild(keyEl);

  const valEl = document.createElement('div');
  valEl.className = 'flex-1 min-w-0';

  if (Array.isArray(value)) {
    const prev = value.slice(0, 8).map(v =>
      typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(4)) : String(v)
    ).join(', ');
    valEl.innerHTML = `<span class="text-slate-300 text-xs font-mono">[${prev}${value.length > 8 ? ` …+${value.length - 8}` : ''}]</span>
      <span class="ml-2 text-[10px] text-slate-600">${value.length}개</span>`;
  } else if (value !== null && typeof value === 'object') {
    valEl.innerHTML = `<pre class="text-[11px] text-slate-300 font-mono whitespace-pre-wrap
      bg-slate-900 rounded p-1.5 border border-slate-700">${JSON.stringify(value, null, 2)}</pre>`;
  } else if (typeof value === 'number') {
    const fmt   = Number.isInteger(value) ? value.toLocaleString() : value.toFixed(6);
    const color = value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-slate-300';
    valEl.innerHTML = `<span class="font-mono text-xs font-semibold ${color}">${fmt}</span>`;
  } else if (typeof value === 'boolean') {
    valEl.innerHTML = value
      ? `<span class="bg-green-900/50 text-green-300 border border-green-700 px-1.5 py-0.5 rounded text-[11px]">true ✓</span>`
      : `<span class="bg-red-900/50 text-red-300 border border-red-700 px-1.5 py-0.5 rounded text-[11px]">false ✗</span>`;
  } else {
    valEl.innerHTML = `<span class="text-slate-200 text-xs">${String(value)}</span>`;
  }

  card.appendChild(valEl);
  return card;
}

function renderResultCards(result) {
  const rc = $('result-cards');
  rc.innerHTML = '';

  const meta = document.createElement('div');
  meta.className = 'flex flex-wrap gap-1.5 mb-2';
  ['chapter', 'topic'].forEach(k => {
    if (result[k]) {
      const b = document.createElement('span');
      b.className = k === 'chapter'
        ? 'bg-indigo-900/60 text-indigo-300 border border-indigo-700 px-2 py-0.5 rounded-full text-[11px] font-mono'
        : 'bg-slate-700 text-slate-200 px-2 py-0.5 rounded-full text-[11px]';
      b.textContent = result[k];
      meta.appendChild(b);
    }
  });
  if (meta.children.length) rc.appendChild(meta);

  const SKIP = new Set(['chapter', 'topic']);
  Object.entries(result).forEach(([k, v]) => {
    if (!SKIP.has(k)) rc.appendChild(renderResultCard(k, v));
  });
}

function resetResultPanel() {
  $('result-placeholder').classList.remove('hidden');
  $('result-stdout').classList.add('hidden');
  $('result-content').classList.add('hidden');
  $('result-error').classList.add('hidden');
  $('elapsed-badge').classList.add('hidden');
  $('stdout-pre').textContent = '';
  $('result-cards').innerHTML = '';
  $('result-json').textContent = '';
  $('error-msg').textContent = '';
  destroyApex();
}

// ══════════════════════════════════════════════════════════════════
//  챕터 목록 & 문서 목록
// ══════════════════════════════════════════════════════════════════
async function loadChapters() {
  const res = await fetch('/api/chapters');
  allChapters = await res.json();
  initChapterGrid(allChapters);
  $('dash-total').textContent = allChapters.length;
  $('stats-text').textContent = `챕터 ${allChapters.length}개`;
}

async function loadDocs() {
  try {
    const res = await fetch('/api/docs');
    if (!res.ok) return;
    allDocs = await res.json();
    renderDocList(allDocs);
    $('dash-docs').textContent = allDocs.length;
  } catch { /* API 없으면 무시 */ }
}

function renderDocList(docs) {
  const listEl = $('doc-list');
  listEl.innerHTML = '';

  if (!docs.length) {
    listEl.innerHTML = '<div class="py-8 text-center text-slate-600 text-xs">문서 없음</div>';
    return;
  }

  // 그룹 구분
  const dictDocs   = docs.filter(d => !parseInt(d.id));
  const numDocs    = docs.filter(d => parseInt(d.id));

  if (numDocs.length) {
    const h = document.createElement('div');
    h.className = 'px-3 pt-3 pb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-wider';
    h.textContent = '📘 학습 가이드';
    listEl.appendChild(h);
    numDocs.forEach(doc => listEl.appendChild(makeDocBtn(doc)));
  }
  if (dictDocs.length) {
    const h = document.createElement('div');
    h.className = 'px-3 pt-3 pb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-wider border-t border-slate-800 mt-2';
    h.textContent = '📖 용어 사전';
    listEl.appendChild(h);
    dictDocs.forEach(doc => listEl.appendChild(makeDocBtn(doc)));
  }
}

function makeDocBtn(doc) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'w-full text-left px-3 py-2 rounded-lg text-xs transition hover:bg-slate-800 text-slate-300 hover:text-slate-100';
  btn.innerHTML = `<span class="font-mono text-emerald-400 text-[10px] mr-2">${doc.id}</span>${doc.title}`;
  btn.addEventListener('click', () => { selectDoc(doc.id, doc.title); setSidebar(false); });
  return btn;
}

// ══════════════════════════════════════════════════════════════════
//  챕터 선택
// ══════════════════════════════════════════════════════════════════
async function selectChapter(chapterId) {
  currentChapterId = chapterId;
  currentMode = 'chapter';
  $('run-btn').disabled = false;
  LS.set('lastChapter', chapterId);

  showLoading('소스 로딩 중…');
  try {
    const [detailRes, sourceRes] = await Promise.all([
      fetch(`/api/chapters/${chapterId}`),
      fetch(`/api/chapters/${chapterId}/source`),
    ]);
    const detail = await detailRes.json();
    const src    = await sourceRes.json();

    // 챕터 정보 바
    $('chapter-info').classList.remove('hidden');
    $('info-id').textContent    = chapterId;
    $('info-title').textContent = detail.title || '';
    const topicEl = $('info-topic');
    if (detail.topic) {
      topicEl.textContent = detail.topic;
      topicEl.classList.remove('hidden');
    } else {
      topicEl.classList.add('hidden');
    }
    const lessonEl = $('info-lesson');
    if (detail.lesson_10min) {
      lessonEl.textContent = `💡 ${detail.lesson_10min}`;
      lessonEl.classList.remove('hidden');
    } else {
      lessonEl.classList.add('hidden');
    }

    // 소스
    $('source-filename').textContent = 'practice.py';
    $('source-code').textContent = src.source;
    if (window.Prism) Prism.highlightElement($('source-code'));

    // README → 설명탭
    $('readme-content').innerHTML = detail.readme
      ? (window.marked ? marked.parse(detail.readme) : `<pre>${detail.readme}</pre>`)
      : '<p class="text-slate-500 text-xs">README가 없습니다.</p>';

    // 대시보드 챕터명 표시
    $('dash-chapter-name').textContent = `▶ ${detail.title || chapterId}`;

    resetResultPanel();
    activateTab('source');
  } catch {
    $('dash-chapter-name').textContent = '로딩 실패';
  } finally {
    hideLoading();
  }
}

// ══════════════════════════════════════════════════════════════════
//  문서 선택
// ══════════════════════════════════════════════════════════════════
async function selectDoc(docId, docTitle) {
  currentMode = 'doc';
  currentChapterId = null;
  $('run-btn').disabled = true;

  $('chapter-info').classList.remove('hidden');
  $('info-id').textContent    = docId + '.md';
  $('info-title').textContent = docTitle || docId;
  $('info-topic').classList.add('hidden');
  $('info-lesson').classList.add('hidden');
  $('source-filename').textContent = docId + '.md';
  $('dash-chapter-name').textContent = `📖 ${docTitle || docId}`;

  showLoading('문서 로딩 중…');
  try {
    const res = await fetch(`/api/docs/${docId}`);
    const doc = await res.json();

    $('source-code').textContent = doc.content;
    if (window.Prism) Prism.highlightElement($('source-code'));

    $('readme-content').innerHTML = doc.content
      ? (window.marked ? marked.parse(doc.content) : `<pre>${doc.content}</pre>`)
      : '<p class="text-slate-500 text-xs">내용이 없습니다.</p>';

    activateTab('readme');
  } catch {
    $('readme-content').innerHTML = '<p class="text-red-400 text-xs">문서를 불러오지 못했습니다.</p>';
    activateTab('readme');
  } finally {
    hideLoading();
  }
}

// ══════════════════════════════════════════════════════════════════
//  코드 복사
// ══════════════════════════════════════════════════════════════════
$('copy-btn').addEventListener('click', async () => {
  await navigator.clipboard.writeText($('source-code').textContent);
  $('copy-btn').textContent = '복사됨!';
  setTimeout(() => { $('copy-btn').textContent = '복사'; }, 2000);
});

// ══════════════════════════════════════════════════════════════════
//  챕터 실행
// ══════════════════════════════════════════════════════════════════
$('run-btn').addEventListener('click', async () => {
  if (!currentChapterId || currentMode !== 'chapter') return;

  showLoading('실행 중…');
  activateTab('result');
  resetResultPanel();
  $('result-placeholder').classList.add('hidden');

  // Canvas 펄스 효과
  if (window._pulseCanvas) window._pulseCanvas();

  const t0 = Date.now();
  try {
    const res  = await fetch(`/api/chapters/${currentChapterId}/run`, { method: 'POST' });
    const data = await res.json();
    const elapsed = Date.now() - t0;

    if (!res.ok) {
      $('error-msg').textContent = data.detail || JSON.stringify(data);
      $('result-error').classList.remove('hidden');
      LS.pushHistory({
        timestamp:  new Date().toISOString(),
        chapterId:  currentChapterId,
        title:      $('info-title').textContent,
        elapsed_ms: data.elapsed_ms || elapsed,
        status:     'error',
        summary:    data.detail || '실행 오류',
      });
    } else {
      // stdout
      if (data.stdout?.trim()) {
        $('stdout-pre').textContent = data.stdout;
        $('result-stdout').classList.remove('hidden');
      }
      // result cards
      if (data.result && Object.keys(data.result).length) {
        renderResultCards(data.result);
        $('result-json').textContent = JSON.stringify(data.result, null, 2);
        $('result-content').classList.remove('hidden');
        // ApexCharts 렌더링
        renderApexFromResult(data.result);
      }
      if (!data.stdout?.trim() && !Object.keys(data.result || {}).length) {
        $('result-placeholder').classList.remove('hidden');
      }

      $('elapsed-ms').textContent = data.elapsed_ms;
      $('elapsed-badge').classList.remove('hidden');

      // 히스토리 저장
      const numKeys = Object.entries(data.result || {})
        .filter(([, v]) => typeof v === 'number' && isFinite(v))
        .map(([k, v]) => `${k}=${typeof v === 'number' ? v.toFixed(3) : v}`)
        .slice(0, 3).join(' | ');

      LS.pushHistory({
        timestamp:  new Date().toISOString(),
        chapterId:  currentChapterId,
        title:      $('info-title').textContent,
        elapsed_ms: data.elapsed_ms,
        status:     'ok',
        summary:    numKeys || (data.stdout?.trim().slice(0, 60) || '성공'),
      });
    }

    refreshHistoryGrid();
    updateDashboard();
  } catch (e) {
    $('error-msg').textContent = e.message;
    $('result-error').classList.remove('hidden');
  } finally {
    hideLoading();
  }
});

// ══════════════════════════════════════════════════════════════════
//  검색 (헤더)
// ══════════════════════════════════════════════════════════════════
$('search').addEventListener('input', e => {
  const q = e.target.value.toLowerCase().trim();
  if (!q) return;
  // 챕터 그리드 모드로 전환 후 검색어 적용
  switchMode('grid');
  $('grid-search').value = q;
  $('grid-search').dispatchEvent(new Event('input'));
});

// ══════════════════════════════════════════════════════════════════
//  대시보드 업데이트
// ══════════════════════════════════════════════════════════════════
function updateDashboard() {
  const hist    = LS.getHistory();
  const today   = new Date().toDateString();
  const todayRuns = hist.filter(h => new Date(h.timestamp).toDateString() === today);

  $('dash-runs').textContent   = hist.length;
  $('dash-streak').textContent = todayRuns.length;

  // 최근 실행 목록
  const recentEl = $('dash-recent');
  recentEl.innerHTML = '';
  hist.slice(0, 5).forEach(h => {
    const div = document.createElement('div');
    div.className = 'flex items-center gap-2 text-[11px] py-1.5 border-b border-slate-800/50';
    const statusCls = h.status === 'ok' ? 'text-emerald-400' : 'text-red-400';
    div.innerHTML = `
      <span class="${statusCls}">${h.status === 'ok' ? '✓' : '✗'}</span>
      <span class="text-indigo-400 font-mono">${(h.chapterId || '').replace('chapter', 'ch')}</span>
      <span class="text-slate-400 truncate flex-1">${h.title || ''}</span>
      <span class="text-slate-600">${h.elapsed_ms || ''}ms</span>`;
    div.addEventListener('click', () => {
      if (h.chapterId) selectChapter(h.chapterId);
    });
    div.style.cursor = 'pointer';
    recentEl.appendChild(div);
  });
}

// ══════════════════════════════════════════════════════════════════
//  히스토리 CSV 내보내기
// ══════════════════════════════════════════════════════════════════
$('export-history-btn').addEventListener('click', () => {
  const hist = LS.getHistory();
  if (!hist.length) return;
  const header = 'timestamp,chapterId,title,elapsed_ms,status,summary\n';
  const rows   = hist.map(h =>
    [h.timestamp, h.chapterId, `"${h.title}"`, h.elapsed_ms, h.status, `"${h.summary}"`].join(',')
  ).join('\n');
  const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a'); a.href = url; a.download = 'run_history.csv';
  a.click(); URL.revokeObjectURL(url);
});

// ══════════════════════════════════════════════════════════════════
//  기록 초기화
// ══════════════════════════════════════════════════════════════════
$('clear-history-btn').addEventListener('click', () => {
  if (!confirm('실행 기록을 모두 삭제할까요?')) return;
  LS.clearHistory();
  refreshHistoryGrid();
  updateDashboard();
});

// ══════════════════════════════════════════════════════════════════
//  초기화
// ══════════════════════════════════════════════════════════════════
(async () => {
  // Canvas 시작
  initCanvas();

  // 히스토리 그리드 초기화
  initHistoryGrid();
  updateHistoryBadge();
  updateDashboard();

  // 챕터 & 문서 로드
  await loadChapters();
  await loadDocs();

  // LocalStorage 복원
  const lastMode = LS.get('sidebarMode', 'dashboard');
  switchMode(lastMode);

  if (currentChapterId) {
    const found = allChapters.find(c => c.id === currentChapterId);
    if (found) selectChapter(currentChapterId);
  }
})();
