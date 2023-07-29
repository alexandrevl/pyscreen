import cv2
import numpy as np
from collections import Counter
import pandas as pd
import random
import csv

from utils.colors_score import analyse_colors

base_colors = pd.read_csv("utils/colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

def colors_img(all_imgs, height, width):
    size = 5
    print("Scanning colors")
    print("\r", end="")
    result = Counter()
    i = 0
    for img in all_imgs:
        i += 1
        print("\r> screens scanned: " + str(i), end="")
        colors_arr = colors_output(img, height, width)
        result.update(colors_arr)
    print("")
    most_common = result.most_common(50)
    final_imgs = Counter()

    for mc in most_common:
        color = tuple(mc[0])
        qnt = mc[1]
        b, g, r = color
        cid, cname, hex = getColorName(r, g, b)
        final_imgs.update({f"{hex}": qnt})
    i = 1
    h_rect = int(height // size)
    final = final_imgs.most_common(size)
    to_harmony = []
    first_three = final_imgs.most_common(3)
    for cl in first_three:
        hex = cl[0]
        to_harmony.append(hex_to_rgb(hex))
    harmony_score, analogous_score, complementary_score, split_complementary_score, triadic_score, monochromatic_score = analyse_colors(to_harmony[0], to_harmony[1], to_harmony[2])
    sum = 0
    for cl in final:
        sum += cl[1]
    img = np.zeros((height, width, 3), dtype=np.uint8)
    rect_height = 25
    cv2.rectangle(img, (0, 0), (width, rect_height), (192, 192, 192), -1)
    # text = "harmony score: " + str(round(harmony_score, 2)) + "%"
    text = "harmony: " + str(round(harmony_score)) + ", analogous: " + str(round(analogous_score)) + ", complementary: " + str(round(complementary_score)) + ", split complementary: " + str(round(split_complementary_score)) + ", triadic: " + str(round(triadic_score)) + ", monochromatic: " + str(round(monochromatic_score))
    
    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 0.4
    thickness = 1
    color = (0, 0, 0)
    text_size, _ = cv2.getTextSize(text, font, fontScale, thickness)
    text_x = (width - text_size[0]) // 2
    text_y = 15
    org = (text_x, text_y)
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False)
    i = rect_height
    for cl in final:
        hex = cl[0]
        qnt = cl[1]
        color_array = getColorHex(hex)
        rect_height = int(qnt / sum * height)
        cv2.rectangle(img, (0, i), (width, i + rect_height), color_array[0], -1)
        text = color_array[2].lower() + " " + hex + " " + str(round(qnt / sum * 100, 2)) + "%"
        font = cv2.FONT_HERSHEY_DUPLEX
        org = (8, i + rect_height - 15)
        fontScale = 0.7
        color = (0, 0, 0)
        thickness = 2
        img = cv2.putText(
            img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )
        color = (255, 255, 255)
        thickness = 1
        img = cv2.putText(
            img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )
        i += rect_height
    cv2.imwrite("result/colors.jpg", img)
    cv2.destroyAllWindows()

def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    hlen = len(hex)
    return tuple(int(hex[i : i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


def getColorName(R, G, B):
    minimum = 10000
    cname = 0
    hex = 0
    for i in range(len(base_colors)):
        d = (
            abs(R - int(base_colors.loc[i, "R"]))
            + abs(G - int(base_colors.loc[i, "G"]))
            + abs(B - int(base_colors.loc[i, "B"]))
        )
        if d <= minimum:
            minimum = d
            cid = base_colors.loc[i, "color"]
            cname = base_colors.loc[i, "color_name"]
            hex = base_colors.loc[i, "hex"]
    
    return [cid, cname, hex]

def getColorHex(hex_param):
    for i in range(len(base_colors)):
        hex = base_colors.loc[i, "hex"]
        cid = base_colors.loc[i, "color"]
        cname = base_colors.loc[i, "color_name"]
        if hex == hex_param:
            return [(int(base_colors.loc[i, "B"]), int(base_colors.loc[i, "G"]), int(base_colors.loc[i, "R"])),cid,cname]     
    return []

def colors_output(img, height, width):
    result = []
    x = 0
    while x < height:
        y = 0
        while y < width:
            b, g, r = img[x, y]
            color = (b, g, r)
            result.append(color)
            y += random.randint(2, 4)
        x += random.randint(2, 5)
    counts = Counter(result)
    return counts