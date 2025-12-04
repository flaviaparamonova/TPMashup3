import requests
from datetime import datetime
import json
import time

BASE_URL = "http://10.194.69.214:3671"
OUTPUT_FILE = "MAX_temp_flow.json"

def get_temperature():
    """Retourne UNE valeur de température depuis l'API."""
    response = requests.get(f"{BASE_URL}/sensors/get_sensors_list")
    if response.status_code != 200:
        print("Erreur capteurs :", response.text)
        return None

    sensors = response.json()
    if not sensors:
        print("Aucun capteur trouvé.")
        return None

    sensor_id = list(sensors.keys())[0]
    temp_url = f"{BASE_URL}/sensors/{sensor_id}/get_temperature"

    temp_response = requests.get(temp_url)
    if temp_response.status_code != 200:
        print("Erreur température :", temp_response.text)
        return None

    temp_data = temp_response.json()
    return temp_data.get("value")


def append_to_json(entry, filename):
    """Ajoute une ligne dans un fichier JSON sous forme de liste."""
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
            else:
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def run_MAX_T():
    """
    Mesure en continu toutes les 15 sec.
    Toutes les 15 minutes -> calcule la valeur max et l’écrit dans MAX_temp_flow.json
    """
    INTERVAL = 15       # 15 sec
    WINDOW_DURATION = 15*60 # 15 minutes -> 900 sec
    NB_MEASURES = WINDOW_DURATION // INTERVAL  # = 60 mesures

    print("Lancement du flot MAX-T… (Ctrl+C pour arrêter)")

    while True:
        values = []  # valeurs collectées pendant les 15 minutes

        print("\n--- Nouvelle fenêtre de 15 minutes ---")

        for i in range(NB_MEASURES):
            temp = get_temperature()

            if temp is not None:
                print(f"Mesure {i+1}/{NB_MEASURES} : {temp}°C")
                values.append(temp)
            else:
                print(f"Mesure {i+1}/{NB_MEASURES} ignorée (erreur).")

            time.sleep(INTERVAL)

        # Quand les 15 minutes sont passées → on calcule MAX
        if values:
            max_temp = max(values)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            entry = {
                "datetime": now,
                "max_temperature": max_temp
            }

            append_to_json(entry, OUTPUT_FILE)

            print("\n=== MAX calculé ===")
            print("Heure :", now)
            print("MAX-T :", max_temp, "°C")
            print(f"Donné ajouté à {OUTPUT_FILE}")

        else:
            print("Aucune valeur valide pendant ces 15 minutes.")


def main():
    run_MAX_T()


if __name__ == "__main__":
    main()
