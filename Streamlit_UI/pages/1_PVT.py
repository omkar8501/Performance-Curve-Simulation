import streamlit as st
import pandas as pd

# Set page layout
st.set_page_config(layout="wide")

# Page Title
st.title('PVT Data')

# Empty Space
st.markdown("<br><br>", unsafe_allow_html=True)

# Label names and their respective keys
labels = ['Oil Gravity', 'Gas Gravity', 'Water Specific Gravity', 'Bubble Point', 'Reservoir Temperature']
keys = ['oil_api', 'sg_gas', 'sg_water', 'bubble_pt', 'res_temp']
formats = ["%.1f", "%.2f", "%.2f", "%.1f", '%.1f']
units = ['°API', '', '', 'psia', '°C']
steps = [0.1, 0.01, 0.01, 0.1, 0.1]

# Dictionary to store the entered values
values = {}

# Loop to create the input pairs dynamically
for i in range(len(labels)):
    col1, col2, col3 = st.columns([1, 1, 1.5])

    with col1:
        st.markdown(f"<p style='font-size:20px; margin-bottom: 0;'>{labels[i]}</p>", unsafe_allow_html=True)

    with col2:
        values[labels[i]] = st.number_input(
            ' ',
            format=formats[i],
            step=steps[i],
            label_visibility='collapsed',
            key=keys[i]
        )

    with col3:
        st.markdown(f"<p style='font-size:20px; margin-bottom: 0; text-align: left; padding-left:20px'>{units[i]}</p>", unsafe_allow_html=True)

