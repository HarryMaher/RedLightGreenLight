# FreBotBridge

##### *What?*
A Twitter bot that uses convolutional neural networks to look at the Fremont Bridge *through the lens* of a local traffic camera and tweet the up-to-the-minute orientation of the Fremont Bridge. Is it up or down?

##### *Who?*
The Fremont Bridge. In Seattle.

##### *Why?*
*not. Why not.

##### *When?*
Always. As long as there's a bridge.

##### *Where?*
In Fremont, Seattle. At the bridge. The Fremont Bridge.\
See: [@BridgeInFremont](https://twitter.com/BridgeInFremont)
<br><br><br>
##### *Misc info*

redLightGreenLight.py downloads and attempts to categorize images of the bridge up or down by comparing pixels in the image that map to the red light's location to pixels in the green light's location. Unfortunately the camera moves around and I can't control it. So it categorizes many things as unknown and then you have to manually categorize images. This is all to build a training set. 

With the training set, follow this tutorial: [https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/)

label_image.py returns a dict with keys as "up" and "down" and values being probabilities of the two orientations. It uses both retrained_ files and tensorflow

tweet_bridge_orientation.py looks at resulting classified image and tweets the orientaiton if it has changed. Re-checks every 150 seconds.
