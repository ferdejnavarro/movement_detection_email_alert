# Movement Detection App

### About
This app allows you to detect movement by using your computer's camera. When
movement is detected, the app captures the frame where the "culprit" is found,
then the image is sent to a desired email account alongside a custom message
including the date and time it happened. The app saves the frames inside the 
'images' folder, which will be deleted once the app is closed.

### How to use
In order to use this app, you must generate an app password in your gmail 
account and enter it in the 'PASSWORD' variable inside 'send_email.py'. 

In the same .py file, you must specify the sender (the same Gmail 
account you generated the app password for) and the receiver, which can any 
desired Gmail account. You must enter both accounts in the SENDER and 
RECEIVER variables respectively.

Your email password is NOT your app password.

To turn off the app, you need to press the 'C' key.
