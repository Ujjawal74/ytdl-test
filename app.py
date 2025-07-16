from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

# 🔽 Hardcoded URLs for `/` endpoint
urls = [
    "https://www.youtube.com/shorts/D5vd6mB36XQ"
]

def extract_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            title = info.get('title', 'Unknown Title')

            result = {
                'url': url,
                'title': title,
                'formats': []
            }

            for f in formats:
                v = f.get('vcodec')
                a = f.get('acodec')

                if v != 'none' and a != 'none':
                    stream_type = 'both'
                elif v != 'none':
                    stream_type = 'video'
                elif a != 'none':
                    stream_type = 'audio'
                else:
                    continue

                quality = f.get('format_note') or f.get('height') or f.get('abr') or 'unknown'
                result['formats'].append({
                    'quality': quality,
                    'type': stream_type,
                    'url': f.get('url')
                })

            return result

    except Exception as e:
        return {
            'url': url,
            'error': str(e)
        }

# Route 1: Home page — returns all formats for hardcoded list
@app.route('/')
def index():
    results = [extract_formats(url) for url in urls]
    return jsonify(results)

# Route 2: /video?link=...
@app.route('/video')
def get_video():
    link = request.args.get('link')
    if not link:
        return jsonify({'error': 'Missing ?link= parameter'}), 400

    result = extract_formats(link)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
