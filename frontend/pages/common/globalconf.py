import streamlit as st


def pageconfig():
    st.set_page_config(page_title="ABC", layout="wide",
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
