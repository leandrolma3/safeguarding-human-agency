"""Standalone precision, recall, and F1 computation from evaluation CSVs.

Complements the accuracy tables produced by `analise_resultados.py`.

Expected CSV columns:
  id, tom, estado, vies_aplicado, resposta_esperada,
  resposta_<strategy> (predicted label, "sim"/"nao"/"indefinido"),
  acerto_<strategy> (0/1 match flag).

If resposta_<strategy> columns are present, precision, recall, and F1
are computed from them directly. Otherwise the script falls back to the
acerto_<strategy> flags and reports accuracy only.
"""

from __future__ import annotations

import argparse
from glob import glob
from pathlib import Path

import pandas as pd


STRATEGIES = [
    "baseline",
    "self_help",
    "skill",
    "combo",
]


def _binary_metrics(
    df: pd.DataFrame, gold_col: str, pred_col: str, positive: str
) -> dict[str, float]:
    """Compute precision, recall, F1, and accuracy for a binary label."""
    gold = df[gold_col].astype(str).str.strip().str.lower()
    pred = df[pred_col].astype(str).str.strip().str.lower()
    positive = positive.lower()

    tp = ((gold == positive) & (pred == positive)).sum()
    fp = ((gold != positive) & (pred == positive)).sum()
    fn = ((gold == positive) & (pred != positive)).sum()
    tn = ((gold != positive) & (pred != positive)).sum()
    total = tp + fp + fn + tn

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0.0
    )
    accuracy = (tp + tn) / total if total else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "support": int(total),
    }


def compute_metrics(
    df: pd.DataFrame, strategy: str, positive: str = "sim"
) -> dict[str, float]:
    """Compute per-strategy metrics, preferring predictions when available."""
    pred_col = f"resposta_{strategy}"
    gold_col = "resposta_esperada"

    if pred_col in df.columns and gold_col in df.columns:
        return _binary_metrics(df, gold_col, pred_col, positive)

    acerto_col = f"acerto_{strategy}"
    if acerto_col in df.columns:
        acc = df[acerto_col].fillna(0).mean()
        return {
            "accuracy": float(acc),
            "precision": float("nan"),
            "recall": float("nan"),
            "f1": float("nan"),
            "support": int(len(df)),
        }

    return {
        "accuracy": float("nan"),
        "precision": float("nan"),
        "recall": float("nan"),
        "f1": float("nan"),
        "support": 0,
    }


def _fmt(value: float) -> str:
    if value != value:
        return "n/a"
    return f"{value * 100:.2f}%"


def summarise(dfs: dict[str, pd.DataFrame], positive: str = "sim") -> str:
    """Build a Markdown report aggregating metrics by strategy and bias."""
    lines: list[str] = []
    lines.append("# Metrics Summary")
    lines.append("")
    lines.append("Positive class: **" + positive + "**.")
    lines.append("")

    for tom, df in sorted(dfs.items()):
        lines.append(f"## Tom: {tom}")
        lines.append("")
        lines.append(
            "### Overall (biased + neutral, strategy-level)"
        )
        lines.append("")
        lines.append(
            "| Strategy | Accuracy | Precision | Recall | F1 | N |"
        )
        lines.append("|---|---|---|---|---|---|")
        for strat in STRATEGIES:
            m = compute_metrics(df, strat, positive=positive)
            lines.append(
                f"| {strat} | {_fmt(m['accuracy'])} | {_fmt(m['precision'])} "
                f"| {_fmt(m['recall'])} | {_fmt(m['f1'])} | {m['support']} |"
            )
        lines.append("")

        if "vies_aplicado" in df.columns and "estado" in df.columns:
            biased = df[df["estado"] == "viesada"]
            biases = sorted(biased["vies_aplicado"].dropna().unique())
            for strat in STRATEGIES:
                lines.append(
                    f"### Per-bias metrics for strategy `{strat}` (biased split only)"
                )
                lines.append("")
                lines.append(
                    "| Bias | Accuracy | Precision | Recall | F1 | N |"
                )
                lines.append("|---|---|---|---|---|---|")
                for bias in biases:
                    sub = biased[biased["vies_aplicado"] == bias]
                    m = compute_metrics(sub, strat, positive=positive)
                    lines.append(
                        f"| {bias} | {_fmt(m['accuracy'])} "
                        f"| {_fmt(m['precision'])} | {_fmt(m['recall'])} "
                        f"| {_fmt(m['f1'])} | {m['support']} |"
                    )
                lines.append("")

    return "\n".join(lines)


def _load(pattern: str) -> dict[str, pd.DataFrame]:
    if "," in pattern:
        files = [f.strip() for f in pattern.split(",")]
    else:
        files = sorted(glob(pattern))
    if not files:
        raise FileNotFoundError(f"No file matched: {pattern}")

    dfs: dict[str, pd.DataFrame] = {}
    for f in files:
        df = pd.read_csv(f)
        if "tom" in df.columns and len(df):
            tom = df["tom"].iloc[0]
        else:
            tom = Path(f).stem
        dfs[tom] = df
    return dfs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute accuracy, precision, recall, and F1 from evaluation CSVs."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Glob pattern for evaluation CSVs, or comma-separated list of paths.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Markdown output path; prints to stdout when omitted.",
    )
    parser.add_argument(
        "--positive",
        default="sim",
        help="Positive class label for precision/recall/F1 (default: sim).",
    )
    args = parser.parse_args()

    dfs = _load(args.input)
    report = summarise(dfs, positive=args.positive)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"Metrics summary written to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
