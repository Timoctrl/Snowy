"""
snowy/ears.py - Snowy's ears! USB microphone + speech recognition.

This file does two jobs:
  1. Records audio from the USB microphone
  2. Sends it to Google's free speech recognition to turn into text

It uses a library called SpeechRecognition which handles all the
hard parts of working with microphones for us.

SETUP NEEDED (run on Pi once):
    sudo apt-get install python3-pyaudio -y
    sudo pip3 install SpeechRecognition --break-system-packages
"""

import os
import speech_recognition as sr


class SnowyEars:
    """
    Snowy's ears - listens to your voice and turns it into text!

    Usage:
        ears = SnowyEars()
        text = ears.listen()
        if text:
            print(f"You said: {text}")
        else:
            print("Didn't catch that!")
    """

    def __init__(self):
        # The Recognizer does the speech-to-text conversion
        self.recognizer = sr.Recognizer()

        # Microphone() automatically picks the default mic.
        # We briefly silence stderr while it loads PyAudio, because ALSA
        # prints a bunch of harmless warnings about missing audio devices.
        # We do this by redirecting stderr at the OS level (safe on ARM).
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        os.dup2(devnull, 2)
        os.close(devnull)
        try:
            self.mic = sr.Microphone()
        finally:
            os.dup2(old_stderr, 2)  # Always restore stderr!
            os.close(old_stderr)

        # Wait this many seconds of silence before deciding you've finished
        # speaking. Default is 0.8s which cuts off too early mid-sentence.
        self.recognizer.pause_threshold = 2.5

        # Calibrate for background noise (takes about 1 second)
        # This helps Snowy ignore hum, fans, etc.
        print("Calibrating microphone... (stay quiet for a moment!)")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Microphone ready! *ear twitch*")

    def listen(self, timeout: float = 6, phrase_limit: float = 8) -> str:
        """
        Listen for speech and return it as text.

        timeout:      how many seconds to wait for you to START speaking
        phrase_limit: maximum seconds to record once you've started

        returns: what you said as a string, or "" if nothing was understood
        """
        try:
            with self.mic as source:
                # Wait for speech, then record until silence
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit,
                )
        except sr.WaitTimeoutError:
            # You didn't say anything within the timeout - that's OK!
            return ""

        # Send the recorded audio to Google's speech recognition (free!)
        try:
            text = self.recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            # Audio was recorded but Google couldn't make out the words
            return ""

        except sr.RequestError as e:
            # No internet, or Google's service is down
            print(f"Speech recognition error: {e}")
            return ""


# ---------------------------------------------------------------
# NOTE: If Snowy can't find your USB microphone, you can tell her
# which one to use by its device index number. Run this on the Pi
# to see all microphones and their numbers:
#
#   python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
#
# Then change:  self.mic = sr.Microphone()
# To:           self.mic = sr.Microphone(device_index=1)  # (use your number)
# ---------------------------------------------------------------
