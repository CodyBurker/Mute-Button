## pip install  pynput
# Py User Input Library
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
    time.sleep(0.05)
    # alt+a to toggle mute
    with keyboard.pressed(Key.alt):
        keyboard.press("a")
        keyboard.release("a")


ser = serial.Serial(port="COM4")

# Helper function to print from within subprocess
def pt(status):
    print(status)


# Subprocess to check for button press, then toggle mute.
def get_button(ser):
    while True:
        x = ser.readline()
        toggle_mute()
        print(x)


def light_on(light_on_var, ser):
    if light_on_var == True:
        ser.write(b"off")
    else:
        ser.write(b"on")


thread = threading.Thread(target=get_button, args=(ser,))
am_muted = False

thread.start()


while True:
    if getZoomStatus.DetectZoomMeeting():
        pt("Meeting detected")
        am_muted_latest = "zoomMute:muted" in getZoomStatus.GetZoomStatus()
        # pt("Latest:" +  am_muted_latest)
        if am_muted != am_muted_latest:
            # pt("Changed:" + am_muted_latest)
            light_on(not am_muted, ser)
        am_muted = am_muted_latest
