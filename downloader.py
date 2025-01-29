import os
from tqdm import tqdm
import yt_dlp

YT_OPTIONS = {
    'format': 'bestaudio[ext=m4a]',
    'outtmpl': './m4a/%(title)s.%(ext)s',
}
if not os.path.exists("./m4a"):
    os.mkdir("./m4a")

print("Welcome to YouTube downloader v2.0 by Grufoony https://github.com/Grufoony")
print("If you want to download a playlist just type 'playlist' or '.p' instead of the video URL, next you can insert the URL of the playlist.")
print("If you want to exit just type '.q' instead of the URL.")
print("")

pl = ["playlist", ".p"]
leave = [".q"]

while True:
    url = input("Insert video URL:\n")
    if url in leave:
        break
    if url in pl:
        url = input("Insert playlist URL:\n")
        if url in leave:
            break
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': './temp/%(id)s.%(ext)s', 'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }]}) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            print(f'Number of videos in playlist: {len(playlist_info["entries"])}')
            for entry in tqdm(playlist_info['entries']):
                try:
                    ydl.download([entry['url']])
                except Exception as e:
                    print(f"Error downloading {entry['title']}: {e}")
    else:
        try:
            with yt_dlp.YoutubeDL(YT_OPTIONS) as ydl:
                ydl.download(url)
        except Exception as e:
            print(f"Error downloading video: {e}")

for file in os.listdir("./m4a"):
    if file.endswith(".m4a"):
        # remove official video tag
        title = file.split("(")[0].strip()
        os.rename(f"./m4a/{file}", f"./m4a/{title}.m4a")

print("Download and conversion complete!")
