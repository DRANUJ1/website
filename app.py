from flask import Flask, render_template, abort
import json

app = Flask(__name__)

# Load video data
with open('videos.json', 'r') as f:
    videos = json.load(f)

@app.route('/')
def home():
    return "📺 Welcome to Movie Stream!"

@app.route('/watch/<id>/<filename>')
def watch(id, filename):
    video = videos.get(id)
    if not video:
        return abort(404)
    return render_template('watch.html', video=video)

@app.route('/books')
def books():
    return render_template('books.html')
