from pytube import YouTube
from pytube import Playlist
import pytube
import os
from moviepy.editor import AudioFileClip
from tqdm import tqdm

print("Welcome to YouTube downloader v 1.0 by Grufoony https://github.com/Grufoony\n")
print("If you want to download a playlist just insert 'playlist' instead of the video url, next you can insert the url of the playlist.\nIf you want to exit just type '.q' instead of the url.\n\n")

while True:
    url = input("Insert video url:\n")
    if url == ".q":
        break
    if url == "playlist":
        url = input("Insert playlist url:\n")
        if url == ".q":
            break
        playlist = Playlist(url)
        print(f'Number of videos in playlist: {len(playlist.video_urls)}')
        for video in tqdm(playlist.videos):
            try:
                audioStream = video.streams.get_by_itag("140")
                audioStream.download(output_path="./temp")
            except pytube.exceptions.AgeRestrictedError:
                print("Age restricted video")
    else:
        try:
            video = YouTube(url)
            audioStream = video.streams.get_by_itag("140")
            audioStream.download(output_path="./temp")
        except pytube.exceptions.AgeRestrictedError:
            print("Age restricted video")

# converting mp4 into mp3

for file in tqdm(os.listdir('./temp')):
    name = file[:-4]
    audio = AudioFileClip(os.path.join("./temp", file))
    audio.write_audiofile(os.path.join("./mp3", name + ".mp3"))
    audio.close()

# cleaning up temp folder

filelist = [ f for f in os.listdir("./temp") if f.endswith(".mp4") ]
for f in tqdm(filelist):
    os.remove(os.path.join("./temp", f))