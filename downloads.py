import resolutions # resolutions.py
import subprocess
import os
import requests
import re
import shutil

scriptPath = os.path.abspath(__file__) # Path to this script.
directoryPath = os.path.dirname(scriptPath) # Path to the directory.

def folderInput():
    folder = input("File location (enter nothing to select the current folder): ")
    folder = folder if folder else directoryPath # Take the folder input if one is specified (else the current folder).

    while True:
        if not os.path.isdir(folder):
            print("This folder doesn't exist! Please, try again!", end = "\n\n")
            folder = input("File location (enter nothing to select the current folder): ")
            folder = folder if folder else directoryPath
        else: break
    return folder


def videoDownload(youtubeVideo, system):
    downloadDirectory = folderInput()
    print("Looking for available resolutions for your video..")
    availableResolutions = resolutions.displayResolutions(youtubeVideo)

    while True:
        resolution = input("Video's resolution: ")
        if resolution not in availableResolutions: print(f"Unavailable resolution! Please, try again.", end = "\n\n")
        else: print("\nPreparing your download.. Download speed depends on your internet connection."); break

    if resolution == "360p": # Resolutions with audio.
        videoToDownload = youtubeVideo.streams.filter(resolution = resolution).first() # Select the 360p.
        youtubeVideo.register_on_progress_callback(downloadProgress) # Progress callback.
        videoTitle = re.sub(r"[<>:\"/\\|?*]", "", youtubeVideo.title) # Remove unvalid characters.
        videoToDownload.download(filename = f"{videoTitle}.mp4", output_path = directoryPath) # Download the video.
        print(f"\n\nDownload finished: \"{os.path.join(downloadDirectory, f"{videoTitle}")}.mp4\"")
    else: # Resolutions without audio.
        videoToDownload = youtubeVideo.streams.filter(resolution = resolution, only_video = True).first() # Select the video file.
        audioToDownload = youtubeVideo.streams.filter(only_audio = True, abr = "128kbps").first() # Select the audio file.
        youtubeVideo.register_on_progress_callback(downloadProgress) # Progress callback.
        videoToDownload.download(filename = "videoSource.mp4") # Download the video file.
        audioToDownload.download(filename = "audioSource.mp3") # Download the audio file.
        print("\nAssembling audio and video..", end = "\n\n")
        ffmpeg = "ffmpeg" # Default.
        if system == "Windows": ffmpeg = "ffmpeg.exe" # Windows.
        elif os.path.exists("/system/build.prop"): ffmpeg = "./ffmpeg" # Android.
        subprocess.run(f"{ffmpeg} -i videoSource.mp4 -i audioSource.mp3 -c:v copy -c:a aac output.mp4", shell = True) # Use ffmpeg to assemble the video file and audio file.
        videoTitle = re.sub(r"[<>:\"/\\|?*]", "", youtubeVideo.title) # Remove unvalid characters.
        os.rename("output.mp4", f"{videoTitle}.mp4") # Set the output video's name to the video title.
        os.remove("videoSource.mp4")
        os.remove("audioSource.mp3")
        if not directoryPath == downloadDirectory: shutil.move(f"./{videoTitle}.mp4", downloadDirectory) # Move the file in the targeted folder if it isn"t the current folder.
        print(f"\nDownload finished: \"{os.path.join(downloadDirectory, f"{videoTitle}")}.mp4\"")


def audioDownload(youtubeVideo):
    downloadDirectory = folderInput()
    audioToDownload = youtubeVideo.streams.filter(only_audio = True, abr = "128kbps").first() # Select the audio only.
    youtubeVideo.register_on_progress_callback(downloadProgress) # Download progress.
    audioTitle = re.sub(r"[<>:\"/\\|?*]", "", youtubeVideo.title) # Remove unvalid characters.
    audioToDownload.download(filename = f"{audioTitle}.mp3", output_path = downloadDirectory) # Download the audio.
    print(f"\n\nDownload finished: \"{os.path.join(downloadDirectory, f"{audioTitle}")}.mp3\"")


def downloadProgress(stream, chunk, sizeRemaining):
    videoSize = stream.filesize
    downloaded = videoSize - sizeRemaining
    percentage = downloaded / videoSize * 100   
    filled = int(20 * downloaded / videoSize)
    empty = 20 - filled
    bar = "[" + "█" * filled + " " * empty + "]"
    print(f"\rDownload's progress: {percentage:.0f}% {bar} ({downloaded / 1000000:.2f}MB/{videoSize / 1000000:.2f}MB).", end = "", flush = True)


def thumbnailDownload(videoThumbnail, videoTitle):
    downloadDirectory = folderInput()
    print("Preparing the download..")
    request = requests.get(videoThumbnail)

    if request.status_code == 200:
        videoTitle = re.sub(r"[<>:\"/\\|?*]", "", videoTitle) # Removing unvalid characters.

        with open(f"{videoTitle}.png", "wb") as file: # Open the file.
            file.write(request.content) # Write the data into a file.
            print(f"\nDownload finished: \"{os.path.join(downloadDirectory, f"{videoTitle}")}.png\"")
            if not directoryPath == downloadDirectory: shutil.move(f"./{videoTitle}.png", downloadDirectory) # Move the file in the targeted file if it isn"t the current folder.
    else: print(f"\nRequest failed with code {request.status_code}.")