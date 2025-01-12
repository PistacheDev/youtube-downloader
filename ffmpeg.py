import os
import subprocess
import urllib.request
import zipfile
import shutil
import sys

def checkInstallation(system): # Check if ffmpeg is installed.
    if system == "Windows":
        if not os.path.isfile("./ffmpeg.exe"): # Check if any "ffmpeg.exe" file is available.
            print("ffmpeg isn't installed!")
            windowsInstallation()
    elif system == "Linux":
        if os.path.exists("/system/build.prop"): # Android devices.
            if not os.path.isfile("./ffmpeg"): # Check if any "ffmpeg" is available.
                print("ffmpeg isn't installed!")
                androidInstallation()
        else:
            packageManager = None
            installed = False

            # Supported linux package managers.
            cmd = {
                0: ["dpkg", "-s", "ffmpeg"],
                1: ["rpm", "-q", "ffmpeg-free.x86_64"],
                2: ["pacman", "-Qi", "ffmpeg"],
                3: ["snap", "list", "ffmpeg"]
            }

            for i in range(len(cmd)):
                fetchResult = linuxFetchPackage(cmd[i])
                if fetchResult != False:
                    packageManager = i;
                    if fetchResult != "":
                        installed = True
                    break

            os.system("clear")

            if packageManager == None:
                # To add your package manager, you can edit the code and send a pull request to https://github.com/PistacheDev/youtube-downloader.
                # Or join the Discord server https://discord.com/invite/RkB3ZQsmGV to request an update.
                print("The program doesn't support your package manager!")
                input("Press [Enter] to close the program..")
                sys.exit()
            elif not installed:
                print("ffmpeg isn't installed!")
                linuxInstallation(packageManager)
    elif system == "Darwin": # Alias MacOS.
        try:
            subprocess.check_call(["ffmpeg", "--version"])
            os.system("clear")
        except:
            os.system("clear")
            print("ffmpeg isn't installed!")
            macosInstallation()
    else:
        # To add your OS, you can edit the code and send a pull request to https://github.com/PistacheDev/youtube-downloader.
        # Or join the Discord server https://discord.com/invite/RkB3ZQsmGV to request an update.
        print("The program doesn't support your operating system!")
        sys.exit()


def linuxFetchPackage(cmd):
    try:
        fetch = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE) # Try to use the package manager.
        if fetch.returncode == 0: return True
        return ""
    except: return False


def windowsInstallation():
    allowed = input(f"Do you allow the installation of ffmpeg? (y/n) ")
    if allowed.lower() == "n": sys.exit()
    print("Downloading the latest version of ffmpeg..")
    urllib.request.urlretrieve("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip", "ffmpeg.zip", reporthook = downloadProgress) # Download the zip file.
    print("\nInstalling ffmpeg..")
    with zipfile.ZipFile("ffmpeg.zip", "r") as zip: zip.extractall("./") # Extract the files.
    shutil.move("./ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe", "./") # Extract the ffmpeg.exe file.
    shutil.rmtree("./ffmpeg-master-latest-win64-gpl") # Delete the other files.
    os.remove("./ffmpeg.zip") # Delete the zip file.
    print("ffmpeg's installation completed! Enjoy!", end = "\n\n")


def androidInstallation():
    allowed = input(f"Do you allow the installation of ffmpeg? (y/n) ")
    if allowed.lower() == "n": sys.exit()
    print("Downloading ffmpeg for Android..")
    urllib.request.urlretrieve("https://github.com/cropsly/ffmpeg-android/releases/download/v0.3.4/prebuilt-binaries.zip", "ffmpeg.zip", reporthook = downloadProgress) # Download the zip file.
    print("\nInstalling ffmpeg..")
    with zipfile.ZipFile("ffmpeg.zip", "r") as zip: zip.extractall("./") # Extract the files.
    shutil.move("./prebuilt-binaries/armeabi-v7a-neon/ffmpeg", "./") # Extract the ffmpeg file.
    shutil.rmtree("./prebuilt-binaries") # Delete the other files.
    os.remove("./ffmpeg.zip") # Delete the zip file.
    print("ffmpeg's installation completed! Enjoy!", end = "\n\n")


def downloadProgress(blockNum, blockSize, totalSize):
    downloaded = blockNum * blockSize
    percentage = downloaded / totalSize * 100   
    filled = int(20 * downloaded / totalSize)
    empty = 20 - filled
    bar = "[" + "█" * filled + " " * empty + "]"
    print(f"\rDownload's progress: {percentage:.0f}% {bar} ({downloaded / 1000000:.2f}MB/{totalSize / 1000000:.2f}MB).", end = "", flush = True)


def linuxInstallation(packageManager):
    allowed = input(f"Do you allow the installation of ffmpeg? (y/n) ")
    if allowed.lower() == "n": sys.exit()

    if packageManager == 0: os.system("sudo apt install ffmpeg -y")
    elif packageManager == 1:
        try:
            os.system("sudo dnf install ffmpeg-free.x86_64 -y")
        except: # If the dnf command failed, we're trying with yum.
            os.system("clear")
            os.system("sudo yum install ffmpeg-free.x86_64 -y")
    elif packageManager == 2: os.system("sudo pacman -Syu ffmpeg")
    elif packageManager == 3: os.system("sudo snap install ffmpeg")
    print("ffmpeg's installation completed! Enjoy!", end = "\n\n")


def macosInstallation():
    allowed = input(f"Do you allow the installation of ffmpeg? (y/n) ")
    if allowed.lower() == "n": sys.exit()

    try:
        subprocess.check_call(["brew", "--version"]) # Check if Homebrew is installed.
    except:
        print("The package manager \"Homebrew\" isn't installed!")
        allowed = input("Do you allow the installation of Homebrew? (y/n) ")
        if allowed.lower() == "n": sys.exit()
        os.system("/bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'") # Install Homebrew from GitHub.
        print("Homebrew's installation completed!", end = "\n\n")

    print("Installing ffmpeg..")
    os.system("brew install ffmpeg")
    print("ffmpeg's installation completed! Enjoy!", end = "\n\n")