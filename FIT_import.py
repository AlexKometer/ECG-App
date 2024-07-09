import fitparse
import numpy as np
import datetime
import streamlit as st

"""
fitfile = fitparse.FitFile('data/other_tests/long_endurance_ride.fit')

time = np.array([])
velocity = np.array([])
heartrate = np.array([])
distance = np.array([])
cadence = np.array([])
power = np.array([])
altitude = np.array([])

dateref = datetime.datetime(1970, 1, 1)

for record in fitfile.get_messages('record'):
    for record_data in record:
        if record_data.name == 'timestamp':
            timediff = (record_data.value-dateref)
            time = np.append(time,timediff.total_seconds())
        elif record_data.name == 'timestamp':
            time = np.append(time,record_data.value)
        elif record_data.name == 'speed':
            velocity = np.append(velocity,record_data.value)
        elif record_data.name == 'heart_rate':
            heartrate = np.append(heartrate,record_data.value)
        elif record_data.name == 'distance':
            distance = np.append(distance,record_data.value)
        elif record_data.name == 'cadence':
            cadence = np.append(cadence,record_data.value)
        elif record_data.name == 'power':
            power = np.append(power,record_data.value)
        elif record_data.name == 'altitude':
            altitude = np.append(altitude,record_data.value)

time_s = np.array([], dtype = np.int64)
for i in range(len(time)+1):
    time_s = np.append(time_s, i)

time = time_s


#print(fitfile.messages)
up =  0
down = 0

for i in range(len(altitude)-1):

    if altitude[i] > altitude[i+1]:
        down = down + (altitude[i]-altitude[i+1])

    else:
        up = up + (altitude[i+1]-altitude[i])


print(up)
print(down)
print("--------------------------------------------------------------------------")
print(altitude.max())
print(altitude.min())
print("--------------------------------------------------------------------------")
print(power.max())
print(power.min())
print(power.mean())
print("--------------------------------------------------------------------------")
print(velocity.max())
print(velocity.min())
print(velocity.mean())
print("--------------------------------------------------------------------------")
print(cadence.max())
print(cadence.min())
print(cadence.mean())"""


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

    return time, velocity, heartrate, distance, cadence, power, altitude


def calculate_elevation_changes(altitude):
    up = 0.0
    down = 0.0
    for i in range(1, len(altitude)):
        elevation_change = altitude[i] - altitude[i - 1]
        if elevation_change > 0:
            up += elevation_change
        else:
            down += abs(elevation_change)
    return up, down


def main():
    file_path = "data/other_tests/long_endurance_test.fit"
    time, velocity, heartrate, distance, cadence, power, altitude = read_fit_file(file_path)

    up, down = calculate_elevation_changes(altitude)

    st.write("**Höhenmeter**")
    st.write(f"Aufwärts: {round(up, 1)} m")
    st.write(f"Abwärts: {round(down, 1)} m")

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


main()
