import subprocess
import requests
import os

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN" # YOUR_TELEGRAM_BOT_TOKEN
CHANNEL_ID = "@yourchannelname"  # Or use chat ID, e.g., -1001234567890 id can be taken from @myidbot or @JsonDumpBot

def download_video(link):
    # Download and merge best video+audio with yt-dlp
    outtmpl = "downloaded.%(ext)s"
    cmd = [
        "yt-dlp",
        "-o", outtmpl,
        "-f", "bestvideo+bestaudio/best",
        link
    ]
    subprocess.run(cmd)
    # Find the final video file
    for ext in ("mp4", "mkv", "webm"):
        filename = f"downloaded.{ext}"
        if os.path.exists(filename):
            return filename
    return None

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    with open(file_path, "rb") as video_file:
        response = requests.post(
            url,
            data={"chat_id": CHANNEL_ID},
            files={"video": video_file}
        )
    if response.ok:
        print("Sent to Telegram!")
    else:
        print("Error:", response.content)

if __name__ == "__main__":
    link = input("Paste Bilibili link: ")
    video_file = download_video(link)
    if video_file:
        send_to_telegram(video_file)
    else:
        print("Download failed")
