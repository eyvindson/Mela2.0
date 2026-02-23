#!/usr/bin/env python3
"""Split a .gpkg into stand-based chunks and run mela2 in parallel.

Example:
    python run_gpkg_multiprocess.py \
        --input data.gpkg \
        --control control_cross_Y.py \
        --output-root mp_runs \
        --cores 8
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class ChunkTask:
    chunk_index: int
    chunk_gpkg: Path
    output_dir: Path
    control_file: Path
    mela2_cmd: str


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a GPKG by standid and run mela2 for each chunk in parallel."
    )
    parser.add_argument("--input", required=True, help="Path to source .gpkg file")
    parser.add_argument("--control", required=True, help="Path to control python file (e.g. control_cross_Y.py)")
    parser.add_argument("--output-root", required=True, help="Directory for chunk gpkg files and outputs")
    parser.add_argument("--cores", type=int, default=os.cpu_count() or 1, help="Number of parallel workers/chunks")
    parser.add_argument("--mela2-cmd", default="mela2", help="Command name/path for mela2 executable")
    parser.add_argument("--keep-existing", action="store_true", help="Reuse existing output-root instead of deleting")
    return parser.parse_args()


def _load_stand_ids(gpkg_path: Path) -> list[int]:
    with sqlite3.connect(gpkg_path) as conn:
        rows = conn.execute("SELECT DISTINCT standid FROM stand ORDER BY standid").fetchall()
    return [int(row[0]) for row in rows]


def _split_evenly(items: Sequence[int], parts: int) -> list[list[int]]:
    if parts <= 1:
        return [list(items)]
    chunk_size = max(1, math.ceil(len(items) / parts))
    return [list(items[i:i + chunk_size]) for i in range(0, len(items), chunk_size)]


def _prune_chunk_gpkg(chunk_path: Path, keep_stand_ids: Sequence[int]) -> None:
    placeholders = ",".join(["?"] * len(keep_stand_ids))
    with sqlite3.connect(chunk_path) as conn:
        conn.execute("PRAGMA foreign_keys = OFF")

        conn.execute(f"DELETE FROM restriction WHERE standid NOT IN ({placeholders})", tuple(keep_stand_ids))
        conn.execute(f"DELETE FROM treestand WHERE standid NOT IN ({placeholders})", tuple(keep_stand_ids))
        conn.execute("DELETE FROM treestratum WHERE treestandid NOT IN (SELECT treestandid FROM treestand)")
        conn.execute(f"DELETE FROM stand WHERE standid NOT IN ({placeholders})", tuple(keep_stand_ids))

        # Optional cleanup for known stand-linked auxiliary tables if they exist.
        for table_name in ("standspecialfeature", "managementarea", "standoperationalrestriction"):
            exists = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
            ).fetchone()
            if exists:
                conn.execute(f"DELETE FROM {table_name} WHERE standid NOT IN ({placeholders})", tuple(keep_stand_ids))

        conn.commit()


def _run_chunk(task: ChunkTask) -> tuple[int, int]:
    cmd = [
        task.mela2_cmd,
        str(task.chunk_gpkg),
        str(task.output_dir),
        str(task.control_file),
        "--delete",
    ]
    print(f"[chunk {task.chunk_index}] Running: {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, check=False)
    return task.chunk_index, result.returncode


def main() -> int:
    args = _parse_args()

    input_path = Path(args.input).resolve()
    control_path = Path(args.control).resolve()
    output_root = Path(args.output_root).resolve()
    workers = max(1, int(args.cores))

    if not input_path.exists() or input_path.suffix.lower() != ".gpkg":
        raise SystemExit(f"Input must be an existing .gpkg file: {input_path}")
    if not control_path.exists():
        raise SystemExit(f"Control file not found: {control_path}")

    if output_root.exists() and not args.keep_existing:
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    stand_ids = _load_stand_ids(input_path)
    if not stand_ids:
        raise SystemExit("No standid rows found in stand table; nothing to process.")

    stand_chunks = _split_evenly(stand_ids, workers)
    print(f"Found {len(stand_ids)} stands -> {len(stand_chunks)} chunk(s)")

    tasks: list[ChunkTask] = []
    for idx, chunk in enumerate(stand_chunks, start=1):
        chunk_dir = output_root / f"chunk_{idx:03d}"
        chunk_dir.mkdir(parents=True, exist_ok=True)

        chunk_gpkg = chunk_dir / f"input_chunk_{idx:03d}.gpkg"
        shutil.copy2(input_path, chunk_gpkg)
        _prune_chunk_gpkg(chunk_gpkg, chunk)

        out_dir = chunk_dir / "out"
        out_dir.mkdir(parents=True, exist_ok=True)

        tasks.append(
            ChunkTask(
                chunk_index=idx,
                chunk_gpkg=chunk_gpkg,
                output_dir=out_dir,
                control_file=control_path,
                mela2_cmd=args.mela2_cmd,
            )
        )

    # Use processes so each chunk is handled by its own worker/CPU slot.
    from multiprocessing import Pool

    with Pool(processes=min(workers, len(tasks))) as pool:
        results = pool.map(_run_chunk, tasks)

    failures = [(i, rc) for i, rc in results if rc != 0]
    if failures:
        print("Some chunk runs failed:")
        for i, rc in failures:
            print(f"  - chunk {i}: exit code {rc}")
        return 1

    print("All chunk runs completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
