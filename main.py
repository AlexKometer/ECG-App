import numpy as np
import streamlit as st
from PIL import Image
from classes import Person
from ecgdata import ECGdata
from create_plot import ecg_plot
from login import login, register
import os
import json
import permissions  # Import the permissions module

st.set_page_config(layout="wide")
DEFAULT_SUBJECT_IDS = {1, 2, 3}

# Secret credentials
# ADMIN ACCOUNT: Username: Admin, Password: PycharmisLOVE!

# Initialize session state
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'show_register' not in st.session_state:
    st.session_state['show_register'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'admin_mode' not in st.session_state:
    st.session_state['admin_mode'] = 'subject'

def home():
    st.title("Welcome to ECG-APP")
    if st.sidebar.button("Login"):
        st.session_state['current_page'] = 'login'
        st.experimental_rerun()
    if st.sidebar.button("Register"):
        st.session_state['current_page'] = 'register'
        st.experimental_rerun()

def login_page():
    login()
    if st.session_state['user'] is not None:
        st.session_state['current_page'] = 'app'
        st.experimental_rerun()

def register_page():
    register()
    if st.session_state['user'] is not None:
        st.session_state['current_page'] = 'app'
        st.experimental_rerun()

def add_subject_page():
    st.title("Add New Subject")

    new_id = permissions.get_next_id()
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    date_of_birth = st.number_input("Date of Birth", min_value=1900, max_value=2023, step=1)
    sex = st.selectbox("Sex", ["male", "female"])
    picture = st.file_uploader("Upload Picture", type=["jpg", "png"])

    if st.button("Save Subject"):
        if picture and firstname and lastname and date_of_birth:
            picture_path = permissions.save_picture(picture, firstname, lastname)
            new_subject = {
                "id": new_id,
                "date_of_birth": date_of_birth,
                "firstname": firstname,
                "lastname": lastname,
                "sex": sex,
                "picture_path": picture_path,
                "ekg_tests": []
            }
            permissions.save_new_subject(new_subject, st.session_state['user']['username'])
            st.success("Subject added successfully!")
            st.session_state['current_page'] = 'app'
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields and upload a picture.")

def subject_mode():
    user = st.session_state['user']
    st.title("ECG-APP")
    st.write(f"Logged in as {user['username']} ({user['role']})")

    # Load basic data
    person_dict = Person.load_person_data()
    person_names = Person.get_person_list(person_dict, user)  # Pass the current user to filter the list

    sf = 500

    # Sidebar
    st.sidebar.header("Navigation")
    current_subject = st.sidebar.radio('Subject:', options=person_names, key="sbVersuchsperson")
    for entry in person_dict:
        if current_subject == entry["lastname"] + ", " + entry["firstname"]:
            subject = Person(entry)

    if st.sidebar.button("Add New Subject"):
        st.session_state['current_page'] = 'add_subject'
        st.experimental_rerun()

    st.sidebar.write("")
    checkbox_mark_peaks = st.sidebar.checkbox("Mark Peaks", value=False, key="cbMarkPeaks")

    subject_ecg = subject.ecg_tests

    if subject_ecg:
        tabs = ["General Information", "ECG", "HR Analysis", "HRV Analysis"]
    else:
        tabs = ["General Information"]

    selected_tab = st.tabs(tabs)

    with selected_tab[0]:
        st.write("#### General Information:", current_subject)

        image = Image.open(subject.get_image_path())
        st.image(image, caption=current_subject)
        st.write("The Year of Birth is: ", subject.date_of_birth)
        st.write("The age of the subject is: ", subject.calculate_person_age())
        st.write("")
        st.write("### Number of ECGs: ", len(subject_ecg))

        for i in range(len(subject_ecg)):
            current_ecg = ECGdata(subject_ecg[i])
            st.write("")
            st.write("Test date: ", current_ecg.date, ":")
            st.write("ECG " + str(i + 1) + ": ", current_ecg.data)
            st.write("Length of the test in seconds: ",
                     int(np.round(len(ECGdata.read_ecg_data(current_ecg.data)) / 500, 0)))

    if subject_ecg:
        with selected_tab[1]:
            list_of_paths = [element['result_link'] for element in subject_ecg]
            selected_ecg_path = st.selectbox('ECG:', options=list_of_paths, key="sbECG")
            if selected_ecg_path:
                df_ecg_data = ECGdata.read_ecg_data(selected_ecg_path)
                peaks = ECGdata.find_peaks(selected_ecg_path)
                st.plotly_chart(ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf))

                for element in subject_ecg:
                    if selected_ecg_path == element['result_link']:
                        ecg_date = element['date']

                st.write("This ecg was recorded on: ", ecg_date)
            else:
                st.write("No ECG data available for this subject.")

        with selected_tab[2]:
            st.write("This is tab 3")
            if len(peaks[0]) > 0:  # Check if there are any peaks
                hr, hr_max, hr_min, hr_mean = ECGdata.estimate_hr(peaks)
                st.write("The maximum heart rate is: ", hr_max)
                st.write("The minimum heart rate is: ", hr_min)
                st.write("The mean heart rate is: ", hr_mean)
                st.write("The estimated maximum heart rate is:", subject.max_hr)
            else:
                st.write("No ECG peaks data available for this subject.")

        with selected_tab[3]:
            if len(peaks[0]) > 0:  # Check if there are any peaks
                st.write("This is tab 4")
                st.write("HRV Analysis")
                hrv = ECGdata.calculate_hrv(peaks)
                st.write("The SDNN is: ", hrv[0])
                st.write("The RMSSD is: ", hrv[1])
            else:
                st.write("No ECG peaks data available for this subject.")

def admin_user_mode():
    st.title("User Editing Mode")
    tabs = st.tabs(["Permissions", "User Management"])

    with tabs[0]:
        st.header("Manage User Permissions")
        user_data = permissions.load_user_data()
        usernames = [user['username'] for user in user_data if user['username'] != 'Admin']

        selected_user = st.radio("Select User to Edit Permissions", options=usernames)

    if selected_user:
            st.write(f"Editing permissions for {selected_user}")

            person_data = Person.load_person_data()
            permissions_list = [
                f"{entry['lastname']}, {entry['firstname']}"
                for entry in person_data
                if entry["id"] not in Person.DEFAULT_SUBJECT_IDS
            ]
            current_permissions = permissions.get_user_permissions(selected_user)

            # Filter current_permissions to ensure they are in permissions_list
            valid_current_permissions = [perm for perm in current_permissions if perm in permissions_list]

            new_permissions = st.multiselect("Permissions", options=permissions_list, default=valid_current_permissions)

            if st.button("Update Permissions"):
                permissions.update_user_permissions(selected_user, new_permissions)
                st.success("Permissions updated successfully!")

    with tabs[1]:
        st.header("User Management")
        user_data = permissions.load_user_data()
        usernames = [user['username'] for user in user_data if user['username'] != 'admin']

        selected_user = st.selectbox("Select User to Delete", options=usernames)

        if selected_user:
            st.write(f"Deleting user: {selected_user}")
            if st.button("Delete User"):
                st.session_state['confirm_delete'] = selected_user

        if 'confirm_delete' in st.session_state and st.session_state['confirm_delete'] == selected_user:
            if st.button("Are you sure you want to delete this user?"):
                permissions.delete_user(selected_user)
                st.success("User deleted successfully!")
                del st.session_state['confirm_delete']
                st.experimental_rerun()
            if st.button("Cancel"):
                del st.session_state['confirm_delete']

def app():
    user = st.session_state['user']
    st.title("ECG-APP")
    st.write(f"Logged in as {user['username']} ({user['role']})")

    # Logout button
    if st.button("Logout"):
        st.session_state['user'] = None
        st.session_state['current_page'] = 'home'
        st.experimental_rerun()

    if user['role'] == 'admin':
        st.sidebar.header("Admin Mode")
        st.session_state['admin_mode'] = st.sidebar.selectbox(
            "Select Mode",
            options=['Subject Mode', 'User Editing Mode']
        )

        if st.session_state['admin_mode'] == 0:
            subject_mode()
        else:
            admin_user_mode()
    else:
        subject_mode()

# Page navigation
if st.session_state['current_page'] == 'home':
    home()
elif st.session_state['current_page'] == 'login':
    login_page()
elif st.session_state['current_page'] == 'register':
    register_page()
elif st.session_state['current_page'] == 'add_subject':
    add_subject_page()
elif st.session_state['current_page'] == 'app':
    app()
