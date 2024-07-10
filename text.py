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



