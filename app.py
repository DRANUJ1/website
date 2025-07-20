from flask import Flask, request, abort, render_template_string, redirect
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["techvjclonefilterbot"]
collection = db["vjcollection"]  # Replace with your collection name

# Telegram file link base URL (adjust as needed)
TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot<your_bot_token>/"

@app.route("/")
def home():
    return "✅ Streaming Bot Working!"

@app.route("/watch/<int:file_id>/<path:filename>")
def stream_video(file_id, filename):
    movie = collection.find_one({"_id": file_id})

    if not movie:
        return abort(404, "Movie not found")

    telegram_file_id = movie.get("file_id")

    if not telegram_file_id:
        return abort(404, "File ID missing in database")

    # Optional: direct Telegram download link
    stream_link = f"https://telegram.me/your_bot_username?start=watch_{file_id}"

    # Basic video player template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{filename}</title>
    </head>
    <body style="background-color:#000; color:white
