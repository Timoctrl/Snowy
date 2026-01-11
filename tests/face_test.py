import time
from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_addr=0x27, num_cols=16, num_rows=2)  # Your address!

lcd.clear()
lcd.write_string("Hello!")
lcd.cursor_pos = (0, 1)
lcd.write_string("I'm Snowy :)")
time.sleep(5)

lcd.clear()
while True:
    lcd.write_string("Snowy Mood:    ")
    lcd.cursor_pos = (0, 1)
    moods = ["HAPPY :)", "SLEEPY ZzZ", "CURIOUS ??"]
    for mood in moods:
        lcd.write_string(mood)
        time.sleep(3)
    lcd.clear()
    

