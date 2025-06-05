import os
from pathlib import Path


class Constant:

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_DIR = os.path.join(BASE_DIR, "data") 
    INPUT_DIR = os.path.join(DATA_DIR, "input") 
    OUTPUT_DIR = os.path.join(DATA_DIR, "output")  
    MODEL_DIR = os.path.join(BASE_DIR,"models/lid.176.bin") 

    FastText_path = os.path.join(INPUT_DIR, "fastText.txt")


# print(Constant.MODEL_DIR)
