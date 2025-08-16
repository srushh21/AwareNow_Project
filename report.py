
def report():
    import streamlit as st
    import pandas as pd
    from datetime import datetime
    import os

    st.set_page_config(page_title="Incident Reporter", layout="centered")
    st.title("📝 Report an Incident")

    # CSV file path
    CSV_FILE = "reports.csv"

    # --- Incident Report Form ---
    with st.form("incident_report_form"):
        category = st.selectbox("Select Incident Category", ["Crime", "Disaster", "Traffic", "Weather"])
        report_title = st.text_input("Incident Title")
        report_description = st.text_area("Description of the Incident")
        report_location = st.text_input("Location (e.g., Street, City, Pincode)")
        submitted = st.form_submit_button("Submit Report")

        if submitted:
            if report_title and report_description and report_location:
                report_data = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "category": category,
                    "title": report_title,
                    "description": report_description,
                    "location": report_location,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Save to CSV
                if os.path.exists(CSV_FILE):
                    df = pd.read_csv(CSV_FILE)
                    df = pd.concat([df, pd.DataFrame([report_data])], ignore_index=True)
                else:
                    df = pd.DataFrame([report_data])
                df.to_csv(CSV_FILE, index=False)

                st.success("✅ Your report has been submitted successfully!")
            else:
                st.error("❌ Please fill in all the fields.")

                