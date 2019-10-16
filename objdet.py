from PIL import Image
from imageai.Detection import ObjectDetection
import os

path = "./download/"
route = "./images/"

if not os.path.exists(route):
    os.makedirs(route)

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
                print(path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a])  # ruta de los archivos .jpg

                image_file = path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a]

                execution_path = os.getcwd()

                detector = ObjectDetection()
                detector.setModelTypeAsRetinaNet()
                detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
                detector.loadModel()

                custom_objects = detector.CustomObjects(car=True)
                detections = detector.detectCustomObjectsFromImage(
                                                                input_type="file",
                                                                custom_objects=custom_objects,
                                                                input_image=os.path.join(execution_path, path + ws_folders[i] + '/' + b_folders[y] + '/' + id_folders[z] + '/' + jpg_files[a]),
                                                                output_image_path=os.path.join(route, jpg_files[a]),
                                                                minimum_percentage_probability=30,
                                                                extract_detected_objects=False)

                wh = []
                subimage = []

                for i in range(0, len(detections)):
                    dots = detections[i]['box_points']
                    coords = [dots[2] - dots[0], dots[3] - dots[1]]
                    subimage += [[coords[0] * coords[1], dots]]
                    wh += [coords[0] * coords[1]]

                maximo = max(wh)

                for x in range(0, len(subimage)):
                    if maximo == subimage[x][0]:
                        maximo = subimage[x][1]

                img = Image.open(image_file)

                im = img.crop((maximo[0], maximo[1], maximo[2], maximo[3]))

                im.save(route + jpg_files[a])

"""
                if c > 0:  # se detectaron autos (mas de 0) en la imagen
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

                    route = "./download/images/"

                    if not os.path.exists(route):
                        os.makedirs(route)

                    for x in range(0, len(data)):
                        if data[x][0] == max_per:
                            os.rename(data[x][1], route + jpg_files[a])  # muevo dicha imagen asociada a una carpeta
                            #shutil.rmtree("./" + "x" + jpg_files[a] + "-objects/")  # remuevo el directorio con los autos detectados de la imagen original
                            #os.remove('./' + 'x' + jpg_files[a])  # remuevo la imagen que se creo en la deteccion de objetos
                else:  # no se detectaron autos en la imagen
                    continue
"""

#  todo a la misma carpeta, archivo y json correpsondiente
#  json de donde viene la imagen (olx o ml)
#  porcentaje minimo
#  50% del ancho original
#  50% del alto origninal
