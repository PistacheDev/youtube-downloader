import requests
import resolutions
import subprocess
import os

def videoDownload(youtubeVideo, videoTitle):
    print('Préparation du téléchargement de la vidéo..')
    availableResolutions = resolutions.displayResolutions(youtubeVideo)

    resolution = input('Quelle résolution souhaitez-vous utiliser pour votre vidéo ? ')
    i = 0

    while i == 0:
        if resolution not in availableResolutions:
            print(f'La résolution entrée ("{resolution}") n\'est pas disponible pour ce téléchargement, veuillez réessayer.', end = '\n\n')
            resolution = input('Quelle résolution souhaitez-vous utiliser pour votre vidéo ? ')
        else:
            i = 1
            print('\nPréparation de votre téléchargement.. La vitesse du téléchargement dépend de votre connexion internet.')
    
    if resolution == '360p':
        videoToDownload = youtubeVideo.streams.filter(resolution=resolution).first()
        youtubeVideo.register_on_progress_callback(pytubeDownloadProgress)
        video = videoToDownload.download()

        print('Progression du téléchargement : 0%.', end = '', flush = True)
        print(f'\n\nTéléchargement terminé : {video}')
    else:
        videoToDownload = youtubeVideo.streams.filter(resolution=resolution, only_video=True).first()
        audioToDownload = youtubeVideo.streams.filter(only_audio=True).first()
        youtubeVideo.register_on_progress_callback(pytubeDownloadProgress)

        videoToDownload.download(filename='videoSource.mp4')
        audioToDownload.download(filename='audioSource.mp3')

        print('Assemblage de la piste vidéo et de la piste audio..', end = '\n\n')
        subprocess.run(f'ffmpeg -i videoSource.mp4 -i audioSource.mp3 -c:v copy -c:a aac output.mp4', shell=True)

        os.rename('output.mp4', f'{videoTitle}.mp4')
        os.remove('videoSource.mp4')
        os.remove('audioSource.mp3')

        print(f'\nTélécargement terminé : "{videoTitle}.mp4"')


def pytubeDownloadProgress(stream, chunk, sizeRemaining):
    videoSize = stream.filesize
    downloadedSize = videoSize - sizeRemaining
    percentage = downloadedSize / videoSize * 100   

    barSize = 20
    filled = int(barSize * downloadedSize / videoSize)
    empty = barSize - filled
    progressBar = '[' + '#' * filled + '-' * empty + ']'

    print(f'\rProgression du téléchargement : {percentage:.0f}% {progressBar} ({downloadedSize / 1000000:.2f}Mo/{videoSize / 1000000:.2f}Mo).', end = '', flush = True)


def thumbnailDownload(videoThumbnail, videoTitle):
    print('Préparation du téléchargement de la miniature..')
    response = requests.get(videoThumbnail)

    if response.status_code == 200:
        with open(f'{videoTitle}.png', 'wb') as file:
            file.write(response.content)
            print(f'\nTéléchargement terminé : "{videoTitle}.png"')