import os
from threading import Thread

# Function that captures an image once the camera has been open
def capture(deviceID):
    takePicture = 'adb -s %s shell \"input keyevent 27\"' % deviceID
    os.system(takePicture)

# Function that loads a picture from the phone to the computer
def pullPicture(deviceID, sleepTime):
    if(deviceID == "9b28cb0d"):
        index = 1
    else:
        index = 2
    os.system('sleep %d' % sleepTime)
    os.system('adb -s %s shell mv /sdcard/DCIM/Camera/IMG_20200125*.jpg /sdcard/DCIM/Camera/image%d.jpg' % (deviceID,index))
    os.system('adb -s %s pull /sdcard/DCIM/Camera/image%d.jpg %s' % (deviceID,index,os.path.abspath("images")))
    os.system('adb -s %s shell rm /sdcard/DCIM/Camera/image%d.jpg' % (deviceID,index))

# our pipeline
def autoPicturePipeline(sleepTimer,deviceID):
    # take a picture
    capture(deviceID)

    #pull the image from phone to computer
    pullPicture(deviceID,sleepTimer)

# main method
def main(sleepTimer=1):
    # devices IDs
    onePlus = "9b28cb0d"
    LG = "LGM470309ce442"

    thread1 = Thread(target=autoPicturePipeline, args=(sleepTimer, onePlus))
    thread2 = Thread(target=autoPicturePipeline, args=(sleepTimer, LG))

    # start the threads
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    main()