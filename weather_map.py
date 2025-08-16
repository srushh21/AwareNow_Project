import streamlit as st
      
st.subheader("Live Map")
st.markdown("""
        <style>
        .fullscreen-map iframe {
            width: 100%;
            height: 90vh;
            border: none;
            border-radius: 10px;
        }
        </style>
        <div class="fullscreen-map">
            <iframe src="https://openweathermap.org/weathermap?basemap=map&cities=true&layer=precipitation&lat=20.5937&lon=78.9629&zoom=4" 
                    allowfullscreen></iframe>
        </div>
        """, unsafe_allow_html=True)


