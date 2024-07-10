import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Make ECG plot with the possibility to mark peaks
"""plots the ECG and marks the peaks"""
def ecg_plot(df_ecg_data, peaks, checkbox_mark_peaks, sf, selected_area_start, selected_area_end):

    if selected_area_start < selected_area_end:
        filtered_df_ecg = df_ecg_data.iloc[selected_area_start:selected_area_end].copy()
        filtered_df_ecg["Zeit in s"] = filtered_df_ecg["Zeit in ms"] / 1000  # Scale x-axis to seconds
        fig_ecg_marked = px.line(filtered_df_ecg, x="Zeit in s", y="Messwerte in mV" )
        fig_ecg_marked.update_traces(line_color='#1E90FF', )
        fig_ecg_marked.update_layout(
            title="ECG Data",
            xaxis_title="Time in s",
            yaxis_title="Voltage in mV",
            showlegend=False,
            xaxis=dict(title_font=dict(color='black')),
            yaxis=dict(title_font=dict(color='black'))
        )
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
                                                marker=dict(size=10, color='#ff7f0e'),
                                                name="Peak"))
    else:
        pass

    return fig_ecg_marked
