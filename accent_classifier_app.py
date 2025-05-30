import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import uuid
import shutil
import random

# Simulated function for accent classification
def classify_accent(audio_path):
    # Placeholder for your model prediction logic
    accents = ['American", "British", "Australian", "Irish", "Canadian']
    return {
        "accent": random.choice(accents),
        "confidence": round(random.uniform(0.7, 0.99), 2)
    }

# YouTube audio downloader
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

# Streamlit App UI
st.set_page_config(page_title="Accent Classifier", layout="centered")

st.title("🗣️ Accent Detection Tool")
st.write("Paste a YouTube link to extract audio and classify the speaker's accent.")

youtube_url = st.text_input("🔗 Enter YouTube URL:")

if st.button("Analyze") and youtube_url:
    st.info("📥 Downloading and processing audio...")
    audio_path = download_audio_from_youtube(youtube_url)

    if audio_path:
        st.success("✅ Audio extracted successfully!")
        st.audio(audio_path)

        # Classify accent
        with st.spinner("🧠 Analyzing accent..."):
            result = classify_accent(audio_path)
            st.markdown("### 🎯 Accent Classification Result")
            st.write(f"**Predicted Accent:** {result['accent']}")
            st.write(f"**Confidence Score:** {result['confidence'] * 100:.1f}%")

        # Clean up temp files
        os.remove(audio_path)
    else:
        st.error("❌ Could not extract audio. Please check the link or try another.")


# Footer
st.markdown("""<hr><center>Built by Joy 🌍 | Powered by Streamlit</center>""", unsafe_allow_html=True)

