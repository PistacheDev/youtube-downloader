def displayResolutions(youtubeVideo):
    availableResolutions = []

    for video in youtubeVideo.streams:
        if video.resolution != None:
            if video.resolution not in availableResolutions:
                availableResolutions.append(video.resolution)

    showResolutions = ', '.join(availableResolutions) # Formatage du texte
    print(f'\nRésolutions disponibles : {showResolutions}')
    return availableResolutions