import numpy as np
from loguru import logger


def check_dimensions(image, mask):
    """Check presence and spacing of images"""
    if image.GetDimension() != mask.GetDimension():
        text = f'Input dimensions mismatch:\nImages has {image.GetDimension()}\nSeg. mask has {mask.GetDimension()}'
        logger.warning(text)
        raise UserWarning(text)


def check_origin(image, mask):
    """Check presence and spacing of images"""
    diff = np.subtract(image.GetOrigin(), mask.GetOrigin())
    diff = diff[diff < 1e-2]
    if len(diff) != 3:
        text = f'Input image mismatch:\nImages has {image.GetOrigin()}\nSegmentation mask has {mask.GetOrigin()}'
        logger.warning(text)
        raise UserWarning(text)
