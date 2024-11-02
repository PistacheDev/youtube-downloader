import resolutions # resolutions.py
import subprocess
import os
import requests
import re
import shutil

scriptPath = os.path.abspath(__file__) # Path to this script.
directoryPath = os.path.dirname(scriptPath) # Path to the directory.

def selectFolderInput():
    folder = input('File location (enter nothing to select the current folder): ')
    folder = folder if folder else directoryPath # Take the folder input if one is specified (else the current folder).

    while True:
        if not os.path.isdir(folder):
            print('This folder doesn\'t exist! Please, try again!', end = '\n\n')
            folder = input('File location (enter nothing to select the current folder): ')
            folder = folder if folder else directoryPath
        else:
            break

    return folder

def videoDownload(youtubeVideo, system):
    downloadDirectory = selectFolderInput()
    print('Looking for available resolutions for your video..')
    availableResolutions = resolutions.displayResolutions(youtubeVideo)
    resolution = input('Video\'s resolution: ')

    while True:
        if resolution not in availableResolutions:
            print(f'Unavailable resolution! Please, try again.', end = '\n\n')
            resolution = input('Video\'s resolution: ')
        else:
            print('\nPreparing your download.. Download speed depends on your internet connection.')
            break

    if resolution == '360p': # Resolutions with audio.
        videoToDownload = youtubeVideo.streams.filter(resolution = resolution).first()
        youtubeVideo.register_on_progress_callback(pytubeDownloadProgress)
        videoTitle = re.sub(r'[<>:"/\\|?*]', '', youtubeVideo.title) # Removing unvalid characters.

        videoToDownload.download(filename = f'{videoTitle}.mp4', output_path = directoryPath)
        print(f'\n\nDownload finished: "{os.path.join(downloadDirectory, f'{videoTitle}')}.mp4"')
    else: # Resolutions without audio.
        videoToDownload = youtubeVideo.streams.filter(resolution = resolution, only_video = True).first()
        audioToDownload = youtubeVideo.streams.filter(only_audio = True, abr = '128kbps').first()
        youtubeVideo.register_on_progress_callback(pytubeDownloadProgress)

        videoToDownload.download(filename = 'videoSource.mp4')
        audioToDownload.download(filename = 'audioSource.mp3')

        print('\nAssembling audio and video..', end = '\n\n')
        ffmpeg = 'ffmpeg'

        if system == 'Windows':
            ffmpeg = 'ffmpeg.exe'
        elif os.path.exists('/system/build.prop'):
            ffmpeg = './ffmpeg'

        subprocess.run(f'{ffmpeg} -i videoSource.mp4 -i audioSource.mp3 -c:v copy -c:a aac output.mp4', shell = True)
        videoTitle = re.sub(r'[<>:"/\\|?*]', '', youtubeVideo.title) # Removing unvalid characters.
        os.rename('output.mp4', f'{videoTitle}.mp4')
        os.remove('videoSource.mp4')
        os.remove('audioSource.mp3')
        if not directoryPath == downloadDirectory: # Move the file in the targeted folder if it isn't the current folder.
            shutil.move(f'./{videoTitle}.mp4', downloadDirectory)

        print(f'\nDownload finished: "{os.path.join(downloadDirectory, f'{videoTitle}')}.mp4"')

def audioDownload(youtubeVideo):
    downloadDirectory = selectFolderInput()
    audioToDownload = youtubeVideo.streams.filter(only_audio = True, abr = '128kbps').first()
    youtubeVideo.register_on_progress_callback(pytubeDownloadProgress)

    audioTitle = re.sub(r'[<>:"/\\|?*]', '', youtubeVideo.title) # Removing unvalid characters.
    audioToDownload.download(filename = f'{audioTitle}.mp3', output_path = downloadDirectory)
    print(f'\n\nDownload finished: "{os.path.join(downloadDirectory, f'{audioTitle}')}.mp3"')

def pytubeDownloadProgress(stream, chunk, sizeRemaining):
    videoSize = stream.filesize
    downloadedSize = videoSize - sizeRemaining
    percentage = downloadedSize / videoSize * 100   

    filled = int(20 * downloadedSize / videoSize)
    empty = 20 - filled
    progressBar = '[' + '█' * filled + ' ' * empty + ']'

    print(f'\rDownload\'s progress: {percentage:.0f}% {progressBar} ({downloadedSize / 1000000:.2f}MB/{videoSize / 1000000:.2f}MB).', end = '', flush = True)

def thumbnailDownload(videoThumbnail, videoTitle):
    downloadDirectory = selectFolderInput()
    print('Preparing the download..')
    request = requests.get(videoThumbnail)

    if request.status_code == 200:
        videoTitle = re.sub(r'[<>:"/\\|?*]', '', videoTitle) # Removing unvalid characters.

        with open(f'{videoTitle}.png', 'wb') as file:
            file.write(request.content)
            print(f'\nDownload finished: "{os.path.join(downloadDirectory, f'{videoTitle}')}.png"')
            if not directoryPath == downloadDirectory: # Move the file in the targeted file if it isn't the current folder.
                shutil.move(f'./{videoTitle}.png', downloadDirectory)
    else:
        print(f'\nRequest failed with code {request.status_code}.')