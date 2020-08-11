## pip install  pynput
# Py User Input Library
# pip install uiautomation
from pynput.keyboard import Key, Listener, Controller as keyboard_controller
import time
import serial
import getZoomStatus
import threading

# Function to toggle mute via keyboard emulation
def toggle_mute():
    # Bring Zoom to focus
    # Press shift, alt, control:
    with keyboard.pressed(Key.shift):
        with keyboard.pressed(Key.alt):
            keyboard.press(Key.ctrl)
            keyboard.release(Key.ctrl)
    time.sleep(0.05)
    # alt+a to toggle mute
    with keyboard.pressed(Key.alt):
        keyboard.press("a")
        keyboard.release("a")

# Helper function to print from within subprocess
def pt(status):
    print(status)


# Subprocess to check for button press, then toggle mute.
def get_button(ser):
    while True:
        x = ser.readline()
        toggle_mute()
        print(x)

# Function to send code to toggle LED from Arduino
def light_on(light_on_var, ser):
    try:
        if light_on_var == True:
            ser.write(b"off")
        else:
            ser.write(b"on")
    except: 
        pt("Error")

# Variable for keyboard controller
keyboard = keyboard_controller()


# Variable to keep track of mute status
am_muted = True
# Loop to keep running in background:
while True:
    try:
        print("Trying Serial Connection:")
        # Set up serial connection
        ser = serial.Serial(port="COM4")
        print("Successful Serial Connection")
        # Set up multithreading
        thread = threading.Thread(target=get_button, args=(ser,))
        # Start background thread to keep track of button presses
        thread.start()
        # Loop to sync light status
        while True:
            # Check whether a meeting is open on the computer:
            try: 
                if getZoomStatus.DetectZoomMeeting():
                    # If there is a meeting, check whether I am muted or not:
                    print("\tMeeting detected")
                    try:
                        am_muted_latest = "zoomMute:muted" in getZoomStatus.GetZoomStatus()
                        # pt("Latest:" +  am_muted_latest)
                        if am_muted != am_muted_latest:
                            print("\t\tGot mute status")
                            # pt("Changed:" + am_muted_latest)
                            light_on(not am_muted, ser)
                        am_muted = am_muted_latest
                    except:
                        print("\t\tError getting mute stats")
            except:
                print("\tError getting Zoom meeting")
    except: 
        print("No device. Attempting reconnect in 10 seconds.")
        time.sleep(10)