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
from upload_test import add_test, save_uploaded_file, is_valid_date

st.set_page_config(layout="wide")

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
if 'upload_page' not in st.session_state:
    st.session_state['upload_page'] = False

def home():
    st.title("Welcome to ECG-APP")
    if st.sidebar.button("Login"):
        st.session_state['current_page'] = 'login'
        st.rerun()
    if st.sidebar.button("Register"):
        st.session_state['current_page'] = 'register'
        st.rerun()

def login_page():
    login()
    if st.session_state['user'] is not None:
        st.session_state['current_page'] = 'app'
        st.rerun()


def register_page():
    register()
    if st.session_state['user'] is not None:
        st.session_state['current_page'] = 'app'
        st.rerun()


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
            st.rerun()
        else:
            st.error("Please fill in all fields and upload a picture.")

    if st.button("Cancel"):
        st.session_state['current_page'] = 'app'
        st.rerun()


def upload_page(subject_id):
    st.title("Upload New Test")

    uploaded_file = st.file_uploader("Choose a file", type=["fit", "txt", "csv"])
    test_date = st.text_input("Test Date (dd.mm.yyyy)")

    if st.button("Save Upload"):
        if uploaded_file and is_valid_date(test_date):
            save_directory = "data/other_tests/"
            if save_uploaded_file(uploaded_file, save_directory):
                add_test(subject_id, uploaded_file, test_date)
                st.session_state['upload_page'] = False
                st.session_state['current_page'] = 'app'
                st.rerun()
        else:
            st.error("Please upload a file and enter a valid date.")

def subject_mode():
    user = st.session_state['user']
    #st.title("ECG-APP")
    #st.write(f"Logged in as {user['username']} ({user['role']})")

    # Load basic data
    person_dict = Person.load_person_data()
    person_names = Person.get_person_list(person_dict, user)  # Pass the current user to filter the list

    sf_basic = 500

    # Sidebar
    st.sidebar.header("Navigation")
    current_subject = st.sidebar.radio('Subject:', options=person_names, key="sbVersuchsperson")
    for entry in person_dict:
        if current_subject == entry["lastname"] + ", " + entry["firstname"]:
            subject = Person(entry)

    if st.sidebar.button("Add New Subject"):
        st.session_state['current_page'] = 'add_subject'
        st.rerun()

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

        # Add a button to navigate to the upload page
        if st.button("Upload New Test"):
            st.session_state['upload_page'] = True
            st.session_state['subject_id'] = subject.id
            st.rerun()

    if subject_ecg:
        with selected_tab[1]:
            list_of_paths = [element['result_link'] for element in subject_ecg]
            selected_ecg_path = st.selectbox('ECG:', options=list_of_paths, key="sbECG")
            if selected_ecg_path:
                df_ecg_data = ECGdata.read_ecg_data(selected_ecg_path)
                peaks = ECGdata.find_peaks(selected_ecg_path)
                st.plotly_chart(ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf_basic))

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
    tabs = st.tabs(["Permissions", "User Management", "Edit User Info"])

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
        usernames = [user['username'] for user in user_data if user['username'] != 'Admin']

        selected_user = st.radio("Select User to Delete", options=usernames)

        if selected_user:
            st.write(f"Deleting user: {selected_user}")
            if st.button("Delete User"):
                st.session_state['confirm_delete'] = selected_user

        if 'confirm_delete' in st.session_state and st.session_state['confirm_delete'] == selected_user:
            if st.button("Are you sure you want to delete this user?"):
                permissions.delete_user(selected_user)
                st.success("User deleted successfully!")
                del st.session_state['confirm_delete']
                st.rerun()
            if st.button("Cancel"):
                del st.session_state['confirm_delete']

    with tabs[2]:
        st.header("Edit User Info & Manage Tests")
        person_dict = Person.load_person_data()
        person_names = [f"{entry['lastname']}, {entry['firstname']}" for entry in person_dict if
                        entry["id"] not in Person.DEFAULT_SUBJECT_IDS]
        selected_subject = st.selectbox('Select Subject:', options=person_names, key="sbEditSubject")

        if selected_subject:
            for entry in person_dict:
                if selected_subject == entry["lastname"] + ", " + entry["firstname"]:
                    subject = Person(entry)
                    break

            st.write(f"Editing {subject.firstname} {subject.lastname}")
            new_firstname = st.text_input("First Name", value=subject.firstname)
            new_lastname = st.text_input("Last Name", value=subject.lastname)
            new_date_of_birth = st.number_input("Date of Birth", min_value=1900, max_value=2023, step=1,
                                                value=subject.date_of_birth)
            new_sex = st.selectbox("Sex", ["male", "female"], index=0 if subject.sex == "male" else 1)

            if st.button("Save Changes"):
                subject.firstname = new_firstname
                subject.lastname = new_lastname
                subject.date_of_birth = new_date_of_birth
                subject.sex = new_sex
                permissions.update_subject(subject)
                st.success("Subject information updated successfully!")
                st.rerun()

            st.write("### ECG Tests")
            for test in subject.ecg_tests:
                st.write(f"Test ID: {test['id']}, Date: {test['date']}")
                if st.button(f"Delete Test {test['id']}", key=f"del_{test['id']}"):
                    subject.ecg_tests.remove(test)
                    permissions.update_subject(subject)
                    st.success(f"Test {test['id']} deleted successfully!")
                    st.rerun()


def app():
    user = st.session_state['user']
    st.title("ECG-APP")
    st.write(f"Logged in as {user['username']} ({user['role']})")

    # Logout button
    if st.button("Logout"):
        st.session_state['user'] = None
        st.session_state['current_page'] = 'home'
        st.rerun()

    if user['role'] == 'admin':
        st.sidebar.header("Admin Mode")
        admin_mode = st.sidebar.toggle("Admin Mode", key="admin_mode", value=True)

        if admin_mode == False:
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
    if st.session_state.get('upload_page', False):
        upload_page(st.session_state['subject_id'])
    else:
        app()
