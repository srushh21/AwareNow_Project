def mlcrime(lang):
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import pickle as pkl
    from sklearn.preprocessing import LabelEncoder
    from sklearn.cluster import KMeans
    from geopy.geocoders import Nominatim
    import folium
    from streamlit_folium import st_folium
    from deep_translator import GoogleTranslator

    # Helper function for translation
    def translate_text(text):
        if lang == "en":
            return text
        try:
            return GoogleTranslator(source="en", target=lang).translate(text)
        except:
            return text

    # ---------------------
    # Load and clean data
    # ---------------------
    df = pd.read_csv("crime_dataset_india (3).csv")
    df['Date of Occurrence'] = pd.to_datetime(df['Date of Occurrence'], errors='coerce')
    df = df.dropna(subset=['City', 'Date of Occurrence', 'Crime Description'])

    if df.empty:
        st.error(translate_text("The dataset is empty after dropping missing values. Please check the input CSV file."))
        st.stop()

    x = df[['City', 'Date of Occurrence']].copy()
    x['Day'] = x['Date of Occurrence'].dt.day
    x['Month'] = x['Date of Occurrence'].dt.month
    x['Year'] = x['Date of Occurrence'].dt.year
    x = x.drop('Date of Occurrence', axis=1)

    le_city = LabelEncoder()
    x['City'] = le_city.fit_transform(x['City'])
    label_encoders = {'City': le_city}

    if x.empty:
        st.error(translate_text("Feature matrix is empty. No valid samples found for KMeans clustering."))
        st.stop()

    kmeans = KMeans(n_clusters=21, random_state=20)
    kmeans.fit(x)

    with open('model1.pkl', 'wb') as f:
        pkl.dump(kmeans, f)

    # ---------------------
    # Streamlit UI
    # ---------------------
    st.title(translate_text("Crime Clustering Analysis (India)"))
    st.subheader(translate_text("Predict Crime Type from City and Date"))

    # User Input
    city_input = st.text_input(translate_text("Enter City"))
    date_input = st.date_input(translate_text("Enter Date of Occurrence"))

    # Initialize session state variables
    if "crime_type" not in st.session_state:
        st.session_state.crime_type = None
        st.session_state.cluster = None
        st.session_state.location = None
        st.session_state.city_input = None

    # Predict button
    if st.button(translate_text("Predict Cluster")):
        if city_input and date_input:
            if city_input in le_city.classes_:
                encoded_city = le_city.transform([city_input])[0]
                day = date_input.day
                month = date_input.month
                year = date_input.year

                input_df = pd.DataFrame([[encoded_city, day, month, year]], columns=['City', 'Day', 'Month', 'Year'])

                with open('model1.pkl', 'rb') as f:
                    model_loaded = pkl.load(f)

                cluster = model_loaded.predict(input_df)[0]

                df['Cluster'] = kmeans.labels_
                most_common_crime = df[df['Cluster'] == cluster]['Crime Description'].mode()

                if not most_common_crime.empty:
                    crime_type = most_common_crime.iloc[0]
                    st.session_state.crime_type = crime_type
                    st.session_state.cluster = cluster
                    st.session_state.city_input = city_input

                    geolocator = Nominatim(user_agent="crime_app")
                    st.session_state.location = geolocator.geocode(city_input)
                else:
                    st.warning(translate_text("No matching crime description found for this cluster."))
                    st.stop()
            else:
                st.error(translate_text("City not found in training data. Please check spelling or try a different city."))
                st.stop()
        else:
            st.warning(translate_text("Please enter both city and date."))
            st.stop()

    # ---------------------
    # Show Prediction
    # ---------------------
    if st.session_state.crime_type and st.session_state.cluster is not None:
        st.success(
            translate_text(f"Predicted Crime Type: **{st.session_state.crime_type}** (Cluster {st.session_state.cluster})")
        )

        location = st.session_state.location
        if location:
            latitude = location.latitude
            longitude = location.longitude

            m = folium.Map(location=[latitude, longitude], zoom_start=12)
            folium.Marker(
                [latitude, longitude],
                popup=f"<b>{st.session_state.city_input}</b><br>{translate_text('Predicted Crime')}: <b>{st.session_state.crime_type}</b><br>Cluster: {st.session_state.cluster}",
                tooltip=translate_text("Click for prediction"),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

            st_folium(m, width=1200, height=600)
        else:
            st.warning(translate_text("Could not locate the city on the map."))
