import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Make ECG plot with the possibility to mark peaks
def ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf, key_suffix=""):
    max_seconds = len(df_ecg_data) // sf
    selected_area_start = 500 * st.number_input(f"Start of the selected area (in s) :{key_suffix}", min_value=0,
                                                max_value=max_seconds, value=0, key=f"start_area_{key_suffix}")
    selected_area_end = (500 * st.number_input(f"End of the selected area (in s) :{key_suffix}", min_value=0,
                                               max_value=max_seconds, value=10, key=f"end_area_{key_suffix}"))

    if selected_area_start < selected_area_end:
        filtered_df_ecg = df_ecg_data.iloc[selected_area_start:selected_area_end].copy()
        filtered_df_ecg["Zeit in s"] = filtered_df_ecg["Zeit in ms"] / 1000  # Scale x-axis to seconds
        fig_ecg_marked = px.line(filtered_df_ecg, x="Zeit in s", y="Messwerte in mV")
        fig_ecg_marked.update_layout(title="ECG Data", xaxis_title="Time in s", yaxis_title="Voltage in mV")
    else:
        st.error("Start value must be less than end value.")
        fig_ecg_marked = px.line()

    if checkbox_mark_peaks:
        # Extract the indices of the peaks
        peak_indices = peaks[0]
        # Filter peaks within the selected range
        filtered_peaks = [peak for peak in peak_indices if selected_area_start <= peak < selected_area_end]
        if filtered_peaks:
            peak_times = df_ecg_data.loc[filtered_peaks, "Zeit in ms"].to_numpy() / 1000
            peak_values = df_ecg_data.loc[filtered_peaks, "Messwerte in mV"].to_numpy()

            fig_ecg_marked.add_trace(go.Scatter(x=peak_times,
                                                y=peak_values,
                                                mode="markers",
                                                marker=dict(size=10, color="red"),
                                                name="Peak"))
    else:
        pass

    return fig_ecg_marked
