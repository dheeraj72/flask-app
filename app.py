from flask import Flask, request, render_template
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    youtube_url = request.form['youtube']

    # Extract video ID from the URL using urlparse and parse_qs
    query = urlparse(youtube_url).query
    video_id = parse_qs(query).get('v', [None])[0]

    if video_id:
        try:
            # Create a YouTube object
            video = YouTube(youtube_url)
            # Get the highest-resolution video stream
            highest_resolution_stream = video.streams.get_highest_resolution()
            # Define your download path (e.g., Downloads folder)
            download_path = file_path()
            highest_resolution_stream.download(download_path)
            message = f"Video downloaded successfully! Saved to: {download_path}"
        except Exception as e:
            message = f"Error downloading video: {e}"
    else:
        message = 'Invalid YouTube URL'

    return render_template('index.html', youtube_url=youtube_url, video_id=video_id, message=message)

def file_path():
    home = os.path.expanduser('~')
    download_path = os.path.join(home, 'Downloads')
    return download_path

@app.route('/download', methods=['POST'])
def download():
    video_id = request.form['video_id']
    quality = request.form['quality']  # Get the selected quality (e.g., 'high', 'medium', 'low')

    try:
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        stream = video.streams.filter(res=quality).first()  # Get the stream based on selected quality
        download_path = file_path()
        stream.download(download_path)
        message = f"Video downloaded successfully! Saved to: {download_path}"
    except Exception as e:
        message = f"Error downloading video: {e}"

    return render_template('index.html', youtube_url='', video_id=video_id, message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
