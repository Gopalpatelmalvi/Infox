"""
🔥 INSTAGRAM AUTO-REPORT BOT API 🔥
Creator: @SENKU_CODEX
Purpose: किसी भी Instagram ID को AUTO-REPORT करके BAN करवाना
Endpoint: /ban?username=target_username&count=1000
Example: /ban?username=hater_profile&count=5000
Warning: EDUCATIONAL PURPOSE ONLY
"""

from flask import Flask, jsonify, request
import requests
import random
import threading
import time
from datetime import datetime
import json
import os

app = Flask(__name__)

# GLOBAL VARIABLES
reports_running = False
report_threads = []
REPORT_LOG = "instagram_reports.log"

# PROXIES LIST (ROTATE KARNE KE LIYE)
PROXIES_LIST = [
    "103.156.141.109:8080",
    "45.7.177.235:39867", 
    "49.0.2.242:8090",
    "182.253.28.124:8080",
    "103.83.232.122:80",
    "190.109.16.145:999",
    "200.105.215.22:33630",
    "45.224.149.238:999"
]

def save_log(username, reports_sent, status):
    """Report ka log save karo"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] USER: {username} | REPORTS: {reports_sent} | STATUS: {status}\n"
    
    with open(REPORT_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    print(f"📝 LOG: {log_entry.strip()}")

def get_random_user_agent():
    """Random User-Agent generate karo"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
        'Instagram 219.0.0.12.117 Android',
        'Instagram 265.0.0.19.301 iOS'
    ]
    return random.choice(user_agents)

def send_single_report(target_username, report_type, proxy=None):
    """
    Single report send karo Instagram ko
    """
    try:
        # Instagram Report API endpoints (ANALYZED)
        report_urls = [
            "https://i.instagram.com/api/v1/users/report/",
            "https://www.instagram.com/api/v1/users/{user_id}/flag/",
            "https://graph.instagram.com/report_user"
        ]
        
        # Report reasons (Instagram ke allowed reasons)
        report_reasons = [
            "spam", "fake_account", "harassment", 
            "hate_speech", "violence", "nudity",
            "intellectual_property", "suicide_self_injury",
            "scam", "terrorism"
        ]
        
        reason = random.choice(report_reasons)
        
        # Headers (Instagram mobile app jaisa)
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-IG-App-ID': '936619743392459',
            'X-IG-Capabilities': '3brTvx8=',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        # Proxy use karo agar available ho
        proxies = None
        if proxy:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
        
        # Form data
        form_data = {
            'source_name': 'profile',
            'reason_id': random.randint(1, 10),
            'frx_context': '',
            'user_id': str(random.randint(1000000, 999999999)),  # Fake user ID
            'target_user': target_username,
            'report_type': reason,
            'session_id': generate_session_id()
        }
        
        # URL select karo
        url = random.choice(report_urls)
        
        # Request send karo
        response = requests.post(
            url,
            headers=headers,
            data=form_data,
            proxies=proxies,
            timeout=10
        )
        
        # Response check karo
        if response.status_code in [200, 201]:
            print(f"✅ Report sent to @{target_username} | Reason: {reason}")
            return True
        else:
            print(f"❌ Failed to report @{target_username} | Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Error reporting @{target_username}: {e}")
        return False

def generate_session_id():
    """Random session ID generate karo"""
    return ''.join(random.choices('abcdef0123456789', k=32))

def mass_report_worker(target_username, report_count, worker_id):
    """
    Mass report sending worker
    """
    global reports_running
    
    reports_sent = 0
    print(f"👷 Worker {worker_id} started for @{target_username}")
    
    while reports_running and reports_sent < report_count:
        try:
            # Random proxy select karo
            proxy = random.choice(PROXIES_LIST) if PROXIES_LIST else None
            
            # Report send karo
            success = send_single_report(target_username, "spam", proxy)
            
            if success:
                reports_sent += 1
                save_log(target_username, reports_sent, "SUCCESS")
            
            # Random delay (1-5 seconds)
            delay = random.uniform(1, 5)
            time.sleep(delay)
            
            # Progress show karo
            if reports_sent % 10 == 0:
                print(f"📊 Worker {worker_id}: {reports_sent}/{report_count} reports sent")
                
        except Exception as e:
            print(f"Worker {worker_id} error: {e}")
            time.sleep(2)
    
    print(f"🏁 Worker {worker_id} finished. Sent {reports_sent} reports.")
    return reports_sent

@app.route('/')
def home():
    return jsonify({
        "message": "🔥 INSTAGRAM AUTO-REPORT BOT API 🔥",
        "creator": "@SENKU_CODEX",
        "endpoint": "/ban?username=TARGET_USERNAME&count=REPORT_COUNT",
        "example": "/ban?username=hater_account&count=1000",
        "warning": "FOR EDUCATIONAL PURPOSE ONLY - USE RESPONSIBLY",
        "note": "Ye API Instagram accounts ko report karke ban karva sakti hai"
    })

@app.route('/ban', methods=['GET'])
def start_ban():
    """
    MAIN ENDPOINT: Instagram ID ko ban karne ke liye
    """
    global reports_running, report_threads
    
    try:
        target_username = request.args.get('username')
        report_count = int(request.args.get('count', 100))
        workers = int(request.args.get('workers', 5))
        
        if not target_username:
            return jsonify({
                "error": "Instagram username required!",
                "usage": "/ban?username=target_ig&count=1000&workers=5"
            }), 400
        
        # Stop any existing reports
        if reports_running:
            reports_running = False
            time.sleep(2)
            report_threads.clear()
        
        # Start fresh
        reports_running = True
        
        print(f"🚀 Starting MASS REPORT attack on @{target_username}")
        print(f"🎯 Target: {target_username}")
        print(f"📈 Reports to send: {report_count}")
        print(f"👥 Workers: {workers}")
        
        # Launch worker threads
        reports_per_worker = report_count // workers
        
        for i in range(workers):
            thread = threading.Thread(
                target=mass_report_worker,
                args=(target_username, reports_per_worker, i+1),
                daemon=True
            )
            report_threads.append(thread)
            thread.start()
        
        return jsonify({
            "status": "attack_started",
            "target": target_username,
            "total_reports": report_count,
            "workers": workers,
            "estimated_time": f"{report_count * 3} seconds",
            "message": f"🔥 MASS REPORT started on @{target_username}! 🔥",
            "log_file": REPORT_LOG,
            "note": "Check /status for progress"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "usage": "/ban?username=target_ig&count=1000"
        }), 500

@app.route('/status')
def get_status():
    """Current attack status check karo"""
    log_size = 0
    if os.path.exists(REPORT_LOG):
        with open(REPORT_LOG, 'r') as f:
            lines = f.readlines()
            log_size = len(lines)
    
    return jsonify({
        "attack_running": reports_running,
        "active_workers": len([t for t in report_threads if t.is_alive()]),
        "total_reports_logged": log_size,
        "log_file": REPORT_LOG,
        "note": "Check log file for detailed report history"
    })

@app.route('/stop')
def stop_attack():
    """Stop all reports"""
    global reports_running
    reports_running = False
    
    return jsonify({
        "status": "stopped",
        "message": "All report attacks stopped",
        "workers_stopped": len(report_threads)
    })

@app.route('/logs')
def view_logs():
    """Report logs dekho"""
    if not os.path.exists(REPORT_LOG):
        return jsonify({"error": "No logs found yet"}), 404
    
    with open(REPORT_LOG, 'r') as f:
        logs = f.readlines()
    
    return jsonify({
        "total_logs": len(logs),
        "recent_logs": logs[-20:]  # Last 20 logs
    })

@app.route('/test')
def test_report():
    """Test report functionality"""
    test_user = "test_account_" + str(random.randint(1000, 9999))
    success = send_single_report(test_user, "spam")
    
    return jsonify({
        "test": "completed",
        "target": test_user,
        "success": success,
        "message": "Test report sent (fake account)"
    })

# ADVANCED FEATURES
@app.route('/multi_ban', methods=['POST'])
def multi_ban():
    """Multiple Instagram IDs ek saath ban karo"""
    try:
        data = request.json
        usernames = data.get('usernames', [])
        reports_per_user = data.get('reports', 100)
        
        if not usernames:
            return jsonify({"error": "No usernames provided"}), 400
        
        results = []
        for username in usernames:
            # Start attack for each user
            thread = threading.Thread(
                target=mass_report_worker,
                args=(username, reports_per_user, f"multi_{username}"),
                daemon=True
            )
            thread.start()
            results.append({
                "username": username,
                "status": "attack_started",
                "reports": reports_per_user
            })
        
        return jsonify({
            "status": "multi_attack_launched",
            "targets": usernames,
            "reports_per_target": reports_per_user,
            "total_reports": len(usernames) * reports_per_user,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# RUN SERVER
if __name__ == '__main__':
    print("""
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    🔥  INSTAGRAM AUTO-REPORT BOT API  🔥
    🔥        by @SENKU_CODEX          🔥
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    
    ⚠️  WARNING: FOR EDUCATIONAL PURPOSE ONLY
    ⚠️  Use responsibly and legally
    
    🌐 API Running on: http://localhost:5000
    📍 Endpoint: /ban?username=TARGET&count=1000
    """)
    
    # Create log file if not exists
    if not os.path.exists(REPORT_LOG):
        with open(REPORT_LOG, 'w') as f:
            f.write("=== INSTAGRAM REPORT BOT LOGS ===\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)