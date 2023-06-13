import os
import cv2
import numpy as np
import pytesseract


class UnsupportedFileTypeError(BaseException):
    pass
    

    
def check_type(path:str) -> str:
    """Check the existance and the type of the file

    Args:
        path (str): file path

    Returns:
        type (str): file type (img, pdf)
    """
    if not os.path.isfile(path=path):
        raise FileNotFoundError(f"There is no file at {path}")

    ext = path[-4:]
    if ext == ".pdf":
        return "pdf"
    elif ext == ".jpg" or ext == ".png" or ext == "jpeg":
        return "img"
    else:
        raise UnsupportedFileTypeError("Unsupported file type!\nPlease check that your file end with '.pdf', '.jpg', '.jpeg' or '.png'")



def image_preprocessing(img_path: str) -> np.array:
    """
    Load, delete background, binarize and clean image
    
    Args:
        img_path (str): path of image
    Returns:
        image (np.array): cleared image
    """
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    se = cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
    bg = cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
    
    img = cv2.divide(img, bg, scale=200)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU )[1] 

    return img


CHARS = ["ذ", "د","ج","ح","خ","ه","ع","غ","ف","ق","ث","ص","ض","ط","ك","م","ن","ت","ا","ل", " ", "-", "ب",
         "ي","س","ش","ظ","و","ز", "ة","ى","ﻻ","ر","ؤ","ئ","ء","أ","0","9","8","7","6","5","4","3","2","1"]


def parsing_text(img: np.array) -> str:
    
    text = pytesseract.image_to_string(img, lang="ara").splitlines()
    text = [line for line in text if line != '']
    cleared_lines = []

    for line in text:
        cleared_line = ""
        for char in line:
            if char in CHARS:
                cleared_line += char

        cleared_lines.append(cleared_line)

    return cleared_lines



def create_lines(text):
    lines = []
    curr_line = ""
    for char in text:
        curr_line += char
        if char == "." or char == ":":
            lines.append(curr_line)
            curr_line = ""

    return lines