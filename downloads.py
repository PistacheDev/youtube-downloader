import resolutions # resolutions.py
import subprocess
import os
import requests
import re

def videoDownload(youtubeVideo, system):
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

        videoToDownload.download(filename = f'{videoTitle}.mp4')
        print(f'\n\nDownload finished: "{videoTitle}.mp4"')
    else: # Resolutions without audio.
        videoToDownload = youtubeVideo.streams.filter(resolution = resolution, only_video = True).first()
        audioToDownload = youtubeVideo.streams.filter(only_audio = True).first()
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

        print(f'\nDownload finished: "{videoTitle}.mp4"')


def audioDownload(youtubeVideo):
    audioToDownload = youtubeVideo.streams.filter(only_audio = True).first()
    youtubeVideo.register_on_progress_callback(pytubeDownloadProgress)

    audioTitle = re.sub(r'[<>:"/\\|?*]', '', youtubeVideo.title) # Removing unvalid characters.
    audioToDownload.download(filename = f'{audioTitle}.mp3')
    print(f'\n\nDownload finished: "{audioTitle}.mp3"')


def pytubeDownloadProgress(stream, chunk, sizeRemaining):
    videoSize = stream.filesize
    downloadedSize = videoSize - sizeRemaining
    percentage = downloadedSize / videoSize * 100   

    filled = int(20 * downloadedSize / videoSize)
    empty = 20 - filled
    progressBar = '[' + '█' * filled + ' ' * empty + ']'

    print(f'\rDownload\'s progress : {percentage:.0f}% {progressBar} ({downloadedSize / 1000000:.2f}MB/{videoSize / 1000000:.2f}MB).', end = '', flush = True)


def thumbnailDownload(videoThumbnail, videoTitle):
    print('Preparing the download..')
    request = requests.get(videoThumbnail)

    if request.status_code == 200:
        videoTitle = re.sub(r'[<>:"/\\|?*]', '', videoTitle) # Removing unvalid characters.

        with open(f'{videoTitle}.png', 'wb') as file:
            file.write(request.content)
            print(f'\nDownload finished: "{videoTitle}.png"')
    else:
        print(f'\nRequest failed with code {request.status_code}.')