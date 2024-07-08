"""


- tests zu personen hinzufügen
- berechtigungen von personen ändern (sieht nur selbst angelegte subjects)
- admin kann alle subjects sehen
- admin kann alle subjects bearbeiten
- admin kann alle subjects löschen
- admin kann anderen usern berechtigungen für subjects ändern


i got this roadmap:
i want following features to implement to this Programm:
- have different users(custom users and 1 admin)
--login page for the users and the admin
--custom users can see the 3 basic subjects and the subjects they add
--admin can see all subjects
--noone can edit the 3 basic subjects
-- only the admin can edit and delete all added users
--custom users can only edit and delete their own subjects
-- it should be able to add tests to the subjects

- i want to make a HRV analysis for the ECG data
-i want to enable an other file input from other file formates like .fit files
"""


"""
json backup:


[
    {
        "id": 1,
        "date_of_birth": 1989,
        "firstname": "Julian",
        "lastname": "Huber",
        "picture_path": "data/pictures/tb.jpg",
        "sex": "male",
        "ekg_tests": [
            {
                "id": 1,
                "date": "10.2.2023",
                "result_link": "data/ekg_data/01_Ruhe.txt"
            },
            {
                "id": 2,
                "date": "11.3.2023",
                "result_link": "data/ekg_data/04_Belastung.txt"
            }
        ]
    },
    {
        "id": 2,
        "date_of_birth": 1967,
        "firstname": "Yannic",
        "lastname": "Heyer",
        "sex": "male",
        "picture_path": "data/pictures/js.jpg",
        "ekg_tests": [
            {
                "id": 3,
                "date": "10.2.2023",
                "result_link": "data/ekg_data/02_Ruhe.txt"
            }
        ]
    },
    {
        "id": 3,
        "date_of_birth": 1973,
        "firstname": "Yunus",
        "lastname": "Schmirander",
        "sex": "male",
        "picture_path": "data/pictures/bl.jpg",
        "ekg_tests": [
            {
                "id": 4,
                "date": "11.3.2023",
                "result_link": "data/ekg_data/03_Ruhe.txt"
            }
        ]
    },
    {
        "id": 4,
        "date_of_birth": 1997,
        "firstname": "Alexander",
        "lastname": "Kometer",
        "sex": "male",
        "picture_path": "data/pictures/Alexander_Kometer.jpg",
        "ekg_tests": []
    },
    {
        "id": 5,
        "date_of_birth": 2010,
        "firstname": "Georg",
        "lastname": "Sagenmeista",
        "sex": "male",
        "picture_path": "data/pictures/Georg_Sagenmeista.jpg",
        "ekg_tests": [],
        "owner": "Alex"
    }
]"""