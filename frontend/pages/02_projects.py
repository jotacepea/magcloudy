import streamlit as st
import requests
from pages.common.globalconf import pageconfig

pageconfig()

st.header("MagCloudy :blue[Projects] :rocket:")

tab1, tab2, tab3 = st.tabs(["My Projects", "My Project Info", "Owl"])

with tab1:
    st.header("My Projects")
    response = requests.get("http://backend:5000/projects")
    print(response)
    st.write(response.text.splitlines())
with tab2:
    st.header("Get Project Info")
    project_id_input = st.text_input(
        "Enter some project id 👇",
        "6fck2obu3244c",
        key="mcprojectid",
    )
    if project_id_input:
        st.write("Getting info for Project ID: ", project_id_input)
    response = requests.get(
        f"http://backend:5000/projects/{project_id_input}/info"
    )
    print(response)
    st.write(response.text.splitlines())

with tab3:
    st.header("An owl")
    st.write(response.text.splitlines())
