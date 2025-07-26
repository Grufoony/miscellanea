from pathlib import Path
import yt_dlp  # pip install yt-dlp

__author__ = "Grufoony"
__version__ = "2.3"

out_dir = Path("./m4a")
out_dir.mkdir(exist_ok=True)

YT_OPTIONS = {
    "format": "bestaudio[ext=m4a]",
    "outtmpl": "./m4a/%(id)s.%(ext)s",
    "ignoreerrors": True,
    "addmetadata": True,
    "postprocessors": [
        {"key": "FFmpegMetadata"},
    ],
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
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        print(f"Error downloading video: {e}")
        continue

    # build the original filename (by id)
    downloaded = out_dir / f"{info.get('id')}.m4a"
    if not downloaded.exists():
        print(f"  • expected file {downloaded} not found, skipping tagging.")
        continue

    # sanitize uploader/title for filesystem
    uploader = info.get("uploader", "Unknown").replace("/", "_")
    title = info.get("title", "Unknown").replace("/", "_")

    # Remove the uploade from the file name
    if uploader in title:
        title = title.replace(uploader, "").strip()
    # remove official video tag
    title = title.split("[")[0].strip()
    # Remove any string between parentheses with "official" in it
    title = title.split("(Official")[0].strip()
    title = title.replace("(Visual)", "").strip()
    # Remove any left special character at the init of the title or at the end
    title = title.strip(" -_?!.,;:()[]{}'\"\\")

    # new filename: "Uploader - Title.m4a"
    new_filename = out_dir / f"{title}.m4a"
    downloaded.rename(new_filename)

print("Download and conversion complete!")
