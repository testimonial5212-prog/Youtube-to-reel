import os
import sys
import subprocess

# ==================================================================
# 🪄 BACKGROUND AUTO-INSTALLER (Error vagar badha tools install thashe)
# ==================================================================
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from yt_dlp import YoutubeDL
except ImportError:
    install('yt-dlp')
    from yt_dlp import YoutubeDL

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    install('moviepy')
    from moviepy.editor import VideoFileClip

import streamlit as st

# ==================================================================
# 🌐 STREAMLIT WEBSITE UI
# ==================================================================

# Browser na tab nu naam ane layout setting
st.set_page_config(page_title="AI YouTube to Reel", layout="centered")

st.title("🎬 AI YouTube to Viral Insta Reel Converter")
st.write("YouTube video ni link muko ane full quality vertical Reel/Short download karo!")

# Link paste karva mate nu box
video_url = st.text_input("YouTube Video Link Ahiya Paste Karo 👇", "")

# Processing Button
if st.button("Generate Viral Reel 🚀"):
    if video_url:
        # Screen par loading animation dekhase
        with st.spinner("Video download ane crop thai rahyo che... aama 1-2 minyt no samay laagi shake che..."):
            try:
                # 1. High Quality MP4 Download Framework
                ydl_opts = {
    'format': 'best',
    # આ નીચેની લાઈનો ઉમેરો:
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # આનાથી ક્યારેક IP બ્લોકમાંથી મુક્તિ મળે છે
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate',
    }
}
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                # 2. Video open karvo ane dimensions ($9:16$ ratio) match karva
                clip = VideoFileClip("temp_web_video.mp4")
                w, h = clip.size
                
                # Vertical frame calculation (Center Crop)
                new_w = int(h * 9 / 16)
                x1 = (w - new_w) // 2
                x2 = x1 + new_w
                
                # Pehli 30 seconds no viral part cut karvo
                cropped_clip = clip.crop(x1=x1, y1=0, x2=x2, y2=h).subclip(0, 30)
                
                output_filename = "viral_insta_reel.mp4"
                
                # High quality rendering format
                cropped_clip.write_videofile(
                    output_filename, 
                    codec="libx264", 
                    audio_codec="aac", 
                    bitrate="5000k", 
                    fps=30,
                    logger=None # background text hide karva mate
                )
                
                # Files safely close karvi jethi crash na thay
                clip.close()
                cropped_clip.close()
                
                # Original moti file delete karvi
                if os.path.exists("temp_web_video.mp4"):
                    os.remove("temp_web_video.mp4")
                
                # 3. Web Par Green Message ane Download Button
                st.success("🎉 Tamari Viral Reel Tayar Che!")
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="⬇️ Download High Quality Reel",
                        data=file,
                        file_name="Insta_Reel_HQ.mp4",
                        mime="video/mp4"
                    )
                
                # Final clean up
                os.remove(output_filename)

            except Exception as e:
                st.error(f"Kaik error aavi, fari try karo: {str(e)}")
    else:
        st.warning("Pehla koi valid YouTube link nako!")
