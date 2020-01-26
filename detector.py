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
    licensePlate = detect_text(os.path.join("images","image11.jpeg"))
    parkingID = 1

    return licensePlate, parkingID


# function that reads image2, this is composed of two subimages
def readImage2():
    img = cv2.imread(os.path.join("images","image2.jpeg"))
    row, col, _ = img.shape
    # integer division
    newCol = col//2

    # split the image into two
    subImage2 = img[:newCol,:]
    parkingID2 = 2

    subImage3 = img[newCol:,:]
    parkingID3 = 3

    # Write the new sub-images
    cv2.imwrite(os.path.join("images","image2.jpeg"),subImage2)
    cv2.imwrite(os.path.join("images","image3.jpeg"),subImage3)

    # Read the text
    licensePlate2 = detect_text(os.path.join("images","image2.jpeg"))
    licensePlate3 = detect_text(os.path.join("images","image3.jpeg"))

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
    except:
        return ""

# our pipeline
def computerVisionPipeline():

    # First we caputure the photos using the phones
    main(1)

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

    if licensePlate2 == "":
        # Turn on
        trigger(3)
    else:
        # Turn off, Occupied
        trigger(2)

    if licensePlate3 == "":
        # Turn on
        trigger(5)
    else:
        # Turn off, Occupied
        trigger(4)

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
        time.sleep(5)