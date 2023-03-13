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
    footer{
        visibility:hidden;
    }
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)


def theend():
    st.sidebar.write(
        f"Selected Project ID: {st.session_state.projectid}")
    st.sidebar.write(
        f"Selected Environment ID: {st.session_state.environmentid}")
