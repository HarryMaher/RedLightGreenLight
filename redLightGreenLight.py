#!/usr/bin/env python3
"""
Current version of the script saves pictures of the bridge in current orientations 
"""
import urllib.request
import time
from PIL import Image


current_state = "blah"  

# Function to calculate average color
def avgColor(colors):
    r = g = b = denom = 0
    for i, j in colors:
        r += i*j[0]
        g += i*j[1]
        b += i*j[2]
        denom += i
    return (r/denom, g/denom, b/denom)

# Writes jpg to "path" file ("up/", "down/", 
# or "unknown/") in the training folder.
def filewrite(path):
    with open(jpg, 'rb') as f:
        data = f.read()
    with open("train/"+path+str(time.time()).split(".")[0]+".jpg", 'wb') as f:
        f.write(data) 

while True:
    # Download Image
    jpg = urllib.request.urlretrieve('https://www.seattle.gov/trafficcams/images/Westlake_N_Dexter_NS.jpg', 'Westlake_N_Dexter_NS.jpg')[0] 

    # Load Image
    im = Image.open(jpg)
    pix = im.load()

    # Check if camera feed is available
    if len(im.crop((0, 0, 20, 20)).getcolors(im.size[0]*im.size[1])) == 1:
        current_state = "maintenance"
        time.sleep(60)
        continue

    # Create list of all colors w/counts in image
    green_light_center = (479, 125) # Change this to center of green stoplight when camera moves
    red_light_center = (460, 125) # Same, but for red light, should just change x

    green_light_colors = im.crop(((green_light_center[0]-3),(green_light_center[1]-3),(green_light_center[0]+3),(green_light_center[1]+3))).getcolors(im.size[0]*im.size[1])
    red_light_colors = im.crop(((red_light_center[0]-3),(red_light_center[1]-3),(red_light_center[0]+3),(red_light_center[1]+3))).getcolors(im.size[0]*im.size[1])
   
    printout = "avgredlight color red:", avgColor(red_light_colors)[0], "avggreenlight color green:", avgColor(green_light_colors)[1]

    if (avgColor(green_light_colors)[1] > 200) and (avgColor(red_light_colors)[0] < avgColor(green_light_colors)[1]):
        print("Bridge is down\n", printout)
        if current_state != "down":
            print("STATE CHANGE TO DOWN - THIS IS WHERE WE'D TWEET!")  # Tweet[eventually] if state has changed   
            filewrite("down/")
            current_state = "down"

    elif (avgColor(red_light_colors)[0] > 200) and (avgColor(red_light_colors)[0] > avgColor(green_light_colors)[1]):
        print("Bridge is up\n", printout)
        filewrite("up/")     
        if current_state != "up":
            print("STATE CHANGE TO UP! - THIS IS WHERE WE'D TWEET")
            current_state = "up"
            
    else:    
        print("wat\n", printout)
        filewrite("unknown/")

    time.sleep(150)
    