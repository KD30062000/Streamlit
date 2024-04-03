import streamlit as st
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import tempfile

# Function to calculate the difference between consecutive frames' SSIM values
def calculate_ssim_difference(frames):
    ssim_diff = []
    w = np.array([[[0.114, 0.587, 0.299]]])

    for i in range(len(frames) - 1):
        pre = cv2.convertScaleAbs(np.sum(frames[i] * w, axis=2))
        after = cv2.convertScaleAbs(np.sum(frames[i + 1] * w, axis=2))
        ssim_value = ssim(pre, after)
        ssim_diff.append(ssim_value)

    return ssim_diff

# Streamlit UI
st.title("SSIM Difference Plot")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi"])

if uploaded_file is not None:
    st.write("Video file uploaded successfully!")
    frames = []

    # Save uploaded video file to temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Read frames from the uploaded video file
    cap = cv2.VideoCapture(temp_file_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        else:
            break
    cap.release()

    # Calculate SSIM difference between consecutive frames
    ssim_diff = calculate_ssim_difference(frames)

    # Plot SSIM difference
    plt.plot(ssim_diff, "g")
    plt.title("SSIM Difference Plot")
    plt.xlabel("Frame Index")
    plt.ylabel("SSIM Difference")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
