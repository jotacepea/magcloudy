import streamlit as st
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.write("# Welcome to MagCloudy! :dizzy:")

st.sidebar.success("Select an option above.")

st.markdown(
    """
    MagCloudy is a tool built specifically for
    interacting with Adobe Commerce Cloud projects.

    ### Want to learn more?
    - Check out [cloud-cli](https://experienceleague.adobe.com/docs/commerce-cloud-service/user-guide/dev-tools/cloud-cli.html?lang=en)
    - Jump into our [documentation](https://experienceleague.adobe.com/docs/commerce-cloud-service/user-guide/overview.html?lang=en)

"""
)

if 'projectid' not in st.session_state:
    st.session_state.projectid = 'noprojid'
if 'environmentid' not in st.session_state:
    st.session_state.environmentid = 'noenvid'
if 'env_target_type' not in st.session_state:
    st.session_state.env_target_type = None

theend()
