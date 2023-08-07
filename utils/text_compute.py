import json
import math
import os
import re
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

def text_compute(array_imgs, height, width, disable_chatgpt):
    print("Processing text")
    all_text = ""
    words_sizes = []
    result_imgs = []
    print("\r", end="")
    total_next = 0
    for img in array_imgs:
        text_from_img = image_to_string(img)
        result_array = get_word_sizes(img)
        blur_ind, blurred_img = blur_specific_words(img, result_array)
        if blur_ind:
            result_imgs.append(blurred_img)
        else:
            result_imgs.append(img)
        if len(result_array) > 0:
            words_sizes.append(result_array)
        all_text += "\n" + text_from_img
        print("\r> screens scanned: " + str(total_next+1), end="")
        total_next += 1
    print("\r")
    result = frequency(all_text)
    result = json.dumps(result.most_common(200))

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
    return result_imgs


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


def load_words_from_file(filename):
    """
    Load regular expressions from a file into a list.

    Parameters:
    - filename: Name of the file to read from.

    Returns:
    - regex_patterns: List of compiled regular expressions.
    """
    regex_patterns = []
    with open(filename, 'r') as f:
        for line in f:
            pattern = line.strip()
            if pattern:  # ensure the pattern is not empty
                regex_patterns.append(re.compile(pattern, re.IGNORECASE))  # compile the pattern for better performance
    return regex_patterns

def blur_specific_words(img, result_array):
    """
    Blurs specific words in the image based on regex patterns from a file.

    Parameters:
    - img: The image on which to apply blur
    - result_array: An array containing word details in the format (word, x, y, w, h)
    - blur_size: The size of the blur, default is (51, 51)

    Returns:
    - img: Image with specific words blurred
    """
    BLUR_CONSTANT = 1.82
    blur_ind = False
    # Load regex patterns from the file
    regex_patterns = load_words_from_file("utils/words_to_blur.txt")

    for index, word_details in enumerate(result_array):
        (word, x, y, w, h) = word_details
        if any(pattern.match(word) for pattern in regex_patterns):
            # print(word_details)
            blur_number = int(BLUR_CONSTANT * h)
            if (blur_number % 2 == 0):
                blur_number += 1
            blur_size = (blur_number, blur_number)
            img = apply_local_blur(img, (x, y), (w, h), blur_size)
            blur_ind = True

    return blur_ind, img

def apply_local_blur(img, top_left, size, blur_intensity=(15, 15)):
    """
    Apply local blur to a specific region of an image.

    Parameters:
    - img: Input image
    - top_left: (x, y) tuple specifying the top left corner of the region to blur
    - size: (width, height) tuple specifying the size of the region to blur
    - blur_intensity: (optional) tuple specifying the intensity of blur in x and y directions. Default is (15, 15).

    Returns:
    - Blurred image
    """

    # Clone the original image
    blurred_img = img.copy()

    # Extract region to blur
    x, y = top_left
    w, h = size
    x -= 5
    y -= 5
    w += 10
    h += 10
    region_to_blur = img[y:y+h, x:x+w]

    # Apply Gaussian blur to the region
    blurred_region = cv2.GaussianBlur(region_to_blur, blur_intensity, 0)

    # Replace the region in the original image with blurred region
    blurred_img[y:y+h, x:x+w] = blurred_region

    return blurred_img
