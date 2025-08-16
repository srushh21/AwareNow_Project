
import streamlit as st

st.set_page_config(page_title="India Weather Heatmap", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'> India Weather Heatmap</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size: 16px; color: #555;'>Select a year to view the corresponding weather heatmap of India</p>",
    unsafe_allow_html=True
)

year = st.selectbox("Select Year", ["Select",2017,2018,2019,2020, 2021, 2022, 2023, 2024, 2025])

image_links = {
    2017:"https://www.skymetweather.com/content/wp-content/uploads/2017/09/29-09-2017-NLM-600-x-315.jpg",
    2018:"https://www.skymetweather.com/content/wp-content/uploads/2018/10/Seasonal-Rainfall-Se2c30-2018-1200-Excess-Rainfall-1-888x500.jpg",
    2019:"https://images.indianexpress.com/2019/06/monsoon-main.jpg",
    2020: "https://akm-img-a-in.tosshub.com/indiatoday/inline-images/Map_2.jpeg?VersionId=..3t.bHSUzdWOXzkwMtEsmtoz96y9F5H&size=750:*",
    2021 : "https://www.legacyias.com/wp-content/uploads/2021/10/image-52.png",
    2022: "https://akm-img-a-in.tosshub.com/aajtak/styles/medium_crop_simple/public/images/story/202204/whatsapp_image_2022-04-04_at_1.49.52_pm.jpeg",
    2023: "https://pbs.twimg.com/media/FzECl7yWcAE0KE5.jpg:large",
    2024: "https://akm-img-a-in.tosshub.com/indiatoday/styles/medium_crop_simple/public/2025-03/image003.jpg?VersionId=Nk7T1WaSMAevidQu.EvMugQkXAZj.s4b&size=750:*",
    2025: "https://akm-img-a-in.tosshub.com/indiatoday/styles/medium_crop_simple/public/2025-03/image004.jpg?VersionId=eABpVHjhpH_TzQH1M8UBPvN32AuhVfuU&size=750:*"
}

if year != "Select":
    st.markdown(
        f"<div style='text-align:center;'><span style='background-color:#1ABC9C; color:white; padding:6px 14px; border-radius:8px; font-size:16px;'>Selected Year: {year}</span></div>",
        unsafe_allow_html=True
    )

    img_path = image_links.get(year)
    if img_path:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-top: 20px;">
                <img src="{img_path}" alt="Weather Heatmap - {year}" 
                     style="border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); max-width: 95%;">
            </div>
            """,
            unsafe_allow_html=True
        )




























































