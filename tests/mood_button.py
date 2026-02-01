import time
import random
from RPLCD.i2c import CharLCD
from gpiozero import Button

# Hardware setup
lcd = CharLCD('PCF8574', 0x27, 2, cols=16, rows=2)
button = Button(18, pull_up=None, active_state=False)

# Mood list
moods = ["HAPPY :)", "SLEEPY ZzZ", "CURIOUS ??", "PLAYFUL!", "GRUMPY >:("]
current_mood = random.choice(moods)

def show_mood():
    lcd.clear()
    lcd.write_string("Snowy feels:")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(current_mood)

def change_mood():
    global current_mood
    current_mood = random.choice(moods)
    show_mood()
    print(f"👂 Ear pressed! Snowy now feels: {current_mood}")

# Button triggers mood change
button.when_released = change_mood

# Show initial mood
show_mood()
print("Press Snowy's ear to change his mood (Ctrl+C to stop)")

# Keep running
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    lcd.clear()
    print("\n😴 Snowy sleeping")
