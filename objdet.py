from PIL import Image
from imageai.Detection import ObjectDetection
import os
import shutil

path = "./download/"
c = 0

ws_folders = os.listdir(path)

for i in range(1, len(ws_folders)):
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
                print(path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a])  # ruta de los archivos .jpg

                execution_path = os.getcwd()

                detector = ObjectDetection()
                detector.setModelTypeAsRetinaNet()
                detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
                detector.loadModel()

                custom_objects = detector.CustomObjects(car=True)
                detections, objects_path = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path, path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a]), output_image_path=os.path.join(execution_path, 'x' + jpg_files[a]), minimum_percentage_probability=30, extract_detected_objects=True)

                for eachObject, eachObjectPath in zip(detections, objects_path):
                    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ",
                          eachObject["box_points"])
                    print("Object's image saved in " + eachObjectPath)
                    print("--------------------------------")
                    c += 1

                if c > 0:  # se detectaron autos en la imagen
                    image_file = "./download/" + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a]
                    img = Image.open(image_file)
                    width, height = img.size
                    image_o_size = width * height  # cantidad de pixeles de la imagen original a comparar

                    data = []
                    percens = []
                    cont = 0
                    path2 = "./" + 'x' + jpg_files[a] + "-objects/"

                    files = os.listdir(path2)
                    q_files = len(files)

                    for j in range(0, q_files):
                        s_image_file = "./" + 'x' + jpg_files[a] + "-objects/car-" + str(j + 1) + ".jpg"
                        img = Image.open(s_image_file)
                        width, height = img.size
                        data += [[(width * height * 100) / image_o_size, s_image_file]]  # guardo en un array el % sobre la cantidad total de pixeles y la ruta de dicha imagen
                        percens += [data[cont][0]]
                        cont += 1

                    max_per = max(percens)  # elijo el porcentaje mayor, su imagen asociada sera el auto principal de la imagen

                    route = "./download/images"

                    if not os.path.exists(route):
                        os.makedirs(route)

                    for x in range(0, len(data)):
                        if data[x][0] == max_per:
                            os.rename(data[i][1], "./download/images/" + jpg_files[a])  # muevo dicha imagen asociada a una carpeta
                            shutil.rmtree("./" + "x" + jpg_files[a] + "-objects/")  # remuevo el directorio con los autos detectados de la imagen original
                            os.remove('./' + 'x' + jpg_files[a])  # remuevo la imagen que se creo en la deteccion de objetos
                else:  # no se detectaron autos en la imagen
                    continue
