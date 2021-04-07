"""This script convert the labels to yolo normalized yolo format"""
import argparse
import fileinput
import os

import cv2
import numpy as np
from tqdm import tqdm


def converter(file_name, coords):
    """convert xmin, ymin, xmax, ymax coordinates normalized yolo format"""
    os.chdir("..")
    image = cv2.imread(file_name + ".jpg")
    image_h = int(image.shape[0])
    image_w = int(image.shape[1])
    xmin = int(coords[0])
    xmax = int(coords[2])
    ymin = int(coords[1])
    ymax = int(coords[3])
    x = (xmin + (xmax-xmin)/2) * 1.0 / image_w
    y = (ymin + (ymax-ymin)/2) * 1.0 / image_h
    w = (xmax-xmin) * 1.0 / image_w
    h = (ymax-ymin) * 1.0 / image_h
    os.chdir("Label")
    return [x, y, w, h]


ROOT_DIR = os.getcwd()

# create dictionary that map class names to indexes
classes = {}
with open("classes.txt", "r") as f:
    for num, line in enumerate(f, 0):
        line = line.rstrip("\n")
        classes[line] = num
    f.close()

# get into Dataset folder
os.chdir(os.path.join("OID", "Dataset"))
DIRS = os.listdir(os.getcwd())

for DIR in DIRS:
    if os.path.isdir(DIR):
        os.chdir(DIR)
        print("Currently in directory:", DIR)

        CLASS_DIRS = os.listdir(os.getcwd())
        for CLASS_DIR in CLASS_DIRS:
            if os.path.isdir(CLASS_DIR):
                os.chdir(CLASS_DIR)
                print("Converting for class:", CLASS_DIR)

                os.chdir("Label")

                for filename in tqdm(os.listdir(os.getcwd())):
                    filename_str = str.split(filename, ".")[0]
                    if filename.endswith(".txt"):
                        annotations = []
                        with open(filename) as f:
                            for line in f:
                                for class_type in classes:
                                    line = line.replace(class_type, str(classes.get(class_type)))
                                labels = line.split()
                                coords = np.asarray([float(labels[1]), float(labels[2]), float(labels[3]), float(labels[4])])
                                coords = converter(filename_str, coords)
                                labels[1:] = coords
                                newline = " ".join(str(i) for i in labels)
                                line = line.replace(line, newline)
                                annotations.append(line)
                            f.close()
                        os.chdir("..")
                        with open(filename, "w") as outfile:
                            for line in annotations:
                                outfile.write(line)
                                outfile.write("\n")
                            outfile.close()
                        os.chdir("Label")
                os.chdir("..")
                os.chdir("..")
        os.chdir("..")
