import requests
import streamlit as st

API_URL = "http://ml-api/predict"
st.title("ML Inference Platform")

uploaded = st.file_uploader("Upload Image")

if uploaded:
    res = requests.post(API_URL, files={"image": uploaded})
    st.json(res.json())