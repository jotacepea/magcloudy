import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Projects] :rocket:")

main_project_id_input = st.text_input(
    "Enter project id you want to work with:",
    value=st.session_state.projectid if st.session_state.projectid != 'noprojid' else '',
    max_chars=13,
    placeholder="6fck2obu3244c",
)
if main_project_id_input:
    st.session_state.projectid = main_project_id_input

if st.session_state.projectid != 'noprojid':
    response = requests.get(
        f"http://backend:5000/webui/{st.session_state.projectid}")
    print(response)
    if response:
        st.write(f"Cloud Web UI [link]({response.text})")


tab1, tab2 = st.tabs(["My Projects", "My Project Info"])

with tab1:
    st.header("My Projects")
    response = requests.get("http://backend:5000/projects")
    print(response)
    st.write(f" ```{response.text}``` ")
with tab2:
    st.header("Project Info")
    info_project_id_input = st.text_input(
        "Enter some project id 👇",
        value=st.session_state.projectid if st.session_state.projectid != 'noprojid' else '',
        placeholder="uyjl6ksvl3koy",
    )
    if info_project_id_input:
        st.write("Getting info for Project ID: ", info_project_id_input)
        response = requests.get(
            f"http://backend:5000/projects/{info_project_id_input}/info"
        )
        print(response)
        st.write(f" ```{response.text}``` ")

theend()
