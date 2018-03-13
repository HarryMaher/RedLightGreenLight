#!/usr/bin/env python3
"""
Use convolutional neural networks to look at a traffic camera pointed at the
Fremont Bridge and tweet the current orientation of the Bridge--is it up or
down? or "I dunno."
"""

import tweepy
import time, datetime
import random

import label_image
# oauth_stuff keeps a cfg dict. Not shared on github. See commented out part for formatting
import oauth_stuff

def current_orientation(orientation_probs):
    print(orientation_probs)
    down_probability = orientation_probs.get("down", 0)
    up_probability = orientation_probs.get("up", 0)

    if down_probability > .97:
        state_of_bridge = "down."
    elif up_probability > .97:
        label_image.write_image()
        state_of_bridge = "up."
    elif down_probability > .5:
        label_image.write_image()
        state_of_bridge =  f"Mayybe down? I'm still learning. lol. idk!\nP={down_probability}"
    elif up_probability > .5:
        label_image.write_image()
        state_of_bridge =  f"Mayybe up? I'm still learning. lol. idk!\nP={up_probability}"
    else:
        label_image.write_image()
        #because it's likely down tbh...
        state_of_bridge = f"I'm v. confused.\nDown P={down_probability}\nUp P={up_probability}"
    return state_of_bridge

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main():
    cfg = oauth_stuff.cfg
    # Copy your own stuff here and uncomment and comment out above line if you
    # want to use your own and not put it on github.
    # cfg = {
    #     "consumer_key"        : "",
    #     "consumer_secret"     : "",
    #     "access_token"        : "",
    #     "access_token_secret" : ""
    #     }

    api = get_api(cfg)
    last_orientation = "down."

    while True:
        new_orientation = current_orientation(label_image.main())

        print(new_orientation)
        if new_orientation != last_orientation:
        
            now = datetime.datetime.now()
            tweet = new_orientation + now.strftime(" %H:%M")
            # status = api.update_status(status=tweet)
            last_orientation = new_orientation
        time.sleep(150)

if __name__ == "__main__":
    main()
