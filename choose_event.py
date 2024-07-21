import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, Draw, MeasureControl
import folium
import requests
import pydeck as pdk


# Sidebar with toggle buttons
with st.sidebar:
    selected = option_menu("Choose", ["Ground Station History Data", "Forcasting"],
                           icons=["list-task", "list-task"],
                           menu_icon="cast", default_index=0)

# Main content based on toggle button selection
if selected == "Ground Station History Data":


    st.write("You selected Ground Station History Data")
    # Add your Task 1 related code here
    df1 = pd.read_csv('Ground_data_after_processing.csv', parse_dates=['Datetime'])
    dataset1 = {
        'Ground Station Data': df1 }
    st.title('Ground Station Data Visualization Dashboard')

    # Sidebar for date and time range selection
    st.sidebar.header('Select Date and Time Range')

    def datetime_range_input(label_start, label_end, min_date, max_date):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(label_start, min_date, key='start_date_input')
            start_time = st.time_input("Start time", pd.Timestamp(min_date).time(), key='start_time_input')
        with col2:
            end_date = st.date_input(label_end, max_date, key='end_date_input')
            end_time = st.time_input("End time", pd.Timestamp(max_date).time(), key='end_time_input')
        start_datetime = pd.to_datetime(f"{start_date} {start_time}")
        end_datetime = pd.to_datetime(f"{end_date} {end_time}")
        return start_datetime, end_datetime


    start_datetime, end_datetime = datetime_range_input(
        'Start date', 'End date',
        df1['Datetime'].min().date(), df1['Datetime'].max().date()
    )

    # Filter Data based on Date and Time Range
    mask = (df1['Datetime'] >= start_datetime) & (df1['Datetime'] <= end_datetime)
    filtered_data = df1.loc[mask]
    
    # Sidebar for plot customization
    st.sidebar.header('Plot Customization')
    # Display Data
    st.write(f'Data from {start_datetime} to {end_datetime}')
    st.dataframe(filtered_data)

    show_plots = st.sidebar.checkbox('Show Plot Customization', value=True, key='show_plots_checkbox')


    if show_plots:
        plot_style = st.sidebar.selectbox('Select Plot Style', plt.style.available, key='plot_style_selectbox')
        x_column = st.sidebar.selectbox('Select X-axis Column', filtered_data.columns, key='x_column_selectbox')
        y_column = st.sidebar.selectbox('Select Y-axis Column', filtered_data.columns, key='y_column_selectbox')

        plot_type = st.sidebar.selectbox('Select Plot Type', [
            'Line Plot', 'Histogram', 'Scatter Plot', 'Box Plot', 'Area Plot', 'Pie Chart'
        ], key='plot_type_selectbox')
        st.title('Ground Station Plotting')


        # Additional customization options
        title = st.sidebar.text_input('Plot Title', f'{plot_type} of {y_column} vs {x_column}')
        xlabel = st.sidebar.text_input('X-axis Label', x_column)
        ylabel = st.sidebar.text_input('Y-axis Label', y_column)
        color = st.sidebar.color_picker('Select Plot Color', '#1f77b4')
        show_grid = st.sidebar.checkbox('Show Grid', True)
        show_legend = st.sidebar.checkbox('Show Legend', True)


        # Apply Plot Style
        plt.style.use(plot_style)

        # Plot Data
        fig, ax = plt.subplots(figsize=(8, 8))
        if plot_type == 'Line Plot':
            ax.plot(filtered_data[x_column], filtered_data[y_column], color=color)
        elif plot_type == 'Histogram':
            ax.hist(filtered_data[y_column], bins=50, color=color)
        elif plot_type == 'Scatter Plot':
            ax.scatter(filtered_data[x_column], filtered_data[y_column], color=color)
        elif plot_type == 'Box Plot':
            ax.boxplot(filtered_data[y_column], patch_artist=True, boxprops=dict(facecolor=color))
        elif plot_type == 'Area Plot':
            ax.fill_between(filtered_data[x_column], filtered_data[y_column], color=color, alpha=0.5)
        else:
            st.stop()


        # Customize plot appearance
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if show_grid:
            ax.grid(True)
        if show_legend:
            ax.legend([plot_type])

        st.pyplot(fig)

        # Sidebar for plot export
        st.sidebar.header('Export Plot')
        export_format = st.sidebar.selectbox('Select Export Format', ['png', 'pdf', 'svg'],
                                             key='export_format_selectbox')
        buffer = BytesIO()
        fig.savefig(buffer, format=export_format)
        buffer.seek(0)

        if st.sidebar.download_button(label=f"Download plot as {export_format}", data=buffer,
                                      file_name=f"plot.{export_format}", key='download_plot_button'):
            st.success(f"Plot downloaded as {export_format}.")

    st.title("Interactive Map")

    # Initialize the map
    latitude, longitude = 29.035, 31.12
    m = folium.Map(location=[latitude, longitude], zoom_start=10,
                   width='600',
                   height='500',
                   control_scale=True
                   )

    # Add a marker with a popup and a tooltip
    folium.Marker(
        [latitude, longitude],
        popup="Ground Station: North Egypt",
        tooltip="Click for more info",
        icon=folium.Icon(icon="info-sign")
    ).add_to(m)

    # Add draw tool
    draw = Draw()
    draw.add_to(m)

    # Add measure tool
    measure = MeasureControl()
    measure.add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m)







elif selected == "Forcasting":
    st.write("You selected Forcasting")
    # Add your Task 2 related code here
    df2 = pd.read_csv('Forecasting_actual_data.csv', parse_dates=['Datetime'])
    dataset2 = {
        'Forcasting': df2 }
    st.title('Forcasting Data Visualization Dashboard')

    # Path to images
    image_paths = {
        'Forecasting': 'Forecasting.PNG',
        'ground_model_error_metrics': 'ground_model_error_metrics.png',
        'Performance Evaluation Metrics for Ground-Based Model': 'Performance Evaluation Metrics for Ground-Based Model.png',
        'Ground_accuracy': 'Ground_accuracy.png'
    }

    # Sidebar for date and time range selection
    st.sidebar.header('Select Date and Time Range')

    def datetime_range_input(label_start, label_end, min_date, max_date):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(label_start, min_date, key='start_date_input')
            start_time = st.time_input("Start time", pd.Timestamp(min_date).time(), key='start_time_input')
        with col2:
            end_date = st.date_input(label_end, max_date, key='end_date_input')
            end_time = st.time_input("End time", pd.Timestamp(max_date).time(), key='end_time_input')
        start_datetime = pd.to_datetime(f"{start_date} {start_time}")
        end_datetime = pd.to_datetime(f"{end_date} {end_time}")
        return start_datetime, end_datetime


    start_datetime, end_datetime = datetime_range_input(
        'Start date', 'End date',
        df2['Datetime'].min().date(), df2['Datetime'].max().date()
    )

    # Filter Data based on Date and Time Range
    mask = (df2['Datetime'] >= start_datetime) & (df2['Datetime'] <= end_datetime)
    filtered_data = df2.loc[mask]

    # Sidebar for plot customization
    st.sidebar.header('Plot Customization')
    # Display Data
    st.write(f'Data from {start_datetime} to {end_datetime}')
    st.dataframe(filtered_data)

    show_plots = st.sidebar.checkbox('Show Plot Customization', value=True, key='show_plots_checkbox')
    st.title('Forcasting Plotting')

    if show_plots:
        plot_style = st.sidebar.selectbox('Select Plot Style', plt.style.available, key='plot_style_selectbox')
        x_column = st.sidebar.selectbox('Select X-axis Column', filtered_data.columns, key='x_column_selectbox')
        y_column = st.sidebar.selectbox('Select Y-axis Column', filtered_data.columns, key='y_column_selectbox')

        plot_type = st.sidebar.selectbox('Select Plot Type', [
            'Line Plot', 'Histogram', 'Scatter Plot', 'Box Plot', 'Area Plot', 'Pie Chart'
        ], key='plot_type_selectbox')

        # Additional customization options
        title = st.sidebar.text_input('Plot Title', f'{plot_type} of {y_column} vs {x_column}')
        xlabel = st.sidebar.text_input('X-axis Label', x_column)
        ylabel = st.sidebar.text_input('Y-axis Label', y_column)
        color = st.sidebar.color_picker('Select Plot Color', '#1f77b4')
        show_grid = st.sidebar.checkbox('Show Grid', True)
        show_legend = st.sidebar.checkbox('Show Legend', True)
        plot_size = st.sidebar.slider('Plot Size', min_value=6, max_value=20, value=7)

        # Apply Plot Style
        plt.style.use(plot_style)

        # Plot Data
        fig, ax = plt.subplots(figsize=(plot_size, plot_size))
        if plot_type == 'Line Plot':
            ax.plot(filtered_data[x_column], filtered_data[y_column], color=color)
        elif plot_type == 'Histogram':
            ax.hist(filtered_data[y_column], bins=50, color=color)
        elif plot_type == 'Scatter Plot':
            ax.scatter(filtered_data[x_column], filtered_data[y_column], color=color)
        elif plot_type == 'Box Plot':
            ax.boxplot(filtered_data[y_column], patch_artist=True, boxprops=dict(facecolor=color))
        elif plot_type == 'Area Plot':
            ax.fill_between(filtered_data[x_column], filtered_data[y_column], color=color, alpha=0.5)
        else:
            st.stop()

        # Customize plot appearance
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if show_grid:
            ax.grid(True)
        if show_legend:
            ax.legend([plot_type])

        st.pyplot(fig)


        st.sidebar.header('Select Image')
        show_images = st.sidebar.checkbox('Show Images', value=False, key='show_images_checkbox')
        st.title('Forcasting Model Result')

        if show_images:
            selected_image = st.sidebar.selectbox('Choose an image to display', list(image_paths.keys()),
                                                  key='image_selectbox')
            st.image(image_paths[selected_image], caption=selected_image, use_column_width=True)


