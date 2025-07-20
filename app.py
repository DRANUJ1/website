from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import os  # ✅ This line was missing

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://nothingxhack:anujk24680@anujkumar.96pqsyb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["techvjclonefilterbot"]
collection = db["vjcollection"]

@app.route("/")
def home():
    return "✅ Streaming Bot Running!"

@app.route("/watch/<int:file_id>/<path:filename>")
def stream_video(file_id, filename):
    movie = collection.find_one({"_id": file_id})

    if not movie:
        return abort(404, "Movie not found")

    telegram_file_id = movie.get("file_id")

    if not telegram_file_id:
        return abort(404, "File ID missing")

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{filename}</title>
        <style>
            body {{
                background-color: #000;
                color: white;
                text-align: center;
                font-family: Arial, sans-serif;
            }}
            video {{
                width: 90%;
                margin-top: 20px;
            }}
            a {{
                color: #0af;
                text-decoration: none;
                margin-top: 10px;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <h3>{filename}</h3>
        <video controls autoplay>
            <source src="https://telegram-videostream.vercel.app/?file_id={telegram_file_id}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <p><a href="https://t.me/TNJANUJBOT?start=watch_{file_id}" target="_blank">📥 Open in Telegram</a></p>
    </body>
    </html>
    """
    return render_template_string(html_template)

 if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

