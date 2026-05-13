"""
PLoS ONE Revision — PONE-D-26-07832
Visualization script for Exp1, Exp3, Exp4a, Exp4b, Exp8

Generates all figures needed for the revision.
Run from the project root directory (where results/ lives).

Usage:
    pip install pandas matplotlib numpy scipy seaborn
    python plot_experiments.py

Outputs to: figures/
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

warnings.filterwarnings("ignore")
matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "lines.linewidth": 1.8,
    "lines.markersize": 6,
})

os.makedirs("figures", exist_ok=True)

# ─────────────────────────────────────────────
# STYLE CONFIG
# ─────────────────────────────────────────────
ALGO_STYLE = {
    "V1_BFS_Full":   {"color": "#2563EB", "marker": "o",  "ls": "-",  "label": "V1 (BFS+Full)"},
    "V2_DFS_Full":   {"color": "#16A34A", "marker": "s",  "ls": "--", "label": "V2 (DFS+Full)"},
    "V3_BFS_Search": {"color": "#9333EA", "marker": "^",  "ls": "-.", "label": "V3 (BFS+Search)"},
    "V4_DFS_Search": {"color": "#EA580C", "marker": "D",  "ls": ":",  "label": "V4 (DFS+Search)"},
    "TopKPFIM":      {"color": "#DC2626", "marker": "P",  "ls": "--", "label": "TopKPFIM"},
    "ITUFP":         {"color": "#64748B", "marker": "X",  "ls": "-.", "label": "ITUFP"},
}

CONFIG_STYLE = {
    "FULL":          {"color": "#2563EB", "hatch": "",    "label": "Full (G1–G4)"},
    "NO_G1_frontier":{"color": "#DC2626", "hatch": "//", "label": "No G1 (frontier)"},
    "NO_G2_item":    {"color": "#EA580C", "hatch": "\\\\","label": "No G2 (item)"},
    "NO_G3_upbound": {"color": "#9333EA", "hatch": "xx", "label": "No G3 (upper bound)"},
    "NO_G4_tidset":  {"color": "#16A34A", "hatch": "..", "label": "No G4 (tidset)"},
    "ONLY_G1":       {"color": "#0891B2", "hatch": "||", "label": "Only G1"},
    "ONLY_G2_G3_G4": {"color": "#64748B", "hatch": "--", "label": "Only G2+G3+G4"},
}

GROUP_COLORS = {"G1": "#2563EB", "G2": "#16A34A", "G3": "#9333EA", "G4": "#EA580C"}

DATASET_NAMES = {
    "chess":           "Chess",
    "mushrooms":       "Mushroom",
    "retail":          "Retail",
    "liquor_11frequent": "Liquor",
}

def get_dataset_label(raw):
    for k, v in DATASET_NAMES.items():
        if k in raw:
            return v
    return raw


# ─────────────────────────────────────────────
# LOADERS
# ─────────────────────────────────────────────
def load_exp1_summaries():
    dfs = []
    for f in os.listdir("results/exp1"):
        if f.endswith("_main_comparison_summary.csv"):
            df = pd.read_csv(f"results/exp1/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_exp1_raw():
    dfs = []
    for f in os.listdir("results/exp1"):
        if f.endswith("_main_comparison_raw.csv"):
            df = pd.read_csv(f"results/exp1/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_exp1_wilcoxon():
    dfs = []
    for f in os.listdir("results/exp1"):
        if f.endswith("_wilcoxon.csv"):
            df = pd.read_csv(f"results/exp1/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_exp3():
    dfs = []
    for f in os.listdir("results/exp3"):
        if f.endswith("_sensitivity_jaccard.csv"):
            df = pd.read_csv(f"results/exp3/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_exp4a():
    dfs = []
    for f in os.listdir("results/exp4a"):
        if f.endswith("_group_ablation_summary.csv"):
            df = pd.read_csv(f"results/exp4a/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_exp4b():
    dfs = []
    for f in os.listdir("results/exp4b"):
        if f.endswith("_group_dominance_heatmap.csv"):
            df = pd.read_csv(f"results/exp4b/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


def load_exp8():
    dfs = []
    for f in os.listdir("results/exp8"):
        if f.endswith("_memory_profile.csv"):
            df = pd.read_csv(f"results/exp8/{f}")
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


# ─────────────────────────────────────────────
# FIGURE 1: Runtime vs k — one panel per dataset
# Addresses: B13, C2 (main comparison + baselines)
# ─────────────────────────────────────────────
def plot_exp1_runtime(df_sum):
    if df_sum.empty:
        print("[skip] Exp1 summary empty")
        return

    datasets = df_sum["dataset"].unique()
    n_ds = len(datasets)
    fig, axes = plt.subplots(1, n_ds, figsize=(4.5 * n_ds, 4), sharey=False)
    if n_ds == 1:
        axes = [axes]

    for ax, ds in zip(axes, datasets):
        sub = df_sum[df_sum["dataset"] == ds]
        algos_present = [a for a in ALGO_STYLE if a in sub["algorithm"].values]
        for algo in algos_present:
            s = sub[sub["algorithm"] == algo].sort_values("k")
            st = ALGO_STYLE[algo]
            ax.plot(
                s["k"], s["runtime_mean_ms"] / 1000,
                color=st["color"], marker=st["marker"],
                linestyle=st["ls"], label=st["label"], zorder=3,
            )
            if "runtime_std_ms" in s.columns:
                ax.fill_between(
                    s["k"],
                    (s["runtime_mean_ms"] - s["runtime_std_ms"]) / 1000,
                    (s["runtime_mean_ms"] + s["runtime_std_ms"]) / 1000,
                    alpha=0.12, color=st["color"],
                )
        ax.set_title(get_dataset_label(ds))
        ax.set_xlabel("k (top-k value)")
        ax.set_ylabel("Runtime (s)" if ax is axes[0] else "")
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))

    handles = [Line2D([0], [0], color=ALGO_STYLE[a]["color"],
                      marker=ALGO_STYLE[a]["marker"], linestyle=ALGO_STYLE[a]["ls"],
                      label=ALGO_STYLE[a]["label"]) for a in ALGO_STYLE]
    fig.legend(handles=handles, loc="lower center", ncol=3,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.15))
    fig.suptitle("Fig. 1 — Runtime vs k (mean ± std, 5 reps)", fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig1_runtime_vs_k.pdf")
    fig.savefig("figures/fig1_runtime_vs_k.png")
    plt.close(fig)
    print("[done] Fig1 — runtime vs k")


# ─────────────────────────────────────────────
# FIGURE 2: Candidates explored vs k
# Shows V1 explores far fewer candidates than baselines
# ─────────────────────────────────────────────
def plot_exp1_candidates(df_sum):
    if df_sum.empty or "closure_checks_mean" not in df_sum.columns:
        print("[skip] Exp1 candidates — missing columns")
        return

    datasets = df_sum["dataset"].unique()
    fig, axes = plt.subplots(1, len(datasets), figsize=(4.5 * len(datasets), 4), sharey=False)
    if len(datasets) == 1:
        axes = [axes]

    for ax, ds in zip(axes, datasets):
        sub = df_sum[df_sum["dataset"] == ds]
        for algo in ALGO_STYLE:
            s = sub[sub["algorithm"] == algo].sort_values("k")
            if s.empty:
                continue
            st = ALGO_STYLE[algo]
            ax.plot(s["k"], s["closure_checks_mean"],
                    color=st["color"], marker=st["marker"],
                    linestyle=st["ls"], label=st["label"], zorder=3)
        ax.set_title(get_dataset_label(ds))
        ax.set_xlabel("k")
        ax.set_ylabel("Closure checks (mean)" if ax is axes[0] else "")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    handles = [Line2D([0], [0], color=ALGO_STYLE[a]["color"],
                      marker=ALGO_STYLE[a]["marker"], linestyle=ALGO_STYLE[a]["ls"],
                      label=ALGO_STYLE[a]["label"]) for a in ALGO_STYLE]
    fig.legend(handles=handles, loc="lower center", ncol=3,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.15))
    fig.suptitle("Fig. 2 — Closure checks vs k", fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig2_closure_checks.pdf")
    fig.savefig("figures/fig2_closure_checks.png")
    plt.close(fig)
    print("[done] Fig2 — closure checks")


# ─────────────────────────────────────────────
# FIGURE 3: Speedup ratio over TopKPFIM baseline
# ─────────────────────────────────────────────
def plot_exp1_speedup(df_sum):
    if df_sum.empty:
        print("[skip] Exp1 speedup")
        return

    datasets = df_sum["dataset"].unique()
    algos_to_compare = ["V1_BFS_Full", "V2_DFS_Full", "V3_BFS_Search", "V4_DFS_Search", "ITUFP"]

    fig, axes = plt.subplots(1, len(datasets), figsize=(4.5 * len(datasets), 4), sharey=False)
    if len(datasets) == 1:
        axes = [axes]

    for ax, ds in zip(axes, datasets):
        sub = df_sum[df_sum["dataset"] == ds]
        baseline = sub[sub["algorithm"] == "TopKPFIM"][["k", "runtime_mean_ms"]].rename(
            columns={"runtime_mean_ms": "base_rt"})
        for algo in algos_to_compare:
            s = sub[sub["algorithm"] == algo].sort_values("k")
            if s.empty:
                continue
            merged = s.merge(baseline, on="k")
            speedup = merged["base_rt"] / merged["runtime_mean_ms"]
            st = ALGO_STYLE.get(algo, {"color": "#888", "marker": "o", "ls": "-", "label": algo})
            ax.plot(merged["k"], speedup, color=st["color"],
                    marker=st["marker"], linestyle=st["ls"], label=st["label"], zorder=3)
        ax.axhline(1.0, color="#DC2626", linestyle=":", linewidth=1.0, alpha=0.7)
        ax.set_title(get_dataset_label(ds))
        ax.set_xlabel("k")
        ax.set_ylabel("Speedup over TopKPFIM" if ax is axes[0] else "")

    handles = [Line2D([0], [0], color=ALGO_STYLE.get(a, {"color": "#888"})["color"],
                      marker=ALGO_STYLE.get(a, {"marker": "o"})["marker"],
                      linestyle=ALGO_STYLE.get(a, {"ls": "-"})["ls"],
                      label=ALGO_STYLE.get(a, {"label": a})["label"]) for a in algos_to_compare]
    fig.legend(handles=handles, loc="lower center", ncol=3,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.15))
    fig.suptitle("Fig. 3 — Speedup vs TopKPFIM baseline", fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig3_speedup_vs_baseline.pdf")
    fig.savefig("figures/fig3_speedup_vs_baseline.png")
    plt.close(fig)
    print("[done] Fig3 — speedup")


# ─────────────────────────────────────────────
# FIGURE 4: Runtime boxplot per algorithm (all datasets combined, at representative k)
# ─────────────────────────────────────────────
def plot_exp1_boxplot(df_raw):
    if df_raw.empty:
        print("[skip] Exp1 boxplot — raw data empty")
        return

    # Take middle k value per dataset
    fig, axes = plt.subplots(1, len(df_raw["dataset"].unique()),
                             figsize=(4.0 * len(df_raw["dataset"].unique()), 4))
    if not hasattr(axes, "__iter__"):
        axes = [axes]

    for ax, ds in zip(axes, df_raw["dataset"].unique()):
        sub = df_raw[df_raw["dataset"] == ds]
        ks = sorted(sub["k"].unique())
        rep_k = ks[len(ks) // 2]
        sub_k = sub[sub["k"] == rep_k]

        algos_ordered = [a for a in ALGO_STYLE if a in sub_k["algorithm"].values]
        data = [sub_k[sub_k["algorithm"] == a]["runtime_ms"].values / 1000
                for a in algos_ordered]
        colors = [ALGO_STYLE[a]["color"] for a in algos_ordered]

        bp = ax.boxplot(data, patch_artist=True, notch=False,
                        widths=0.55, showfliers=True,
                        medianprops={"color": "white", "linewidth": 2},
                        flierprops={"marker": "o", "markersize": 4, "alpha": 0.5})
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
        for whisker in bp["whiskers"]:
            whisker.set(linewidth=1.0, alpha=0.7)
        for cap in bp["caps"]:
            cap.set(linewidth=1.0, alpha=0.7)

        ax.set_xticks(range(1, len(algos_ordered) + 1))
        ax.set_xticklabels([ALGO_STYLE[a]["label"].split(" ")[0] for a in algos_ordered],
                           rotation=30, ha="right")
        ax.set_title(f"{get_dataset_label(ds)}  (k={rep_k})")
        ax.set_ylabel("Runtime (s)" if ax is axes[0] else "")

    fig.suptitle("Fig. 4 — Runtime distribution (5 reps, representative k)", fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig4_runtime_boxplot.pdf")
    fig.savefig("figures/fig4_runtime_boxplot.png")
    plt.close(fig)
    print("[done] Fig4 — boxplot")


# ─────────────────────────────────────────────
# FIGURE 5: Exp3 — Uncertainty sensitivity (Jaccard vs reference)
# Addresses: B12, C3 (CRITICAL)
# ─────────────────────────────────────────────
def plot_exp3_sensitivity(df):
    if df.empty:
        print("[skip] Exp3 — no data")
        return

    params = df["param"].unique()
    datasets = df["dataset"].unique()

    n_params = len(params)
    n_ds = len(datasets)
    param_labels = {"alpha": r"$\alpha$", "rho": r"$\rho$",
                    "p_min": r"$P_{\min}$", "p_max": r"$P_{\max}$"}

    fig, axes = plt.subplots(n_ds, n_params, figsize=(3.5 * n_params, 3.5 * n_ds),
                             squeeze=False)

    cmap_ds = ["#2563EB", "#16A34A", "#9333EA", "#EA580C"]

    for row_idx, ds in enumerate(datasets):
        ds_sub = df[df["dataset"] == ds]
        for col_idx, param in enumerate(params):
            ax = axes[row_idx][col_idx]
            sub = ds_sub[ds_sub["param"] == param].sort_values("value")
            if sub.empty:
                ax.set_visible(False)
                continue

            color = cmap_ds[row_idx % len(cmap_ds)]
            ax.plot(sub["value"], sub["jaccard_vs_reference"],
                    color=color, marker="o", linestyle="-", linewidth=1.8)
            ax.fill_between(sub["value"], sub["jaccard_vs_reference"],
                            alpha=0.12, color=color)
            ax.set_ylim(-0.05, 1.15)
            ax.axhline(0.85, color="#DC2626", linestyle="--", linewidth=1.0,
                       label="Threshold (0.85)")
            ax.axhline(1.0, color="#64748B", linestyle=":", linewidth=0.8, alpha=0.6)

            if row_idx == 0:
                ax.set_title(param_labels.get(param, param), fontsize=10)
            if col_idx == 0:
                ax.set_ylabel(f"{get_dataset_label(ds)}\nJaccard", fontsize=8)
            ax.set_xlabel(param_labels.get(param, param), fontsize=8)
            ax.set_ylim(0.8, 1.05)

    axes[0][0].legend(loc="lower right", fontsize=7)
    fig.suptitle("Fig. 5 — Uncertainty sensitivity: Jaccard stability of top-k output\n"
                 "(vs. reference run, per parameter sweep)", fontsize=10, y=1.01)
    fig.tight_layout()
    fig.savefig("figures/fig5_sensitivity_jaccard.pdf")
    fig.savefig("figures/fig5_sensitivity_jaccard.png")
    plt.close(fig)
    print("[done] Fig5 — sensitivity Jaccard")


# ─────────────────────────────────────────────
# FIGURE 6: Exp3 — Sensitivity runtime variation
# ─────────────────────────────────────────────
def plot_exp3_runtime(df):
    if df.empty or "runtime_mean_ms" not in df.columns:
        print("[skip] Exp3 runtime — no data")
        return

    params = df["param"].unique()
    datasets = df["dataset"].unique()
    n_params = len(params)
    param_labels = {"alpha": r"$\alpha$", "rho": r"$\rho$",
                    "p_min": r"$P_{\min}$", "p_max": r"$P_{\max}$"}

    fig, axes = plt.subplots(len(datasets), n_params,
                             figsize=(3.5 * n_params, 3.2 * len(datasets)), squeeze=False)
    cmap_ds = ["#2563EB", "#16A34A", "#9333EA", "#EA580C"]

    for row_idx, ds in enumerate(datasets):
        ds_sub = df[df["dataset"] == ds]
        for col_idx, param in enumerate(params):
            ax = axes[row_idx][col_idx]
            sub = ds_sub[ds_sub["param"] == param].sort_values("value")
            if sub.empty:
                ax.set_visible(False)
                continue
            color = cmap_ds[row_idx % len(cmap_ds)]
            ax.plot(sub["value"], sub["runtime_mean_ms"] / 1000,
                    color=color, marker="s", linestyle="-")
            if row_idx == 0:
                ax.set_title(param_labels.get(param, param))
            if col_idx == 0:
                ax.set_ylabel(f"{get_dataset_label(ds)}\nRuntime (s)", fontsize=8)
            ax.set_xlabel(param_labels.get(param, param), fontsize=8)

    fig.suptitle("Fig. 6 — Runtime variation across uncertainty parameters", fontsize=10, y=1.01)
    fig.tight_layout()
    fig.savefig("figures/fig6_sensitivity_runtime.pdf")
    fig.savefig("figures/fig6_sensitivity_runtime.png")
    plt.close(fig)
    print("[done] Fig6 — sensitivity runtime")


# ─────────────────────────────────────────────
# FIGURE 7: Exp4a — Group ablation speedup bar chart
# Addresses: B11, B13 (MAJOR)
# ─────────────────────────────────────────────
def plot_exp4a_speedup(df):
    if df.empty:
        print("[skip] Exp4a — no data")
        return

    datasets = df["dataset"].unique()
    ks = sorted(df["k"].unique())

    n_ds = len(datasets)
    n_k = len(ks)
    fig, axes = plt.subplots(n_ds, n_k,
                             figsize=(3.5 * n_k, 3.5 * n_ds), squeeze=False)

    configs_ordered = [c for c in CONFIG_STYLE if c in df["config"].values]

    for row_idx, ds in enumerate(datasets):
        ds_sub = df[df["dataset"] == ds]
        for col_idx, k in enumerate(ks):
            ax = axes[row_idx][col_idx]
            sub = ds_sub[ds_sub["k"] == k]
            if sub.empty:
                ax.set_visible(False)
                continue

            x = np.arange(len(configs_ordered))
            speedups = []
            colors = []
            hatches = []
            labels = []
            for cfg in configs_ordered:
                row = sub[sub["config"] == cfg]
                sp = float(row["speedup_vs_full"].values[0]) if not row.empty else 1.0
                speedups.append(sp)
                colors.append(CONFIG_STYLE[cfg]["color"])
                hatches.append(CONFIG_STYLE[cfg]["hatch"])
                labels.append(CONFIG_STYLE[cfg]["label"])

            bars = ax.bar(x, speedups, color=colors, hatch=hatches,
                          edgecolor="white", linewidth=0.5, alpha=0.82)
            ax.axhline(1.0, color="#64748B", linestyle="--", linewidth=1.0, alpha=0.7)
            ax.set_xticks(x)
            ax.set_xticklabels([CONFIG_STYLE[c]["label"].split(" ")[0]
                                 for c in configs_ordered], rotation=40, ha="right", fontsize=7)
            ax.set_ylabel("Speedup vs FULL" if col_idx == 0 else "")

            ds_label = ds.split("/")[-1].replace("_uncertain.txt", "").replace("processed_data", "")
            if row_idx == 0:
                ax.set_title(f"k={k}")
            if col_idx == 0:
                ax.set_ylabel(f"{get_dataset_label(ds_label)}\nSpeedup vs FULL", fontsize=8)

    legend_patches = [mpatches.Patch(facecolor=CONFIG_STYLE[c]["color"],
                                      hatch=CONFIG_STYLE[c]["hatch"],
                                      label=CONFIG_STYLE[c]["label"])
                      for c in configs_ordered]
    fig.legend(handles=legend_patches, loc="lower center", ncol=4,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.08))
    fig.suptitle("Fig. 7 — Group ablation: speedup relative to full TUFCI", fontsize=10, y=1.01)
    fig.tight_layout()
    fig.savefig("figures/fig7_group_ablation_speedup.pdf")
    fig.savefig("figures/fig7_group_ablation_speedup.png")
    plt.close(fig)
    print("[done] Fig7 — group ablation speedup")


# ─────────────────────────────────────────────
# FIGURE 8: Exp4a — Closure checks per config
# ─────────────────────────────────────────────
def plot_exp4a_closure(df):
    if df.empty or "closure_checks_mean" not in df.columns:
        print("[skip] Exp4a closure — missing column")
        return

    datasets = df["dataset"].unique()
    ks = sorted(df["k"].unique())
    configs_ordered = [c for c in CONFIG_STYLE if c in df["config"].values]

    fig, axes = plt.subplots(len(datasets), len(ks),
                             figsize=(3.5 * len(ks), 3.5 * len(datasets)), squeeze=False)

    for row_idx, ds in enumerate(datasets):
        ds_sub = df[df["dataset"] == ds]
        for col_idx, k in enumerate(ks):
            ax = axes[row_idx][col_idx]
            sub = ds_sub[ds_sub["k"] == k]
            if sub.empty:
                ax.set_visible(False)
                continue
            x = np.arange(len(configs_ordered))
            vals = [float(sub[sub["config"] == c]["closure_checks_mean"].values[0])
                    if not sub[sub["config"] == c].empty else 0 for c in configs_ordered]
            colors = [CONFIG_STYLE[c]["color"] for c in configs_ordered]
            ax.bar(x, vals, color=colors, edgecolor="white", linewidth=0.5, alpha=0.82)
            ax.set_xticks(x)
            ax.set_xticklabels([CONFIG_STYLE[c]["label"].split(" ")[0]
                                 for c in configs_ordered], rotation=40, ha="right", fontsize=7)
            if row_idx == 0:
                ax.set_title(f"k={k}")
            ds_label = ds.split("/")[-1].replace("_uncertain.txt", "")
            if col_idx == 0:
                ax.set_ylabel(f"{get_dataset_label(ds_label)}\nClosure checks", fontsize=8)

    fig.suptitle("Fig. 8 — Closure checks per pruning config", fontsize=10, y=1.01)
    fig.tight_layout()
    fig.savefig("figures/fig8_ablation_closure.pdf")
    fig.savefig("figures/fig8_ablation_closure.png")
    plt.close(fig)
    print("[done] Fig8 — ablation closure checks")


# ─────────────────────────────────────────────
# FIGURE 9: Exp4b — Group dominance heatmap
# Addresses: B11 — role of each pruning group
# ─────────────────────────────────────────────
def plot_exp4b_heatmap(df):
    if df.empty:
        print("[skip] Exp4b — no data")
        return

    datasets = df["dataset"].unique()
    groups = ["G1", "G2", "G3", "G4"]

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    for ax_idx, metric in enumerate(["marginal_benefit_pct", "exclusive_benefit_pct"]):
        ax = axes[ax_idx]
        mat = np.zeros((len(datasets), len(groups)))
        row_labels = []
        for ri, ds in enumerate(datasets):
            row_labels.append(get_dataset_label(ds))
            for ci, g in enumerate(groups):
                row = df[(df["dataset"] == ds) & (df["group"] == g)]
                if not row.empty:
                    mat[ri, ci] = float(row[metric].values[0])

        im = ax.imshow(mat, cmap="RdYlGn", aspect="auto", vmin=-20, vmax=100)
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels(groups)
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels)
        for ri in range(len(datasets)):
            for ci in range(len(groups)):
                ax.text(ci, ri, f"{mat[ri, ci]:.1f}%",
                        ha="center", va="center", fontsize=8,
                        color="white" if abs(mat[ri, ci]) > 40 else "black")
        title = ("Marginal benefit\n(% slowdown when removed)"
                 if metric == "marginal_benefit_pct"
                 else "Exclusive benefit\n(% speedup from group alone)")
        ax.set_title(title, fontsize=9)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.suptitle("Fig. 9 — Pruning group dominance analysis (Exp4b)", fontsize=10, y=1.01)
    fig.tight_layout()
    fig.savefig("figures/fig9_group_dominance_heatmap.pdf")
    fig.savefig("figures/fig9_group_dominance_heatmap.png")
    plt.close(fig)
    print("[done] Fig9 — group dominance heatmap")


# ─────────────────────────────────────────────
# FIGURE 10: Exp4b — Runtime comparison bars (FULL vs NONE vs ONLY groups)
# ─────────────────────────────────────────────
def plot_exp4b_bars(df):
    if df.empty:
        print("[skip] Exp4b bars — no data")
        return

    datasets = df["dataset"].unique()
    n_ds = len(datasets)
    fig, axes = plt.subplots(1, n_ds, figsize=(5 * n_ds, 4), sharey=False)
    if n_ds == 1:
        axes = [axes]

    for ax, ds in zip(axes, datasets):
        sub = df[df["dataset"] == ds]
        full_rt = float(sub["runtime_full_ms"].iloc[0]) / 1000
        none_rt = float(sub["runtime_none_ms"].iloc[0]) / 1000

        groups = sub["group"].values
        only_rts = sub["runtime_only_group_ms"].values / 1000
        no_rts = sub["runtime_no_group_ms"].values / 1000

        x = np.arange(len(groups))
        w = 0.35
        ax.bar(x - w / 2, only_rts, w, label="Only this group",
               color=[GROUP_COLORS[g] for g in groups], alpha=0.8, edgecolor="white")
        ax.bar(x + w / 2, no_rts, w, label="All except this group",
               color=[GROUP_COLORS[g] for g in groups], alpha=0.4,
               edgecolor=[GROUP_COLORS[g] for g in groups], linewidth=1.5, hatch="//")
        ax.axhline(full_rt, color="#2563EB", linestyle="-", linewidth=1.5, label=f"FULL ({full_rt:.2f}s)")
        ax.axhline(none_rt, color="#DC2626", linestyle="--", linewidth=1.5, label=f"NONE ({none_rt:.2f}s)")

        ax.set_xticks(x)
        ax.set_xticklabels(groups)
        ax.set_xlabel("Pruning group")
        ax.set_ylabel("Runtime (s)" if ax is axes[0] else "")
        ax.set_title(get_dataset_label(ds))
        ax.legend(fontsize=7)

    fig.suptitle("Fig. 10 — Group contribution: runtime with only/without each group", fontsize=10, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig10_group_contribution_bars.pdf")
    fig.savefig("figures/fig10_group_contribution_bars.png")
    plt.close(fig)
    print("[done] Fig10 — group contribution bars")


# ─────────────────────────────────────────────
# FIGURE 11: Exp8 — Peak heap memory comparison
# Addresses: C4 (MAJOR)
# ─────────────────────────────────────────────
def plot_exp8_memory(df):
    if df.empty:
        print("[skip] Exp8 — no data")
        return

    # Aggregate: mean peak heap per (dataset, k, algorithm)
    mem = df.groupby(["dataset", "k", "algorithm"])[["peak_heap_mb", "runtime_ms"]].mean().reset_index()
    datasets = mem["dataset"].unique()
    n_ds = len(datasets)
    algos = ["V1_BFS_Full", "V2_DFS_Full", "TopKPFIM", "ITUFP"]

    fig, axes = plt.subplots(2, n_ds, figsize=(4.5 * n_ds, 7))
    if n_ds == 1:
        axes = axes.reshape(2, 1)

    for col_idx, ds in enumerate(datasets):
        ds_sub = mem[mem["dataset"] == ds]

        # Top row: peak heap
        ax = axes[0][col_idx]
        for algo in algos:
            s = ds_sub[ds_sub["algorithm"] == algo].sort_values("k")
            if s.empty:
                continue
            st = ALGO_STYLE.get(algo, {"color": "#888", "marker": "o", "ls": "-", "label": algo})
            ax.plot(s["k"], s["peak_heap_mb"], color=st["color"],
                    marker=st["marker"], linestyle=st["ls"], label=st["label"])
        ax.set_title(get_dataset_label(ds))
        ax.set_xlabel("k")
        ax.set_ylabel("Peak heap (MB)" if col_idx == 0 else "")

        # Bottom row: frontier size
        ax2 = axes[1][col_idx]
        if "max_frontier_size" in df.columns:
            fs = df.groupby(["dataset", "k", "algorithm"])["max_frontier_size"].mean().reset_index()
            ds_fs = fs[fs["dataset"] == ds]
            for algo in algos:
                s = ds_fs[ds_fs["algorithm"] == algo].sort_values("k")
                if s.empty:
                    continue
                st = ALGO_STYLE.get(algo, {"color": "#888", "marker": "o", "ls": "-", "label": algo})
                ax2.plot(s["k"], s["max_frontier_size"], color=st["color"],
                         marker=st["marker"], linestyle=st["ls"], label=st["label"])
        ax2.set_xlabel("k")
        ax2.set_ylabel("Max frontier size" if col_idx == 0 else "")

    handles = [Line2D([0], [0], color=ALGO_STYLE.get(a, {"color": "#888"})["color"],
                      marker=ALGO_STYLE.get(a, {"marker": "o"})["marker"],
                      linestyle=ALGO_STYLE.get(a, {"ls": "-"})["ls"],
                      label=ALGO_STYLE.get(a, {"label": a})["label"]) for a in algos]
    fig.legend(handles=handles, loc="lower center", ncol=2,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.05))
    axes[0][0].set_title("Peak heap memory (MB)")
    axes[1][0].set_title("Max frontier size (PQ / Stack / Buffer)")
    fig.suptitle("Fig. 11 — Memory profile: peak heap and frontier size (Exp8)", fontsize=10, y=1.01)
    fig.tight_layout()
    fig.savefig("figures/fig11_memory_profile.pdf")
    fig.savefig("figures/fig11_memory_profile.png")
    plt.close(fig)
    print("[done] Fig11 — memory profile")


# ─────────────────────────────────────────────
# FIGURE 12: Comparative runtime table heatmap (all datasets × algorithms at max k)
# ─────────────────────────────────────────────
def plot_exp1_summary_heatmap(df_sum):
    if df_sum.empty:
        print("[skip] summary heatmap — empty")
        return

    algos = [a for a in ALGO_STYLE if a in df_sum["algorithm"].values]
    datasets = df_sum["dataset"].unique()

    # Use max k per dataset
    pivot_rows = []
    for ds in datasets:
        ds_sub = df_sum[df_sum["dataset"] == ds]
        max_k = ds_sub["k"].max()
        row = {"dataset": get_dataset_label(ds)}
        for algo in algos:
            s = ds_sub[(ds_sub["algorithm"] == algo) & (ds_sub["k"] == max_k)]
            row[ALGO_STYLE[algo]["label"]] = (
                round(s["runtime_mean_ms"].values[0] / 1000, 2) if not s.empty else np.nan
            )
        pivot_rows.append(row)

    pivot = pd.DataFrame(pivot_rows).set_index("dataset")

    fig, ax = plt.subplots(figsize=(10, max(3, 0.6 * len(datasets))))
    mat = pivot.values.astype(float)
    im = ax.imshow(mat, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    for ri in range(mat.shape[0]):
        for ci in range(mat.shape[1]):
            v = mat[ri, ci]
            label = f"{v:.2f}s" if not np.isnan(v) else "—"
            ax.text(ci, ri, label, ha="center", va="center", fontsize=8,
                    color="white" if v > np.nanpercentile(mat, 75) else "black")
    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04).set_label("Runtime (s)")
    ax.set_title("Fig. 12 — Runtime summary at max k (heatmap, seconds)", fontsize=10)
    fig.tight_layout()
    fig.savefig("figures/fig12_runtime_summary_heatmap.pdf")
    fig.savefig("figures/fig12_runtime_summary_heatmap.png")
    plt.close(fig)
    print("[done] Fig12 — summary heatmap")


# ─────────────────────────────────────────────
# FIGURE 13: Memory vs runtime scatter (Exp8)
# ─────────────────────────────────────────────
def plot_exp8_scatter(df):
    if df.empty:
        print("[skip] Exp8 scatter — no data")
        return

    mem = df.groupby(["dataset", "k", "algorithm"])[["peak_heap_mb", "runtime_ms"]].mean().reset_index()
    algos = ["V1_BFS_Full", "V2_DFS_Full", "TopKPFIM", "ITUFP"]

    fig, ax = plt.subplots(figsize=(7, 5))
    for algo in algos:
        s = mem[mem["algorithm"] == algo]
        if s.empty:
            continue
        st = ALGO_STYLE.get(algo, {"color": "#888", "marker": "o", "ls": "-", "label": algo})
        ax.scatter(s["runtime_ms"] / 1000, s["peak_heap_mb"],
                   c=st["color"], marker=st["marker"],
                   s=60, alpha=0.75, label=st["label"], zorder=3)

    ax.set_xlabel("Runtime (s)")
    ax.set_ylabel("Peak heap (MB)")
    handles = [Line2D([0], [0], color=ALGO_STYLE.get(a, {"color": "#888"})["color"],
                      marker=ALGO_STYLE.get(a, {"marker": "o"})["marker"],
                      linestyle="", label=ALGO_STYLE.get(a, {"label": a})["label"]) for a in algos]
    ax.legend(handles=handles)
    ax.set_title("Fig. 13 — Memory vs runtime trade-off (Exp8, all datasets & k values)", fontsize=10)
    fig.tight_layout()
    fig.savefig("figures/fig13_memory_vs_runtime.pdf")
    fig.savefig("figures/fig13_memory_vs_runtime.png")
    plt.close(fig)
    print("[done] Fig13 — memory vs runtime scatter")


# ─────────────────────────────────────────────
# FIGURE 14: Wilcoxon significance summary
# ─────────────────────────────────────────────
def plot_wilcoxon_summary(df_wilcoxon):
    if df_wilcoxon.empty:
        print("[skip] Wilcoxon — no data")
        return

    datasets = df_wilcoxon["dataset"].unique()
    comparisons = df_wilcoxon["comparison"].unique()

    # Build a pivot: rows = comparison, cols = dataset, values = p-value (NaN-safe)
    mat = np.full((len(comparisons), len(datasets)), np.nan)
    v1_faster_mat = np.zeros((len(comparisons), len(datasets)), dtype=bool)

    for ri, cmp in enumerate(comparisons):
        for ci, ds in enumerate(datasets):
            row = df_wilcoxon[(df_wilcoxon["comparison"] == cmp) & (df_wilcoxon["dataset"] == ds)]
            if not row.empty:
                pv = row["p_value"].values[0]
                try:
                    mat[ri, ci] = float(pv)
                except (ValueError, TypeError):
                    mat[ri, ci] = np.nan
                v1_faster_mat[ri, ci] = bool(row["v1_faster"].values[0])

    fig, axes = plt.subplots(1, 2, figsize=(11, max(3, 0.5 * len(comparisons))))
    # Left: p-value heatmap (log scale, NaN = grey)
    ax = axes[0]
    display = np.where(np.isnan(mat), -1, mat)
    cmap = plt.cm.RdYlGn.copy()
    cmap.set_bad(color="#CCCCCC")
    im = ax.imshow(np.where(display < 0, np.nan, display), cmap=cmap,
                   aspect="auto", vmin=0, vmax=0.10)
    ax.set_xticks(range(len(datasets)))
    ax.set_xticklabels([get_dataset_label(d) for d in datasets], rotation=30, ha="right")
    ax.set_yticks(range(len(comparisons)))
    ax.set_yticklabels([c.replace("V1_vs_", "") for c in comparisons], fontsize=7)
    for ri in range(mat.shape[0]):
        for ci in range(mat.shape[1]):
            v = mat[ri, ci]
            label = f"{v:.3f}" if not np.isnan(v) else "N/A"
            ax.text(ci, ri, label, ha="center", va="center", fontsize=6.5,
                    color="black")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label("p-value")
    ax.set_title("p-value (V1 vs others,\n 5 reps Wilcoxon)", fontsize=9)

    # Right: V1 faster?
    ax2 = axes[1]
    v1_display = v1_faster_mat.astype(float)
    im2 = ax2.imshow(v1_display, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax2.set_xticks(range(len(datasets)))
    ax2.set_xticklabels([get_dataset_label(d) for d in datasets], rotation=30, ha="right")
    ax2.set_yticks(range(len(comparisons)))
    ax2.set_yticklabels([c.replace("V1_vs_", "") for c in comparisons], fontsize=7)
    for ri in range(v1_faster_mat.shape[0]):
        for ci in range(v1_faster_mat.shape[1]):
            ax2.text(ci, ri, "✓" if v1_faster_mat[ri, ci] else "✗",
                     ha="center", va="center", fontsize=9,
                     color="white" if v1_faster_mat[ri, ci] else "#444")
    ax2.set_title("V1 faster?\n(✓ = yes)", fontsize=9)

    fig.suptitle("Fig. 14 — Wilcoxon signed-rank test: V1 vs each algorithm", fontsize=10, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig14_wilcoxon_summary.pdf")
    fig.savefig("figures/fig14_wilcoxon_summary.png")
    plt.close(fig)
    print("[done] Fig14 — Wilcoxon summary")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("Loading data …")
    df_sum = load_exp1_summaries()
    df_raw = load_exp1_raw()
    df_wilcoxon = load_exp1_wilcoxon()
    df_sens = load_exp3()
    df_abl = load_exp4a()
    df_dom = load_exp4b()
    df_mem = load_exp8()

    print(f"  Exp1 summary rows: {len(df_sum)}")
    print(f"  Exp1 raw rows:     {len(df_raw)}")
    print(f"  Exp1 Wilcoxon:     {len(df_wilcoxon)}")
    print(f"  Exp3 sensitivity:  {len(df_sens)}")
    print(f"  Exp4a ablation:    {len(df_abl)}")
    print(f"  Exp4b dominance:   {len(df_dom)}")
    print(f"  Exp8 memory:       {len(df_mem)}")
    print()

    print("Generating figures …")
    plot_exp1_runtime(df_sum)
    plot_exp1_candidates(df_sum)
    plot_exp1_speedup(df_sum)
    plot_exp1_boxplot(df_raw)
    plot_exp3_sensitivity(df_sens)
    plot_exp3_runtime(df_sens)
    plot_exp4a_speedup(df_abl)
    plot_exp4a_closure(df_abl)
    plot_exp4b_heatmap(df_dom)
    plot_exp4b_bars(df_dom)
    plot_exp8_memory(df_mem)
    plot_exp12_summary_heatmap = plot_exp1_summary_heatmap
    plot_exp12_summary_heatmap(df_sum)
    plot_exp8_scatter(df_mem)
    plot_wilcoxon_summary(df_wilcoxon)

    print()
    print("All figures saved to figures/")
    print()
    print("Files generated:")
    for f in sorted(os.listdir("figures")):
        size_kb = os.path.getsize(f"figures/{f}") // 1024
        print(f"  figures/{f}  ({size_kb} KB)")


if __name__ == "__main__":
    main()