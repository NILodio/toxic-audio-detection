import requests as rs
import streamlit as st


def get_api(params):
    url = "http://api:8086/audio_predict/"
    response = rs.get(url, params=params, timeout=20)
    return response.content


def main():
    st.title("Offensive Audio Detector")

    st.write("Upload an audio file (.mp3 or .wav)")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

    if uploaded_file is not None and st.button("Check Audio"):
        params = {"audio_file": uploaded_file}
        data = get_api(params)

        st.write(data.decode("utf-8"))

        # Display result based on API response
        if b"1" in data:
            st.error("Offensive Audio Detected!")
        else:
            st.success("No Offensive Audio Detected!")


if __name__ == "__main__":
    main()
