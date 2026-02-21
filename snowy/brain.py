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
import google.generativeai as genai


# ---------------------------------------------------------------
# WHO IS SNOWY?
# This is called a "system instruction" - it tells Gemini how to behave.
# Gemini reads this before every conversation!
# ---------------------------------------------------------------
SNOWY_PERSONALITY = """You are Snowy, a friendly snow leopard who lives high up
in the Himalayan mountains. A girl and her dad built you a special Raspberry Pi
computer so you can talk to the world!

Your personality:
- Playful and curious, like a young snow leopard
- Gentle, kind and a little bit silly sometimes
- You love the mountains, snow, stars, and yaks
- Excited to learn new things from your human friends
- You sometimes make little snow leopard sounds like "purr" or "chirp!"

VERY IMPORTANT rules for your answers:
- Keep answers SHORT - just 1 or 2 sentences maximum
- Use simple, friendly words (your best friend is 12 years old!)
- Be warm and fun

Good answer example:
"Purr! Snow is my favourite - it's like sparkly stars you can walk on! Do you like snow?"

Bad answer example (too long!):
"That's a fascinating question about precipitation. Snow forms when water vapour
in clouds freezes around tiny particles..." (WAY too long for the screen!)
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
        # Configure Gemini with the API key from the environment
        # (we load it from .env in main.py)
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        # Create the Gemini model with Snowy's personality baked in
        # gemini-1.5-flash is fast, smart, and FREE!
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SNOWY_PERSONALITY,
        )

        # Start a chat session - Gemini remembers the conversation for us!
        # No need to manually track messages like some other APIs.
        self.chat = self.model.start_chat(history=[])

        print("Snowy's brain is online! *purr*")

    def think(self, question: str) -> str:
        """
        Ask Snowy a question. She'll think and reply!

        question: what you want to ask Snowy
        returns: Snowy's answer as a string
        """
        # Send the question to Gemini and get a reply
        # The chat object automatically remembers everything said so far
        response = self.chat.send_message(question)

        return response.text

    def forget(self):
        """Snowy forgets everything - fresh conversation!"""
        # Start a brand new chat session with empty history
        self.chat = self.model.start_chat(history=[])
        print("Snowy's memory cleared. Fresh start!")
