import json
from datetime import datetime
import os

class Person:
    DEFAULT_SUBJECT_IDS = {1, 2, 3}  # IDs of the subjects that are accessible to all users

    @staticmethod
    def load_person_data():
        """A Function that knows where the person Database is and returns a Dictionary with the Persons"""
        try:
            with open('data/person_db.json') as file:
                person_data = json.load(file)
            return person_data
        except json.JSONDecodeError:
            return []  # Return an empty list if JSON is invalid or empty

    @staticmethod
    def get_person_list(person_data, current_user):
        """A Function that takes the persons-dictionary and returns a list of all person names the current user is allowed to see"""
        list_of_names = []
        for entry in person_data:
            if current_user['role'] == 'admin' or entry.get("owner") == current_user['username'] or entry["id"] in Person.DEFAULT_SUBJECT_IDS:
                list_of_names.append(entry["lastname"] + ", " + entry["firstname"])
        return list_of_names

    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.sex = person_dict["sex"]
        self.ecg_tests = person_dict["ekg_tests"]
        self.owner = person_dict.get("owner", "")
        self.age = self.calculate_person_age()
        self.max_hr = self.estimated_max_hr(self.age, self.sex)

    def get_image_path(self):
        return self.picture_path

    def get_sex(self):
        return self.sex

    def calculate_person_age(self):
        current_year = datetime.now().year
        age = current_year - self.date_of_birth
        return age

    def estimated_max_hr(self, age, sex):
        if sex == "male":
            max_hr_calc = 223 - 0.9 * age
        elif sex == "female":
            max_hr_calc = 226 - 1.0 * age
        return max_hr_calc

    def to_dict(self):
        return {
            "id": self.id,
            "date_of_birth": self.date_of_birth,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "picture_path": self.picture_path,
            "sex": self.sex,
            "ekg_tests": self.ecg_tests,
            "owner": self.owner
        }