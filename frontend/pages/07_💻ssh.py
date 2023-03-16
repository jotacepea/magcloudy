import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Secure Shell] :computer:")


tab1, tab2 = st.tabs(
    ["SHH", ""])

with tab1:
    st.header("Instances")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading config file for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/ssh/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            for inst in response.text.strip().split():
                st.write(f" ```ssh {inst}``` ")

theend()
