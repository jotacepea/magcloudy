import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Activities] :bookmark_tabs:")

activity_id_input = st.text_input(
    "Enter some activity id 👇",
    placeholder='2eqedl7pxynpa',
)

tab1, tab2, tab3 = st.tabs(
    ["Activities",
     "Activity Info",
     "Activity Log"])

with tab1:
    st.header("Last Project Activities in this Env")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading activities for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/activities/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Activity info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if activity_id_input:
            response = requests.get(
                f"{st.session_state.reqfqdn}/activities/{st.session_state.projectid}/{st.session_state.environmentid}/{activity_id_input}")
        else:
            response = requests.get(
                f"{st.session_state.reqfqdn}/activities/{st.session_state.projectid}/{st.session_state.environmentid}/last")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")


with tab3:
    st.header("Log")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Avtivity log for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if activity_id_input:
            response = requests.get(
                f"{st.session_state.reqfqdn}/activities/log/{st.session_state.projectid}/{st.session_state.environmentid}/{activity_id_input}")
        else:
            response = requests.get(
                f"{st.session_state.reqfqdn}/activities/log/{st.session_state.projectid}/{st.session_state.environmentid}/last")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
