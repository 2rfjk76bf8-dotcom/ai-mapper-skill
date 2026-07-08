---
name: ai-mapper
description: Use when the user asks Codex to run /ai-mapper, AI mapping, map early Chinese AI software projects, founders, independent developers, open-source builders, AI product teams, or AI talent leads into an Obsidian research artifact.
---

# AI Mapper

Create source-backed Obsidian reports for early Chinese/China-relevant AI software projects and qualified talent leads. Every normal run uses `TOPIC=通用扫描`; save artifacts and do not leave the result only in chat.

## Core Contract

## Forced No-Subagent Pipeline

Normal `/ai-mapper` runs must use the no-subagent forced pipeline unless the user explicitly asks for parallel lane processors after the Exa Candidate Queue is already complete. Main Codex remains the only actor allowed to run recall, Elsewhere API, validation, rating, final writing, latest-pointer updates, and run-report writing.

Mandatory hard gates:

1. Exa recall is only valid after every MCP Exa response is saved to a workspace JSON file and recorded through `scripts/forced_pipeline.py record-exa-response`. Every returned URL must become one row in `{WORKSPACE}/exa-candidates.jsonl` before filtering, dedupe, enrichment, or context-mode compression. If an Exa response cannot be recorded, stop and mark the run `blocked`; do not hand-transcribe a partial queue.
2. Elsewhere API usage must write `{WORKSPACE}/elsewhere-api-audit.jsonl`, one row per endpoint call with `endpoint_group`, `endpoint`, `query`, `status`, returned counts, extracted candidate count, and notes. When Elsewhere is available, complete runs must cover these endpoint groups: `search_chunks`, `whats_new`, `topics`, `content_detail`, `entity_lookup`, and `entity_card_or_edges`. Five extracted candidates without endpoint coverage is not enough.
3. Before writing any complete final report or updating `{BASE}/最新AI项目与人才Mapping.md` as a complete/latest result, run `scripts/forced_pipeline.py guard-final --workspace "$WORKSPACE" --elsewhere-status {available|missing_key|quota_exhausted|rate_limited|error|not_run}`. If it fails because selected-mode recall/open/source-family gates are below minimum while Exa is available and the workspace is writable, this is not a valid `blocked` deliverable; continue Exa recall, persistence, and mandatory opening until the minimum gates pass. Write `blocked` only for a real blocker such as Exa unavailable, response persistence impossible, workspace write failure, or an original-source access failure that makes public verification impossible after the required recall/open work has been attempted.
4. `scripts/validate_run.py --workspace "$WORKSPACE"` remains the final schema validator. The forced pipeline guard checks workflow completeness; `validate_run.py` checks artifact consistency. Both must pass before a run can be called `complete`.
5. Subagents are not part of the default architecture. They may process lane candidates only after Main Codex has passed Exa recall persistence gates and only if the user explicitly asks for parallel processing. They must never run recall, mutate final artifacts, update latest pointers, or bypass `forced_pipeline.py guard-final`.

Fail-closed rule: if a gate is missing, unclear, or impossible to verify mechanically, stop the complete path. Do not compensate with prose, manual counts, or partial hand-written JSONL.

Under-minimum gate rule: a quantity shortfall is work still in progress, not a stopping state. If `guard-final` reports `Total Exa candidate URLs`, query/source paths, opened/fetched pages, source families, or C-funding lane gates below the selected-mode minimum and Exa/workspace are still available, Main Codex must keep running recall/opening. Do not write final/latest, do not rewrite canonical JSONL files to status-only, and do not call the run `blocked` merely because the current count is below target.


- Use current web/source inspection. Do not use memory for current projects, people, funding, dates, activity, or contact paths.
- Use `TOPIC=通用扫描` for every normal run. If the user mentions a direction, treat it as an emphasis inside the generic scan and do not narrow the scan.
- Use exactly four raw-search lanes: `A-dev`, `B-content`, `C-funding`, `D-academic`.
- Broad discovery (`通用扫描`, new topic, A/B/C/D coverage) uses four raw-search lanes by default, not four search agents. Main Codex performs all front-stage Exa candidate recall for those lanes. Do not use subagents before the Exa Candidate Queue exists. Narrow enrichment, known leads, one-lane repair, Elsewhere API discovery/source handling, and Lark/Base row updates may run sequentially.
- Front-stage lane recall is Exa-only: Exa returns the open-web candidate URLs/results for A/B/C/D lane files. Lane processors may open/fetch assigned Exa candidates and public pages needed to verify those candidates, then filter noise and turn candidates into detailed raw cases.
- Elsewhere API is mandatory for every complete run. Resolve the key and run a lightweight availability preflight before broad discovery. If Elsewhere is available, run keyword intelligence, project discovery, and financing pass as normal. If no key is configured or the API returns quota/rate exhaustion such as `429 quota_exceeded`, continue with Exa + open public sources as `degraded / Exa-only`: still write the standard final/raw/latest paths, do not create alternate `*-exa-only` filenames, mark completeness as degraded in final/latest/run-report, and write `待补 Elsewhere` only for missing keyword intelligence, Elsewhere discovery/supplement, Elsewhere Financing Pass, or ecosystem-context gaps. Do not use Elsewhere as the next-step option for team/person/background/contact fields. Elsewhere-discovered candidates must be recorded in an `Elsewhere API discovery/supplement` pool with attribution and `source_origin=Elsewhere API`, not inserted into A/B/C/D lane files as if Exa found them. Do not ask Exa to operate Elsewhere API, do not let subagents use the Elsewhere key, and do not mix Elsewhere claims into Exa evidence without attribution.
- Elsewhere is mandatory but never the team/person backfill path. After candidate discovery, Main Codex must run a public-web enrichment pass for likely A/B projects and all named people whether Elsewhere is available or not. Missing core team, responsible person, background, contact, financing, product proof, customer/user proof, original repo/model/demo, or true event date must be written as a concrete public-web/Codex search gap, never as an Elsewhere backfill option.
- Exa summaries, highlights, rank order, and snippets are radar signals only. They cannot be rating evidence, contact evidence, freshness evidence, or A/B justification until backtraced to openable original sources.
- Every broad Exa recall result must be persisted before filtering to `{WORKSPACE}/exa-candidates.jsonl`. This file is the canonical recall audit trail for every Exa-returned URL, including rows later dropped, deduped, or not selected for review. Context-mode compression and lane queue compaction must not remove rows; the run report's `Total Exa candidate URLs` actual count must reconcile with non-status rows in this JSONL file. If it cannot be written, fail validation instead of claiming delivery.
- Exa candidate handling uses full lightweight triage, not high-potential cherry-picking. Every `exa-candidates.jsonl` row must receive lightweight tags before selection: `source_family_hint`, `entry_type_hint`, `possible_signal`, `risk_reason`, `entity_cluster_id`, `must_open_reason`, and `review_decision`. Open/fetch all rows whose `must_open_reason` is not `none`; use adaptive continuation for productive buckets. A row that was not opened/fetched must never be marked `dropped`; use `not_selected` or `unreviewed` with a concrete reason.
- Lightweight triage is hypothesis-only and must never become final writing. Triage may write only routing fields such as `candidate_name_hypothesis`, `source_family_hint`, `entry_type_hint`, `possible_signal`, `risk_reason`, `entity_cluster_id`, `must_open_reason`, and `review_decision`. Triage must not write or imply final `项目名`, `一句话描述`, `融资状态`, `true_event_date`, `评级`, `关联人才与背景`, or `项目背景与证据`. These final fields may only be written from opened/fetched original-source evidence objects.
- Normal runs are recency-first. For market/startup/funding discovery, A/B priority comes from true events within the latest 30 days from run date: financing announcements, product launches, repo/model releases, customer/deployment proof, founder posts, or substantive company/investor/news pages. 31-60 day items are observation candidates; older items are background unless a new event reactivates them. Exa `publishedDate`, crawl date, snippets, or search rank must never be used as the true event date.
- Keep the final output schema fixed: project tables and talent tables only. Do not create a separate academic talent table, scholar table, community-signal table, or ranking table. Strong academic evidence enters existing project rows when the artifact is a projectized paper/system/benchmark/repo/demo/product; authors and labs go into `关联人才与背景`, and only independently qualified, source-backed people enter the existing talent table.
- Public source discovery is openable-source-first. Broad ranking databases, generic AI tool directories, generic community feeds, login/paywall/account-only databases, and closed communities are out of scope. Keep only directly openable public community/product signals that can be searched and verified without login: Product Hunt, GitHub/GitHub Trending/GitHub releases, Hugging Face Trending/models/spaces/datasets, and open original project/repo/product/paper/funding pages.
- If context-mode is present, use it as the context-hygiene path between Exa recall and verification: keep payloads compact without shrinking recall breadth. Preserve query, URL, title, source type, short why-matter reason, and fetch/open status; compress summaries/highlights and raw page text, not candidate coverage. Store/index candidate queues or fetched candidate pages with `ctx_index` / `ctx_fetch_and_index`, and use `ctx_search` / `ctx_execute` to retrieve only the evidence snippets needed for raw rows. Context-mode is not source evidence, memory, ranking authority, or a replacement for opening original public pages. Do not reduce `numResults`, skip candidate URLs, or run fewer Exa queries merely to save context. If context-mode is unavailable or not useful for a narrow run, continue with broad Exa recall plus compact payloads and record the limitation.
- Main Codex owns setup, topic plan, Exa recall coordination, validation, dedupe, enrichment, rating, final reports, latest pointer, run report, and any Lark/Base mutation. Main Codex turns strong raw cases into high-density project decision table rows first and talent rows when named person/team, person-project relation, recent action, and background evidence are available.
- Optional subagents are allowed only after Main Codex has produced the Exa Candidate Queue. They are candidate processors, not search agents: they must not run independent web search, broad discovery, or add candidate sources outside the provided Exa queue. If more recall is needed, they ask Main Codex to run another Exa pass. They write only their assigned result file and must not edit topic files, validation/rating files, final reports, run reports, latest pointer, or other lanes.
- Do not paste large final tables in chat. Return paths, counts, and limitations.
- The final artifact must be decision-ready, not just a radar list. Project discovery comes first: A/B project rows should surface high-potential projects even when founder/person/contact fields are incomplete. Responsible person and background are enrichment fields for project rows and required for talent rows; contact is optional context only. If missing, write the concrete future detailed-search value instead of blocking a strong project from A/B.
- Recruitment/job-board paths are banned as discovery, evidence, contact path, or rating signal: Boss直聘, 拉勾, 猎聘, 脉脉招聘, hiring pages/posts/posters.
- Use only publicly openable sources plus mandatory Elsewhere API when it is available. Resolve an `els_live_...` key before discovery. If no key is configured/provided or the API quota/rate limit is exhausted, record the Elsewhere limitation using `references/blockers.md`, continue as `degraded / Exa-only` if Exa is available, write all standard output paths, and do not mark the run `complete`. Do not use other platforms or pages that require an account, private app state, private browser session, QR code, or CAPTCHA to search or verify facts. If a candidate depends on a closed source outside Elsewhere, drop it or record a public-source limitation; do not ask the user for access to closed platforms.

## Resource Layout

Keep `SKILL.md` as the executable contract: scope, lanes, gates, artifact paths, mandatory Elsewhere handling, and completion rules.

- Read `references/examples.md` only when examples are needed for raw row shape, high-density project table rows, talent rows, downgrade decisions, or output-quality checks.
- Read `references/source-policy.md` before every run; it defines mandatory Elsewhere use, public-source boundaries, evidence classes, and banned sources.
- Read `references/run-modes.md` and `references/run-modes.json` before Exa recall; they define default `adaptive standard scan`, deep-map triggers, gate budgets, lane allocation, and early-stop rules.
- Read `references/run-states.md` before final/latest/run-report writing; it defines `complete`, `degraded / Exa-only`, and `blocked` transitions.
- Read `references/source-families.md` before source coverage counting; it defines allowed source-family counting and non-counting sources.
- Read `references/structured-artifacts.md` before validation/rating; it defines `exa-candidates.jsonl`, `candidates.jsonl`, and `evidence.jsonl`.
- Read `references/rating-rubric.md` before validation/rating; it defines A/B/C gates and downgrade rules.
- Read `references/schemas.md` before writing `validated.md`, `rated.md`, final reports, raw artifacts, or latest pointer files.
- Read `references/blockers.md` when Exa, Elsewhere, context-mode, or public evidence is missing or blocked.
- Read `references/pressure-tests.md` when editing this skill or auditing whether future agents follow it.
- Use `scripts/preflight.py` before broad recall to classify Elsewhere key/quota state and record Exa/context-mode tool status.
- Use `scripts/validate_run.py` after editing the skill package and after every completed mapping run.
- Put future long reference material in `references/`.
- Add `scripts/` only for deterministic helpers that would otherwise be rewritten repeatedly.
- Add `assets/` only for reusable output templates or files used in produced artifacts.


## Scope And Rating

For `TOPIC=通用扫描`, stay inside Chinese/China-relevant AI software and qualified talent leads: AI Agent, MCP, coding agent, AI office/productivity, agent memory, personal AI, developer tools, workflow integration, agent/coding security, AI infra tied to routing/cost/runtime.

Treat these as background unless explicitly requested or strongly tied to the scope: broad robotics/embodied AI, broad multimodal/video/3D, overseas-only startups, mature companies, B-round-or-later companies, large financing, big-platform projects, generic media/newsletters/podcasts. Academic-only people lists are not a separate output target. Academic work can become a project lead only when it is projectized: a paper/system/benchmark/repo/demo/product/lab spinout with strong evidence such as top venue, citation/usage, open repo/demo/model, benchmark adoption, commercialization, or financing signal. Put the artifact in the project table and put authors/labs/founders in `关联人才与背景`.

Every rated project lead must answer: `是什么项目`, `为什么值得看`, `已有证据是什么`, `缺什么`, `下一步补全项`. Talent rows should answer: `找谁`, `为什么值得看`, `已有证据是什么`, `缺什么`, `下一步补全项`. Do not force a contact recommendation field in final output.

Output quality bar:

- A project row = high-priority project decision table row, not necessarily directly contactable. It must identify the project/product/repo/paper-system, explain why it matters now, cite at least one openable original, credible public source, or attributed Elsewhere API source, state available team/person/contact information if found, and explicitly mark missing person/contact/background fields as `待补`.
- A project row cannot be supported only by one media/report page when core team, funding status, and product proof are all unresolved. If public-web enrichment cannot verify at least one stronger original source family such as product/company site, GitHub/release, repo/model/demo, customer/deployment proof, investor/VC page, company announcement, founder/team page, or public profile, cap the project at B even when the true event date is recent.
- A talent row = high-priority compact talent card. It must name the responsible person/team when known, connect them to the company/project/work, cite recent original evidence, and summarize background without spreading evidence across many columns. Contact is optional context inside `背景` only when public and useful. Do not invent or require a direct outreach recommendation.
- B row = detailed search candidate. It must say exactly which missing field blocks stronger confidence: Background, Contact, Freshness, Funding, Evidence, Why now, Project signal, Customer/user proof, or Person-project relation. `下一步补全项` is for the next detailed content search, not a user action checklist.
- Final A/B project and talent sections must be higher-density than raw tables: project tables use the mentor-decision fields from `references/schemas.md`: `项目名`, `一句话描述`, `AI 软件细分方向`, `产品形态`, `项目背景与证据`, `融资状态`, `关联人才与背景`, `下一步补全项`, `评级`, `来源链接`, `采集日期`, `最近有效动态日期`. Talent tables intentionally use the compact schema in `references/schemas.md`: `姓名/昵称`, `关联公司/项目`, `最近动作`, `身份`, `背景`, `评级`. Each row must be detailed enough for 李曼 to make an immediate judgment without opening raw files. Omit `触达建议`.
- C / 暂不跟进 row = why it is kept only as light context or background; do not spend table space pretending it is an outreach target.
- Talent rows must not be filler copied from project rows. A/B talent rows require a recent, evidence-backed action, preferably within the last 30 days for normal scans; stale people move to C/background or stay only in project enrichment.
- For example row shapes and downgrade patterns, read `references/examples.md`. For binding rating rules, read `references/rating-rubric.md`.

A-class project requires project gates first. Person/contact/background are enrichment fields, not hard gates for project-level A.

| Gate | Requirement |
|---|---|
| Scope | Chinese/China-relevant AI software under topic |
| Early | not mature, big-company, B-round-or-later, or high-financing |
| Project signal | clear product/repo/company/program/paper-system with a concrete AI software direction |
| Person/team | optional for project-level A; if missing, write `待补负责人/核心团队` and the exact future detailed-search path |
| Background | optional for project-level A; if missing, write `待补团队背景` |
| Contact | optional for project-level A; if missing, write `待补触达路径`; generic support/PR/sales/contact forms are allowed as weak project-level contact but must not be treated as personal outreach |
| Freshness | market/startup/funding leads need a true event date within the latest 30 days for A; 31-60 days is normally B/继续观察; older items are C/background unless there is a new event. Academic project leads need a recent paper/repo/model/demo event or a current productization/funding signal. Exa crawl/published dates are not freshness evidence. |
| Evidence | product/demo/GitHub/research paper/repo/model/funding/user/customer/repeated output |
| Why now | concrete reason for 李曼 to care now, not market heat |

Generic support, PR, sales, HR, company forms, and `contact@` alone cannot make a talent A, but they do not block project-level A when project signal, freshness, evidence, and why-now are strong. Ratings: `A / 重点关注`, `B / 继续观察`, `C / 轻量记录`, `暂不跟进`.

## Paths

Use these exact paths:

```bash
BASE="/Users/lixiaoran/ObsidianVault/AI-Mapping"
DATE="$(date +%m%d)"
WORKSPACE="$BASE/runs/ai-mapper-$(date +%Y%m%d-%H%M%S)"
RESULTS="$WORKSPACE/results"
FINAL="$BASE/${DATE}-ai-mapper.md"
RAW_DIR="$BASE/raw"
RAW="$RAW_DIR/${DATE}-ai-mapper-raw.md"
mkdir -p "$RESULTS" "$RAW_DIR" "$BASE"
```

Required artifacts:

```text
{WORKSPACE}/topic.md
{WORKSPACE}/topics.md
{WORKSPACE}/results/A-dev.md
{WORKSPACE}/results/B-content.md
{WORKSPACE}/results/C-funding.md
{WORKSPACE}/results/D-academic.md
{WORKSPACE}/validated.md
{WORKSPACE}/rated.md
{WORKSPACE}/exa-candidates.jsonl
{WORKSPACE}/candidates.jsonl
{WORKSPACE}/evidence.jsonl
{WORKSPACE}/AI项目与人才Mapping.md
{WORKSPACE}/run-report.md
{BASE}/{MMDD}-ai-mapper.md
{BASE}/raw/{MMDD}-ai-mapper-raw.md
{BASE}/最新AI项目与人才Mapping.md
```

Artifact paths are stable across complete, degraded, and blocked runs. Do not create alternate `*-exa-only` filenames. Put availability/completeness status inside the files, especially the final report, latest pointer, and run report.

Do not create private-source review artifacts. Closed or account-only sources are not part of the workflow; record them only as public-source limitations when they explain coverage gaps.


## Search Plan

Always set `TOPIC=通用扫描`. Do not ask the user to choose a direction. If the user names a field such as AI客服、AI办公自动化、MCP应用、AI Agent, or AI教育, record it in `topic.md` as `用户强调方向`, but keep the four-lane generic scan.

Write `topic.md`, then `topics.md` with 3 directions and 5 keyword groups per direction. Each group combines:

- direction terms: `AI Agent`, `MCP`, `Coding Agent`, `browser agent`, `computer use`, `Figma to code`, `原型转代码`, `vLLM`, `模型路由`, `Agent memory`, `prompt injection`, `企业数据`
- early-action terms: `近30天`, `本月`, `最新融资`, `完成融资`, `天使轮`, `种子轮`, `Pre-A`, `内测`, `求反馈`, `我做了一个`, `独立开发`, `创业组队`, `招募用户`, `发布`, `上线`
- talent terms: `GitHub`, `开源`, `论文`, `顶会`, `引用`, `黑客松`, `演讲`, `作者`, `创始人`, `核心开发者`
- source pack and expected entry types: `person`, `project`, `repo`, `content`, `event`, `paper`

### Recency Gate

Before broad recall, compute the run-date windows and write them into `topic.md`:

- `priority_window`: run date minus 30 days through run date.
- `observation_window`: run date minus 60 days through run date, excluding `priority_window`.
- `background_window`: anything older than 60 days unless there is a new event inside `priority_window`.

For every kept candidate, separate and record the dates in raw notes, `validated.md`, `rated.md`, and `run-report.md`:

- `source_page_date`: article/page/post/release page date.
- `true_event_date`: financing, launch, release, paper acceptance/posting, repo release, model upload, customer/deployment, or other real event date.
- `exa_returned_date`: Exa `publishedDate` or crawl-like date if present.
- `collection_date`: run date.
- `date_decision`: which date was used for freshness and why.

Never promote a candidate because Exa returned it as recent. If the original page is old, undated, or only newly crawled, downgrade or keep it as background unless another openable source proves a recent true event.

### Priority Objective

The scan optimizes for `最近、最新、最值得` plus `未来潜在 candidate`, in that order:

- P0: true event inside the priority window and strong project/person signal, especially new financing, launch, product release, repo/model release, demo day, customer/deployment, founder post, or Elsewhere-reported market event.
- P1: future-potential candidate: no financing yet or incomplete background, but early product/repo/paper-system/team signal is strong enough that it should stay in `validated.md` for later enrichment.
- P2: context/background: mature, late-stage, big-platform, stale, closed-source-only, or useful only for market map.

Do not optimize for a tiny final A list. Keep enough P0/P1 candidates through raw and validated so the final A/B decision table is a ranked market map, not a hand-picked sample. If many rows pass A/B gates, include them; do not cap A merely because the table is long.

### Recall Volume Gate

A normal `通用扫描` uses `adaptive standard scan` by default, not the old 600-candidate deep-map gate. Read `references/run-modes.md` before Exa recall and write the selected `run_mode` into `topic.md` and `run-report.md`.

Default standard scan budgets are minimum / target / cap, not a single hard number: total Exa query/source paths `36 / 40-70 / 80`, candidate URLs `160 / 180-320 / 350`, opened/fetched original pages `50 / 60-100 / 120`, and raw P0/P1 leads `30 / 35-70 / 80`. C-funding stays the highest-weight lane, using the lane allocation in `references/run-modes.md`.

Use `deep map` budgets only when the user explicitly asks for `深度扫`, `全量市场地图`, `重扫一遍`, `尽可能不要漏`, or equivalent high-recall language. Deep map keeps the old high-recall shape: candidate URLs about `500-600`, opened pages about `150-180`, and raw leads `100+`.

After the selected mode's minimum gates pass, Main Codex may stop before the target/cap only when the `Early Stop Rule` in `references/run-modes.md` passes. Record the marginal-yield batch size, new P0/P1 count, duplicate/stale/out-of-scope pattern, and stop/continue decision in `run-report.md`. Do not stop before minimum gates pass, and do not shrink recall merely to save context. If the current count is below minimum, the only valid next action is more recall/opening or documenting a real external blocker; partial evidence is not a deliverable state.

### Source Coverage Gate

The scan must cover enough independent source families according to the selected run mode. Default `adaptive standard scan` requires at least 10 distinct open source families across the four lanes and at least 6 funding/venture source families in `C-funding`; targets are 12-16 and 6-8. `deep map` requires at least 18 source families and at least 10 funding/venture source families. Count source families such as Elsewhere API, 36氪, 投资界, 创业邦, 猎云网, 亿欧, 雷峰网, 新智元, 量子位, 机器之心, InfoQ, DoNews, TechNode, KrASIA, VC newsroom/portfolio pages, company announcements, GitHub, Product Hunt, Hugging Face, arXiv/OpenReview/Semantic Scholar/OpenAlex, demo-day/accelerator pages. If a source family is queried but yields no openable candidates, record `queried/no usable result` instead of silently ignoring it.

### C-funding Exa Query Matrix

`C-funding` must be generated from a query matrix, not a few hand-written broad queries. Main Codex must combine source families, AI software terms, and funding/event terms into source-specific Exa queries before broad recall. Do not let 36氪 dominate the lane merely because it returns many results.

Source-family terms:

- Chinese venture/media: `36氪`, `投资界`, `创业邦`, `猎云网`, `亿欧`, `雷峰网`, `新智元`, `量子位`, `机器之心`, `InfoQ`, `DoNews`
- English/overseas China tech: `TechNode`, `KrASIA`
- Original/near-original funding sources: `company announcement`, `investor portfolio`, `VC newsroom`, `accelerator demo day`, `roadshow`, `incubator`

AI software terms:

- `AI Agent`, `企业级智能体`, `Agent OS`, `Coding Agent`, `AI 编程`, `AI office`, `AI 办公`, `AI 表格`, `workflow automation`, `MCP`, `AI 软件应用`, `AI infra`, `模型路由`, `RAG`, `数据智能体`, `AI 搜索`, `Agent memory`, `prompt injection`, `agent security`

Funding/event terms:

- `融资`, `完成融资`, `获融资`, `天使轮`, `种子轮`, `Pre-A`, `A轮`, `首发`, `独家`, `投资方`, `领投`, `跟投`, `创始人`, `创业`, `发布`, `上线`, `内测`, `商业化`, `客户案例`

For adaptive standard scan, `C-funding` must run at least 12 source-specific query/source paths and should target 14-22, covering at least 6 usable funding/venture source families. At least one query must target each high-value family when Exa is available: 36氪, 投资界, 创业邦, 猎云网/亿欧/雷峰网, 机器之心/量子位/新智元, InfoQ/DoNews, TechNode/KrASIA, and investor/company/VC newsroom pages. If a source family returns no openable candidates, record `queried/no usable result` in `run-report.md` and continue the matrix rather than collapsing back to 36氪-only recall.

Example query templates:

```text
site:36kr.com AI Agent 企业级智能体 融资 天使轮 种子轮 2026 7月 创始人 投资方
site:pedaily.cn AI 软件应用 AI Agent 融资 天使轮 种子轮 2026 7月
site:cyzone.cn AI Agent Coding Agent 融资 创业 2026 7月
site:lieyunwang.com AI 软件 智能体 融资 2026 天使轮 Pre-A
site:iyiou.com AI office AI办公 智能体 融资 创业 2026
site:leiphone.com AI Agent AI软件 应用 创业 融资 2026
site:jiqizhixin.com AI Agent Coding Agent 创业 融资 产品发布 2026
site:infoq.cn AI Agent AI infra 模型路由 创业 融资 2026
site:donews.com AI Agent AI办公 融资 创业 发布 2026
site:technode.com China AI agent startup funding seed round July 2026
site:kr-asia.com China AI software startup funding AI agent seed round July 2026
AI Agent startup funding China investor portfolio newsroom July 2026 seed angel
```

Before Exa recall, resolve Elsewhere API connection status with a lightweight preflight. If Elsewhere is available, run Elsewhere keyword intelligence plus project discovery. If no key is configured/provided or the API returns quota/rate exhaustion, write an `Elsewhere unavailable` block into `topic.md`, `topics.md`, final report/latest pointer, and `run-report.md`; then continue broad Exa recall as `degraded / Exa-only` using baseline query groups and mark only the missing Elsewhere source layer as `待补 Elsewhere`. Team/person/background/contact gaps still require public-web/Codex search wording. For keyword intelligence, refresh frontier industry vocabulary, founder/company phrasing, product categories, investor language, recent financing terms, and emerging topic names related to the generic scan and any user-emphasized direction. Write a compact `Elsewhere Keyword Intelligence` block into `topics.md`:

```markdown
## Elsewhere Keyword Intelligence
| Seed/topic | Elsewhere query | Frontier terms | Founder/company phrases | Exa query angles | Evidence note |
|---|---|---|---|---|---|
```

Use this block to improve Exa query phrasing, synonyms, and source-intent coverage. Do not treat Elsewhere keyword hits alone as candidate evidence.

For Elsewhere project discovery, run targeted Elsewhere queries for source-backed reporting on relevant companies, products, founders, funding, and ecosystem themes. Extract project/company/person names from every relevant Elsewhere chunk/article instead of using the article only as vocabulary. Keep these candidates separate from A/B/C/D lane files and record them as an `Elsewhere API discovery/supplement` pool with query, endpoint, title/author/date, URL, extracted project/person facts, verification status, and next source to verify. Elsewhere-discovered projects can enter `validated.md`, `rated.md`, and final tables when the reporting is substantive and linkable, subject to the rating caps below. Use the selected run mode's Elsewhere budget from `references/run-modes.md`: default standard scan minimum/target/cap is `5 / 8-15 / 20` Elsewhere financing/startup candidate facts; deep map minimum is `20`. If Elsewhere is available but returns fewer direct candidates, explicitly state which queries produced no project candidates and diagnose the cause. The final report or run report must name which Elsewhere candidates entered A/B/C and which were downgraded, so Elsewhere discovery is visible instead of hidden in notes.

For each keyword group, Main Codex prepares and runs Exa-ready natural-language queries that describe the ideal page, not just keywords. Each lane should cover candidate discovery, project/product/repo signal, recent activity, true event date, and then contact/background backtracing when possible. Broad recall must use a candidate-queue payload, not page-body payload: prefer `web_search_advanced_exa` with `enableSummary: false`, no subpages, `highlightsMaxCharacters` capped to a small routing snippet, and `textMaxCharacters` set to a very small positive value such as `1` rather than `0` because some providers treat `0` as unlimited/default. Use `web_search_exa` only for narrow spot checks where a long result cannot threaten context. Keep the payload compact, but preserve recall breadth: do not lower result counts, skip query variants, or omit candidate URLs merely to save context. Use context-mode indexed fetching for reading the best returned URLs when highlights are insufficient. Use `web_fetch_exa` only as a last-mile verifier with `maxCharacters` capped and small URL batches; never use it to bulk-open lane candidates into chat. In either case, the original public page is the evidence, not the summary layer. If Exa is unavailable, pause broad discovery and record the blocker in `run-report.md`; do not fall back to direct web/source search for front-stage sourcing.


## Exa Targets And Lead Types

Use Exa to find early projects/products/repos/paper-systems with concrete AI software activity, and use Elsewhere API in parallel as mandatory China tech/venture context and discovery support. Responsible actor, founder, maintainer, background, and contact are enrichment targets after a project is found; they are not prerequisites for project discovery or project-level A. The rows below are query targets and post-recall verification roles, not independent lane-processor search starting points.

| Purpose | Exa target / post-Exa role |
|---|---|
| Exa Radar | `mcp__exa.web_search_exa`, `mcp__exa.web_search_advanced_exa`, `mcp__exa.web_fetch_exa` for broad open-web recall, source/date filters, and first-pass candidate URLs |
| Context Hygiene | `mcp__context_mode.ctx_index`, `ctx_fetch_and_index`, `ctx_search`, `ctx_execute` for storing/querying Exa candidate queues and fetched original pages without dumping raw payloads into conversation context |
| Elsewhere API | Main Codex only; `elsewhere.news/api/v1` connected mode for first-hand China tech/venture reporting, semantic chunks, content detail, entity cards, and relationship edges. Use as an attributed data source for keyword intelligence, project discovery, financing/startup facts, and ecosystem context; never as an Exa lane and never as the required team/person/background backfill path. |
| Public community/product radar - allowlist only | Product Hunt launches, GitHub/GitHub Trending/GitHub releases, Hugging Face Trending/models/spaces/datasets, plus ModelScope/Gitee public project pages only when directly openable and tied to a concrete repo/model/project |
| Funding/venture discovery - open only | 36氪, 投资界, 创业邦, 猎云网, 亿欧, 雷峰网, 新智元, 量子位, 机器之心, InfoQ, DoNews, TechNode, KrASIA, company announcements, investor/VC portfolio pages, VC newsroom pages, and public synchronized article pages that are directly openable without login/CAPTCHA |
| Academic discovery - open only | arXiv, OpenReview, Semantic Scholar, OpenAlex, Papers With Code, ACL Anthology, CVF, NeurIPS/ICLR/ICML proceedings, project/repo/demo pages linked from papers, public lab/project pages |
| Verification | product site, GitHub repo, Hugging Face page, paper page, author page, company page, funding article, investor page, event page |
| Enrichment | founder/GitHub/public X profiles, personal sites, product/company pages, investor portfolio public pages, paper author/lab pages, Semantic Scholar/OpenAlex profiles |
| Ranking/Index | Only open public radar from Product Hunt, GitHub Trending/repo/release velocity, and Hugging Face Trending/models/spaces/datasets. Exclude broad榜单数据库, generic AI tool directories, generic community feeds, and sources requiring login/account/paywall/CAPTCHA. |

These source roles classify what Exa returns and where evidence is verified; they do not authorize lane processors to run independent candidate discovery. Broad raw lane search starts with Exa Radar, then backtraces kept Exa candidates through openable Public Discovery, Verification, Enrichment, Funding/venture, Academic, and the narrow public radar allowlist above. Context Hygiene may store and query the Exa Candidate Queue or fetched candidate pages, but it never creates candidates outside Exa and never becomes a cited evidence source. Elsewhere API is mandatory and is the exception as a Main-Codex-operated data source: it provides keyword intelligence, discovers source-backed project/person candidates, and adds attributed financing/market/ecosystem facts. Team/person/background/contact fields must still be resolved or marked as unresolved through public-web/Codex search, not an Elsewhere backfill option. Elsewhere candidates stay in the `Elsewhere API discovery/supplement` pool and must not be counted as a fifth raw-search lane or written into lane result files. Discard sources that require an account, private app state, private browser session, QR code, paywall, or CAPTCHA to search or view. If a lane processor finds a promising source outside the Exa queue, it must request Main Codex handling before using it as a candidate. Record Exa usage, Elsewhere usage, context-mode usage, and extra public verification sources in 来源质量复盘.

Use Product Hunt, GitHub Trending, and Hugging Face Trending only as radar for product names, category timing, launch/release velocity, open-source momentum, and competing products. Do not use broad rankings/tool directories/community heat as discovery or rating inputs. Backtrace every candidate to original project/product/repo/model/paper/funding/customer evidence and a true recent event date before A/B project consideration.

## Elsewhere API Data Source

Elsewhere is a first-hand reporting corpus for China's tech and venture ecosystem. It is not an Exa tool and not a lane processor tool. Main Codex operates it directly as a mandatory project-discovery, evidence, and enrichment source for every complete run. If it is unavailable because the key is missing or quota/rate limits are exhausted, the run may continue only as `degraded / Exa-only` with standard output paths and explicit status labels. Read `references/source-policy.md` for the binding source rules.

Mandatory Elsewhere pass:

- Resolve the key before discovery: `KEY="${ELSEWHERE_KEY:-$(cat ~/.config/elsewhere/key 2>/dev/null)}"`.
- If no `els_live_...` key is found, or the API returns quota/rate exhaustion such as `429 quota_exceeded`, write the Elsewhere unavailable/degraded block from `references/blockers.md`, continue with Exa + open public sources when Exa is available, and mark the run `degraded / Exa-only`; do not mark it `complete`.
- Run keyword intelligence before Exa query drafting.
- Run project discovery before validation and keep it in `Elsewhere API discovery/supplement`.
- Run the `Elsewhere Financing Pass` before C-funding rating. Elsewhere is not allowed to be only keyword/context in a normal run.
- Run enrichment checks for likely A/B projects and all named people before final rating.
- Do not use Elsewhere as a substitute for opening original project/repo/product/funding pages when those pages are needed for the row type.

Operation rules:

1. Read the Elsewhere API reference before first endpoint use in a session and use exact field names.
2. For keyword intelligence and project discovery, prefer `GET /search/chunks?q=&k=&published_after=&recency=prefer`, `GET /topics?q=&limit=`, and `GET /relation-keys?category=` when useful. For entity/fact enrichment, prefer `GET /entities/find?name=`, `GET /entities/search?q=&k=`, `GET /entities/{id}/card`, `GET /entities/{id}/edges`, and `GET /content/{type}/{id}?lang=zh`.
3. Attribute every substantive Elsewhere-derived claim as `Elsewhere · {author/title/date}` with link. For `search/chunks`, build links as `https://elsewhere.news/zh/{author_slug}/{slug}`; never invent slugs.
4. Never paste full articles. Use concise facts, context, numbers, relationships, and uncertainty.
5. Keep Elsewhere facts separate from Exa/open-web facts in notes. If they conflict, record the contradiction and do not silently merge.
6. Elsewhere-discovered names may be new project/person candidates, not only enrichment for existing rows. If Elsewhere surfaces a source-backed project/person, Main Codex may add it as an `Elsewhere API discovery/supplement` candidate in validated/rated, with `来源平台=Elsewhere API`, `source_origin=Elsewhere API`, API query/endpoint, and explicit attribution. Do not put Elsewhere-only discoveries into lane result files as if they came from Exa.
7. Elsewhere-only candidates can enter the output table when the reporting itself is substantive and linkable, but they cannot be rated A unless project signal, freshness, why-now, and at least one original/open project/product/repo/company/funding source are also verified or clearly not needed for that row type. Otherwise keep B / 待补原始项目证据 or C / 背景样本.

Output integration:

### Elsewhere Financing Pass

Run this pass after keyword intelligence and before `validated.md` when Elsewhere is available. If Elsewhere is unavailable because the key is missing or quota/rate limits are exhausted, skip these API calls, record the exact unavailable reason, set Elsewhere financing/startup candidate facts to `0 / degraded`, and write `待补 Elsewhere Financing Pass` only where this missing source affects Elsewhere-derived financing/startup context:

1. Use the active date windows. Query with `published_after` for the priority window and again for the observation window when needed. Prefer `recency=filter` for strict date windows and `recency=prefer` for broader semantic expansion.
2. Use financing-event queries, not only product-category queries. Include combinations of `融资`, `完成融资`, `天使轮`, `种子轮`, `Pre-A`, `早期项目`, `一级市场`, `投资方`, `创始人`, plus AI software categories such as `AI Agent`, `AI office`, `Coding Agent`, `MCP`, `AI infra`, `模型路由`, `企业数据`, `workflow automation`.
3. Use `/search/chunks` with high enough `k` to inspect article clusters, not just top snippets. For candidate-rich content, fetch `/content/{type}/{id}?lang=zh` and extract every mentioned company/project/person/funding/investor fact.
4. Use `/me/whats-new?since=<priority_window_start>&lang=zh` when connected, then inspect funding- and startup-related items even if they were not returned by semantic search.
5. Use `/topics?q=融资 AI&limit=...`, `/topics?q=一级市场 AI&limit=...`, and topic detail endpoints when useful to find article clusters. Use entity search/cards/edges when a candidate company/person is found and the schema exposes financing, investment, founder, or portfolio relationships.
6. Each extracted candidate fact must include: project/company, person if present, financing/event phrase, investor if present, article/content title, author, published date, Elsewhere URL, and next original source to verify.
7. Follow the selected mode's Elsewhere financing/startup fact budget from `references/run-modes.md`: standard scan `5 / 8-15 / 20`, deep map minimum `20`. If Elsewhere returns zero direct candidates, mark the Elsewhere section partial and diagnose whether the cause is query design, endpoint coverage, date filter, API/key issue, or true coverage gap.

- In `topics.md`, add `Elsewhere Keyword Intelligence` when used. Preserve Elsewhere query, extracted terms, founder/company phrases, and how they changed Exa query angles.
- In `validated.md`, add an `Elsewhere API discovery/supplement` subsection when Elsewhere is used for project discovery or new candidate sourcing. Preserve query/endpoint, title/author/date, URL, extracted candidate facts, original-source verification status, and whether the fact came from the `Elsewhere Financing Pass`.
- In the final report or `run-report.md`, add an Elsewhere discovery summary by candidate name: `entered A/B`, `entered C/background`, `downgraded`, or `not used`, with the reason. Elsewhere-sourced projects must be visible even when they are not promoted.
- In `项目背景与证据`, add Elsewhere facts only when they explain the project, product status, founder logic, funding, market context, or recent action.
- In `关联人才与背景`, prefer public-web/Codex search sources for founder/team background and person-project relationship. Elsewhere facts may be cited only when source-backed and linkable; they must not be the required follow-up path for unresolved team/person fields.
- In `来源链接`, include the Elsewhere article/content URL when Elsewhere materially supports a project row. In `项目背景与证据` or talent `背景`, label the fact as `Elsewhere API · {author/title/date}`.
- In `下一步补全项`, do not use Elsewhere backfill or coverage wording for Team, Person, Background, Contact, Product proof, Customer/user proof, Evidence, or Date verification. Use the exact public-web/Codex search gap instead.
- In 来源质量复盘, add a row for `Elsewhere API`: `用途 | query count | keyword terms/chunks/entities/content used | entered A/B | gaps/limitations`.

## Public Source Boundary

Closed platforms are out of scope for search, enrichment, evidence, and rating, except mandatory Elsewhere API through the user's configured/provided key. A project lead can survive when public sources or attributed Elsewhere API reporting are enough to verify the project/product/repo, current activity, and evidence. Responsible person/team and background are enrichment fields for project leads and required for talent rows; contact path is optional context only and never a final talent-column. Read `references/source-policy.md` for the full source boundary.

When a promising candidate points to a closed source:

1. Try to find equivalent public or attributed Elsewhere API evidence from product, repo, author, event, media, paper, investor pages, or Elsewhere article/entity/content endpoints.
2. If equivalent evidence exists, use that evidence and cite the source type clearly.
3. If no public evidence exists, drop the candidate or keep it as `暂不跟进 / 公开证据不足`.
4. Record the limitation in `run-report.md`; do not create a follow-up queue that depends on private user session state.

Tag every raw lead:

| Entry type | Resolution |
|---|---|
| `person` | person -> project/work -> background -> contact |
| `project` | project -> founder/author/maintainer/team -> background -> contact |
| `repo` | repo -> owner/contributors/maintainer -> product/use case -> contact |
| `content` | content -> mentioned person/project -> original evidence -> contact |
| `event` | event -> participating project/team/person -> post-event activity -> contact |
| `paper` | paper -> authors/lab/repo -> application potential -> contact |

Target normalized object: `项目/产品/Repo -> 做了什么 -> 最近动作 -> 项目信号 -> 负责人/团队(可待补) -> 背景(可待补) -> 触达路径(可待补) -> 是否值得跟进`.


## Raw Search

For broad runs, create the four A/B/C/D lane result files. Do not spawn subagents for front-stage search. Main Codex first creates the Exa Candidate Queue. After that, Main Codex may process lanes sequentially, or use optional subagents only for large scans where parallel filtering/enrichment of provided Exa candidates is worth the context overhead. Optional subagent policy: model `gpt-5.4-mini`, reasoning `medium`, one result file per candidate processor.

Default lane path:

1. Main Codex runs broad Exa-only recall for the lane using the lane's keyword groups, source intent, date window, and any `Elsewhere Keyword Intelligence` terms written in `topics.md`, while keeping returned payloads in candidate-queue mode. Use `web_search_advanced_exa` with `enableSummary: false`, no subpages, `highlightsMaxCharacters` capped to a short routing snippet, and `textMaxCharacters: 1`; do not request or accept full page bodies during broad recall. Append every Exa-returned candidate URL/result to `{WORKSPACE}/exa-candidates.jsonl` before filtering, dedupe, enrichment, or context-mode compression. Persist query phrase, lane, URL, normalized URL/domain, returned title/source type hint, Exa returned/published/crawl dates when present, short highlight/routing reason, why it might matter, returned rank/batch id, collection date, lightweight triage fields, `selected_for_review=false`, `fetch_status=pending`, and empty keep/drop fields. Also write a compact lane queue view for human inspection.
2. Immediately after each lane recall batch, Main Codex updates `{WORKSPACE}/exa-candidates.jsonl` and then writes the lane's `Exa Candidate Queue` block before doing any candidate filtering or enrichment. The lane queue may be a compact review view, but the JSONL file must preserve every Exa-returned URL. Before selecting rows to open, run full lightweight triage over all rows: infer source family, entry type, possible signal, risk reason, and project/person/repo cluster; then set `must_open_reason` and `review_decision`. Triage outputs are routing hypotheses only. They must be named and treated as hypotheses (`candidate_name_hypothesis`, `possible_signal`, `risk_reason`) and must not populate final writing fields. When a row is selected, opened, kept, validated, or rated, update `selected_for_review`, `fetch_status`, `keep_drop_status`, `keep_drop_reason`, and `candidate_id` if known. Only opened/fetched rows may receive `keep_drop_status=dropped`.
3. If context-mode is available, Main Codex immediately indexes `{WORKSPACE}/exa-candidates.jsonl` plus that lane's freshly written candidate queue with `ctx_index` using a source label like `ai-mapper-{date}-{lane}-candidate-queue`. For large or high-potential URL sets, use `ctx_fetch_and_index` or `ctx_execute` extraction on Exa-returned URLs before reading long pages into conversation context. This is mandatory for broad runs unless context-mode itself is unavailable; do not wait until raw files are merged at the end. Context-mode may compact snippets and page text, but it must not shrink or rewrite the full Exa candidate audit trail. If context-mode fetching/extraction is unavailable or broken, do not attempt to replace it by bulk `web_fetch_exa` calls into chat; either repair context-mode first or mark the run partial with a `Context-Mode Unavailable` limitation.
4. Main Codex uses `ctx_search` / `ctx_execute` over the indexed queue or fetched pages to support triage and evidence routing. These snippets are routing aids only; Exa text and context-mode snippets are not source evidence.
5. Open/fetch by mandatory buckets, not by vague high-potential feel. Set `must_open_reason` to one of: `official_source`, `funding_source`, `investor_or_vc_source`, `repo_or_model_source`, `paper_or_project_source`, `query_top_result`, `source_family_coverage`, `cluster_representative`, `long_tail_audit`, or `none`. Rows with any non-`none` reason must be selected and opened/fetched unless blocked; rows with `none` remain `not_selected`/`unreviewed`, never `dropped`.
6. Use adaptive continuation after mandatory buckets: for each lane/source-family/query bucket, open another small batch only when the previous batch produced new P0/P1 candidates, new entity clusters, stronger original evidence, or financing/team/date proof. Stop a bucket only after recording low marginal yield, duplicate/stale/out-of-scope patterns, and remaining `not_selected` count.
7. Main Codex or a candidate processor opens/fetches the assigned Exa candidates and discards Exa-only noise before creating raw leads. Verification fetches must be bounded: prefer context-mode indexed fetch/extraction; if using `web_fetch_exa`, cap `maxCharacters`, batch only a few mandatory-bucket/high-yield URLs, and extract structured facts instead of reading or pasting article bodies. The original openable public page, repo, paper, model, product page, or credible report is the evidence.
8. For each kept candidate, create evidence-backed verification fields before raw/final writing: `verified_entity_name`, `verified_event_type`, `claim_supported`, `source_page_date`, `true_event_date` or explicit `date_decision`, `openable_original_url`, and `confidence_level`. If a field is only known from Exa title/snippet or lightweight triage, keep it as a hypothesis in raw/validated notes and do not write it as a final fact.
9. For each kept candidate, produce a detailed raw case: `谁在做 -> 做了什么 -> 最近动作 -> 真实事件日期 -> 背景 -> 触达路径 -> 问什么 -> 缺什么证据`.
10. Drop closed-source candidates outside Elsewhere unless equivalent public or attributed Elsewhere API evidence can support the raw lead.

Common lane-processing instruction:

```text
读取 {WORKSPACE}/topics.md 和已生成的 Exa Candidate Queue。只写指定 lane 的 result file。
不要做独立搜索或新增候选来源。只处理 Main Codex 提供的 Exa query / 候选 URL / 初筛理由，再打开/抓取原始页面筛选。Exa 摘要、Exa publishedDate/crawl date 和 context-mode 检索片段都不能直接写成事实、真实事件日期或评级证据；必须回到原始公开页面。
必须使用当前 web/source inspection，不凭记忆编项目、日期、融资、创始人或联系方式。
每条 raw lead 必须在“最近动态”或“备注”里拆分记录：source_page_date、true_event_date、exa_returned_date（如有）、collection_date、date_decision。不能用 Exa 日期替代真实事件日期。
遇到账号、私域 App、私有浏览器会话、QR 或 CAPTCHA 依赖时，不作为证据；寻找等价公开来源，找不到则降级或丢弃，并在限制中记录。
每条线索包含：名称、入口类型、类型、赛道、找谁、为什么找、怎么找、找了之后问什么、最近动态、主证据链接、补充证据链接、联系入口、证据等级、备注。
备注写：背景：{学校/前公司/项目/成绩/未确认}; 触达：{入口/未确认}; 日期：{source_page_date/true_event_date/exa_returned_date/date_decision}; 已查：{GitHub/公开 X/官网/contact/活动页/论文页/引用页...}。
禁止招聘/岗位页面。
```

Lane coverage:

- `A-dev`: GitHub/GitHub Trending/GitHub releases, Hugging Face Trending/models/spaces/datasets, Product Hunt launches, ModelScope/Gitee public project pages only when directly openable and tied to a concrete project, public hackathons/developer challenges.
- `B-content`: official/company/founder/product blogs, public launch pages, public founder/product retrospectives, demo-day recaps, accelerator interviews, and public synchronized article pages. Do not use generic community/comment feeds except Product Hunt/GitHub/Hugging Face pages from the explicit allowlist.
- `C-funding`: 36氪, 投资界, 创业邦, 猎云网, 亿欧, 雷峰网, 新智元, 量子位, 机器之心, InfoQ, DoNews, TechNode, KrASIA, company announcements, investor/VC portfolio/newsroom pages, public synchronized article pages, incubators, accelerators, demo days, roadshows. Company homepages are verification/enrichment sources when they verify project signal, product status, current action, funding/customer claims, or optional named people/contact details.
- `D-academic`: arXiv, OpenReview, Semantic Scholar, OpenAlex, Papers With Code, ACL Anthology, CVF, NeurIPS/ICLR/ICML proceedings, project/repo/demo pages linked from papers, public lab pages. Citation/venue/repo/demo signals feed project rows and `关联人才与背景`; do not create a separate academic talent table.

Minimum per lane: follow `references/run-modes.md`. Default standard scan uses adaptive lane targets (`A-dev` 10-14 queries, `B-content` 8-12, `C-funding` 14-22, `D-academic` 8-12) with C-funding as the highest-weight lane. Deep map uses the higher lane targets in `references/run-modes.md`. Preserve candidate breadth with enough `numResults`; keep all plausible P0/P1 raw leads through validation. If a lane falls below the selected mode's query/candidate/opened/raw/source-family minimum, write the exact source exhaustion or access blocker in `run-report.md` and mark the run partial/degraded as appropriate. Context compression must not be used as a reason to search less. A lane may be processed by Main Codex or an optional subagent after the Exa Candidate Queue exists, but the output schema is identical and no non-Exa candidate sources may be added by processors. The opened/fetched set must include all mandatory buckets plus adaptive continuation, not only rows that look high-potential from Exa title/snippet.

Each lane result file must include an `Exa Candidate Queue` block before the raw table:

```markdown
## Exa Candidate Queue
| Exa query | Candidate URL | Why it might matter | Opened/fetched? | Keep/drop reason |
|---|---|---|---|---|
```

Raw result table:

```markdown
| 名称 | 入口类型 | 类型 | 一句话描述 | 赛道 | 找谁 | 为什么找 | 怎么找 | 找了之后问什么 | 最近动态 | 主证据链接 | 补充证据链接 | 联系入口 | 证据等级 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

For a raw example row, read `references/examples.md#raw-lead-example`. Do not copy example names as real leads.

Coverage block must include: 搜索次数, 有效线索, 入口类型分布, 找到背后的人/团队, 找到联系方式或触达入口. Evidence levels: `S` original/GitHub/author/product/contact page; `A` founder interview/team/verified/direct profile/Elsewhere first-hand reporting with attribution; `B` media/event/podcast/report/Elsewhere analysis or mention; `C` weak but checkable; `无效`. Elsewhere keyword intelligence alone is not evidence.


## Validate, Enrich, Rate

After raw search, check all four result files exist and are non-empty; repair a missing lane once. Continue on empty lane only with a run-report limitation. Before rating, read `references/rating-rubric.md`.

Write `validated.md` from the four lane files and keep `exa-candidates.jsonl`, `candidates.jsonl`, and `evidence.jsonl` in sync with every normalized candidate and material evidence item:

- Confirm `exa-candidates.jsonl` contains one non-status row for every Exa-returned candidate URL counted in the run report, including dropped, stale, duplicate, and not-selected rows. Missing Exa rows are an audit failure, not a harmless context-saving omission.
- Confirm every Exa row has lightweight triage fields and that all non-`none` `must_open_reason` rows were opened/fetched or explicitly blocked. Rows not opened/fetched must not be marked `dropped`; keep them as `not_selected` or `unreviewed`.
- Merge duplicates while preserving useful evidence.
- Add a separate `Elsewhere API discovery/supplement` subsection. When Elsewhere is available, include discovery and enrichment candidates; do not count it as a fifth raw-search lane. Mark each item as `source_origin=Elsewhere API` and include API endpoint/query, title/author/date, URL, extracted candidate facts, whether an original project/product/person source was also verified, and final disposition by name. In `degraded / Exa-only` runs, keep the subsection with status `not run - Elsewhere unavailable` and the exact reason, so downstream readers can see the gap.
- Normalize each entry type through identity resolution before rating.
- Run date audit before rating: every A/B candidate needs source page date, true event date, collection date, and date decision. Exa-only returned dates do not count. If the true event date is older than the active window, downgrade or keep as background unless there is a newer verified event.
- Academic leads enter `项目类线索` only when there is a projectized artifact: paper/system/benchmark/repo/demo/model/product/lab spinout. Put author/lab/citation/venue/background in `关联人才与背景`; do not create a separate academic talent table.
- `无效` cannot enter project/talent tables.
- Rated rows need at least one openable, traceable, non-repost evidence link.
- Search-layer-only candidates cannot enter `rated.md`: Exa snippets/summaries/returned dates and context-mode snippets are routing aids, not evidence. In a `degraded / Exa-only` run, candidates may enter `rated.md` only after they are backtraced to openable original public pages. Elsewhere API candidates may enter `rated.md` only when the Elsewhere article/content/entity evidence is linkable and source-backed; if the original project/product/person source is not also verified, cap the row at B unless it is explicitly a background/context row. If the source does not support the claimed fact, keep the item in raw/validated as a candidate or downgrade to `暂不跟进 / 待补证据`.
- Final-writing evidence firewall: `项目名`, `一句话描述`, `融资状态`, `关联人才与背景`, `最近有效动态日期`, `评级`, and `项目背景与证据` must be derived from `evidence.jsonl` objects or opened/fetched original pages, never from `exa-candidates.jsonl` triage fields alone. If only a title/snippet suggests a name, funding, date, or relationship, write the exact unresolved gap (`Evidence`, `Date verification`, `Funding`, `Person-project relation`, or `Background`) and cap/downgrade the row instead of turning the hypothesis into fact.
- Preserve raw team/contact notes; do not collapse to generic `未确认`.
- No identifiable person/team and no contact path no longer automatically drops a strong project. Keep it as a project lead if product signal, freshness, evidence, and why-now are strong; mark `待补负责人/核心团队` and `待补触达路径`. Do not enter it into the talent table until person/team is resolved.
- Product evidence with weak team background may still be A/B project-level if project signal is strong; mark missing team background and make the future detailed-search gap explicit.
- GitHub projects above 5000 stars, big-company products, B-round-or-later, mature/high-financing companies -> background samples unless explicitly requested or exposing under-covered qualified talent.
- Ranking/index/community appearance is not rating evidence by itself. Use only the open allowlist of Product Hunt, GitHub Trending/repo/release velocity, and Hugging Face Trending/models/spaces/datasets as radar, then backtrace every product to original project/product/repo/model/paper/funding/customer evidence and recent true event date before A/B consideration. Named person/team and contact are enrichment targets, not hard project gates.
- Closed-source evidence outside Elsewhere cannot support factual claims. If a useful project is only visible through closed sources, keep it as `暂不跟进 / 公开证据不足`; if there is an openable public project/product/funding/source page or attributed Elsewhere API source, missing person/contact fields may be marked `待补`.

### Public-Web Enrichment Pass

Before rating likely A/B candidates and all named people, Main Codex runs targeted Exa searches and opens public pages already tied to Exa candidates. This pass is mandatory in complete and `degraded / Exa-only` runs. It is separate from Elsewhere: Elsewhere can add China tech/venture context and entity relationships, but it must not be used as an excuse to skip open-web checks.

For each likely A/B project, attempt to resolve and record four fields before `rated.md`:

1. Team: founder, core members, maintainer, author, lab, or stable public handle.
2. Funding: round, amount, investors, event date, or a clear `未公开披露` after checking open funding sources.
3. Product proof: product/company site, docs, demo, GitHub/release, model/dataset, customer/deployment page, or public product page.
4. Date proof: source page date, true event date, Exa returned date, collection date, and why the true event date controls freshness.

If any field remains unresolved, write the public sources checked plus the exact gap enum. Do not use Elsewhere backfill wording for Team, Person, Background, Contact, Funding, Product proof, Customer/user proof, Evidence, or Date verification. A single media/report source plus unresolved Team/Funding/Product proof normally caps the row at B.

Targeted public enrichment queries include:

```text
{项目/公司} 创始人 团队 核心成员 作者
{项目/公司} 作者 GitHub X 个人网站 邮箱
{人名} 学校 毕业 前公司 项目 论文 开源 比赛 GitHub X
{项目/公司} contact 邮箱 微信 Twitter X GitHub
{项目/公司} 加速器 创业营 Demo Day 路演 投资机构
{项目/公司} 融资 近30天 天使轮 种子轮 Pre-A 投资方 日期 36氪 投资界 创业邦 猎云网 亿欧 雷峰网 新智元 量子位 机器之心 InfoQ DoNews TechNode KrASIA
{项目/论文/系统} arXiv OpenReview Semantic Scholar OpenAlex citations GitHub demo benchmark dataset model Hugging Face Papers With Code
{项目} Product Hunt GitHub Trending GitHub release Hugging Face Trending model space dataset
```

When Elsewhere is available, keep it as a separate attributed source/discovery/financing pass after or alongside this public-web pass. In `degraded / Exa-only` runs, record Elsewhere as unavailable in the status/source-quality sections, but team/person/background gaps must still be expressed as public-web/Codex search gaps.

After enrichment and before `rated.md`, run a Talent Recovery Pass:

- Extract every named person/team from `关联人才与背景`, raw `找谁`, funding articles, founder/team pages, GitHub maintainers, paper authors, event/demo-day pages, interviews, and other open public pages. Do not depend on Elsewhere entity cards for talent recovery.
- For each extracted person, try to fill the compact talent fields from `references/schemas.md`: `姓名/昵称`, `关联公司/项目`, `最近动作`, `身份`, `背景`, `评级`.
- `最近动作` must include an absolute true event date when available. Normal scans prioritize the last 30 days; older people can stay only when there is a newer verified project action or they are clearly strategic background.
- If the person has a clear project relation plus recent action plus source-backed background, promote to A/B talent even when direct contact is missing. Do not require contact to avoid an empty talent table.
- If the project is strong but the person is unresolved, keep the project row and write `待补负责人/核心团队`; do not invent a talent row.

Create an A-class project audit before `rated.md`. Funding values: `已融资 · {轮次/金额/投资方/真实融资日期/报道日期}`, `未公开披露`, `商业化中 · 未披露融资`, or `大厂/实验室/社区背景样本`; write `未融资` only with explicit source support. Incomplete B rows must name the concrete future detailed-search gap using the gap enum in `references/rating-rubric.md`, not a generic action.

For A-class and downgrade examples, read `references/examples.md#rating-and-downgrade-examples` and `references/rating-rubric.md`.

Before writing final reports, run an output-quality pass:

1. Re-audit every A project row against project gates: Scope, Early, Project signal, Freshness, Evidence, Why now, and Date decision. Person, Background, and Contact are audited as enrichment status: `resolved / partial / 待补`, not pass/fail blockers.
2. Expand every A/B project row into a mentor-decision table row. The table itself must carry the detailed project background, product evidence, person/team background, funding status, uncertainty, true event date, and next completion field; do not rely on separate notes to make the row understandable.
3. Check A/B rows for generic filler: `未确认`, `待补`, `官网`, `contact@`, `可关注`, or market-heat reasons. `待补` is allowed only when paired with a concrete `下一步补全项` for future detailed research; otherwise replace with evidence, a narrower search gap, or downgrade.
4. Keep raw-discovery breadth in raw/validated files; final A/B sections must increase information density in the table rows themselves. Decision cards are optional reinforcement; tables are the primary judgment surface.
5. Do not add a required `触达建议` field. Contact paths may remain in raw/validated notes when public, but final talent tables must not include contact columns and final judgment should not hinge on direct outreach readiness.

## Output Schemas

Read `references/schemas.md` before writing any output artifact. It is the binding schema reference for `validated.md`, `rated.md`, final reports, raw concatenation, latest pointer, high-density project/talent tables, optional judgment cards, and source-quality recap.

Final top-level report must contain complete tables, not just links, and must start with a `运行状态` block: run mode (`adaptive standard scan` / `deep map` / `blocked`), completeness (`complete`, `degraded / Exa-only`, or `blocked`), Elsewhere status, Exa status, stop reason, and impact. Raw artifact concatenates A/B/C/D result files under `# AI-Mapper Raw - {MM-DD}`. Latest pointer includes 更新时间, 搜索主题, 运行模式, 完整性状态, Elsewhere 状态, Exa 状态, 停止原因, 运行目录, 最终文件, 原始合并文件, 结构化候选文件, 结构化证据文件, 运行报告.


## Run Report

`run-report.md` must include:

- 完整性状态 for the whole run (`complete`, `degraded / Exa-only`, or `blocked`) and for A/B/C/D, `validated.md`, `rated.md`
- A 类项目审计: `名称 | Scope | Early | Project signal | Evidence | Freshness | Date decision | Why now | Person status | Background status | Contact status | Result`
- Public-Web Enrichment Pass: candidate name, public queries/source families checked, Team/Funding/Product proof/Date proof status, unresolved gap enum, and whether the row was capped at B because only one media/report source supported it.
- 真实日期审计: `名称 | source_page_date | true_event_date | exa_returned_date | collection_date | date_decision | 结果`
- 字段质量: 背后的人/团队, 团队背景密度, 联系方式/触达入口
- Exa 召回质量: query count, candidate URLs, opened/fetched candidates, kept raw leads, Exa-only drops, stale/crawl-date drops, main limitations
- Exa candidate audit: `exa-candidates.jsonl` non-status row count, duplicate URL count, selected_for_review count, opened/fetched count, dropped/not-selected/stale/crawl-date counts, and not-persisted count. Not-persisted must be `0`; if the run report says 230 Exa candidate URLs, `exa-candidates.jsonl` must contain at least 230 non-status rows.
- Exa triage/open audit: all-row lightweight triage completion, `must_open_reason` distribution, mandatory-bucket opened/fetched/blocked counts, query/source-family/lane coverage counts, entity-cluster representative coverage, adaptive continuation decisions, and any remaining `not_selected`/`unreviewed` counts. Report zero rows where `keep_drop_status=dropped` but `fetch_status` is not `opened`/`fetched`/`blocked`.
- Run mode and budget: selected `run_mode`, minimum/target/cap table from `references/run-modes.md`, deep-map trigger if any, and early-stop/marginal-yield decision
- Exa Search Quantity Gate: total query/source paths, lane query counts, domain/source-filtered query counts, `startPublishedDate`/date-filtered query counts, candidate URLs, opened/fetched pages, kept raw leads, and whether each selected-mode minimum passed
- Recall Volume Gate: total candidate URLs, total opened/fetched pages, total raw leads, C-funding query/candidate/opened/raw counts, lane-level misses, whether the run is complete or partial
- Source Coverage Gate: source families queried, source families with usable candidates, C-funding source-family coverage, queried/no-usable-result sources, and coverage gaps
- Gate pass/fail table, exactly using this header: `Gate | Required | Actual | Pass? | Notes`. Required gate names: `Total Exa query/source paths`, `Total Exa candidate URLs`, `Total opened/fetched original pages`, `Total raw P0/P1 leads`, `C-funding query/source paths`, `C-funding candidate URLs`, `C-funding opened/fetched pages`, `C-funding raw financing/startup leads`, `Source families`, `C-funding source families`, `Elsewhere financing/startup candidate facts`. `Required` must reflect the selected mode from `references/run-modes.md`, not a hard-coded deep-map number. A complete run must mark every selected-mode gate `PASS`; degraded Exa-only runs may mark Elsewhere gate `DEGRADED/N/A/PARTIAL/FAIL` with `0` when Elsewhere is unavailable, but all Exa/public-source gates still need to pass for delivery.
- Elsewhere API 使用质量: connection status, availability preflight result, quota/rate status if unavailable, keyword-intelligence query count, discovery/supplement/enrichment query count, Elsewhere Financing Pass endpoints/queries, chunks/entities/content used, financing/startup candidate facts extracted, rows discovered, rows enriched, Elsewhere API discovery/supplement rows added, Elsewhere candidate names and disposition, Elsewhere-only rows capped/downgraded, coverage gaps, attribution links. If zero direct Elsewhere candidates are found, include a root-cause diagnosis instead of treating it as normal. In `degraded / Exa-only` runs, mark Elsewhere financing/startup candidate facts as `0 / degraded` and explain why the run still produced standard-path artifacts.
- 输出质量门: A project rows checked, A/B high-density table rows expanded, downgraded from A, B rows with concrete 下一步补全项, generic-filler issues remaining
- 公开来源限制: closed/account-only/paywall candidates dropped, equivalent public evidence found, unresolved public-source gaps
- 入口类型质量: `入口类型 | raw lead | resolved to person/team | entered A/B | 主要问题`
- 来源质量复盘 using the same source-quality columns as final report, including Exa, mandatory Elsewhere API, GitHub, Product Hunt, Hugging Face, academic sources, product sites, funding/media pages, investor/company pages, and closed-source drops. Do not include broad ranking databases or generic community feeds as valid source classes.
- 最终产出 counts: A/B/C 类项目, 人才表, 暂不跟进
- 运行限制

## Completion Response

Answer with completeness status, final report path, raw artifact path, latest pointer path, run report path, A/B/C project counts, talent count, and limitations only after `guard-final` and `validate_run.py` have passed for a complete or valid degraded run, or after a real blocker has been recorded. If either script fails because selected-mode quantity/open/source-family gates are below minimum and Exa/workspace are available, do not send a completion response with artifact paths and counts; continue recall/opening instead. For `degraded / Exa-only`, explicitly say Elsewhere was unavailable, the standard output paths were still used, and team/person/background fields were handled by public-web/Codex search gaps rather than Elsewhere backfill wording.
