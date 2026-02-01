import time
import random
from RPLCD.i2c import CharLCD
from gpiozero import Button, LED

# Hardware setup
lcd = CharLCD('PCF8574', 0x27, 2, cols=16, rows=2)
button = Button(18, pull_up=None, active_state=False)

# Three separate LEDs for RGB
red_led = LED(17)
blue_led = LED(27)  # Note: you said LED 2 is blue on GPIO27
green_led = LED(22)

# Mood definitions with colors
moods = {
    "HAPPY :)": (1, 1, 0),      # Red + Green = Yellow
    "SLEEPY ZzZ": (0, 0.3, 0),  # Dim blue
    "CURIOUS ??": (0, 0, 1),    # Green
    "PLAYFUL!": (1, 0, 1),      # Red + Blue = Purple
    "GRUMPY >:(": (1, 0, 0)     # Red only
}

current_mood = random.choice(list(moods.keys()))

def set_eye_color(r, g, b):
    """Set LED brightness (0.0 to 1.0)"""
    if r > 0:
        red_led.on()
    else:
        red_led.off()
    
    if g > 0:
        green_led.on()
    else:
        green_led.off()
    
    if b > 0:
        blue_led.on()
    else:
        blue_led.off()

def show_mood():
    # Update LCD
    lcd.clear()
    lcd.write_string("Snowy feels:")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(current_mood)
    
    # Update eye color
    r, g, b = moods[current_mood]
    set_eye_color(r, g, b)

def change_mood():
    global current_mood
    # Pick a different mood (not the current one)
    available_moods = [m for m in moods.keys() if m != current_mood]
    current_mood = random.choice(available_moods)
    show_mood()
    print(f"👂 Mood changed! Snowy feels: {current_mood}")

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
    red_led.off()
    blue_led.off()
    green_led.off()
    print("\n😴 Snowy sleeping")
