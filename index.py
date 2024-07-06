import pytube
import sys
import downloads # Script

while True:
    videoUrl = input('Lien de la vidéo YouTube : ')
    youtubeVideo = pytube.YouTube(videoUrl)
    print('Recherche des informations sur la vidéo..')

    videoTitle = youtubeVideo.title
    videoThumbnail = youtubeVideo.thumbnail_url
    videoAuthor = youtubeVideo.author
    videoRestriction = 'Non'
    videoViews = youtubeVideo.views

    if youtubeVideo.age_restricted == True:
        videoRestriction = 'Oui'

    print('\nInformations sur la vidéo :')
    print(f'- Titre : "{videoTitle}"')
    print(f'- Miniature : {videoThumbnail}')
    print(f'- Auteur : {videoAuthor}')
    print(f'- Restriction adulte : {videoRestriction}')
    print(f'- Nombre de vues : {videoViews} vue(s)')

    print('\nQue souhaitez-vous télécharger ?')
    print('1) La vidéo')
    print('2) La miniature')
    print('3) Les deux')

    download = input('\nNuméro de l\'option voulue : ')
    i = 0

    while i == 0:
        if download == '1':
            downloads.videoDownload(youtubeVideo, videoTitle)
            i = 1
        elif download == '2':
            downloads.thumbnailDownload(videoThumbnail, videoTitle)
            i = 1
        elif download == '3':
            downloads.thumbnailDownload(videoThumbnail, videoTitle)
            downloads.videoDownload(youtubeVideo, videoTitle)
            i = 1
        else:
            print(f'L\'option entrée ("{download}") n\'est pas valide.', end = '\n\n')
            download = input('Numéro de l\'option voulue : ')

    restart = input('Souhaitez-vous faire un autre téléchargement ? (o/n) ')

    if restart == 'n':
        sys.exit()