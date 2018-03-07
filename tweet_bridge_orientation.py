#!/usr/bin/env python3
"""
Use convolutional neural networks to look at a traffic camera pointed at the
Fremont Bridge and tweet the current orientation of the Bridge--is it up or
down? or "I dunno."
"""

import tweepy
import time

import label_image
# This keeps a cfg dict containing configs for oauth. Not shared on github.
import oauth_stuff

def current_orientation(orientation_probs):
    if orientation_probs.get("down", 0) > .94:
        return "down."
    # I'm not sure how accurate it is in the up, so setting it low for now.
    elif orientation_probs.get("up", 0) > .75:
        return "up."
    else:
        return "I dunno."


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
        orientation_probs = label_image.main()
        new_orientation = current_orientation(orientation_probs)

        print(new_orientation)
        if new_orientation != last_orientation:
            status = api.update_status(status=new_orientation)
            last_orientation = new_orientation
        time.sleep(150)

if __name__ == "__main__":
    main()
