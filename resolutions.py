def displayResolutions(youtubeVideo):
    availableResolutions = []

    for video in youtubeVideo.streams:
        if video.resolution is not None:
            if video.resolution not in availableResolutions:
                availableResolutions.append(video.resolution)

    availableResolutions = sorted(availableResolutions, key = lambda x: int(x[:-1])) # Display the resolutions in an ascending order.
    showResolutions = ', '.join(availableResolutions)

    print(f'\nAvailable resolutions: {showResolutions}')
    return availableResolutions