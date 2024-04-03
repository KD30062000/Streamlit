# import streamlit as st
# import cv2
# import numpy as np
# import tempfile
# import os
#
# # Function to detect forgery in a video
# def detect_forgery(video):
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         temp_file.write(video.read())
#         temp_file_path = temp_file.name
#     cap = cv2.VideoCapture(temp_file_path)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#
#     frame_difference_threshold = 40398001  # Adjust threshold as per your requirement
#
#     forgery_detected = False
#
#     # Read the first frame
#     ret, prev_frame = cap.read()
#     prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
#
#     # Loop through the frames
#     for i in range(1, frame_count):
#         ret, curr_frame = cap.read()
#         if not ret:
#             break
#
#         curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
#
#         # Calculate frame difference
#         frame_difference = cv2.absdiff(curr_frame_gray, prev_frame)
#         st.write(np.sum(frame_difference))
#
#         # Check if frame difference exceeds threshold
#         if np.sum(frame_difference) > frame_difference_threshold:
#             forgery_detected = True
#             break
#
#         prev_frame = curr_frame_gray
#
#     cap.release()
#     os.unlink(temp_file_path)
#
#     if forgery_detected:
#         return "Forged"
#     else:
#         return "Authentic"
#
# def main():
#     st.title("Video Forgery Detection App")
#     st.write("Upload a video to check if it's forged or authentic.")
#
#     # File uploader widget
#     uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi"])
#
#     if uploaded_file is not None:
#         # Display the uploaded video
#         st.video(uploaded_file)
#
#         # Run forgery detection
#         forgery_result = detect_forgery(uploaded_file)
#
#         # Display the result
#         st.write("Result:", forgery_result)
#
# if __name__ == "__main__":
#     main()


import streamlit as st
import cv2
import tempfile

def detect_forgery(original_path, forged_path):
    original_video = cv2.VideoCapture(original_path)
    forged_video = cv2.VideoCapture(forged_path)

    # Check if videos opened successfully
    if not original_video.isOpened() or not forged_video.isOpened():
        st.error("Error: Could not open videos.")
        return False

    frame_count = 0
    forgery_detected = False
    while True:
        # Read frames from both videos
        ret_o, frame_o = original_video.read()
        ret_f, frame_f = forged_video.read()

        # Check if frames were read successfully
        if not ret_o or not ret_f:
            break

        # Compare frames pixel by pixel
        difference = cv2.absdiff(frame_o, frame_f)
        mean_diff = cv2.mean(difference)[0]

        # Adjust threshold based on your requirement
        threshold = 2  # You can adjust this threshold value
        if mean_diff > threshold:
            forgery_detected = True
            break

        frame_count += 1

    # Release video objects
    original_video.release()
    forged_video.release()

    if forgery_detected:
        st.warning("Forgery detected: Frames were deleted.")
    else:
        st.success("No forgery detected: Frames were not deleted.")

# Streamlit UI
st.title("Forgery Detection")

original_file = st.file_uploader("Upload original video file", type=["mp4", "avi"])
forged_file = st.file_uploader("Upload forged video file", type=["mp4", "avi"])

if original_file and forged_file:
    st.write("Original video file uploaded successfully!")
    st.write("Forged video file uploaded successfully!")

    # Save uploaded files to temporary directory
    with tempfile.NamedTemporaryFile(delete=False) as temp_original_file:
        temp_original_file.write(original_file.read())
        original_path = temp_original_file.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_forged_file:
        temp_forged_file.write(forged_file.read())
        forged_path = temp_forged_file.name

    detect_forgery(original_path, forged_path)




