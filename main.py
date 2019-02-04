# Import openCV and Numpy Libraries
import cv2
import numpy as np

#importing google text to speech api
from gtts import gTTS
import os

# Start Video Capture
cap = cv2.VideoCapture(0)
# Language in which you want to convert
language = 'en'
#variables for speech
str_red = 'the Color is Red'
str_yellow = 'the Color is Yellow'
str_green = 'the Color is Green'

#creating mp3 files for speech
#passing the text and lanuguage to the engine
#slow=False to tell the module that the converted audio should have high speed
redobj = gTTS(text=str_red, lang=language, slow=False)
redobj.save("red.mp3")

yellowobj = gTTS(text=str_yellow, lang=language, slow=False)
yellowobj.save("yellow.mp3")

greenobj = gTTS(text=str_green, lang=language, slow=False)
greenobj.save("green.mp3")

color = None


# Indefinitely initiate Video Stream
while(True):
    # Read each frame from the camera
    ret, frame = cap.read()

    # Define colors and their lower and higher bounds
    # borrowed from https://pastebin.com/WVhfmphS
    lowerBoundDict     = {'red'    : (166, 84,141),
                          'yellow' : ( 23, 59,119),
                          'green'  : ( 66,122,129)}

    higherBoundDict    = {'red'    : (186,255,255),
                          'yellow' : ( 54,255,255),
                          'green'  : ( 86,255,255)}

    standardColorsDict = {'red'    : (  0,  0,255),
                          'yellow' : (  0,255,217),
                          'green'  : (  0,255,  0)}

    # Convert raw image data to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply colored-mask for each color
    red_image_mask = cv2.inRange(hsv, lowerBoundDict['red'], higherBoundDict['red'])
    yellow_image_mask = cv2.inRange(hsv, lowerBoundDict['yellow'], higherBoundDict['yellow'])
    green_image_mask = cv2.inRange(hsv, lowerBoundDict['green'], higherBoundDict['green'])

    # Add bitwise functionality
    red_res = cv2.bitwise_and(frame,frame, mask=red_image_mask)
    yellow_res = cv2.bitwise_and(frame,frame, mask=yellow_image_mask)
    green_res = cv2.bitwise_and(frame,frame, mask=green_image_mask)

    # Convert colored-images to grayscale
    redToGray = cv2.cvtColor(red_res, cv2.COLOR_BGR2GRAY)
    yellowToGray = cv2.cvtColor(yellow_res, cv2.COLOR_BGR2GRAY)
    greenToGray = cv2.cvtColor(green_res, cv2.COLOR_BGR2GRAY)

    # Resize the image to a smaller size
    resizedFrame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    resizedRed = cv2.resize(redToGray, (0,0), fx=0.5, fy=0.5)
    resizedYellow = cv2.resize(yellowToGray, (0,0), fx=0.5, fy=0.5)
    resizedGreen = cv2.resize(greenToGray, (0,0), fx=0.5, fy=0.5)

    # Display windows
    cv2.imshow('frame',resizedFrame)
    cv2.imshow('red', resizedRed)
    cv2.imshow('yellow', resizedYellow)
    cv2.imshow('green', resizedGreen)

    # Count the the total number of red, yellow, and green pixels
    redPixelCount = cv2.countNonZero(redToGray)
    yellowPixelCount = cv2.countNonZero(yellowToGray)
    greenPixelCount = cv2.countNonZero(greenToGray)

    # Determine strongest color
    # Say the color out loud

    if (redPixelCount > yellowPixelCount) and (redPixelCount > greenPixelCount):
        currentColor = 'Red'
        if currentColor != color:
            color = 'Red'

            str_red = 'the Color is Red'
            print (str_red)

            #opens mp3 file (w/default) and plays audio
            os.system("red.mp3")

    elif (yellowPixelCount > redPixelCount) and (yellowPixelCount > greenPixelCount):
        currentColor = 'Yellow'
        if currentColor != color:
            color = 'Yellow'
            #cplor = yellow
            print (str_yellow)

            #opens mp3 file (w/default) and plays audio
            os.system("yellow.mp3")
    elif (greenPixelCount > redPixelCount) and (greenPixelCount > yellowPixelCount):
        currentColor = 'Green'
        if currentColor != color:
            color = 'Green'
            #color = green
            print (str_green)

            #opens mp3 file (w/default) and plays audio
            os.system("green.mp3")
    else:
        print ('No Conclusion')



    # Stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop camera capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
