import requests
from datetime import datetime
import json


BASE_URL = "http://10.194.69.214:3671"

def get_temperature():
    response = requests.get(f"{BASE_URL}/sensors/get_sensors_list")
    if response.status_code != 200:
        print("Erreur en lisant la liste des capteurs :", response.text)
        return None

    sensors = response.json()
    if not sensors:
        print("Aucun capteur trouvé.")
        return None

    sensor_id = list(sensors.keys())[0]
    temperature_url = f"{BASE_URL}/sensors/{sensor_id}/get_temperature"
    temp_response = requests.get(temperature_url)
    if temp_response.status_code != 200:
        print("Erreur en lisant la température :", temp_response.text)
        return None

    temp_data = temp_response.json()
    return temp_data.get("value")

def main():
    print("status de votre requete")
    print("200 - ok")
    print("4XX - client-side error")
    temperature_value = get_temperature()
    if temperature_value is not None:
        print("Valeur de temperature (°C) :", temperature_value)

if __name__ == "__main__":
    main()
