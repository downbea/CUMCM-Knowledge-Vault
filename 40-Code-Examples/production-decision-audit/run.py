from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from itertools import product
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(__file__).resolve().parent / "output" / "matplotlib")
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import yaml
from scipy.stats import beta, binom

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def output_root(config_path: Path, config: dict) -> Path:
    return (config_path.resolve().parent / config["paths"]["output_root"]).resolve()


def git_commit(root: Path) -> str:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).strip()
        return value
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unavailable"


def minimal_fixed_sample_plan(
    p0: float, p1: float, accept_at_p0: float, reject_at_p1: float, max_n: int
) -> dict[str, float | int]:
    """Find the smallest (n,c): accept when X<=c, otherwise reject."""
    for n in range(1, max_n + 1):
        c = np.arange(n + 1)
        accept0 = binom.cdf(c, n, p0)
        reject1 = binom.sf(c, n, p1)
        feasible = np.flatnonzero((accept0 >= accept_at_p0) & (reject1 >= reject_at_p1))
        if feasible.size:
            cutoff = int(feasible[0])
            return {
                "p0": p0,
                "p1": p1,
                "n": n,
                "accept_max_defects": cutoff,
                "accept_probability_p0": float(binom.cdf(cutoff, n, p0)),
                "reject_probability_p1": float(binom.sf(cutoff, n, p1)),
            }
    raise ValueError(f"No plan found by n={max_n} for p1={p1}")


def exact_decision_boundaries(n: int, p0: float) -> dict[str, int | float | None]:
    reject_candidates = [x for x in range(n + 1) if binom.sf(x - 1, n, p0) <= 0.05]
    accept_candidates = [x for x in range(n + 1) if binom.cdf(x, n, p0) <= 0.10]
    reject_min = min(reject_candidates) if reject_candidates else None
    accept_max = max(accept_candidates) if accept_candidates else None
    return {
        "n": n,
        "p0": p0,
        "accept_if_defects_at_most": accept_max,
        "reject_if_defects_at_least": reject_min,
        "inconclusive_from": None if accept_max is None else accept_max + 1,
        "inconclusive_to": None if reject_min is None else reject_min - 1,
    }


POLICIES = {
    "009": (1, 1, 1),
    "010": (1, 1, 0),
    "011": (1, 0, 1),
    "012": (1, 0, 0),
    "013": (0, 1, 1),
    "014": (0, 1, 0),
    "015": (0, 0, 1),
    "016": (0, 0, 0),
}


def no_disassembly_profit(case: dict, inspect_1: int, inspect_2: int, inspect_product: int) -> float:
    """Expected profit per eventually delivered good unit, without disassembly.

    This is the closed-form model in P03 section 6.1 / Table 3 rows 009--016.
    """
    effective_p1 = 0.0 if inspect_1 else float(case["p1"])
    effective_p2 = 0.0 if inspect_2 else float(case["p2"])
    good_probability = (1.0 - effective_p1) * (1.0 - effective_p2) * (1.0 - float(case["p3"]))
    component_1 = (
        (float(case["buy1"]) + float(case["inspect1"])) / (1.0 - float(case["p1"]))
        if inspect_1
        else float(case["buy1"])
    )
    component_2 = (
        (float(case["buy2"]) + float(case["inspect2"])) / (1.0 - float(case["p2"]))
        if inspect_2
        else float(case["buy2"])
    )
    cost_per_attempt = component_1 + component_2 + float(case["assembly"])
    if inspect_product:
        cost_per_attempt += float(case["inspect_final"])
        expected_cost = cost_per_attempt / good_probability
    else:
        expected_cost = cost_per_attempt / good_probability
        expected_cost += float(case["exchange"]) * (1.0 / good_probability - 1.0)
    return float(case["price"]) - expected_cost


def reproduce_p03_table(config: dict) -> pd.DataFrame:
    reported = config["paper_p03_reported_profit"]
    rows: list[dict[str, float | int | str]] = []
    for policy, choices in POLICIES.items():
        for case in config["problem2_cases"]:
            computed = no_disassembly_profit(case, *choices)
            expected = float(reported[policy][int(case["case"]) - 1])
            rows.append(
                {
                    "policy": policy,
                    "case": int(case["case"]),
                    "inspect_part_1": choices[0],
                    "inspect_part_2": choices[1],
                    "inspect_product": choices[2],
                    "computed_profit": computed,
                    "paper_profit_2dp": expected,
                    "absolute_difference_to_rounded_paper": abs(computed - expected),
                    "within_reported_2dp_tolerance": abs(computed - expected) <= 0.01,
                }
            )
    return pd.DataFrame(rows)


def bayesian_policy_demo(config: dict, rng: np.random.Generator) -> tuple[pd.DataFrame, dict]:
    cfg = config["bayesian_demo"]
    case = next(row.copy() for row in config["problem2_cases"] if row["case"] == cfg["case"])
    a = float(cfg["prior_alpha"]) + int(cfg["observed_defects"])
    b = float(cfg["prior_beta"]) + int(cfg["sample_size"]) - int(cfg["observed_defects"])
    draws = int(cfg["posterior_draws"])
    probabilities = rng.beta(a, b, size=(draws, 3))
    scores = np.zeros((draws, len(POLICIES)), dtype=float)
    policy_ids = list(POLICIES)
    for i, (p1, p2, p3) in enumerate(probabilities):
        varied = case | {"p1": float(p1), "p2": float(p2), "p3": float(p3)}
        for j, choices in enumerate(POLICIES.values()):
            scores[i, j] = no_disassembly_profit(varied, *choices)
    winners = np.argmax(scores, axis=1)
    posterior_mean_case = case | {"p1": a / (a + b), "p2": a / (a + b), "p3": a / (a + b)}
    plug_in = np.array([no_disassembly_profit(posterior_mean_case, *x) for x in POLICIES.values()])
    plug_in_index = int(np.argmax(plug_in))
    oracle = scores[np.arange(draws), winners]
    plug_in_scores = scores[:, plug_in_index]
    summary = pd.DataFrame(
        {
            "policy": policy_ids,
            "selection_count": np.bincount(winners, minlength=len(policy_ids)),
            "selection_probability": np.bincount(winners, minlength=len(policy_ids)) / draws,
            "posterior_mean_profit": scores.mean(axis=0),
            "profit_p05": np.quantile(scores, 0.05, axis=0),
            "profit_p95": np.quantile(scores, 0.95, axis=0),
        }
    )
    meta = {
        "posterior_alpha": a,
        "posterior_beta": b,
        "posterior_mean": a / (a + b),
        "posterior_95_interval": [float(beta.ppf(0.025, a, b)), float(beta.ppf(0.975, a, b))],
        "plug_in_policy": policy_ids[plug_in_index],
        "mean_perfect_information_regret": float(np.mean(oracle - plug_in_scores)),
        "draws": draws,
    }
    return summary, meta


def make_figures(out: Path, plans: pd.DataFrame, bayes: pd.DataFrame) -> None:
    figures = out / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    p_grid = np.linspace(0, 0.30, 301)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for row in plans.itertuples(index=False):
        acceptance = binom.cdf(int(row.accept_max_defects), int(row.n), p_grid)
        ax.plot(p_grid, acceptance, label=f"p1={row.p1:.2f}: n={row.n}, c={row.accept_max_defects}")
    ax.axvline(0.10, color="black", linestyle="--", linewidth=1)
    ax.set(xlabel="真实次品率", ylabel="接收概率", title="精确二项抽样方案的 OC 曲线")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    for suffix in ("png", "svg"):
        fig.savefig(figures / f"sampling_oc_curves.{suffix}", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    shown = bayes[bayes["selection_probability"] > 0].copy()
    ax.bar(shown["policy"], shown["selection_probability"], color="#4C78A8")
    ax.set(xlabel="策略编号（P03 表3）", ylabel="成为最优策略的后验概率", title="Beta 后验下策略稳定性（示例）")
    ax.set_ylim(0, 1)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    for suffix in ("png", "svg"):
        fig.savefig(figures / f"posterior_policy_stability.{suffix}", dpi=180)
    plt.close(fig)


def run(config_path: Path) -> dict:
    started = time.time()
    config = load_config(config_path)
    out = output_root(config_path, config)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(int(config["seed"]))

    sampling = config["sampling"]
    plans = pd.DataFrame(
        [
            minimal_fixed_sample_plan(
                float(sampling["nominal_defect_rate"]),
                float(p1),
                float(sampling["acceptable_probability_at_nominal"]),
                float(sampling["reject_probability_at_alternative"]),
                int(sampling["maximum_sample_size"]),
            )
            for p1 in sampling["alternative_defect_rates"]
        ]
    )
    plans.to_csv(out / "exact_sampling_plans.csv", index=False, encoding="utf-8-sig")

    boundaries = exact_decision_boundaries(
        int(sampling["paper_p03_sample_size"]), float(sampling["nominal_defect_rate"])
    )
    (out / "p03_n43_exact_boundaries.json").write_text(
        json.dumps(boundaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    p03 = reproduce_p03_table(config)
    p03.to_csv(out / "p03_no_disassembly_reproduction.csv", index=False, encoding="utf-8-sig")

    bayes, bayes_meta = bayesian_policy_demo(config, rng)
    bayes.to_csv(out / "beta_binomial_policy_stability.csv", index=False, encoding="utf-8-sig")
    make_figures(out, plans, bayes)

    metrics = {
        "reproduction_grade": "partial-result-level + method-level + example-validation",
        "p03_no_disassembly_cells": int(len(p03)),
        "p03_cells_within_reported_2dp_tolerance": int(
            p03["within_reported_2dp_tolerance"].sum()
        ),
        "p03_max_absolute_difference_to_rounded_value": float(
            p03["absolute_difference_to_rounded_paper"].max()
        ),
        "sampling_alternative_sensitivity": plans.to_dict("records"),
        "p03_n43_exact_boundaries": boundaries,
        "bayesian_demo": bayes_meta,
    }
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    batch_root = config_path.resolve().parents[2]
    runtime = {
        "started_at_epoch": started,
        "finished_at_epoch": time.time(),
        "elapsed_seconds": time.time() - started,
        "seed": int(config["seed"]),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "matplotlib": plt.matplotlib.__version__,
        "config_sha256": sha256(config_path),
        "code_sha256": sha256(Path(__file__)),
        "data_sha256": "official B-problem values embedded in config.yaml; source PDF hashes are recorded in approved paper notes",
        "git_commit": git_commit(batch_root),
        "command": "python run.py --config config.yaml",
    }
    (out / "runtime.json").write_text(json.dumps(runtime, ensure_ascii=False, indent=2), encoding="utf-8")
    environment = "\n".join(
        [
            f"python={sys.version.replace(chr(10), ' ')}",
            f"platform={platform.platform()}",
            f"numpy={np.__version__}",
            f"pandas={pd.__version__}",
            f"scipy={scipy.__version__}",
            f"matplotlib={plt.matplotlib.__version__}",
            f"pyyaml={yaml.__version__}",
            f"seed={config['seed']}",
            f"git_commit={runtime['git_commit']}",
            f"config_sha256={runtime['config_sha256']}",
            f"code_sha256={runtime['code_sha256']}",
        ]
    )
    (out / "environment.txt").write_text(environment + "\n", encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.yaml"))
    args = parser.parse_args()
    metrics = run(args.config)
    rendered = json.dumps(metrics, ensure_ascii=False, indent=2)
    (output_root(args.config, load_config(args.config)) / "run.log").write_text(
        rendered + "\n", encoding="utf-8"
    )
    print(rendered)


if __name__ == "__main__":
    main()
