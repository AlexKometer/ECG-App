import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import fitparse
import numpy as np
import datetime
import streamlit as st
import classes
import matplotlib.pyplot as plt



#reads a .csv-File
def read_my_csv(path):
    df = pd.read_csv(path, sep="\t", header=None)
    df.columns = ["Messwerte in mV", "Zeit in ms"]
    return df

#reads a .FIT-File
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

    time_s = np.array([], dtype=np.int64)
    for i in range(len(time)):
        time_s = np.append(time_s, i)

    time = time_s


    df = pd.DataFrame({
        'Time in s': time,
        'Velocity': velocity,
        'HeartRate': heartrate,
        'Distance': distance,
        'Cadence': cadence,
        'PowerOriginal': power,
        'Altitude': altitude
    })

    return df, time, velocity, heartrate, distance, cadence, power, altitude


#creats the Power-Plot
def make_plot_power(df_power, hr_max):
    # Create a plot with two y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df_power["Time in s"], y=df_power["PowerOriginal"], name="PowerOriginal", line=dict(color="black", width=0.7)),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df_power["Time in s"], y=df_power["HeartRate"], name="HeartRate", line=dict(color="royalblue", width=0.7)),
        secondary_y=True,
    )
    fig.update_xaxes(title_text="Time in s")

    fig.update_yaxes(title_text="Power (watts)", title_font=dict(color="black"), tickfont=dict(color="black"),
                     secondary_y=False)
    fig.update_yaxes(title_text="Heart Rate (bpm)", title_font=dict(color="royalblue"),
                     tickfont=dict(color="royalblue"), secondary_y=True)

    max_value = max(df_power["PowerOriginal"].max(), df_power["HeartRate"].max())

    fig.update_yaxes(range=[0, max_value], secondary_y=False)
    fig.update_yaxes(range=[0, max_value], secondary_y=True)

    # Define the heart rate zones
    zone1 = hr_max * 0.6
    zone2 = hr_max * 0.7
    zone3 = hr_max * 0.8
    zone4 = hr_max * 0.9

    # Create a column for each heart rate zone
    df_power["Zone1"] = df_power["HeartRate"] < zone1
    df_power["Zone2"] = (df_power["HeartRate"] >= zone1) & (df_power["HeartRate"] < zone2)
    df_power["Zone3"] = (df_power["HeartRate"] >= zone2) & (df_power["HeartRate"] < zone3)
    df_power["Zone4"] = (df_power["HeartRate"] >= zone3) & (df_power["HeartRate"] < zone4)
    df_power["Zone5"] = df_power["HeartRate"] >= zone4

    # Calculate the time in each zone
    zone_counts = {
        "Zone1": df_power["Zone1"].sum(),
        "Zone2": df_power["Zone2"].sum(),
        "Zone3": df_power["Zone3"].sum(),
        "Zone4": df_power["Zone4"].sum(),
        "Zone5": df_power["Zone5"].sum(),
    }
    # Add the heart rate zones to the plot
    fig.add_hrect(y0=0, y1=zone1, fillcolor="lightgreen", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone1, y1=zone2, fillcolor="green", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone2, y1=zone3, fillcolor="yellow", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone3, y1=zone4, fillcolor="orange", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=zone4, y1=hr_max, fillcolor="red", opacity=0.5, layer="below", line_width=0)

    return fig, zone_counts

#calculates the total elevation of the test
def calculate_elevation_changes(df):
    altitude = df['Altitude']
    up = 0.0
    down = 0.0
    for i in range(1, len(altitude)):
        elevation_change = altitude[i] - altitude[i - 1]
        if elevation_change > 0:
            up += elevation_change
        else:
            down += abs(elevation_change)
    return up, down


#creat a table with a statistic of the test and plots the power and the heartrate
def main(subject, path):

    file_path = path
    df, time, velocity, heartrate, distance, cadence, power, altitude = read_fit_file(file_path)

    up, down = calculate_elevation_changes(df)

    st.write("**Altitude**")
    st.write(f"Upwards: {np.round(up, 1)} m")
    st.write(f"Downwards: {np.round(down, 1)} m")

    st.write("**Statistics**")
    data = [
        {"Metric": "Heartrate Max - calculation ", "Value": np.round(subject.max_hr, 1), "Unit": "bpm"},
        {"Metric": "Heartrate Max", "Value": np.round(heartrate.max(), 1), "Unit": "bpm"},
        {"Metric": "Heartrate Min", "Value": np.round(heartrate.min(), 1), "Unit": "bpm"},
        {"Metric": "Heartrate Mean", "Value": np.round(heartrate.mean(), 1), "Unit": "bpm"},
        {"Metric": "Altitude Max", "Value": np.round(altitude.max(), 1), "Unit": "m"},
        {"Metric": "Altitude Min", "Value": np.round(altitude.min(), 1), "Unit": "m"},
        {"Metric": "Power Max", "Value": np.round(power.max(), 1), "Unit": "W"},
        {"Metric": "Power Min", "Value": np.round(power.min(), 1), "Unit": "W"},
        {"Metric": "Power Mean", "Value": np.round(power.mean(), 1), "Unit": "W"},
        {"Metric": "Velocity Max", "Value": np.round(velocity.max(), 1), "Unit": "m/s"},
        {"Metric": "Velocity Min", "Value": np.round(velocity.min(), 1), "Unit": "m/s"},
        {"Metric": "Velocity Mean", "Value": np.round(velocity.mean(), 1), "Unit": "m/s"},
        {"Metric": "Cadence Max", "Value": np.round(cadence.max(), 1), "Unit": "rpm"},
        {"Metric": "Cadence Min", "Value": np.round(cadence.min(), 1), "Unit": "rpm"},
        {"Metric": "Cadence Mean", "Value": np.round(cadence.mean(), 1), "Unit": "rpm"},
    ]
    df_data = pd.DataFrame(data)
    df_data['Value'] = df_data['Value'].apply(lambda x: f'{x:.1f}')

    st.table(df_data)

    """fig, zone_counts = make_plot_power(df, hr_max)
    st.plotly_chart(fig)"""




