import requests as rs
import streamlit as st

text = st.text_input("Text")


def get_api(params):
    url = "http://api:8086/predict/"
    response = rs.get(url, params=params, timeout=20)
    return response.content


if st.button("Get response"):
    params = {
        "text": text,
    }

    data = get_api(params)
    st.write(data)

    if b"1" in data:
        st.text("Offensive text")
    else:
        st.text("Not offensive")
