#RAINFALL

import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Weather Map", layout="wide")

API_KEY = "c24f70a890c583d233cbd498262f6294"
CITY = "Mumbai"

def fetch_coords(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}"
    data = requests.get(url).json()
    return data['coord']['lat'], data['coord']['lon'] if data.get("cod") == 200 else (None, None)

def add_layers(map_obj):
    layers = {
        "Clouds": "clouds_new",
        "Rain": "precipitation_new",
        "Wind": "wind_new"
    }
    for name, layer in layers.items():
        folium.raster_layers.TileLayer(
            tiles=f"https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
            attr="OpenWeatherMap", name=name, overlay=True
        ).add_to(map_obj)

st.title(" Rainfall Overlay")

if st.button("Show Rainfall Map"):
    lat, lon = fetch_coords(CITY)
    if lat and lon:
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], popup=CITY).add_to(m)
        add_layers(m)
        folium.LayerControl().add_to(m)
        folium_static(m, width=700, height=500)
    else:
        st.error("Unable to fetch location.")










