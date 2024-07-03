import tkinter
import downloader # Script

def displayTitle(fetchVideo, app):
    videoTitle = fetchVideo.title
    tkinter.Label(app, text=f'Titre : "{videoTitle}"', font='arial 12 bold').place(x=5, y=105)

def displayResolutions(fetchVideo, app):
    availableResolutions = []

    for video in fetchVideo.streams:
        if video.resolution != None:
            if video.resolution not in availableResolutions:
                availableResolutions.append(video.resolution)

    showResolutions = ', '.join(availableResolutions)
    tkinter.Label(app, text=f'Résolutions disponibles : {showResolutions}', font='arial 12 bold').place(x=5, y=125)

    tkinter.Label(app, text='Résolution de la vidéo à télécharger :', font='arial 15 bold').place(x=220, y=170)
    userResolution = tkinter.StringVar()
    tkinter.Entry(app, width=95, textvariable=userResolution).place(x=17, y=200)
    tkinter.Button(app, text='Envoyer', font='arial 15 bold', bg='red', padx=2, command=lambda:downloader.choiceResolution(userResolution, availableResolutions, app, fetchVideo)).place(x=356, y=229)