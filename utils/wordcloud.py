import re
from collections import Counter
from re import findall

import unidecode
from wordcloud import WordCloud

def wordcloud_write_frequency(all_text):
    print("Creating wordcloud")
    wordcloudText = ""
    palavras = findall(r"\w+", all_text)
    for word in palavras:
        word = unidecode.unidecode(word.lower())
        if len(word) >= 3 and not word.isnumeric():
            wordcloudText += word + " "
    wordcloud = WordCloud(width=width, height=height, stopwords=stopwords).generate(
        wordcloudText
    )
    wordcloud.to_file("result/wordcloud.png")

def wordcloud_write_all(arrays):
    print("Creating wordcloud")
    wordcloudDict = {}
    for array in arrays:
        for tup in array:
            word, x, y, size = tup
            word = unidecode.unidecode(word.lower())
            if len(word) >= 3 and not word.isnumeric():
                if word in wordcloudDict:
                    wordcloudDict[word] += size
                else:
                    wordcloudDict[word] = size
    wordcloud = WordCloud(width=width, height=height, stopwords=stopwords).generate_from_frequencies(wordcloudDict)
    wordcloud.to_file("result/wordcloud.png")

def wordcloud_write(words_size, stopwords, height, width):
    print("Creating wordcloud")
    wordcloudDict = {}
    for array in words_size:
        for tup in array:
            word, x, y, size = tup
            word = unidecode.unidecode(word.lower())
            # Remove all non-alphabetic characters
            word = re.sub(r'[^a-z]', '', word)
            # Check if the cleaned word is not empty and its length is greater than or equal to 3
            if word and len(word) >= 3:
                if word in wordcloudDict:
                    wordcloudDict[word] += size
                else:
                    wordcloudDict[word] = size
    wordcloud = WordCloud(width=width, height=height, stopwords=stopwords).generate_from_frequencies(wordcloudDict)
    wordcloud.to_file("result/wordcloud.png")