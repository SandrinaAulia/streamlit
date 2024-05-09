import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from streamlit_option_menu import option_menu

import base64
from view import home
from view import clustering

# Function to read image file as base64
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# # Set page configuration
st.set_page_config(layout="wide", page_title=" Dashboard Analisis Segmentasi Pelanggan ", page_icon="📊")

# Function to set background image using base64
def set_background():
    img = get_img_as_base64("data/air.jpg")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to set sidebar image
def set_sidebar_image():
    st.sidebar.image("data/logo.png", caption="")
    st.sidebar.title("Welcome!")

    with st.sidebar:
        page = option_menu("Main Menu",
                           ["Home", "Clustering"],
                           icons=["house", "book"],
                           menu_icon="cast", default_index=0,
                           styles={
                               "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px",
                                            "--hover-color": "#53a2c2"},
                               "nav-link-selected": {"background-color": "#53a2c2"},
                           })

    if page == "Home":
        home.main()
    elif page == "Clustering":
        clustering.main()

# Main function
def main():
    set_background()  # Set background image
    set_sidebar_image()  # Set sidebar image

if __name__ == '__main__':
    main()