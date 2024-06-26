from moviepy.editor import VideoFileClip, AudioFileClip # Importation de "moviepy".
import string
import os

def progression(stream, chunk, sizeRemaining):
    videoSize = stream.filesize # Calcul de la taille de la vidéo.
    downloadedSize = videoSize - sizeRemaining # Calcul du nombre d'octets téléchargés.
    percentage = downloadedSize / videoSize * 100 # Mise en place d'un pourcentage avec les valeurs obtenues.
    print(f'\rProgression du téléchargement : {percentage:.0f}% ({downloadedSize / 1000000:.2f}Mo/{videoSize / 1000000:.2f}Mo).', end = '', flush = True) # Mise à jour du pourcentage.

def downloadSources(fetchVideo, resolution):
    print('\nPréparation de votre téléchargement.. La vitesse du téléchargement dépend de votre connexion internet.')

    videoToDownload = fetchVideo.streams.filter(resolution=resolution).first() # Recherche de la piste vidéo.
    audioToDownload = fetchVideo.streams.filter(only_audio=True).first() # Recherche de la piste audio.
    fetchVideo.register_on_progress_callback(progression) # Demande des informations sur la vidéo pour la progression.
    print('Progression du téléchargement : 0%.', end = '', flush = True)

    video = videoToDownload.download(filename='video.mp4') # Téléchargement de la piste vidéo.
    audio = audioToDownload.download(filename='audio.mp3') # Téléchargement de la piste audio.

    print('\n\nAssemblage de la vidéo en cours.. Veuillez patienter.', end = '\n\n')
    return video, audio # Envoie des informations sur les différentes pistes de la vidéo.

def combineSources(video, audio, fetchVideo):
    videoClip = VideoFileClip(video)
    audioClip = AudioFileClip(audio)

    fullVideo = videoClip.set_audio(audioClip)
    videoTitle = fetchVideo.title

    validValues = "-_.() %s%s" % (string.ascii_letters, string.digits)
    validVideoName = ''.join(value for value in videoTitle if value in validValues)

    fullVideo.write_videofile(f'{validVideoName}.mp4', codec='h264')
    os.remove(video)
    os.remove(audio)