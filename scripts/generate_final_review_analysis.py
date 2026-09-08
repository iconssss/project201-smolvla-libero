"""Generate CPU-only archive analyses from the cached completed-run artifacts."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT = Path(__file__).resolve().parents[1]
CACHE = PROJECT / "artifacts" / "cache" / "final_review"
DOCS = PROJECT / "docs"
RESULTS = PROJECT / "results"
FIGURES = PROJECT / "figures"

SUITES = ["libero_spatial", "libero_object", "libero_goal", "libero_10"]
SUITE_LABELS = {
    "libero_spatial": "LIBERO Spatial",
    "libero_object": "LIBERO Object",
    "libero_goal": "LIBERO Goal",
    "libero_10": "LIBERO Long",
}


def task_results() -> list[dict[str, object]]:
    a2 = json.loads((CACHE / "a2_per_episode_raw.json").read_text(encoding="utf-8"))
    a5 = json.loads((CACHE / "a5_eval_info.json").read_text(encoding="utf-8"))
    a2_grouped: dict[tuple[str, int], list[bool]] = defaultdict(list)
    for episode in a2:
        a2_grouped[(episode["suite"], int(episode["task_id"]))].append(bool(episode["success"]))
    a5_grouped: dict[tuple[str, int], list[bool]] = {}
    for item in a5["per_task"]:
        a5_grouped[(item["task_group"], int(item["task_id"]))] = [
            bool(value) for value in item["metrics"]["successes"]
        ]

    rows: list[dict[str, object]] = []
    for suite in SUITES:
        for task_id in range(10):
            a2_successes = a2_grouped[(suite, task_id)]
            a5_successes = a5_grouped[(suite, task_id)]
            if len(a2_successes) != 10 or len(a5_successes) != 10:
                raise ValueError(f"Expected ten episodes for {suite}/{task_id}.")
            a2_success = sum(a2_successes)
            a5_success = sum(a5_successes)
            rows.append(
                {
                    "suite": suite,
                    "suite_label": SUITE_LABELS[suite],
                    "task_id": task_id,
                    "a2_success": a2_success,
                    "a2_failure": 10 - a2_success,
                    "a2_rate_percent": a2_success * 10,
                    "a5_success": a5_success,
                    "a5_failure": 10 - a5_success,
                    "a5_rate_percent": a5_success * 10,
                    "delta_pp": (a5_success - a2_success) * 10,
                }
            )
    return rows


def write_task_outputs(rows: list[dict[str, object]]) -> None:
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    csv_path = RESULTS / "A2_A5_TASK_SUCCESS_FAILURE_MATRIX.csv"
    fields = list(rows[0])
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    suite_rows: list[dict[str, object]] = []
    for suite in SUITES:
        selected = [row for row in rows if row["suite"] == suite]
        suite_rows.append(
            {
                "suite": suite,
                "suite_label": SUITE_LABELS[suite],
                "a2_success": sum(int(row["a2_success"]) for row in selected),
                "a2_failure": sum(int(row["a2_failure"]) for row in selected),
                "a5_success": sum(int(row["a5_success"]) for row in selected),
                "a5_failure": sum(int(row["a5_failure"]) for row in selected),
            }
        )
    for row in suite_rows:
        row["a2_rate_percent"] = row["a2_success"]
        row["a5_rate_percent"] = row["a5_success"]
        row["delta_pp"] = row["a5_rate_percent"] - row["a2_rate_percent"]
        row["episode_count"] = 100
    overall = {
        "suite": "overall",
        "suite_label": "Overall",
        "a2_success": sum(int(row["a2_success"]) for row in suite_rows),
        "a2_failure": sum(int(row["a2_failure"]) for row in suite_rows),
        "a5_success": sum(int(row["a5_success"]) for row in suite_rows),
        "a5_failure": sum(int(row["a5_failure"]) for row in suite_rows),
    }
    overall["a2_rate_percent"] = overall["a2_success"] / 4
    overall["a5_rate_percent"] = overall["a5_success"] / 4
    overall["delta_pp"] = overall["a5_rate_percent"] - overall["a2_rate_percent"]
    overall["episode_count"] = 400
    suite_rows.append(overall)
    suite_csv = RESULTS / "A2_A5_SUITE_COMPARISON.csv"
    with suite_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(suite_rows[0]))
        writer.writeheader()
        writer.writerows(suite_rows)

    values = [[float(row["delta_pp"]) for row in rows if row["suite"] == suite] for suite in SUITES]
    fig, ax = plt.subplots(figsize=(13, 4.8), constrained_layout=True)
    image = ax.imshow(values, cmap="RdBu_r", vmin=-100, vmax=100, aspect="auto")
    ax.set_xticks(range(10), [f"Task {i}" for i in range(10)])
    ax.set_yticks(range(4), [SUITE_LABELS[suite] for suite in SUITES])
    ax.set_title("A5 minus A2 endpoint success rate (percentage points; 10 episodes per task)")
    for y, suite_values in enumerate(values):
        for x, value in enumerate(suite_values):
            ax.text(x, y, f"{value:+.0f}", ha="center", va="center", fontsize=9)
    fig.colorbar(image, ax=ax, label="A5 − A2 (pp)")
    fig.savefig(FIGURES / "A2_A5_task_level_delta_matrix.png", dpi=180)
    plt.close(fig)

    task_lines = []
    for row in rows:
        task_lines.append(
            "| {suite_label} | {task_id} | {a2_success}/10 | {a2_failure}/10 | {a2_rate_percent:.0f}% | "
            "{a5_success}/10 | {a5_failure}/10 | {a5_rate_percent:.0f}% | {delta_pp:+.0f} |".format(**row)
        )
    suite_lines = []
    for row in suite_rows:
        suite_lines.append(
            "| {suite_label} | {a2_success}/{episode_count} | {a2_rate_percent:.2f}% | {a5_success}/{episode_count} | {a5_rate_percent:.2f}% | {delta_pp:+.2f} |".format(**row)
        )
    changed_up = sum(row["delta_pp"] > 0 for row in rows)
    changed_down = sum(row["delta_pp"] < 0 for row in rows)
    unchanged = 40 - changed_up - changed_down
    (DOCS / "A2_A5_DESCRIPTIVE_COMPARISON.md").write_text(
        "# A2 vs A5：任务级描述性 Endpoint 对照\n\n"
        "## 目的与边界\n\n"
        "本文件复用已完成的 A2 released-anchor 与 A5 final evaluation artifact，汇总 4 个 suite、每 suite 10 个 task、每 task 10 个 episode 的 endpoint success。"
        "它是冻结闭环协议下的单 seed 描述性对照，不是配对统计检验，也不构成因果归因。结果不应表述为“证明改进”或“显著改进”。\n\n"
        "A2 和 A5 均使用同一 LIBERO task list、固定初始化、seed=0、hard reset、原生 success predicate、相对控制、双相机、8D state、7D action、W1 串行调度；"
        "A5 显式冻结 `n_action_steps=1`，A2 released anchor 的原生设置亦为 1。两次运行不能被当作跨 seed 的统计结论，且 artifact 未提供可用于逐 episode 配对检验的相同 init-state 序列证明。\n\n"
        "## Suite-level endpoint 对照\n\n"
        "| Suite | A2 success | A2 rate | A5 success | A5 rate | A5 − A2 (pp) |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: |\n"
        + "\n".join(suite_lines)
        + "\n\n## 40-task success/failure matrix\n\n"
        "A2/A5 success 与 failure 分别是该 task 的 10 个 episode 计数。完整 CSV：`../results/A2_A5_TASK_SUCCESS_FAILURE_MATRIX.csv`。\n\n"
        "| Suite | Task | A2 success | A2 failure | A2 rate | A5 success | A5 failure | A5 rate | Delta (pp) |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n"
        + "\n".join(task_lines)
        + "\n\n## 描述性解读\n\n"
        f"总体 endpoint success 为 A2 66.75%（267/400）与 A5 71.50%（286/400），差值 +4.75 pp。40 个 task 中，{changed_up} 个 task 的 A5 endpoint rate 更高、{changed_down} 个更低、{unchanged} 个相同。"
        "这只是同一冻结基准条件下两个 endpoint 的观测差异；它不隔离初始化、优化或其他潜在因素，也没有估计多 seed 不确定性。\n\n"
        "![Task-level delta matrix](../figures/A2_A5_task_level_delta_matrix.png)\n",
        encoding="utf-8",
    )


METRIC = re.compile(
    r"step:(?P<step>[\d.]+)(?P<unit>K?)\s+.*?loss:(?P<loss>[-+\deE.]+)\s+"
    r"grdn:(?P<grad>[-+\deE.]+)\s+lr:(?P<lr>[-+\deE.]+).*?"
    r"smp/s:(?P<throughput>[-+\deE.]+)\s+mem_gb:(?P<memory>[-+\deE.]+)"
)


def training_metrics() -> list[dict[str, float]]:
    metrics: dict[float, dict[str, float]] = {}
    for line in (CACHE / "a4_100k_final.log").read_text(encoding="utf-8", errors="replace").splitlines():
        match = METRIC.search(line)
        if not match:
            continue
        values = match.groupdict()
        step = float(values["step"]) * (1000 if values["unit"] == "K" else 1)
        metrics[step] = {
            "step": step,
            "loss": float(values["loss"]),
            "grad_norm": float(values["grad"]),
            "learning_rate": float(values["lr"]),
            "throughput_samples_per_s": float(values["throughput"]),
            "memory_gb": float(values["memory"]),
        }
    return [metrics[step] for step in sorted(metrics)]


def write_training_outputs(metrics: list[dict[str, float]]) -> None:
    if not metrics:
        raise ValueError("No A4 metrics matched the expected log format.")
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    with (RESULTS / "A4_TRAINING_DYNAMICS.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(metrics[0]))
        writer.writeheader()
        writer.writerows(metrics)

    x = [item["step"] for item in metrics]
    panels = [
        ("loss", "Training loss", "#1f77b4"),
        ("learning_rate", "Learning rate", "#ff7f0e"),
        ("grad_norm", "Gradient norm", "#2ca02c"),
        ("throughput_samples_per_s", "Throughput (samples/s)", "#9467bd"),
        ("memory_gb", "GPU memory (GB)", "#8c564b"),
    ]
    fig, axes = plt.subplots(3, 2, figsize=(12, 10), constrained_layout=True)
    for ax, (key, title, color) in zip(axes.flat, panels):
        ax.plot(x, [item[key] for item in metrics], color=color, linewidth=1.25)
        ax.set_title(title)
        ax.set_xlabel("Optimizer step")
        ax.grid(alpha=0.25)
    axes.flat[-1].axis("off")
    fig.suptitle("A4 100K training dynamics (existing log only)", fontsize=14)
    fig.savefig(FIGURES / "A4_training_dynamics.png", dpi=180)
    plt.close(fig)

    def stats(key: str) -> tuple[float, float, float]:
        values = [item[key] for item in metrics]
        return min(values), sum(values) / len(values), max(values)

    loss_min, loss_mean, loss_max = stats("loss")
    grad_min, grad_mean, grad_max = stats("grad_norm")
    rate_min, _, rate_max = stats("learning_rate")
    throughput_min, throughput_mean, throughput_max = stats("throughput_samples_per_s")
    memory_min, memory_mean, memory_max = stats("memory_gb")
    (DOCS / "A4_TRAINING_DYNAMICS.md").write_text(
        "# A4 100K Training Dynamics\n\n"
        "## 来源与边界\n\n"
        "本分析只解析已完成 A4 训练的既有日志 `logs/A4_100k_final.log`，未启动训练、未加载或评估任何 checkpoint。"
        f"解析到 {len(metrics)} 个去重后的周期性记录，覆盖 step {int(x[0])} 至 {int(x[-1])}。\n\n"
        "## 汇总\n\n"
        "| Metric | Min | Mean | Max |\n| --- | ---: | ---: | ---: |\n"
        f"| Training loss | {loss_min:.3f} | {loss_mean:.3f} | {loss_max:.3f} |\n"
        f"| Learning rate | {rate_min:.2e} | — | {rate_max:.2e} |\n"
        f"| Gradient norm | {grad_min:.3f} | {grad_mean:.3f} | {grad_max:.3f} |\n"
        f"| Throughput (samples/s) | {throughput_min:.0f} | {throughput_mean:.1f} | {throughput_max:.0f} |\n"
        f"| GPU memory (GB) | {memory_min:.2f} | {memory_mean:.2f} | {memory_max:.2f} |\n\n"
        "日志中存在 loss、learning rate、gradient norm、throughput 和 memory 字段。曲线用于呈现已记录训练过程的数值稳定性；"
        "它们不替代独立验证指标，也不支持泛化能力结论。\n\n"
        "![A4 training dynamics](../figures/A4_training_dynamics.png)\n",
        encoding="utf-8",
    )


def main() -> None:
    rows = task_results()
    write_task_outputs(rows)
    write_training_outputs(training_metrics())


if __name__ == "__main__":
    main()
