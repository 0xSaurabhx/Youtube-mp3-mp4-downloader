import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import shutil
import os

BOT_TOKEN = '6556103654:AAGDzRHqFPY7RCrAirbbNXNTO96EJI3yPic'
CHANNEL_ID = '-1002144289063'

st.set_page_config(page_icon="⬇️", page_title="Youtube MP3 & MP4 Downloader")

st.sidebar.title("OWNER ONLY")
password = st.sidebar.text_input("Enter Password", type='password')
if st.sidebar.button("Delete Files"):
    if password == os.environ['PASSWORD']:
        if os.path.exists("./MP3"):
            shutil.rmtree("./MP3")
        if os.path.exists("./MP4"):
            shutil.rmtree("./MP4")
        st.success("Files deleted successfully!")
    else:
        st.sidebar.write("Wrong Password")

def main():
    st.title("YouTube Video Downloader")
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
                id = video_url.split("=")[-1]
                if quality == "480p":
                    stream = yt.streams.filter(res="480p").first()
                elif quality == "720p":
                    stream = yt.streams.filter(res="720p").first()
                elif quality == "1080p":
                    stream = yt.streams.filter(res="1080p").first()
                if stream is None:
                    stream = yt.streams.get_highest_resolution()
                if format == "MP4":
                    with st.spinner("Downloading..."):
                        stream.download(filename=f"{id}.mp4",output_path="./MP4/")
                    with open(f"./MP4/{id}.mp4", "rb") as file:
                        btn = st.download_button(
                            label="Download File",
                            data=file.read(),
                            file_name=f"{id}.mp4",
                        )
                    st.success("MP4 Download completed successfully!")
                elif format == "MP3":
                    with st.spinner("Downloading..."):
                        stream.download(filename=f"{id}.mp4",output_path="./MP3/")
                        video_path = f"./MP3/{id}.mp4"
                        audio_path = f"./MP3/{id}.mp3"
                    with st.spinner("Converting..."):
                        AudioSegment.from_file(video_path).export(audio_path, format="mp3")
                    with open(f"./MP3/{id}.mp4", "rb") as file:
                        btn = st.download_button(
                            label="Download File",
                            data=file.read(),
                            file_name=f"{id}.mp4",
                        )
                    st.success("MP3 Converted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a YouTube video URL.")

if __name__ == "__main__":
    main()
