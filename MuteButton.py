## pip install  pynput
#Py User Input Library
# pip install uiautomation
from pynput.keyboard import Key, Listener, Controller as keyboard_controller
import time
import serial
import getZoomStatus
import threading
keyboard = keyboard_controller()

def toggle_mute():
    # Bring Zoom to focus
    # Press shift, alt, control:
    with keyboard.pressed(Key.shift):
        with keyboard.pressed(Key.alt):
            keyboard.press(Key.ctrl)
            keyboard.release(Key.ctrl)
    time.sleep(.05)
    # alt+a to toggle mute
    with keyboard.pressed(Key.alt):
        keyboard.press('a')
        keyboard.release('a')

ser = serial.Serial(port='COM4')

def pt(status):
    print(status)

def sync_status(ser):
    import uiautomation
    while True:
        if(getZoomStatus.DetectZoomMeeting()):
            pt("Meeting detected")
            status=getZoomStatus.GetZoomStatus()
            if("zoomMute:muted" in status):
                pt("Muted")
                ser.write(b'off')
            else:
                pt("Unmuted")
                ser.write(b'on')

thread = threading.Thread(target=sync_status, args=(ser,))
thread.start()

while (True):
    ser.readline()
    toggle_mute()
    print("ToggleMute")