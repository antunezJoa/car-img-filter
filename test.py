from PIL import Image
# from imageai.Detection import ObjectDetection
import os
import shutil
import time

path = "./download/"
c = 0

ws_folders = os.listdir(path)

for i in range(0, len(ws_folders)):
    b_folders = os.listdir(path + ws_folders[i])
    if 'item_links.json' in b_folders:
        b_folders.remove('item_links.json')
    if 'items.json' in b_folders:
        b_folders.remove('items.json')

    for y in range(0, len(b_folders)):
        id_folders = os.listdir(path + ws_folders[i] + '/' + b_folders[y])

        for z in range(0, len(id_folders)):
            jpg_files = os.listdir(path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z])
            jpg_files.remove('meta.json')

            for a in range(0, len(jpg_files)):
                print(path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a])
                time.sleep(1)
