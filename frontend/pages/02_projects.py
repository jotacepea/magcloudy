import streamlit as st
import requests
import time
from numpy import random

from pages.common.globalconf import pageconfig

pageconfig()


# http://127.0.01:5000/ is from the flask api
# response = requests.get("http://backend:5000/posts/2")
# print(response.json())
# st.write(response.json())

# response = requests.get("http://backend:5000/check")
# print(response.json())
# st.write(response.json())


def get_user_name():
    return 'John'


with st.echo():
    # Everything inside this block will be both printed to the screen
    # and executed.

    def get_punctuation():
        return '!!!'

    greeting = "Hi there, "
    value = get_user_name()
    punctuation = get_punctuation()

    st.write(greeting, value, punctuation)

# And now we're back to _not_ printing to the screen
foo = 'bar'
st.write('Done!')


with st.container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(random.randn(50, 3))

st.write("This is outside the container")

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=33)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=33)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=33)

st.header('This is a header')
st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')

# left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
# left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
# with right_column:
# chosen = st.radio(
# 'Sorting hat',
# ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
# st.write(f"You are in {chosen} house!")

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")
