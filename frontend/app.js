// ── DOM 참조 ────────────────────────────────────────────────────────────────
const $  = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

const sidebarEl      = $('sidebar');
const toggleBtn      = $('sidebar-toggle');
const iconMenu       = $('icon-menu');
const iconClose      = $('icon-close');
const overlayEl      = $('overlay');
const searchEl       = $('search');
const chapterListEl  = $('chapter-list');
const sidebarFooter  = $('sidebar-footer');
const statsText      = $('stats-text');
const subtitle       = $('subtitle');
const runBtn         = $('run-btn');
const copyBtn        = $('copy-btn');

// 챕터 정보 카드
const chapterInfo    = $('chapter-info');
const infoId         = $('info-id');
const infoTitle      = $('info-title');
const infoTopic      = $('info-topic');
const infoLesson     = $('info-lesson');

// 탭 패널
const sourceCode        = $('source-code');
const sourcePre         = $('source-pre');
const sourceFilename    = $('source-filename');
const resultJson        = $('result-json');
const resultCards       = $('result-cards');
const resultContent     = $('result-content');
const resultStdout      = $('result-stdout');
const stdoutPre         = $('stdout-pre');
const resultError       = $('result-error');
const resultPlaceholder = $('result-placeholder');
const errorMsg          = $('error-msg');
const elapsedBadge      = $('elapsed-badge');
const elapsedMs         = $('elapsed-ms');
const readmeContent     = $('readme-content');
const loadingOverlay    = $('loading-overlay');
const loadingMsg        = $('loading-msg');

// ── 상태 ────────────────────────────────────────────────────────────────────
let currentChapterId = null;
let currentMode      = 'chapter';   // 'chapter' | 'doc'
let allChapters      = [];
let allDocs          = [];

// ── 모듈 그룹 정의 (chapter번호 범위로 구분) ──────────────────────────────
const MODULE_GROUPS = [
  { label: '모듈 1: Python & 데이터 기초',    range: [1,  5]  },
  { label: '모듈 2: 데이터 분석 & 전처리',    range: [6,  15] },
  { label: '모듈 3: 머신러닝 기초',           range: [16, 20] },
  { label: '모듈 4: 딥러닝 기초',             range: [21, 30] },
  { label: '모듈 5: 심화 / 확장 토픽',        range: [31, 99] },
  { label: '모듈 6: 퀀트 ML/DL 실전',         range: [100, 114] },
];

function getGroupLabel(chapterId) {
  const num = parseInt(chapterId.replace('chapter', ''), 10);
  const g = MODULE_GROUPS.find(({ range }) => num >= range[0] && num <= range[1]);
  return g ? g.label : '기타';
}

// ── 사이드바 토글 ─────────────────────────────────────────────────────────
function setSidebar(open) {
  sidebarEl.classList.toggle('-translate-x-full', !open);
  sidebarEl.classList.toggle('translate-x-0', open);
  iconMenu.classList.toggle('hidden', open);
  iconClose.classList.toggle('hidden', !open);
  overlayEl.classList.toggle('hidden', !open);
}

toggleBtn.addEventListener('click', () => {
  const isHidden = sidebarEl.classList.contains('-translate-x-full');
  setSidebar(isHidden);
});
overlayEl.addEventListener('click', () => setSidebar(false));

// ── 로딩 오버레이 ─────────────────────────────────────────────────────────
function showLoading(msg = '처리 중…') {
  loadingMsg.textContent = msg;
  loadingOverlay.classList.remove('hidden');
}
function hideLoading() {
  loadingOverlay.classList.add('hidden');
}

// ── 탭 전환 ───────────────────────────────────────────────────────────────
$$('.tab-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    $$('.tab-btn').forEach((b) => {
      b.classList.toggle('active', b === btn);
      b.classList.toggle('border-indigo-500', b === btn);
      b.classList.toggle('text-indigo-400', b === btn);
      b.classList.toggle('border-transparent', b !== btn);
      b.classList.toggle('text-slate-400', b !== btn);
    });
    $$('.tab-panel').forEach((p) => p.classList.toggle('hidden', p.id !== `tab-${tab}`));
  });
});

function activateTab(tabName) {
  const btn = document.querySelector(`[data-tab="${tabName}"]`);
  if (btn) btn.click();
}

// ── 코드 복사 ─────────────────────────────────────────────────────────────
copyBtn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(sourceCode.textContent);
  copyBtn.textContent = '복사됨!';
  setTimeout(() => { copyBtn.innerHTML = `<svg class="w-3.5 h-3.5 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg> 복사`; }, 2000);
});

// ── 결과 렌더링 헬퍼 ──────────────────────────────────────────────────────

/**
 * 단일 키-값 쌍을 카드 형태로 렌더링합니다.
 * 값 타입에 따라 배지 색상과 레이아웃을 다르게 표시합니다.
 */
function renderResultCard(key, value) {
  const card = document.createElement('div');
  card.className = 'flex items-start gap-3 bg-slate-800/60 border border-slate-700 rounded-lg px-4 py-2.5';

  const keyEl = document.createElement('span');
  keyEl.className = 'flex-none font-mono text-xs text-indigo-300 pt-0.5 min-w-[120px]';
  keyEl.textContent = key;
  card.appendChild(keyEl);

  const valEl = document.createElement('div');
  valEl.className = 'flex-1 min-w-0';

  if (Array.isArray(value)) {
    // 배열: 첫 10개만 표시하고 나머지는 생략
    const preview = value.slice(0, 10).map(v =>
      typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(4)) : String(v)
    ).join(', ');
    const suffix = value.length > 10 ? ` … (+${value.length - 10}개)` : '';
    valEl.innerHTML = `<span class="text-slate-300 text-sm font-mono">[${preview}${suffix}]</span>
      <span class="ml-2 text-xs text-slate-500">배열 ${value.length}개</span>`;
  } else if (value !== null && typeof value === 'object') {
    // 중첩 객체: 들여쓰기 표시
    valEl.innerHTML = `<pre class="text-xs text-slate-300 font-mono whitespace-pre-wrap break-words bg-slate-900 rounded p-2 border border-slate-700">${JSON.stringify(value, null, 2)}</pre>`;
  } else if (typeof value === 'number') {
    // 숫자: 적절한 소수점 표시 + 색상
    const formatted = Number.isInteger(value) ? value.toLocaleString() : value.toFixed(6);
    const colorClass = value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-slate-300';
    valEl.innerHTML = `<span class="font-mono text-sm font-semibold ${colorClass}">${formatted}</span>`;
  } else if (typeof value === 'boolean') {
    valEl.innerHTML = value
      ? `<span class="bg-green-900/50 text-green-300 border border-green-700 px-2 py-0.5 rounded text-xs font-mono">true ✓</span>`
      : `<span class="bg-red-900/50 text-red-300 border border-red-700 px-2 py-0.5 rounded text-xs font-mono">false ✗</span>`;
  } else {
    // 문자열 / 기타
    valEl.innerHTML = `<span class="text-slate-200 text-sm">${String(value)}</span>`;
  }

  card.appendChild(valEl);
  return card;
}

/**
 * run() 결과 dict 전체를 카드 목록으로 렌더링합니다.
 * chapter / topic 키는 헤더로 따로 표시합니다.
 */
function renderResultCards(result) {
  resultCards.innerHTML = '';

  // chapter + topic을 배지로 표시
  const meta = document.createElement('div');
  meta.className = 'flex flex-wrap gap-2 mb-2';
  if (result.chapter) {
    const badge = document.createElement('span');
    badge.className = 'bg-indigo-900/60 text-indigo-300 border border-indigo-700 px-2.5 py-1 rounded-full text-xs font-mono';
    badge.textContent = result.chapter;
    meta.appendChild(badge);
  }
  if (result.topic) {
    const badge = document.createElement('span');
    badge.className = 'bg-slate-700 text-slate-200 px-2.5 py-1 rounded-full text-xs';
    badge.textContent = result.topic;
    meta.appendChild(badge);
  }
  if (meta.children.length) resultCards.appendChild(meta);

  // 나머지 키-값 카드
  const SKIP_KEYS = new Set(['chapter', 'topic']);
  Object.entries(result).forEach(([k, v]) => {
    if (SKIP_KEYS.has(k)) return;
    resultCards.appendChild(renderResultCard(k, v));
  });
}

// ── 실행결과 패널 초기화 ──────────────────────────────────────────────────
function resetResultPanel() {
  resultPlaceholder.classList.remove('hidden');
  resultStdout.classList.add('hidden');
  resultContent.classList.add('hidden');
  resultError.classList.add('hidden');
  elapsedBadge.classList.add('hidden');
  stdoutPre.textContent = '';
  resultCards.innerHTML = '';
  resultJson.textContent = '';
  errorMsg.textContent = '';
}

// ── 챕터 목록 로드 ────────────────────────────────────────────────────────
async function loadChapters() {
  const res = await fetch('/api/chapters');
  allChapters = await res.json();
  renderChapterList(allChapters);
  sidebarFooter.classList.remove('hidden');
  statsText.textContent = `챕터 ${allChapters.length}개`;
}

function renderChapterList(chapters) {
  chapterListEl.innerHTML = '';

  const grouped = {};
  chapters.forEach((c) => {
    const g = getGroupLabel(c.id);
    if (!grouped[g]) grouped[g] = [];
    grouped[g].push(c);
  });

  const orderedGroups = MODULE_GROUPS.map((m) => m.label).filter((l) => grouped[l]);
  const extras = Object.keys(grouped).filter((l) => !orderedGroups.includes(l));

  [...orderedGroups, ...extras].forEach((groupLabel) => {
    // 그룹 헤더
    const header = document.createElement('div');
    header.className = 'px-3 pt-3 pb-1 text-xs font-semibold text-slate-500 uppercase tracking-wider';
    header.textContent = groupLabel;
    chapterListEl.appendChild(header);

    grouped[groupLabel].forEach((c) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.dataset.chapterId = c.id;
      btn.className = [
        'w-full text-left px-3 py-2 rounded-lg text-sm transition',
        'hover:bg-slate-800 text-slate-300 hover:text-slate-100',
        currentChapterId === c.id ? 'bg-indigo-900/40 text-indigo-300 font-medium' : '',
      ].join(' ');
      btn.innerHTML = `<span class="font-mono text-indigo-400 text-xs mr-2">${c.id.replace('chapter','ch')}</span>${c.title || c.topic || c.id}`;
      btn.addEventListener('click', () => {
        selectChapter(c.id);
        setSidebar(false);
      });
      chapterListEl.appendChild(btn);
    });
  });
}

// ── 학습 문서 목록 로드 ───────────────────────────────────────────────────
async function loadDocs() {
  try {
    const res = await fetch('/api/docs');
    if (!res.ok) return;
    allDocs = await res.json();
    renderDocList(allDocs);
  } catch (_) { /* 도큐먼트 API 없으면 무시 */ }
}

function renderDocList(docs) {
  if (!docs.length) return;

  const section = document.createElement('div');
  section.className = 'mt-2 border-t border-slate-800 pt-2';

  const header = document.createElement('div');
  header.className = 'px-3 pt-2 pb-1 text-xs font-semibold text-slate-500 uppercase tracking-wider';
  header.textContent = '📚 모듈 6 학습 문서';
  section.appendChild(header);

  docs.forEach((doc) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'w-full text-left px-3 py-2 rounded-lg text-sm transition hover:bg-slate-800 text-slate-300 hover:text-slate-100';
    btn.innerHTML = `<span class="font-mono text-emerald-400 text-xs mr-2">${doc.id}</span>${doc.title}`;
    btn.addEventListener('click', () => {
      selectDoc(doc.id, doc.title);
      setSidebar(false);
    });
    section.appendChild(btn);
  });

  chapterListEl.appendChild(section);
}

// ── 검색 ──────────────────────────────────────────────────────────────────
searchEl.addEventListener('input', () => {
  const q = searchEl.value.toLowerCase().trim();
  if (!q) {
    renderChapterList(allChapters);
    renderDocList(allDocs);
    return;
  }
  const filtered = allChapters.filter(
    (c) => c.id.includes(q) || (c.title || '').toLowerCase().includes(q) || (c.topic || '').toLowerCase().includes(q)
  );
  renderChapterList(filtered);
});

// ── 챕터 선택 ────────────────────────────────────────────────────────────
async function selectChapter(chapterId) {
  currentChapterId = chapterId;
  currentMode = 'chapter';
  runBtn.disabled = false;

  // 사이드바 활성화 표시 갱신
  $$('[data-chapter-id]').forEach((b) => {
    b.classList.toggle('bg-indigo-900/40', b.dataset.chapterId === chapterId);
    b.classList.toggle('text-indigo-300', b.dataset.chapterId === chapterId);
    b.classList.toggle('font-medium', b.dataset.chapterId === chapterId);
  });

  showLoading('소스 로딩 중…');
  try {
    const [detailRes, sourceRes] = await Promise.all([
      fetch(`/api/chapters/${chapterId}`),
      fetch(`/api/chapters/${chapterId}/source`),
    ]);
    const detail = await detailRes.json();
    const src    = await sourceRes.json();

    // 챕터 정보 카드
    chapterInfo.classList.remove('hidden');
    infoId.textContent    = chapterId;
    infoTitle.textContent = detail.title || '';
    if (detail.topic) {
      infoTopic.textContent = detail.topic;
      infoTopic.classList.remove('hidden');
    } else {
      infoTopic.classList.add('hidden');
    }
    if (detail.lesson_10min) {
      infoLesson.textContent = `💡 ${detail.lesson_10min}`;
      infoLesson.classList.remove('hidden');
    } else {
      infoLesson.classList.add('hidden');
    }
    subtitle.textContent = detail.title || chapterId;

    // 소스코드 표시
    sourceFilename.textContent = 'practice.py';
    sourceCode.textContent = src.source;
    if (window.Prism) Prism.highlightElement(sourceCode);

    // README 표시
    readmeContent.innerHTML = detail.readme
      ? (window.marked ? marked.parse(detail.readme) : `<pre>${detail.readme}</pre>`)
      : '<p class="text-slate-500">README가 없습니다.</p>';

    // 결과 패널 초기화
    resetResultPanel();

    activateTab('source');
  } catch (e) {
    subtitle.textContent = '로딩 실패';
  } finally {
    hideLoading();
  }
}

// ── 학습 문서 선택 ────────────────────────────────────────────────────────
async function selectDoc(docId, docTitle) {
  currentMode = 'doc';
  currentChapterId = null;
  runBtn.disabled = true;

  chapterInfo.classList.remove('hidden');
  infoId.textContent    = docId + '.md';
  infoTitle.textContent = docTitle || docId;
  infoTopic.classList.add('hidden');
  infoLesson.classList.add('hidden');
  subtitle.textContent  = docTitle || docId;
  sourceFilename.textContent = docId + '.md';

  showLoading('문서 로딩 중…');
  try {
    const res = await fetch(`/api/docs/${docId}`);
    const doc = await res.json();

    sourceCode.textContent = doc.content;
    if (window.Prism) Prism.highlightElement(sourceCode);

    readmeContent.innerHTML = doc.content
      ? (window.marked ? marked.parse(doc.content) : `<pre>${doc.content}</pre>`)
      : '<p class="text-slate-500">내용이 없습니다.</p>';

    activateTab('readme');
  } catch (e) {
    readmeContent.innerHTML = '<p class="text-red-400">문서를 불러오지 못했습니다.</p>';
    activateTab('readme');
  } finally {
    hideLoading();
  }
}

// ── 실행 ─────────────────────────────────────────────────────────────────
runBtn.addEventListener('click', async () => {
  if (!currentChapterId || currentMode !== 'chapter') return;
  showLoading('실행 중…');
  activateTab('result');
  resetResultPanel();
  resultPlaceholder.classList.add('hidden');

  try {
    const res  = await fetch(`/api/chapters/${currentChapterId}/run`, { method: 'POST' });
    const data = await res.json();

    if (!res.ok) {
      errorMsg.textContent = data.detail || JSON.stringify(data);
      resultError.classList.remove('hidden');
    } else {
      // ── stdout (print 출력) 표시 ────────────────────────────────────
      if (data.stdout && data.stdout.trim()) {
        stdoutPre.textContent = data.stdout;
        resultStdout.classList.remove('hidden');
      }

      // ── run() 반환값 구조화 표시 ────────────────────────────────────
      if (data.result && Object.keys(data.result).length > 0) {
        renderResultCards(data.result);
        resultJson.textContent = JSON.stringify(data.result, null, 2);
        resultContent.classList.remove('hidden');
      }

      // stdout도 result도 없으면 빈 결과 안내
      if ((!data.stdout || !data.stdout.trim()) && (!data.result || !Object.keys(data.result).length)) {
        resultPlaceholder.classList.remove('hidden');
        const hint = resultPlaceholder.querySelector('p');
        if (hint) hint.textContent = '실행 완료 — 출력이 없습니다.';
      }

      // ── 소요 시간 배지 ───────────────────────────────────────────────
      elapsedMs.textContent = data.elapsed_ms;
      elapsedBadge.classList.remove('hidden');
    }
  } catch (e) {
    errorMsg.textContent = e.message;
    resultError.classList.remove('hidden');
  } finally {
    hideLoading();
  }
});

// ── 초기화 ────────────────────────────────────────────────────────────────
(async () => {
  await loadChapters();
  await loadDocs();
})();
