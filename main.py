import numpy as np
import pandas as pd

import cv2
import argparse

from collections import defaultdict
from utils.utils import detect_comp, detect_normal_frames, log_data

# Selected points for gathering information
SELECTED_POINTS = {
    "1": (215, 45),
    "2": (255, 255),
    "3": (175, 225),
    "4": (240, 422),
    "5": (510, 32),
    "6": (540, 255),
    "7": (465, 225),
    "8": (450, 405),
    "9": (300, 120),
    "10": (440, 157),
    "11": (361, 183),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vid_dir", type=str, default="./vid1.ravi")
    parser.add_argument("--save_dir", type=str, default="./result/dataset.csv")
    args = parser.parse_args()
    print("Argument: ", args)

    assert args.vid_dir[-4:] == "ravi", "The format of the video must be *.ravi"

    log_temp = {}  # Temp Variable for extracting features
    log_temp["component"] = []

    for key, val in SELECTED_POINTS.items():
        log_temp[key] = []

    log_temp["Cycle"] = []

    cap = cv2.VideoCapture(args.vid_dir)  # Opens a video file for capturing

    # Fetch undecoded RAW video streams
    cap.set(
        cv2.CAP_PROP_FORMAT, -1
    )  # Format of the Mat objects. Set value -1 to fetch undecoded RAW video streams (as Mat 8UC1). [Using cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) is not working]

    cols = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Get video frames width
    rows = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Get video frames height

    frame_rate = cap.get(
        cv2.CAP_PROP_FPS
    )  # Get the frame rate for calculating the cycle
    flag = 0  # Indicator of a frame with component
    frame_num = 0
    prv_frame = 0  # Aux variable for frame detection
    comp_cycle = defaultdict(int)  # For logging the cycle of the frame components
    comp_idx = 0  # Aux variable for

    while True:
        (
            ret,
            frame,
        ) = (
            cap.read()
        )  # Read next video frame (undecoded frame is read as long row vector).

        if not ret:
            break  # Stop reading frames when ret = False (after the last frame is read).

        # Counting the frame number
        frame_num += 1

        # View frame as int16 elements, and reshape to cols x rows (each pixel is signed 16 bits)
        frame = frame.view(np.int16).reshape(rows, cols)

        frame_8bit = np.zeros((rows, cols), dtype=np.uint8)

        # It looks like the first line contains some data (not pixels).
        # data_line = frame[0, :]
        frame_roi = frame[1:, :]  # Ignore the first row.

        # Normalizing frame to range [0, 255], and get the result as type uint8 (this part is used just for making the data visible).
        normed = cv2.normalize(
            frame_roi, frame_8bit, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
        )
        normed = np.uint8(normed)

        # Finding frames that contain components
        com_res = detect_comp(frame_roi)

        # Using frames contain components for logging data
        if com_res and flag == 0:
            comp_cycle[comp_idx] = frame_num
            flag = 1
            comp_idx += 1
            log_temp = log_data(normed, comp_idx, log_temp, SELECTED_POINTS)
            log_temp["Cycle"].append(f"{(frame_num-prv_frame)/frame_rate:.2f} (s)")
            prv_frame = frame_num
        elif detect_normal_frames(frame_roi):
            flag = 0

    # Saving the output dataset
    pd.DataFrame(log_temp).to_csv(args.save_dir, index=False)
    cap.release()


if __name__ == "__main__":
    main()
