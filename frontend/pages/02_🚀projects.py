import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Projects] :rocket:")

st.header("My Projects")
response = requests.get("http://backend:5000/projects")
print(response)
st.write(f" ```{response.text}``` ")

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


tab1, tab2, tab3 = st.tabs(
    ["Project Info", "Project Settings", "Project Users"])

with tab1:
    st.header("Info")
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
        for indx, projinfoline in enumerate(response.text.strip().split('\n')):
            if 'title' in projinfoline:
                projinfoline = projinfoline.replace("|", "")
                print(projinfoline)
                st.write(f" ```{projinfoline}``` ")
        st.write(f" ```{response.text}``` ")
with tab2:
    st.header("Settings")
    settings_project_id_input = st.text_input(
        "Enter some project id 👇",
        value=st.session_state.projectid if st.session_state.projectid != 'noprojid' else '',
        placeholder="uyjl6ksvl3koy",
        key="settings_project_id_text_input",
    )
    if settings_project_id_input:
        st.write("Getting settings for Project ID: ", info_project_id_input)
        response = requests.get(
            f"http://backend:5000/projects/{info_project_id_input}/settings"
        )
        print(response)
        st.write(f" ```{response.text}``` ")
with tab3:
    st.header("Users")
    settings_project_id_input = st.text_input(
        "Enter some project id 👇",
        value=st.session_state.projectid if st.session_state.projectid != 'noprojid' else '',
        placeholder="uyjl6ksvl3koy",
        key="users_project_id_text_input",
    )
    if settings_project_id_input:
        st.write("Getting users for Project ID: ", info_project_id_input)
        response = requests.get(
            f"http://backend:5000/users/{info_project_id_input}"
        )
        print(response)
        st.write(f" ```{response.text}``` ")

theend()
