from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    # 总用户数
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    # 流失率
    if any(word in normalized for word in ["流失率", "总体流失", "整体流失"]):
        return f"总体流失率为{float(metrics['流失率']):.1%}，共{int(metrics['流失人数']):,}名用户在{int(metrics['用户数']):,}名用户中流失。"

    # 偏好品类
    if any(word in normalized for word in ["偏好品类", "哪个品类", "品类最多", "最多用户"]):
        top_cat = category_df.loc[category_df["用户数"].idxmax(), "PreferedOrderCat"]
        top_count = int(category_df.loc[category_df["用户数"].idxmax(), "用户数"])
        return f"偏好品类中用户最多的是{top_cat}，有{top_count:,}名用户。"

    # 生命周期风险
    if any(word in normalized for word in ["生命周期", "风险最高", "哪个阶段", "阶段风险"]):
        max_idx = segment_df["流失率"].idxmax()
        max_row = segment_df.loc[max_idx]
        return f"生命周期中风险最高的是{max_row['TenureGroup']}阶段，流失率达{max_row['流失率']:.1%}（{int(max_row['用户数'])}人中{int(max_row['流失人数'])}人流失）。"

    # 订单
    if any(word in normalized for word in ["平均订单", "订单数", "订单"]):
        return f"平均订单数为{float(metrics['平均订单数']):.2f}单，订单数中位数为{int(metrics['订单数中位数'])}单。"

    # 不支持的问题
    return "抱歉，当前问答系统仅支持以下类型的问题：总用户数、总体流失率、偏好品类、生命周期风险和平均订单数。"
