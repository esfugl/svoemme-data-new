from datetime import datetime, timedelta
import json
import requests
import time

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Den fulde rå URL til DMI's EDR-tjeneste
base_url = "https://opendataapi.dmi.dk/v1/forecastedr/collections/harmonie_dini_sf/position"
full_url = f"{base_url}?coords=POINT(12.635 55.655)&datetime={dato_streng}&parameter-name=temperature-2m"

headers = {
    "Accept": "application/json",
    "User-Agent": "GitHubActions-DMI-WeatherFetch/1.0"
}

print("Forbinder til DMI Frie Data API...")
print(f"Henter temperatur for Amager Strand ({dato_streng})...")

# 3. Logik til at håndtere 429 "Too Many Requests" ved at prøve igen
max_forsoeg = 3
ventetid = 5  # sekunder vi venter første gang

for forsoeg in range(max_forsoeg):
    try:
        response = requests.get(full_url, headers=headers)
        
        # Hvis vi bliver blokeret af hastighedsbegrænsning
        if response.status_code == 429:
            print(f"Forseg {forsoeg + 1} fejlede: Serveren er overbelastet (429). Vent i {ventetid} sekunder...")
            time.sleep(ventetid)
            ventetid *= 2  # Ganger ventetiden op til næste gang (Exponential Backoff)
            continue
            
        print(f"Server svarede med statuskode: {response.status_code}")
        response.raise_for_status()

        # 4. Hvis kaldet lykkes, læser vi JSON-strukturen ud
        data = response.json()
        print("\n=== SUCCESS: VEJRDATA MODTAGET FRA DMI ===")
        print(json.dumps(data, indent=4, ensure_ascii=False))
        break  # Bryd ud af løkken da vi fik vores data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Fejl opstod: {http_err}")
        break
    except json.JSONDecodeError:
        print("Fejl: Svaret kunne ikke læses som JSON.")
        break
    except requests.exceptions.RequestException as e:
        print(f"Netværksfejl: {e}")
        break
else:
    print(f"\nFejl: Kunne ikke hente data efter {max_forsoeg} forsøg pga. serverbelastning.")
