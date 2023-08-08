import pytesseract
import re
import unidecode


def get_word_sizes(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang="por+eng")    
    result = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 50:  # only consider words with confidence higher than 60%
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            # (x, y, w, h) = (data['par_num'][i], data['line_num'][i], data['word_num'][i], data['height'][i])
            word = remove_special_chars_and_accents(data['text'][i])
            if len(word) >= 3:
                result.append((word, x, y, w, h))  # appending word, width and height to the result list
    return result

def remove_special_chars_and_accents(string):
    # # Remove special characters
    string = re.sub(r'[^\w\s.,-/:]', '', string)

    # Remove accents
    string = unidecode.unidecode(string)
    string = string.lower()

    return string