import cv2
import numpy as np
import math


def get_frames(inputFile):
    global height, width, channels
    rate = 4
    cam = cv2.VideoCapture(inputFile)
    total_frames = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Frames in video: " + str(round(total_frames)))
    print("Frames to capture: " + str(math.floor(total_frames // rate)))
    total_frames_captured = 0
    all_frames = []
    to_rec = 0
    print("\r", end="")
    while True:
        ret, frame = cam.read()
        if ret:
            if to_rec == rate - 1:
                total_frames_captured += 1
                print("\r> screens captured: " + str(total_frames_captured), end="")
                height, width, channels = frame.shape
                all_frames.append(frame)
                to_rec = 0
            else:
                to_rec += 1
        if ret == False:
            break
    cam.release()
    cv2.destroyAllWindows()
    print("")
    return (height, width, all_frames)


def clean_unique(imgs, rate_index):
    print("\r", end="")
    total_write = 0
    result_imgs = []
    for index, img in enumerate(imgs):
        if index > 0:
            res = cv2.absdiff(
                cv2.cvtColor(imgs[index][100:height, 0:width], cv2.COLOR_BGR2GRAY),
                cv2.cvtColor(imgs[index - 1][100:height, 0:width], cv2.COLOR_BGR2GRAY),
            )
            res = res.astype(np.uint8)
            percentage = 1 - (np.count_nonzero(res) / res.size)
            if percentage <= rate_index:
                cv2.imwrite(
                    "result/" + str(total_write).zfill(4) + ".jpg", imgs[index - 1]
                )
                result_imgs.append(imgs[index - 1])
                total_write += 1
                print("\r> screens promoted: " + str(total_write), end="")
    cv2.imwrite("result/" + str(total_write).zfill(4) + ".jpg", imgs[len(imgs) - 1])
    result_imgs.append(imgs[len(imgs) - 1])
    print("\r> screens promoted: " + str(total_write+1), end="")
    print("")
    return result_imgs


def compare_files(imgs, rate_index, depth):
    range_limits = depth
    range_min = range_limits * (-1)
    range_max = range_limits + 1
    result_imgs = []
    total_next = 0
    print("\r", end="")
    for index, img in enumerate(imgs):
        total = 0
        for y in range(range_min, range_max):
            if index >= range_limits and index <= len(imgs) + range_min - 1 and y != 0:
                res = cv2.absdiff(
                    cv2.cvtColor(imgs[index][100:height, 0:width], cv2.COLOR_BGR2GRAY),
                    cv2.cvtColor(
                        imgs[index + y][100:height, 0:width], cv2.COLOR_BGR2GRAY
                    ),
                )
                res = res.astype(np.uint8)
                percentage = 1 - (np.count_nonzero(res) / res.size)
                total += percentage
        rate = total / 6
        if rate > rate_index:
            total_next += 1
            result_imgs.append(imgs[index])
            print("\r> screens promoted: " + str(total_next), end="")
    print("")
    return result_imgs

def remove_duplicates(all_imgs):
    result = all_imgs.copy()
    for index, img in enumerate(all_imgs):
        if (index + 1) < (len(result) - 1):
            for y in range(index + 1, (len(result) - 1)):
                if y <= (len(result) - 1):
                    res = cv2.absdiff(
                        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                        cv2.cvtColor(result[y], cv2.COLOR_BGR2GRAY),
                    )
                    res = res.astype(np.uint8)
                    percentage = 1 - (np.count_nonzero(res) / res.size)
                    if percentage > 0.95:
                        result.pop(y)
    return result