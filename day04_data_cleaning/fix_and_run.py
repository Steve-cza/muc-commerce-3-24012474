"""修复 Day 04 Notebook 的 TODO 并生成缺失产出"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

NB_PATH = Path("notebooks/day04_pm_user_cleaning_project.ipynb")
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 修复 Notebook TODOs
with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 定义函数替换文本
func_replacements = {
    # Cell 8: build_quality_report
    'def build_quality_report(data):\n    """返回字段级数据质量报告。"""\n    # TODO：返回一个 DataFrame，至少包含：\n    # 数据类型、缺失数量、缺失比例(%)、唯一值数量\n    pass': '''def build_quality_report(data):
    """返回字段级数据质量报告。"""
    report = pd.DataFrame({
        "数据类型": data.dtypes,
        "缺失数量": data.isna().sum(),
        "缺失比例(%)": (data.isna().sum() / len(data) * 100).round(2),
        "唯一值数量": data.nunique()
    })
    report.index.name = "字段"
    return report''',

    # Uncomment quality_before
    '# quality_before = build_quality_report(raw_df)\n# display(quality_before)': 'quality_before = build_quality_report(raw_df)\ndisplay(quality_before)',

    # Cell 10: Initial audit
    '# print("完全重复行数：", ...)': 'print("完全重复行数：", raw_df.duplicated().sum())',
    '# print("CustomerID 重复数量：", ...)': 'print("CustomerID 重复数量：", raw_df["CustomerID"].duplicated().sum())',
    '# print(raw_df["Churn"].value_counts())': 'print(raw_df["Churn"].value_counts())',
    '# print("流失率：", ...)': 'print("流失率：", raw_df["Churn"].mean())',

    '# for col in ["PreferredLoginDevice", "PreferredPaymentMode", "PreferedOrderCat"]:\n#     print(f"\\n{col}")\n#     print(raw_df[col].value_counts())': '''for col in ["PreferredLoginDevice", "PreferredPaymentMode", "PreferedOrderCat"]:
    print(f"\\n{col}")
    print(raw_df[col].value_counts())''',

    # Cell 14: clean_ecommerce_data
}

# For the clean_ecommerce_data function - it's a long replacement
clean_func = '''def clean_ecommerce_data(data):
    """
    清洗电商用户行为数据。
    """
    cleaned = data.copy()
    logs = []

    # 删除完全重复行
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    dup_count = before - len(cleaned)
    logs.append({"操作": "删除完全重复行", "影响行数": dup_count})

    # 中位数填补数值缺失
    for col in NUMERIC_MISSING_COLS:
        if col in cleaned.columns:
            miss_before = cleaned[col].isna().sum()
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            if miss_before > 0:
                logs.append({"操作": f"中位数填补 {col}", "影响行数": miss_before})

    # 类别标准化
    for col, mapping in CATEGORY_MAPPINGS.items():
        if col in cleaned.columns:
            affected = cleaned[col].isin(mapping.keys()).sum()
            cleaned[col] = cleaned[col].replace(mapping)
            logs.append({"操作": f"类别标准化 {col}", "影响行数": affected})

    # Churn 和 Complain 转整数
    for col in ["Churn", "Complain"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(int)

    cleaning_log = pd.DataFrame(logs)
    return cleaned, cleaning_log'''

func_replacements['def clean_ecommerce_data(data):\n    """\n    清洗电商用户行为数据。\n\n    参数：\n        data: 原始用户行为 DataFrame\n\n    返回：\n        cleaned_df: 清洗后的 DataFrame\n        cleaning_log: 处理日志 DataFrame\n    """\n    # TODO：复制数据，避免覆盖原始数据\n    # TODO：创建日志列表 logs\n    # TODO：删除完全重复行，并记录日志\n    # TODO：对 NUMERIC_MISSING_COLS 使用中位数填补，并记录每列影响数量\n    # TODO：对 CATEGORY_MAPPINGS 完成类别标准化，并记录每条映射影响数量\n    # TODO：将 Churn 和 Complain 转为整数类型\n    # TODO：返回 cleaned_df 与 cleaning_log\n    pass'] = clean_func

# Cell 16: Execute cleaning
func_replacements['# cleaned_df, cleaning_log = clean_ecommerce_data(raw_df)\n#\n# display(cleaning_log)\n# cleaned_df.head()'] = 'cleaned_df, cleaning_log = clean_ecommerce_data(raw_df)\n\ndisplay(cleaning_log)\ncleaned_df.head()'

# Cell 18: outlier report
outlier_code = '''# 构建 TenureGroup
tenure_bins = [0, 6, 12, 24, float("inf")]
tenure_labels = ["0-6个月", "7-12个月", "13-24个月", "24个月以上"]
cleaned_df["TenureGroup"] = pd.cut(cleaned_df["Tenure"], bins=tenure_bins, labels=tenure_labels, right=True)

# 新建 IsMobileLogin
cleaned_df["IsMobileLogin"] = (cleaned_df["PreferredLoginDevice"] == "Mobile Phone").astype(int)

# 异常值检测
numeric_cols = ["Tenure", "WarehouseToHome", "HourSpendOnApp", "NumberOfDeviceRegistered",
                "NumberOfAddress", "OrderCount", "DaySinceLastOrder", "CashbackAmount"]
outlier_records = []
for col in numeric_cols:
    if col in cleaned_df.columns:
        q1 = cleaned_df[col].quantile(0.25)
        q3 = cleaned_df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = ((cleaned_df[col] < lower) | (cleaned_df[col] > upper)).sum()
        outlier_records.append({"字段": col, "Q1": round(q1,2), "Q3": round(q3,2), "下限": round(lower,2), "上限": round(upper,2), "候选异常值": outliers})

outlier_report = pd.DataFrame(outlier_records)
display(outlier_report)'''

func_replacements['# TODO：构建 tenure_bins、tenure_labels，并用 pd.cut 新建 TenureGroup\n# TODO：新建 IsMobileLogin，移动端为 1，其他设备为 0\n# TODO：生成 outlier_report（每行对应一个待检查字段）'] = outlier_code

# Cell 20: business rules
biz_rules = '''business_rule_report = pd.DataFrame({
    "规则": ["Tenure 不能为负数", "HourSpendOnApp 应在 0-24 之间", "NumberOfAddress 不应异常高"],
    "不合规记录数": [
        int((cleaned_df["Tenure"] < 0).sum()),
        int(((cleaned_df["HourSpendOnApp"] < 0) | (cleaned_df["HourSpendOnApp"] > 24)).sum()),
        int((cleaned_df["NumberOfAddress"] > 20).sum())
    ]
})
display(business_rule_report)'''

func_replacements['# business_rule_report = pd.DataFrame({\n#     "规则": [...],\n#     "不合规记录数": [...]\n# })\n# display(business_rule_report)\n#\n# 处理结论：'] = biz_rules + '\n# 处理结论：以上规则仅用于教学检查，不强行修改数据。'

# Cell 22: Final validation and export
final_code = '''quality_after = build_quality_report(cleaned_df)

assert cleaned_df[NUMERIC_MISSING_COLS].isna().sum().sum() == 0
assert "Phone" not in cleaned_df["PreferredLoginDevice"].unique()
assert "COD" not in cleaned_df["PreferredPaymentMode"].unique()
assert "CC" not in cleaned_df["PreferredPaymentMode"].unique()
assert {"TenureGroup", "IsMobileLogin"}.issubset(cleaned_df.columns)

quality_before.to_csv(OUTPUT_DIR / "data_quality_before.csv", index=True, encoding="utf-8-sig")
quality_after.to_csv(OUTPUT_DIR / "data_quality_after.csv", index=True, encoding="utf-8-sig")
cleaning_log.to_csv(OUTPUT_DIR / "cleaning_log.csv", index=False, encoding="utf-8-sig")
cleaned_df.to_csv(OUTPUT_DIR / "ecommerce_customer_cleaned.csv", index=False, encoding="utf-8-sig")
outlier_report.to_csv(OUTPUT_DIR / "outlier_report.csv", index=False, encoding="utf-8-sig")
business_rule_report.to_csv(OUTPUT_DIR / "business_rule_report.csv", index=False, encoding="utf-8-sig")

print("所有文件已导出 ✅")'''

func_replacements['# TODO：完成最终验收\n# quality_after = build_quality_report(cleaned_df)\n#\n# assert cleaned_df[NUMERIC_MISSING_COLS].isna().sum().sum() == 0\n# assert "Phone" not in cleaned_df["PreferredLoginDevice"].unique()\n# assert "COD" not in cleaned_df["PreferredPaymentMode"].unique()\n# assert "CC" not in cleaned_df["PreferredPaymentMode"].unique()\n# assert {"TenureGroup", "IsMobileLogin"}.issubset(cleaned_df.columns)\n#\n# TODO：导出下列文件，使用 utf-8-sig 编码：\n# quality_before.to_csv(OUTPUT_DIR / "data_quality_before.csv", index=True, encoding="utf-8-sig")\n# quality_after.to_csv(OUTPUT_DIR / "data_quality_after.csv", inde'] = final_code

# Apply fixes
fix_count = 0
for cell in nb['cells']:
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else str(cell['source'])
    new_src = src
    for old, new in func_replacements.items():
        if old in new_src:
            new_src = new_src.replace(old, new)
            fix_count += 1
    if new_src != src:
        cell['source'] = [new_src]

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Fixed {fix_count} TODOs in Day 04 notebook ✅")

# 2. 直接运行清洗流程生成产出
RAW_DATA = ROOT.parent / "data" / "E Commerce Dataset.xlsx"
raw_df = pd.read_excel(RAW_DATA, sheet_name="E Comm")

NUMERIC_MISSING_COLS = ["Tenure", "WarehouseToHome", "HourSpendOnApp", "NumberOfDeviceRegistered",
                        "SatisfactionScore", "NumberOfAddress", "OrderCount", "DaySinceLastOrder"]
CATEGORY_MAPPINGS = {
    "PreferredLoginDevice": {"Phone": "Mobile Phone"},
    "PreferredPaymentMode": {"COD": "Cash on Delivery", "CC": "Credit Card"},
}

# 清洗前质量报告
def build_quality_report(data):
    report = pd.DataFrame({
        "数据类型": data.dtypes,
        "缺失数量": data.isna().sum(),
        "缺失比例(%)": (data.isna().sum() / len(data) * 100).round(2),
        "唯一值数量": data.nunique()
    })
    report.index.name = "字段"
    return report

quality_before = build_quality_report(raw_df)

# 清洗函数
def clean_ecommerce_data(data):
    cleaned = data.copy()
    logs = []
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    logs.append({"操作": "删除完全重复行", "影响行数": before - len(cleaned)})
    for col in NUMERIC_MISSING_COLS:
        if col in cleaned.columns:
            miss = cleaned[col].isna().sum()
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            if miss > 0:
                logs.append({"操作": f"中位数填补 {col}", "影响行数": miss})
    for col, mapping in CATEGORY_MAPPINGS.items():
        if col in cleaned.columns:
            affected = cleaned[col].isin(mapping.keys()).sum()
            cleaned[col] = cleaned[col].replace(mapping)
            logs.append({"操作": f"类别标准化 {col}", "影响行数": affected})
    for col in ["Churn", "Complain"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(int)
    return cleaned, pd.DataFrame(logs)

cleaned_df, cleaning_log = clean_ecommerce_data(raw_df)

# 清洗后质量
quality_after = build_quality_report(cleaned_df)

# 异常值报告
numeric_cols = ["Tenure", "WarehouseToHome", "HourSpendOnApp", "NumberOfDeviceRegistered",
                "NumberOfAddress", "OrderCount", "DaySinceLastOrder", "CashbackAmount"]
outlier_records = []
for col in numeric_cols:
    if col in cleaned_df.columns:
        q1 = cleaned_df[col].quantile(0.25)
        q3 = cleaned_df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_records.append({
            "字段": col, "Q1": round(q1, 2), "Q3": round(q3, 2),
            "下限": round(lower, 2), "上限": round(upper, 2),
            "候选异常值": int(((cleaned_df[col] < lower) | (cleaned_df[col] > upper)).sum())
        })
outlier_report = pd.DataFrame(outlier_records)

# 业务规则
business_rule_report = pd.DataFrame({
    "规则": ["Tenure 不能为负数", "HourSpendOnApp 应在 0-24", "NumberOfAddress 不应异常高"],
    "不合规记录数": [
        int((cleaned_df["Tenure"] < 0).sum()),
        int(((cleaned_df["HourSpendOnApp"] < 0) | (cleaned_df["HourSpendOnApp"] > 24)).sum()),
        int((cleaned_df["NumberOfAddress"] > 20).sum())
    ]
})

# 导出
quality_before.to_csv(OUTPUT_DIR / "data_quality_before.csv", index=True, encoding="utf-8-sig")
quality_after.to_csv(OUTPUT_DIR / "data_quality_after.csv", index=True, encoding="utf-8-sig")
cleaning_log.to_csv(OUTPUT_DIR / "cleaning_log.csv", index=False, encoding="utf-8-sig")
cleaned_df.to_csv(OUTPUT_DIR / "ecommerce_customer_cleaned.csv", index=False, encoding="utf-8-sig")
outlier_report.to_csv(OUTPUT_DIR / "outlier_report.csv", index=False, encoding="utf-8-sig")
business_rule_report.to_csv(OUTPUT_DIR / "business_rule_report.csv", index=False, encoding="utf-8-sig")

print(f"\nDay 04 产出文件:")
for f in sorted(OUTPUT_DIR.glob("*.csv")):
    print(f"  {f.name}: {f.stat().st_size:>8} bytes")
print("Day 04 全部完成 ✅")
