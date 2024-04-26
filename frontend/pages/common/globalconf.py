import streamlit as st


def pageconfig():
    st.set_page_config(page_title="MagCloudy",
                       layout="wide",
                       initial_sidebar_state="expanded")

    hide_menu = """
    <style>
    #MainMenu {
        visibility:hidden;
    }
    .stDeployButton {
        display:none;
    }
    footer{
        visibility:hidden;
    }
    #stDecoration {
        display:none;
    }
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)


def theend():
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
