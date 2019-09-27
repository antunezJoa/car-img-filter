from PIL import Image
from imageai.Detection import ObjectDetection
import os
import shutil

path = "./download/"

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

                execution_path = os.getcwd()

                detector = ObjectDetection()
                detector.setModelTypeAsRetinaNet()
                detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
                detector.loadModel()

                custom_objects = detector.CustomObjects(car=True)
                detections, objects_path = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path, path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a]), output_image_path=os.path.join(execution_path, jpg_files[a]), minimum_percentage_probability=30, extract_detected_objects=True)

                for eachObject, eachObjectPath in zip(detections, objects_path):
                    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ",
                          eachObject["box_points"])
                    print("Object's image saved in " + eachObjectPath)
                    print("--------------------------------")

                    image_file = "./download/" + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a]
                    img = Image.open(image_file)
                    width, height = img.size
                    image_o_size = width * height

                    data = []
                    percens = []
                    cont = 0
                    path = "/home/laboratorio/Descargas/downloaders/" + jpg_files[a] + "-objects/"

                    files = os.listdir(path)
                    q_files = len(files)

                    for i in range(1, q_files):
                        image_file = "./downloaders/" + jpg_files[a] + "-objects/car-" + str(i) + ".jpg"
                        img = Image.open(image_file)
                        width, height = img.size
                        data += [[(width * height * 100) / image_o_size, image_file]]
                        print(data)
                        percens += [data[cont][0]]
                        print(percens)
                        cont += 1

                    max_per = max(percens)

                    route = "./download/images"

                    if not os.path.exists(route):
                        os.makedirs(route)

                    for i in range(0, len(data)):
                        if data[i][0] == max_per:
                            os.rename(data[i][1], "./download/images/" + jpg_files[a])
                            #shutil.rmtree("./" + jpg_files[a] + "-objects/")
                            # how to delete only the new image
