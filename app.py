import yt_dlp


def get_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        print(f"\n📺 Title: {info.get('title')}")
        for f in formats:
            # Determine stream type
            v = f.get('vcodec')
            a = f.get('acodec')

            if v != 'none' and a != 'none':
                stream_type = 'both'
            elif v != 'none':
                stream_type = 'video'
            elif a != 'none':
                stream_type = 'audio'
            else:
                continue  # Skip unknown

            quality = f.get('format_note') or f.get(
                'height') or f.get('abr') or 'unknown'
            print(f"🔸 {quality} | {stream_type} | {f.get('url')}")


# 🔽 List of video/playlist URLs
urls = [
    "https://www.youtube.com/shorts/D5vd6mB36XQ"
]

for url in urls:
    try:
        get_formats(url)
    except Exception as e:
        print(f"Error processing {url}: {e}")
