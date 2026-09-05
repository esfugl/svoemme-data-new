from datetime import datetime, timedelta
import json
import requests

# 1. Regn automatisk datoen ud for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Korrekt Base URL til DMI's åbne EDR API endpoint for en position
url = "https://dmi.dk"

# 3. Parametre opbygget præcis efter DMI's tekniske specifikationer
params = {
    "coords": "POINT(12.635 55.655)",  # Amager Strand (Længdegrad Breddegrad)
    "datetime": dato_streng,
    "f": "json"                         # Tvinger serveren til at sende JSON retur
}

# HTTP Headers for at sikre, at serveren ved, vi forventer JSON
headers = {
    "Accept": "application/json"
}

print(f"Henter DMI vejrudsigt for dato: {dato_streng}...")

try:
    # 4. Lav selve kaldet
    response = requests.get(url, params=params, headers=headers)
    
    # Udskriver statuskoden, så vi kan fejlsøge (f.eks. 200 OK, 400 Bad Request, 404 Not Found)
    print(f"Server svarer med statuskode: {response.status_code}")
    
    # Kaster en fejl, hvis serveren returnerede en fejlkode
    response.raise_for_status()

    # 5. Læs JSON-data ud
    data = response.json()

    print("\n=== VEJRPROGNOSE FOR AMAGER STRAND I MORGEN KL 08:00 ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP fejl opstod: {http_err}")
    print("Serverens rå svar var:")
    print(response.text[:500])  # Vis de første 500 tegn af fejlsiden for nemmere fejlfinding
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl eller JSON-fortolkningsfejl: {e}")
