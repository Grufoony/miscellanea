import os
import yt_dlp

__author__ = "Grufoony"
__version__ = "2.1"

YT_OPTIONS = {
    "format": "bestaudio[ext=m4a]",
    "outtmpl": "./m4a/%(title)s.%(ext)s",
    "ignoreerrors": True,
}
if not os.path.exists("./m4a"):
    os.mkdir("./m4a")

print(f"Welcome to YouTube downloader v{__version__} by {__author__} https://github.com/Grufoony")
print("If you want to exit just type 'quit' or similar keywords instead of the URL.\n")

while True:
    url = input("Insert video URL:\n")
    if url in [".q", "quit", "exit", "leave", "stop", "end", "close"]:
        break
    try:
        with yt_dlp.YoutubeDL(YT_OPTIONS) as ydl:
            ydl.download(url)
    except Exception as e:
        print(f"Error downloading video: {e}")

for file in os.listdir("./m4a"):
    if file.endswith(".m4a"):
        original_name = file
        # remove extension
        file = file[:-4]
        # remove official video tag
        title = file.split("[")[0].strip()
        # Remove any string between parentheses with "official" in it
        title = title.split("(Official")[0].strip()
        os.rename(f"./m4a/{original_name}", f"./m4a/{title}.m4a")

print("Download and conversion complete!")
