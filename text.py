"""
- bei test upload auswahl was es ist EKG/HRV, art des testes/fahrrad...
- je nachdem was für tests zur verfügung stehen tabs ändern
ist ein ekg ausgewählt so soll ecg und ekg daten verfügbar sein
ist es ein fit file leistungsdiagramm, powercurve, ...



Roadmap:

- upload_tests:
    - add a field for the type of test (same style as the permissions in the user.json)
        - EKG
        - fit
        - VO2max test
        - other
    - depending on the type of test, different tabs should be available
        - EKG:
            - Test data should be available in tab 2
            - mark peaks chekcbox in tab 2
            - ECG data in tab 3
            - HRV analysis in tab 4
            - add HRV visualisation
        - fit:
            - Test data should be available in tab 2
            - Powercurve in tab 3
        - VO2max test:
            - Test data in tab 2
            - VO2max analysis in tab 3
        - other:
            - Test data in tab 2
            - no further analysis

- design ideas:
    - sidebar:
        from top to bottom:
            - logout button
            - Subject selection (dropdown)
            - upload test button
    - tab 1:
        - col 1 (left): user picture
        - col 2 (middle): user data
        - col 3 (right): test data



Graphische darstelluing
VO2max wie in progÜ1
power curve wie in progÜ2

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