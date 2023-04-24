import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Disk Usage] :floppy_disk:")


tab1, tab2 = st.tabs(
    ["Disk", "Mounts"])

with tab1:
    st.header("Disk Usage per Instance")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting disk usage for: **{st.session_state.projectid}** in **{st.session_state.environmentid}** Instances")
        response = requests.get(
            f"http://backend:5000/ssh/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            if len(response.text.strip().split()) == 1:
                st.write(f" ```HD Usage {response.text.strip().split()}``` ")
                response = requests.get(
                    f"http://backend:5000/disk/{st.session_state.projectid}/{st.session_state.environmentid}")
                print(response)
                st.write(f" ```\n{response.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response.text.strip().split()):
                    st.write(f" ```HD Usage {inst}``` ")
                    response = requests.get(
                        f"http://backend:5000/disk/{st.session_state.projectid}/{st.session_state.environmentid}/{indx + 1}")
                    print(indx, inst, response)
                    st.write(f" ```\n{response.text.strip()}\n``` ")
with tab2:
    st.header("Mounts Usage per Instance")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Mounts size for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/mounts/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
        response = requests.get(
            f"http://backend:5000/mounts/{st.session_state.projectid}/{st.session_state.environmentid}/size")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
