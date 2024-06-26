from pytube import YouTube # Importation du module "pytube".
import sys # Importation du module "sys".

# Importation des fonctions des autres scripts.
from resolution import getResolution
from fixAudio import downloadSources, combineSources

while True:
    videoUrl = input('Entrez le lien de la vidéo à télécharger : ')
    fetchVideo = YouTube(videoUrl) # Recherche de la vidéo sur YouTube.
    resolution = getResolution(fetchVideo) # Recherche et propose les résolutions de la vidéo à l'utilisateur.

    video, audio = downloadSources(fetchVideo, resolution) # Téléchargement des éléments de la vidéo.
    combineSources(video, audio, fetchVideo) # Assemblage de la piste audio et de la piste vidéo.

    print('Vidéo téléchargée avec succès !')
    restart = input('\nVous souhaitez télécharger une autre vidéo ? (o/n) ')

    if restart == 'n':
        sys.exit() # Fermeture du programme si l'utilisateur ne veut pas d'un nouveau téléchargement.