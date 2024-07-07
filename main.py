import numpy as np
import streamlit as st
from PIL import Image
from classes import Person
from ecgdata import EKGdata
# from file_input import load_person_data, get_person_list, get_image_path, get_ecg_path, read_ecg_data, calculate_person_age, get_year_of_birth, get_ekg_test_date, get_sex
from create_plot import ecg_plot
# from ecg_analytics import peak_detection, calculate_hr_data, estimated_max_hr
from user_management import new_user

# Load basic data
person_dict = Person.load_person_data()
person_names = Person.get_person_list(person_dict)

sf = 500

# Streamlit settings
st.set_page_config(layout="wide")
st.title("ECG-APP")

# Sidebar
st.sidebar.header("Navigation")
current_user = st.sidebar.radio('Subject:', options=person_names, key="sbVersuchsperson")
for entry in person_dict:
    if current_user == entry["lastname"] + ", " + entry["firstname"]:
        username = Person(entry)
button_new_user = st.sidebar.button("New User", key="btnNewUser")
button_edit_user = st.sidebar.button("Edit User", key="btnEditUser")
button_delete_user = st.sidebar.button("Delete User 🗑️", key="btnDeleteUser")
st.sidebar.write("")
checkbox_mark_peaks = st.sidebar.checkbox("Mark Peaks", value=False, key="cbMarkPeaks")

if button_new_user:
    st.session_state.step = 1
    st.session_state.basic_info = {}
    new_user()

elif st.session_state.get("step", 0) > 0:
    new_user()

elif button_edit_user:
    st.write("Edit user functionality is not implemented yet.")

elif button_delete_user:
    st.write("Delete user functionality is not implemented yet.")

else:
    tab1, tab2, tab3 = st.tabs([current_user, "ECG", "HR Analysis"])
    with tab1:
        st.write("#### General Information:", current_user)

        image = Image.open(username.get_image_path())
        st.image(image, caption=current_user)
        st.write("The Year of Birth is: ", username.date_of_birth)
        st.write("The age of the subject is: ", username.calculate_person_age())
        user_ecg = username.ekg_tests
        # test_date = get_ekg_test_date(person_dict, current_user)
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
        print(user_ecg)
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
        st.write("The estimated maximum heart rate is:", username.max_hr)


# TODO MUST DO
#  Geburtsjahr, Name und Bild der Personen wird angezeigt (2pkt) --> Done
#  Auswahlmöglichkeit für Tests, sofern mehr als ein Test bei einer Person vorliegt (4pkt) --> Done
#  Anzeigen des Testdatums und der gesamtem Länge der Zeitreihe in Sekunden (4pkt) --> Done
#  EKG-Daten werden beim Einlesen sinnvoll resampelt, um Ladezeiten zu verkürzen (2pkt) --> Done
#  Sinnvolle Berechnung der Herzrate über den gesamten Zeitraum wird angezeigt (2pkt) --> Done
#  Nutzer:in kann sinnvollen Zeitbereich für Plots auswählen (2pkt) --> Done
#  Stil z.B. Namenskonventionen, sinnvolle Aufteilung in Module, Objektorientierung (4pkt)
#  Kommentare und Docstrings (2pkt)
#  Design für Computer Bildschirm optimiert und optisch ansprechend (2pkt)
#  Deployment auf Heroku oder Streamlit Sharing (2pkt)


# TODO: optional
#  Daten aus einer anderen Datenquelle einlesen (z.B. .fit oder kml) (4pkt)
#  Neue Daten mit einem Nutzer verknüpfen (4pkt)
#  Nutzer und Test-Daten editierbar machen (4pkt)
#  Daten in einer SQLite oder tinyDB speichern (6pkt)
#  Gefundene Peaks im Plot anzeigen (2pkt) --> Done
#  Herzrate im sinnvollen gleitenden Durchschnitt als Plot anzeigen (2pkt)
#  Ausrechnen des Maximalpuls basierend auf Alter. Anzeige im Dashboard (1pkt) --> Done
#  Herzratenvariabilität anzeigen (2pkt)
#  Weitere eigene: Vorzustellen in Pitch-Sessiona

# TODO Ideas:
#  zugriff beim bearbeiten begrenzen, Stammdaten können nicht angefasst werden, ebenfalls löschen
#  es soll möglich sein das eine neue person kein ekg hat (jump seite 3)
#  adding ecg, User Login
#
