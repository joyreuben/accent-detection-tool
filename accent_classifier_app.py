import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os
import uuid
import tempfile
import urllib.parse
import yt_dlp

# Page config
st.set_page_config(page_title="Accent Classifier", layout="centered")
st.title("🗣️ English Accent Detection Tool")
st.markdown("Upload a YouTube URL and we'll extract and analyze the speaker’s English accent.")

# Function to clean and normalize YouTube URLs
def clean_youtube_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)

        # Handle youtu.be URLs
        if "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip("/")
        elif "youtube.com" in parsed.netloc and "v" in query:
            video_id = query["v"][0]
        else:
            raise ValueError("Could not parse video ID from URL.")

        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        return None

# Function to download and convert audio
def extract_audio_from_youtube(url):
    try:
        st.info("📥 Downloading and extracting audio using yt_dlp...")

        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the converted file
        for file in os.listdir(temp_dir):
            if file.endswith(".wav"):
                return os.path.join(temp_dir, file)

        st.error("⚠️ Could not find the audio file after extraction.")
        return None

    except Exception as e:
        st.error(f"❌ Audio extraction failed: {e}")
        return None

# Sidebar form
with st.sidebar:
    st.header("🎬 Input YouTube URL")
    youtube_url = st.text_input("Paste the YouTube link here", placeholder="e.g. https://youtu.be/abc123XYZ")

# Main logic
if youtube_url:
    cleaned_url = clean_youtube_url(youtube_url)
    if not cleaned_url:
        st.error("❌ Invalid or unsupported YouTube URL format.")
    else:
        st.success("✅ Valid YouTube URL detected!")
        audio_file = extract_audio_from_youtube(cleaned_url)

        if audio_file:
            st.audio(audio_file, format="audio/wav")
            st.success("✅ Audio ready for analysis.")
            st.markdown("👉 You can now proceed with accent classification here.")
        else:
            st.error("❌ Could not prepare the audio. Please check the link or try another.")

# Footer
st.markdown("""<hr><center>Built by Joy 🌍 | Powered by Streamlit</center>""", unsafe_allow_html=True)

