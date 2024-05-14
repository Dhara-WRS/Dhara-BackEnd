import requests

ENDPOINT_URL = "https://eo50kupab21we1w.m.pipedream.net"

def send_location_to_endpoint(location_name, latitude, longitude):
    data = {"name": location_name, "Latitude": latitude, "Longitude": longitude}
    response = requests.post(ENDPOINT_URL, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        print("Location name sent successfully!")
    else:
        print(f"Failed to send location name. Status code: {response.status_code}")
    # print("Response:", response.content)


if __name__ == "__main__":
    location_name = "VITTAL NAGAR, KOTA, RAJASTHAN, INDIA"
    latitude = 25.7196
    longitude = 75.8577
    send_location_to_endpoint(location_name, latitude, longitude)
