import os
import requests
from flask import Flask, render_template, abort
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Setup
MONGO_URI = os.environ.get("MONGO_URI")  # Set this in Render environment
client = MongoClient(MONGO_URI)
db = client.get_database("techvjclonefilterbot")  # your DB name
collection = db.get_collection("vjcollection")  # your collection name

@app.route("/watch/<id>")
def watch(id):
    video = collection.find_one({"id": id})
    if not video:
        return abort(404)

    file_id = video.get("file_id")
    title = video.get("title", "Untitled Video")
    poster = video.get("poster", "/static/default.jpg")

    # Fetch Telegram File Path
    bot_token = os.environ.get("BOT_TOKEN")
    res = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    if not res.ok or 'result' not in res.json():
        return abort(500)

    file_path = res.json()['result']['file_path']
    video_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    return render_template("player.html", title=title, poster=poster, video_url=video_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
