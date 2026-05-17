# narmer_live_server.py
import json, time, threading
from flask import Flask, jsonify
import sqlite3

DB_PATH = "C:/Users/ip/narmer_enterprise/backend/narmer_project/narmer_v56.db"
app = Flask(__name__)

def get_latest_data():
    """قراءة أحدث الأبعاد من قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT dimensions FROM score_history ORDER BY timestamp DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
    except:
        pass
    return {d: 75.0 for d in DIMS_AR}

@app.route("/api/live")
def live_data():
    dims = get_latest_data()
    export = []
    for d in DIMS_AR:
        export.append({"dimension": d, "value": dims.get(d, 50), "weight": float(WEIGHTS[DIMS_AR.index(d)])})
    return jsonify(export)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050)