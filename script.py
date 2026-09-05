from datetime import datetime, timedelta
import requests

# 1. Regn automatisk datoen ud for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Definer URL og parametre til DMI
url = "https://dmi.dk"
params = {
    "coords": "POINT(12.635 55.655)",  # Amager Strand
    "datetime": dato_streng,
    "f": "json",
}

print(f"Henter DMI vejrudsigt for dato: {dato_streng}...")

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # 3. Udskriv resultatet direkte i loggen (Gør det synligt i GitHub Actions)
    print("\n=== VEJRUDGIGT FOR AMAGER STRAND I MORGEN KL 08:00 ===")
    
    # Her kan du udskrive hele JSON-svaret, så du kan læse det i din log:
    import json
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"Kunne ikke hente data fra DMI API: {e}")
