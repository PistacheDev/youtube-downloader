from pytube import YouTube

videoURL = input('Entrez le lien de la vidéo à télécharger : ')
fetchVideo = YouTube(videoURL)

print('Téléchargement en cours..')
video = fetchVideo.streams.get_highest_resolution()

video.download()
print('Vidéo téléchargée avec succès !')