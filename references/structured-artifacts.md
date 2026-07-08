# AI Mapper Structured Artifacts

Use these alongside Markdown artifacts. Markdown remains the human decision surface; JSONL makes validation and repair deterministic.

## Required Files In Each Workspace

```text
{WORKSPACE}/exa-candidates.jsonl
{WORKSPACE}/candidates.jsonl
{WORKSPACE}/evidence.jsonl
```

For blocked runs, create each JSONL file with one `record_type: "status"` record explaining the blocker. Do not leave these files empty. For complete/degraded runs, every Exa-returned URL must be preserved in `exa-candidates.jsonl`, and every A/B project and talent row must map back to at least one candidate and one evidence object.

## Status Records For Blocked Runs

When a run is blocked before candidates or evidence can be collected, write one status record to `exa-candidates.jsonl`, `candidates.jsonl`, and `evidence.jsonl`:

```json
{"record_type":"status","status":"blocked","run_mode":"blocked","blocker_reason":"Exa unavailable","collection_date":"2026-07-07","notes":"No candidate/evidence records were produced."}
```

Required status keys: `record_type`, `status`, `run_mode`, `blocker_reason`, `collection_date`, `notes`. Validator accepts this status record instead of full candidate/evidence keys only when `record_type` is `status`.

## `exa-candidates.jsonl`

One JSON object per Exa-returned candidate URL/result before filtering, dedupe, enrichment, or rating. This is the canonical recall audit trail. Lane Markdown queues may be compact review views; this JSONL file must preserve the full Exa return set.

Required keys:

| Key | Meaning |
|---|---|
| `record_id` | Stable local id such as `exa_0001` |
| `lane` | `A-dev`, `B-content`, `C-funding`, or `D-academic` |
| `exa_query` | Exact Exa query or source path that returned the URL |
| `query_batch_id` | Batch id tying rows to one Exa request |
| `returned_rank` | Rank/index in the Exa response when available |
| `url` | Returned URL exactly as provided |
| `normalized_url` | Canonicalized URL used for dedupe |
| `domain` | URL domain |
| `title` | Returned title |
| `source_type_hint` | Returned/source-inferred type such as repo, funding, product, paper, media, investor |
| `source_family_hint` | Initial source family guess before verification |
| `entry_type_hint` | Lightweight guess: project, person, repo, content, event, paper, funding, investor, product, or unknown |
| `possible_signal` | Lightweight signal: product, funding, team, repo, paper, demo, customer, launch, background, or unknown |
| `risk_reason` | Lightweight risk: stale, duplicate, generic_directory, closed_source, weak_snippet, off_scope, mature, or empty |
| `entity_cluster_id` | Cluster id for likely same project/person/repo across URLs, empty until clustered |
| `must_open_reason` | `official_source`, `funding_source`, `investor_or_vc_source`, `repo_or_model_source`, `paper_or_project_source`, `query_top_result`, `source_family_coverage`, `cluster_representative`, `long_tail_audit`, or `none` |
| `review_decision` | `must_open`, `adaptive_open`, `not_selected`, `defer`, or `blocked` |
| `exa_returned_date` | Exa returned/crawl-like date if present |
| `exa_published_date` | Exa `publishedDate` if present |
| `exa_crawl_date` | Crawl-like date if present |
| `highlight_or_snippet` | Short routing snippet/highlight, not evidence |
| `why_it_might_matter` | Short routing reason for audit and later review |
| `collection_date` | Run date |
| `run_mode` | `adaptive standard scan` or `deep map` |
| `selected_for_review` | Boolean; starts false and becomes true if opened or reviewed |
| `fetch_status` | `pending`, `opened`, `fetched`, `blocked`, `not_selected`, or `not_needed` |
| `keep_drop_status` | `unreviewed`, `kept_raw`, `dropped`, `validated`, `rated`, or `background` |
| `keep_drop_reason` | Why the row was kept, dropped, left unreviewed, or downgraded |
| `candidate_id` | Linked normalized candidate id, empty until resolved |

## `candidates.jsonl`

One JSON object per normalized project/person candidate.

Required keys:

| Key | Meaning |
|---|---|
| `candidate_id` | Stable local id such as `cand_001` |
| `name` | Normalized project/person name |
| `entry_type` | `project`, `person`, `repo`, `content`, `event`, or `paper` |
| `lane` | `A-dev`, `B-content`, `C-funding`, `D-academic`, or `Elsewhere API discovery/supplement` |
| `source_origin` | `Exa`, `Elsewhere API`, or `manual-public-verification` |
| `run_mode` | `adaptive standard scan` or `deep map` |
| `status` | `raw`, `validated`, `rated`, `dropped`, `blocked` |
| `rating` | `A / 重点关注`, `B / 继续观察`, `C / 轻量记录`, `暂不跟进`, or empty before rating |
| `gap_type` | One of the gap enum values in `references/rating-rubric.md` |
| `evidence_ids` | Array of evidence ids supporting the row |
| `notes` | Short uncertainty or dedupe note |

## `evidence.jsonl`

One JSON object per source-backed evidence item.

Required keys:

| Key | Meaning |
|---|---|
| `evidence_id` | Stable local id such as `ev_001` |
| `candidate_id` | Candidate id this evidence supports |
| `url` | Openable URL or Elsewhere URL |
| `source_family` | Source family from `references/source-families.md` |
| `source_type` | product, repo, funding, investor, paper, model, demo, profile, event, media, Elsewhere, etc. |
| `evidence_level` | `S`, `A`, `B`, `C`, or `无效` |
| `claim_supported` | The concrete fact this evidence supports |
| `source_page_date` | Page/article/post/release date or empty if absent |
| `true_event_date` | Real event date used for freshness or empty if not date evidence |
| `exa_returned_date` | Exa returned/crawl-like date if present, never used as freshness evidence |
| `collection_date` | Run date |
| `date_decision` | Which date controls freshness and why |
| `openable_status` | `opened`, `fetched`, `blocked`, `paywall`, `captcha`, `closed`, or `not_needed` |

## Validation Rules

- A/B final rows require at least one non-`无效` evidence object with `openable_status` `opened` or `fetched`.
- A/B final rows require `true_event_date` or a clear `date_decision` explaining why date is not applicable.
- Complete/degraded runs require one `exa-candidates.jsonl` non-status row for every Exa-returned candidate URL counted in the run report's `Total Exa candidate URLs` gate.
- Every non-status Exa row must have lightweight triage fields: `entry_type_hint`, `possible_signal`, `risk_reason`, `entity_cluster_id`, `must_open_reason`, and `review_decision`.
- Any row whose `must_open_reason` is not `none` must have `selected_for_review=true` and `fetch_status` of `opened`, `fetched`, or `blocked`.
- Rows with `fetch_status` outside `opened`/`fetched`/`blocked` must not use `keep_drop_status=dropped`; use `not_selected` or `unreviewed` instead.
- Context-mode compression and lane queue compaction cannot justify missing `exa-candidates.jsonl` rows.
- Exa/context-mode snippets cannot be evidence objects unless backtraced to an original public URL.
- Elsewhere-only candidates can be B at most unless original/open project/product/repo/company/funding evidence is also verified.
