// Build submission/deck/BEHAVIOR-PROBE.pptx.
// Hard-suite numbers: hosted Valkyrie runs (results/hosted/final.json).
// Easy-suite slide: earlier self-hosted runs (valkyrie/results/final.json).
//   cd submission/deck && NODE_PATH=./node_modules node build_deck.js
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const SKILL = "/Users/vsk/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/c8520d02-9af6-4103-acc8-4cf22680da02/783d3bb0-cb62-4f31-8b06-afdbf9adcf6d/skills/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const ROOT = path.resolve(__dirname, "../..");
const HOSTED = JSON.parse(fs.readFileSync(path.join(ROOT, "results/hosted/final.json"), "utf8"));
const LOCAL = JSON.parse(fs.readFileSync(path.join(ROOT, "valkyrie/results/final.json"), "utf8"));
const F = {
  cells: [...HOSTED.cells.map(c => ({ ...c, dataset: c.condition, gain_per_probe: c.gain_vs_noprobe != null && c.probes_mean ? c.gain_vs_noprobe / c.probes_mean : null })),
          ...LOCAL.cells.filter(c => c.dataset === "noprobe" || c.dataset === "probe10")],
  pairs: HOSTED.pairs,
};
const IDEAL0 = HOSTED.ideal.no_probes;
const IDEAL3 = HOSTED.ideal.three_probes;
const hard = HOSTED.ideal.cases;
const cell = (m, ds) => F.cells.find(c => c.model === m && c.dataset === ds);
const NAMES = { "claude-opus-5-5": "Opus 5.5", "claude-fable-5-2": "Fable 5.2", "claude-sonnet-5-5": "Sonnet 5.5", "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol" };
const MODELS = Object.keys(NAMES).filter(m => cell(m, "hard-probe10"))
  .sort((a, b) => cell(b, "hard-probe10").err_acc - cell(a, "hard-probe10").err_acc);
const P = v => v == null ? "–" : (100 * v).toFixed(0) + "%";
const P1 = v => v == null ? "–" : (100 * v).toFixed(1);
const nOf = ds => Math.max(...F.cells.filter(c => c.dataset === ds).map(c => c.n));
const vals = ds => MODELS.map(m => cell(m, ds) ? +(100 * cell(m, ds).err_acc).toFixed(1) : 0);
const spread = ds => { const v = vals(ds); return Math.max(...v) - Math.min(...v); };
const best = ds => MODELS.map(m => cell(m, ds)).filter(Boolean).sort((a, b) => b.err_acc - a.err_acc)[0];

const THEME = {
  name: "Chalk and Marker", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "17241F", lt1: "FFFFFF", dk2: "2C463B", lt2: "EEF2EF", accent1: "E4572E", accent2: "F2B134",
            accent3: "3E8E8F", accent4: "8A9A93", accent5: "5B7DB1", accent6: "B8C6BF", hlink: "3E8E8F", folHlink: "8A9A93" },
};
const HEX = THEME.colors;
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "BEHAVIOR-PROBE: do agents ask before they assume?";
pres.author = "BEHAVIOR-PROBE";
const C = pres.SchemeColor;

const footer = (color) => [
  { text: { text: "BEHAVIOR-PROBE · Valkyrie benchmark", options: { x: 0.5, y: 5.22, w: 6, h: 0.25, fontSize: 10, color, isTextBox: true, margin: 0 } } },
];
pres.defineSlideMaster({
  title: "Title dark", background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.55, w: 6.2, h: 1.6, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 3.3, w: 6.0, h: 1.0, fontSize: 18, color: C.accent6, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Content light", background: { color: HEX.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.35, w: 9.0, h: 0.75, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text1, valign: "middle", margin: 0 }, text: "" } },
    ...footer(HEX.accent4),
  ],
  slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontSize: 10, color: HEX.accent4, align: "right" },
});
pres.defineSlideMaster({
  title: "Content dark", background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.35, w: 9.0, h: 0.75, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.background1, valign: "middle", margin: 0 }, text: "" } },
    ...footer(HEX.accent6),
  ],
  slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontSize: 10, color: HEX.accent6, align: "right" },
});

const T = (slide, text, o) => slide.addText(text, { isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, ...o });
const card = (slide, x, y, w, h, fill, name) => slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill }, objectName: name });
const chalk = (slide, x, y, a, b, ans, wrong, color, size = 20) => {
  // a little column-subtraction "board" with the student's answer
  T(slide, [{ text: String(a), options: { breakLine: true } }, { text: "− " + b, options: { breakLine: true } }, { text: String(ans), options: { color: wrong ? HEX.accent1 : color, bold: true } }],
    { x, y, w: 1.5, h: 1.25, fontFace: "Courier New", fontSize: size, color, align: "right", valign: "top" });
};
const chartBase = (title) => ({
  showTitle: false, catAxisLabelColor: HEX.dk1, valAxisLabelColor: HEX.accent4, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 12, valAxisLabelFontSize: 10, valGridLine: { color: "E3E8E5", size: 0.75 }, catGridLine: { style: "none" },
  valAxisMinVal: 0, valAxisMaxVal: 100, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 10, dataLabelColor: HEX.dk1,
  showValue: true, dataLabelFormatCode: "0", valAxisLabelFormatCode: "0\"%\"",
});

/* 1 · Title */
pres.addSection({ title: "Opening" });
let s = pres.addSlide({ masterName: "Title dark", sectionTitle: "Opening" });
s.addText("Do agents ask before they assume?", { placeholder: "title" });
s.addText("BEHAVIOR-PROBE: a Valkyrie benchmark for active hypothesis testing", { placeholder: "body" });
card(s, 7.2, 1.2, 2.3, 3.1, HEX.dk2, "board");
chalk(s, 7.55, 1.45, 477, 48, 339, true, HEX.lt1, 24);
T(s, "correct: 429", { x: 7.45, y: 2.85, w: 1.8, h: 0.3, fontSize: 12, color: HEX.accent6, align: "right" });
T(s, "Predict this student's next mistake, or ask first?", { x: 7.45, y: 3.3, w: 1.85, h: 0.8, fontSize: 12, italic: true, color: HEX.accent2, align: "right" });
s.addNotes("BEHAVIOR-PROBE tests one skill: noticing that your evidence fits several explanations, and asking the question that tells them apart. The example is a real hard-suite student: 477 minus 48 should be 429, but this student writes 339.");

/* 2 · Problem + headline */
pres.addSection({ title: "Why" });
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Why" });
s.addText("Agents guess when they should ask", { placeholder: "title" });
T(s, [
  { text: "Real tasks arrive underspecified", options: { bold: true, breakLine: true } },
  { text: "A good agent notices when the evidence fits several explanations, then asks the cheapest question that tells them apart.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 8 } },
  { text: "Most benchmarks can't see this", options: { bold: true, breakLine: true } },
  { text: "They hand over everything up front, or grade only the final answer.", options: {} },
], { x: 0.5, y: 1.35, w: 4.3, h: 3.4, fontSize: 15, color: HEX.dk1, valign: "top", paraSpaceAfter: 4 });
const b0 = best("hard-noprobe"), b10 = best("hard-probe10");
[[b0.err_acc, "best model, no probes", HEX.accent4], [b10.err_acc, "best model, ≤10 optional probes", HEX.accent3], [IDEAL3, "ideal reasoner, 3 probes", HEX.accent1]].forEach(([v, lbl, col], i) => {
  const y = 1.3 + i * 1.2;
  card(s, 5.3, y, 4.2, 1.05, HEX.lt2, "stat" + i);
  T(s, P(v), { x: 5.5, y: y + 0.12, w: 1.7, h: 0.8, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: col, valign: "middle" });
  T(s, lbl, { x: 7.25, y: y + 0.12, w: 2.1, h: 0.8, fontSize: 14, color: HEX.dk1, valign: "middle" });
});
T(s, "Hard suite, accuracy on the questions where the student errs.", { x: 5.3, y: 4.9, w: 4.2, h: 0.25, fontSize: 10, color: HEX.accent4 });
s.addNotes(`Headline numbers, all on the hard suite. Best model without probes: ${P1(b0.err_acc)}%. Best with up to 10 optional probes: ${P1(b10.err_acc)}%. An ideal reasoner reaches ${P1(IDEAL3)}% with just 3 well-chosen probes.`);

/* 3 · Task */
pres.addSection({ title: "Benchmark" });
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Benchmark" });
s.addText("The task: predict one student's mistakes", { placeholder: "title" });
const steps = [
  ["1", "Observe", "4–6 past answers from one simulated student with a hidden buggy procedure"],
  ["2", "Probe (optional)", "Ask the student any new problem, up to the budget. The host enforces it and refuses test questions."],
  ["3", "Predict", "Answer and confidence for 40 new problems: what this student will write, not the correct answer"],
];
steps.forEach(([n, h, d], i) => {
  const x = 0.5 + i * 3.1;
  card(s, x, 1.35, 2.85, 2.25, HEX.lt2, "step" + n);
  s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: 1.55, w: 0.5, h: 0.5, fill: { color: i === 1 ? HEX.accent2 : HEX.dk2 }, line: { color: i === 1 ? HEX.accent2 : HEX.dk2 }, objectName: "num" + n });
  T(s, n, { x: x + 0.2, y: 1.55, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: i === 1 ? HEX.dk1 : HEX.lt1, align: "center", valign: "middle" });
  T(s, h, { x: x + 0.85, y: 1.55, w: 1.9, h: 0.5, fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: HEX.dk1, valign: "middle" });
  T(s, d, { x: x + 0.2, y: 2.2, w: 2.45, h: 1.3, fontSize: 13, color: HEX.dk1, valign: "top" });
});
T(s, "Scored on the 20 questions per case where the student errs. Correct arithmetic earns nothing.", { x: 0.5, y: 3.85, w: 9, h: 0.35, fontSize: 14, bold: true, color: HEX.accent1 });
T(s, "Example student (H001):  477 − 48 → 339   ·   821 − 42 → 689   ·   432 − 400 → 32", { x: 0.5, y: 4.3, w: 9, h: 0.35, fontFace: "Courier New", fontSize: 12, color: HEX.dk2 });
s.addNotes("Each case is one simulated student. The agent sees a few of their past answers, can optionally probe, then predicts 40 answers with confidences. We score only the questions where the student is wrong, so getting the arithmetic right earns nothing; the agent has to model the bug.");

/* 4 · Two suites */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Benchmark" });
s.addText("Two suites, the hard one ambiguous by design", { placeholder: "title" });
const rows = [["", "Easy", "Hard"], ["Possible students", "13 textbook bugs", "2,304 (2 interacting bugs)"], ["Cases", "20", String(hard.length)],
  ["Observations", "6", "4, chosen so many students fit"], ["Test questions", "random, 3–4 digits", "contested, 3–5 digits"], ["Validity", "–", "no impossible steps"]];
s.addTable(rows.map((r, i) => r.map((t, j) => ({ text: t, options: { bold: i === 0 || j === 0, color: i === 0 ? HEX.lt1 : HEX.dk1, fill: { color: i === 0 ? (j === 2 ? HEX.accent1 : HEX.dk2) : (i % 2 ? HEX.lt2 : HEX.lt1) } } }))),
  { x: 0.5, y: 1.35, w: 5.6, colW: [1.7, 1.6, 2.3], fontSize: 13, fontFace: THEME.bodyFontFace, border: { type: "none" }, rowH: 0.48, valign: "middle" });
card(s, 6.5, 1.35, 3.0, 2.9, HEX.dk2, "why-hard");
T(s, [{ text: "Why it's hard", options: { bold: true, fontSize: 16, color: HEX.accent2, breakLine: true } },
  { text: "Recognizing a famous bug doesn't help. The agent has to keep several rules in mind, and the test questions are exactly where those rules disagree.", options: { color: HEX.lt1, fontSize: 13 } }],
  { x: 6.75, y: 1.55, w: 2.55, h: 2.5, valign: "top", paraSpaceAfter: 6 });
s.addNotes("The easy suite reuses 13 classic bugs from the education literature and gets solved quickly. The hard suite combines two interacting bugs out of 2,304 possibilities, shows only 4 observations chosen to be ambiguous, and asks test questions where the students that fit those observations disagree.");

/* 5 · Ceiling */
s = pres.addSlide({ masterName: "Content dark", sectionTitle: "Benchmark" });
s.addText("Hard, but provably solvable", { placeholder: "title" });
[[IDEAL0, "ideal reasoner from the 4 observations alone"], [IDEAL3, "ideal reasoner after 3 greedy probes"]].forEach(([v, lbl], i) => {
  const x = 0.5 + i * 3.0;
  T(s, P(v), { x, y: 1.5, w: 2.8, h: 1.2, fontFace: THEME.headFontFace, fontSize: 60, bold: true, color: i ? HEX.accent2 : HEX.lt1 });
  T(s, lbl, { x, y: 2.75, w: 2.6, h: 0.7, fontSize: 14, color: HEX.accent6, valign: "top" });
});
T(s, [{ text: "Every case stores its own ceiling.", options: { bold: true, breakLine: true, color: HEX.lt1 } },
  { text: "A Bayesian reasoner over all 2,304 students computes the best achievable score, so a low agent score can be read as the agent failing, not the task being impossible.", options: { color: HEX.accent6 } }],
  { x: 6.6, y: 1.55, w: 2.9, h: 2.6, fontSize: 14, valign: "top", paraSpaceAfter: 6 });
s.addNotes(`For each hard case we compute an ideal reasoner: a uniform prior over all 2,304 students and a majority vote among those consistent with the evidence. From the observations alone it scores ${P1(IDEAL0)}% on average. After 3 probes chosen to split the remaining students most evenly, it scores ${P1(IDEAL3)}%.`);

/* 6 · Isolation */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Benchmark" });
s.addText("The grader never enters the sandbox", { placeholder: "title" });
const box = (x, y, w, h, fill, head, lines, name, ink = HEX.dk1) => {
  card(s, x, y, w, h, fill, name);
  T(s, [{ text: head, options: { bold: true, fontSize: 14, breakLine: true } }, ...lines.map((l, i) => ({ text: l, options: { fontSize: 12, breakLine: i < lines.length - 1 } }))],
    { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: h - 0.24, color: ink, valign: "top", paraSpaceAfter: 2 });
};
box(0.5, 1.4, 2.7, 2.6, HEX.lt2, "Agent container", ["Claude Code or Codex", "instruction.md (public)", "probe client", "no internet but model APIs"], "sandbox");
box(3.75, 1.4, 2.7, 1.2, HEX.dk2, "Oracle sidecar", ["holds the rule · budget · refuses test Qs"], "probe", HEX.lt1);
box(3.75, 2.8, 2.7, 1.2, HEX.dk2, "Harbor verifier", ["answer key arrives after the agent"], "service", HEX.lt1);
box(7.0, 1.4, 2.5, 2.6, HEX.lt2, "Never in the agent's container", ["hidden rule", "answer key", "grader", "probe log"], "private");
s.addShape(pres.shapes.LINE, { x: 3.2, y: 2.0, w: 0.55, h: 0, line: { color: HEX.accent1, width: 2, endArrowType: "triangle" }, objectName: "a1" });
s.addShape(pres.shapes.LINE, { x: 3.2, y: 3.4, w: 0.55, h: 0, line: { color: HEX.accent3, width: 2, beginArrowType: "triangle" }, objectName: "a2" });
s.addShape(pres.shapes.LINE, { x: 6.45, y: 2.7, w: 0.55, h: 0, line: { color: HEX.accent4, width: 2, beginArrowType: "triangle", endArrowType: "triangle" }, objectName: "a3" });
T(s, "Harbor tasks on hosted Valkyrie, Modal sandboxes, Claude Code and Codex harnesses.", { x: 0.5, y: 4.35, w: 9, h: 0.5, fontSize: 13, color: HEX.dk2 });
s.addNotes("Each task is a Harbor task on Valkyrie, run on Modal. The agent container holds only the public instruction. The hidden rule lives in an oracle sidecar that answers probes, enforces the budget, refuses test questions and logs every probe. The answer key and grader are copied in only after the agent finishes.");

/* 7 · No probes */
pres.addSection({ title: "Results" });
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Results" });
s.addText("Without probes, every model stalls", { placeholder: "title" });
s.addChart(pres.charts.BAR, [{ name: "No probes", labels: MODELS.map(m => NAMES[m]), values: vals("hard-noprobe") }],
  { ...chartBase(), x: 0.4, y: 1.25, w: 5.6, h: 3.75, barDir: "col", chartColors: [HEX.accent4], showLegend: false, dataLabelPosition: "outEnd" });
const n0 = nOf("hard-noprobe");
T(s, [{ text: `Ideal reasoner: ${P(IDEAL0)}`, options: { bold: true, color: HEX.accent1, fontSize: 18, breakLine: true } },
  { text: `Every model is below the ceiling the observations allow. They settle on one rule that fits instead of weighing the alternatives.`, options: { color: HEX.dk1, fontSize: 14, breakLine: true } },
  { text: " ", options: { fontSize: 6, breakLine: true } },
  { text: `Spread across models: ${spread("hard-noprobe").toFixed(0)} pts. With n = ${n0}, the 95% CIs overlap, so the models are statistically tied.`, options: { color: HEX.accent4, fontSize: 12 } }],
  { x: 6.3, y: 1.4, w: 3.2, h: 3.4, valign: "top", paraSpaceAfter: 4 });
s.addNotes(`Hard suite, no probe tool, n = ${n0} cases per model. Accuracy on error questions: ` + MODELS.map(m => `${NAMES[m]} ${P1(cell(m, "hard-noprobe").err_acc)}% (95% CI ${P1(cell(m, "hard-noprobe").ci95[0])}–${P1(cell(m, "hard-noprobe").ci95[1])})`).join("; ") + ".");

/* 8 · Probes split the field */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Results" });
s.addText("Optional probes split the field", { placeholder: "title" });
const series = [["No probes", "hard-noprobe"], ["≤3 probes", "hard-probe3"], ["≤10 probes", "hard-probe10"]].filter(([, ds]) => MODELS.some(m => cell(m, ds)));
s.addChart(pres.charts.BAR, series.map(([name, ds]) => ({ name, labels: MODELS.map(m => NAMES[m]), values: vals(ds) })),
  { ...chartBase(), x: 0.4, y: 1.2, w: 9.2, h: 3.55, barDir: "col", barGrouping: "clustered", chartColors: [HEX.accent4, HEX.accent2, HEX.accent3].slice(0, series.length),
    showLegend: true, legendPos: "t", legendFontFace: "+mn-lt", legendFontSize: 12, legendColor: HEX.dk1, dataLabelPosition: "outEnd", dataLabelFontSize: 9 });
T(s, `With 10 optional probes, scores spread over ${spread("hard-probe10").toFixed(0)} points, against ${spread("hard-noprobe").toFixed(0)} without probes.`, { x: 0.5, y: 4.8, w: 9, h: 0.35, fontSize: 13, bold: true, color: HEX.dk1 });
s.addNotes(`Same ${hard.length} hard cases, both conditions. ` + MODELS.map(m => `${NAMES[m]}: ${series.map(([n, ds]) => `${n} ${P1(cell(m, ds)?.err_acc)}%`).join(", ")}`).join(". ") + ".");

/* 9 · Who probes */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Results" });
s.addText("Who chooses to probe", { placeholder: "title" });
s.addChart(pres.charts.BAR, [{ name: "Probes per task", labels: MODELS.map(m => NAMES[m]), values: MODELS.map(m => +cell(m, "hard-probe10").probes_mean.toFixed(1)) }],
  { ...chartBase(), x: 0.4, y: 1.25, w: 5.6, h: 3.75, barDir: "bar", chartColors: MODELS.map(m => m === "claude-sonnet-5-5" ? HEX.accent1 : HEX.accent3),
    valAxisMaxVal: 10, valAxisLabelFormatCode: "0", dataLabelFormatCode: "0.0", showLegend: false, dataLabelPosition: "outEnd" });
const son = cell("claude-sonnet-5-5", "hard-probe10");
T(s, [{ text: son ? `Sonnet 5.5 probed in ${son.cases_probed} of ${son.n} cases` : "", options: { bold: true, color: HEX.accent1, fontSize: 18, breakLine: true } },
  { text: `and gained only ${P1(son.gain_vs_noprobe)} points over no probes. The other models probed in nearly every case.`, options: { color: HEX.dk1, fontSize: 14, breakLine: true } },
  { text: " ", options: { fontSize: 6, breakLine: true } },
  { text: "Same instruction for every model: probing is \"entirely up to you\".", options: { color: HEX.accent4, fontSize: 12, italic: true } }],
  { x: 6.3, y: 1.4, w: 3.2, h: 3.4, valign: "top", paraSpaceAfter: 4 });
s.addNotes("Hard suite with up to 10 optional probes: average probes per task. " + MODELS.map(m => `${NAMES[m]} ${cell(m, "hard-probe10").probes_mean.toFixed(2)} probes, probed in ${cell(m, "hard-probe10").cases_probed}/${cell(m, "hard-probe10").n} cases`).join("; ") + ".");

/* 9b · Concrete failure */
const FX = JSON.parse(fs.readFileSync(path.join(ROOT, "docs/failure_example.json"), "utf8"));
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Results" });
s.addText(`Case ${FX.case}: ${P(FX.no_probe)} to ${P(FX.with_probes)} by asking`, { placeholder: "title" });
const obsRows = [["Observed", "Student", "Correct"], ...FX.observations.map(o => [`${o.a} − ${o.b}`, String(o.student_answer), String(o.a - o.b)])];
s.addTable(obsRows.map((r, i) => r.map((t, j) => ({ text: t, options: { bold: i === 0 || j === 1, color: i === 0 ? HEX.lt1 : (j === 1 && i > 0 && +t !== +r[2] ? HEX.accent1 : HEX.dk1), fontFace: i ? "Courier New" : THEME.bodyFontFace, align: j ? "right" : "left", fill: { color: i === 0 ? HEX.dk2 : HEX.lt2 } } }))),
  { x: 0.5, y: 1.3, w: 3.6, colW: [1.6, 1.0, 1.0], fontSize: 13, border: { type: "none" }, rowH: 0.4, valign: "middle" });
T(s, "Four answers fit many rules.", { x: 0.5, y: 3.4, w: 3.6, h: 0.35, fontSize: 13, italic: true, color: HEX.accent4 });
const fxCards = [
  [P(FX.no_probe), `${FX.model_name}, no probes`, "Picked a rule that fit all 4 answers and applied it confidently.", HEX.accent4],
  [P(FX.with_probes), `${FX.model_name}, ${FX.probes_used} probes`, "Tested its guess on new problems, found the real rule, got every error right.", HEX.accent3],
  [P(FX.low_reward), `${FX.low_model}, ${FX.low_probes} probes`, "Had the same tool, didn't use it, and scored 0.", HEX.accent1],
];
fxCards.forEach(([v, who, what, col], i) => {
  const y = 1.3 + i * 1.2;
  card(s, 4.5, y, 5.0, 1.05, HEX.lt2, "fx" + i);
  T(s, v, { x: 4.65, y: y + 0.12, w: 1.4, h: 0.8, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: col, valign: "middle" });
  T(s, [{ text: who, options: { bold: true, breakLine: true } }, { text: what, options: {} }], { x: 6.1, y: y + 0.1, w: 3.3, h: 0.85, fontSize: 12, color: HEX.dk1, valign: "middle" });
});
T(s, `Hidden rule: when a column needs a borrow, the student ${FX.rule}.`, { x: 0.5, y: 3.85, w: 3.6, h: 0.95, fontSize: 10, color: HEX.accent4, valign: "top" });
s.addNotes(`A real trace from the hosted run. On case ${FX.case}, ${FX.model_name} scored ${P1(FX.no_probe)}% on the student's errors without probes and ${P1(FX.with_probes)}% with ${FX.probes_used} probes. ${FX.low_model} had the same optional tool, used ${FX.low_probes} probes, and scored ${P1(FX.low_reward)}%.`);

/* 10 · Efficiency */
const HEAVY = MODELS.map(m => cell(m, "hard-probe10")).filter(c => c && c.probes_mean >= 8);
s = pres.addSlide({ masterName: "Content dark", sectionTitle: "Results" });
s.addText("Same number of probes, very different results", { placeholder: "title" });
[[b0.err_acc, `best with no probes (${NAMES[b0.model]})`, HEX.accent6], [b10.err_acc, `best with ≤10 probes (${NAMES[b10.model]})`, HEX.lt1], [IDEAL3, "ideal reasoner with 3 probes", HEX.accent2]].forEach(([v, lbl, col], i) => {
  const x = 0.5 + i * 3.05;
  T(s, P(v), { x, y: 1.45, w: 2.8, h: 1.1, fontFace: THEME.headFontFace, fontSize: 52, bold: true, color: col });
  T(s, lbl, { x, y: 2.55, w: 2.7, h: 0.6, fontSize: 13, color: HEX.accent6, valign: "top" });
});
T(s, `${HEAVY.map(c => NAMES[c.model]).join(", ")} use ${Math.min(...HEAVY.map(c => c.probes_mean)).toFixed(1)}–${Math.max(...HEAVY.map(c => c.probes_mean)).toFixed(1)} probes per task, yet score ${Math.min(...HEAVY.map(c => 100 * c.err_acc)).toFixed(0)}–${Math.max(...HEAVY.map(c => 100 * c.err_acc)).toFixed(0)}%. Which problems a model asks about matters more than how many it asks.`,
  { x: 0.5, y: 3.45, w: 9, h: 0.9, fontSize: 15, color: HEX.lt1, valign: "top" });
s.addNotes("Even 10 probes don't get any model near what 3 information-maximizing probes achieve for the ideal reasoner. Gain per probe, in points: " + MODELS.map(m => { const c = cell(m, "hard-probe10"); return `${NAMES[m]} ${c.gain_per_probe != null && c.probes_mean >= 1 ? P1(c.gain_per_probe) : "n/a"}`; }).join("; ") + ".");

/* 11 · Transfer */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Results" });
s.addText("Bigger problems break the fitted rule", { placeholder: "title" });
s.addChart(pres.charts.BAR, [
  { name: "3-digit", labels: MODELS.map(m => NAMES[m]), values: MODELS.map(m => +(100 * cell(m, "hard-probe10").familiar).toFixed(1)) },
  { name: "4–5-digit", labels: MODELS.map(m => NAMES[m]), values: MODELS.map(m => +(100 * cell(m, "hard-probe10").transfer).toFixed(1)) }],
  { ...chartBase(), x: 0.4, y: 1.2, w: 6.2, h: 3.8, barDir: "col", barGrouping: "clustered", chartColors: [HEX.accent3, HEX.accent1], showLegend: true, legendPos: "t",
    legendFontFace: "+mn-lt", legendFontSize: 12, legendColor: HEX.dk1, dataLabelPosition: "outEnd", dataLabelFontSize: 9 });
T(s, [{ text: "Hard suite, ≤10 probes", options: { bold: true, color: HEX.dk1, fontSize: 16, breakLine: true } },
  { text: "Observations are mostly 3-digit. Rules that fit them often aren't checked on larger problems, where extra borrows and zeros trigger behavior the agent never saw.", options: { color: HEX.dk1, fontSize: 14 } }],
  { x: 6.9, y: 1.4, w: 2.6, h: 3.4, valign: "top", paraSpaceAfter: 6 });
s.addNotes("Error-question accuracy on 3-digit vs 4–5-digit questions, hard suite with up to 10 probes. " + MODELS.map(m => `${NAMES[m]} ${P1(cell(m, "hard-probe10").familiar)}% vs ${P1(cell(m, "hard-probe10").transfer)}%`).join("; ") + ".");

/* 12 · Easy suite */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Results" });
s.addText("Easy suite: a sanity check, solved by probing", { placeholder: "title" });
const easyRows = [["Model", "No probes", "≤10 probes", "Probes/task"], ...MODELS.map(m => [NAMES[m], P1(cell(m, "noprobe")?.err_acc) + "%", P1(cell(m, "probe10")?.err_acc) + "%", cell(m, "probe10")?.probes_mean.toFixed(1) ?? "–"])];
s.addTable(easyRows.map((r, i) => r.map((t, j) => ({ text: t, options: { bold: i === 0 || j === 0, color: i === 0 ? HEX.lt1 : HEX.dk1, align: j ? "right" : "left", fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt2 : HEX.lt1) } } }))),
  { x: 0.5, y: 1.35, w: 5.6, colW: [1.9, 1.2, 1.3, 1.2], fontSize: 13, fontFace: THEME.bodyFontFace, border: { type: "none" }, rowH: 0.45, valign: "middle" });
T(s, [{ text: "The 13 textbook bugs are recognizable.", options: { bold: true, breakLine: true } }, { text: "Any model that probes reaches 97–100%. The hard suite is the leaderboard.", options: {} }],
  { x: 6.5, y: 1.45, w: 3.0, h: 2.5, fontSize: 14, color: HEX.dk1, valign: "top", paraSpaceAfter: 6 });
s.addNotes("Easy suite, 20 cases: without probes, models score 72–92% on error questions. With optional probes, every model that actually probes scores 97–100%.");

/* 13 · Integrity + errata */
pres.addSection({ title: "Rigor" });
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Rigor" });
s.addText("How we kept it honest", { placeholder: "title" });
const items = [
  ["Uncertainty", `Bootstrap 95% CIs over cases. Paired bootstrap for model comparisons: ${F.pairs.filter(p => p.significant).length} of ${F.pairs.length} pairs differ significantly.`],
  ["Caught a broken probe tool", "In our first, self-hosted version the probe server collided with the Tracker's own port. Trajectories showed \"Not Found\". We fixed it, then moved the oracle into a Harbor sidecar."],
  ["Validity filter", "Hard cases exclude any item needing an impossible step (digit outside 0–9, or a borrow past the leftmost column). Checked: 0 remain."],
  ["Full audit trail", "Every task's trajectory, probes and grader output are kept in Valkyrie. Run IDs are in the README."],
];
items.forEach(([h, d], i) => {
  const x = 0.5 + (i % 2) * 4.6, y = 1.3 + Math.floor(i / 2) * 1.85;
  card(s, x, y, 4.4, 1.65, HEX.lt2, "rig" + i);
  T(s, [{ text: h, options: { bold: true, fontSize: 15, breakLine: true, color: i === 1 ? HEX.accent1 : HEX.dk1 } }, { text: d, options: { fontSize: 12, color: HEX.dk1 } }],
    { x: x + 0.2, y: y + 0.15, w: 4.0, h: 1.35, valign: "top", paraSpaceAfter: 4 });
});
s.addNotes("We report confidence intervals and paired comparisons rather than raw rankings. We also report our own mistakes. The probe port collision invalidated the first probe runs. We found it in the trajectories, fixed it, and re-ran everything.");

/* 14 · Limitations */
s = pres.addSlide({ masterName: "Content light", sectionTitle: "Rigor" });
s.addText("Limitations and next steps", { placeholder: "title" });
const lim = [["Synthetic students", "Measures hypothesis testing under controlled ambiguity, not tutoring real learners."],
  ["Harness confound", "Claude ran on claude_code, GPT on codex. Next: one shared harness."],
  ["One run per cell", "CIs cover case sampling, not sampling temperature. Next: repeated seeds."],
  ["Free probes", "Next: cost-weighted scoring that rewards the most informative question."]];
lim.forEach(([h, d], i) => {
  const y = 1.3 + i * 0.92;
  s.addShape(pres.shapes.OVAL, { x: 0.5, y: y + 0.08, w: 0.45, h: 0.45, fill: { color: i < 2 ? HEX.accent1 : HEX.accent3 }, line: { color: i < 2 ? HEX.accent1 : HEX.accent3 }, objectName: "lim" + i });
  T(s, String(i + 1), { x: 0.5, y: y + 0.08, w: 0.45, h: 0.45, fontSize: 14, bold: true, color: HEX.lt1, align: "center", valign: "middle" });
  T(s, [{ text: h + "  ", options: { bold: true } }, { text: d, options: {} }], { x: 1.15, y, w: 8.3, h: 0.62, fontSize: 15, color: HEX.dk1, valign: "middle" });
});
s.addNotes("The main limitations: the domain is synthetic, the two providers used different harnesses, each cell is a single run, and probes cost nothing within the budget. Each one has a clear next step.");

/* 15 · Close */
pres.addSection({ title: "Close" });
s = pres.addSlide({ masterName: "Title dark", sectionTitle: "Close" });
s.addText("Asking is the skill", { placeholder: "title" });
s.addText(`Without probes, models stall below ${P(IDEAL0)}. With optional probes they spread over ${spread("hard-probe10").toFixed(0)} points, and none reaches the ${P(IDEAL3)} that 3 good questions earn.`, { placeholder: "body" });
card(s, 7.0, 1.35, 2.5, 2.9, HEX.dk2, "deliver");
T(s, [{ text: "In the submission", options: { bold: true, color: HEX.accent2, fontSize: 14, breakLine: true } },
  { text: "Write-up + run IDs", options: { bullet: true, breakLine: true } }, { text: "README with traces", options: { bullet: true, breakLine: true } },
  { text: "Harbor tasks on Valkyrie", options: { bullet: true, breakLine: true } }, { text: "Interactive HTML report", options: { bullet: true, breakLine: true } }, { text: "Results with 95% CIs", options: { bullet: true } }],
  { x: 7.2, y: 1.55, w: 2.15, h: 2.5, fontSize: 12, color: HEX.lt1, valign: "top", paraSpaceAfter: 4 });
s.addNotes("The takeaway: what separates current agents isn't inference ability, it's whether and how well they gather evidence. Everything needed to reproduce this is in the submission.");

(async () => {
  const out = path.join(__dirname, "BEHAVIOR-PROBE.pptx");
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
