#!/usr/bin/env python3
"""
main.py - SNOWY THE SNOW LEOPARD!

This is the main program. Run it on your Raspberry Pi with:

    python3 main.py

HOW IT WORKS:
    1.  Snowy wakes up (LCD + eyes switch on)
    2.  Press Snowy's ear (the button)
    3.  SPEAK your question into the USB microphone
    4.  Snowy's eyes blink blue while she listens and thinks
    5.  Snowy's answer scrolls across the LCD!
    6.  Press the ear again to ask another question
    7.  Press Ctrl+C to put Snowy to sleep

BEFORE YOU RUN THIS:
    Install audio support:
        sudo apt-get install python3-pyaudio -y
        sudo pip3 install SpeechRecognition google-genai python-dotenv --break-system-packages

    Make sure you have a .env file with your API key:
        nano .env   →  add line:  GEMINI_API_KEY=your-key-here
"""

import os
import time

# python-dotenv reads the .env file and loads GEMINI_API_KEY
# into the environment. We do this FIRST, before importing anything else!
try:
    from dotenv import load_dotenv
    load_dotenv()  # Reads .env file in the current directory
except ImportError:
    pass  # That's OK - the key can also be set manually with 'export'

# Now import Snowy's modules
from snowy.brain import SnowyBrain
from snowy.hardware import SnowyBody
from snowy.ears import SnowyEars


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


def _show_idle(body, brain):
    """
    Show Snowy's idle screen. Eyes go red if quota is exhausted so you
    can see at a glance whether she can answer questions or not.
    """
    if brain.quota_ok:
        body.show_face("Press my ear", "then speak!")
        body.set_eyes("curious")   # green = ready
    else:
        body.show_face("No credits!", "Try tomorrow")
        body.set_eyes("grumpy")    # red = quota exhausted


def main():
    """The main program - Snowy comes to life here!"""

    # Step 0: Make sure the API key is ready
    check_api_key()

    print()
    print("=" * 35)
    print("  Snowy is waking up...  *yaaawn*  ")
    print("=" * 35)
    print()

    # Step 1: Wake up Snowy's brain (Gemini AI), ears (mic), and body (hardware)
    brain = SnowyBrain()
    body  = SnowyBody()
    ears  = SnowyEars()   # This calibrates the mic - keep quiet for 1 second!

    # Step 2: Startup greeting on the LCD
    body.show_face("Hello! I am", "Snowy! ^..^")
    body.set_eyes("happy")
    time.sleep(2)

    _show_idle(body, brain)

    print("Snowy is ready!")
    print("Press the ear button, then speak your question.")
    print("Press Ctrl+C at any time to shut Snowy down.\n")

    # Step 3: Main loop - keep going until Ctrl+C
    try:
        while True:

            # --- WAIT FOR BUTTON ---
            print("Waiting for button press...")
            body.wait_for_button()
            print("Button pressed! Listening...")

            # --- LISTEN ---
            body.show_face("Listening...", "Speak now! :)")
            body.set_eyes("curious")

            # Record from the USB microphone and convert speech to text
            question = ears.listen(timeout=6, phrase_limit=8)
            print(f"Heard: {question!r}")

            # If nothing was heard, go back to waiting
            if not question:
                body.show_face("Hmm? I didn't", "catch that!")
                body.set_eyes("sleepy")
                time.sleep(2)
                _show_idle(body, brain)
                continue

            # Show what Snowy heard (so you can check it was right!)
            body.show_face("I heard:", question[:16])
            time.sleep(1)

            # --- THINK ---
            body.show_face("Hmm let me", "think... *paw*")
            body.blink_eyes("thinking", times=4, speed=0.3)
            print(f"Snowy is thinking about: {question!r}")

            # Ask Gemini AI!
            try:
                answer = brain.think(question)
            except Exception as err:
                print(f"Error from Gemini: {err}")
                body.set_eyes("grumpy")
                if brain._is_quota_error(err):
                    brain.quota_ok = False
                    body.show_face("No credits!", "Try tomorrow")
                else:
                    body.show_face("Oops! Brain", "got confused!")
                time.sleep(2)
                # idle state will be set at bottom of loop
                continue

            # --- ANSWER ---
            print(f"Snowy says: {answer}\n")
            body.set_eyes("happy")
            body.scroll_text(answer, pause=2.5)

            # --- READY AGAIN ---
            _show_idle(body, brain)

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
