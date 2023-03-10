import streamlit as st
import requests
from pages.common.globalconf import pageconfig

pageconfig()

st.write("# Welcome to MagCloudy :blue[Info Page]! 👋")

tab1, tab2, tab3 = st.tabs(["Version", "Auth", "List"])

with tab1:
    st.header("MagCloudy: Cli Version")
    response = requests.get("http://backend:5000/mgcliversion")
    print(response)
    st.write(response.text.splitlines())

with tab2:
    st.header("MagCloudy: Cli Auth Info")
    response = requests.get("http://backend:5000/mgcliauth")
    print(response)
    st.write(response.text.splitlines())

with tab3:
    st.header("MagCloudy: Cli Cmd List")
    response = requests.get("http://backend:5000/mgclilist")
    print(response)
    st.write(response.text.splitlines())
