import numpy as np
import streamlit as st
from PIL import Image
from classes import Person
from ecgdata import EKGdata
from create_plot import ecg_plot
from login import login, register

st.set_page_config(layout="wide")

# Secret credentials
"""ADMIN ACCOUNT: Username: admin, Password: CodingisLOVE"""

# Initialize session state
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'show_register' not in st.session_state:
    st.session_state['show_register'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

def home():
    st.title("Welcome to ECG-APP")
    st.write("Please choose an option:")
    if st.button("Login"):
        st.session_state['current_page'] = 'login'
        st.experimental_rerun()  # Trigger a rerun immediately after setting the page
    if st.button("Register"):
        st.session_state['current_page'] = 'register'
        st.experimental_rerun()  # Trigger a rerun immediately after setting the page

def login_page():
    login()
    if st.session_state['user'] is not None:
        st.session_state['current_page'] = 'app'
        st.experimental_rerun()  # Trigger a rerun immediately after setting the page

def register_page():
    register()
    if st.session_state['user'] is not None:
        st.session_state['current_page'] = 'app'
        st.experimental_rerun()  # Trigger a rerun immediately after setting the page

def app():
    user = st.session_state['user']
    st.title("ECG-APP")
    st.write(f"Logged in as {user['username']} ({user['role']})")

    # Logout button
    if st.button("Logout"):
        st.session_state['user'] = None
        st.session_state['current_page'] = 'home'
        st.experimental_rerun()

    # Load basic data
    person_dict = Person.load_person_data()
    person_names = Person.get_person_list(person_dict)

    sf = 500

    # Streamlit settings


    # Sidebar
    st.sidebar.header("Navigation")
    current_user = st.sidebar.radio('Subject:', options=person_names, key="sbVersuchsperson")
    for entry in person_dict:
        if current_user == entry["lastname"] + ", " + entry["firstname"]:
            subject = Person(entry)
    st.sidebar.write("")
    checkbox_mark_peaks = st.sidebar.checkbox("Mark Peaks", value=False, key="cbMarkPeaks")

    tab1, tab2, tab3 = st.tabs([current_user, "ECG", "HR Analysis"])
    with tab1:
        st.write("#### General Information:", current_user)

        image = Image.open(subject.get_image_path())
        st.image(image, caption=current_user)
        st.write("The Year of Birth is: ", subject.date_of_birth)
        st.write("The age of the subject is: ", subject.calculate_person_age())
        user_ecg = subject.ekg_tests
        st.write("")
        st.write("### Number of ECGs: ", len(user_ecg))

        for i in range(len(user_ecg)):
            current_ekg = EKGdata(user_ecg[i])
            st.write("")
            st.write("Test date: ", current_ekg.date, ":")
            st.write("ECG " + str(i + 1) + ": ", current_ekg.data)
            st.write("Length of the test in seconds: ",
                     int(np.round(len(EKGdata.read_ecg_data(current_ekg.data)) / 500, 0)))

    with tab2:
        list_of_paths = []
        for element in user_ecg:
            list_of_paths.append(element['result_link'])
        selected_ecg_path = st.selectbox('ECG:', options=list_of_paths, key="sbECG")
        df_ecg_data = EKGdata.read_ecg_data(selected_ecg_path)
        peaks = EKGdata.find_peaks(selected_ecg_path)
        st.plotly_chart(ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf))

        for element in user_ecg:
            if selected_ecg_path == element['result_link']:
                ekg_date = element['date']

        st.write("This ecg was recorded on: ", ekg_date)

    with tab3:
        st.write("This is tab 3")
        hr, hr_max, hr_min, hr_mean = EKGdata.estimate_hr(peaks)

        st.write("The maximum heart rate is: ", hr_max)
        st.write("The minimum heart rate is: ", hr_min)
        st.write("The mean heart rate is: ", hr_mean)
        st.write("The estimated maximum heart rate is:", subject.max_hr)

# Page navigation
if st.session_state['current_page'] == 'home':
    home()
elif st.session_state['current_page'] == 'login':
    login_page()
elif st.session_state['current_page'] == 'register':
    register_page()
elif st.session_state['current_page'] == 'app':
    app()
