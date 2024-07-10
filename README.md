# ECG-App

This repository is the final assignment of the Programming exercise II 
Authors of this repository are: Alexander Kometer and Georg Sagmeister



**The basic exercises for this assignment where:**
- display the name, year of birth of the subject
- Opertunity to choose between the tests if a person has more than 1 test
- Display the testdate and the lenght of the test
- ECG data should be resamplet to shorten loading times
- Users can choose a time span of the tests
- Commentary and Docstrings
- Design optimized for computer monitors and optical appealing
- Deployment on Heroku or Streamlit Sharing

  
**Further more in our project we tried to do following free objectives:**
- implement a User-Login
- deploy different levels of permissions(Admin/User model)
- import data from other filetypes(.fit-files in our case)
- connect new tests with a subject
- make subject data and tests editable
- display heartrates reasonable
- calculate the HRV

 ## Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/AlexKometer/ECG-App
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```
> [!IMPORTANT]
> To log in u can use following options:

**Admin**
> Username: Admin

> Password: PycharisLOVE!


**Jasper**
> Username: Jasper

> Password: JasperV!


**Julian**
> Username: Julian

> Password: JulianH!

