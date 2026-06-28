import streamlit as st
import os
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

# Website nu Title
st.title("🎬 AI YouTube to Viral Insta Reel Converter")
st.write("Khali YouTube video ni link muko ane full quality vertical Reel download karo!")

# Link input box
video_url = st.text_input("YouTube Video Link Ahiya Paste Karo 👇", "")

if st.button("Generate Viral Reel 🚀"):
    if video_url:
        with st.spinner("Video download ane crop thai rahyo che... aama thodo samay lagshe..."):
            try:
                # 1. High Quality Download
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                    'outtmpl': 'temp_web_video.mp4',
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                # 2. 9:16 Aspect Ratio ma Auto Crop (Center mathi)
                clip = VideoFileClip("temp_web_video.mp4")
                w, h = clip.size
                new_w = int(h * 9 / 16)
                x1 = (w - new_w) // 2
                x2 = x1 + new_w
                
                # Pehli 30 seconds no viral part cut thashe
                cropped_clip = clip.crop(x1=x1, y1=0, x2=x2, y2=h).subclip(0, 30)
                
                output_filename = "viral_insta_reel.mp4"
                cropped_clip.write_videofile(
                    output_filename, 
                    codec="libx264", 
                    audio_codec="aac", 
                    bitrate="5000k", 
                    fps=30
                )
                
                clip.close()
                cropped_clip.close()
                os.remove("temp_web_video.mp4")
                
                # 3. Web UI upar Download Button aapvu
                st.success("🎉 Tamari Viral Reel Tayar Che!")
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="⬇️ Download High Quality Reel",
                        data=file,
                        file_name="Insta_Reel_HQ.mp4",
                        mime="video/mp4"
                    )
                
                # Clean up output file after offering download
                os.remove(output_filename)

            except Exception as e:
                st.error(f"Kaik error aavi: {str(e)}")
    else:
        st.warning("Pehla koi valid YouTube link nako!")
