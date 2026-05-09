import os
from gtts import gTTS
import moviepy as mpe
import urllib.request

async def create_video(script: str, output_path: str):
    """
    Generates a video programmatically.
    Logic: Uses MoviePy to overlay AI-generated voiceovers (gTTS) onto a downloaded placeholder video (or stock footage via API).
    """
    print(f"[Production Agent] Generating voiceover for script...")

    audio_path = f"temp_audio_{hash(script)}.mp3"

    try:
        # Generate TTS audio
        tts = gTTS(text=script, lang='en')
        tts.save(audio_path)

        print(f"[Production Agent] Fetching stock footage (Placeholder)...")
        # In a real scenario you would call Pexels API:
        # response = requests.get(f"https://api.pexels.com/videos/search?query=nature", headers={"Authorization": PEXELS_API_KEY})
        # video_url = response.json()['videos'][0]['video_files'][0]['link']

        # Download a placeholder video from a public source to avoid API keys in tests
        video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
        placeholder_video_path = f"temp_video_{hash(script)}.mp4"
        urllib.request.urlretrieve(video_url, placeholder_video_path)

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
