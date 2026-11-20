# PalmTransit — Campus Shuttle Agent (Demo)

A Streamlit demo for campus shuttle disruption management and commuter assistance. **All data is simulated; this is not a live transit system.**

## Run locally
1. Install Python 3.10+
2. Open a terminal in this folder
3. Run:
   ```bash
   python -m venv .venv
   # Windows: .venv\\Scripts\\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Features
- Scenario switcher (normal, sandstorm, event barrier, GPS conflict/stale/dark, crowding, accessibility, combined)
- Rule-based status resolver and honest fallback messaging
- Commuter question interface
- Smart boarding stop suggestions
- Reroute proposals staged for Transport Officer review
- Approval/rejection actions and SQLite audit trail

## Important demo boundaries
- GPS, weather, crowd, route and timetable feeds are mock/simulated.
- No LLM API is connected in this starter repository. Commuter answers use deterministic templates, so the project can run without API keys.
- Reroute approval changes proposal state in the demo database; it does not affect actual vehicles.
- For real deployment, integrate authenticated feeds, map/routing APIs, secure identity/roles, and safety validation.

## Architecture
Streamlit UI → commuter/reroute logic → simulated data tools + rule-based resolver → SQLite audit/proposal storage → officer review.
