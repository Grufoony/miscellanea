import asyncio
import logging
from pathlib import Path
import requests

from mutagen.mp4 import MP4, MP4Cover
from shazamio import Shazam
import yt_dlp  # pip install yt-dlp

__author__ = "Grufoony"
__version__ = "3.0"

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(levelname)s - %(message)s")

logging.getLogger("symphonia_bundle_mp3.demuxer").setLevel(logging.ERROR)

out_dir = Path("./m4a")
out_dir.mkdir(exist_ok=True)

YT_OPTIONS = {
    "format": "bestaudio[ext=m4a]",
    "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
    "ignoreerrors": True,
    "addmetadata": True,
    "postprocessors": [
        {"key": "FFmpegMetadata"},
    ],
}

# Initialize ShazamIO
shazam = Shazam()


# Helper to run async Shazam recognition from sync code
def recognize_track(file_path: str) -> dict:
    return asyncio.run(shazam.recognize(file_path))


logging.info(
    f"Welcome to YouTube downloader v{__version__} by {__author__} https://github.com/Grufoony"
)
logging.info("Type 'quit' to exit.")

while True:
    url = input("\n       Insert video URL:\t").strip()
    if url.lower() in {".q", "quit", "exit", "leave", "stop", "end", "close"}:
        break

    try:
        with yt_dlp.YoutubeDL(YT_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        continue

    video_id = info.get("id")
    downloaded_path = out_dir / f"{video_id}.m4a"
    if not downloaded_path.exists():
        logging.warning(f"Expected file {downloaded_path} not found, skipping tagging.")
        continue

    # Sanitize metadata fields
    uploader = info.get("uploader", "Unknown").replace("/", "_")
    raw_title = info.get("title", "Unknown").replace("/", "_")
    title = raw_title
    if uploader in title:
        title = title.replace(uploader, "").strip()
    title = title.split("[")[0].strip()
    title = title.split("(Official")[0].strip()
    title = title.replace("(Visual)", "").strip()
    title = title.strip(" -_?!.,;:()[]{}'\"\\")

    # Identify via ShazamIO
    logging.info("Identifying track via Shazam_IO...")
    try:
        result = recognize_track(str(downloaded_path))
    except Exception as e:
        logging.warning(f"Shazam recognition failed: {e}")
        result = {}

    track_data = result.get("track", {})
    artist = track_data.get("subtitle", uploader)
    song_title = track_data.get("title", title)
    images = track_data.get("images", {})
    cover_url = images.get("coverart") or images.get("background")

    # Load and update tags
    audio = MP4(str(downloaded_path))
    audio.tags["\u00a9nam"] = [song_title]
    audio.tags["\u00a9ART"] = [artist]
    # Extract album, year, and genre from Shazam metadata
    album = ""
    year = info.get("upload_date", "")[:4]
    genre = ""
    # Primary genre field
    genres_info = track_data.get("genres", {}).get("primary")
    if genres_info:
        genre = genres_info
    # Fallback: look into sections metadata
    sections = track_data.get("sections", [])
    if sections and "metadata" in sections[0]:
        for item in sections[0]["metadata"]:
            key = item.get("title", "").lower()
            text = item.get("text", "")
            if key == "album":
                album = text
            elif key in {"released", "release date", "year"}:
                year = text.split("-")[0]
            elif key == "genre":
                genre = text

    audio.tags["\u00a9alb"] = [album]
    audio.tags["\u00a9day"] = [year]
    audio.tags["\u00a9gen"] = [genre]
    audio.tags["desc"] = [info.get("description", "")]
    audio.tags["ldes"] = [info.get("webpage_url", "")]

    # Embed cover art
    if cover_url:
        logging.info("Downloading cover art...")
        try:
            img_data = requests.get(cover_url).content
            audio.tags["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
        except Exception as e:
            logging.warning(f"Could not embed cover art: {e}")

    audio.save()

    # Rename file to "Artist - Title.m4a"
    safe_artist = artist.replace("/", "_")
    new_name = f"{safe_artist} - {song_title}.m4a"
    new_path = out_dir / new_name
    downloaded_path.rename(new_path)

    logging.info(f"Downloaded and tagged: {new_name}")

logging.info("All downloads complete!")
