const state = {
  sources: [],
  books: [],
  currentBookId: "",
  currentChunkSourceId: "",
  currentView: "dashboard",
};

const titles = {
  dashboard: ["Dashboard", "本地知识库只读工作台"],
  datasets: ["Datasets", "教材、视觉清单、知识图谱文件概览"],
  chunks: ["Chunks", "查看教材分块、图片引用和原文"],
  visuals: ["Visual Evidence", "查看视觉证据、caption 和原图"],
  query: ["RAG Query", "采集人工 query，运行本地文本/视觉/KG evidence bundle"],
  graph: ["Graph", "搜索 Neo4j 导入前后的本地知识边"],
  reports: ["Eval Reports", "浏览 RAG 与视觉 caption 评测报告"],
};

async function api(path) {
  const response = await fetch(path);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${text}`);
  }
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return response.json();
  return response.text();
}

async function apiJson(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${text}`);
  }
  return response.json();
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function clear(node) {
  node.replaceChildren();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function fileUrl(path) {
  return `/api/file?path=${encodeURIComponent(path)}`;
}

function listText(value) {
  if (Array.isArray(value)) return value.filter(Boolean).join(", ");
  if (value && typeof value === "object") return JSON.stringify(value);
  return value ?? "";
}

function parseTags(value) {
  return String(value || "")
    .split(/[,\s，、]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function setQueryStatus(text) {
  document.getElementById("rag-status").textContent = text || "";
}

function visualExerciseLabel(item) {
  const exercise = item.exercise_number || "";
  const subquestion = item.subquestion_number || "";
  if (!exercise && !subquestion) return "";
  return `练习 ${exercise}${subquestion ? ` / 小题 ${subquestion}` : ""}`;
}

function activate(view) {
  state.currentView = view;
  document.querySelectorAll(".view").forEach((node) => node.classList.remove("active"));
  document.querySelectorAll(".nav-button").forEach((node) => node.classList.remove("active"));
  document.getElementById(view).classList.add("active");
  document.querySelector(`[data-view="${view}"]`).classList.add("active");
  document.getElementById("page-title").textContent = titles[view][0];
  document.getElementById("page-subtitle").textContent = titles[view][1];
  loadView(view);
}

async function loadDashboard() {
  const data = await api("/api/dashboard");
  const metricGrid = document.getElementById("metric-grid");
  clear(metricGrid);
  [
    ["Sources", data.sources],
    ["Chunks", data.chunks],
    ["Visual Items", data.visual_items],
    ["Visual Captions", data.visual_captions],
    ["KG Nodes", data.kg_nodes],
    ["KG Edges", data.kg_edges],
  ].forEach(([label, value]) => {
    const card = el("div", "metric-card");
    card.append(el("span", "", label));
    card.append(el("strong", "", value));
    metricGrid.append(card);
  });

  const relationList = document.getElementById("relation-list");
  clear(relationList);
  data.relations.forEach(([name, count]) => {
    const item = el("div", "stack-item");
    item.innerHTML = `<strong>${escapeHtml(name)}</strong><span>${count} edges</span>`;
    relationList.append(item);
  });

  const collectionList = document.getElementById("collection-list");
  clear(collectionList);
  data.collections.forEach((collection) => {
    const item = el("div", "stack-item");
    item.innerHTML = `<strong>${escapeHtml(collection.name)}</strong><span>${escapeHtml(collection.kind)} · ${collection.docs} docs</span>`;
    collectionList.append(item);
  });
}

async function loadSources() {
  const data = await api("/api/sources");
  state.sources = data.items;
  const table = document.getElementById("dataset-table");
  clear(table);
  const header = el("div", "table-row header");
  header.innerHTML = "<span>Source</span><span>Kind</span><span>Chunks</span><span>Visuals</span><span>KG Edges</span>";
  table.append(header);
  data.items.forEach((item) => {
    const row = el("div", "table-row");
    row.innerHTML = `
      <span><strong>${escapeHtml(item.title)}</strong><br><small class="muted">${escapeHtml(item.source_id)}</small></span>
      <span>${escapeHtml(item.kind)}</span>
      <span>${item.chunks}</span>
      <span>${item.visuals}</span>
      <span>${item.kg_edges}</span>
    `;
    table.append(row);
  });
  document.getElementById("dataset-count").textContent = `${data.items.length} sources`;
  populateSourceSelects(data.items);
}

function populateSourceSelects(items) {
  const visualSelect = document.getElementById("visual-source");
  if (visualSelect.options.length === 0) {
    visualSelect.append(new Option("全部视觉源", ""));
    items.filter((item) => item.kind === "visuals").forEach((item) => {
      visualSelect.append(new Option(item.title, item.source_id));
    });
  }
}

async function loadBooks() {
  const data = await api("/api/books");
  state.books = data.items;
  if (!state.currentBookId && state.books.length) {
    state.currentBookId = state.books[0].book_id;
    state.currentChunkSourceId = "";
  }
  renderBookList();
  renderSourceTabs();
}

function renderBookList() {
  const list = document.getElementById("book-list");
  clear(list);
  state.books.forEach((book) => {
    const card = el("div", "book-card");
    if (book.book_id === state.currentBookId) card.classList.add("active");
    card.innerHTML = `
      <strong>${escapeHtml(book.title)}</strong>
      <p>${escapeHtml(book.description)}</p>
      <div class="badges">
        <span class="badge">${book.chunks} chunks</span>
        <span class="badge">${book.image_refs} images</span>
        <span class="badge">${book.kg_edges} KG</span>
      </div>
    `;
    card.addEventListener("click", () => {
      state.currentBookId = book.book_id;
      state.currentChunkSourceId = "";
      document.getElementById("chunk-query").value = "";
      renderBookList();
      renderSourceTabs();
      loadChunks();
    });
    list.append(card);
  });
}

function renderSourceTabs() {
  const list = document.getElementById("chunk-list");
  const book = state.books.find((item) => item.book_id === state.currentBookId);
  if (!book) return;
  let tabs = list.querySelector(".source-tabs");
  if (!tabs) {
    tabs = el("div", "source-tabs");
  } else {
    clear(tabs);
  }
  const allButton = el("button", "source-tab");
  if (!state.currentChunkSourceId) allButton.classList.add("active");
  allButton.innerHTML = `<strong>全部版本</strong><br><span>${book.chunks} chunks</span>`;
  allButton.addEventListener("click", () => {
    state.currentChunkSourceId = "";
    renderSourceTabs();
    loadChunks();
  });
  tabs.append(allButton);
  book.sources.forEach((source) => {
    const button = el("button", "source-tab");
    if (state.currentChunkSourceId === source.source_id) button.classList.add("active");
    button.innerHTML = `<strong>${escapeHtml(source.title)}</strong><br><span>${source.chunks} chunks · ${source.kg_edges} KG</span>`;
    button.addEventListener("click", () => {
      state.currentChunkSourceId = source.source_id;
      renderSourceTabs();
      loadChunks();
    });
    tabs.append(button);
  });
  return tabs;
}

async function loadChunks() {
  if (!state.sources.length) await loadSources();
  if (!state.books.length) await loadBooks();
  const q = document.getElementById("chunk-query").value.trim();
  const params = new URLSearchParams({ limit: "500" });
  if (state.currentChunkSourceId) {
    params.set("source_id", state.currentChunkSourceId);
  } else if (state.currentBookId) {
    params.set("book_id", state.currentBookId);
  }
  if (q) params.set("q", q);
  const data = await api(`/api/chunks?${params.toString()}`);
  const list = document.getElementById("chunk-list");
  clear(list);
  const tabs = renderSourceTabs();
  if (tabs) list.append(tabs);
  const countLine = el(
    "div",
    "list-note",
    `显示 ${data.items.length} / ${data.total ?? data.items.length} 个 chunk${data.truncated ? "，结果仍被截断" : ""}`
  );
  list.append(countLine);
  data.items.forEach((item) => {
    const row = el("div", "list-item");
    row.innerHTML = `
      <strong>${escapeHtml(item.chunk_id)} · ${escapeHtml(item.source_title)}</strong>
      <p>${escapeHtml(item.preview)}</p>
      <div class="badges">
        <span class="badge">${item.chars} chars</span>
        <span class="badge">${item.image_refs} images</span>
        <span class="badge">${item.kg_edges} KG edges</span>
        <span class="badge">${escapeHtml(item.lesson_title || "no title")}</span>
      </div>
    `;
    row.addEventListener("click", () => showChunk(item.source_id, item.chunk_id, row));
    list.append(row);
  });
  if (!data.items.length) list.append(el("div", "list-item", "没有匹配 chunk"));
}

async function showChunk(sourceId, chunkId, rowNode) {
  document.querySelectorAll("#chunk-list .list-item").forEach((n) => n.classList.remove("active"));
  rowNode.classList.add("active");
  const data = await api(`/api/chunk?source_id=${encodeURIComponent(sourceId)}&chunk_id=${encodeURIComponent(chunkId)}`);
  const pane = document.getElementById("chunk-detail");
  pane.classList.remove("empty");
  const imageRefs = Array.isArray(data.image_refs) ? data.image_refs : [];
  const resolvedImages = Array.isArray(data.resolved_images) ? data.resolved_images : [];
  const kgEdges = Array.isArray(data.kg_edges) ? data.kg_edges : [];
  const imageGrid = resolvedImages.length
    ? `<div class="image-grid">${resolvedImages
        .slice(0, 80)
        .map((image) => {
          const img = image.primary_path
            ? `<img src="${fileUrl(image.primary_path)}" alt="${escapeHtml(image.basename)}" />`
            : `<div class="empty">未解析到图片</div>`;
          const visual = (image.visuals || [])[0];
          return `<div class="image-tile">${img}<div>
            <strong>${escapeHtml(image.basename)}</strong><br>
            ${visual ? `${escapeHtml(visual.image_type || "")} · ${escapeHtml(visual.topic || "")}` : "no visual caption"}
          </div></div>`;
        })
        .join("")}</div>`
    : `<p class="muted">没有解析到图片引用。</p>`;
  const edgeList = kgEdges.length
    ? `<div class="kg-edge-list">${kgEdges
        .map((edge) => {
          const query = encodeURIComponent(edge.source || edge.target || "");
          return `<div class="kg-edge-item">
            <strong>${escapeHtml(edge.source)} -- ${escapeHtml(edge.relation)} -> ${escapeHtml(edge.target)}</strong>
            <p>${escapeHtml(edge.review_note || edge.context_condition || edge.evidence || "")}</p>
            <div class="badges">
              <span class="badge">${escapeHtml(edge.knowledge_type || "unknown")}</span>
              <span class="badge">${escapeHtml(edge.source_group || "")}</span>
              <span class="badge">confidence ${escapeHtml(edge.confidence ?? "")}</span>
            </div>
            <button class="secondary-button graph-jump" data-query="${query}">在图谱中查看</button>
          </div>`;
        })
        .join("")}</div>`
    : `<p class="muted">没有关联到 accepted KG 边。</p>`;
  pane.innerHTML = `
    <h2>${escapeHtml(data.chunk_id)} · ${escapeHtml(data.source_title)}</h2>
    <div class="badges">
      <span class="badge">${escapeHtml(sourceId)}</span>
      <span class="badge">${String(data.text || "").length} chars</span>
      <span class="badge">${imageRefs.length} image refs</span>
      <span class="badge">${kgEdges.length} KG edges</span>
    </div>
    <h3>Resolved Images</h3>
    ${imageGrid}
    <h3>Accepted KG Edges</h3>
    ${edgeList}
    <h3>Text</h3>
    <pre>${escapeHtml(data.text || "")}</pre>
    <h3>Raw Metadata</h3>
    <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
  `;
  pane.querySelectorAll(".graph-jump").forEach((button) => {
    button.addEventListener("click", () => {
      document.getElementById("graph-query").value = decodeURIComponent(button.dataset.query || "");
      activate("graph");
    });
  });
}

async function loadVisuals() {
  if (!state.sources.length) await loadSources();
  const source = document.getElementById("visual-source").value;
  const q = document.getElementById("visual-query").value.trim();
  const params = new URLSearchParams({ limit: "120" });
  if (source) params.set("source_id", source);
  if (q) params.set("q", q);
  const data = await api(`/api/visuals?${params.toString()}`);
  const list = document.getElementById("visual-list");
  clear(list);
  data.items.forEach((item) => {
    const row = el("div", "list-item");
    const exerciseLabel = visualExerciseLabel(item);
    row.innerHTML = `
      <strong>${escapeHtml(item.visual_id || "no visual id")}</strong>
      <p>${escapeHtml(item.caption || item.topic || "")}</p>
      <div class="badges">
        <span class="badge">${escapeHtml(item.visual_source_title || item.visual_source)}</span>
        ${exerciseLabel ? `<span class="badge">${escapeHtml(exerciseLabel)}</span>` : ""}
        <span class="badge">${escapeHtml(item.image_type || "unknown")}</span>
        ${item.musical_object ? `<span class="badge">${escapeHtml(item.musical_object)}</span>` : ""}
      </div>
    `;
    row.addEventListener("click", () => showVisual(item, row));
    list.append(row);
  });
  if (!data.items.length) list.append(el("div", "list-item", "没有匹配视觉证据"));
}

function showVisual(item, rowNode) {
  document.querySelectorAll("#visual-list .list-item").forEach((n) => n.classList.remove("active"));
  rowNode.classList.add("active");
  const pane = document.getElementById("visual-detail");
  pane.classList.remove("empty");
  const image = item.image_path
    ? `<img src="${fileUrl(item.image_path)}" alt="${escapeHtml(item.visual_id)}" />`
    : `<p class="muted">没有 image_path</p>`;
  const exerciseLabel = visualExerciseLabel(item);
  const fields = [
    ["Source", item.visual_source_title || item.visual_source],
    ["Exercise", exerciseLabel],
    ["Evidence", item.evidence_type],
    ["Visual Type", item.visual_type || item.image_type],
    ["Object", item.musical_object || item.topic],
    ["Root", item.root],
    ["Quality / Mode", item.quality_or_mode],
    ["Position / Shape", item.position_or_shape],
    ["Intervals", listText(item.intervals)],
    ["Keywords", listText(item.retrieval_keywords)],
  ].filter(([, value]) => value !== undefined && value !== null && String(value).trim() !== "");
  const fieldRows = fields
    .map(([label, value]) => `<div class="meta-label">${escapeHtml(label)}</div><div>${escapeHtml(value)}</div>`)
    .join("");
  pane.innerHTML = `
    <h2>${escapeHtml(item.visual_id || "Visual Evidence")}</h2>
    <div class="badges">
      <span class="badge">${escapeHtml(item.visual_source_title || item.visual_source)}</span>
      <span class="badge">${escapeHtml(item.image_type || "unknown")}</span>
      ${exerciseLabel ? `<span class="badge">${escapeHtml(exerciseLabel)}</span>` : ""}
      ${item.caption_layer ? `<span class="badge">${escapeHtml(item.caption_layer)}</span>` : ""}
    </div>
    <h3>Image</h3>
    ${image}
    <h3>Fields</h3>
    <div class="metadata-grid">${fieldRows}</div>
    <h3>Caption / Context</h3>
    <pre>${escapeHtml(item.caption_full || item.caption || "")}</pre>
    ${item.arrangement_value ? `<h3>Arrangement Value</h3><pre>${escapeHtml(item.arrangement_value)}</pre>` : ""}
    ${item.question_text ? `<h3>Question Context</h3><pre>${escapeHtml(item.question_text)}</pre>` : ""}
    <h3>Path</h3>
    <pre>${escapeHtml(item.image_path || "")}</pre>
    ${item.source_image ? `<h3>Source Image</h3><pre>${escapeHtml(item.source_image)}</pre>` : ""}
    ${item.bbox && Object.keys(item.bbox).length ? `<h3>BBox</h3><pre>${escapeHtml(JSON.stringify(item.bbox, null, 2))}</pre>` : ""}
  `;
}

async function loadGraph() {
  const summary = await api("/api/graph/summary");
  await loadGraphFilters();
  const stats = document.getElementById("graph-summary");
  clear(stats);
  [
    ["Nodes", summary.nodes],
    ["Edges", summary.edges],
    ["Relations", summary.relations.length],
    ["Groups", summary.source_groups.length],
  ].forEach(([label, value]) => {
    const item = el("div", "mini-stat");
    item.innerHTML = `<strong>${value}</strong><br><span class="muted">${label}</span>`;
    stats.append(item);
  });
  await searchGraph();
}

async function loadQueryWorkbench() {
  const prompts = await api("/api/query/prompts");
  renderQueryGuidance(prompts);
  await loadQueryLogs();
}

function renderQueryGuidance(data) {
  const container = document.getElementById("query-guidance");
  clear(container);
  const principleList = el("div", "guidance-grid");
  (data.principles || []).forEach((item) => {
    const card = el("div", "guidance-card");
    card.innerHTML = `<strong>${escapeHtml(item.title)}</strong><p>${escapeHtml(item.text)}</p>`;
    principleList.append(card);
  });
  container.append(principleList);

  const templateTitle = el("h3", "", "可直接改写的 query 模板");
  container.append(templateTitle);
  const templateList = el("div", "template-list");
  (data.templates || []).forEach((item) => {
    const card = el("button", "template-card");
    card.innerHTML = `
      <strong>${escapeHtml(item.label)}</strong>
      <span>${escapeHtml(item.query)}</span>
      <small>${escapeHtml((item.tags || []).join(", "))}</small>
    `;
    card.addEventListener("click", () => {
      document.getElementById("rag-query").value = item.query;
      document.getElementById("rag-tags").value = (item.tags || []).join(", ");
    });
    templateList.append(card);
  });
  container.append(templateList);

  const axesTitle = el("h3", "", "本阶段评测关注点");
  container.append(axesTitle);
  const axes = el("ul", "axis-list");
  (data.evaluation_axes || []).forEach((axis) => axes.append(el("li", "", axis)));
  container.append(axes);
}

function collectQueryPayload() {
  return {
    query: document.getElementById("rag-query").value.trim(),
    notes: document.getElementById("rag-notes").value.trim(),
    tags: parseTags(document.getElementById("rag-tags").value),
    top_k: Number(document.getElementById("rag-top-k").value || 5),
    kg_limit: Number(document.getElementById("rag-kg-limit").value || 8),
    context: {
      source: "frontend_manual_query_workbench",
      intended_user_scope: "guitar_arrangement_user",
      exercise_queries_are_regression_tests_only: true,
    },
  };
}

async function saveManualQuery() {
  const payload = collectQueryPayload();
  if (!payload.query) {
    alert("先写一条 query。");
    return;
  }
  setQueryStatus("保存中...");
  try {
    await apiJson("/api/query/save", { ...payload, status: "draft" });
    setQueryStatus("已保存草稿");
    await loadQueryLogs();
  } catch (error) {
    console.error(error);
    setQueryStatus("保存失败");
    alert(`保存失败：${error.message}`);
  }
}

async function runManualQuery() {
  const payload = collectQueryPayload();
  if (!payload.query) {
    alert("先写一条 query。");
    return;
  }
  const runButton = document.getElementById("rag-run");
  runButton.disabled = true;
  setQueryStatus("运行中，首次加载本地 embedding 模型会稍慢...");
  try {
    const data = await apiJson("/api/query/run", payload);
    renderQueryResult(data);
    await loadQueryLogs();
    setQueryStatus("运行完成");
  } catch (error) {
    console.error(error);
    setQueryStatus("运行失败");
    alert(`运行失败：${error.message}`);
  } finally {
    runButton.disabled = false;
  }
}

function renderEvidenceSection(title, items) {
  const section = el("section", "evidence-section");
  section.append(el("h3", "", `${title} (${items.length})`));
  if (!items.length) {
    section.append(el("p", "muted", "没有召回证据"));
    return section;
  }
  items.slice(0, 8).forEach((item, index) => {
    const card = el("div", "evidence-card");
    card.innerHTML = `
      <div class="evidence-title">
        <strong>${index + 1}. ${escapeHtml(item.evidence_id)}</strong>
        <span>${Number(item.score || 0).toFixed(3)}</span>
      </div>
      <div class="badges">
        <span class="badge">${escapeHtml(item.evidence_type)}</span>
        <span class="badge">${escapeHtml(item.source_id)}</span>
      </div>
      <p>${escapeHtml(item.content || "")}</p>
    `;
    section.append(card);
  });
  return section;
}

function renderQueryResult(data) {
  const bundle = data.bundle || {};
  const judgement = bundle.judgement || {};
  const analysis = bundle.analysis || {};
  document.getElementById("rag-result-summary").textContent =
    `${analysis.intent || "unknown"} · sufficient=${judgement.sufficient} · confidence=${judgement.confidence}`;
  const pane = document.getElementById("rag-result");
  pane.classList.remove("empty");
  clear(pane);

  const summary = el("div", "query-summary");
  summary.innerHTML = `
    <h3>Analysis</h3>
    <div class="metadata-grid">
      <div class="meta-label">Intent</div><div>${escapeHtml(analysis.intent)}</div>
      <div class="meta-label">Style</div><div>${escapeHtml(listText(analysis.style_hints))}</div>
      <div class="meta-label">Theory</div><div>${escapeHtml(listText(analysis.theory_terms))}</div>
      <div class="meta-label">Technique</div><div>${escapeHtml(listText(analysis.technique_terms))}</div>
      <div class="meta-label">Report</div><div>${escapeHtml(data.report_md || "")}</div>
    </div>
  `;
  pane.append(summary);

  const judge = el("div", "query-judge");
  judge.innerHTML = `
    <h3>Judgement</h3>
    <pre>${escapeHtml(JSON.stringify(judgement, null, 2))}</pre>
    <h3>Timings</h3>
    <pre>${escapeHtml(JSON.stringify(bundle.timings || {}, null, 2))}</pre>
  `;
  pane.append(judge);
  pane.append(renderEvidenceSection("Text Evidence", bundle.text_evidence || []));
  pane.append(renderEvidenceSection("Visual Evidence", bundle.visual_evidence || []));
  pane.append(renderEvidenceSection("KG Evidence", bundle.kg_evidence || []));
}

async function loadQueryLogs() {
  const data = await api("/api/query/logs?limit=120");
  const list = document.getElementById("query-log-list");
  clear(list);
  (data.items || []).forEach((item) => {
    const row = el("div", "list-item");
    const judgement = item.judgement || {};
    row.innerHTML = `
      <strong>${escapeHtml(item.query || "")}</strong>
      <p>${escapeHtml(item.notes || item.intent || item.status || "")}</p>
      <div class="badges">
        <span class="badge">${escapeHtml(item.status || "draft")}</span>
        ${item.intent ? `<span class="badge">${escapeHtml(item.intent)}</span>` : ""}
        ${judgement.sufficient !== undefined ? `<span class="badge">sufficient ${escapeHtml(judgement.sufficient)}</span>` : ""}
        ${(item.tags || []).map((tag) => `<span class="badge">${escapeHtml(tag)}</span>`).join("")}
      </div>
    `;
    row.addEventListener("click", () => {
      document.getElementById("rag-query").value = item.query || "";
      document.getElementById("rag-notes").value = item.notes || "";
      document.getElementById("rag-tags").value = (item.tags || []).join(", ");
    });
    list.append(row);
  });
  if (!data.items || !data.items.length) list.append(el("div", "list-item", "还没有人工 query 记录"));
}

async function searchGraph() {
  const q = document.getElementById("graph-query").value.trim();
  const params = new URLSearchParams({ q, limit: "45" });
  const relation = document.getElementById("graph-relation").value;
  const sourceGroup = document.getElementById("graph-source-group").value;
  const knowledgeType = document.getElementById("graph-knowledge-type").value;
  if (relation) params.set("relation", relation);
  if (sourceGroup) params.set("source_group", sourceGroup);
  if (knowledgeType) params.set("knowledge_type", knowledgeType);
  const data = await api(`/api/graph/search?${params.toString()}`);
  renderGraph(data);
  renderEdges(data.raw_edges || []);
}

async function loadGraphFilters() {
  const data = await api("/api/graph/filters");
  fillSelect("graph-relation", "全部关系", data.relations || []);
  fillSelect("graph-source-group", "全部来源", data.source_groups || []);
  fillSelect("graph-knowledge-type", "全部类型", data.knowledge_types || []);
}

function fillSelect(id, firstLabel, values) {
  const select = document.getElementById(id);
  const current = select.value;
  clear(select);
  select.append(new Option(firstLabel, ""));
  values.forEach((value) => select.append(new Option(value, value)));
  if ([...select.options].some((option) => option.value === current)) {
    select.value = current;
  }
}

function renderGraph(data) {
  const svg = document.getElementById("graph-svg");
  clear(svg);
  const nodes = data.nodes || [];
  const edges = data.edges || [];
  const width = 900;
  const height = 520;
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) * 0.38;
  const positions = new Map();
  nodes.forEach((node, index) => {
    const angle = (Math.PI * 2 * index) / Math.max(nodes.length, 1);
    positions.set(node.id, {
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius,
    });
  });
  edges.forEach((edge) => {
    const s = positions.get(edge.source);
    const t = positions.get(edge.target);
    if (!s || !t) return;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", s.x);
    line.setAttribute("y1", s.y);
    line.setAttribute("x2", t.x);
    line.setAttribute("y2", t.y);
    line.setAttribute("stroke", "#b9c2d0");
    line.setAttribute("stroke-width", "1.2");
    svg.append(line);
  });
  nodes.forEach((node) => {
    const pos = positions.get(node.id);
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", pos.x);
    circle.setAttribute("cy", pos.y);
    circle.setAttribute("r", "22");
    circle.setAttribute("fill", "#e8eef9");
    circle.setAttribute("stroke", "#2454a6");
    circle.setAttribute("stroke-width", "1.5");
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", pos.x);
    text.setAttribute("y", pos.y + 40);
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-size", "11");
    text.setAttribute("fill", "#1d2430");
    text.textContent = truncate(node.label, 24);
    group.append(circle, text);
    svg.append(group);
  });
}

function renderEdges(edges) {
  const list = document.getElementById("graph-edge-list");
  clear(list);
  edges.forEach((edge) => {
    const card = el("div", "edge-card");
    card.innerHTML = `
      <strong>${escapeHtml(edge.source)} -- ${escapeHtml(edge.relation)} -> ${escapeHtml(edge.target)}</strong>
      <p>${escapeHtml(edge.context_condition || edge.review_note || edge.evidence || "")}</p>
      <div class="badges">
        <span class="badge">${escapeHtml(edge.knowledge_type || "unknown")}</span>
        <span class="badge">${escapeHtml(edge.source_group || "")}</span>
        <span class="badge">${escapeHtml(edge.chunk_id || "no chunk")}</span>
      </div>
    `;
    list.append(card);
  });
  if (!edges.length) list.append(el("div", "edge-card", "没有匹配图谱边"));
}

function truncate(text, length) {
  text = String(text || "");
  return text.length > length ? `${text.slice(0, length)}...` : text;
}

async function loadReports() {
  const data = await api("/api/reports");
  const list = document.getElementById("report-list");
  clear(list);
  data.items.forEach((item) => {
    const row = el("div", "list-item");
    row.innerHTML = `
      <strong>${escapeHtml(item.name)}</strong>
      <p>${Math.round(item.size / 1024)} KB · ${new Date(item.modified * 1000).toLocaleString()}</p>
    `;
    row.addEventListener("click", () => showReport(item.name, row));
    list.append(row);
  });
}

async function showReport(name, rowNode) {
  document.querySelectorAll("#report-list .list-item").forEach((n) => n.classList.remove("active"));
  rowNode.classList.add("active");
  const text = await api(`/api/report?name=${encodeURIComponent(name)}`);
  const pane = document.getElementById("report-detail");
  pane.classList.remove("empty");
  pane.innerHTML = `<h2>${escapeHtml(name)}</h2><pre class="report-markdown">${escapeHtml(text)}</pre>`;
}

async function loadView(view) {
  try {
    if (view === "dashboard") await loadDashboard();
    if (view === "datasets") await loadSources();
    if (view === "chunks") await loadChunks();
    if (view === "visuals") await loadVisuals();
    if (view === "query") await loadQueryWorkbench();
    if (view === "graph") await loadGraph();
    if (view === "reports") await loadReports();
  } catch (error) {
    console.error(error);
    alert(`加载失败：${error.message}`);
  }
}

document.querySelectorAll(".nav-button").forEach((button) => {
  button.addEventListener("click", () => activate(button.dataset.view));
});

document.getElementById("refresh-button").addEventListener("click", () => loadView(state.currentView));
document.getElementById("chunk-search").addEventListener("click", loadChunks);
document.getElementById("chunk-query").addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadChunks();
});
document.getElementById("visual-search").addEventListener("click", loadVisuals);
document.getElementById("visual-query").addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadVisuals();
});
document.getElementById("rag-run").addEventListener("click", runManualQuery);
document.getElementById("rag-save").addEventListener("click", saveManualQuery);
document.getElementById("query-log-refresh").addEventListener("click", loadQueryLogs);
document.getElementById("graph-search").addEventListener("click", searchGraph);
document.getElementById("graph-query").addEventListener("keydown", (event) => {
  if (event.key === "Enter") searchGraph();
});
["graph-relation", "graph-source-group", "graph-knowledge-type"].forEach((id) => {
  document.getElementById(id).addEventListener("change", searchGraph);
});

loadSources().then(() => activate("dashboard"));
