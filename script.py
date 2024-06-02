from pytube import YouTube # Importation du module "pytube".
import sys # Importation du module "sys".

while True:
    # Input demandant le lien de la vidéo YouTube à télécharger.
    videoURL = input('Entrez le lien de la vidéo à télécharger : ')
    fetchVideo = YouTube(videoURL) # Recherche de la vidéo sur YouTube, et, demande de la progression du téléchargement.
    video = fetchVideo.streams.get_highest_resolution()

    # Input demandant si un chemin de destination personnalisé est nécessaire.
    print('Souhaitez-vous choisir un chemin de destination personnalisé ?')
    destination = input("Si ce n'est pas le cas, laisser ce champ vide, sinon, renseignez le chemin d'accès : ")

    print('Téléchargement de votre vidéo en cours.. La vitesse du téléchargement dépend de votre connexion internet.')
    # Téléchargement de la vidéo avec le module et enregistrement au chemin de destination chosi.
    if destination == '':
        video.download()
    else:
        video.download(destination)

    print('Vidéo téléchargée avec succès !')
    restart = input('\nVous souhaitez télécharger une autre vidéo ? (o/n) ') # Relancement du programme en fonction de l'utilisateur.

    # Fermeture du programme si non.
    if restart == 'n':
        sys.exit()