# -*- coding: utf-8 -*-
"""Day 10: 三个分类模型的训练、比较与应用"""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42
TEST_SIZE = 0.20
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data/ecommerce_customer_cleaned.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# TODO 10-0
STUDENT_NAME = "陈子昂"
STUDENT_ID = "24012474"
CLASS_NAME = "2026实训2班"
assert STUDENT_NAME and STUDENT_ID and CLASS_NAME
print(f"学生：{STUDENT_NAME} / {STUDENT_ID} / {CLASS_NAME}")

# === 任务1：口径恢复 ===
print("\n=== 任务1：数据口径 ===")
df = pd.read_csv(DATA_PATH)
print(f"形状：{df.shape}，流失率：{df['Churn'].mean():.2%}")
assert df.shape == (5630, 22)

TARGET = "Churn"
ID_COL = "CustomerID"  # TODO 10-1
assert ID_COL == "CustomerID"
X = df.drop(columns=[TARGET, ID_COL]).copy()
y = df[TARGET].astype(int).copy()
customer_ids = df[ID_COL].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)
test_customer_ids = customer_ids.loc[X_test.index]
print(f"训练集：{X_train.shape}，流失率={y_train.mean():.2%}")
print(f"测试集：{X_test.shape}，流失率={y_test.mean():.2%}")
assert len(X_train) == 4504 and len(X_test) == 1126
assert abs(y_train.mean() - y_test.mean()) < 0.001

# === 任务2-4：构建并训练三个模型 ===
print("\n=== 任务2-4：训练三个模型 ===")
cat_features = X.select_dtypes(include=["object", "string"]).columns.tolist()
num_features = X.columns.difference(cat_features).tolist()

def build_preprocessor():
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("num", num_pipe, num_features),
        ("cat", cat_pipe, cat_features),
    ])

def build_pipeline(model):
    return Pipeline([("preprocessor", build_preprocessor()), ("model", model)])

fitted_models = {}
predictions = {}
probabilities = {}

# 逻辑回归
pipe_lr = build_pipeline(LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE))
pipe_lr.fit(X_train, y_train)
fitted_models["logistic_regression"] = pipe_lr
predictions["logistic_regression"] = pipe_lr.predict(X_test)
probabilities["logistic_regression"] = pipe_lr.predict_proba(X_test)[:, 1]
print(f"逻辑回归：预测流失 {int(predictions['logistic_regression'].sum())} 人")

# 决策树
pipe_dt = build_pipeline(DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, class_weight="balanced", random_state=RANDOM_STATE))
pipe_dt.fit(X_train, y_train)
fitted_models["decision_tree"] = pipe_dt
predictions["decision_tree"] = pipe_dt.predict(X_test)
probabilities["decision_tree"] = pipe_dt.predict_proba(X_test)[:, 1]
print(f"决策树：预测流失 {int(predictions['decision_tree'].sum())} 人")

# 随机森林
pipe_rf = build_pipeline(RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=10, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1))
pipe_rf.fit(X_train, y_train)
fitted_models["random_forest"] = pipe_rf
predictions["random_forest"] = pipe_rf.predict(X_test)
probabilities["random_forest"] = pipe_rf.predict_proba(X_test)[:, 1]
print(f"随机森林：预测流失 {int(predictions['random_forest'].sum())} 人")

# === 任务5：模型比较 ===
print("\n=== 任务5：模型比较 ===")
baseline_pipe = build_pipeline(DummyClassifier(strategy="prior", random_state=RANDOM_STATE))
baseline_pipe.fit(X_train, y_train)
fitted_models["baseline"] = baseline_pipe
predictions["baseline"] = baseline_pipe.predict(X_test)
probabilities["baseline"] = baseline_pipe.predict_proba(X_test)[:, 1]

def metric_row(name):
    pred = predictions[name]
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    return {
        "model": name,
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "churn_recall": recall_score(y_test, pred, zero_division=0),
        "predicted_churn_count": int(pred.sum()),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }

order = ["baseline", "logistic_regression", "decision_tree", "random_forest"]
comparison = pd.DataFrame([metric_row(n) for n in order])
comparison.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)
print(comparison.to_string(index=False))
print()

# Confusion matrix summary
cm = comparison[["model", "tn", "fp", "fn", "tp"]].copy()
cm["total"] = cm[["tn", "fp", "fn", "tp"]].sum(axis=1)
cm.to_csv(OUTPUT_DIR / "confusion_matrix_summary.csv", index=False)
assert (cm["total"] == len(y_test)).all()
print(cm.to_string(index=False))

# === 任务6：选择最终模型 ===
print("\n=== 任务6：选择模型 ===")
# 随机森林综合表现最好：准确率>最低参照线，流失召回率最高，FN最低
SELECTED_MODEL_NAME = "random_forest"  # TODO 10-2
allowed = {"logistic_regression", "decision_tree", "random_forest"}
assert SELECTED_MODEL_NAME in allowed

selected_pipeline = fitted_models[SELECTED_MODEL_NAME]
selected_prediction = predictions[SELECTED_MODEL_NAME]
selected_probability = probabilities[SELECTED_MODEL_NAME]
print(f"最终模型：{SELECTED_MODEL_NAME}")

# 选择说明
selection_note = (
    "选择随机森林作为最终模型。"
    "虽然逻辑回归和决策树也有一定效果，但随机森林在流失召回率上表现最好，"
    "能识别出更多真正的流失用户（FN最低）。"
    "同时其准确率也高于最低参照线。"
    "随机森林通过100棵树投票，比单棵决策树更稳定，不易过拟合。"
)  # TODO 10-3
assert 80 <= len(selection_note) <= 180
(OUTPUT_DIR / "model_selection_note.txt").write_text(selection_note, encoding="utf-8")
print(f"选择说明 ({len(selection_note)}字)：{selection_note}")

# === 任务7：输出预测 ===
print("\n=== 任务7：输出预测 ===")
customer_pred = pd.DataFrame({
    "CustomerID": test_customer_ids.to_numpy(),
    "actual_churn": y_test.to_numpy(),
    "predicted_churn": selected_prediction.astype(int),
    "churn_probability": selected_probability,
})
customer_pred["prediction_correct"] = (customer_pred["actual_churn"] == customer_pred["predicted_churn"])
customer_pred.to_csv(OUTPUT_DIR / "customer_churn_predictions.csv", index=False)
assert len(customer_pred) == 1126
assert customer_pred["CustomerID"].is_unique
print(f"客户预测表：{len(customer_pred)} 行，全部唯一")
print(customer_pred.head())

# 高风险名单
high_risk = (customer_pred.query("predicted_churn == 1")
    .sort_values("churn_probability", ascending=False)
    .reset_index(drop=True))
high_risk.to_csv(OUTPUT_DIR / "high_risk_customers.csv", index=False)
print(f"高风险客户：{len(high_risk)} 人")
print(high_risk.head(10))

# 特征重要性
preprocessor = selected_pipeline.named_steps["preprocessor"]
model = selected_pipeline.named_steps["model"]
feature_names = preprocessor.get_feature_names_out()
if hasattr(model, "feature_importances_"):
    imp_vals = model.feature_importances_
elif hasattr(model, "coef_"):
    imp_vals = np.abs(model.coef_[0])
else:
    imp_vals = np.zeros(len(feature_names))
fi = pd.DataFrame({"feature": feature_names, "importance": imp_vals}).sort_values("importance", ascending=False).reset_index(drop=True)
fi.to_csv(OUTPUT_DIR / "feature_importance.csv", index=False)
print("\nTop 10 特征重要性：")
print(fi.head(10))

# === 任务8：保存模型 ===
print("\n=== 任务8：保存模型 ===")
MODEL_PATH = OUTPUT_DIR / "selected_model.joblib"
joblib.dump(selected_pipeline, MODEL_PATH)
reloaded = joblib.load(MODEL_PATH)
reload_pred = reloaded.predict(X_test)
assert np.array_equal(reload_pred, selected_prediction)
metadata = {
    "selected_model": SELECTED_MODEL_NAME,
    "random_state": RANDOM_STATE,
    "test_rows": len(X_test),
    "feature_columns": X.columns.tolist(),
}
(OUTPUT_DIR / "model_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"模型已保存并验证通过：{MODEL_PATH}")

# === 任务9：复盘 ===
print("\n=== 任务9：复盘 ===")
reflection = (
    "最低参照线全部预测为未流失，准确率虽高但流失召回率为零，"
    "完全不能识别流失用户，说明准确率不是评价分类模型的唯一指标。"
    "三个正式模型使用同一训练集和测试集公平比较，"
    "以确保对比结果可信。随机森林在本任务中综合表现最优，"
    "准确率最高且流失召回率优秀，能有效识别流失用户。"
    "模型输出的流失概率可用于对用户排序，"
    "将高概率用户列入优先关注名单，由业务团队进一步跟进干预，"
    "实现从数据预测到业务行动的闭环，降低客户流失率。"
)  # TODO 10-4
assert 150 <= len(reflection) <= 250
(OUTPUT_DIR / "reflection.txt").write_text(reflection, encoding="utf-8")
print(f"复盘 ({len(reflection)}字)：{reflection}")

# === 提交检查 ===
print("\n=== 提交检查 ===")
required = {
    "model_comparison.csv", "confusion_matrix_summary.csv",
    "customer_churn_predictions.csv", "high_risk_customers.csv",
    "feature_importance.csv", "selected_model.joblib",
    "model_metadata.json", "model_selection_note.txt", "reflection.txt",
}
actual = {p.name for p in OUTPUT_DIR.iterdir() if p.is_file()}
missing = required - actual
print("成果文件：", sorted(actual))
assert not missing, f"缺少：{sorted(missing)}"
print("Day 10 完成！")
