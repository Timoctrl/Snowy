# Snowy the Snow Leopard

An AI-powered Lego snow leopard built with a Raspberry Pi 3B and Claude AI.
Built by a dad and daughter as a hands-on electronics + coding project!

## What Snowy can do

- Press her ear (button) → ask her a question → she answers on her LCD face!
- Her LED eyes change colour based on her mood
- She remembers the conversation so she can refer back to earlier things
- Powered by **Google Gemini** AI (free tier!)

## Hardware

| Part | Where |
|------|-------|
| Raspberry Pi 3B | Outside the Lego head |
| 1602A LCD (I2C) | Snowy's face |
| Red LED (GPIO 17) | Eye |
| Blue LED (GPIO 27) | Eye |
| Green LED (GPIO 22) | Eye |
| Push button (GPIO 18) | Ear |

## File layout

```
main.py              ← Run this to start Snowy!
snowy/
  brain.py           ← Claude AI (Snowy's personality + memory)
  hardware.py        ← LCD, LEDs, button control
tests/
  blink.py           ← Test a single LED
  face_test.py       ← Test the LCD screen
```

## Setting up on the Pi (one-time)

**1. Install libraries**

```bash
sudo pip3 install google-generativeai python-dotenv RPLCD gpiozero --break-system-packages
```

**2. Get a free Gemini API key**

Go to **aistudio.google.com/apikey**, sign in with Google, and click **Create API key**.

**3. Save your API key in a .env file**

```bash
cd ~/Snowy
nano .env
```

Type this (use your real key):
```
GEMINI_API_KEY=AIzaxxxxxxxxxx
```
Save with `Ctrl+O`, `Enter`, `Ctrl+X`.

> **Important:** The .env file is listed in .gitignore so it will never be
> accidentally uploaded to GitHub. Keep your key safe!

## Running Snowy

```bash
cd ~/Snowy
git pull origin main     # get the latest code
python3 main.py
```

Then press Snowy's ear and type a question!

## Coming next

- [ ] USB microphone → speak questions instead of typing
- [ ] Speaker + amp board → Snowy speaks her answers aloud
- [ ] Servo motor → tail wagging!
- [ ] Ultrasonic sensor → Snowy notices when you walk nearby
