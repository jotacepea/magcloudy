import streamlit as st
import requests
from pages.common.globalconf import pageconfig

pageconfig()

st.write("# Welcome to INFO PAGE! 👋")

response = requests.get("http://backend:5000/check")
print(response)
st.write(response.text.splitlines())


response = requests.get("http://backend:5000/magecloud")
print(response)
st.write(response.text.splitlines())
