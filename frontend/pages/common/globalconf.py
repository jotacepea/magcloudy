import streamlit as st

enable_select_proj_env_warning = True

def pageconfig():
    st.set_page_config(
        page_title="MagCloudy",
        page_icon=":material/cloud_alert:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    hide_menu = """
    <style>
    #MainMenu {
        visibility: hidden;
    }
    .stAppDeployButton {
        display: none;
    }
    footer{
        visibility: hidden;
    }
    #stDecoration {
        display: none;
    }
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)

def set_default_cache_values():
    if 'projectid' not in st.session_state:
        st.session_state.projectid = 'noprojid'
    if 'environmentid' not in st.session_state:
        st.session_state.environmentid = 'noenvid'
    if 'envappid' not in st.session_state:
        st.session_state.envappid = 'noenvappid'
    if 'env_target_type' not in st.session_state:
        st.session_state.env_target_type = None
    if 'projectregiondomain' not in st.session_state:
        st.session_state.projectregiondomain = None

def clear_session_state():
    keys = list(st.session_state.keys())
    for key in keys:
        if key not in ['reqfqdn', 'default_api_backend_name', 'default_api_backend_port']:
            st.session_state.pop(key)
    set_default_cache_values()

def clear_cache():
    st.cache_data.clear()
    #st.cache_resource.clear() # Not needed for now
    clear_session_state()

def theend(enable_select_proj_env_warning = True):
    if st.session_state.projectid == 'noprojid':
        st.sidebar.write(
            f"Selected Project ID: :red[{st.session_state.projectid}]")
    else:
        st.sidebar.write(
            f"Selected Project ID: :blue[{st.session_state.projectid}]")
    if st.session_state.environmentid == 'noenvid':
        st.sidebar.write(
            f"Selected Environment ID: :red[{st.session_state.environmentid}]")
    else:
        st.sidebar.write(
            f"Selected Environment ID: :green[{st.session_state.environmentid}]")
    if st.session_state.envappid == 'noenvappid':
        st.sidebar.write(
            f"Selected App ID: :red[{st.session_state.envappid}]")
    else:
        st.sidebar.write(
            f"Selected App ID: :green[{st.session_state.envappid}]")
    if st.session_state.env_target_type is None:
        st.sidebar.write(
            f"Environment Type: :red[{st.session_state.env_target_type}]")
    else:
        st.sidebar.write(
            f"Environment Type: :orange[{st.session_state.env_target_type}]")
    if st.session_state.projectregiondomain is None:
        st.sidebar.write(
            f"Project Region Domain: :red[{st.session_state.projectregiondomain}]")
    else:
        st.sidebar.write(
            f"Project Region Domain: :orange[{st.session_state.projectregiondomain}]")
    
    # Warning message to remember users to select project and environment, if not already selected!!
    if st.session_state.projectid == 'noprojid' or st.session_state.environmentid == 'noenvid':
        if enable_select_proj_env_warning:
            st.warning('''Please remember to select the Project ID **(in projects)** and 
                       the Environment **(in environments info)** you would like to work with!!!''', icon="⚠️")
