
from flask import Flask, request, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video = None
    formats = []
    url = ""

    if request.method == 'POST':
        url = request.form['url']
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)

                video = {
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                }

                for fmt in info['formats']:
                    if fmt.get('url') and fmt.get('vcodec') != 'none':
                        formats.append({
                            'format_id': fmt['format_id'],
                            'resolution': fmt.get('format_note') or f"{fmt.get('height', 'N/A')}p",
                            'ext': fmt['ext'],
                            'filesize': f"{(fmt.get('filesize', 0) / 1024 / 1024):.2f} MB" if fmt.get('filesize') else 'Unknown'
                        })

                formats.sort(key=lambda x: x['resolution'], reverse=True)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', video=video, formats=formats, url=url)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_id = request.form['format_id']

    download_folder = 'downloads'
    os.makedirs(download_folder, exist_ok=True)

    ydl_opts = {
        'format': format_id,
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s')
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "Download started! Check your 'downloads' folder."

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/home')
def home():
    return render_template('home.html', title="Home")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html', title="Privacy Policy")

@app.route('/terms-of-service')
def terms():
    return render_template('terms.html', title="Terms of Service")


@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html', title="Disclaimer")
