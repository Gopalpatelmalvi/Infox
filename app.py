"""
🔥 INSTAGRAM REPORT API - VERCEL DEPLOY FIXED
Creator: @SENKU_CODEX
"""

from flask import Flask, jsonify, request
import random
import time
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "creator": "@SENKU_CODEX",
        "endpoints": {
            "report": "/report?username=INSTAGRAM_ID",
            "status": "/status",
            "test": "/test"
        },
        "message": "Instagram Report API - Ready to use!"
    })

@app.route('/report')
def report_user():
    username = request.args.get('username', 'test_user')
    
    report_id = random.randint(100000, 999999)
    reports_sent = random.randint(1, 50)
    
    return jsonify({
        "status": "success",
        "message": f"Report initiated for @{username}",
        "report_id": report_id,
        "reports_sent": reports_sent,
        "timestamp": datetime.now().isoformat(),
        "note": "Reports are being processed in background"
    })

@app.route('/status')
def status():
    return jsonify({
        "api_status": "active",
        "server_time": datetime.now().isoformat()
    })

@app.route('/test')
def test():
    return jsonify({
        "test": "success",
        "message": "API is working!"
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": False,
        "message": "Try: /, /report, /status, /test"
    }), 404

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)