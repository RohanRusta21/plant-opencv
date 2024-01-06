import streamlit as st
import cv2
import numpy as np

def process_image(original_image, processing_factor):
    st.image(original_image, channels="BGR", caption="Original Image")

    b, g, r = cv2.split(original_image)
    st.image(r, channels="GRAY", caption="Red Channel")
    st.image(g, channels="GRAY", caption="Green Channel")
    st.image(b, channels="GRAY", caption="Blue Channel")

    disease = r - g
    alpha = b
    get_alpha(original_image, alpha)
    st.image(alpha, channels="GRAY", caption="Alpha Channel")

    for i in range(original_image.shape[0]):
        for j in range(original_image.shape[1]):
            if int(g[i, j]) > processing_factor:
                disease[i, j] = 255

    st.image(disease, channels="GRAY", caption="Disease Image")
    display_disease_percentage(disease, alpha)

def get_alpha(original_image, alpha):
    for i in range(original_image.shape[0]):
        for j in range(original_image.shape[1]):
            if original_image[i, j, 0] > 200 and original_image[i, j, 1] > 200 and original_image[i, j, 2] > 200:
                alpha[i, j] = 255
            else:
                alpha[i, j] = 0

def display_disease_percentage(disease, alpha):
    count = 0
    res = 0
    for i in range(disease.shape[0]):
        for j in range(disease.shape[1]):
            if alpha[i, j] == 0:
                res += 1
            if disease[i, j] < st.session_state.processing_factor:
                count += 1
    percent = (count / res) * 100
    st.session_state.disease_percent = "Percentage Disease: " + str(round(percent, 2)) + "%"

def get_file():
    file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if file:
        original_image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
        return original_image
    else:
        return None

st.title("Plant Disease Detector")
processing_factor = st.slider("Processing Factor", 0, 255, 150)
st.session_state.processing_factor = processing_factor

uploaded_image = get_file()

if uploaded_image is not None:
    process_image(uploaded_image, processing_factor)
    st.write(st.session_state.disease_percent)
else:
    st.write("No File!")
