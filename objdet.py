from PIL import Image
from imageai.Detection import ObjectDetection
import os
import glob
import json

route = "./images/"  # en esta carpeta se guardaran las imagenes filtradas y sus respectivos .json
if not os.path.exists(route):
    os.makedirs(route)

path = './download/'

ws_folders = os.listdir(path)  # listado de las carpetas dentro de /download

big_list = []

print("Making list...")  # lista con las rutas de todas las imagenes (archivos .jpg)
# de la carpeta de las subcarpetas de download/

for ws in ws_folders:
    print(ws)

    b_folders = os.listdir(path + str(ws))
    if 'item_links.json' in b_folders:
        b_folders.remove('item_links.json')
    if 'items.json' in b_folders:
        b_folders.remove('items.json')
    if 'info.json' in b_folders:
        b_folders.remove('info.json')

    cont = 0

    for b in b_folders:
        print(ws, "/", b, "/", cont + 1, "of", len(b_folders))
        big_list += glob.glob("/home/laboratorio/Descargas/downloaders/download/" + ws + "/" + b + "/*/*.jpg")
        cont += 1

for z in range(0, len(big_list)):
    big_list[z] = str(big_list[z]).replace("/home/laboratorio/Descargas/downloaders/", '')  # reemplazo esta ruta
    # porque ya se predefinio en la librera de imageAI

for i in range(0, len(big_list)):
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()

    print("Analazing", big_list[i], "/ image", (i + 1), "of", len(big_list))
    if 'ml' in big_list[i]:
        website = 'ml'
    elif 'olx' in big_list[i]:
        website = 'olx'
    elif 'demotores' in big_list[i]:
        website = 'demotores'
    elif 'rosariogarage' in big_list[i]:
        website = 'rosariogarage'
    else:
        website = 'unknown'

    custom_objects = detector.CustomObjects(car=True)
    detections = detector.detectCustomObjectsFromImage(
        input_type="file",
        custom_objects=custom_objects,
        input_image=os.path.join(execution_path, big_list[i]),
        output_image_path=os.path.join(route, "car" + str(i + 1) + ".jpg"),
        output_type="file",
        minimum_percentage_probability=90,
        extract_detected_objects=False)

    if len(detections) == 0:  # no detecto autos
        os.remove(route + "car" + str(i + 1) + ".jpg")  # que borre la foto y continue
        print("No cars detected")
        continue

    else:  # si detecto autos
        wh = []
        subimage = []
        data = {}

        for y in range(0, len(detections)):
            dots = detections[y]['box_points']
            coords = [dots[2] - dots[0], dots[3] - dots[1]]
            subimage += [[coords[0] * coords[1], dots]]
            wh += [coords[0] * coords[1]]

        maximo = max(wh)

        for x in range(0, len(subimage)):
            if maximo == subimage[x][0]:
                maximo = subimage[x][1]

        img = Image.open(route + "car" + str(i + 1) + ".jpg")

        im = img.crop((maximo[0], maximo[1], maximo[2], maximo[3]))

        im.save(route + "car" + str(i + 1) + ".jpg")

        print("Car image saved")

        # creo archivo .json

        data['website'] = website

        with open(route + "car" + str(i + 1) + '.json', 'w') as fp:
            json.dump(data, fp)

        print("Created .json")
