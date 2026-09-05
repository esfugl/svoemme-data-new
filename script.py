from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Den korrekte, aktive URL til DMI's åbne Forecast EDR API
url = "https://dmi.dk"

# 3. Parametre opbygget præcis efter DMI's specifikationer
params = {
    "coords": "POINT(12.635 55.655)",  # Amager Strand (længdegrad breddegrad)
    "datetime": dato_streng,
    "f": "json"                         # Vi beder eksplicit om rå JSON data
}

headers = {
    "Accept": "application/json",
    "User-Agent": "GitHubActions-DMI-WeatherFetch/1.0"
}

print("Forbinder til DMI Open Data API...")
print(f"Henter data for Amager Strand til dato: {dato_streng}")

try:
    # 4. Lav API-kaldet til DMI uden omdirigeringer
    response = requests.get(url, params=params, headers=headers, allow_redirects=False)
    
    print(f"Server svarede med statuskode: {response.status_code}")
    response.raise_for_status()

    # 5. Fortolk JSON-dataen
    data = response.json()
    print("\n=== SUCCESS: VEJRDATA MODTAGET FRA DMI ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Fejl: {http_err}")
    print(f"Serverens svar var: {response.text[:300]}")
except json.JSONDecodeError:
    print("Fejl: Kunne ikke læse svaret som JSON. Serveren sendte i stedet:")
    print(response.text[:300])
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
