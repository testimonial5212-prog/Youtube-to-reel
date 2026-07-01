import os
import streamlit as st
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

st.set_page_config(page_title="AI Video to Reel", layout="centered")

st.title("🎬 Viral Reel Converter")

url = st.text_input("YouTube Link Muko:")

if st.button("Generate Reel"):
    if url:
        with st.spinner("Processing..."):
            try:
                # 403 error ne rokva mate vadhare detailed headers
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                    'outtmpl': 'temp_web_video.mp4',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'referer': 'https://www.youtube.com/',
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Video Crop Logic
                clip = VideoFileClip("temp_web_video.mp4")
                w, h = clip.size
                new_w = int(h * 9 / 16)
                x1 = (w - new_w) // 2
                
                cropped_clip = clip.crop(x1=x1, y1=0, x2=x1+new_w, y2=h).subclip(0, 30)
                
                output = "final_reel.mp4"
                cropped_clip.write_videofile(output, codec="libx264", audio_codec="aac", bitrate="2000k", fps=30, logger=None)
                
                st.success("Teyar che!")
                with open(output, "rb") as f:
                    st.download_button("Download Reel", f, "reel.mp4")
                
                clip.close()
                cropped_clip.close()
                os.remove("temp_web_video.mp4")
                os.remove(output)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write("Tip: Jo 403 error aave to, YouTube aana IP ne block kare che.")
