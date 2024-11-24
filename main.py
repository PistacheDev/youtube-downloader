import platform
import ffmpeg # ffmpeg.py
import pytubefix
import downloads # downloads.py
import os

try:
    system = platform.system()
    ffmpeg.checkInstallation(system)

    while True:
        videoUrl = input('YouTube video\'s link: ')
        youtubeVideo = pytubefix.YouTube(videoUrl)
        print('Fetching video\'s data..')

        videoTitle = youtubeVideo.title
        videoThumbnail = youtubeVideo.thumbnail_url
        videoAuthor = youtubeVideo.author
        channelUrl = youtubeVideo.channel_url
        videoRestriction = youtubeVideo.age_restricted
        videoViews = youtubeVideo.views

        print('\nVideo\'s information :')
        print(f'- Title: "{videoTitle}"')
        print(f'- Thumbnail: {videoThumbnail}')
        print(f'- Author: {videoAuthor} ({channelUrl})')
        print(f'- 18+: {'Yes' if videoRestriction == True else 'No'}')
        print(f'- Views count: {videoViews} views')

        print('\nWhat do you want to download?')
        print('1) The full video')
        print('2) Audio only')
        print('3) Thumbnail')
        download = input('\nOption\'s number: ')

        while True:
            if download == '1':
                downloads.videoDownload(youtubeVideo, system);
                break
            elif download == '2':
                downloads.audioDownload(youtubeVideo)
                break
            elif download == '3':
                downloads.thumbnailDownload(videoThumbnail, videoTitle)
                break
            else:
                print(f'Please, try again.', end = '\n\n')
                download = input('Option\'s number: ')

        restart = input('Ready for an another download? (y/n) ')

        if restart.lower() == 'n':
            break

        os.system('cls' if system == 'Windows' else 'clear')
except Exception as err:
    print(f'\nThe program crashed!\nError: {err}', end = '\n\n')
    input('Press [Enter] to close the program..')