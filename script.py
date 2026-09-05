from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. DEN KORREKTE API URL (Rettet fra forecastdata til forecastedr)
url = "https://opendataapi.dmi.dk/v1/forecastedr/collections/harmonie_dini_sf/position"

# 3. Parametre jf. DMI standarden (inkl. parameter for temperatur)
params = {
    "coords": "POINT(12.635 55.655)",  # Amager Strand
    "crs": "crs84",
    "datetime": dato_streng,
    "parameter-name": "temperature-2m", # Henter lufttemperatur
    "f": "json"                          # Garanterer JSON-format retur
}

headers = {
    "Accept": "application/json",
    "User-Agent": "GitHubActions-DMI-WeatherFetch/1.0"
}

print("Forbinder til DMI Frie Data API...")
print(f"Henter temperatur for Amager Strand ({dato_streng})...")

try:
    # Lav kaldet - nu tillader vi redirects hvis DMI internt fordeler trafikken
    response = requests.get(url, params=params, headers=headers, allow_redirects=True)
    
    print(f"Server svarede med statuskode: {response.status_code}")
    response.raise_for_status()

    # 4. Fortolk JSON-dataen
    data = response.json()
    print("\n=== SUCCESS: VEJRDATA MODTAGET FRA DMI ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Fejl: {http_err}")
    print(f"Serverens rå svar var: {response.text[:300]}")
except json.JSONDecodeError:
    print("Fejl: Svaret kunne ikke læses som JSON. Råt svar fra serveren:")
    print(response.text[:300])
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
