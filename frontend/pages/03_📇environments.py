import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Environments] :card_index:")


tab1, tab2 = st.tabs(["Environments", "Env Info"])

with tab1:
    st.header("All Environments")
    if st.session_state.projectid != 'noprojid':
        st.write(f"_{st.session_state.projectid}_")
        response = requests.get(
            f"http://backend:5000/environments/{st.session_state.projectid}")
        print(response)
        st.write(response.text.splitlines())

with tab2:
    st.header("Environment Info")
    environment_id_input = st.text_input(
        "Enter some environment name 👇",
        value=st.session_state.environmentid if st.session_state.environmentid != 'noenvid' else '',
        placeholder="staging",
    )
    if environment_id_input:
        st.session_state.environmentid = environment_id_input
    if environment_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write("Getting info for Environment: ", environment_id_input)
        response = requests.get(
            f"http://backend:5000/environments/{st.session_state.projectid}/{environment_id_input}/url")
        print(response)
        if response:
            st.write(f"Cloud Env URL [link]({response.text})")
        response = requests.get(
            f"http://backend:5000/environments/{st.session_state.projectid}/{environment_id_input}/info"
        )
        print(response)
        st.write(response.text.splitlines())

theend()
