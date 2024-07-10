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



import fitparse
import numpy as np
import datetime
import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def read_fit_file(file_path):
    fitfile = fitparse.FitFile(file_path)

    time = np.array([])
    velocity = np.array([])
    heartrate = np.array([])
    distance = np.array([])
    cadence = np.array([])
    power = np.array([])
    altitude = np.array([])

    Zeitref = datetime.datetime(1970, 1, 1)
    for record in fitfile.get_messages('record'):
        for record_data in record:
            if record_data.name == 'timestamp':
                timediff = (record_data.value - Zeitref)
                time = np.append(time, timediff.total_seconds())
            elif record_data.name == 'speed':
                velocity = np.append(velocity, record_data.value)
            elif record_data.name == 'heart_rate':
                heartrate = np.append(heartrate, record_data.value)
            elif record_data.name == 'distance':
                distance = np.append(distance, record_data.value)
            elif record_data.name == 'cadence':
                cadence = np.append(cadence, record_data.value)
            elif record_data.name == 'power':
                power = np.append(power, record_data.value)
            elif record_data.name == 'altitude':
                altitude = np.append(altitude, record_data.value)

    df = pd.DataFrame({
        'Time in s': time,
        'Velocity': velocity,
        'HeartRate': heartrate,
        'Distance': distance,
        'Cadence': cadence,
        'PowerOriginal': power,
        'Altitude': altitude
    })


def calculate_elevation_changes(df):
    altitude = df['altitude']
    up = 0.0
    down = 0.0
    for i in range(1, len(altitude)):
        elevation_change = altitude[i] - altitude[i - 1]
        if elevation_change > 0:
            up += elevation_change
        else:
            down += abs(elevation_change)
    return up, down


def power_curve(power):
    sorted_power_W = np.sort(power)
    print(sorted_power_W)

    plt.plot(sorted_power_W)
    plt.title('Power Curve')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')
    plt.savefig('power_curve.png')
    plt.show()


def find_best_effort(df):
    t_w = [1, 2, 5, 10, 20, 30, 60, 120, 300, 600, 1200, 1800]  # Daten nicht länge vorhanden
    power_curve = []
    df_clean = df.dropna(subset=['PowerOriginal'])

    for interval in t_w:
        rolling_mean = df_clean['PowerOriginal'].rolling(window=interval).mean()
        max_average_power = rolling_mean.max()
        power_curve.append(max_average_power)

    # power_curve_df = pd.DataFrame (list (power_curve.items()), columns=['Interval (s)', 'Max Average Power'])

    return t_w, power_curve


def make_plot_power(power, heartrate):
    # Create a plot with two y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=time, y=df2, name="PowerOriginal", line=dict(color="black")),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=time, y=df2, name="HeartRate", line=dict(color="royalblue")),
        secondary_y=True,
    )
    fig.update_xaxes(title_text="Time in s")

    fig.update_yaxes(title_text="Power (watts)", title_font=dict(color="black"), tickfont=dict(color="black"),
                     secondary_y=False)
    fig.update_yaxes(title_text="Heart Rate (bpm)", title_font=dict(color="royalblue"),
                     tickfont=dict(color="royalblue"), secondary_y=True)

    max_value = max(power.max(), heartrate.max())

    fig.update_yaxes(range=[0, max_value], secondary_y=False)
    fig.update_yaxes(range=[0, max_value], secondary_y=True)

    # Define the heart rate zones
    zone1 = hr_max * 0.6
    zone2 = hr_max * 0.7
    zone3 = hr_max * 0.8
    zone4 = hr_max * 0.9


    """power_zone1 = power < 0.6 * heartrate.max()
    power_zone2 = (power >= 0.6 * heartrate.max().max()) & (power < 0.7 * heartrate.max().max())
    power_zone3 = (power >= 0.7 * heartrate.max().max()) & (power < 0.8 * heartrate.max().max())
    power_zone4 = (power >= 0.8 * heartrate.max().max()) & (power < 0.9 * heartrate.max().max())
    power_zone5 = (power >= 0.9 * heartrate.max().max()) & (power < heartrate.max().max())"""

    # Create a column for each heart rate zone

    power_zone1 = heartrate < zone1
    power_zone2 = (heartrate >= zone1) & (heartrate < zone2)
    power_zone3 = (heartrate >= zone2) & (heartrate < zone3)
    power_zone4 = (heartrate >= zone3) & (heartrate < zone4)
    power_zone5 = (heartrate >= zone4) & (heartrate < hr_max)

    # Calculate the time in each zone
    zone_counts = {
        "Zone1": power_zone1.sum(),
        "Zone2": power_zone2.sum(),
        "Zone3": power_zone3.sum(),
        "Zone4": power_zone4.sum(),
        "Zone5": power_zone5.sum(),
    }
    # Add the heart rate zones to the plot
    fig.add_hrect(y0=0, y1=zone1, fillcolor="lightgreen", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone1, y1=zone2, fillcolor="green", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone2, y1=zone3, fillcolor="yellow", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone3, y1=zone4, fillcolor="orange", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone4, y1=hr_max, fillcolor="red", opacity=0.5, layer="below", line_width=0)

    return fig, zone_counts















def main():
    file_path = "data/other_tests/long_endurance_ride.fit"
    time, velocity, heartrate, distance, cadence, power, altitude = read_fit_file(file_path)

    up, down = calculate_elevation_changes(altitude)

    st.write("**Höhenmeter**")
    st.write(f"Aufwärts: {round(up, 1)} m")
    st.write(f"Abwärts: {round(down, 1)} m")

    power_curve(power)

    st.write("**Statistiken**")
    data = [
        {"Metric": "Altitude Max", "Value": round(altitude.max(), 1), "Unit": "m"},
        {"Metric": "Altitude Min", "Value": round(altitude.min(), 1), "Unit": "m"},
        {"Metric": "Power Max", "Value": round(power.max(), 1), "Unit": "W"},
        {"Metric": "Power Min", "Value": round(power.min(), 1), "Unit": "W"},
        {"Metric": "Power Mean", "Value": round(power.mean(), 1), "Unit": "W"},
        {"Metric": "Velocity Max", "Value": round(velocity.max(), 1), "Unit": "m/s"},
        {"Metric": "Velocity Min", "Value": round(velocity.min(), 1), "Unit": "m/s"},
        {"Metric": "Velocity Mean", "Value": round(velocity.mean(), 1), "Unit": "m/s"},
        {"Metric": "Cadence Max", "Value": round(cadence.max(), 1), "Unit": "rpm"},
        {"Metric": "Cadence Min", "Value": round(cadence.min(), 1), "Unit": "rpm"},
        {"Metric": "Cadence Mean", "Value": round(cadence.mean(), 1), "Unit": "rpm"},
    ]
    st.table(data)


file_path = "data/other_tests/long_endurance_ride.fit"
time, velocity, heartrate, distance, cadence, power, altitude = read_fit_file(file_path)

# import all required libraries and modules from read_pandas.py

from plotly.subplots import make_subplots

# Read the Power data
# df2 = pd.read_csv ("data/activities/activity.csv")
df2 = power

tab1, tab2 = st.tabs(["Power-Data", "Power curve"])

with tab1:
    st.subheader("Interaktiver Plot")
    st.header("Power- & Heart-Data")
    hr_max = st.number_input('Please enter the maximum heartrate (0 = no Input -> max_hr generated from data):',
                             min_value=0, max_value=300, value=0, step=1)  # Input for the maximum heartrate
    if hr_max == 0:
        hr_max = df2.max()  # Set the maximum heartrate to the maximum heartrate from the data
    elif hr_max < df2.max():  # Warn the user if the input is lower than the maximum heartrate from the data
        st.markdown("The maximum heartrate from data is:", df2["HeartRate"].max())
        st.markdown("Are you sure you want to use a lower value?")

    fig, zone_counts = make_plot_power(df2, heartrate)

    # Calculate Power statistics
    st.write("Maximum power:", power.max(), "watts")
    st.write("Average power:", power.mean(), "watts")

    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        # Calculate time in each zone
        st.write("Time in Zone 1:", zone_counts["Zone1"], "s")
        st.write("Time in Zone 2:", zone_counts["Zone2"], "s")
        st.write("Time in Zone 3:", zone_counts["Zone3"], "s")
        st.write("Time in Zone 4:", zone_counts["Zone4"], "s")
        st.write("Time in Zone 5:", zone_counts["Zone5"], "s")

    with col2:
        # Calculate average power in each zone
        zones = ['Zone1', 'Zone2', 'Zone3', 'Zone4', 'Zone5']
        for zone in zones:
            if zone in df2.columns and df2[zone].any():
                average_power = round(df2[df2[zone]]['PowerOriginal'].mean())
                st.write(f"Average power in {zone}:", average_power, "watts")

with tab2:
    st.subheader("Power curve")
    timeline, power_curve = find_best_effort(df2)
    fig = px.line(x=timeline, y=power_curve, title="Power curve", log_x=True)
    fig.update_yaxes(title_text="Power in [W]")
    fig.add_traces(go.Scatter(
        x=timeline,
        y=power_curve,
        fill='tozeroy',
        fillcolor='rgba(211, 211, 211, 0.3)',
        mode='none',

    ))
    fig.update_layout(
        xaxis=dict(
            title='Duration in [mm:ss]',
            tickmode='array',
            tickvals=timeline,
            ticktext=['0:01', '0:02', '0:05', '0:10', '0:20', '0:30', '1:00', '2:00', '5:00', '10:00', '20:00', '30:00']
        )
    )
    st.plotly_chart(fig)

    st.write(power_curve)
