import ffmpeg
import os

def fixAudioIssue(videoTitle):
    videoSource = ffmpeg.input('videoSource.mp4')
    audioSource = ffmpeg.input('audioSource.mp3')
    ffmpeg.output(videoSource, audioSource, f'{videoTitle}.mp4').run()

    os.remove('videoSource.mp4')
    os.remove('audioSource.mp3')