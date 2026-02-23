#!/usr/bin/env python3
"""Descriptive management-style summary from a mela2 simulation sqlite DB.

This script classifies each leaf alternative into descriptive archetypes using:
- stand age at the leaf (`stands.dominant_storey_age`)
- number of thinning / clearfell / regeneration / soil-prep actions along the node path
- optional explicit style tags (prefix configurable, default: `style_`)

Example:
  python scripts/management_style_summary.py out/simulation_results.db
"""

from __future__ import annotations

import argparse
import ast
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class PathStats:
    thin_count: int = 0
    clearfell_count: int = 0
    regen_count: int = 0
    soilprep_count: int = 0
    explicit_style_tags: list[str] | None = None


def parse_tags(raw: str | None) -> set[str]:
    if not raw:
        return set()
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, set):
            return {str(x) for x in parsed}
        if isinstance(parsed, (list, tuple)):
            return {str(x) for x in parsed}
        return {str(parsed)}
    except Exception:
        return {x.strip() for x in raw.split(",") if x.strip()}


def _safe_float(v) -> float | None:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None


def _infer_path_stats(cur: sqlite3.Cursor, stand: str, leaf_identifier: str, style_prefix: str) -> PathStats:
    # Node identifiers form a path like 0-1-2. Include all prefixes as ancestors.
    parts = leaf_identifier.split("-")
    prefixes = ["-".join(parts[:i]) for i in range(1, len(parts) + 1)]

    placeholders = ",".join("?" for _ in prefixes)
    rows = cur.execute(
        f"""
        SELECT identifier, done_treatment, tags
        FROM nodes
        WHERE stand = ? AND identifier IN ({placeholders})
        """,
        [stand, *prefixes],
    ).fetchall()

    stats = PathStats(explicit_style_tags=[])
    for _id, treatment, tag_text in rows:
        t = (treatment or "").lower()
        tags = parse_tags(tag_text)

        # explicit style tags from control event tags
        for tg in tags:
            if tg.startswith(style_prefix):
                stats.explicit_style_tags.append(tg)

        # Heuristics for treatment counting
        if "cut" in t or "thin" in t:
            stats.thin_count += 1
        if "clear" in t or "final" in t:
            stats.clearfell_count += 1
        if "regeneration" in t or "plant" in t:
            stats.regen_count += 1
        if "soil_surface_preparation" in t or "mound" in t:
            stats.soilprep_count += 1

        # Tag-level fallback for custom naming
        if any("clear" in tg for tg in tags):
            stats.clearfell_count += 1
        if any("thin" in tg for tg in tags):
            stats.thin_count += 1

    # De-duplicate style tags while keeping stable order
    stats.explicit_style_tags = list(dict.fromkeys(stats.explicit_style_tags))
    return stats


def classify_leaf(age: float | None, stats: PathStats) -> str:
    """Descriptive class labels inspired by management-policy style archetypes."""
    if stats.clearfell_count == 0 and stats.thin_count >= 3:
        return "continuous_cover_thinning_dominated"

    if age is not None and age > 100:
        return "extended_rotation_management"

    if age is not None and age < 70:
        if stats.regen_count >= 1:
            return "shortened_rotation_regeneration_driven"
        return "shortened_rotation_management"

    if stats.regen_count >= 2:
        return "regeneration_intensive_pathway"

    if stats.soilprep_count >= 1 and stats.regen_count >= 1:
        return "site_prep_plus_regeneration"

    return "baseline_or_mixed_management"


def summarize(db_path: str, style_prefix: str) -> None:
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    rows = cur.execute(
        """
        SELECT n.stand, n.identifier, n.tags, s.dominant_storey_age
        FROM nodes n
        LEFT JOIN stands s ON s.node = n.identifier AND s.identifier = n.stand
        WHERE n.leaf = 1
        """
    ).fetchall()

    if not rows:
        print("No leaf rows found in nodes table.")
        return

    class_counter: Counter[str] = Counter()
    explicit_style_counter: Counter[str] = Counter()
    stand_class_counter: defaultdict[str, Counter[str]] = defaultdict(Counter)

    for stand, leaf_id, leaf_tags, dominant_age in rows:
        _ = leaf_tags  # currently unused, path-level tags are used
        age = _safe_float(dominant_age)
        stats = _infer_path_stats(cur, stand, leaf_id, style_prefix)
        class_name = classify_leaf(age, stats)

        class_counter[class_name] += 1
        stand_class_counter[str(stand)][class_name] += 1

        if stats.explicit_style_tags:
            for tg in stats.explicit_style_tags:
                explicit_style_counter[tg] += 1
        else:
            explicit_style_counter["style_unknown"] += 1

    total = sum(class_counter.values())
    print("=== Descriptive management summary (leaf alternatives) ===")
    print(f"Total leaf alternatives: {total}")

    print("\nInferred descriptive classes:")
    for cls, n in class_counter.most_common():
        print(f"  {cls:40s} {n:8d} ({100.0*n/total:5.1f}%)")

    print("\nExplicit style tags seen in paths:")
    for style, n in explicit_style_counter.most_common():
        print(f"  {style:40s} {n:8d}")

    print("\nPer-stand dominant inferred class:")
    dominant = Counter()
    for stand, c in stand_class_counter.items():
        d_cls, _ = c.most_common(1)[0]
        dominant[d_cls] += 1
    for cls, n in dominant.most_common():
        print(f"  {cls:40s} {n:8d} stands")

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db", help="Path to simulation sqlite database (e.g. out/simulation_results.db)")
    parser.add_argument("--style-prefix", default="style_", help="Tag prefix used for explicit style tags")
    args = parser.parse_args()
    summarize(args.db, args.style_prefix)
