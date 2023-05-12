import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Projects] :rocket:")

st.header("My Projects")
response = requests.get("http://backend:5000/projects")
print(response)
st.write(f" ```\n{response.text.strip()}\n``` ")

main_project_id_input = st.text_input(
    "Enter project id you want to work with: 👇",
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
        st.write(
            f"### Cloud Project [Web UI]({response.text.strip()}) ###")


tab1, tab2, tab3, tab4 = st.tabs(
    ["Project Info", "Project Subscription", "Project Settings", "Project Users"])

with tab1:
    st.header("Info")
    if st.session_state.projectid != 'noprojid':
        st.write("Getting info for Project ID: ", st.session_state.projectid)
        response = requests.get(
            f"http://backend:5000/projects/{st.session_state.projectid}/info"
        )
        print(response)
        for indx, projinfoline in enumerate(response.text.strip().split('\n')):
            if 'title' in projinfoline:
                projinfoline = projinfoline.replace("|", "")
                print(projinfoline)
                st.write(f" ```{projinfoline}``` ")
        st.write(f" ```\n{response.text.strip()}\n``` ")
with tab2:
    st.header("Subscription")
    if st.session_state.projectid != 'noprojid':
        st.write("Getting Subscription info for Project ID: ",
                 st.session_state.projectid)
        response = requests.get(
            f"http://backend:5000/projects/{st.session_state.projectid}/subscription"
        )
        print(response)
        st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("Settings")
    if st.session_state.projectid != 'noprojid':
        st.write("Getting settings for Project ID: ",
                 st.session_state.projectid)
        response = requests.get(
            f"http://backend:5000/projects/{st.session_state.projectid}/settings"
        )
        print(response)
        for indx, projsettline in enumerate(response.text.strip().split('\n')):
            if 'development_' in projsettline:
                projsettline = projsettline.replace(",", "")
                print(projsettline)
                st.write(f" ```{projsettline}``` ")
        st.write(f" ```\n{response.text.strip()}\n``` ")
with tab4:
    st.header("Users")
    if st.session_state.projectid != 'noprojid':
        st.write("Getting users for Project ID: ", st.session_state.projectid)
        response = requests.get(
            f"http://backend:5000/users/{st.session_state.projectid}"
        )
        print(response)
        st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
