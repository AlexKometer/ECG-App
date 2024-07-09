import numpy as np
import streamlit as st
from PIL import Image
from classes import Person
from ecgdata import ECGdata
from create_plot import ecg_plot
import os
import json
import permissions  # Import the permissions module
from login import authenticate, register_user
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

#Home-Screen
def home():
    st.title("Welcome to ECG-APP")
    st.write("Please use the sidebar to login or register.")
    if st.session_state['user'] is None:
        if st.session_state['show_register']:
            sidebar_register()
        else:
            sidebar_login()
    else:
        st.sidebar.success("Logged in")

#Login-page
def sidebar_login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state['user'] = user
            st.session_state['current_page'] = 'app'
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")
    if st.sidebar.button("Register"):
        st.session_state['show_register'] = True
        st.rerun()

#Register -page
def sidebar_register():
    st.sidebar.header("Register")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = ["user"]
    if st.sidebar.button("Register"):
        if register_user(username, password, role):
            st.sidebar.success("User registered successfully!")
            st.session_state['show_register'] = False
            st.rerun()
        else:
            st.sidebar.error("Registration failed. Username may already be taken.")
    if st.sidebar.button("Back to Login"):
        st.session_state['show_register'] = False
        st.rerun()


#add new Subject
def add_subject_page():
    if st.session_state['user'] is None:
        st.session_state['current_page'] = 'home'
        st.rerun()

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


#upload new Test
def upload_page(subject_id):
    st.title("Upload New Test")

    uploaded_file = st.file_uploader("Choose a file", type=["fit", "txt", "csv"])
    test_date = st.text_input("Test Date (dd.mm.yyyy)")
    test_types = st.multiselect("Test Type", ["EKG", "fit", "VO2max test", "power data", "other"])

    if st.button("Save Upload"):
        if uploaded_file and is_valid_date(test_date) and test_types:
            save_directory = "data/other_tests/"
            if save_uploaded_file(uploaded_file, save_directory):
                add_test(subject_id, uploaded_file, test_date, test_types)  # Use test_types here
                st.session_state['upload_page'] = False
                st.session_state['current_page'] = 'app'
                st.rerun()
        else:
            st.error("Please upload a file, enter a valid date, and select at least one test type.")

    if st.button("Cancel"):
        st.session_state['upload_page'] = False
        st.session_state['current_page'] = 'app'
        st.rerun()



#Infomation about the subject
def subject_mode():
    user = st.session_state['user']

    person_dict = Person.load_person_data()
    print("Person dictionary:", person_dict)  # Debug print

    person_names = Person.get_person_list(person_dict, user)
    print("Person names:", person_names)  # Debug print

    sf = 500

    st.sidebar.header("Navigation")
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state['user'] = None
        st.session_state['current_page'] = 'home'
        st.rerun()

    if st.sidebar.button("Add New Subject", key="add_subject_button"):
        st.session_state['current_page'] = 'add_subject'
        st.rerun()

    current_subject = st.sidebar.selectbox('Subject:', options=person_names, key="sbVersuchsperson")
    print("Current subject:", current_subject)  # Debug print

    # Initialize subject to None
    subject = None

    for entry in person_dict:
        if current_subject == entry["lastname"] + ", " + entry["firstname"]:
            subject = Person(entry)

    if st.sidebar.button("Upload New Test", key="upload_test_button"):
        if subject:
            st.session_state['upload_page'] = True
            st.session_state['subject_id'] = subject.id
            st.rerun()

    if subject is None:
        st.write("No subject selected.")
        return

    st.sidebar.write("")
    checkbox_mark_peaks = st.sidebar.checkbox("Mark Peaks", value=False, key="cbMarkPeaks")

    subject_ecg = subject.ecg_tests
    print("Subject ECG tests:", subject_ecg)  # Debug print

    # Always add General Information tab
    tabs = ["General Information"]
    added_tabs = set()  # Keep track of added tabs

    if subject_ecg:
        for test in subject_ecg:
            for test_type in test["types"]:
                if test_type == "EKG" and "ECG Data" not in added_tabs:
                    tabs.extend(["Test Data", "ECG Data", "HRV Analysis"])
                    added_tabs.update(["ECG Data", "HRV Analysis"])
                elif test_type == "fit" and "Powercurve" not in added_tabs:
                    tabs.extend(["Test Data", "Powercurve"])
                    added_tabs.add("Powercurve")
                elif test_type == "VO2max test" and "VO2max Analysis" not in added_tabs:
                    tabs.extend(["Test Data", "VO2max Analysis"])
                    added_tabs.add("VO2max Analysis")
                elif test_type == "power data" and "Power Data" not in added_tabs:
                    tabs.extend(["Test Data", "Power Data"])
                    added_tabs.add("Power Data")
                elif test_type == "other" and "Test Data" not in added_tabs:
                    tabs.extend(["Test Data"])
                    added_tabs.add("Test Data")
                break

    selected_tab = st.tabs(tabs)

    with selected_tab[0]:
        st.write("#### General Information:", current_subject)

        image = Image.open(subject.get_image_path())
        st.image(image, caption=current_subject)
        st.write("The Year of Birth is: ", subject.date_of_birth)
        st.write("The age of the subject is: ", subject.calculate_person_age())
        st.write("")
        st.write("### Number of Tests: ", len(subject_ecg))

        for i in range(len(subject_ecg)):
            current_ecg = ECGdata(subject_ecg[i])
            st.write("")
            st.write("Test date: ", current_ecg.date, ":")
            st.write("Test type: ", ", ".join(current_ecg.types), ":")
            st.write("Test " + str(i + 1) + ": ", current_ecg.data)
            st.write("Length of the test in seconds: ",
                     int(np.round(len(ECGdata.read_ecg_data(current_ecg.data)) / 500, 0)))

    # Create a mapping of test type to tab index
    tab_indices = {tab_name: index for index, tab_name in enumerate(tabs)}

    peaks = None  # Initialize peaks

    if "ECG Data" in tabs:
        with selected_tab[tab_indices["ECG Data"]]:
            print("Subject ECG tests for ECG Data tab:", subject_ecg)  # Debug print
            list_of_paths = [element['result_link'] for element in subject_ecg if "EKG" in element["types"]]
            print("List of paths for ECG Data:", list_of_paths)  # Debug print

            # Check if there are any paths and set a default selection
            if list_of_paths:
                selected_ecg_path = st.selectbox('ECG:', options=list_of_paths, index=0, key="sbECG")
                print("Selected ECG path:", selected_ecg_path)  # Debug print
                if selected_ecg_path:
                    df_ecg_data = ECGdata.read_ecg_data(selected_ecg_path)
                    peaks = ECGdata.find_peaks(selected_ecg_path)
                    st.plotly_chart(ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf, key_suffix="ECG"))

                    for element in subject_ecg:
                        if selected_ecg_path == element['result_link']:
                            ecg_date = element['date']

                    st.write("This ECG was recorded on: ", ecg_date)
                else:
                    st.write("No ECG data available for this subject.")
            else:
                st.write("No ECG data available for this subject.")

    if "HRV Analysis" in tabs:
        with selected_tab[tab_indices["HRV Analysis"]]:
            st.write("This is tab 4")
            if peaks and len(peaks[0]) > 0:
                hr, hr_max, hr_min, hr_mean = ECGdata.estimate_hr(peaks)
                st.write("The maximum heart rate is: ", hr_max)
                st.write("The minimum heart rate is: ", hr_min)
                st.write("The mean heart rate is: ", hr_mean)
                st.write("The estimated maximum heart rate is:", subject.max_hr)
            else:
                st.write("No ECG peaks data available for this subject.")

            if peaks and len(peaks[0]) > 0:
                st.write("HRV Analysis")
                hrv = ECGdata.calculate_hrv(peaks)
                st.write("The SDNN is: ", hrv[0])
                st.write("The RMSSD is: ", hrv[1])
            else:
                st.write("No ECG peaks data available for this subject.")

    if "Powercurve" in tabs:
        with selected_tab[tab_indices["Powercurve"]]:
            st.write("Powercurve Analysis")
            # Add your powercurve visualization code here

    if "VO2max Analysis" in tabs:
        with selected_tab[tab_indices["VO2max Analysis"]]:
            st.write("VO2max Analysis")
            # Add your VO2max analysis code here

    if "Power Data" in tabs:
        with selected_tab[tab_indices["Power Data"]]:
            st.write("Power Data Analysis")
            # Add your power data visualization code here

    if "Test Data" in tabs and "General Information" not in tabs:
        with selected_tab[tab_indices["Test Data"]]:
            st.write("Other Test Data")
            # Add other test data visualization code here



#Admin User
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

#Login - Logout
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
        admin_mode = st.sidebar.radio(
            "Select Mode",
            options=['Subject Mode', 'User Editing Mode'],
            key='admin_mode'
        )

        if admin_mode == 'Subject Mode':
            subject_mode()
        else:
            admin_user_mode()
    else:
        subject_mode()


# Page navigation
if st.session_state['current_page'] == 'home':
    home()
elif st.session_state['show_register']:
    sidebar_register()
elif st.session_state['current_page'] == 'add_subject':
    add_subject_page()
elif st.session_state['current_page'] == 'app':
    if st.session_state.get('upload_page', False):
        upload_page(st.session_state['subject_id'])
    else:
        app()
else:
    sidebar_login()
