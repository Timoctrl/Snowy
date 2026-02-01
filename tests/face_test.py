import time
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27, 2, cols=16, rows=2)  # Correct for 1602A backpack!

lcd.clear()
lcd.write_string("Hello!")
lcd.cursor_pos = (1, 0)
lcd.write_string("I'm Snowy :)")
time.sleep(5)

lcd.clear()
moods = ["HAPPY :)", "SLEEPY ZzZ", "CURIOUS ??"]
while True:
    for mood in moods:
        lcd.clear()
        lcd.write_string("Snowy Mood:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(mood)
        time.sleep(3)
