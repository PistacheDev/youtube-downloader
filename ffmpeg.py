import os
import subprocess
import urllib.request
import zipfile
import shutil
import sys

def checkInstallation(system):
    if system == 'Windows':
        if os.path.isfile('./ffmpeg.exe'):
            print('Great! ffmpeg is installed!')
        else:
            print('ffmpeg isn\'t installed!')
            windowsInstallation()
    elif system == 'Linux':
        if os.path.exists('/system/build.prop'): # Android devices.
            if os.path.isfile('./ffmpeg'):
                print('Great! ffmpeg is installed!')
            else:
                print('ffmpeg isn\'t installed!')
                androidInstallation()
        else:
            isInstalled = False
            packageManager = None
            cmdList = {
                0: ['snap', 'list', 'ffmpeg'],
                1: ['dpkg', '-s', 'ffmpeg'],
                2: ['rpm', '-q', 'ffmpeg-free.x86_64'],
                3: ['pacman', '-Q', 'ffmpeg']
            }

            for i in range(len(cmdList)):
                fetchResult = linuxFetchPackage(cmdList[i])
                if fetchResult != False:
                    if fetchResult:
                        isInstalled = True
                    packageManager = i
                    break

            if isInstalled:
                os.system('clear')
                print('Great! ffmpeg is installed!')
            elif packageManager == None:
                os.system('clear')
                print('The program doesn\'t support your package manager!')
                sys.exit()
            else:
                os.system('clear')
                print('ffmpeg isn\'t installed!')
                linuxInstallation(packageManager)
    elif system == 'Darwin': # Alias MacOS.
        try:
            subprocess.check_call(['ffmpeg', '--version'])
            os.system('clear')
            print('Great! ffmpeg is installed!')
        except:
            os.system('clear')
            print('ffmpeg isn\'t installed!')
            macosInstallation()
    else:
        print('The program doesn\'t support your operating system!')
        sys.exit()

def linuxFetchPackage(cmd):
    try:
        fetchPackage = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if fetchPackage.returncode == 0:
            return True
        return ''
    except:
        return False

def windowsInstallation():
    allowed = input(f'Do you allow the installation of ffmpeg? (y/n) ')

    if allowed.lower() == 'n':
        sys.exit()

    print('Downloading the latest version of ffmpeg..')
    downloadUrl = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
    urllib.request.urlretrieve(downloadUrl, 'ffmpeg.zip', reporthook = ffmpegDownloadProgress)

    print('\nExtracting files..')
    with zipfile.ZipFile('ffmpeg.zip', 'r') as zip:
        zip.extractall('./')

    print('Installing ffmpeg..')
    shutil.move('./ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe', './')
    shutil.rmtree('./ffmpeg-master-latest-win64-gpl')
    os.remove('./ffmpeg.zip')
    print('ffmpeg\'s installation completed! Enjoy!', end = '\n\n')

def androidInstallation():
    allowed = input(f'Do you allow the installation of ffmpeg? (y/n) ')

    if allowed.lower() == 'n':
        sys.exit()

    print('Downloading ffmpeg for Android..')
    downloadUrl = 'https://github.com/cropsly/ffmpeg-android/releases/download/v0.3.4/prebuilt-binaries.zip'
    urllib.request.urlretrieve(downloadUrl, 'ffmpeg.zip', reporthook = ffmpegDownloadProgress)
    
    print('\nExtracting files..')
    with zipfile.ZipFile('ffmpeg.zip', 'r') as zip:
        zip.extractall('./')

    print('Installing ffmpeg..')
    shutil.move('./prebuilt-binaries/armeabi-v7a-neon/ffmpeg', './')
    shutil.rmtree('./prebuilt-binaries')
    os.remove('./ffmpeg.zip')
    print('ffmpeg\'s installation completed! Enjoy!', end = '\n\n')

def ffmpegDownloadProgress(blockNum, blockSize, totalSize):
    downloadedSize = blockNum * blockSize
    percentage = downloadedSize / totalSize * 100   
    filled = int(20 * downloadedSize / totalSize)
    empty = 20 - filled
    progressBar = '[' + '█' * filled + ' ' * empty + ']'
    print(f'\rDownload\'s progress: {percentage:.0f}% {progressBar} ({downloadedSize / 1000000:.2f}MB/{totalSize / 1000000:.2f}MB).', end = '', flush = True)

def linuxInstallation(packageManager):
    allowed = input(f'Do you allow the installation of ffmpeg? (y/n) ')

    if allowed.lower() == 'n':
        sys.exit()

    if packageManager == 0:
        os.system('sudo apt install ffmpeg -y')
    elif packageManager == 1:
        os.system('sudo snap install ffmpeg')
    elif packageManager == 2:
        try:
            os.system('sudo dnf install ffmpeg-free.x86_64 -y')
        except:
            os.system('clear')
            os.system('sudo yum install ffmpeg-free.x86_64 -y')
    elif packageManager == 3:
        os.system('sudo pacman -S ffmpeg')

    print('ffmpeg\'s installation completed! Enjoy!', end = '\n\n')

def macosInstallation():
    allowed = input(f'Do you allow the installation of ffmpeg? (y/n) ')

    if allowed.lower() == 'n':
        sys.exit()

    try:
        subprocess.check_call(['brew', '--version'])
    except:
        print('The package manager "Homebrew" isn\'t installed!')
        allowed = input('Do you allow the installation of Homebrew? (y/n) ')

        if allowed.lower() == 'n':
            sys.exit()

        os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        print('Homebrew\'s installation completed!', end = '\n\n')

    print('Installing ffmpeg..')
    os.system('brew install ffmpeg')
    print('ffmpeg\'s installation completed! Enjoy!', end = '\n\n')