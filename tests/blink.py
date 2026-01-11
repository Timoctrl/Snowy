#!/usr/bin/env python3
"""
Snowy Blink Test - GPIO17 LED blink.
Freenove Ch1 adapted.[file:2]
"""
from gpiozero import LED
from time import sleep
from signal import pause

led = LED(17)  # Red LED, GPIO17 (BCM)

print("Snowy eyes: Ctrl+C to sleep")
try:
    while True:
        led.on(); print("👁 ON"); sleep(0.5)
        led.off(); print("👁 OFF"); sleep(0.5)
except KeyboardInterrupt:
    print("😴")
    led.close()
