const state = {
  sources: [],
  books: [],
  currentBookId: "",
  currentChunkSourceId: "",
  currentView: "dashboard",
  lastQueryFeedbackContext: null,
  lastSessionId: "",
};

const titles = {
  dashboard: ["Dashboard", "本地知识库与 Agentic RAG 研发工作台"],
  datasets: ["Datasets", "教材、视觉清单、知识图谱文件概览"],
  chunks: ["Chunks", "查看教材分块、图片引用和原文"],
  visuals: ["Visual Evidence", "查看视觉证据、caption 和原图"],
  query: ["RAG Query", "采集人工 query，运行本地文本/视觉/KG evidence bundle"],
  fullchain: ["Full Chain", "验证 Query Normalizer、RAG、rerank 与答案生成闭环"],
  memory: ["Memory", "复盘人工 query、RAG、Full Chain 和反馈事件"],
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

function parseMaybeJsonList(value) {
  if (Array.isArray(value)) return value.filter(Boolean);
  if (!value) return [];
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (!trimmed) return [];
    try {
      const parsed = JSON.parse(trimmed);
      if (Array.isArray(parsed)) return parsed.filter(Boolean);
    } catch {
      return [trimmed];
    }
  }
  return [];
}

function pathBasename(path) {
  return String(path || "").split(/[\\/]/).filter(Boolean).pop() || "";
}

function setQueryStatus(text) {
  document.getElementById("rag-status").textContent = text || "";
}

function setChainStatus(text) {
  document.getElementById("chain-status").textContent = text || "";
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
    visual_collection: document.getElementById("rag-visual-collection").value,
    use_normalizer: document.getElementById("rag-use-normalizer").checked,
    rerank_backend: document.getElementById("rag-rerank-backend").value,
    rerank_model: document.getElementById("rag-rerank-model").value.trim(),
    rerank_weight: Number(document.getElementById("rag-rerank-weight").value || 0.35),
    rerank_batch_size: Number(document.getElementById("rag-rerank-batch-size").value || 4),
    rerank_max_length: Number(document.getElementById("rag-rerank-max-length").value || 1024),
    context: {
      source: "frontend_manual_query_workbench",
      intended_user_scope: "guitar_arrangement_user",
      exercise_queries_are_regression_tests_only: true,
    },
  };
}

function collectFullChainPayload() {
  return {
    query: document.getElementById("chain-query").value.trim(),
    notes: document.getElementById("chain-notes").value.trim(),
    tags: parseTags(document.getElementById("chain-tags").value),
    top_k: Number(document.getElementById("chain-top-k").value || 5),
    kg_limit: Number(document.getElementById("chain-kg-limit").value || 8),
    visual_collection: document.getElementById("chain-visual-collection").value,
    use_normalizer: document.getElementById("chain-use-normalizer").checked,
    compose_answer: true,
    rerank_backend: document.getElementById("chain-rerank-backend").value,
    rerank_model: document.getElementById("chain-rerank-model").value.trim(),
    rerank_weight: Number(document.getElementById("chain-rerank-weight").value || 0.35),
    rerank_batch_size: Number(document.getElementById("chain-rerank-batch-size").value || 4),
    rerank_max_length: Number(document.getElementById("chain-rerank-max-length").value || 1024),
    context: {
      source: "frontend_full_chain_test",
      intended_user_scope: "guitar_arrangement_user",
      exercise_queries_are_regression_tests_only: true,
      compose_answer: true,
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
    const data = await apiJson("/api/query/save", { ...payload, status: "draft" });
    state.lastSessionId = data.session_id || data.session?.session_id || "";
    setQueryStatus(`已保存草稿${state.lastSessionId ? ` · session=${state.lastSessionId}` : ""}`);
    await loadQueryLogs();
  } catch (error) {
    console.error(error);
    setQueryStatus("保存失败");
    alert(`保存失败：${error.message}`);
  }
}

async function normalizeManualQuery() {
  const payload = collectQueryPayload();
  if (!payload.query) {
    alert("先写一条 query。");
    return;
  }
  const button = document.getElementById("rag-normalize");
  button.disabled = true;
  setQueryStatus("正在调用 LLM 规范化 query...");
  try {
    const data = await apiJson("/api/query/normalize", payload);
    state.lastSessionId = data.session_id || data.session?.session_id || "";
    renderQueryPlanOnly(data.query_plan || {});
    await loadQueryLogs();
    setQueryStatus(`规范化完成，QueryPlan 已显示在下方${state.lastSessionId ? ` · session=${state.lastSessionId}` : ""}`);
  } catch (error) {
    console.error(error);
    setQueryStatus("规范化失败");
    alert(`规范化失败：${error.message}`);
  } finally {
    button.disabled = false;
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
    state.lastSessionId = data.session_id || data.session?.session_id || "";
    renderQueryResult(data);
    await loadQueryLogs();
    setQueryStatus(`运行完成${state.lastSessionId ? ` · session=${state.lastSessionId}` : ""}`);
  } catch (error) {
    console.error(error);
    setQueryStatus("运行失败");
    alert(`运行失败：${error.message}`);
  } finally {
    runButton.disabled = false;
  }
}

async function runFullChainQuery() {
  const payload = collectFullChainPayload();
  if (!payload.query) {
    alert("先写一条全链路 query。");
    return;
  }
  const runButton = document.getElementById("chain-run");
  runButton.disabled = true;
  setChainStatus("运行全链路：规范化、召回、rerank、生成答案...");
  try {
    const data = await apiJson("/api/query/run", payload);
    state.lastSessionId = data.session_id || data.session?.session_id || "";
    renderFullChainResult(data);
    await loadQueryLogs();
    setChainStatus(`全链路完成${state.lastSessionId ? ` · session=${state.lastSessionId}` : ""}`);
  } catch (error) {
    console.error(error);
    setChainStatus("全链路失败");
    alert(`全链路失败：${error.message}`);
  } finally {
    runButton.disabled = false;
  }
}

function renderToolPlan(queryPlan) {
  const retrievalPlan = queryPlan.retrieval_plan || {};
  const rows = Object.entries(retrievalPlan).map(([name, item]) => {
    const enabled = item && item.enabled ? "on" : "off";
    return `
      <div class="tool-plan-row">
        <strong>${escapeHtml(name)}</strong>
        <span class="badge">${enabled}</span>
        <p>${escapeHtml(item?.query || "")}</p>
        <small>${escapeHtml(item?.reason || "")}</small>
      </div>
    `;
  });
  return rows.join("") || "<p class=\"muted\">没有工具计划</p>";
}

function scoreSelect(id, label, options = ["2 准确", "1 部分", "0 错误/缺失"], defaultValue = "2") {
  return `
    <label>
      ${escapeHtml(label)}
      <select id="${id}">
        ${options
          .map((text) => {
            const value = String(text).slice(0, 1);
            return `<option value="${escapeHtml(value)}" ${value === defaultValue ? "selected" : ""}>${escapeHtml(text)}</option>`;
          })
          .join("")}
      </select>
    </label>
  `;
}

function enabledToolsFromPlan(queryPlan) {
  return Object.entries(queryPlan?.retrieval_plan || {})
    .filter(([, item]) => item?.enabled)
    .map(([name]) => name);
}

function bundleSummary(bundle) {
  const judgement = bundle?.judgement || {};
  return {
    intent: bundle?.analysis?.intent || "",
    plan: (bundle?.plan || []).map((task) => task.name),
    text_count: (bundle?.text_evidence || []).length,
    visual_count: (bundle?.visual_evidence || []).length,
    kg_count: (bundle?.kg_evidence || []).length,
    sufficient: judgement.sufficient,
    confidence: judgement.confidence,
    warnings: judgement.warnings || [],
    timings: bundle?.timings || {},
    rerank_config: bundle?.rerank_config || {},
    model_rerank: bundle?.answer_seed?.model_rerank || {},
  };
}

function appendFeedbackPanel(pane, context) {
  state.lastQueryFeedbackContext = context;
  const queryPlan = context.query_plan || {};
  const enabledTools = new Set(enabledToolsFromPlan(queryPlan));
  const panel = el("section", "feedback-panel");
  panel.innerHTML = `
    <h3>人工反馈评分</h3>
    <p class="muted">用于评测 Query Normalizer 是否规范；提交后写入本地 feedback jsonl。</p>
    <div class="feedback-grid">
      ${scoreSelect("feedback-schema", "Schema 合规", ["1 合规", "0 不合规"], "1")}
      ${scoreSelect("feedback-intent", "Intent 准确度")}
      ${scoreSelect("feedback-tools", "工具选择")}
      ${scoreSelect("feedback-slots", "槽位抽取")}
      ${scoreSelect("feedback-tool-query", "工具 Query 质量")}
      ${scoreSelect("feedback-downstream", "下游 Bundle", ["2 好", "1 一般", "0 差/未运行"], context.source === "run" ? "2" : "0")}
      ${scoreSelect("feedback-overall", "总体评分", ["5 很好", "4 可用", "3 一般", "2 较差", "1 不可用"], "4")}
      <label>
        期望 Intent
        <select id="feedback-expected-intent">
          ${[
            "",
            "style_arrangement",
            "fretboard_voicing",
            "visual_shape_recommendation",
            "rhythm_riff_design",
            "harmonic_reharmonization",
            "mixed_arrangement",
            "score_analysis_followup",
            "caption_regression_test",
          ]
            .map((item) => `<option value="${escapeHtml(item)}" ${item === queryPlan.intent ? "selected" : ""}>${escapeHtml(item || "未标注")}</option>`)
            .join("")}
        </select>
      </label>
    </div>
    <div class="feedback-tools">
      <strong>期望工具</strong>
      ${["fretboard_text", "style_text", "visual_caption", "kg"]
        .map(
          (name) => `
            <label class="inline-check">
              <input class="feedback-tool" type="checkbox" value="${name}" ${enabledTools.has(name) ? "checked" : ""} />
              ${name}
            </label>
          `
        )
        .join("")}
    </div>
    <div class="feedback-tools">
      <strong>错误标签</strong>
      ${[
        ["schema_error", "格式错误"],
        ["intent_error", "意图错"],
        ["tool_miss", "漏工具"],
        ["tool_overuse", "工具过多"],
        ["slot_miss", "槽位漏抽"],
        ["tool_query_bad", "检索 query 差"],
        ["downstream_bad", "下游召回差"],
      ]
        .map(
          ([value, label]) => `
            <label class="inline-check">
              <input class="feedback-tag" type="checkbox" value="${value}" />
              ${label}
            </label>
          `
        )
        .join("")}
    </div>
    <label class="feedback-notes">
      备注
      <textarea id="feedback-notes" rows="3" placeholder="例如：漏掉 kg；visual_caption query 太泛；style_hints 正确但 tools 过多。"></textarea>
    </label>
    <div class="toolbar">
      <button id="feedback-submit" class="primary-button" type="button">提交反馈</button>
      <span id="feedback-status" class="muted"></span>
    </div>
  `;
  pane.append(panel);
  document.getElementById("feedback-submit").addEventListener("click", submitQueryFeedback);
}

async function submitQueryFeedback() {
  const context = state.lastQueryFeedbackContext;
  if (!context) {
    alert("还没有可评价的 QueryPlan。");
    return;
  }
  const button = document.getElementById("feedback-submit");
  const status = document.getElementById("feedback-status");
  button.disabled = true;
  status.textContent = "保存中...";
  const payload = {
    query: context.query || "",
    source: context.source || "normalize",
    normalized_query: context.query_plan?.normalized_query || "",
    intent: context.query_plan?.intent || context.bundle?.analysis?.intent || "",
    expected_intent: document.getElementById("feedback-expected-intent").value,
    expected_tools: [...document.querySelectorAll(".feedback-tool:checked")].map((node) => node.value),
    failure_tags: [...document.querySelectorAll(".feedback-tag:checked")].map((node) => node.value),
    notes: document.getElementById("feedback-notes").value.trim(),
    scores: {
      schema_score: Number(document.getElementById("feedback-schema").value),
      intent_score: Number(document.getElementById("feedback-intent").value),
      tool_selection_score: Number(document.getElementById("feedback-tools").value),
      slot_score: Number(document.getElementById("feedback-slots").value),
      tool_query_score: Number(document.getElementById("feedback-tool-query").value),
      downstream_score: Number(document.getElementById("feedback-downstream").value),
      overall_score: Number(document.getElementById("feedback-overall").value),
    },
    query_plan: context.query_plan || {},
    bundle_summary: context.bundle_summary || {},
    report_md: context.report_md || "",
    session_id: context.session_id || "",
  };
  try {
    const data = await apiJson("/api/query/feedback", payload);
    status.textContent = `已保存：${data.feedback_log}`;
  } catch (error) {
    console.error(error);
    status.textContent = "保存失败";
    alert(`保存反馈失败：${error.message}`);
  } finally {
    button.disabled = false;
  }
}

function renderQueryPlanOnly(queryPlan) {
  document.getElementById("rag-result-summary").textContent =
    `${queryPlan.intent || "unknown"} · normalized`;
  const pane = document.getElementById("rag-result");
  pane.classList.remove("empty");
  clear(pane);
  const card = el("div", "query-summary");
  card.innerHTML = `
    <h3>LLM QueryPlan</h3>
    <div class="metadata-grid">
      <div class="meta-label">Normalized</div><div>${escapeHtml(queryPlan.normalized_query || "")}</div>
      <div class="meta-label">Intent</div><div>${escapeHtml(queryPlan.intent || "")}</div>
      <div class="meta-label">Style</div><div>${escapeHtml(listText(queryPlan.style_hints || []))}</div>
      <div class="meta-label">Materials</div><div>${escapeHtml(listText([...(queryPlan.harmonic_materials || []), ...(queryPlan.melodic_materials || [])]))}</div>
      <div class="meta-label">Goals</div><div>${escapeHtml(listText(queryPlan.arrangement_goals || []))}</div>
    </div>
    <h3>Tool Queries</h3>
    <div class="tool-plan-grid">${renderToolPlan(queryPlan)}</div>
    <h3>Raw Plan</h3>
    <pre>${escapeHtml(JSON.stringify(queryPlan, null, 2))}</pre>
  `;
  pane.append(card);
  appendFeedbackPanel(pane, {
    source: "normalize",
    query: queryPlan.raw_query || document.getElementById("rag-query").value.trim(),
    query_plan: queryPlan,
    bundle_summary: {},
    report_md: "",
    session_id: state.lastSessionId || "",
  });
  pane.scrollIntoView({ behavior: "smooth", block: "start" });
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
    const modelRerank = item.metadata?.model_rerank || null;
    const rawMetadata = item.metadata?.raw_metadata || {};
    const imagePath = item.metadata?.image_path || rawMetadata.crop_path || rawMetadata.image_path || "";
    const imageRefs = [
      ...parseMaybeJsonList(item.metadata?.image_refs),
      ...parseMaybeJsonList(rawMetadata.image_refs),
    ];
    const rerankBadge = modelRerank
      ? `<span class="badge">rerank +${Number(modelRerank.delta || 0).toFixed(3)}</span>`
      : "";
    const imageBadge = imagePath
      ? `<a class="badge" href="${fileUrl(imagePath)}" target="_blank" rel="noreferrer">image</a>`
      : imageRefs.length
        ? `<span class="badge">${imageRefs.length} image refs</span>`
        : "";
    card.innerHTML = `
      <div class="evidence-title">
        <strong>${index + 1}. ${escapeHtml(item.evidence_id)}</strong>
        <span>${Number(item.score || 0).toFixed(3)}</span>
      </div>
      <div class="badges">
        <span class="badge">${escapeHtml(item.evidence_type)}</span>
        <span class="badge">${escapeHtml(item.source_id)}</span>
        ${rerankBadge}
        ${imageBadge}
      </div>
      <p>${escapeHtml(item.content || "")}</p>
    `;
    section.append(card);
  });
  return section;
}

function renderModelRerankStatus(bundle) {
  const groups = bundle?.answer_seed?.model_rerank || {};
  const timings = bundle?.timings || {};
  const labels = ["text", "visual", "kg"];
  return `
    <h3>Model Rerank</h3>
    <div class="metadata-grid">
      ${labels
        .map((name) => {
          const status = groups[name] || {};
          const text = status.enabled
            ? `${status.provider || "local"} · ${status.count || 0} items · weight=${status.weight ?? ""}`
            : `off · ${status.reason || "disabled"}`;
          return `<div class="meta-label">${escapeHtml(name)}</div><div>${escapeHtml(text)}</div>`;
        })
        .join("")}
      <div class="meta-label">Latency</div><div>${Number(timings.model_rerank_seconds || 0).toFixed(4)}s</div>
    </div>
  `;
}

function renderQueryResult(data) {
  const bundle = data.bundle || {};
  const queryPlan = data.query_plan || bundle.query_plan || null;
  const judgement = bundle.judgement || {};
  const analysis = bundle.analysis || {};
  const rerankConfig = bundle.rerank_config || {};
  const visualCollection = bundle.visual_collection || {};
  const promptVersions = bundle.prompt_versions || {};
  document.getElementById("rag-result-summary").textContent =
    `${analysis.intent || "unknown"} · ${visualCollection.profile || "formal"} · sufficient=${judgement.sufficient} · confidence=${judgement.confidence}`;
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
      <div class="meta-label">Visual Library</div><div>${escapeHtml(visualCollection.label || visualCollection.collection || "正式视觉库")}</div>
      <div class="meta-label">Prompt Versions</div><div>${escapeHtml(JSON.stringify(promptVersions))}</div>
      <div class="meta-label">Rerank</div><div>${escapeHtml(`${rerankConfig.backend || "none"} · weight=${rerankConfig.weight ?? ""} · max=${rerankConfig.max_length ?? ""}`)}</div>
      <div class="meta-label">Report</div><div>${escapeHtml(data.report_md || "")}</div>
    </div>
  `;
  pane.append(summary);
  if (queryPlan || data.normalizer_error) {
    const planCard = el("div", "query-plan-panel");
    planCard.innerHTML = `
      <h3>LLM QueryPlan</h3>
      ${data.normalizer_error ? `<p class="warning-text">Normalizer fallback: ${escapeHtml(data.normalizer_error)}</p>` : ""}
      ${
        queryPlan
          ? `<div class="metadata-grid">
              <div class="meta-label">Normalized</div><div>${escapeHtml(queryPlan.normalized_query || "")}</div>
              <div class="meta-label">Intent</div><div>${escapeHtml(queryPlan.intent || "")}</div>
              <div class="meta-label">Tools</div><div>${escapeHtml(Object.entries(queryPlan.retrieval_plan || {}).filter(([, item]) => item?.enabled).map(([name]) => name).join(", "))}</div>
              <div class="meta-label">Goals</div><div>${escapeHtml(listText(queryPlan.arrangement_goals || []))}</div>
            </div>
            <div class="tool-plan-grid">${renderToolPlan(queryPlan)}</div>`
          : "<p class=\"muted\">本次未生成 QueryPlan。</p>"
      }
    `;
    pane.append(planCard);
  }

  const judge = el("div", "query-judge");
  judge.innerHTML = `
    <h3>Judgement</h3>
    <pre>${escapeHtml(JSON.stringify(judgement, null, 2))}</pre>
    ${renderModelRerankStatus(bundle)}
    <h3>Timings</h3>
    <pre>${escapeHtml(JSON.stringify(bundle.timings || {}, null, 2))}</pre>
  `;
  pane.append(judge);
  pane.append(renderEvidenceSection("Text Evidence", bundle.text_evidence || []));
  pane.append(renderEvidenceSection("Visual Evidence", bundle.visual_evidence || []));
  pane.append(renderEvidenceSection("KG Evidence", bundle.kg_evidence || []));
  appendFeedbackPanel(pane, {
    source: "run",
    query: bundle.query || document.getElementById("rag-query").value.trim(),
    query_plan: queryPlan || {},
    bundle,
    bundle_summary: bundleSummary(bundle),
    report_md: data.report_md || "",
    session_id: data.session_id || data.session?.session_id || "",
  });
}

function renderComposedAnswer(answer, errorText = "") {
  const section = el("section", "query-summary");
  if (errorText) {
    section.innerHTML = `
      <h3>Answer Composer Error</h3>
      <p class="warning-text">${escapeHtml(errorText)}</p>
    `;
    return section;
  }
  if (!answer) {
    section.innerHTML = "<h3>Composed Answer</h3><p class=\"muted\">没有生成答案。</p>";
    return section;
  }
  const evidenceUsed = (answer.evidence_used || [])
    .map((item) => `<li><code>${escapeHtml(item.evidence_id || "")}</code> ${escapeHtml(item.why || item.role || "")}</li>`)
    .join("");
  const advice = (answer.style_arrangement_advice || [])
    .map((item) => `<li>${escapeHtml(item.advice || "")} <small>${escapeHtml(listText(item.evidence_ids || []))}</small></li>`)
    .join("");
  const options = (answer.fretboard_options || [])
    .map((item) => `<li><strong>${escapeHtml(item.label || "")}</strong> ${escapeHtml(item.usage || "")} <small>${escapeHtml(item.evidence_id || "")}</small></li>`)
    .join("");
  section.innerHTML = `
    <h3>Composed Answer</h3>
    <p><strong>${escapeHtml(answer.summary || "")}</strong></p>
    <p>${escapeHtml(answer.answer || "")}</p>
    <div class="two-column compact-columns">
      <div>
        <h4>Evidence Used</h4>
        <ul>${evidenceUsed || "<li>无</li>"}</ul>
      </div>
      <div>
        <h4>Fretboard Options</h4>
        <ul>${options || "<li>无</li>"}</ul>
      </div>
    </div>
    <h4>Arrangement Advice</h4>
    <ul>${advice || "<li>无</li>"}</ul>
    <h4>Theory Checks</h4>
    <ul>${(answer.theory_checks || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>无</li>"}</ul>
    <h4>Uncertainties</h4>
    <ul>${(answer.uncertainties || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>无</li>"}</ul>
    <details>
      <summary>Raw Answer JSON</summary>
      <pre>${escapeHtml(JSON.stringify(answer, null, 2))}</pre>
    </details>
  `;
  return section;
}

function collectAnswerEvidenceIds(answer) {
  const ids = new Set();
  (answer?.evidence_used || []).forEach((item) => {
    if (item?.evidence_id) ids.add(item.evidence_id);
  });
  (answer?.fretboard_options || []).forEach((item) => {
    if (item?.evidence_id) ids.add(item.evidence_id);
  });
  (answer?.style_arrangement_advice || []).forEach((item) => {
    (item?.evidence_ids || []).forEach((id) => ids.add(id));
  });
  (answer?.kg_reasoning || []).forEach((item) => {
    if (item?.evidence_id) ids.add(item.evidence_id);
  });
  return ids;
}

function collectVisualImageItems(bundle, answer) {
  const referenced = collectAnswerEvidenceIds(answer);
  return (bundle.visual_evidence || [])
    .filter((item) => !referenced.size || referenced.has(item.evidence_id))
    .map((item) => {
      const metadata = item.metadata || {};
      const raw = metadata.raw_metadata || {};
      const imagePath = metadata.image_path || raw.crop_path || raw.image_path || "";
      if (!imagePath) return null;
      return {
        evidence_id: item.evidence_id,
        title: item.title || raw.musical_object || "",
        path: imagePath,
        visual_id: metadata.visual_id || raw.visual_id || "",
        note: visualExerciseLabel({
          exercise_number: metadata.exercise_number || raw.exercise_number,
          subquestion_number: metadata.subquestion_number || raw.subquestion_number,
        }),
      };
    })
    .filter(Boolean);
}

function collectTextImageRefItems(bundle) {
  const rows = [];
  (bundle.text_evidence || []).forEach((item) => {
    const metadata = item.metadata || {};
    const raw = metadata.raw_metadata || {};
    const refs = [
      ...parseMaybeJsonList(metadata.image_refs),
      ...parseMaybeJsonList(raw.image_refs),
    ];
    const uniqueRefs = [...new Set(refs.map((ref) => String(ref)))].filter(Boolean);
    if (!uniqueRefs.length) return;
    rows.push({
      evidence_id: item.evidence_id,
      title: item.title || raw.source_title || "",
      page_hint: metadata.page_hint || raw.page_hint || "",
      refs: uniqueRefs,
    });
  });
  return rows;
}

function renderImageEvidenceSidebar(bundle, answer) {
  const aside = el("aside", "answer-image-sidebar");
  const visualItems = collectVisualImageItems(bundle, answer);
  const textRows = collectTextImageRefItems(bundle);
  const visualCards = visualItems
    .map(
      (item) => `
        <article class="answer-image-card">
          <img src="${fileUrl(item.path)}" alt="${escapeHtml(item.evidence_id)}" loading="lazy" />
          <strong>${escapeHtml(item.evidence_id)}</strong>
          <span>${escapeHtml(item.title)}</span>
          ${item.note ? `<small>${escapeHtml(item.note)}</small>` : ""}
          <code>${escapeHtml(item.path)}</code>
        </article>
      `
    )
    .join("");
  const textCards = textRows
    .map(
      (row) => `
        <article class="image-ref-map">
          <strong>${escapeHtml(row.evidence_id)}</strong>
          <span>${escapeHtml(row.title)}${row.page_hint ? ` · p.${escapeHtml(row.page_hint)}` : ""}</span>
          <ol>
            ${row.refs
              .map(
                (ref, index) => `
                  <li>
                    <a href="${fileUrl(ref)}" target="_blank" rel="noreferrer">${escapeHtml(`img_${index + 1}: ${pathBasename(ref)}`)}</a>
                    <code>${escapeHtml(ref)}</code>
                  </li>
                `
              )
              .join("")}
          </ol>
        </article>
      `
    )
    .join("");
  aside.innerHTML = `
    <h3>图片证据</h3>
    <p class="muted">显示答案引用到的视觉证据图，以及文本证据保留的 image_refs 对照。</p>
    <h4>Answer Visuals (${visualItems.length})</h4>
    ${visualCards || "<p class=\"muted\">答案没有引用可显示的视觉图片。</p>"}
    <h4>Text Image Refs (${textRows.length})</h4>
    ${textCards || "<p class=\"muted\">文本证据没有 image_refs。</p>"}
  `;
  return aside;
}

function renderFullChainResult(data) {
  const bundle = data.bundle || {};
  const queryPlan = data.query_plan || bundle.query_plan || null;
  const judgement = bundle.judgement || {};
  const answer = data.composed_answer || bundle.composed_answer || null;
  const answerError = data.answer_composer_error || bundle.answer_composer_error || "";
  const visualCollection = bundle.visual_collection || {};
  const promptVersions = bundle.prompt_versions || answer?.prompt_versions || {};
  document.getElementById("chain-result-summary").textContent =
    `${bundle.analysis?.intent || "unknown"} · ${visualCollection.profile || "formal"} · sufficient=${judgement.sufficient} · answer=${answer ? "ok" : answerError ? "error" : "none"}`;
  const pane = document.getElementById("chain-result");
  pane.classList.remove("empty");
  clear(pane);
  const layout = el("div", "fullchain-result-grid");
  const main = el("div", "fullchain-main");
  const sidebar = renderImageEvidenceSidebar(bundle, answer);
  layout.append(main, sidebar);
  pane.append(layout);
  main.append(renderComposedAnswer(answer, answerError));

  const planCard = el("div", "query-plan-panel");
  planCard.innerHTML = `
    <h3>QueryPlan / Judgement</h3>
    ${queryPlan ? `<div class="tool-plan-grid">${renderToolPlan(queryPlan)}</div>` : "<p class=\"muted\">未生成 QueryPlan。</p>"}
    <h4>Judgement</h4>
    <pre>${escapeHtml(JSON.stringify(judgement, null, 2))}</pre>
    <h4>Prompt Versions</h4>
    <pre>${escapeHtml(JSON.stringify(promptVersions, null, 2))}</pre>
    ${renderModelRerankStatus(bundle)}
    <h4>Timings</h4>
    <pre>${escapeHtml(JSON.stringify(bundle.timings || {}, null, 2))}</pre>
  `;
  main.append(planCard);
  main.append(renderEvidenceSection("Text Evidence", bundle.text_evidence || []));
  main.append(renderEvidenceSection("Visual Evidence", bundle.visual_evidence || []));
  main.append(renderEvidenceSection("KG Evidence", bundle.kg_evidence || []));
  pane.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadQueryLogs() {
  const data = await api("/api/query/logs?limit=120");
  const list = document.getElementById("query-log-list");
  clear(list);
  (data.items || []).forEach((item) => {
    const row = el("div", "list-item");
    const judgement = item.judgement || {};
    const rerankConfig = item.rerank_config || {};
    const visualCollection = item.visual_collection || {};
    row.innerHTML = `
      <strong>${escapeHtml(item.query || "")}</strong>
      <p>${escapeHtml(item.normalized_query || item.notes || item.intent || item.status || "")}</p>
      <div class="badges">
        <span class="badge">${escapeHtml(item.status || "draft")}</span>
        ${item.intent ? `<span class="badge">${escapeHtml(item.intent)}</span>` : ""}
        ${visualCollection.profile ? `<span class="badge">${escapeHtml(visualCollection.profile)}</span>` : ""}
        ${rerankConfig.backend ? `<span class="badge">rerank ${escapeHtml(rerankConfig.backend)}</span>` : ""}
        ${judgement.sufficient !== undefined ? `<span class="badge">sufficient ${escapeHtml(judgement.sufficient)}</span>` : ""}
        ${(item.tags || []).map((tag) => `<span class="badge">${escapeHtml(tag)}</span>`).join("")}
      </div>
    `;
    row.addEventListener("click", () => {
      document.getElementById("rag-query").value = item.query || "";
      document.getElementById("rag-notes").value = item.notes || "";
      document.getElementById("rag-tags").value = (item.tags || []).join(", ");
      if (rerankConfig.backend) document.getElementById("rag-rerank-backend").value = rerankConfig.backend;
      if (rerankConfig.model) document.getElementById("rag-rerank-model").value = rerankConfig.model;
      if (rerankConfig.weight !== undefined) document.getElementById("rag-rerank-weight").value = rerankConfig.weight;
      if (rerankConfig.batch_size !== undefined) document.getElementById("rag-rerank-batch-size").value = rerankConfig.batch_size;
      if (rerankConfig.max_length !== undefined) document.getElementById("rag-rerank-max-length").value = rerankConfig.max_length;
      if (visualCollection.profile) document.getElementById("rag-visual-collection").value = visualCollection.profile;
    });
    list.append(row);
  });
  if (!data.items || !data.items.length) list.append(el("div", "list-item", "还没有人工 query 记录"));
}

async function loadMemorySessions() {
  const q = document.getElementById("memory-query").value.trim();
  const status = document.getElementById("memory-status").value;
  const params = new URLSearchParams({ limit: "160" });
  if (q) params.set("q", q);
  if (status) params.set("status", status);
  const data = await api(`/api/memory/sessions?${params.toString()}`);
  const list = document.getElementById("memory-list");
  clear(list);
  (data.items || []).forEach((item) => {
    const row = el("div", "list-item");
    const summary = item.bundle_summary || {};
    row.innerHTML = `
      <strong>${escapeHtml(item.query || "")}</strong>
      <p>${escapeHtml(item.normalized_query || item.notes || item.intent || item.memory_type || "")}</p>
      <div class="badges">
        <span class="badge">${escapeHtml(item.status || "unknown")}</span>
        ${item.memory_type ? `<span class="badge">${escapeHtml(item.memory_type)}</span>` : ""}
        ${item.intent ? `<span class="badge">${escapeHtml(item.intent)}</span>` : ""}
        ${item.answer_status ? `<span class="badge">answer ${escapeHtml(item.answer_status)}</span>` : ""}
        ${summary.sufficient !== undefined ? `<span class="badge">sufficient ${escapeHtml(summary.sufficient)}</span>` : ""}
        ${(item.tags || []).map((tag) => `<span class="badge">${escapeHtml(tag)}</span>`).join("")}
      </div>
      <small>${escapeHtml(item.timestamp || "")}</small>
    `;
    row.addEventListener("click", () => showMemorySession(item.session_id, row));
    list.append(row);
  });
  if (!data.items || !data.items.length) list.append(el("div", "list-item", "还没有 session memory"));
}

async function showMemorySession(sessionId, rowNode) {
  if (!sessionId) return;
  document.querySelectorAll("#memory-list .list-item").forEach((node) => node.classList.remove("active"));
  rowNode?.classList.add("active");
  const data = await api(`/api/memory/session?session_id=${encodeURIComponent(sessionId)}`);
  const item = data.item || {};
  const summary = item.bundle_summary || {};
  const events = item.events || [];
  const pane = document.getElementById("memory-detail");
  pane.classList.remove("empty");
  pane.innerHTML = `
    <h2>${escapeHtml(item.memory_type || item.status || "Session")}</h2>
    <div class="meta-grid">
      <div><div class="meta-label">Session</div><code>${escapeHtml(item.session_id || "")}</code></div>
      <div><div class="meta-label">Time</div><span>${escapeHtml(item.timestamp || "")}</span></div>
      <div><div class="meta-label">Status</div><span>${escapeHtml(item.status || "")}</span></div>
      <div><div class="meta-label">Source</div><span>${escapeHtml(item.source || "")}</span></div>
    </div>
    <h3>Query</h3>
    <p>${escapeHtml(item.query || "")}</p>
    ${item.normalized_query ? `<h3>Normalized Query</h3><p>${escapeHtml(item.normalized_query)}</p>` : ""}
    <h3>Tags / Intent</h3>
    <p>${escapeHtml([item.intent, ...(item.tags || [])].filter(Boolean).join(" · ")) || "未标注"}</p>
    <h3>Bundle Summary</h3>
    <pre>${escapeHtml(JSON.stringify(summary, null, 2))}</pre>
    <h3>Reports</h3>
    <div class="meta-grid">
      <div><div class="meta-label">Markdown</div><code>${escapeHtml(item.report_md || "")}</code></div>
      <div><div class="meta-label">JSON</div><code>${escapeHtml(item.report_json || "")}</code></div>
    </div>
    <h3>QueryPlan</h3>
    <pre>${escapeHtml(JSON.stringify(item.query_plan || {}, null, 2))}</pre>
    <h3>Events (${events.length})</h3>
    <div class="memory-event-list">
      ${
        events.length
          ? events
              .map(
                (event) => `
                  <article class="memory-event">
                    <strong>${escapeHtml(event.event_type || "")}</strong>
                    <span>${escapeHtml(event.timestamp || "")}</span>
                    <pre>${escapeHtml(JSON.stringify(event.payload || event.summary || {}, null, 2))}</pre>
                  </article>
                `
              )
              .join("")
          : "<p class=\"muted\">暂无事件。</p>"
      }
    </div>
    <h3>Raw Session</h3>
    <pre>${escapeHtml(JSON.stringify(item, null, 2))}</pre>
  `;
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
    if (view === "fullchain") await loadQueryLogs();
    if (view === "memory") await loadMemorySessions();
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
document.getElementById("rag-normalize").addEventListener("click", normalizeManualQuery);
document.getElementById("rag-save").addEventListener("click", saveManualQuery);
document.getElementById("chain-run").addEventListener("click", runFullChainQuery);
document.getElementById("query-log-refresh").addEventListener("click", loadQueryLogs);
document.getElementById("memory-search").addEventListener("click", loadMemorySessions);
document.getElementById("memory-query").addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadMemorySessions();
});
document.getElementById("memory-status").addEventListener("change", loadMemorySessions);
document.getElementById("graph-search").addEventListener("click", searchGraph);
document.getElementById("graph-query").addEventListener("keydown", (event) => {
  if (event.key === "Enter") searchGraph();
});
["graph-relation", "graph-source-group", "graph-knowledge-type"].forEach((id) => {
  document.getElementById(id).addEventListener("change", searchGraph);
});

loadSources().then(() => activate("dashboard"));
