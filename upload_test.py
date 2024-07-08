import streamlit as st
import os
import numpy as np
import streamlit as st
from PIL import Image
from classes import Person
from ecgdata import ECGdata
from create_plot import ecg_plot
from login import login, register
import os
import json


# Funktion zum Speichern hochgeladener Dateien
def save_uploaded_file(uploaded_file, directory):
    try:
        # Erstellen des Verzeichnisses, falls es nicht existiert
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Speichern der Datei im angegebenen Verzeichnis
        with open(os.path.join(directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")
        return False


# Streamlit App
st.title("Datei-Upload und Speichern")

uploaded_file = st.file_uploader("Wählen Sie eine Datei zum Hochladen aus", type=None)

if uploaded_file is not None:
    save_directory = 'data/other_tests'

    if save_uploaded_file(uploaded_file, save_directory):
        st.success(f"Die Datei wurde erfolgreich im Verzeichnis '{save_directory}' gespeichert.")
    else:
        st.error("Es gab einen Fehler beim Speichern der Datei.")

def give_new_id(subject_id):
        person_dict = Person.load_person_data()
        max_id = 0
        test_date = st.text_input("Datum des EKG-Tests (Format: TT-MM-JJJJ")
        for entry in person_dict:
            for test in entry.get("ekg_tests", []):
                if test["id"] > max_id:
                    max_id = test["id"]
                    print(max_id)
            if entry["id"] == subject_id:
                print(entry)
                with open("data/person_db.json", 'r+') as f:
                    print(entry["ekg_tests"])
                    entry["ekg_tests"].append(
                        {
                            "id": max_id,
                            "date": test_date,
                            "result_link": "data/other_tests/"
                        })
                    json.dump(entry,f,indent=4)

give_new_id(5)

