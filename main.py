from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import yt_dlp

app = FastAPI()

@app.get("/download")
async def download_video(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '/tmp/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        
        # Скачиваем файл
        ydl.download([url])
        
    return StreamingResponse(open(f"/tmp/{video_title}.mp3", "rb"), media_type="audio/mp3")
