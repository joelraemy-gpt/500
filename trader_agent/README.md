# Trader Agent (Paper-first, Compliance-first)

## Überblick
Dieses Projekt implementiert ein modulares Trading-Agent-System mit Fokus auf Stabilität, Auditierbarkeit und Risk-Management.

- **Default: Paper Trading**
- **LIVE nur bei explizitem `LIVE_TRADING=true`**
- JSON-Logging + SQLite Audit-Trail
- Kill-Switch Kommando vorhanden

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

## CLI
```bash
trader-agent paper --symbols AAPL,MSFT --iterations 20
trader-agent backtest --symbol AAPL --from-date 2025-01-01 --to-date 2025-01-31
trader-agent status
trader-agent kill-switch --close-positions
trader-agent live
```

## Sicherheit / Compliance
- Keine Captcha-/2FA-Umgehung.
- Keine Secrets im Code oder Logs.
- Plus500-Adapter ist als Compliance-Stub angelegt; keine inoffizielle API/Reverse-Engineering-Integration.
- Für echte Live-Automation nur offiziell erlaubte Broker-APIs verwenden.

## Risikokontrollen
- Risk per trade (% equity)
- Max daily loss
- Max trades/day
- Max open positions
- Stop-Loss Pflicht im Signalmodell

## Tests
```bash
pytest
```
