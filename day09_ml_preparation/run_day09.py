# -*- coding: utf-8 -*-
"""Day 09: 第一次接触机器学习 - 完整运行脚本"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data/ecommerce_customer_cleaned.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
RANDOM_STATE = 42
TEST_SIZE = 0.20
pd.set_option("display.max_columns", 80)

# TODO 9-0
STUDENT_NAME = "陈子昂"
STUDENT_ID = "24012474"
CLASS_NAME = "2026实训2班"
assert STUDENT_NAME and STUDENT_ID and CLASS_NAME
print(f"学生：{STUDENT_NAME} / {STUDENT_ID} / {CLASS_NAME}")

# === 任务1 ===
print("\n=== 任务1：6人小实验 ===")
toy = pd.DataFrame({
    "用户": list("ABCDEF"),
    "Tenure": [1, 24, 3, 18, 2, 30],
    "Complain": [1, 0, 0, 1, 1, 0],
    "Churn": [1, 0, 1, 0, 1, 0],
})
toy["人工规则预测"] = ((toy["Tenure"] <= 3) & (toy["Complain"] == 1)).astype(int)
toy["是否判断正确"] = toy["人工规则预测"] == toy["Churn"]
print(toy)
correct = int(toy["是否判断正确"].sum())
found = int(((toy["人工规则预测"] == 1) & (toy["Churn"] == 1)).sum())
print(f"判断正确：{correct}/6, 流失找到：{found}/3")
print("C用户Tenure=3但Complain=0，规则漏掉。机器学习可从数据中自动学习模式。")

# === 任务2 ===
print("\n=== 任务2：读取真实数据 ===")
df = pd.read_csv(DATA_PATH)
print(f"形状：{df.shape}，流失率：{df['Churn'].mean():.2%}")
assert df.shape == (5630, 22)
assert df["CustomerID"].is_unique
assert set(df["Churn"].unique()) == {0, 1}
assert int(df.isna().sum().sum()) == 0
print("验证通过")

# === 任务3 ===
print("\n=== 任务3：X和y ===")
TARGET = "Churn"
ID_COL = "CustomerID"
assert ID_COL == "CustomerID"
X = df.drop(columns=[TARGET, ID_COL]).copy()
y = df[TARGET].astype(int).copy()
print(f"X: {X.shape}, y: {y.shape} (CustomerID和Churn已排除)")

# === 任务4 ===
print("\n=== 任务4：特征方案 ===")
cat_features = X.select_dtypes(include="object").columns.tolist()
num_features = X.select_dtypes(exclude="object").columns.tolist()
derived = ["TenureGroup", "IsMobileLogin"]

rows = []
for col in df.columns:
    if col == ID_COL:
        role, action, reason = "identifier", "drop", "仅用于追踪"
    elif col == TARGET:
        role, action, reason = "target", "separate", "希望预测的答案"
    elif col in derived:
        role, action, reason = "derived_feature", "candidate", "由已有字段转换"
    elif col in cat_features:
        role, action, reason = "categorical_feature", "one_hot", "文字类别需转0/1列"
    else:
        role, action, reason = "numeric_feature", "numeric_pipeline", "数值处理"
    rows.append({"feature": col, "role": role, "dtype": str(df[col].dtype), "action": action, "reason": reason})

feature_schema = pd.DataFrame(rows)
feature_schema.to_csv(OUTPUT_DIR / "feature_schema.csv", index=False, encoding="utf-8-sig")
print(feature_schema[["feature", "role", "action"]].to_string(index=False))

# === 任务5 ===
print("\n=== 任务5：分层划分 ===")
STRATIFY_TARGET = y
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=STRATIFY_TARGET)

split_summary = pd.DataFrame([
    {"split": "train", "rows": len(X_train), "churn_rate": y_train.mean()},
    {"split": "test", "rows": len(X_test), "churn_rate": y_test.mean()},
])
split_summary.to_csv(OUTPUT_DIR / "split_summary.csv", index=False, encoding="utf-8-sig")
print(split_summary)
assert abs(y_train.mean() - y_test.mean()) < 0.01
print("stratify=y：训练测试流失比例接近")

# === 任务6 ===
print("\n=== 任务6：预处理 ===")
num_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
cat_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])
preprocessor = ColumnTransformer([
    ("num", num_pipe, num_features),
    ("cat", cat_pipe, cat_features),
])

X_tr = preprocessor.fit_transform(X_train)
X_te = preprocessor.transform(X_test)
names = preprocessor.get_feature_names_out()

assert X_tr.shape[1] == X_te.shape[1] == 36
assert np.isfinite(X_tr).all() and np.isfinite(X_te).all()
print(f"训练矩阵：{X_tr.shape}，测试矩阵：{X_te.shape}，列数：{X_tr.shape[1]}，无缺失/无穷值")
preview = pd.DataFrame(X_tr[:20], columns=names)
preview.to_csv(OUTPUT_DIR / "model_matrix_preview.csv", index=False, encoding="utf-8-sig")
print(preview.head())

# === 任务7 ===
print("\n=== 任务7：最低参照线 ===")
baseline = DummyClassifier(strategy="prior", random_state=RANDOM_STATE)
baseline.fit(X_tr, y_train)
y_pred = baseline.predict(X_te)

bm = pd.DataFrame({
    "metric": ["accuracy", "churn_recall", "predicted_churn_count"],
    "value": [accuracy_score(y_test, y_pred), recall_score(y_test, y_pred, pos_label=1, zero_division=0), int(y_pred.sum())],
})
bm.to_csv(OUTPUT_DIR / "baseline_metrics.csv", index=False, encoding="utf-8-sig")
print(bm)
print(f"真实流失：{int(y_test.sum())}，预测流失：{int(y_pred.sum())}")

# === 任务8 ===
print("\n=== 任务8：复盘 ===")
reflection = (
    "特征是判断时可查看的信息（如使用月数、投诉情况），"
    "标签是希望预测的答案（Churn）。"
    "训练集让模型学习规律，测试集检验未见用户的效果。"
    "最低参照线永远预测人数最多的未流失类，"
    "准确率约83%但流失召回率为0，完全无法识别任何流失用户，"
    "因此不能用于寻找流失用户。正式模型必须超过这一基线才有价值。"
)
assert 100 <= len(reflection) <= 200
print(f"复盘 ({len(reflection)}字)")
print(reflection)

# === 提交检查 ===
print("\n=== 提交检查 ===")
required = {"feature_schema.csv", "split_summary.csv", "model_matrix_preview.csv", "baseline_metrics.csv"}
actual = {p.name for p in OUTPUT_DIR.glob("*.csv")}
print("成果文件：", sorted(actual))
assert required.issubset(actual)
print("Day 09 完成！")
