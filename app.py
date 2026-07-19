"""
电商用户行为分析 Web 数据展示项目 (Day 07)
Flask Web 系统：登录、看板、筛选与离线问答
"""
import os
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, send_file
from services.data_service import get_overall_metrics, get_segment_analysis, get_cross_analysis, get_category_data, get_filtered_data, get_download_data
from services.qa_service import get_qa_response

app = Flask(__name__)
app.secret_key = "day07_secret_key_change_me"
app.permanent_session_lifetime = timedelta(minutes=30)

# ==================== 登录 ====================
VALID_USERS = {"student": "day07"}


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    if username in VALID_USERS and VALID_USERS[username] == password:
        session["user"] = username
        session.permanent = True
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="账号或密码错误"), 401


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ==================== 看板 ====================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))

    category = request.args.get("category", "all")
    metrics = get_overall_metrics()
    segments = get_segment_analysis()
    cross = get_cross_analysis()
    category_data = get_category_data()

    # 筛选
    filtered_df = get_filtered_data(category)
    filtered_metrics = None
    if category != "all" and not filtered_df.empty:
        filtered_metrics = {
            "总用户数": int(filtered_df["CustomerID"].nunique()),
            "流失用户数": int(filtered_df[filtered_df["Churn"] == 1]["CustomerID"].nunique()),
            "总体流失率": f"{filtered_df['Churn'].mean() * 100:.1f}%",
            "平均订单数": f"{filtered_df['OrderCount'].mean():.2f}",
        }

    return render_template(
        "dashboard.html",
        metrics=metrics,
        segments=segments.to_dict("records"),
        cross=cross.to_dict("records"),
        category_data=list(category_data.keys()),
        current_category=category,
        filtered_metrics=filtered_metrics,
    )


# ==================== API ====================
@app.route("/api/ask", methods=["POST"])
def api_ask():
    """离线问答 API"""
    data = request.get_json()
    question = data.get("question", "").strip() if data else ""
    if not question:
        return jsonify({"answer": "请输入您的问题。"}), 400
    answer = get_qa_response(question)
    return jsonify({"question": question, "answer": answer})


@app.route("/api/categories")
def api_categories():
    """获取品类列表"""
    if "user" not in session:
        return jsonify({"error": "未登录"}), 401
    cats = ["all"] + list(get_category_data().columns)
    return jsonify({"categories": cats})


# ==================== 拓展A：下载筛选结果 ====================
@app.route("/download")
def download_filtered():
    """导出当前筛选条件的 CSV"""
    category = request.args.get("category", "all")
    df = get_download_data(category)
    if df.empty:
        return jsonify({"error": "没有可导出的数据"}), 400

    filename = f"filtered_data_{category}.csv" if category != "all" else "filtered_data_all.csv"
    csv_data = df.to_csv(index=False, encoding="utf-8-sig")
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    return response


# ==================== 拓展B：生命周期详情页 ====================
@app.route("/segments")
def segments_page():
    if "user" not in session:
        return redirect(url_for("index"))
    segments = get_segment_analysis()
    cross = get_cross_analysis()
    return render_template("segments.html", segments=segments.to_dict("records"), cross=cross.to_dict("records"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
