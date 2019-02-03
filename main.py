# Import openCV and Numpy Libraries
import cv2
import numpy as np

# Import Google Text-To-Speech API
from gtts import gTTS
import os

print ('Generating MP3 files and setting up image configurations...')

# Configuration of Text to Speech Specifications
language = 'en'
redString = 'The color is red'
yellowString = 'The color is yellow'
greenString = 'The color is green'

# Creation of mp3 files for speech
# Passing the language and test to the engine
redObject = gTTS(text=redString, lang=language, slow=False)
redObject.save("red.mp3")
yellowObject = gTTS(text=yellowString, lang=language, slow=False)
yellowObject.save("yellow.mp3")
greenObject = gTTS(text=greenString, lang=language, slow=False)
greenObject.save("green.mp3")

# Create a color null color variable
color = None

# Specify text formatting for OpenCV window
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (100,450)
fontScale = 1
fontColor = (255,255,255)
lineType = 2

'''
# Google Initialization
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.types.SynthesisInput(text="Hello, World!")
'''

# Start Video Capture
cap = cv2.VideoCapture(0)

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

    # Smoothen the image with a Gaussian blur
    frameBlur = cv2.GaussianBlur(frame, (5,5),0)

    # Convert raw image data to HSV
    hsv = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2HSV)

    # Apply colored-mask for each color
    red_image_mask = cv2.inRange(hsv, lowerBoundDict['red'], higherBoundDict['red'])
    yellow_image_mask = cv2.inRange(hsv, lowerBoundDict['yellow'], higherBoundDict['yellow'])
    green_image_mask = cv2.inRange(hsv, lowerBoundDict['green'], higherBoundDict['green'])

    # Add bitwise functionality
    red_res = cv2.bitwise_and(frameBlur,frameBlur, mask=red_image_mask)
    yellow_res = cv2.bitwise_and(frameBlur,frameBlur, mask=yellow_image_mask)
    green_res = cv2.bitwise_and(frameBlur,frameBlur, mask=green_image_mask)

    # Convert colored-images to grayscale
    redToGray = cv2.cvtColor(red_res, cv2.COLOR_BGR2GRAY)
    yellowToGray = cv2.cvtColor(yellow_res, cv2.COLOR_BGR2GRAY)
    greenToGray = cv2.cvtColor(green_res, cv2.COLOR_BGR2GRAY)

    # Resize the image to a smaller size
    #resizedFrame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    resizedRed = cv2.resize(redToGray, (0,0), fx=0.5, fy=0.5)
    resizedYellow = cv2.resize(yellowToGray, (0,0), fx=0.5, fy=0.5)
    resizedGreen = cv2.resize(greenToGray, (0,0), fx=0.5, fy=0.5)

    # Display current color on the screen
    cv2.putText(frame, 'Current Color is: {}'.format(color), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

    # Display windows
    cv2.imshow('Raw Frame',frame)
    cv2.imshow('Red Mask', resizedRed)
    cv2.imshow('Yellow Mask', resizedYellow)
    cv2.imshow('Green Mask', resizedGreen)

    # Count the the total number of red, yellow, and green pixels
    redPixelCount = cv2.countNonZero(redToGray)
    yellowPixelCount = cv2.countNonZero(yellowToGray)
    greenPixelCount = cv2.countNonZero(greenToGray)

    # Determine strongest color
    if (redPixelCount > yellowPixelCount) and (redPixelCount > greenPixelCount):
        currentColor = 'Red'
        if currentColor != color:
            color = 'Red'
            print ('the Color is Red')

            # Opens generated mp3 file and plays audio
            os.system('red.mp3')

    elif (yellowPixelCount > redPixelCount) and (yellowPixelCount > greenPixelCount):
        currentColor = 'Yellow'
        if currentColor != color:
            color = 'Yellow'
            print ('the Color is Yellow')

            # Opens generated mp3 file and plays audio
            os.system('yellow.mp3')

    elif (greenPixelCount > redPixelCount) and (greenPixelCount > yellowPixelCount):
        currentColor = 'Green'
        if currentColor != color:
            color = 'Green'
            print ('the Color is Green')

            # Opens generated mp3 file and plays audio
            os.system('green.mp3')
            
    else:
        currentColor = None
        if currentColor != color:
            color = None
            print ('the Color is None')

    # Stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop camera capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
