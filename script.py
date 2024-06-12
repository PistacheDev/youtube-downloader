from pytube import YouTube # Importation du module "pytube".
import sys # Importation du module "sys".

# Fonction qui va afficher la progression du téléchargement de la vidéo.
def progression(stream, chunk, sizeRemaining):
    videoSize = stream.filesize # Calcul de la taille de la vidéo.
    downloadedSize = videoSize - sizeRemaining # Calcul du nombre d'octets téléchargés.
    percentage = downloadedSize / videoSize * 100 # Mise en place d'un pourcentage avec les valeurs obtenues.
    print(f'\rProgression du téléchargement : {percentage:.0f}% ({downloadedSize / 1000000:.2f}Mo/{videoSize / 1000000:.2f}Mo).', end = '', flush = True) # Mise à jour du pourcentage.

while True: # Boucle du programme.
    videoURL = input('Entrez le lien de la vidéo à télécharger : ') # Demande du lien de la vidéo YouTube à télécharger.
    fetchVideo = YouTube(videoURL) # Recherche de la vidéo sur YouTube.

    print('Préparation du téléchargement en cours..', end = '\n\n')
    video = fetchVideo.streams.get_highest_resolution() # Récupération de la vidéo.
    fetchVideo.register_on_progress_callback(progression) # Demande des informations sur la vidéo pour la progression.

    print('Souhaitez-vous choisir un chemin de destination personnalisé ?')
    destination = input("Si ce n'est pas le cas, laisser ce champ vide, sinon, renseignez le chemin d'accès : ")

    print('\nTéléchargement de votre vidéo en cours.. La vitesse du téléchargement dépend de votre connexion internet.')
    print('Progression du téléchargement : 0%.', end = '', flush = True)

    if destination == '':
        video.download('downloads') # Enregistrement de la vidéo dans le dossier "downloads" en cas de chemin de destination non renseigné.
    else:
        video.download(destination) # Enregistrement de la vidéo dans le chemin de destination personnalisé s'il a été renseigné.

    print('\nVidéo téléchargée avec succès !')
    restart = input('\nVous souhaitez télécharger une autre vidéo ? (o/n) ') # Demande pour lancer le téléchargement d'une autre vidéo.

    if restart == 'n':
        sys.exit() # Fermeture du programme si l'utilisateur ne veut pas d'un nouveau téléchargement.