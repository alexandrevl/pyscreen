import json
import math
import os
from collections import Counter
from re import findall

import cv2
import nltk
import pytesseract
import unidecode

from utils.chatgpt import chatgpt
from utils.word_sizes import get_word_sizes
from utils.wordcloud import wordcloud_write

nltk.download("stopwords", quiet=True)
stopwords = nltk.corpus.stopwords.words("portuguese")

def text_compute(final_imgs, height, width, disable_chatgpt):
    print("Processing text")
    all_text = ""
    words_sizes = []
    print("\r", end="")
    total_next = 0
    for img in final_imgs:
        text_from_img = image_to_string(img)
        result_array = get_word_sizes(img)
        if len(result_array) > 0:
            words_sizes.append(result_array)
        all_text += "\n" + text_from_img
        total_next += 1
        print("\r> screens scanned: " + str(total_next+1), end="")
    print("\r")
    result = frequency(all_text)
    result = json.dumps(result.most_common(200))
    # print(all_text)
    # result['all_text'] = all_text
    with open("result/all_text.txt", "w") as f:
        f.write(str(words_sizes))
    with open("result/words_count.json", "w") as f:
        f.write(str(result))
    if not disable_chatgpt:
        print("ChatGPT analysis started (this may take a while)")
        chatgpt_result = chatgpt(str(words_sizes))
        with open("result/chatgpt.txt", "w") as f:
            f.write(str(chatgpt_result))
    wordcloud_write(words_sizes, stopwords, height, width)
    return result


def frequency(string):
    palavras = findall(r"\w+", string)
    result = []
    for word in palavras:
        word = unidecode.unidecode(word.lower())
        if not word in stopwords and len(word) >= 3 and not word.isnumeric():
            result.append(word)
    counts = Counter(result)
    return counts


def image_to_string(img):
    height, width, channels = img.shape
    cropped_image = img[100:height, 0:width]
    img = cropped_image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, channels)
    text = pytesseract.image_to_string(gray, lang="por+eng")
    return text
