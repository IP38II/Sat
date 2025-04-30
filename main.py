import time
from time import sleep
import subprocess
import requests
import os
import folium
import webbrowser

def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux and macOS
        os.system('clear')

# Option 1: View ISS Position
def ISSLOC():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    clear_screen()

    print(f"ISS Position:\nLatitude: {data['iss_position']['latitude']}, Longitude: {data['iss_position']['longitude']}\n")
    input("Press Enter to return to the main menu...")
    main()

# Option 2: Track ISS on Map
def isst():
    clear_screen()
    print("Loading ISS position on map...")
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    lat = float(data['iss_position']['latitude'])
    lon = float(data['iss_position']['longitude'])

    m = folium.Map(location=[lat, lon], zoom_start=2)
    folium.Marker([lat, lon], tooltip="ISS").add_to(m)
    map_file = "iss_map.html"
    m.save(map_file)
    webbrowser.open(map_file)

    input("Map opened in your browser. Press Enter to return to the main menu...")
    main()

# Option 3: People in Space
def ppls():
    clear_screen()
    print("People currently in space:\n")
    try:
        response = requests.get("http://api.open-notify.org/astros.json", timeout=10)  # <-- timeout added
        response.raise_for_status()  # Raise an error for bad HTTP status
        data = response.json()

        for person in data['people']:
            print(f"{person['name']} on {person['craft']}")
        
        print(f"\nTotal: {data['number']} people in space.")
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")
    
    input("\nPress Enter to return to the main menu...")
    main()


# Option 4: View Satellite Data (Mock-up using CelesTrak TLE)
def satd():
    clear_screen()
    print("This feature fetches TLE data from CelesTrak.")
    print("Example satellite: ISS (ZARYA)")

    tle_url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(tle_url)
    tle_data = response.text

    print("\nFirst few lines of TLE data:\n")
    lines = tle_data.strip().splitlines()
    for i in range(0, 6, 3):  # Show just the first satellite
        print(lines[i])
        print(lines[i + 1])
        print(lines[i + 2])
    
    input("\nPress Enter to return to the main menu...")
    main()

# Option 5: Space Weather (from NOAA SWPC)
def wd():
    clear_screen()
    print("Recent space weather alerts (from NOAA):\n")
    try:
        response = requests.get("https://services.swpc.noaa.gov/products/alerts.json")
        alerts = response.json()

        if not alerts:
            print("No recent alerts.")
        else:
            for alert in alerts[-5:]:  # Show last 5 alerts
                print(f"- {alert['message']}")

    except Exception as e:
        print(f"Failed to fetch space weather: {e}")

    input("\nPress Enter to return to the main menu...")
    main()

# Main Menu
def main():
    clear_screen()
    print("Welcome to the SAT Project Tool")
    print("\nMenu:")
    print("1 - View where the ISS is")
    print("2 - Live ISS Tracking on a Map")
    print("3 - List All People Currently in Space")
    print("4 - View Satellite Details")
    print("5 - View Space Weather Data")
    
    choice = input("Select an option: ")

    if choice == "1":
        ISSLOC()
    elif choice == "2":
        isst()
    elif choice == "3":
        ppls()
    elif choice == "4":
        satd()
    elif choice == "5":
        wd()
    else:
        print("Invalid option selected.")
        sleep(1.5)
        main()

if __name__ == "__main__":
    main()
