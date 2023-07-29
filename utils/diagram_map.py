import cv2
import numpy as np
from collections import Counter
import pandas as pd
import random
import csv


def result_map(all_imgs):
    nodes = []
    edges = []
    stack = []
    for i, img in enumerate(all_imgs):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if (i > 1):
            y = len(stack)-1
            while y > 0:
                b_img_gray = cv2.cvtColor(stack[y], cv2.COLOR_BGR2GRAY)
                res = cv2.absdiff(img_gray, b_img_gray)
                res = res.astype(np.uint8)
                percentage = 1 - (np.count_nonzero(res) / res.size)
                if percentage > 0.85:
                    temp = stack[y,len(stack)-1]
                    print(i,y)
                y -= 1
        stack.append(img)
    return ""
            
    
def result_map_old2(all_imgs):
    nodes = []
    edges = []
    back_connect = 0
    for i, img in enumerate(all_imgs):
        if i > 0:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if back_connect == 0:
                for i2, img_index in enumerate(nodes):
                    back_img_gray = cv2.cvtColor(
                        all_imgs[int(img_index)], cv2.COLOR_BGR2GRAY
                    )
                    res = cv2.absdiff(img_gray, back_img_gray)
                    res = res.astype(np.uint8)
                    percentage = 1 - (np.count_nonzero(res) / res.size)
                    if percentage > 0.8:
                        # print(i, img_index, percentage, str(i + 1).zfill(4))
                        # nodes.append(str(i).zfill(4))
                        if (i + 1) < len(all_imgs):
                            edge = {
                                "data": {
                                    "source": str(img_index).zfill(4),
                                    "target": str(i + 1).zfill(4),
                                }
                            }
                            i += 1
                            edges.append(edge)
                            # print(edge, i)
                        back_connect = 1
                        break
                else:
                    if back_connect == 0:
                        nodes.append(str(i).zfill(4))
                        edge = {
                            "data": {
                                "source": str(i - 1).zfill(4),
                                "target": str(i).zfill(4),
                            }
                        }
                        edges.append(edge)
            else:
                nodes.append(str(i).zfill(4))
                back_connect = 0
        else:
            nodes.append(str(i).zfill(4))
    result = {"nodes": nodes, "edges": edges}
    result = "result_map=" + str(result)
    # print(result)
    with open("diagram/result_map.js", "w") as f:
        f.write(result)
    return result


def result_map_old(all_imgs):
    nodes = []
    edges = []
    source_back = -1
    for index, img in enumerate(all_imgs):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if index > 0:
            is_fw = -1
            for index_back in range(index):
                back_img_gray = cv2.cvtColor(all_imgs[index_back], cv2.COLOR_BGR2GRAY)
                res = cv2.absdiff(img_gray, back_img_gray)
                res = res.astype(np.uint8)
                percentage = 1 - (np.count_nonzero(res) / res.size)
                if percentage > 0.9:
                    is_fw = index_back
                    source_back = index_back
                    break
            if is_fw == -1:
                source = index - 1
                if source_back > -1:
                    source = source_back
                    source_back = -1
                nodes.append(str(index).zfill(4))
                if str(source).zfill(4) in nodes:
                    edges.append(
                        {
                            "data": {
                                "source": str(source).zfill(4),
                                "target": str(index).zfill(4),
                            }
                        }
                    )

        else:
            nodes.append(str(index).zfill(4))
    # edges.append({"data": {"source": "0000", "target": "0001"}})
    result = {"nodes": nodes, "edges": edges}
    result = "result_map=" + str(result)
    # print(result)
    with open("diagram/result_map.js", "w") as f:
        f.write(result)
    return result
    