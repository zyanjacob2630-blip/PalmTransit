# PalmTransit — Gemini-powered demo

Campus shuttle disruption and commuter agent with **simulated data**. Gemini is used for conversational reasoning and tool calling; the Python rules and officer approval guardrails remain in charge of safety-critical actions.

## Install and run (Windows)
1. Extract the folder.
2. Install Python 3.10 or newer.
3. Open terminal in this folder and run:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in this folder. Copy `.env.example` and paste your Gemini key into `GEMINI_API_KEY`.
5. Start:
   ```bash
   streamlit run app.py
   ```

## API key setup
- Get a key from Google AI Studio: https://aistudio.google.com/app/apikey
- `.env` is ignored by Git. **Never commit or share your key.**
- Streamlit Cloud users can use app settings → Secrets with:
  ```toml
  GEMINI_API_KEY = "your-key"
  GEMINI_MODEL = "gemini-2.5-flash"
  ```

## Gemini agent tools
- `service_status`: read simulated status feeds
- `alerts`: read simulated alert feeds
- `boarding_stops`: query stop recommendations
- `stage_reroute`: stage a proposal for officer review

Gemini can call these tools. Route proposals never become operational from the AI response alone. The officer console remains the approval gate.

## Demo data and limitations
- GPS, weather, events, crowding, stops and timetable information are simulated.
- This is not connected to real shuttle vehicles or feeds.
- A reroute proposal does not change real service.
- The demo uses rule-based simulated feed resolution and fallback messaging.
- Keep your API key private and monitor your API provider's usage limits.

## Start
`streamlit run app.py`
