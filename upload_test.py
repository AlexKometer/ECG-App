import streamlit as st
import os
import json
from classes import Person
from datetime import datetime

#saving a new uploaded file
def save_uploaded_file(uploaded_file, directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Fehler beim Speichern der Datei: {e}")
        return False

#adding the test to a subject
def add_test(subject_id, uploaded_file, test_date, test_types):
    person_dict = Person.load_person_data()
    max_id = 0

    for entry in person_dict:
        for test in entry.get("ekg_tests", []):
            if test["id"] > max_id:
                max_id = test["id"]

    new_test_id = max_id + 1
    test_added = False

    for entry in person_dict:
        if entry["id"] == subject_id:
            if not "ekg_tests" in entry:
                entry["ekg_tests"] = []
            entry["ekg_tests"].append(
                {
                    "id": new_test_id,
                    "date": test_date,
                    "result_link": f"data/other_tests/{uploaded_file.name}",
                    "types": test_types  # Use test_types here
                }
            )
            test_added = True
            break

    if test_added:
        with open("data/person_db.json", 'w') as f:
            json.dump(person_dict, f, indent=4)
        st.success("The test was successfully added.")
    else:
        st.error("Error: Subject ID not found.")

#checks if the date-format is valid
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


