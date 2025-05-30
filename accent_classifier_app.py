import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
from pydub.utils import which
import os
import uuid

# Set ffmpeg path (important for Streamlit Cloud)
AudioSegment.converter = which("ffmpeg")

# Function to clean YouTube URL
def clean_youtube_url(url):
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    elif "youtube.com" in url:
        return url.split("&")[0].split("?")[0]
    return url

# Function to download and convert YouTube audio
def download_audio_from_youtube(url, output_filename="output_audio.wav"):
    try:
        url = clean_youtube_url(url)
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        if not stream:
            raise Exception("No audio stream found!")

        temp_filename = f"{uuid.uuid4()}.mp4"
        downloaded_file = stream.download(filename=temp_filename)

        # Convert to WAV using pydub
        audio = AudioSegment.from_file(downloaded_file)
        audio.export(output_filename, format="wav")
        os.remove(downloaded_file)

        return output_filename

    except Exception as e:
        st.error(f"❌ Audio extraction failed: {e}")
        return None

# Streamlit UI
st.title("🎙️ English Accent Detection Tool")

video_url = st.text_input("Enter a YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Analyze"):
    if video_url:
        st.info("🔄 Extracting audio from video...")

        audio_path = download_audio_from_youtube(video_url)

        if audio_path:
            st.success("✅ Audio successfully extracted!")
            st.audio(audio_path)
            st.markdown(f"""
<div style='background-color: #f0f8ff; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;'>
<b>Accent:</b> {result['accent']}<br>
<b>Confidence:</b> {result['confidence']}%<br>
<b>Summary:</b> {result['summary']}
</div>
""", unsafe_allow_html=True)

            # 👉 Placeholder: Call your accent classifier here
            st.write("🔍 Now run your classifier on the extracted audio file.")

    else:
        st.warning("⚠️ Please enter a YouTube URL.")
