/* =====================================================================
   NeuralNetViz — Canvas-based neural network forward-pass simulator
   Used by: hotel_stock.html, stock_lab.html
   ===================================================================== */

class NeuralNetViz {
  /**
   * @param {HTMLCanvasElement} canvasEl
   * @param {Object} vizData  — shape returned by backend nn_viz field
   */
  constructor(canvasEl, vizData) {
    this.canvas = canvasEl;
    this.ctx    = canvasEl.getContext("2d");
    this.data   = vizData;
    this.sampleIdx  = 0;
    this.activeStep = -1;   // -1 = initial (all grey), 0..n-1 = layers activated
    this._timer = null;
    this._computeLayout();
    this._draw(-1);
  }

  // ── layout ─────────────────────────────────────────────────────────

  _computeLayout() {
    const d  = this.data;
    const nl = d.layer_sizes.length;
    const disp = d.display_indices;

    const R     = 14;   // neuron radius
    const VGAP  = 44;   // vertical gap between neuron centres
    const HGAP  = 150;  // horizontal gap between layer centres
    const LPAD  = 82;   // left pad (input labels)
    const RPAD  = 115;  // right pad (output label)
    const TPAD  = 30;
    const BPAD  = 60;   // bottom pad (layer labels + full-size text)

    const maxCnt = Math.max(...disp.map(d => d.length));
    const W = LPAD + (nl - 1) * HGAP + RPAD;
    const H = TPAD + BPAD + (maxCnt - 1) * VGAP + R * 2;

    this.canvas.width  = W;
    this.canvas.height = H;

    this._R    = R;
    this._LPAD = LPAD;
    this._TPAD = TPAD;
    this._VGAP = VGAP;
    this._HGAP = HGAP;
    this._BPAD = BPAD;

    // Neuron positions [layer][neuron] = {x, y}
    this._pos = [];
    for (let l = 0; l < nl; l++) {
      const cnt    = disp[l].length;
      const x      = LPAD + l * HGAP;
      const totalH = (cnt - 1) * VGAP;
      const startY = TPAD + R + ((H - TPAD - BPAD - R * 2) - totalH) / 2;
      const layer  = [];
      for (let k = 0; k < cnt; k++) {
        layer.push({ x, y: startY + k * VGAP });
      }
      this._pos.push(layer);
    }
  }

  // ── public API ──────────────────────────────────────────────────────

  reset() {
    if (this._timer) { clearTimeout(this._timer); this._timer = null; }
    this.activeStep = -1;
    this._draw(-1);
  }

  setSample(idx) {
    this.sampleIdx = idx;
    this.reset();
  }

  startAnim(speedMs = 700) {
    if (this._timer) { clearTimeout(this._timer); this._timer = null; }
    const nl = this.data.layer_sizes.length;
    this.activeStep = 0;
    const tick = () => {
      this._draw(this.activeStep);
      if (this.activeStep < nl - 1) {
        this.activeStep++;
        this._timer = setTimeout(tick, speedMs);
      } else {
        this._timer = null;
      }
    };
    tick();
  }

  stepForward() {
    if (this._timer) { clearTimeout(this._timer); this._timer = null; }
    const nl = this.data.layer_sizes.length;
    if (this.activeStep < nl - 1) this.activeStep++;
    this._draw(this.activeStep);
  }

  // ── drawing ─────────────────────────────────────────────────────────

  _draw(activeStep) {
    const ctx    = this.ctx;
    const d      = this.data;
    const sample = d.samples[this.sampleIdx];
    const nl     = d.layer_sizes.length;
    const R      = this._R;

    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // ── connections ───────────────────────────────────────────────────
    for (let l = 0; l < nl - 1; l++) {
      const fromP  = this._pos[l];
      const toP    = this._pos[l + 1];
      const wMat   = d.weight_matrices[l];
      const connActive  = activeStep > l;
      const connAnimating = activeStep === l;

      let maxW = 1e-9;
      for (const row of wMat) for (const w of row) maxW = Math.max(maxW, Math.abs(w));

      for (let f = 0; f < fromP.length; f++) {
        for (let t = 0; t < toP.length; t++) {
          const w     = wMat[f][t];
          const normW = Math.abs(w) / maxW;

          let alpha, lw;
          if (connActive) {
            alpha = normW * 0.65 + 0.05;
            lw    = normW * 2.2 + 0.3;
          } else if (connAnimating) {
            alpha = normW * 0.35 + 0.04;
            lw    = normW * 1.5 + 0.3;
          } else {
            alpha = 0.05;
            lw    = 0.5;
          }

          const clr = w >= 0
            ? `rgba(52,211,153,${alpha.toFixed(3)})`
            : `rgba(251,113,133,${alpha.toFixed(3)})`;

          ctx.beginPath();
          ctx.moveTo(fromP[f].x, fromP[f].y);
          ctx.lineTo(toP[t].x,   toP[t].y);
          ctx.strokeStyle = clr;
          ctx.lineWidth   = lw;
          ctx.stroke();
        }
      }
    }

    // ── neurons ───────────────────────────────────────────────────────
    for (let l = 0; l < nl; l++) {
      const isActive = activeStep >= l && activeStep >= 0;
      const acts     = sample.activations[l];
      const isOut    = l === nl - 1;

      let maxAct = 1e-9;
      for (const a of acts) maxAct = Math.max(maxAct, Math.abs(a));

      for (let k = 0; k < this._pos[l].length; k++) {
        const p       = this._pos[l][k];
        const act     = acts[k];
        const normAct = Math.abs(act) / maxAct;

        // Glow
        if (isActive && normAct > 0.15) {
          const grd = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, R * 2.8);
          const alpha = (normAct * 0.38).toFixed(3);
          const glowClr = isOut
            ? (sample.prob >= 0.5 ? `rgba(52,211,153,${alpha})` : `rgba(251,113,133,${alpha})`)
            : `rgba(99,102,241,${alpha})`;
          grd.addColorStop(0, glowClr);
          grd.addColorStop(1, "rgba(0,0,0,0)");
          ctx.fillStyle = grd;
          ctx.beginPath();
          ctx.arc(p.x, p.y, R * 2.8, 0, Math.PI * 2);
          ctx.fill();
        }

        // Body
        ctx.beginPath();
        ctx.arc(p.x, p.y, R, 0, Math.PI * 2);
        if (isActive) {
          if (isOut) {
            const conf = Math.abs(sample.prob - 0.5) * 2;
            const v = Math.floor(conf * 160);
            ctx.fillStyle = sample.prob >= 0.5
              ? `rgb(20,${80 + v},60)`
              : `rgb(${80 + v},20,30)`;
          } else {
            const v = Math.floor(normAct * 150);
            ctx.fillStyle = `rgb(${20 + v},${30 + Math.floor(v * 0.7)},${80 + v})`;
          }
        } else {
          ctx.fillStyle = "#1e293b";
        }
        ctx.fill();

        ctx.strokeStyle = isActive
          ? (isOut ? (sample.prob >= 0.5 ? "#34d399" : "#fb7185") : "#6366f1")
          : "#334155";
        ctx.lineWidth = isActive ? 1.5 : 0.8;
        ctx.stroke();

        // Value text inside neuron
        if (isActive) {
          ctx.fillStyle = normAct > 0.45 ? "#fff" : "#94a3b8";
          ctx.font = "9px monospace";
          ctx.textAlign    = "center";
          ctx.textBaseline = "middle";
          const txt = isOut
            ? `${(sample.prob * 100).toFixed(0)}%`
            : (Math.abs(act) < 10 ? act.toFixed(2) : act.toFixed(1));
          ctx.fillText(txt, p.x, p.y);
        }
      }

      // Layer label (below last neuron)
      const layerNames = [
        "입력층",
        ...Array.from({ length: nl - 2 }, (_, i) => `은닉층 ${i + 1}`),
        "출력층",
      ];
      const labelColors = [
        "#94a3b8",
        ...Array(nl - 2).fill("#a5b4fc"),
        "#34d399",
      ];
      const bottomY = Math.max(...this._pos[l].map(p => p.y)) + R + 6;

      ctx.fillStyle = labelColors[l];
      ctx.font = "bold 10px monospace";
      ctx.textAlign    = "center";
      ctx.textBaseline = "top";
      ctx.fillText(layerNames[l], this._pos[l][0].x, bottomY);

      const fullSz = d.layer_sizes[l];
      const dispSz = this._pos[l].length;
      if (fullSz > dispSz) {
        ctx.fillStyle = "#475569";
        ctx.font = "9px monospace";
        ctx.fillText(`(${fullSz}개 중 ${dispSz}표시)`, this._pos[l][0].x, bottomY + 13);
      }
    }

    // ── input feature labels ──────────────────────────────────────────
    if (d.input_labels) {
      for (let k = 0; k < this._pos[0].length; k++) {
        const p = this._pos[0][k];
        ctx.fillStyle    = activeStep >= 0 ? "#94a3b8" : "#475569";
        ctx.font         = "9px monospace";
        ctx.textAlign    = "right";
        ctx.textBaseline = "middle";
        ctx.fillText(d.input_labels[k] || "", p.x - R - 5, p.y);
      }
    }

    // ── output prediction label ───────────────────────────────────────
    const nl2 = nl;
    if (activeStep >= nl2 - 1 && activeStep >= 0) {
      const outP = this._pos[nl2 - 1][0];
      const prob = sample.prob;
      ctx.font         = "bold 11px monospace";
      ctx.textAlign    = "left";
      ctx.textBaseline = "middle";
      ctx.fillStyle    = prob >= 0.5 ? "#34d399" : "#fb7185";
      ctx.fillText(
        `${prob >= 0.5 ? "▲ 상승" : "▼ 하락"}  ${(prob * 100).toFixed(1)}%`,
        outP.x + R + 8,
        outP.y,
      );
    }
  }
}

/* ------------------------------------------------------------------
   mountNNViz(containerId, canvasId, vizData)
   — Helper to wire up the NeuralNetViz with standard control buttons.
   Buttons expected inside container:
     #<id>-play   #<id>-step   #<id>-reset
     #<id>-sample-0  #<id>-sample-1
   Speed select (optional): #<id>-speed
   Info text (optional):    #<id>-info
   ------------------------------------------------------------------ */
function mountNNViz(containerId, canvasId, vizData) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const viz = new NeuralNetViz(canvas, vizData);

  const $ = id => document.getElementById(`${containerId}-${id}`);
  const infoEl = $("info");

  function updateInfo() {
    if (!infoEl) return;
    const sample = vizData.samples[viz.sampleIdx];
    const fn     = vizData.activation_fn || "relu";
    const layers = vizData.layer_sizes;
    infoEl.textContent =
      `현재 샘플: ${sample.label}  |  활성화 함수: ${fn}  |  층 구성: ${layers.join(" → ")}`;
  }

  const playBtn = $("play");
  if (playBtn) playBtn.addEventListener("click", () => {
    const speedEl = $("speed");
    const speed = speedEl ? parseInt(speedEl.value, 10) : 700;
    viz.startAnim(speed);
    updateInfo();
  });

  const stepBtn = $("step");
  if (stepBtn) stepBtn.addEventListener("click", () => {
    viz.stepForward();
    updateInfo();
  });

  const resetBtn = $("reset");
  if (resetBtn) resetBtn.addEventListener("click", () => {
    viz.reset();
    updateInfo();
  });

  // Sample selector buttons
  [0, 1].forEach(i => {
    const btn = $(`sample-${i}`);
    if (!btn) return;
    btn.addEventListener("click", () => {
      viz.setSample(i);
      updateInfo();
      // Update active styling
      [0, 1].forEach(j => {
        const b = $(`sample-${j}`);
        if (!b) return;
        const isActive = j === i;
        b.classList.toggle("bg-indigo-600", isActive);
        b.classList.toggle("bg-slate-700",  !isActive);
        b.classList.toggle("text-white",    isActive);
        b.classList.toggle("text-slate-300", !isActive);
      });
    });
  });

  updateInfo();
  return viz;
}
