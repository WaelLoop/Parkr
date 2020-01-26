import os
import subprocess
from threading import Thread

# Function that captures an image once the camera has been open
def capture(deviceID):
    takePicture = 'adb -s %s shell \"input keyevent 27\"' % deviceID
    os.system(takePicture)

# Function that loads a picture from the phone to the computer
def pullPicture(deviceID, sleepTime):
    #OnePlus Command
    if(deviceID == "9b28cb0d"):
        os.system('sleep %d' % sleepTime)
        os.system('adb -s %s shell mv /sdcard/DCIM/Camera/IMG_20200126* /sdcard/DCIM/Camera/image1.jpg' % (deviceID))
        os.system('adb -s %s pull /sdcard/DCIM/Camera/image1.jpg %s' % (deviceID, os.path.abspath("images")))
        os.system('adb -s %s shell rm /sdcard/DCIM/Camera/image1.jpg' % (deviceID))
    #LG Command
    else :
        os.system('sleep %d' % sleepTime)
        subprocess.call('adb -s %s shell mv /sdcard/DCIM/Camera/20200126* /sdcard/DCIM/Camera/image2.jpg' % deviceID,shell=True)
        subprocess.call('adb -s %s pull /sdcard/DCIM/Camera/image2.jpg %s' % (deviceID, os.path.abspath("images")), shell=True)
        subprocess.call('adb -s %s shell rm /sdcard/DCIM/Camera/image2.jpg' % deviceID,shell=True)

# our pipeline
def autoPicturePipeline(sleepTimer,deviceID):
    # take a picture
    capture(deviceID)

    #pull the image from phone to computer
    pullPicture(deviceID,sleepTimer)

# main method
def main(sleepTimer=5):
    # devices IDs
    onePlus = "9b28cb0d"
    samsung = "R58M246LLTA"

    thread1 = Thread(target=autoPicturePipeline, args=(sleepTimer, onePlus))
    thread2 = Thread(target=autoPicturePipeline, args=(sleepTimer, samsung))

    # start the threads
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    main()