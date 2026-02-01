from gpiozero import LED
from time import sleep

red = LED(17)
green = LED(27)
blue = LED(22)

print("Testing RED (GPIO17)...")
red.on()
sleep(2)
red.off()

print("Testing GREEN (GPIO27)...")
green.on()
sleep(2)
green.off()

print("Testing BLUE (GPIO22)...")
blue.on()
sleep(2)
blue.off()

print("All off")
