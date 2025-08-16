
def Feedback():
    import streamlit as st
    import pandas as pd
    from datetime import datetime
    import os
    import time

    st.set_page_config("User Feedback Form", layout="centered")

    st.title("📋 User Feedback Form")

    # CSV file path
    file_path = "feedback_responses.csv"

    # Define consistent column headers
    columns = [
        "Timestamp", "Name", "Email", "User Type", "Usage", "Features Used",
        "Overall Rating", "Design Rating", "Speed Rating", "Alert Accuracy",
        "Liked Most", "Issues Faced", "Suggestions",
        "Bug Reported", "Bug Description", "Bug Time"
    ]

    # --- Feedback Form ---
    with st.form("feedback_form", clear_on_submit=True):
        st.header(" User Info")
        name = st.text_input("Name *")
        email = st.text_input("Email")

        user_type = st.selectbox("You are a:", ["Student", "Professional", "Other"])
        usage = st.radio("How often do you use this app?", ["Daily", "Weekly", "Occasionally"])

        st.header("⭐ Ratings")
        features = st.multiselect("Which features did you use?", ["Live Alerts", "Maps", "Weather", "Nearby Services"])
        overall = st.slider("Overall Satisfaction", 1, 5, 3)
        design = st.slider("Design & UI", 1, 5, 3)
        speed = st.slider("Speed", 1, 5, 3)
        accuracy = st.slider("Alert Accuracy", 1, 5, 3)

        st.header("💬 Feedback")
        liked = st.text_area("What did you like most?")
        issues = st.text_area("Any issues faced?")
        suggestions = st.text_area("Suggestions for improvement")

        
        
        st.header("🐞 Bug Report (Optional)")
        bug_reported = st.checkbox("Did you face a bug?")
        bug_desc = ""
        bug_time = ""
        if bug_reported:
            bug_desc = st.text_area("Describe the bug")
            bug_time = st.time_input("What time did the bug occur?")

        submitted = st.form_submit_button("Submit Feedback")
        
        
    # --- Submission Logic ---
    if submitted:
        if name.strip() == "":
            st.error("⚠️ Please enter your name before submitting.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            feedback_data = {
                "Timestamp": timestamp,
                "Name": name,
                "Email": email,
                "User Type": user_type,
                "Usage": usage,
                "Features Used": ", ".join(features),
                "Overall Rating": overall,
                "Design Rating": design,
                "Speed Rating": speed,
                "Alert Accuracy": accuracy,
                "Liked Most": liked,
                "Issues Faced": issues,
                "Suggestions": suggestions,
                "Bug Reported": bug_reported,
                "Bug Description": bug_desc,
                "Bug Time": str(bug_time) if bug_reported else ""
            }

            # Create DataFrame and save to CSV
            df = pd.DataFrame([feedback_data], columns=columns)

            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            st.success("✅ Thank you! Your feedback has been submitted.")
            st.toast("Refreshing for next response...", icon="🔄")
            time.sleep(2)
            st.rerun()

    # --- Admin Section: Password Protected ---
    st.header("🔐 Admin Panel - View Feedback")

    with st.expander("Admin Login"):
        password = st.text_input("Enter Admin Password", type="password")
        if password == "admin123":  # Change this password securely
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path, on_bad_lines='warn')
                    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
                    unique_dates = df["Timestamp"].dt.date.unique()

                    selected_date = st.date_input(
                        "📅 Filter by Date",
                        value=datetime.today().date(),
                        min_value=min(unique_dates),
                        max_value=max(unique_dates)
                    )

                    filtered_df = df[df["Timestamp"].dt.date == selected_date]
                    st.write(f"Showing responses for: **{selected_date}**")
                    st.dataframe(filtered_df, use_container_width=True)

                except Exception as e:
                    st.error(f"Error reading the CSV: {e}")
            else:
                st.info("No feedback submitted yet.")
        elif password != "":
            st.error("❌ Incorrect password.")


Feedback()
