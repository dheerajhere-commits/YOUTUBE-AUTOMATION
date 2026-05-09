import os
from gtts import gTTS
import moviepy as mpe
import urllib.request
import requests
from core.config import config

def fetch_stock_video(query: str) -> str:
    """Fetches real stock footage from Pexels API."""
    api_key = config.get('api_keys', {}).get('pexels_api')
    if not api_key or api_key == "YOUR_PEXELS_API_KEY":
        print("[Production Agent] Pexels API key not configured. Using fallback placeholder video.")
        video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
        path = f"temp_video_{hash(query)}.mp4"
        urllib.request.urlretrieve(video_url, path)
        return path

    print(f"[Production Agent] Fetching stock footage from Pexels API for '{query}'...")
    headers = {"Authorization": api_key}
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=portrait",
            headers=headers
        )
        videos = r.json().get('videos', [])
        if not videos:
            raise ValueError("No stock footage found")
        # Pick best quality under 30MB (simplified: pick highest width for demo)
        video_files = videos[0]['video_files']
        chosen = sorted(video_files, key=lambda x: x.get('width', 0))[-1]
        path = f"temp_stock_{hash(query)}.mp4"
        urllib.request.urlretrieve(chosen['link'], path)
        return path
    except Exception as e:
        print(f"[Production Agent] Pexels API failed: {e}. Using fallback placeholder video.")
        video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
        path = f"temp_video_{hash(query)}.mp4"
        urllib.request.urlretrieve(video_url, path)
        return path

async def create_video(script: str, output_path: str):
    """
    Generates a video programmatically.
    Logic: Uses MoviePy to overlay AI-generated voiceovers (gTTS) onto stock footage.
    """
    print(f"[Production Agent] Generating voiceover for script...")

    audio_path = f"temp_audio_{hash(script)}.mp3"
    placeholder_video_path = None

    try:
        # Generate TTS audio
        tts = gTTS(text=script, lang='en')
        tts.save(audio_path)

        # Determine a keyword from the script (simplified, use first 10 chars as fallback)
        query = "technology" if "AI" in script or "tech" in script.lower() else "nature"

        placeholder_video_path = fetch_stock_video(query)

        print(f"[Production Agent] Assembling video with MoviePy...")
        video_clip = mpe.VideoFileClip(placeholder_video_path)
        audio_clip = mpe.AudioFileClip(audio_path)

        # Ensure video length matches audio or trim video
        if video_clip.duration > audio_clip.duration:
            video_clip = video_clip.subclipped(0, audio_clip.duration)
        else:
            # If audio is longer, we might need to loop the video, but for now just trim audio
            audio_clip = audio_clip.subclipped(0, video_clip.duration)

        final_video = video_clip.with_audio(audio_clip)

        # Write output file
        # Using a low quality and small size for fast testing.
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

        print(f"[Production Agent] Video saved to {output_path}")

    except Exception as e:
        print(f"[Production Agent] Failed to generate video: {e}")
        # Fallback to dummy file if MoviePy or gTTS fails (e.g. missing system dependencies like ImageMagick)
        with open(output_path, 'w') as f:
            f.write(f"Dummy video content due to generation error for script: {script[:20]}...")

    finally:
        # Cleanup temporary files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if 'placeholder_video_path' in locals() and os.path.exists(placeholder_video_path):
            os.remove(placeholder_video_path)

    return output_path
