from flask import Flask, jsonify, render_template_string
import psutil, socket

app = Flask(__name__)

HTML = open("index.html").read()

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/stats")
def stats():
    net = psutil.net_io_counters()
    return jsonify({
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "net_sent_mb": round(net.bytes_sent / 1024 / 1024, 1),
        "net_recv_mb": round(net.bytes_recv / 1024 / 1024, 1),
        "hostname": socket.gethostname(),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
