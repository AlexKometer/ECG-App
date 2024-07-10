import pandas as pd
import scipy as sc
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from classes import Person
import pyhrv.time_domain as td

class ECGdata:
    def __init__(self, ecg_dict):
        self.id = ecg_dict["id"]
        self.date = ecg_dict["date"]
        self.data = ecg_dict["result_link"]
        self.types = ecg_dict.get("types", ["other"])

        if "EKG" in self.types:
            self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])
        else:
            self.df = None  # FIT files or other non-ECG files should not be read as text

    def get_ecg_path(person, id):
        data = person.ecg_tests
        for element in data:
            if element['id'] == id:
                return element['result_link']
            else:
                return ("User ", person.id, "hat kein EKG mit der ID ", id)

    @staticmethod
    def read_ecg_data(ecg_path):
        if ecg_path:
            df_ecg_data = pd.read_csv(ecg_path, sep="\t", header=None)
            df_ecg_data.columns = ["Messwerte in mV", "Zeit in ms"]
            df_ecg_data["Zeit in ms"] = df_ecg_data["Zeit in ms"] - df_ecg_data["Zeit in ms"].iloc[0]
            return df_ecg_data
        return pd.DataFrame(columns=["Messwerte in mV", "Zeit in ms"])

    @staticmethod
    def find_peaks(path):
        if path:
            df = ECGdata.read_ecg_data(path)
            peaks = sc.signal.find_peaks(df["Messwerte in mV"], height=350)
            return peaks
        return ([], {})

    @staticmethod
    def estimate_hr(peaks):
        if len(peaks[0]) > 0:
            peak_interval = np.diff(peaks[0])
            peak_interval_seconds = peak_interval / 1000
            hr = np.round(60 / peak_interval_seconds, 0)
            hr_max = int(np.round(hr.max()))
            hr_min = int(np.round(hr.min()))
            hr_mean = int(np.round(hr.mean()))
            return hr, hr_max, hr_min, hr_mean
        return None, None, None, None

    @staticmethod
    def calculate_hrv(peaks):
        if len(peaks[0]) > 0:
            peak_interval = np.diff(peaks[0])
            peak_interval_seconds = peak_interval / 1000
            df = pd.DataFrame(peak_interval_seconds)
            rr_intervals = df.values
            time_domain_results = td.time_domain(rr_intervals)
            SDNN = np.round(time_domain_results['sdnn'], 1)
            RMSSD = np.round(time_domain_results['rmssd'], 1)
            return SDNN, RMSSD
        return None, None
