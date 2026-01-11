# Snowy 🐆❄️

AI-powered Lego Snow Leopard that uses Google Gemini for high-level decision making and Python-controlled hardware for movement and sensing.

## Features ✅

- Autonomous exploration behaviors
- Voice interaction and natural-language control via Google Gemini
- Sensor-based navigation (ultrasonic, IR, bump sensors)
- Camera-based perception (optional object detection)
- Simple API for custom behaviors and remote control

## Hardware 🔧

- **Brain:** Raspberry Pi 3B
- **Peripherals:** Freenove Ultimate Starter Kit (motors, sensors, LEDs)
- **Optional:** Raspberry Pi Camera, motor driver HAT, battery pack

## Software 🧠

- **Language:** Python 3.10+
- **Key libraries:** `gpiozero`, `RPi.GPIO`, `opencv-python`, `requests`, `asyncio`
- **Integration:** Google Gemini API (requires API key)

> Note: Keep your Gemini API key secure. Set it via an environment variable (see Quick start).

## Quick start 🚀

1. Clone the repo:

   ```bash
   git clone <repo-url>
   cd Snowy
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set your Gemini API key:

   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. Run the main controller:

   ```bash
   python src/main.py
   ```

## Development 🛠️

- Project layout: `src/` (code), `tests/` (unit tests), `docs/` (optional docs)
- Run tests: `pytest`
- Follow conventional commits for pull requests

## Contributing 🤝

Contributions are welcome! Open issues for bugs or feature requests and submit pull requests for changes. Please add tests and update docs for new features.

## License 📄

This project is available under the **MIT License**. See `LICENSE` for details.

## Contact

For questions or help, open an issue or contact the project maintainer.

---

*Initial commit: README*