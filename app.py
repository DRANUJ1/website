from flask import Flask, render_template, request, abort
import os
import requests

app = Flask(__name__)

@app.route("/watch/<id>/<path:filename>")
def watch(id, filename):
    from flask import request, abort, send_file
    file_id = request.args.get("hash")

    if not file_id:
        return abort(400, "Missing file_id (hash)")

    print("DEBUG:", id, filename, file_id)

    # yahan aap telegram file download logic ya redirect logic likh sakte ho
    return f"Filename: {filename}, ID: {id}, File_ID: {file_id}"


    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        return abort(500, "BOT_TOKEN not configured")

    # Get file path from Telegram
    r = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}")
    if not r.ok or 'result' not in r.json():
        return abort(404, "File not found in Telegram")

    file_path = r.json()["result"]["file_path"]
    video_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    return render_template("player.html", title=filename, poster="/static/poster.jpg", video_url=video_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
