import os
from flask import Flask, render_template, request, jsonify
from sentinel_engine import SentinelEngine

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
engine = SentinelEngine()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/system-stats", methods=["GET"])
def get_system_stats():
    try:
        stats = engine.get_system_stats()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/processes", methods=["GET"])
def get_processes():
    limit = int(request.args.get("limit", 35))
    sort_by = request.args.get("sort_by", "memory")
    try:
        procs = engine.get_process_list(limit=limit, sort_by=sort_by)
        return jsonify({"success": True, "processes": procs, "count": len(procs)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/process/<int:pid>", methods=["GET"])
def get_process_detail(pid):
    try:
        detail = engine.get_process_detail(pid)
        return jsonify(detail)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


if __name__ == "__main__":
    print("Iniciando Sentinel Node PRO Dashboard en http://localhost:5007")
    app.run(host="0.0.0.0", port=5007, debug=False)
