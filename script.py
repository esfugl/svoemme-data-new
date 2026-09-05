from datetime import datetime
import json
import os
import requests

# 1. Definer API-kaldet til DMI
url = "https://dmi.dk"
params = {
    "coords": "POINT(12.635 55.655)",
    "datetime": "2026-09-06T06:00:00Z",  # Erstattes evt. dynamisk i rigtig drift
    "f": "json",
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Eksempel: Vi henter temperaturen (DMI parametre varierer, tjek dokumentation)
    # Her gemmer vi blot det rå JSON-svar som et eksempel i en logfil
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filnavn = f"vejrdata_{timestamp}.json"

    with open(filnavn, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Data gemt i {filnavn}")

except requests.exceptions.RequestException as e:
    print(f"API fejl: {e}")
