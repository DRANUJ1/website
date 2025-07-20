import os
import requests
from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route("/watch/<file_id>")
def watch_by_file_id(file_id):
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        return "BOT_TOKEN not set", 500

    # Get file path from Telegram
    res = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    if not res.ok or 'result' not in res.json():
        return abort(404)

    file_path = res.json()['result']['file_path']
    video_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    # Optional: auto title from file name
    filename = file_path.split("/")[-1]
    title = filename.replace("_", " ")

    # You can skip poster or use a default
    poster = "/static/default-poster.jpg"

    return render_template("player.html", title=title, poster=poster, video_url=video_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
