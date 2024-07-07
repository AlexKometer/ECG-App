import json
from datetime import datetime
import os


class Person:
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("../ECGApp/data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " + eintrag["firstname"])
        return list_of_names

    @staticmethod
    def find_person_data_by_id(suchstring):
        person_data = Person.load_person_data()

        if suchstring == "None":
            return {}

        for eintrag in person_data:

            if (eintrag["id"] == suchstring):
                print()

                return eintrag
        else:
            return {}

    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.sex = person_dict["sex"]
        self.ekg_tests = person_dict["ekg_tests"]
        self.age = self.calculate_person_age()
        self.max_hr = self.estimated_max_hr(self.age, self.sex)

    def get_image_path(self):
        return self.picture_path

    def get_sex(self):
        return self.sex

    def calculate_person_age(self):
        age = datetime.now ().year - self.date_of_birth
        return age

    def estimated_max_hr(self, age, sex):
        if sex == "male":
            max_hr_calc = 223 - 0.9 * age
        elif sex == "female":
            max_hr_calc = 226 - 1.0 * age

        return max_hr_calc

