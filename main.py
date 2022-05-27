
"""
Date Created: May 27th 2022
Author: Abhimanyu Sangitrao
Purpose: This is a hands-on project as a part of Programming tutorials by CodeWithHarry Youtube Channel by the name of 
         'Python Progrmming for absolute beginners in Hindi'
"""
# ------------------------------------------ Imports ------------------------------------------------------#
import tkinter #inuilt module to build a GUI in python
import PIL.Image, PIL.ImageTk #pillow module being used to work around with images
import cv2 # opencv-python module to work with images
from functools import partial
import threading
import imutils
import time
# ------------------------------------------ Imports Ends ------------------------------------------------------#

# Setting the dimensions of the main GUI screen
SET_WIDTH = 650
SET_HEIGHT = 368

# define a video stream from which the video shall be played in the program
stream = cv2.VideoCapture('./img/clip.mp4')

# ------------------------------------------------ Action Functions ----------------------------------------------- #
def play(speed):
    '''
    This function is used just to play a video clip at a particular speed along with some text
    '''
    print("You clicked on Play!")
    print(f"speed is: {speed}")
    
    # change the speed of the video clip as per user input
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES) # get the current frame number of the clip being displayed
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed) 
    # getting video stream using opencv
    # grabbed - boolean to tell whether you have taken the stream correctly or not, frame - frame number read from the stream
    grabbed, frame = stream.read()
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) #an array
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # Adding a Text showing 'Decision Pending..' for more real effect
    canvas.create_text(132,24,fill='white',font='Times 24 bold',text='Decision Pending..')

def out():
    '''
    This function gives a decision if the player is out as declared by the Third Umpire.
    '''
    # Creating a separate thread so that the main program continues to run and the GUI does not get hanged
    thread = threading.Thread(target=pending,args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    '''
    This function gives a decision if the player is not-out as declared by the Third Umpire.
    '''
    # Creating a separate thread so that the main program continues to run and the GUI does not get hanged
    thread = threading.Thread(target=pending,args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is Not Out")


def pending(decision):
    '''
    This function runs for both cases if the player is out/not-out as declared by the Third Umpire and displays the 
    result accordingly on the GUI along with the image of the Sponsor.
    '''
    # 1. Display decision pending image
    frame = cv2.cvtColor(src=cv2.imread("./img/pending.png"), code=cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) # Resize the image in case it has some other dimensions
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 2. Wait for 1 second
    time.sleep(1)
    # 3. Display sponsor image
    frame = cv2.cvtColor(src=cv2.imread("./img/sponsor.png"), code=cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) # Resize the image in case it has some other dimensions
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 4. Wait for 1.5 second
    time.sleep(1.5)
    # 5. Display Out/Not Out
    if decision == 'out':
        decisionImg = './img/out.png'
    else:
        decisionImg = './img/not_out.png'
    frame = cv2.cvtColor(src=cv2.imread(decisionImg), code=cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) # Resize the image in case it has some other dimensions
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 6. Wait for 1.5 second
    time.sleep(1.5)

# -------------------------------------------------- Action Functions ends --------------------------------------- #

# build a main window of tkinter GUI
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")

# Creating a plain canvas to add buttons and images
canvas = tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)

# Adding an image to the GUI using pillow and opencv modules
cv_img = cv2.cvtColor(src=cv2.imread("./img/welcome.png"), code=cv2.COLOR_BGR2RGB) # converted the image color code from BGR to RGB using opencv
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

# packing the above image to canvas with a specified position
# without this step, the image(photo) won't get displayed in the GUI window
image_on_canvas = canvas.create_image(0,0,anchor=tkinter.NW,image=photo)
canvas.pack()

# Adding Buttons to control playback
#  > In order to add an action to the button, use the 'command' argument and define the action in a python function
#  > In order to pass arguments to the action function, use the 'partial' function from functools module
btn = tkinter.Button(window, text='<< Previous (fast)',width=50, command=partial(play,-25))
btn.pack()

btn = tkinter.Button(window, text='<< Previous (Slow)',width=50,command=partial(play,-2))
btn.pack()

btn = tkinter.Button(window, text='>> Next (Slow)',width=50,command=partial(play,2))
btn.pack()

btn = tkinter.Button(window, text='>> Next (fast)',width=50, command=partial(play,25)) #used partial from functools
btn.pack()

btn = tkinter.Button(window, text='Give Out',width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text='Give Not Out',width=50, command=not_out)
btn.pack()
# ----------------------------------------------------------------------------------------------------------------------------- #

# Run the app (GUI)
window.mainloop()
