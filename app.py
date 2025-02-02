# app.py (Flask后端)
from flask import Flask, jsonify, request, render_template
from datetime import datetime
from collections import deque

app = Flask(__name__)

# 存储最近50次检查结果和外部提供的可用率
status_data = {
    "checks": deque(maxlen=50),  # 保存最近50条记录
    "availability": 0.0  # 来自POST请求的可用率
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def get_status():
    return jsonify({
        "checks": list(status_data["checks"]),
        "availability": status_data["availability"],
        "current_count": len(status_data["checks"])
    })


@app.route('/post', methods=['POST'])
def post_check():
    # 接收并处理表单数据
    form_data = request.form

    status = ["Success!","Incorrect Answer","TimeOut","Error"]

    # 构建检查记录
    check_entry = {
        "status_type": int(form_data.get("status_type", -1)),
        "status_code": int(form_data.get("status_code", 0)),
        "status": status[int(form_data.get("status_type", -1))],
        "duration": float(form_data.get("duration", 0)),
        "timestamp": str(form_data.get("timestamp")) + "Z"
    }

    # 更新数据和可用率
    status_data["checks"].append(check_entry)
    status_data["availability"] = float(form_data.get("availability", 0.0))

    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)