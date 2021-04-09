from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

def download(url):
    video = url.streams.first()
    filepath = video.download()
    return filepath

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        url = YouTube(session['link'])
        return render_template('see_video.html',url=url, filetitle = url.title, fileimg = url.thumbnail_url, length = url.length, channel=url.author, views=url.views, published=url.publish_date.strftime("%d %B, %Y"))
    return render_template('index.html')

@app.route("/download",methods=['GET','POST'])
def see_video():
    if request.method == 'POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filename = video.download()
        return send_file(filename, as_attachment=True)
    return redirect(url_for('index.html'))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
