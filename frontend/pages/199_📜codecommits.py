import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Code Commits] :scroll:")


tab1, tab2 = st.tabs(
    ["Commits", "Commit Info"])

with tab1:
    st.header("Last commits")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading Commits for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/commits/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Info")
    commit_id_input = st.text_input(
        "Enter some code commit id 👇",
        value='HEAD',
        placeholder='HEAD',
    )
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Commit info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/commits/{st.session_state.projectid}/{st.session_state.environmentid}/{commit_id_input}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
