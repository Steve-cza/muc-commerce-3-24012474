from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    # TODO 2-1：在已有两张指标卡基础上，增加"总体流失率"和"平均订单数"。
    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{float(metric_map['流失率']):.1%}", "note": "%"},
        {"label": "平均订单数", "value": f"{float(metric_map['平均订单数']):.2f}", "note": "单"},
    ]

    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()
    # TODO 3-1：选择具体品类后筛选table_df。
    if selected_category != "全部":
        mask = category_df["PreferedOrderCat"] == selected_category
        table_df = category_df[mask].copy()

    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]
    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")

    # TODO 2-2：找出流失率最高的生命周期阶段，并生成一句数据观察。
    max_idx = segment_df["流失率"].idxmax()
    max_row = segment_df.loc[max_idx]
    insight = f"【{max_row['TenureGroup']}】阶段流失率最高，达{max_row['流失率']:.1%}（{int(max_row['用户数'])}人中{int(max_row['流失人数'])}人流失），需重点关注该阶段用户的留存策略。"

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }
