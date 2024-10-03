def displayResolutions(youtubeVideo):
    availableResolutions = []

    for video in youtubeVideo.streams:
        if video.resolution != None:
            if video.resolution not in availableResolutions:
                availableResolutions.append(video.resolution)

    showResolutions = ', '.join(availableResolutions)
    print(f'\nAvailable resolutions: {showResolutions}')
    return availableResolutions