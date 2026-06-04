# Guitar Arrangement Inspiration Agent

一个面向吉他编配分析的本地 Agentic RAG / Knowledge Graph 项目。

项目目标是把吉他教材、风格课程、练习答案图和后续的 `.gp5`/乐谱分析结果整合成可追溯的检索系统：文本 RAG 负责教材解释，视觉 caption 层负责具体指型/谱例证据，Neo4j 知识图谱负责技法、风格和编配启发关系。

## Current Highlights

- 本地 Chroma RAG：接入本地 Qwen3 embedding，支持指板教材正文、风格文本和视觉 caption 检索。
- Neo4j KG：导入吉他指板、funk、mathrock 等技法与编配关系。
- VLM 降维视觉层：将教材答案图转成结构化 caption，再使用文本 embedding 检索。
- Query Layer：`scripts/query_rag_bundle.py` 可以把自然语言问题拆成文本、视觉和 KG 检索任务，并输出可审查 evidence bundle。
- 可视化原型：`backend/app.py` + `frontend/` 提供分块、知识导入和图谱查看的本地前后端雏形。

## Repository Layout

```text
backend/                 FastAPI backend and local visualization API
frontend/                Static frontend prototype
scripts/                 KG/RAG extraction, ingestion, evaluation, query scripts
config/                  Local processing config examples
data/knowledge/          Lightweight curated KG edge samples and Cypher exports
data/eval/               Evaluation and execution reports
PROJECT_FRAMEWORK.md     Project architecture and roadmap
PROJECT_GUIDE.md         Earlier project guide
```

Large/private assets are intentionally not committed:

- `.env`
- raw books and course files
- processed OCR/image batches
- Chroma databases
- local embedding model weights
- virtual environments and caches

## Query Layer Smoke Test

Example:

```powershell
.\.venv-mineru\Scripts\python.exe scripts\query_rag_bundle.py `
  --query "Fmaj7琶音怎么发展成math rock风格riff" `
  --top-k 5 `
  --report-md data/eval/query_rag_bundle_fmaj7_mathrock.md `
  --report-json data/eval/query_rag_bundle_fmaj7_mathrock.json
```

See:

```text
data/eval/QUERY_LAYER_EXECUTION_REPORT.md
```

## Remote Setup

1. Open GitHub and create a new empty repository.
2. Do not initialize it with README, `.gitignore`, or license, because this local project already has initial files.
3. After creating the repository, copy its HTTPS or SSH URL.
4. Add it locally:

```powershell
git remote add origin <your-repo-url>
```

5. Push the prepared branch:

```powershell
git push -u origin project-bootstrap
```

