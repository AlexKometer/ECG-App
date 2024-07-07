import pandas as pd
import scipy as sc
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from classes import Person


class EKGdata:

    ## Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        # pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms', ])

    def get_ecg_path(person, id):
        data = person.ekg_tests
        for element in data:
            if element['id'] == id:
                return element['result_link']
            else:
                return ("User ", person.id, "hat kein EKG mit der ID ", id)

    def read_ecg_data(ecg_path):
        df_ecg_data = pd.read_csv(ecg_path, sep="\t", header=None)
        df_ecg_data.columns = ["Messwerte in mV", "Zeit in ms"]
        df_ecg_data["Zeit in ms"] = df_ecg_data["Zeit in ms"] - df_ecg_data["Zeit in ms"].iloc[0]

        return df_ecg_data

    def find_peaks(path):
        df = EKGdata.read_ecg_data(path)
        peaks = sc.signal.find_peaks(df["Messwerte in mV"], height=350)
        return peaks

    def estimate_hr(peaks):
        peak_interval = np.diff(peaks[0])
        peak_interval_seconds = peak_interval / 1000
        hr = np.round(60 / peak_interval_seconds, 0)
        hr_max = int(np.round(hr.max()))
        hr_min = int(np.round(hr.min()))
        hr_mean = int(np.round(hr.mean()))
        return hr, hr_max, hr_min, hr_mean

    def plot_time_series(path, peaks):
        df = EKGdata.read_ecg_data(path)

        max_seconds = len(df) // 500
        selected_area_start = 500 * st.sidebar.number_input("Start of the selected area (in s) :", min_value=0,
                                                            max_value=max_seconds, value=0)
        selected_area_end = (500 * st.sidebar.number_input("End of the selected area (in s) :", min_value=0,
                                                           max_value=max_seconds, value=max_seconds))

        if selected_area_start < selected_area_end:
            filtered_df_ecg = df.iloc[selected_area_start:selected_area_end]
            filtered_df_ecg["Zeit in s"] = filtered_df_ecg["Zeit in ms"] / 1000  # Scale x-axis to seconds
            fig_ecg_marked = px.line(filtered_df_ecg, x="Zeit in s", y="Messwerte in mV")
            fig_ecg_marked.update_layout(title="ECG Data", xaxis_title="Time in s", yaxis_title="Voltage in mV")
        else:
            st.error("Start value must be less than end value.")
            fig_ecg_marked = px.line()

        peak_indices = peaks[0]
        # Filter peaks within the selected range
        filtered_peaks = [peak for peak in peak_indices if selected_area_start <= peak < selected_area_end]
        if filtered_peaks:
            peak_times = df.iloc[filtered_peaks]["Zeit in ms"].to_numpy() / 1000
            peak_values = df.iloc[filtered_peaks]["Messwerte in mV"].to_numpy()

            fig_ecg_marked.add_trace(go.Scatter(x=peak_times,
                                                y=peak_values,
                                                mode="markers",
                                                marker=dict(size=10, color="red"),
                                                name="Peak"))

        st.plotly_chart(fig_ecg_marked)
