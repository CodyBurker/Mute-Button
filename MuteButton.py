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

# Subprocess to check for button press, then toggle mute.
def get_button(ser):
    while ser.is_open:
        try:
            x = ser.readline()
            toggle_mute()
            print("\t\t\tToggle Mute")
        except:
            ser.close()
            print("Button Disconnected")  

# Function to send code to toggle LED from Arduino
def light_on(light_on_var, ser):
    try:
        if light_on_var == True:
            ser.write(b"off")
        else:
            ser.write(b"on")
    except:
        print("\t\t\tError changing light.")
        ser.close()

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
        while ser.is_open:
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
                            try:
                                light_on(not am_muted, ser)
                            except: 
                                is_connected=False
                                print('\t\t\tDisconnected from button!')
                        am_muted = am_muted_latest
                    except:
                        print("\t\tError getting mute stats")
                else: 
                    print("\tNo meeting detected. Checking again in 3s")
                    if am_muted == False:
                        am_muted = False
                        light_on(not am_muted, ser)
                    serial.tools.list_ports_windows
                    time.sleep(3)
            except:
                print("\tError getting Zoom meeting")
    except: 
        print("No device. Attempting reconnect in 10 seconds.")
        time.sleep(10)