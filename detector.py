import time
from google.cloud import vision
import io
import os
import cv2
from autoPicture import main
import subprocess
from arduino.pyduino import trigger

"""
NOTE: Image1 holds the parkingID = 1
      Image2 holds the parkingID = 2,3
"""

# function that reads image1
def readImage1():
    licensePlate = detect_text(os.path.join("images", "image1.jpg"))
    licensePlate = licensePlate.split('\n')
    print(licensePlate)

    lst = [lp for lp in licensePlate if (lp.isupper() and len(lp) == 7)]

    parkingID = 1
    if len(lst) == 1:
        return lst[0].replace(" ",""), parkingID
    else:
        licensePlate = ""
        return licensePlate,parkingID


# function that reads image2, this is composed of two subimages
def readImage2():
    # Read the text
    licensePlates = detect_text(os.path.join("images","image2.jpg"))
    licensePlates = licensePlates.split('\n')

    lst = [lp for lp in licensePlates if (lp.isupper() and len(lp) == 7) or lp == "SON"]

    print(lst)

    if len(lst) == 1 and lst[0] != "SON":
        licensePlate3 = lst[0].replace(" ","")
        licensePlate2 = ""
    elif len(lst) == 2 and lst[0] == "SON":
        licensePlate2 = lst[1].replace(" ","")
        licensePlate3 = ""
    elif len(lst) == 2 and lst[0] != "SON":
        licensePlate2 = lst[1].replace(" ","")
        licensePlate3 = lst[0].replace(" ","")
    elif len(lst) == 1 and lst[0] == "SON":
        licensePlate2 = ""
        licensePlate3 = ""
    else:
        licensePlate2 = ""
        licensePlate3 = ""

    parkingID2 = 2
    parkingID3 = 3


    return licensePlate2,parkingID2,licensePlate3,parkingID3



"""Detects text in the file."""
def detect_text(image):
    try:
        client = vision.ImageAnnotatorClient()

        with io.open(image, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        return texts[0].description.strip()
    except Exception as e:
        print(e)
        return ""

# our pipeline
def computerVisionPipeline():

    # First we caputure the photos using the phones
    main(1)

    time.sleep(4)

    # Now we read the images
    licensePlate1,parkingID1 = readImage1()
    licensePlate2,parkingID2,licensePlate3,parkingID3 = readImage2()

    # trigger arduino simulation accordingly
    if licensePlate1 == "":
        # Turn on
        trigger(1)
    else:
        # Turn off, Occupied
        trigger(0)

    time.sleep(1)

    if licensePlate2 == "":
        # Turn on
        trigger(3)
    else:
        # Turn off, Occupied
        trigger(2)

    time.sleep(1)

    if licensePlate3 == "":
        # Turn on
        trigger(5)
    else:
        # Turn off, Occupied
        trigger(4)

    time.sleep(1)

    # Send the requests to flask server
    host = '132.205.229.124'
    command = f'curl -s {host}:8080/updateParkingSpot?licensePlate={licensePlate1}&parkingID={parkingID1}'
    command2 = f'curl -s {host}:8080/updateParkingSpot?licensePlate={licensePlate2}&parkingID={parkingID2}'
    command3 = f'curl -s {host}:8080/updateParkingSpot?licensePlate={licensePlate3}&parkingID={parkingID3}'

    subprocess.call(command, shell=True)
    subprocess.call(command2, shell=True)
    subprocess.call(command3, shell=True)


if __name__ == '__main__':
    while(True):
        computerVisionPipeline()
        # perform the function every 5 seconds
        time.sleep(2)
