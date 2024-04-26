import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os

st.set_page_config(page_icon="⬇️", page_title="Youtube MP3 & MP4 Downloader")

def main():
    st.title("YouTube Video ⬇️loader")
    video_url = st.text_input("Enter YouTube Video URL:")
    format = st.selectbox("Select Format", ["MP4", "MP3"])
    if format == "MP4":
        quality = st.selectbox("Select Quality", ["480p", "720p", "1080p"])
    else:
        quality = st.selectbox("Select Quality", ["720p", "1080p"])
    if st.button("Download"):
        if video_url:
            try:
                yt = YouTube(video_url)
                if quality == "480p":
                    stream = yt.streams.filter(res="480p").first()
                elif quality == "720p":
                    stream = yt.streams.filter(res="720p").first()
                elif quality == "1080p":
                    stream = yt.streams.filter(res="1080p").first()
                if stream is None:
                    stream = yt.streams.get_highest_resolution()
                
                st.markdown(f"Downloading **{yt.title}** at {quality}...")
                if format == "MP4":
                    stream.download()
                elif format == "MP3":
                    stream.download(filename="temp_video.mp4")
                    video_path = "temp_video.mp4"
                    audio_path = "temp_audio.mp3"
                    AudioSegment.from_file(video_path).export(audio_path, format="mp3")
                    os.remove(video_path)
                    st.success("MP3 Download completed successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a YouTube video URL.")

if __name__ == "__main__":
    main()
