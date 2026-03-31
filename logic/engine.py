"""
engine.py
=========
Core logic for:
  1. analyze_interests(text) → ranked list of career role matches
  2. generate_roadmap(slug)  → structured phase list from roadmap.sh JSON
"""

import os
import json
import re
from difflib import SequenceMatcher

from logic.market_data import ROLES, get_role, get_all_roles

# ── Path to the developer-roadmap JSON files ───────────────────────────────
_REPO_DATA = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "developer-roadmap", "src", "data", "roadmaps"
)


# ══════════════════════════════════════════════════════════════════════════════
# 1. INTEREST → CAREER ROLES
# ══════════════════════════════════════════════════════════════════════════════

def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower()).strip()


def _keyword_score(user_words: list[str], role: dict) -> float:
    """
    Score a role against user's interest words.
    Returns 0.0–1.0 composite score.
    """
    keywords = role["match_keywords"]
    user_text = " ".join(user_words)

    # Exact keyword match (highest weight)
    exact_hits = sum(1 for kw in keywords if kw in user_text)
    exact_score = min(exact_hits / max(len(keywords), 1), 1.0)

    # Fuzzy token match (lower weight)
    fuzzy_hits = 0
    for word in user_words:
        for kw in keywords:
            ratio = SequenceMatcher(None, word, kw).ratio()
            if ratio > 0.82:
                fuzzy_hits += ratio
                break

    fuzzy_score = min(fuzzy_hits / max(len(keywords), 1), 1.0)

    # Market demand bonus (slightly prefer high-demand roles on close ties)
    demand_bonus = role["demand_score"] / 1000.0

    return (exact_score * 0.65) + (fuzzy_score * 0.25) + demand_bonus


def analyze_interests(raw_text: str, top_n: int = 5) -> list[dict]:
    """
    Given a free-text interests string, return the top_n best-matching roles
    with their full market intelligence data, sorted by relevance score.
    """
    if not raw_text or not raw_text.strip():
        # Default: return top roles by demand score
        return sorted(get_all_roles(), key=lambda r: r["demand_score"], reverse=True)[:top_n]

    user_words = _normalize(raw_text).split()
    if not user_words:
        return sorted(get_all_roles(), key=lambda r: r["demand_score"], reverse=True)[:top_n]

    scored = []
    for slug, role in ROLES.items():
        score = _keyword_score(user_words, role)
        if score > 0:
            scored.append((score, role))

    # Sort by score descending, break ties by demand_score
    scored.sort(key=lambda x: (x[0], x[1]["demand_score"]), reverse=True)

    results = [r for _, r in scored[:top_n]]

    # If fewer than 2 matches, backfill with top demand roles not already included
    if len(results) < 2:
        existing_slugs = {r["slug"] for r in results}
        backfill = [
            r for r in sorted(get_all_roles(), key=lambda x: x["demand_score"], reverse=True)
            if r["slug"] not in existing_slugs
        ]
        results += backfill[: top_n - len(results)]

    return results[:top_n]


# ══════════════════════════════════════════════════════════════════════════════
# 2. ROADMAP GENERATION
# ══════════════════════════════════════════════════════════════════════════════

_PHASE_COLORS = [
    {"accent": "#00F2FE", "label_bg": "rgba(0,242,254,0.12)"},
    {"accent": "#4FACFE", "label_bg": "rgba(79,172,254,0.12)"},
    {"accent": "#a78bfa", "label_bg": "rgba(167,139,250,0.12)"},
    {"accent": "#34d399", "label_bg": "rgba(52,211,153,0.12)"},
    {"accent": "#f59e0b", "label_bg": "rgba(245,158,11,0.12)"},
    {"accent": "#ec4899", "label_bg": "rgba(236,72,153,0.12)"},
]


def _load_json(slug: str) -> dict | None:
    path = os.path.join(_REPO_DATA, slug, f"{slug}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_nodes(data: dict) -> list[dict]:
    nodes = []
    for node in data.get("nodes", []):
        node_type = node.get("type", "")
        label = node.get("data", {}).get("label", "").strip()
        resources = node.get("data", {}).get("resources", [])
        if node_type in ("topic", "subtopic", "title") and label:
            nodes.append({
                "id":        node.get("id", ""),
                "type":      node_type,
                "label":     label,
                "resources": resources or [],
                "y":         node.get("position", {}).get("y", 0),
            })
    nodes.sort(key=lambda n: n["y"])
    return nodes


def _group_into_phases(nodes: list[dict]) -> list[dict]:
    phases = []
    current = None

    for node in nodes:
        if node["type"] == "title":
            if current and current["topics"]:
                phases.append(current)
            current = {"title": node["label"], "topics": []}
        elif node["type"] == "topic":
            if current is None:
                current = {"title": node["label"], "topics": []}
            else:
                if current["topics"]:
                    phases.append(current)
                current = {"title": node["label"], "topics": []}
        elif node["type"] == "subtopic":
            if current is None:
                current = {"title": "Getting Started", "topics": []}
            current["topics"].append({
                "label":     node["label"],
                "id":        node["id"],
                "resources": node["resources"],
            })

    if current and current["topics"]:
        phases.append(current)

    # Cap at 12
    if len(phases) > 12:
        overflow = phases[12:]
        extra = []
        for p in overflow:
            extra.extend(p["topics"])
        phases = phases[:12]
        if extra:
            phases.append({"title": "Advanced Topics", "topics": extra})

    for i, phase in enumerate(phases):
        phase["color"] = _PHASE_COLORS[i % len(_PHASE_COLORS)]
        phase["index"] = i + 1

    return phases


def generate_roadmap(slug: str) -> dict:
    """
    Returns structured roadmap data for a given role slug.
    Also includes market intelligence from market_data.
    """
    role_meta = get_role(slug)
    if not role_meta:
        # Try to find the roadmap_slug from any role that matches
        for r in get_all_roles():
            if r.get("roadmap_slug") == slug:
                role_meta = r
                break

    roadmap_slug = role_meta["roadmap_slug"] if role_meta else slug
    title = role_meta["title"] if role_meta else slug.replace("-", " ").title()

    data = _load_json(roadmap_slug)
    if not data:
        return {
            "found": False,
            "slug": slug,
            "roadmap_slug": roadmap_slug,
            "title": title,
            "phases": [],
            "total_topics": 0,
            "market": role_meta,
        }

    nodes = _parse_nodes(data)
    phases = _group_into_phases(nodes)
    total = sum(len(p["topics"]) for p in phases)

    return {
        "found": True,
        "slug": slug,
        "roadmap_slug": roadmap_slug,
        "title": title,
        "phases": phases,
        "total_topics": total,
        "market": role_meta,
    }
