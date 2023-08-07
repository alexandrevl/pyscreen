#!/usr/bin/env python3
import argparse
import gc
import mimetypes
import os
import cv2
from pathlib import Path

from utils.clean_folders import clean_folders
from utils.colors import colors_img
from utils.frames import (clean_unique, analyze_image_similarity, get_frames,
                          remove_duplicates)
from utils.text_compute import text_compute


def parse_arguments():
    parser = argparse.ArgumentParser(description='PyScreen - Advanced Screen Recording Analyzer')
    parser.add_argument('--input', type=str, help='The path to the input video file.')
    parser.add_argument('--disable_chatgpt', action='store_true', help='Disable ChatGPT analysis.')
    args = parser.parse_args()

    if args.input is None:
        print("No input file specified. Use --input <path/to/file>")
        exit(1)

    # Check if file exists
    video_path = Path(args.input)
    if not video_path.is_file():
        print("The specified file does not exist.")
        exit(1)

    # Check if file is a video
    mimetype, _ = mimetypes.guess_type(args.input)
    if not mimetype or not mimetype.startswith('video'):
        print("The specified file is not a video.")
        exit(1)

    return args

def write_img_to_file(img, total_write):
    filename = "result/" + str(total_write).zfill(4) + ".jpg"
    cv2.imwrite(filename, img)
    return img

def write_to_file(array_imgs):
    count = 0
    for img in array_imgs:
        write_img_to_file(img, count)
        count += 1
    return array_imgs

########
# Main #
########
if __name__ == "__main__":
    args = parse_arguments()
    if args.input is None:
        print("No input file specified.")
        exit(1)
    video = args.input

    print("Getting start...")

    print("Cleanning folders")
    clean_folders()
    print("Getting screenshosts from " + video)
    height, width, all_frames = get_frames(video)
    # all_frames = get_frames(video)
    print("First compare and clean")
    first_imgs = analyze_image_similarity(all_frames, 0.75, 3)
    del all_frames
    gc.collect()
    print("Second compare and clean")
    second_imgs = analyze_image_similarity(first_imgs, 0.65, 2)
    del first_imgs
    gc.collect()
    print("Cleanning for unique screens")
    final_imgs = clean_unique(second_imgs, 0.84)
    del second_imgs
    no_duplicates = remove_duplicates(final_imgs)
    gc.collect()
    colors_img(no_duplicates, height, width)
    imgs_to_write = text_compute(final_imgs, height, width, args.disable_chatgpt)
    write_to_file(imgs_to_write)
    print("Perfect! Check folder: result/")