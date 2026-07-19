"""
离线问答服务 - 基于 CSV 数据的规则问答
所有数值从 CSV 读取，不在回答字符串中写死。
"""
import re
from services.data_service import get_overall_metrics, get_segment_analysis, get_cross_analysis, get_category_data


def get_qa_response(question):
    """根据问题类型返回对应的数据回答"""
    q = question.strip().lower()

    # 1. 总体规模
    if any(k in q for k in ["多少用户", "用户数", "总用户", "系统中有多少", "总共有多少"]):
        m = get_overall_metrics()
        return (
            f"系统中总共有 {m['用户数']} 名用户。"
        )

    # 2. 流失情况
    if any(k in q for k in ["流失率", "总体流失", "流失用户", "流失人数", "多少流失"]):
        m = get_overall_metrics()
        return (
            f"总体流失率为 {m['总体流失率']}，流失人数为 {m['流失人数']} 人。"
        )

    # 3. 偏好品类
    if any(k in q for k in ["品类", "最多", "最受欢迎", "哪个品类", "偏好", "prefer"]):
        cats = get_category_data()
        if cats:
            top_cat = max(cats, key=cats.get)
            return f"偏好品类为 '{top_cat}' 的用户最多，共 {cats[top_cat]} 人。"
        return "暂无品类数据。"

    # 4. 生命周期 / 阶段
    if any(k in q for k in ["生命周期", "阶段", "风险最高", "哪个阶段", "tenure", "最长"]):
        seg = get_segment_analysis()
        if not seg.empty:
            highest_risk = seg.loc[seg["流失率"].idxmax()]
            lowest_risk = seg.loc[seg["流失率"].idxmin()]
            return (
                f"风险最高的阶段是 '{highest_risk['TenureGroup']}'，流失率为 {highest_risk['流失率'] * 100:.1f}%；"
                f"最稳定的阶段是 '{lowest_risk['TenureGroup']}'，流失率为 {lowest_risk['流失率'] * 100:.1f}%。"
            )
        return "暂无生命周期数据。"

    # 5. 订单情况
    if any(k in q for k in ["订单", "平均订单", "订单数", "order"]):
        m = get_overall_metrics()
        return (
            f"平均订单数为 {m['平均订单数']}，订单数中位数为 {m['订单数中位数']}。"
        )

    # 6. 支付方式
    if any(k in q for k in ["支付", "payment", "付款方式", "支付方式"]):
        cross = get_cross_analysis()
        if not cross.empty:
            top_payment = cross.groupby("PreferredPaymentMode", sort=False)["用户数"].sum().idxmax()
            return f"最常用的支付方式是 '{top_payment}'。"
        return "暂无支付方式数据。"

    # 7. 流失率最高的组合
    if any(k in q for k in ["最高流失", "流失最高", "最高风险", "最大风险"]):
        cross = get_cross_analysis()
        if not cross.empty and cross["流失率"].max() > 0:
            worst = cross.loc[cross["流失率"].idxmax()]
            return (
                f"流失率最高的组合是：生命周期阶段 '{worst['TenureGroup']}' + "
                f"支付方式 '{worst['PreferredPaymentMode']}'，"
                f"流失率为 {worst['流失率'] * 100:.1f}%，样本数 {int(worst['用户数'])}。"
            )
        return "暂无交叉分析数据。"

    # 8. 不支持的问题
    return "抱歉，我不支持回答这个问题。您可以问我关于用户规模、流失率、偏好品类、生命周期阶段、订单情况、支付方式等问题。"
