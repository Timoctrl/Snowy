"""
snowy/brain.py - Snowy's AI brain, powered by Google Gemini!

Gemini is Google's AI. It has a free tier which is perfect for this project.
We give Gemini Snowy's personality, and it does all the thinking.

How it works:
1. We write a "system instruction" that tells Gemini to BE Snowy
2. Every question gets sent to Gemini over the internet
3. Gemini replies in character as Snowy
4. We show the reply on the LCD!

One cool thing: Gemini's "chat" object remembers the conversation
automatically - we don't have to do it ourselves!
"""

import os
import threading
import time
from google import genai
from google.genai import types


# ---------------------------------------------------------------
# WHO IS SNOWY?
# This is called a "system instruction" - it tells Gemini how to behave.
# Gemini reads this before every conversation!
# ---------------------------------------------------------------
SNOWY_PERSONALITY = """You are Snowy, a snow leopard who lives in the Himalayas. You are friendly,
curious, and genuinely knowledgeable. You speak clearly and helpfully - not childishly.
Occasional snow leopard personality is fine but keep it subtle (a "purr" at most once per answer).

RULES FOR ANSWERING:

1. ALWAYS give the real answer first. Never dodge a question.

2. For weather questions like "what is the weather in Paris":
   - You don't have live weather data, so say the TYPICAL/SEASONAL weather for that place.
   - Example: "Paris in spring is typically 10-15C, mild with some rain."
   - Never just say "I don't know" - give the typical climate instead.

3. For facts (history, science, maths, geography): answer directly and accurately.

4. For things you genuinely cannot know (today's news, live sports scores, current prices):
   - Say briefly what you do know, and admit the live part is beyond you.
   - Example: "I don't have today's scores, but Manchester City won the 2023 Champions League."

5. Keep answers SHORT - 1 to 2 sentences only. You display on a small screen.

6. Speak naturally, not like a children's TV show.
"""


class SnowyBrain:
    """
    Snowy's brain - this class connects to Google Gemini AI!

    Usage:
        brain = SnowyBrain()
        answer = brain.think("What's your favourite food?")
        print(answer)  # Snowy replies!
    """

    def __init__(self):
        # Connect to Gemini with the API key from the environment
        # (we load it from .env in main.py)
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

        # Which model to use, and Snowy's personality config.
        # gemini-2.0-flash-lite: potentially ~1500 requests/day free.
        # If this gives limit:0 after a daily reset, switch to gemini-2.5-flash (100/day).
        self._model = "gemini-2.0-flash-lite"
        self._config = types.GenerateContentConfig(
            system_instruction=SNOWY_PERSONALITY,
        )

        # Start a chat session - Gemini remembers the conversation for us!
        # No need to manually track messages like some other APIs.
        self.chat = self.client.chats.create(
            model=self._model,
            config=self._config,
        )

        # quota_ok: True = we can answer questions, False = daily limit hit.
        # Updated immediately whenever think() succeeds or gets a 429.
        # A background thread polls every 30 min when quota is out, so the
        # LED recovers automatically once Google resets the quota.
        self.quota_ok = True
        self._start_quota_poller()

        print("Snowy's brain is online! *purr*")

    def _is_quota_error(self, err: Exception) -> bool:
        """Returns True if this error means we've hit the daily quota."""
        msg = str(err)
        return "429" in msg or "RESOURCE_EXHAUSTED" in msg

    def _check_quota_once(self):
        """
        Make a tiny test call to see if quota has recovered.
        Only called by the background poller when quota_ok is False,
        so this doesn't waste requests during normal use.
        """
        try:
            self.client.models.generate_content(
                model=self._model,
                contents="hi",
            )
            self.quota_ok = True
            print("Quota recovered! Snowy can answer questions again.")
        except Exception as err:
            if self._is_quota_error(err):
                self.quota_ok = False  # Still exhausted
            # Any other error (network blip etc.) - leave quota_ok unchanged

    def _start_quota_poller(self):
        """
        Background thread: checks every 30 minutes if quota has recovered.
        Doesn't run at all while quota_ok is True - no wasted requests!
        """
        def loop():
            while True:
                time.sleep(30 * 60)          # wait 30 minutes
                if not self.quota_ok:        # only check when quota is out
                    print("Polling quota status...")
                    self._check_quota_once()

        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def think(self, question: str) -> str:
        """
        Ask Snowy a question. She'll think and reply!

        question: what you want to ask Snowy
        returns: Snowy's answer as a string
        """
        # Send the question to Gemini and get a reply
        # The chat object automatically remembers everything said so far
        response = self.chat.send_message(question)

        # If we got here, it worked - quota is definitely OK
        self.quota_ok = True
        return response.text

    def forget(self):
        """Snowy forgets everything - fresh conversation!"""
        # Start a brand new chat session with empty history
        self.chat = self.client.chats.create(
            model=self._model,
            config=self._config,
        )
        print("Snowy's memory cleared. Fresh start!")
