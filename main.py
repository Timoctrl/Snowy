#!/usr/bin/env python3
"""
main.py - SNOWY THE SNOW LEOPARD!

This is the main program. Run it on your Raspberry Pi with:

    python3 main.py

HOW IT WORKS:
    1.  Snowy wakes up (LCD + eyes switch on)
    2.  Press Snowy's ear (the button)
    3.  Type your question on the keyboard
    4.  Snowy's eyes go blue while she thinks
    5.  Snowy's answer scrolls across the LCD!
    6.  Press the ear again to ask another question
    7.  Press Ctrl+C to put Snowy to sleep

BEFORE YOU RUN THIS:
    Make sure you have a .env file with your API key:
        echo 'GEMINI_API_KEY=your-key-here' > .env

    And install the libraries:
        sudo pip3 install google-generativeai python-dotenv RPLCD gpiozero --break-system-packages
"""

import os
import time

# python-dotenv reads the .env file and puts ANTHROPIC_API_KEY
# into the environment so anthropic can find it automatically.
# We do this FIRST, before importing anything else!
try:
    from dotenv import load_dotenv
    load_dotenv()  # Reads .env file in the current directory
except ImportError:
    pass  # That's OK - the key can also be set manually with 'export'

# Now import Snowy's modules
from snowy.brain import SnowyBrain
from snowy.hardware import SnowyBody


def check_api_key():
    """Check the API key is set before we start. Friendly error if not."""
    if not os.environ.get("GEMINI_API_KEY"):
        print()
        print("ERROR: GEMINI_API_KEY not found!")
        print()
        print("You need to create a .env file like this:")
        print("   1. Open a terminal on the Pi")
        print("   2. Go to the Snowy folder: cd ~/Snowy")
        print("   3. Run: nano .env")
        print("   4. Type this (with your real key):")
        print("        GEMINI_API_KEY=AIzaxxxxx")
        print("   5. Save: Ctrl+O, Enter, Ctrl+X")
        print()
        print("Get a free key at: aistudio.google.com/apikey")
        print()
        raise SystemExit(1)


def main():
    """The main program - Snowy comes to life here!"""

    # Step 0: Make sure the API key is ready
    check_api_key()

    print()
    print("=" * 35)
    print("  Snowy is waking up...  *yaaawn*  ")
    print("=" * 35)
    print()

    # Step 1: Wake up Snowy's brain (Claude AI) and body (hardware)
    brain = SnowyBrain()
    body  = SnowyBody()

    # Step 2: Startup greeting on the LCD
    body.show_face("Hello! I am", "Snowy! ^..^")
    body.set_eyes("happy")
    time.sleep(2)

    body.show_face("Press my ear", "to talk! :)")
    body.set_eyes("curious")

    print("Snowy is ready!")
    print("Press the ear button to start a conversation.")
    print("Press Ctrl+C at any time to shut Snowy down.\n")

    # Step 3: Main loop - keep going until Ctrl+C
    try:
        while True:

            # --- WAIT FOR BUTTON ---
            print("Waiting for button press...")
            body.wait_for_button()
            print("Button pressed!")

            # --- LISTEN ---
            body.show_face("I'm listening", "...")
            body.set_eyes("curious")

            # Get the question from the keyboard
            # (Later we'll replace this with the microphone!)
            print()
            try:
                question = input("Ask Snowy: ").strip()
            except EOFError:
                # EOFError can happen in some SSH setups
                break

            # If nothing was typed, just go back to waiting
            if not question:
                body.show_face("Hmm? I didn't", "hear anything!")
                time.sleep(2)
                body.show_face("Press my ear", "to talk! :)")
                body.set_eyes("curious")
                continue

            # --- THINK ---
            body.show_face("Hmm let me", "think... *paw*")
            body.blink_eyes("thinking", times=4, speed=0.3)
            print(f"\nSnowy is thinking about: {question!r}")

            # Ask Claude AI! This goes over the internet to Anthropic.
            try:
                answer = brain.think(question)
            except Exception as err:
                # Something went wrong (no internet? wrong key?)
                print(f"Error from Claude: {err}")
                answer = "Oh no, my brain got confused! Try again?"
                body.set_eyes("grumpy")
                body.show_face("Oops! Brain", "got confused!")
                time.sleep(2)
                body.show_face("Press my ear", "to talk! :)")
                body.set_eyes("curious")
                continue

            # --- SPEAK ---
            print(f"Snowy says: {answer}\n")
            body.set_eyes("happy")
            body.scroll_text(answer, pause=2.5)

            # --- READY AGAIN ---
            body.show_face("Press my ear", "to talk! :)")
            body.set_eyes("curious")

    except KeyboardInterrupt:
        # Ctrl+C was pressed - time to sleep!
        print("\n\nPutting Snowy to sleep... *purr*")

    finally:
        # Always clean up, even if something went wrong
        body.show_face("Goodbye!", "Purrrr... zzz")
        body.set_eyes("sleepy")
        time.sleep(2)
        body.power_down()
        print("Snowy is asleep. Goodnight!")


if __name__ == "__main__":
    main()
