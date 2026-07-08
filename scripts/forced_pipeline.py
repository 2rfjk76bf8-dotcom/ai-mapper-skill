#!/usr/bin/env python3
"""Fail-closed guardrail for ai-mapper runs without sub-agents.

This script is intentionally deterministic. It does not decide which leads are
interesting; it only enforces that recall and evidence plumbing happened before
final output can be treated as complete.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse, urlunparse


LANES = {"A-dev", "B-content", "C-funding", "D-academic"}

STANDARD_MINIMUMS = {
    "Total Exa query/source paths": 36,
    "Total Exa candidate URLs": 160,
    "Total opened/fetched original pages": 50,
    "Total raw P0/P1 leads": 30,
    "C-funding query/source paths": 12,
    "C-funding candidate URLs": 70,
    "C-funding opened/fetched pages": 18,
    "C-funding raw financing/startup leads": 10,
    "Source families": 10,
    "C-funding source families": 6,
    "Elsewhere financing/startup candidate facts": 5,
}

DEEP_MINIMUMS = {
    "Total Exa query/source paths": 100,
    "Total Exa candidate URLs": 500,
    "Total opened/fetched original pages": 150,
    "Total raw P0/P1 leads": 100,
    "C-funding query/source paths": 50,
    "C-funding candidate URLs": 300,
    "C-funding opened/fetched pages": 80,
    "C-funding raw financing/startup leads": 50,
    "Source families": 18,
    "C-funding source families": 10,
    "Elsewhere financing/startup candidate facts": 20,
}

REQUIRED_ELSEWHERE_ENDPOINT_GROUPS = {
    "search_chunks",
    "whats_new",
    "topics",
    "content_detail",
    "entity_lookup",
    "entity_card_or_edges",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_exa_payload(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return [row for row in payload["results"] if isinstance(row, dict)]
    if isinstance(payload, list):
        results: list[dict[str, object]] = []
        for item in payload:
            if isinstance(item, dict) and isinstance(item.get("results"), list):
                results.extend(row for row in item["results"] if isinstance(row, dict))
            elif isinstance(item, dict) and item.get("type") == "text":
                text = str(item.get("text", ""))
                try:
                    inner = json.loads(text)
                except json.JSONDecodeError:
                    continue
                if isinstance(inner, dict) and isinstance(inner.get("results"), list):
                    results.extend(row for row in inner["results"] if isinstance(row, dict))
        return results
    raise ValueError(f"Unsupported Exa response shape: {path}")


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/") or "/", "", "", ""))


def source_family(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if "github.com" in domain:
        return "GitHub"
    if "36kr.com" in domain:
        return "36氪"
    if "huggingface.co" in domain:
        return "Hugging Face"
    if "producthunt.com" in domain:
        return "Product Hunt"
    if any(name in domain for name in ("arxiv", "openreview", "semanticscholar", "openalex", "alphaxiv")):
        return "arXiv/OpenReview/Semantic Scholar/OpenAlex"
    if any(name in domain for name in ("technode", "kr-asia", "kr-asia.com")):
        return "TechNode / KrASIA"
    if any(name in domain for name in ("cyzone", "lieyunwang", "iyiou", "donews", "infoq")):
        return "Funding/media"
    return "Product/company site" if "." in domain else "unknown"


def entry_type(url: str, title: str) -> str:
    text = f"{url} {title}".lower()
    if "github.com" in text:
        return "repo"
    if any(term in text for term in ("arxiv", "openreview", "paper", "benchmark", "论文")):
        return "paper"
    if any(term in text for term in ("融资", "funding", "seed", "pre-a", "angel", "天使轮", "种子轮")):
        return "funding"
    if any(term in text for term in ("launch", "发布", "上线", "product")):
        return "project"
    return "unknown"


def must_open_reason(family: str, kind: str, rank: int) -> str:
    if kind == "repo":
        return "repo_or_model_source"
    if kind == "paper":
        return "paper_or_project_source"
    if kind == "funding":
        return "funding_source"
    if family in {"Product/company site", "Hugging Face", "Product Hunt"}:
        return "official_source"
    if rank <= 3:
        return "query_top_result"
    return "none"


def next_record_index(path: Path) -> int:
    rows = read_jsonl(path)
    return len([row for row in rows if row.get("record_type") != "status"]) + 1


def record_exa_response(args: argparse.Namespace) -> int:
    if args.lane not in LANES:
        raise SystemExit(f"invalid lane: {args.lane}")
    workspace = Path(args.workspace)
    exa_path = workspace / "exa-candidates.jsonl"
    start = next_record_index(exa_path)
    results = load_exa_payload(Path(args.response_file))
    rows: list[dict[str, object]] = []
    for offset, result in enumerate(results):
        url = str(result.get("url") or result.get("id") or "").strip()
        if not url:
            continue
        rank = int(result.get("rank") or offset + 1)
        title = str(result.get("title") or "")
        family = source_family(url)
        kind = entry_type(url, title)
        reason = must_open_reason(family, kind, rank)
        rows.append(
            {
                "record_id": f"exa_{start + len(rows):04d}",
                "lane": args.lane,
                "exa_query": args.query,
                "query_batch_id": args.batch_id,
                "returned_rank": rank,
                "url": url,
                "normalized_url": normalize_url(url),
                "domain": urlparse(url).netloc.lower(),
                "title": title,
                "source_type_hint": kind,
                "source_family_hint": family,
                "entry_type_hint": kind,
                "possible_signal": "funding" if kind == "funding" else ("repo" if kind == "repo" else ("paper" if kind == "paper" else "product")),
                "risk_reason": "empty" if title else "weak_snippet",
                "entity_cluster_id": "",
                "must_open_reason": reason,
                "review_decision": "must_open" if reason != "none" else "not_selected",
                "exa_returned_date": str(result.get("publishedDate") or ""),
                "exa_published_date": str(result.get("publishedDate") or ""),
                "exa_crawl_date": str(result.get("crawlDate") or ""),
                "highlight_or_snippet": " ".join(str(x) for x in result.get("highlights", [])[:1]) if isinstance(result.get("highlights"), list) else "",
                "why_it_might_matter": title or url,
                "collection_date": args.collection_date,
                "run_mode": args.run_mode,
                "selected_for_review": reason != "none",
                "fetch_status": "pending",
                "keep_drop_status": "unreviewed",
                "keep_drop_reason": "recorded before filtering; original Exa return preserved",
                "candidate_id": "",
            }
        )
    append_jsonl(exa_path, rows)
    print(json.dumps({"recorded": len(rows), "path": str(exa_path)}, ensure_ascii=False))
    return 0


def gate_minimums(run_mode: str) -> dict[str, int]:
    return DEEP_MINIMUMS if run_mode == "deep map" else STANDARD_MINIMUMS


def count_raw_p0_p1(candidates: list[dict[str, object]]) -> int:
    count = 0
    for row in candidates:
        if row.get("status") not in {"raw", "validated", "rated"}:
            continue
        rating = str(row.get("rating", ""))
        notes = str(row.get("notes", ""))
        if rating.startswith(("A", "B")) or "P0" in notes or "P1" in notes:
            count += 1
    return count


def count_elsewhere_facts(candidates: list[dict[str, object]]) -> int:
    return sum(1 for row in candidates if row.get("source_origin") == "Elsewhere API")


def actuals(workspace: Path) -> dict[str, int]:
    exa = [row for row in read_jsonl(workspace / "exa-candidates.jsonl") if row.get("record_type") != "status"]
    candidates = [row for row in read_jsonl(workspace / "candidates.jsonl") if row.get("record_type") != "status"]
    opened = [row for row in exa if row.get("fetch_status") in {"opened", "fetched"}]
    c_funding = [row for row in exa if row.get("lane") == "C-funding"]
    c_opened = [row for row in c_funding if row.get("fetch_status") in {"opened", "fetched"}]
    families = {str(row.get("source_family_hint")) for row in exa if row.get("source_family_hint")}
    c_families = {str(row.get("source_family_hint")) for row in c_funding if row.get("source_family_hint")}
    query_paths = {(row.get("lane"), row.get("query_batch_id")) for row in exa}
    c_query_paths = {(row.get("lane"), row.get("query_batch_id")) for row in c_funding}
    c_raw = [
        row
        for row in candidates
        if row.get("lane") == "C-funding" and row.get("status") in {"raw", "validated", "rated"}
    ]
    return {
        "Total Exa query/source paths": len(query_paths),
        "Total Exa candidate URLs": len(exa),
        "Total opened/fetched original pages": len(opened),
        "Total raw P0/P1 leads": count_raw_p0_p1(candidates),
        "C-funding query/source paths": len(c_query_paths),
        "C-funding candidate URLs": len(c_funding),
        "C-funding opened/fetched pages": len(c_opened),
        "C-funding raw financing/startup leads": len(c_raw),
        "Source families": len(families),
        "C-funding source families": len(c_families),
        "Elsewhere financing/startup candidate facts": count_elsewhere_facts(candidates),
    }


def elsewhere_endpoint_errors(workspace: Path, elsewhere_status: str) -> list[str]:
    if elsewhere_status != "available":
        return []
    rows = read_jsonl(workspace / "elsewhere-api-audit.jsonl")
    groups = {str(row.get("endpoint_group")) for row in rows}
    missing = sorted(REQUIRED_ELSEWHERE_ENDPOINT_GROUPS - groups)
    if missing:
        return [f"Elsewhere endpoint coverage incomplete; missing: {', '.join(missing)}"]
    return []


def exa_transition_errors(workspace: Path) -> list[str]:
    errors: list[str] = []
    rows = read_jsonl(workspace / "exa-candidates.jsonl")
    required = [row for row in rows if row.get("must_open_reason") not in {"", "none", None}]
    unopened = [
        str(row.get("record_id"))
        for row in required
        if row.get("fetch_status") not in {"opened", "fetched", "blocked"}
    ]
    if unopened:
        preview = ", ".join(unopened[:10])
        errors.append(f"mandatory Exa rows not opened/fetched/blocked: {preview}")
    bad_dropped = [
        str(row.get("record_id"))
        for row in rows
        if row.get("keep_drop_status") == "dropped" and row.get("fetch_status") not in {"opened", "fetched", "blocked"}
    ]
    if bad_dropped:
        errors.append(f"unopened rows marked dropped: {', '.join(bad_dropped[:10])}")
    duplicates = [url for url, count in Counter(str(row.get("normalized_url")) for row in rows).items() if url and count > 1]
    if duplicates:
        errors.append(f"duplicate normalized_url rows require explicit duplicate status: {', '.join(duplicates[:5])}")
    return errors


def guard_final(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace)
    minimums = gate_minimums(args.run_mode)
    values = actuals(workspace)
    errors: list[str] = []
    quantity_errors: list[str] = []
    for gate, minimum in minimums.items():
        actual = values.get(gate, 0)
        if actual < minimum:
            message = f"{gate}: actual {actual} below minimum {minimum}"
            errors.append(message)
            quantity_errors.append(message)
    errors.extend(elsewhere_endpoint_errors(workspace, args.elsewhere_status))
    errors.extend(exa_transition_errors(workspace))
    if errors:
        sys.stderr.write("ai-mapper forced pipeline forbids final/latest output:\n")
        if quantity_errors:
            sys.stderr.write(
                "- Quantity/open/source-family gates below minimum are not a valid blocked deliverable "
                "while Exa/workspace are available; continue Exa recall, persistence, and mandatory opening.\n"
            )
        for error in errors:
            sys.stderr.write(f"- {error}\n")
        return 1
    print(json.dumps({"status": "pass", "actuals": values}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ai-mapper no-subagent forced pipeline guard")
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record-exa-response", help="Append every Exa-returned URL before filtering")
    record.add_argument("--workspace", required=True)
    record.add_argument("--lane", required=True, choices=sorted(LANES))
    record.add_argument("--query", required=True)
    record.add_argument("--batch-id", required=True)
    record.add_argument("--response-file", required=True)
    record.add_argument("--collection-date", required=True)
    record.add_argument("--run-mode", default="adaptive standard scan", choices=["adaptive standard scan", "deep map"])
    record.set_defaults(func=record_exa_response)

    guard = sub.add_parser("guard-final", help="Fail closed unless recall, Elsewhere, and open-page gates pass")
    guard.add_argument("--workspace", required=True)
    guard.add_argument("--run-mode", default="adaptive standard scan", choices=["adaptive standard scan", "deep map"])
    guard.add_argument("--elsewhere-status", default="available", choices=["available", "missing_key", "quota_exhausted", "rate_limited", "error", "not_run"])
    guard.set_defaults(func=guard_final)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
