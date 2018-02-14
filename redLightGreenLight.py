import math
import requests
import urllib
import time
import os
from PIL import Image


current_state = "blah" #switch to "down" when done testing

# Function to calculate average color
def avgColor(colors):
    r=g=b=denom=0
    for i,j in colors:
        r += i*j[0]
        g += i*j[1]
        b += i*j[2]
        denom += i
    return (r/denom,g/denom,b/denom)

# Function for distance between two RGB colors
def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

while True:
    # Download Image
    jpg = urllib.request.urlretrieve('https://www.seattle.gov/trafficcams/images/Westlake_N_Dexter_NS.jpg', 'Westlake_N_Dexter_NS.jpg')[0] 

    # Load Image
    im = Image.open(jpg)
    pix = im.load()

    # Check if camera feed is available
    if len(im.crop((0,0,20,20)).getcolors(im.size[0]*im.size[1])) == 1:
        current_state = "maintenance"

    # Create list of all colors w/counts in image
    redLightColors = im.crop((370,135,380,148)).getcolors(im.size[0]*im.size[1])
    greenLightColors = im.crop((393,135,405,148)).getcolors(im.size[0]*im.size[1])

   

    # Define Black/Red/Green RGB values
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    # Test image color
    if distance(avgColor(greenLightColors),green) < distance(avgColor(greenLightColors),black) and distance(avgColor(redLightColors),black) < distance(avgColor(redLightColors),red):
        print("Bridge is down")

        #this is where the file goes.
        path = "train/"+str(time.time()).split(".")[0]+".jpg"
        if current_state != "down":
            print("STATE CHANGE TO DOWN - THIS IS WHERE WE'D TWEET!")
            with open(jpg, 'rb') as f:
                data = f.read()
            with open(path, 'wb') as f:
                f.write(data)
            current_state = "down"
    elif distance(avgColor(redLightColors),red) < distance(avgColor(redLightColors),black) and distance(avgColor(greenLightColors),black) < distance(avgColor(greenLightColors),green):
        print("Bridge is up")
        if current_state != "up":
            print("STATE CHANGE TO UP! - THIS IS WHERE WE'D TWEET")
            with open(jpg, 'rb') as f:
                data = f.read()
            with open("down_"+path, 'wb') as f:
                f.write(data)
            current_state = "up"
    else:
        print("I am experiencing a temporary episode of colorblindness")

        # Following section of code for debugging
        print("Red Light: " + str(avgColor(redLightColors)))
        print("Dist RL to Red: " + str(distance(avgColor(redLightColors),red)))
        print("Dist RL to Black: " + str(distance(avgColor(redLightColors),black)))
        print("Green Light: " + str(avgColor(greenLightColors)))
        print("Dist GL to Green: " + str(distance(avgColor(greenLightColors),red)))
        print("Dist GL to Black: " + str(distance(avgColor(greenLightColors),black)))
    

    time.sleep(60)
