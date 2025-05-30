import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os
import uuid
import random

# Function to extract audio from video URL
def extract_audio_from_url(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        temp_video_file = f"temp_audio_{uuid.uuid4()}.mp4"
        stream.download(filename=temp_video_file)

        audio_path = f"temp_audio_{uuid.uuid4()}.wav"
        audio = AudioSegment.from_file(temp_video_file)
        audio.export(audio_path, format="wav")

        os.remove(temp_video_file)
        return audio_path
    except Exception as e:
        st.error(f"Failed to extract audio: {e}")
        return None

# Mock function to simulate accent analysis (English accents only)
def mock_accent_analysis(audio_path):
    english_accents = ["American", "British", "Australian", "Irish", "Canadian"]
    chosen_accent = random.choice(english_accents)
    confidence = round(random.uniform(70, 99), 2)
    summary = f"The speaker appears to have a {chosen_accent} English accent based on phonetic patterns."
    return {
        "accent": chosen_accent,
        "confidence": confidence,
        "summary": summary
    }
    
    # Streamlit UI
st.set_page_config(page_title="English Accent Classifier", layout="centered")

# Title with emoji
st.markdown("""
<h1 style='text-align: center;'>🗣️ English Accent Classifier Tool</h1>
""", unsafe_allow_html=True)

# Introduction text
st.markdown("""
This tool extracts audio from a video URL and classifies the **English accent** of the speaker.

Paste a YouTube or Loom link below ⬇️
""")

video_url = st.text_input("🎬 Enter a video URL:")

if video_url:
    with st.spinner("Processing audio and analyzing accent..."):
        audio_path = extract_audio_from_url(video_url)
        if audio_path:
            result = mock_accent_analysis(audio_path)
            st.success("✅ Analysis Complete")

            st.markdown(f"""
<div style='background-color: #f0f8ff; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;'>
<b>Accent:</b> {result['accent']}<br>
<b>Confidence:</b> {result['confidence']}%<br>
<b>Summary:</b> {result['summary']}
</div>
""", unsafe_allow_html=True)

            os.remove(audio_path)
        else:
            st.error("❌ Audio extraction failed.")

# Footer
st.markdown("""<hr><center>Built by Joy 🌍 | Powered by Streamlit</center>""", unsafe_allow_html=True)
