import tkinter
import fixAudio # Script

def showProgression(stream, chunk, sizeRemaining):
    videoSize = stream.filesize
    downloadedSize = videoSize - sizeRemaining
    percentage = downloadedSize / videoSize * 100   

    barSize = 20
    filled = int(barSize * downloadedSize / videoSize)
    empty = barSize - filled
    progressBar = '[' + '#' * filled + '-' * empty + ']'

    if not hasattr(showProgression, 'label'):
        showProgression.label = tkinter.Label()
        showProgression.label.place(x=5, y=270)

    showProgression.label.config(text=f'Progression du téléchargement : {percentage:.0f}% {progressBar} ({downloadedSize / 1000000:.2f}Mo/{videoSize / 1000000:.2f}Mo).', font='arial 12 bold')
    showProgression.label.update_idletasks()

def choiceResolution(resolutionInput, availableResolutions, app, fetchVideo):
    if resolutionInput.get() not in availableResolutions:
        tkinter.Label(app, text='Résolution non disponible, veuillez réessayer.', font='arial 15 bold', fg='red').place(x=180, y=270)
    else:
        videoResolution = resolutionInput.get()
        downloadVideo(fetchVideo, videoResolution, app)

def downloadVideo(fetchVideo, videoResolution, app):
    if videoResolution == '360p':
        video = fetchVideo.streams.filter(resolution=videoResolution).first()
        fetchVideo.register_on_progress_callback(showProgression)
        video.download()
    else:
        video = fetchVideo.streams.filter(resolution=videoResolution, only_video=True).first()
        audio = fetchVideo.streams.filter(only_audio=True).first()
        fetchVideo.register_on_progress_callback(showProgression)

        video.download(filename='videoSource.mp4')
        audio.download(filename='audioSource.mp3')

        tkinter.Label(app, text='Assemblage de l\'audio et de la vidéo.. Voir le terminal pour la progression.', font='arial 12 bold').place(x=5, y=290)
        fixAudio.fixAudioIssue(fetchVideo.title)

    tkinter.Label(app, text='Vidéo téléchargée !', font='arial 15 bold', fg='green').place(x=310, y=311)