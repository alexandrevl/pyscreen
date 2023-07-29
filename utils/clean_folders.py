
import os

def clean_folders():
    # os.remove("result.json")
    path = "result/"
    if not os.path.exists(path):
        os.makedirs(path)
    files = sorted(os.listdir(path))
    for f in files:
        os.remove(path + f)
    return True