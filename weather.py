import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF

API_KEY = "c24f70a890c583d233cbd498262f6294"
CITY_FILE = "CITY_NAME.csv"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json()

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json()

def create_forecast_df(forecast_data):

    forecast_list = forecast_data["list"]
    records = []
    for f in forecast_list:
        dt = datetime.fromtimestamp(f["dt"])
        temp = f["main"]["temp"]
        rain = f.get("rain", {}).get("3h", 0)
        records.append({"Datetime": dt, "Temperature (°C)": temp, "Rainfall (mm)": rain})
    return pd.DataFrame(records)

def generate_alerts(weather_data):
    alerts = []
    main = weather_data.get("main", {})
    temp = main.get("temp")
    humidity = main.get("humidity")
    rain_data = weather_data.get("rain", {})
    rain_1h = rain_data.get("1h", 0) if rain_data else 0

    if temp and temp > 40:
        alerts.append("Heatwave Warning: Temperature exceeds 40°C.")
    if rain_1h and rain_1h > 10:
        alerts.append(f"Heavy Rain Alert: {rain_1h} mm rainfall expected in 1 hour.")
    if humidity and humidity > 85:
        alerts.append("High Humidity Alert: May feel more uncomfortable.")
    if not alerts:
        alerts.append("No significant weather alerts.")
    return alerts

def generate_pdf(city, weather_data, alerts):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Weather Report for {city}", ln=True, align="C")
    pdf.cell(200, 10, txt="", ln=True)

    for key, val in weather_data["main"].items():
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {val}", ln=True)
    pdf.cell(200, 10, txt=f"Wind Speed: {weather_data['wind']['speed']} km/h", ln=True)
    pdf.cell(200, 10, txt=f"Weather: {weather_data['weather'][0]['description'].capitalize()}", ln=True)

    if alerts:
        pdf.cell(200, 10, txt="Alerts:", ln=True)
        for alert in alerts:
            pdf.cell(200, 10, txt=f"  - {alert}", ln=True)

    filepath = f"{city}_weather_report.pdf"
    pdf.output(filepath)
    return filepath



st.set_page_config(page_title="India Weather Forecast", layout="wide")
st.title("India Weather Forecast with Rainfall Info")

cities = ["Select","Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Gujrat", "Punjab"]
city1 = st.selectbox("Select City", cities)

if st.button("Get Weather Forecast"):
    weather1 = get_weather(city1)
    forecast1 = get_forecast(city1)

    if "main" in weather1: 
        col1, col2 = st.columns(2)

        with col1:
            st.header(f" {city1}")
            st.metric("Temperature", f"{weather1['main']['temp']} °C")
            st.image(f"http://openweathermap.org/img/wn/{weather1['weather'][0]['icon']}@2x.png")
            st.write("**Description:**", weather1["weather"][0]["description"].capitalize())
            st.write("**Humidity:**", f"{weather1['main']['humidity']} %")
            st.write("**Wind Speed:**", f"{weather1['wind']['speed']} km/h")

            alerts1 = generate_alerts(weather1)
            if alerts1:
                st.warning(" Alerts:\n" + "\n".join(alerts1))

            if st.button("Download Report", key="1"):
                path = generate_pdf(city1, weather1, alerts1)
                with open(path, "rb") as file:
                    st.download_button("Download PDF", file, file_name=path)

        st.subheader(f"5-Day Forecast for {city1} (Temperature & Rainfall)")
        forecast_df = create_forecast_df(forecast1)
        fig = px.line(
            forecast_df,
            x="Datetime",
            y=["Temperature (°C)", "Rainfall (mm)"],
            labels={"value": "Value", "variable": "Metric"},
            title="Temperature & Rainfall Forecast"
        )
        st.plotly_chart(fig, use_container_width=True)





















































# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# from datetime import datetime
# from fpdf import FPDF

# API_KEY = "c24f70a890c583d233cbd498262f6294"
# # CITY_FILE = "CITY_NAME.csv"

# # --- Functions ---
# def get_weather(city):
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#     return requests.get(url).json()

# def get_forecast(city):
#     url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
#     return requests.get(url).json()

# def create_forecast_df(forecast_data):
#     records = []
#     for f in forecast_data["list"]:
#         dt = datetime.fromtimestamp(f["dt"])
#         temp = f["main"]["temp"]
#         rain = f.get("rain", {}).get("3h", 0)
#         records.append({"Datetime": dt, "Temperature (°C)": temp, "Rainfall (mm)": rain})
#     return pd.DataFrame(records)

# def generate_alerts(weather_data):
#     alerts = []
#     temp = weather_data.get("main", {}).get("temp")
#     humidity = weather_data.get("main", {}).get("humidity")
#     rain_1h = weather_data.get("rain", {}).get("1h", 0)

#     if temp and temp > 40:
#         alerts.append("Heatwave Warning: Temperature exceeds 40°C.")
#     if rain_1h and rain_1h > 10:
#         alerts.append(f"Heavy Rain Alert: {rain_1h} mm rainfall expected in 1 hour.")
#     if humidity and humidity > 85:
#         alerts.append("High Humidity Alert: May feel more uncomfortable.")
#     if not alerts:
#         alerts.append("No significant weather alerts.")
#     return alerts

# def generate_pdf(city, weather_data, alerts):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"Weather Report for {city}", ln=True, align="C")
#     pdf.ln(5)

#     for key, val in weather_data["main"].items():
#         pdf.cell(200, 10, txt=f"{key.capitalize()}: {val}", ln=True)
#     pdf.cell(200, 10, txt=f"Wind Speed: {weather_data['wind']['speed']} km/h", ln=True)
#     pdf.cell(200, 10, txt=f"Weather: {weather_data['weather'][0]['description'].capitalize()}", ln=True)

#     if alerts:
#         pdf.cell(200, 10, txt="Alerts:", ln=True)
#         for alert in alerts:
#             pdf.cell(200, 10, txt=f"  - {alert}", ln=True)

#     path = f"{city}_weather_report.pdf"
#     pdf.output(path)
#     return path

# # --- Streamlit App ---
# st.set_page_config(page_title="India Weather Forecast", layout="wide")
# st.title("India Weather Forecast with Rainfall Info")

# # Read cities from Excel
# try:
#     df_cities = pd.read_excel(CITY_FILE)
#     cities = ["Select"] + df_cities.iloc[:, 0].dropna().tolist()
# except Exception as e:
#     st.error(f"Error loading city file: {e}")
#     cities = ["Select", "Delhi", "Mumbai", "Bangalore"]

# city1 = st.selectbox("Select City", cities)

# if st.button("Get Weather Forecast") and city1 != "Select":
#     weather1 = get_weather(city1)
#     forecast1 = get_forecast(city1)

#     if "main" in weather1:
#         col1, col2 = st.columns(2)

#         # Current Weather
#         with col1:
#             st.header(f"{city1}")
#             st.metric("Temperature", f"{weather1['main']['temp']} °C")
#             st.image(f"http://openweathermap.org/img/wn/{weather1['weather'][0]['icon']}@2x.png")
#             st.write("**Description:**", weather1["weather"][0]["description"].capitalize())
#             st.write("**Humidity:**", f"{weather1['main']['humidity']} %")
#             st.write("**Wind Speed:**", f"{weather1['wind']['speed']} km/h")

#             alerts1 = generate_alerts(weather1)
#             for alert in alerts1:
#                 st.warning(alert)

#             if st.button("Download Report", key="1"):
#                 path = generate_pdf(city1, weather1, alerts1)
#                 with open(path, "rb") as file:
#                     st.download_button("Download PDF", file, file_name=path)

#         # 5-day Forecast
#         st.subheader(f"5-Day Forecast for {city1} (Temperature & Rainfall)")
#         forecast_df = create_forecast_df(forecast1)
#         fig = px.line(
#             forecast_df,
#             x="Datetime",
#             y=["Temperature (°C)", "Rainfall (mm)"],
#             labels={"value": "Value", "variable": "Metric"},
#             title="Temperature & Rainfall Forecast"
#         )
#         st.plotly_chart(fig, use_container_width=True)


