
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.markdown(
    "<h1 style='text-align: center; color: red;'>AwareNow</h1>",
    unsafe_allow_html=True
)

USER_LOGINS_FILE_CSV = 'user_logins_awarenow.csv'
USER_LOGINS_FILE_EXCEL = 'user_logins_awarenow.xlsx'


FIRST_NAMES = ["Arnav", "Renee", "Madhav", "Lakshay", "Vidur", "Advika", "Prisha", "Ehsaan", "Yashvi", "Mannat"]
LAST_NAMES = ["Dayal", "Virk", "Wason", "Seth", "Toor", "Rao", "Sura", "Shah", "Ramachandran", "Krishnan"]

ADMIN_ID = "admin"
ADMIN_PASSWORD = "password123"


def read_user_logins():
    try:
        return pd.read_csv(USER_LOGINS_FILE_CSV)
    except FileNotFoundError:
      
        return pd.DataFrame(columns=['user_id', 'first_name', 'last_name', 'age', 'location', 'email', 'password', 'login_time', 'logout_time', 'feedback'])

def append_new_user(email, password):     


    df = read_user_logins()            #Reads current users.

    new_user_id = df['user_id'].max() + 1 if not df.empty else 1001  # Creates a new user ID: either max(existing IDs) + 1 or 1001 if no users yet.

   
    new_first_name = random.choice(FIRST_NAMES)
    new_last_name = random.choice(LAST_NAMES)
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

    new_user_data = {
        'user_id': new_user_id,
        'first_name': new_first_name,
        'last_name': new_last_name,
        'age': '',
        'location': '',
        'email': email,
        'password': password,
        'login_time': current_time,
        'logout_time': '',
        'feedback': ''
    }

    df = pd.concat([df, pd.DataFrame([new_user_data])], ignore_index=True)

    try:
        df.to_csv(USER_LOGINS_FILE_CSV, index=False)
        df.to_excel(USER_LOGINS_FILE_EXCEL, index=False)
        st.success(f"Registration successful for {new_first_name} {new_last_name}! You can now log in.")
        return True
    except PermissionError:
        st.error(f"Permission denied: Unable to write to user data files. Please close any open files and try again.")
        return False
    except Exception as e:
        st.error(f"An error occurred while saving the user data: {e}")
        return False


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_email = None
    st.session_state.language_selected = False

if not st.session_state.language_selected:
    st.markdown(
    "<h3 style='text-align: center; color: grey;'>Real-Time Local Alert and Safety Information System</h3>",
    unsafe_allow_html=True
)


    lang = st.selectbox("Select Language", (" --Select -- ", "English", "हिन्दी", "मराठी"))
    if st.button("Get Started") and lang != " --Select -- ":
        st.session_state.language_selected = True
        st.session_state.lang_code = {"English": "en", "हिन्दी": "hi", "मराठी": "mr"}.get(lang, "en")
        st.rerun()
    st.stop()
else:
    st.title("AwareNow")   
    st.markdown("Real-Time Local Alert and Safety Information System")


if not st.session_state.logged_in:
    st.subheader("User and Admin Portal")
    choice = st.radio("Select your role:", ('Admin', 'User'), key='role_choice')

    if choice == 'Admin':
        with st.form("admin_form"):
            admin_id = st.text_input("Admin ID")
            admin_password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if admin_id == ADMIN_ID and admin_password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'Admin'
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Invalid Admin ID or Password")

    elif choice == 'User':
        user_choice = st.radio("Choose an option:", ('Login', 'Register'), key='user_option')

        if user_choice == 'Login':
            with st.form("user_login_form"):
                user_email = st.text_input("Email")
                user_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    df = read_user_logins()
                    user_row = df[(df['email'] == user_email) & (df['password'] == user_password)]
                    if not user_row.empty:
                        st.session_state.logged_in = True
                        st.session_state.user_type = 'User'
                        st.session_state.user_email = user_email
                        st.success("User login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        elif user_choice == 'Register':
            with st.form("user_register_form"):
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                if st.form_submit_button("Register"):
                    if not new_email or not new_password:
                        st.error("Email and password cannot be empty.")
                    else:
                        df = read_user_logins()
                        if new_email in df['email'].values:
                            st.error("This email is already registered. Please login.")
                        else:
                            append_new_user(new_email, new_password)
else:

    st.sidebar.header(f"Logged in as: {st.session_state.user_type}")
    if st.session_state.user_type == 'User':
        st.sidebar.text(f"Email: {st.session_state.user_email}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.user_email = None
        st.rerun()

    if st.session_state.user_type == 'Admin':
        st.header("Admin Dashboard")
    elif st.session_state.user_type == 'User':
        st.header("User Dashboard")
        st.success(f"Welcome, {st.session_state.user_email}! You have successfully logged in.")


























