import platform
import ffmpeg # ffmpeg.py
import pytubefix
import downloads # downloads.py
import os

try:
    system = platform.system() # Detect the OS.
    ffmpeg.checkInstallation(system) # Check if ffmpeg is installed.

    while True:
        url = input("YouTube video's link: ")
        youtubeVideo = pytubefix.YouTube(url) # Fetch the video with pytubefix.
        print("Fetching video's data..")

        # Fetch informations.
        title = youtubeVideo.title
        thumbnail = youtubeVideo.thumbnail_url
        author = youtubeVideo.author
        channel = youtubeVideo.channel_url
        restriction = youtubeVideo.age_restricted
        views = youtubeVideo.views

        print(f"\nVideo's information :\n- Title: \"{title}\"\n- Thumbnail: {thumbnail}\n- Author: {author} ({url})\n- 18+: {"Yes" if restriction == True else "No"}\n- Views count: {views} views")
        print("\nWhat do you want to download?\n1) The full video\n2) Audio only\n3) Thumbnail")

        while True:
            download = input("\nOption's number: ")
            if download == "1": downloads.videoDownload(youtubeVideo, system); break
            elif download == "2": downloads.audioDownload(youtubeVideo); break
            elif download == "3": downloads.thumbnailDownload(thumbnail, title); break
            else: print(f"Please, try again.", end = "\n\n") # Bad option.

        restart = input("Ready for an another download? (y/n) ")
        if restart.lower() == "n": break
        os.system("cls" if system == "Windows" else "clear") # Clear the terminal.
except Exception as err:
    print(f"\nThe program crashed!\nError: {err}", end = "\n\n")
    input("Press [Enter] to close the program..")