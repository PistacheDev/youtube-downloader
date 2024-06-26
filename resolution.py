def getResolution(fetchVideo):
    availableResolutions = [] # Tableau qui va contenir toutes les résolutions disponibles de la vidéo.
    print("Recherche d'informations sur la vidéo..")

    for video in fetchVideo.streams:
        if video.resolution != None: # Si la valeur n'est pas égal à None.
            if video.resolution not in availableResolutions: # Si la valeur n'est pas déjà présente dans le tableau.
                availableResolutions.append(video.resolution) # Envoie de la valeur dans le tableau.

    print('\nRésolutions disponibles :', end = ' ')
    showResolutions = ', '.join(availableResolutions) # Affichage des valeurs du tableau.
    print(f'{showResolutions}')

    i = 0
    resolution = input('Entrer la résolution que vous souhaitez télécharger : ')

    while i == 0: # Demande à l'utilisateur la résolution tant qu'elle n'est pas valide.
        if resolution not in availableResolutions: # Si la résolution de la vidéo n'est pas dans le tableau
            i = 0
            print("La résolution entrée n'est pas prise en charge par la vidéo sélectionnée.")
            resolution = input('\nEntrer la résolution que vous souhaitez télécharger : ')
        else:
            i = 1

    return resolution