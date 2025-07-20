import os
import json
import requests
from flask import Flask, render_template, abort

app = Flask(__name__)

# Load video data once
with open('videos.json', 'r') as f:
    videos = json.load(f)

@app.route("/watch/<id>/<filename>")
def watch(id, filename):
    video = videos.get(id)
    if not video:
        return abort(404)

    file_id = video.get("file_id")
    title = video.get("title")
    poster = video.get("poster")

    # Get Telegram file path
    bot_token = os.environ.get("BOT_TOKEN")
    res = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    if not res.ok:
        return abort(500)

    file_path = res.json()['result']['file_path']
    video_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    return render_template("player.html", title=title, poster=poster, video_url=video_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
