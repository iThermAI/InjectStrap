import numpy as np


def detect_comp(bit16_frame, threshold: int = -800):
    """This function detects frames that all 3 components
        come in front of the camera, and remind there for a while.
        This function works based on the intensity of pixels when
        the component comes. The treshold is selected based on the
        observation of the pixels' values where the components are there.
        Index 450:580 are where left side component is located.
    Args:
        bit16_frame (numpy.int16): 16bit thermal frame
        threshold (int): treshold for detecting components

    Returns:
        boolean: outputs whether it is component or not
    """

    return np.mean(bit16_frame[:, 450:580]) > threshold


def detect_normal_frames(bit16_frame, threshold: int = -2000):
    """This fucntion output true when frames are in normal more,
        do not contain any components.

    Args:
        bit16_frame (numpy.int16): 16bit thermal frame
        threshold (int): treshold for getting out from component mode frames

    Returns:
        boolean: outputs whether should out the component mode or not
    """

    return np.mean(bit16_frame[:, 450:580]) < threshold


def log_data(
    img,
    com_num,
    log_temp,
    points,
    ratio: float = 0.423,
    intercept: float = 23.97,
    region_temp_treshold: int = 90,
    squre_dim: int = 50,
):
    """This function logs information from selected part.
        Converting from pixels' values to Temprature is done
        with a linear scaling. The ratio and intercept for this
        line is drived from 40-50 static frame.

    Args:
        img (numpy.int8): 8bit gray scale img
        com_num (int): Component's frame number
        log_temp (dict): Aux variable for logging information
        points (dict): Selected points for logging information
        ratio (float, optional): Ratio of the scaler line. Defaults to 0.423.
        intercept (float, optional): Intercept of the scaler line. Defaults to 23.97.
        region_temp_treshold (int, optional): A treshold for discarting pixels that do not cointain component. Defaults to 90.
        squre_dim (int, optional): Area where pixels should be saved. Defaults to 50.

    Returns:
        log_temp (dict): logged info for a frame that contain components
    """

    log_temp["component"].append(com_num)

    assert squre_dim % 2 == 0, "The diameter must be an even number"

    margin = int(squre_dim / 2)

    for key, val in points.items():
        sub_arr = (ratio) * img[
            val[1] - margin : val[1] + margin, val[0] - margin : val[0] + margin
        ] + intercept
        mask = sub_arr > region_temp_treshold  # Upper to 90 C
        sum_arr = np.sum(sub_arr * mask)
        len_arr = np.sum(mask)
        log_temp[key].append(f"{sum_arr / len_arr:.2f} (C)")

    return log_temp
