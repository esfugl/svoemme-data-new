from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Den officielle API-adresse til DMI EDR
url = "https://opendataapi.dmi.dk/v1/forecastedr/collections/harmonie_dini_sf/position"

# 3. Parametre tilpasset DMI's standarder (f=covjson i stedet for f=json)
params = {
    "coords": "POINT(12.635 55.655)",     # Amager Strand
    "datetime": dato_streng,
    "parameter-name": "temperature-2m",   # Vi beder specifikt om lufttemperatur
    "f": "covjson"                         # DETTE RETTER FEJLEN: CoverageJSON format
}

headers = {
    "Accept": "application/json",
    "User-Agent": "GitHubActions-DMI-WeatherFetch/1.0"
}

print("Forbinder til DMI Frie Data API...")
print(f"Henter vejrdata for Amager Strand ({dato_streng})...")

try:
    response = requests.get(url, params=params, headers=headers)
    
    print(f"Server svarede med statuskode: {response.status_code}")
    response.raise_for_status()

    # Svaret modtages i JSON-struktur, selvom det følger covjson-standarden
    data = response.json()
    print("\n=== SUCCESS: VEJRDATA MODTAGET FRA DMI ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Fejl: {http_err}")
    print(f"Serverens rå svar var: {response.text}")
except json.JSONDecodeError:
    print("Fejl: Kunne ikke fortolke svaret som JSON-struktur.")
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
