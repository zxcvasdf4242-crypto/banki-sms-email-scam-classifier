# ScamShield Pro — Banking SMS & Email Scam Triage

A modular Streamlit academic demo. It uses transparent weighted rules to explain message indicators, accepts CSV batches, and stores local history. No API keys, database server, or downloaded model are required.

## Run on macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```
Open the localhost URL printed in Terminal.

## CSV upload
Upload a CSV with a message column. Common names (`message`, `text`, `sms`, `email`, `content`, `body`, `message_text`) are detected. If not found, select the correct column manually. A sample file is included.

## Features
- Dashboard and recent activity
- Single message analysis with explainable signals
- Batch CSV analysis and downloadable results
- Local history, filtering, export and clear-history action
- Explanation of rules and limitations

## Limitations
This is a rule-based educational prototype, not a trained production model. Risk score is not a probability. False positives and false negatives are possible. Never paste passwords, OTPs, account numbers, or private customer data.
