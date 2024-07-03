import platform
import tkinter
import pytube
import getInfos # Script

userPlatform = platform.system()
app = tkinter.Tk()
app.geometry('800x600')
app.resizable(0, 0)
app.title('Youtube Downloader - https://github.com/PistacheDev/youtube-downloader')

if userPlatform == 'Linux':
    icon = tkinter.PhotoImage('icon.ico')
    app.iconphoto(False, icon)
elif userPlatform == 'Windows' :
    app.iconbitmap('icon.ico')
else:
    print(f'"{userPlatform}" n\'est pas pris en charge !\nVous pouvez modifier le repo github (https://github.com/PistacheDev/youtube-downloader) afin de l\'adapter pour vous et les autres utilisateurs.')
    app.destroy()

tkinter.Label(app, text='Lien de la vidéo à télécharger :', font='arial 15 bold').place(x=250, y=5)
videoUrl = tkinter.StringVar()
tkinter.Entry(app, width=95, textvariable=videoUrl).place(x=17, y=35)
tkinter.Button(app, text='Télécharger', font='arial 15 bold', bg='red', padx=2, command=lambda:launchDownloader(videoUrl, app)).place(x=336, y=64)

def launchDownloader(videoUrl, app):
    fetchVideo = pytube.YouTube(str(videoUrl.get()))
    getInfos.displayTitle(fetchVideo, app)
    getInfos.displayResolutions(fetchVideo, app)

app.mainloop()