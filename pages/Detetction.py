import streamlit as st
import os
import cv2
import random
import matplotlib.pyplot as plt

# Function to delete random frames from a video
def delete_random_frames(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Generate list of random frame indices to delete
    frames_to_delete = random.sample(range(frame_count), 10)
    frames_to_delete.sort()

    # Open output video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_index = 0
    deleted_frames_indices = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index not in frames_to_delete:
            out.write(frame)
        else:
            deleted_frames_indices.append(frame_index)
        frame_index += 1

    cap.release()
    out.release()

    return deleted_frames_indices

# Function to plot the deleted frames
def plot_deleted_frames(frame_count, deleted_frames_indices):
    deleted_frames = [0] * frame_count
    for idx in deleted_frames_indices:
        deleted_frames[idx] = 1

    plt.figure(figsize=(10, 6))
    plt.plot(range(frame_count), deleted_frames, 'ro')
    plt.title('Deleted Frames')
    plt.xlabel('Frame Index')
    plt.ylabel('Deleted')
    plt.yticks([0, 1], ['No', 'Yes'])
    plt.grid(True)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# Streamlit UI
st.title("Random Frame Deletion")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi"])

if uploaded_file is not None:
    st.write("Video file uploaded successfully!")
    video_path = "input_video.mp4"
    output_path = "output_video.mp4"

    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    deleted_frames_indices = delete_random_frames(video_path, output_path)

    st.write("Random frames deleted successfully!")
    st.write("You can download the modified video below:")
    st.download_button(label="Download modified video", data=open(output_path, "rb").read(), file_name="output_video.mp4")

    st.write("Visualizing deleted frames:")
    plot_deleted_frames(frame_count, deleted_frames_indices)
