from pathlib import Path
import yt_dlp  # pip install yt-dlp

__author__ = "Grufoony"
__version__ = "2.2"

out_dir = Path("./m4a")
out_dir.mkdir(exist_ok=True)

YT_OPTIONS = {
    "format": "bestaudio[ext=m4a]",
    "outtmpl": "./m4a/%(title)s.%(ext)s",
    "ignoreerrors": True,
}
print(
    f"Welcome to YouTube downloader v{__version__} by {__author__} https://github.com/Grufoony"
)
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

for file in out_dir.glob("*.m4a"):
    title = file.stem
    # remove official video tag
    title = title.split("[")[0].strip()
    # Remove any string between parentheses with "official" in it
    title = title.split("(Official")[0].strip()

    new_file = out_dir / f"{title}.m4a"
    # Rename the file
    if new_file != file:
        file.rename(new_file)

print("Download and conversion complete!")
