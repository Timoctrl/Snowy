from gpiozero import Button
from signal import pause

button = Button(18, pull_up=None, active_state=False)  # Active low, no internal pull

def on_press():
    print("👂 Ear released!")

def on_release():
    print("👂 Ear pressed!")

button.when_pressed = on_press
button.when_released = on_release

print("Press Snowy's ear (Ctrl+C to stop)")
pause()
