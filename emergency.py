def Emergency():

    import streamlit as st
    from streamlit_geolocation import streamlit_geolocation
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    import requests
    import folium
    from streamlit_folium import folium_static
    import pandas as pd
    import numpy as np

    # --- Constants ---
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    HOSPITAL_SEARCH_RADIUS_KM = 2
    POLICE_SEARCH_RADIUS_KM = 5

    HOSPITAL_RADIUS_METERS = HOSPITAL_SEARCH_RADIUS_KM * 1000
    POLICE_RADIUS_METERS = POLICE_SEARCH_RADIUS_KM * 1000

    # --- Functions ---
    def get_nearby_places(latitude, longitude, tags, radius_meters):
        bbox_south = latitude - (radius_meters / 111111)  
        bbox_north = latitude + (radius_meters / 111111)
        bbox_west = longitude - (radius_meters / (111111 * abs(np.cos(np.radians(latitude)))))
        bbox_east = longitude + (radius_meters / (111111 * abs(np.cos(np.radians(latitude)))))

        query = f"""
        [out:json][timeout:25];
        (
        node{tags}(around:{radius_meters},{latitude},{longitude});
        way{tags}(around:{radius_meters},{latitude},{longitude});
        relation{tags}(around:{radius_meters},{latitude},{longitude});
        );
        out center;
        """
        try:
            response = requests.post(OVERPASS_API_URL, data=query)
            response.raise_for_status()
            data = response.json()
            places = []
            for element in data['elements']:
                lat = element.get('lat', element['center']['lat'] if 'center' in element else None)
                lon = element.get('lon', element['center']['lon'] if 'center' in element else None)
                if lat is not None and lon is not None:
                    name = element.get('tags', {}).get('name', 'Unknown')
                    address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'N/A'))
                    places.append({'name': name, 'lat': lat, 'lon': lon, 'address': address})
            return places
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from OpenStreetMap: {e}")
            return []

    def display_map(user_location, hospitals, police_stations):
        if user_location and user_location['latitude'] and user_location['longitude']:
            m = folium.Map(location=[user_location['latitude'], user_location['longitude']], zoom_start=14)

            # User location marker
            folium.Marker(
                location=[user_location['latitude'], user_location['longitude']],
                popup="Your Location",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

            # Hospitals
            for hospital in hospitals:
                folium.Marker(
                    location=[hospital['lat'], hospital['lon']],
                    popup=f"Hospital: {hospital['name']}<br>Address: {hospital['address']}",
                    icon=folium.Icon(color="red", icon="medkit")
                ).add_to(m)

            # Police Stations
            for police_station in police_stations:
                folium.Marker(
                    location=[police_station['lat'], police_station['lon']],
                    popup=f"Police Station: {police_station['name']}<br>Address: {police_station['address']}",
                    icon=folium.Icon(color="darkblue", icon="shield")
                ).add_to(m)

            folium_static(m)
        else:
            st.warning("Could not get your location to display the map.")

    # --- Streamlit App ---
    st.set_page_config(layout="wide")
    st.title("Nearby Emergency Services (India)")

    st.markdown("""
        This app detects your current location and shows nearby hospitals and police stations
        within a specified radius in India.
    """)

    # Location input method
    location_option = st.radio(
        "Choose your location input method:",
        ("Use Live Location", "Enter City Manually")
    )

    user_lat = None
    user_lon = None
    user_location_display_text = ""

    if location_option == "Use Live Location":
        st.info("Please allow location access when prompted by your browser.")
        location = streamlit_geolocation()

        if location and location['latitude'] and location['longitude']:
            user_lat = location['latitude']
            user_lon = location['longitude']
            user_location_display_text = f"Your current location: Latitude {user_lat:.4f}, Longitude {user_lon:.4f}"
        else:
            st.warning("Waiting for location access... Please click 'Allow' in your browser if prompted.")
            st.info("If location access is denied or not available, the map and nearby places won't be displayed.")

    elif location_option == "Enter City Manually":
        city_name = st.text_input("Enter city name (e.g., Mumbai, Delhi):", "")
        if city_name:
            geolocator = Nominatim(user_agent="emergency_services_app")
            try:
                location_by_city = geolocator.geocode(city_name, country_codes='in')
                if location_by_city:
                    user_lat = location_by_city.latitude
                    user_lon = location_by_city.longitude
                    user_location_display_text = f"Location for {city_name}: Latitude {user_lat:.4f}, Longitude {user_lon:.4f}"
                else:
                    st.error(f"Could not find coordinates for '{city_name}'. Please try a different city name.")
            except Exception as e:
                st.error(f"Error during geocoding: {e}. Please try again.")

    # If location is found
    if user_lat is not None and user_lon is not None:
        st.write(user_location_display_text)

        # Hospitals
        st.subheader(f"Hospitals within {HOSPITAL_SEARCH_RADIUS_KM} km:")
        hospital_tags = '["amenity"="hospital"]'
        hospitals = get_nearby_places(user_lat, user_lon, hospital_tags, HOSPITAL_RADIUS_METERS)

        if hospitals:
            hospital_data_raw = []
            for hosp in hospitals:
                distance = geodesic((user_lat, user_lon), (hosp['lat'], hosp['lon'])).km
                hospital_data_raw.append({
                    'Name': hosp['name'],
                    'Address': hosp['address'],
                    'Distance_Raw': distance
                })
            hospital_data_raw.sort(key=lambda x: x['Distance_Raw'])

            hospital_data_display = []
            for hosp_raw in hospital_data_raw:
                hospital_data_display.append({
                    'Name': hosp_raw['Name'],
                    'Address': hosp_raw['Address'],
                    'Distance (km)': f"{hosp_raw['Distance_Raw']:.2f}"
                })
            df_hospitals = pd.DataFrame(hospital_data_display)
            st.dataframe(df_hospitals, use_container_width=True)
        else:
            st.info(f"No hospitals found within {HOSPITAL_SEARCH_RADIUS_KM} km of your location.")

        # Police Stations
        st.subheader(f"Police Stations within {POLICE_SEARCH_RADIUS_KM} km:")
        police_tags = '["amenity"="police"]'
        police_stations = get_nearby_places(user_lat, user_lon, police_tags, POLICE_RADIUS_METERS)

        if police_stations:
            police_data_raw = []
            for police in police_stations:
                distance = geodesic((user_lat, user_lon), (police['lat'], police['lon'])).km
                police_data_raw.append({
                    'Name': police['name'],
                    'Address': police['address'],
                    'Distance_Raw': distance
                })
            police_data_raw.sort(key=lambda x: x['Distance_Raw'])

            police_data_display = []
            for police_raw in police_data_raw:
                police_data_display.append({
                    'Name': police_raw['Name'],
                    'Address': police_raw['Address'],
                    'Distance (km)': f"{police_raw['Distance_Raw']:.2f}"
                })
            df_police = pd.DataFrame(police_data_display)
            st.dataframe(df_police, use_container_width=True)
        else:
            st.info(f"No police stations found within {POLICE_SEARCH_RADIUS_KM} km of your location.")

        # Map View
        st.subheader("Map View:")
        display_map({'latitude': user_lat, 'longitude': user_lon}, hospitals, police_stations)

    else:
        if location_option == "Enter City Manually" and not city_name:
            st.info("Please enter a city name to find emergency services.")
