# ECG-App

This repository is the final assignment of the Programming exercise II 
Authors of this repository are: Alexander Kometer and Georg Sagmeister



**The basic exercises for this assignment where:**
- Display the name, year of birth of the subject
- Opportunity to choose between the tests if a person has more than 1 test
- Display the testdate and the lenght of the test
- ECG data should be resampled to shorten loading times
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

## Features

### User Management

- **Login/Register**: Users can register for an account or log in using their credentials. User roles are distinguished as 'admin' or 'custom'.
- **Admin Features**: Admins can manage user permissions, delete users, and edit user information and tests.

### Subject Management

- **Add New Subject**: Users can add new subjects to the database by providing the subject's details and uploading a profile picture.
- **View Subject Information**: Users can view detailed information about each subject, including their name, date of birth, age, sex, and a list of their tests.

### Test Management

- **Upload New Test**: Users can upload new tests for a subject. The supported test types are ECG and FIT tests.
- **Test Data Visualization**: The app provides detailed visualizations and analyses for the uploaded test data.

### ECG Test Features

- **ECG Test Data**: View detailed ECG test data, including the length of the test and the test date.
- **ECG Plots**: Visualize ECG data with the option to mark peaks. Users can select specific areas of the ECG data to zoom in for detailed analysis.
- **Heart Rate Analysis**: The app provides heart rate analysis, including maximum, minimum, and mean heart rates. Additionally, it calculates heart rate variability (HRV) metrics such as SDNN and RMSSD.

### FIT Test Features

- **FIT Test Data**: View detailed FIT test data, including various metrics like heart rate, altitude, power, velocity, and cadence.
- **Power Curve Analysis**: The app visualizes the power curve and provides insights into different heart rate zones during the test.
- **Elevation Changes**: The app calculates and displays the total elevation gain and loss during the test.

