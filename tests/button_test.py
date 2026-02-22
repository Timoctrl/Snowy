#!/usr/bin/env python3
"""
tests/button_test.py - Diagnose the ear button wiring

Run this to figure out exactly how your button is wired:

    python3 tests/button_test.py

It checks all four possible configurations and tells you
which one shows "not pressed" when you're not touching the button.
THAT is the right config for hardware.py.
"""

import time
from gpiozero import Button

GPIO_PIN = 18

CONFIGS = [
    (
        "pull_up=True, active LOW  (Pi pull-up, button → GND)",
        dict(pull_up=True),
    ),
    (
        "pull_up=False, active HIGH (Pi pull-down, button → 3.3V)",
        dict(pull_up=False),
    ),
    (
        "pull_up=None, active_state=False (external pull-up, button → GND)",
        dict(pull_up=None, active_state=False),
    ),
    (
        "pull_up=None, active_state=True  (external pull-down, button → 3.3V)",
        dict(pull_up=None, active_state=True),
    ),
]

print()
print(f"Button diagnostic — GPIO {GPIO_PIN}")
print("=" * 55)
print("Do NOT touch the button while this runs!")
print("=" * 55)
print()

results = []
for label, kwargs in CONFIGS:
    try:
        b = Button(GPIO_PIN, **kwargs)
        time.sleep(0.15)
        pressed = b.is_pressed
        b.close()
        time.sleep(0.15)
        verdict = "BAD  (reads as pressed when it shouldn't)" if pressed else "GOOD (reads as not-pressed ✓)"
        print(f"  {verdict}")
        print(f"    {label}")
        print()
        if not pressed:
            results.append((label, kwargs))
    except Exception as e:
        print(f"  ERROR: {e}")
        print(f"    {label}")
        print()

print("=" * 55)
if results:
    print(f"✓ Working config(s) found:")
    for label, kwargs in results:
        print(f"    Button({GPIO_PIN}, {', '.join(f'{k}={v}' for k,v in kwargs.items())})")
else:
    print("✗ No config showed 'not pressed'.")
    print("  Check your wiring - the button wire may be")
    print("  connected to GND directly with no resistor,")
    print("  or the button might be physically stuck.")
print("=" * 55)
print()
