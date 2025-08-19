import asyncio
import logging
from pathlib import Path
import requests

from mutagen.mp4 import MP4, MP4Cover
from shazamio import Shazam
import yt_dlp  # pip install yt-dlp

__author__ = "Grufoony"
__version__ = "3.1"

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(levelname)s - %(message)s")
logging.getLogger("symphonia_bundle_mp3.demuxer").setLevel(logging.ERROR)

out_dir = Path("./m4a")
out_dir.mkdir(exist_ok=True)

OUTTMLP = str(out_dir / "%(id)s.%(ext)s")
OUTTMLP_PLAYLIST = str(out_dir / "%(playlist_title)s/%(id)s.%(ext)s")

ALLOW_PLAYLIST = False

YT_OPTIONS = {
    "format": "bestaudio[ext=m4a]",
    "ignoreerrors": True,
    "addmetadata": True,
    "postprocessors": [
        {"key": "FFmpegMetadata"},
    ],
    # "outtmpl": will be set after
    # "playlistend": 2, # Debug only
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
    if len(url) == 0:
        continue
    if url.lower() in {".q", "quit", "exit", "leave", "stop", "end", "close"}:
        break
    if url.lower() in {"playlist"}:
        ALLOW_PLAYLIST = not ALLOW_PLAYLIST
        if ALLOW_PLAYLIST:
            logging.info("Playlist download enabled.")
        else:
            logging.info("Playlist download disabled.")
        continue

    if not ALLOW_PLAYLIST:
        # remove from url "&list=" and all character after
        url = url.split("&list=")[0]

    YT_OPTIONS["outtmpl"] = OUTTMLP_PLAYLIST if "&list=" in url else OUTTMLP

    try:
        with yt_dlp.YoutubeDL(YT_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        continue

    # Always work with a list of entries
    entries = [e for e in info.get("entries", []) if e] if "entries" in info else [info]

    for entry in entries:
        video_id = entry.get("id")
        downloaded_path = Path(ydl.prepare_filename(entry))
        if not downloaded_path.exists():
            logging.warning(
                f"Expected file {downloaded_path} not found, skipping tagging."
            )
            continue

        # --- sanitize metadata ---
        uploader = entry.get("uploader", "Unknown").replace("/", "_")
        raw_title = entry.get("title", "Unknown").replace("/", "_")
        title = raw_title
        if uploader in title:
            title = title.replace(uploader, "").strip()
        title = title.split("[")[0].strip()
        title = title.split("(Official")[0].strip()
        title = title.replace("(Visual)", "").strip()
        title = title.strip(" -_?!.,;:()[]{}'\"\\")

        # --- shazam recognition ---
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

        # --- tagging ---
        audio = MP4(str(downloaded_path))
        audio.tags["\u00a9nam"] = [song_title]
        audio.tags["\u00a9ART"] = [artist]
        album = ""
        year = entry.get("upload_date", "")[:4]
        genre = ""
        genres_info = track_data.get("genres", {}).get("primary")
        if genres_info:
            genre = genres_info
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
        audio.tags["desc"] = [entry.get("description", "")]
        audio.tags["ldes"] = [entry.get("webpage_url", "")]

        if cover_url:
            logging.info("Downloading cover art...")
            try:
                img_data = requests.get(cover_url).content
                audio.tags["covr"] = [
                    MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)
                ]
            except Exception as e:
                logging.warning(f"Could not embed cover art: {e}")

        audio.save()

        # --- rename inside same folder ---
        safe_artist = artist.replace("/", "_")
        safe_title = song_title.replace("/", "_")
        if "(" in safe_title and ")" not in safe_title:
            safe_title += ")"
        new_name = f"{safe_artist} - {safe_title}.m4a"
        new_path = downloaded_path.parent / new_name

        try:
            downloaded_path.rename(new_path)
            logging.info(f"Downloaded and tagged: {new_path.relative_to(out_dir)}")
        except Exception as e:
            logging.error(f"Could not rename {downloaded_path} -> {new_path}: {e}")
