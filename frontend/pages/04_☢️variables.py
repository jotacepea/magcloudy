import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Environment Variables] :radioactive_sign:")


tab1, tab2 = st.tabs(["Project Vars", "Environment Vars"])

with tab1:
    st.header("Env Variables at Project Level")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write("Getting Env Vars for: ", st.session_state.projectid)
        response = requests.get(
            f"http://backend:5000/variables/{st.session_state.projectid}")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

with tab2:
    st.header("Env Variables at Environment Level")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write("Getting Env Vars for: ", st.session_state.projectid,
                 "in", st.session_state.environmentid)
        response = requests.get(
            f"http://backend:5000/variables/{st.session_state.projectid}/{st.session_state.environmentid}/e")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

theend()
