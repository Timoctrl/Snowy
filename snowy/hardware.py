"""
snowy/hardware.py - Controls Snowy's body!

This file talks to the physical parts of Snowy:
  - LCD face  (the little screen that shows text)
  - LED eyes  (the three coloured lights)
  - Ear button (the push button)

Think of this file as the "nervous system" connecting
the Raspberry Pi to the real world.

PIN REFERENCE (from your build):
  GPIO 17 (Pin 11) = Red LED
  GPIO 27 (Pin 13) = Blue LED
  GPIO 22 (Pin 15) = Green LED
  GPIO 18 (Pin 12) = Button
  I2C address 0x27 = LCD screen
"""

import time
from RPLCD.i2c import CharLCD
from gpiozero import LED, Button


# ---------------------------------------------------------------
# EYE COLOURS
# Each mood is a combination of which LEDs are on/off.
# True = ON, False = OFF
# Red + Green = Yellow (happy!)
# Red + Blue  = Purple (playful!)
# ---------------------------------------------------------------
EYE_COLOURS = {
    "happy":    {"red": True,  "blue": False, "green": True},   # Yellow
    "thinking": {"red": False, "blue": True,  "green": False},  # Blue
    "curious":  {"red": False, "blue": False, "green": True},   # Green
    "playful":  {"red": True,  "blue": True,  "green": False},  # Purple
    "grumpy":   {"red": True,  "blue": False, "green": False},  # Red
    "sleepy":   {"red": False, "blue": True,  "green": False},  # Dim blue
    "off":      {"red": False, "blue": False, "green": False},  # All off
}


class SnowyBody:
    """
    Controls all of Snowy's physical hardware.

    Usage:
        body = SnowyBody()
        body.show_face("Hello!", "I am Snowy")
        body.set_eyes("happy")
        body.wait_for_button()
    """

    def __init__(self):
        # Set up the LCD screen (Snowy's face)
        # PCF8574 is the chip on the back of the LCD
        # 0x27 is the address (like a phone number for the screen)
        self.lcd = CharLCD("PCF8574", 0x27, 2, cols=16, rows=2)

        # Set up the three LED eyes
        self.red   = LED(17)   # Red eye   (GPIO 17, Pin 11)
        self.blue  = LED(27)   # Blue eye  (GPIO 27, Pin 13)
        self.green = LED(22)   # Green eye (GPIO 22, Pin 15)

        # Set up the ear button
        # pull_up=False → Pi's internal pull-DOWN resistor keeps GPIO 18 LOW
        # when not pressed. Button connects GPIO 18 to 3.3V when pressed
        # (active HIGH wiring - confirmed by button_test.py).
        self.ear = Button(18, pull_up=False)

        # Make sure all LEDs are off at startup - previous session may have
        # left them on (e.g. the sleepy/blue eyes from the shutdown sequence)
        self.set_eyes("off")

        print("Snowy's body is ready!")

    # -----------------------------------------------------------
    # EYE CONTROL
    # -----------------------------------------------------------

    def set_eyes(self, mood: str):
        """
        Change eye colour to match a mood.
        mood: one of "happy", "thinking", "curious", "playful",
                     "grumpy", "sleepy", "off"
        """
        colours = EYE_COLOURS.get(mood, EYE_COLOURS["off"])
        self.red.on()   if colours["red"]   else self.red.off()
        self.blue.on()  if colours["blue"]  else self.blue.off()
        self.green.on() if colours["green"] else self.green.off()

    def blink_eyes(self, mood: str, times: int = 3, speed: float = 0.2):
        """Blink the eyes in a mood colour - useful for 'thinking' animation."""
        for _ in range(times):
            self.set_eyes(mood)
            time.sleep(speed)
            self.set_eyes("off")
            time.sleep(speed)
        self.set_eyes(mood)

    # -----------------------------------------------------------
    # LCD FACE CONTROL
    # -----------------------------------------------------------

    def show_face(self, line1: str, line2: str = ""):
        """
        Show text on the LCD.
        line1: top row    (max 16 characters)
        line2: bottom row (max 16 characters, optional)
        """
        self.lcd.clear()
        self.lcd.write_string(line1[:16])  # Trim to 16 chars just in case
        if line2:
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(line2[:16])

    def scroll_text(self, text: str, pause: float = 2.5):
        """
        Show a long message on the LCD, scrolling page by page.

        This works by:
        1. Splitting the text into words
        2. Packing words into 16-char lines (like fitting words on a page)
        3. Showing 2 lines at a time, then pausing, then showing the next 2

        text: the full message to display
        pause: how long (seconds) to show each page before scrolling
        """
        # Step 1: split text into words
        words = text.split()

        # Step 2: pack words into 16-char LCD lines
        lines = []
        current_line = ""
        for word in words:
            # Will this word fit on the current line?
            space_needed = len(word) + (1 if current_line else 0)
            if len(current_line) + space_needed <= 16:
                current_line += (" " if current_line else "") + word
            else:
                # Word doesn't fit - save current line, start new one
                if current_line:
                    lines.append(current_line)
                current_line = word

        # Don't forget the last line!
        if current_line:
            lines.append(current_line)

        # Step 3: show lines in pairs (2 lines = 1 page on the LCD)
        for i in range(0, len(lines), 2):
            top    = lines[i]
            bottom = lines[i + 1] if i + 1 < len(lines) else ""
            self.show_face(top, bottom)
            time.sleep(pause)

    # -----------------------------------------------------------
    # BUTTON CONTROL
    # -----------------------------------------------------------

    def wait_for_button(self):
        """
        Pause the program until the ear button is pressed.
        The program will just sit here waiting... (that's OK!)
        """
        self.ear.wait_for_press()

    # -----------------------------------------------------------
    # SHUTDOWN
    # -----------------------------------------------------------

    def power_down(self):
        """Turn off all lights and clear the LCD. Goodnight Snowy!"""
        self.lcd.clear()
        self.set_eyes("off")
