from imageai.Detection import ObjectDetection
import os
import glob
import json
import shutil


def makelist():
    route = "./detections/images/"  # en esta carpeta se guardaran las imagenes filtradas y sus respectivos .json
    if not os.path.exists(route):
        os.makedirs(route)

    ws_folders = os.listdir('./download/')  # listado de las carpetas dentro de /download

    big_list = []
    jpglist = {}
    y = 0

    for ws in ws_folders:
        print("MAKING THE", ws.upper(), "PHOTO LIST...")

        b_folders = os.listdir('./download/' + str(ws))
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
        big_list[z] = big_list[z].replace("/home/laboratorio/Descargas/downloaders/", '')  # reemplazo esta
        # ruta porque ya se predefine en la librera de imageAI al estar el archivo dentro de /downloaders
        jpglist['jpg' + str(y)] = big_list[z]
        with open('./detections/jpglist.json', "w") as file:
            json.dump(jpglist, file)
        print("Saved", jpglist['jpg' + str(y)], "images saved:", y)
        y += 1

    jpglist['images_number'] = y
    with open('./detections/images.json', "w") as file:
        json.dump(jpglist, file)

    print("Images saved")


def car_detections():
    images = {}

    with open('./detections/jpglist.json', 'r') as f:
        jpgs = f.read()

    paths = json.loads(jpgs)

    imgdet = 0  # downloads es el contador que indica en cual link arranca la descarga de imagenes

    images_number = 300000  # aca va el numero de links guardados en el json

    for imgdet in range(imgdet, images_number):
        #  en caso de no poder ver el error en consola y ver en que imagen te quedaste
        #  creo un archivo que va guardando el ultimo estado de imgdet, o sea la ultima imagen que analicé

        images['images'] = imgdet
        with open('./detections/info.json', "w") as file:
            json.dump(images, file)

        realimage = paths['jpg' + str(imgdet)]  # realimage es la imagen original la cual hay que analizar

        execution_path = os.getcwd()

        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()

        print("Analazing", realimage, "/ image", imgdet + 1, "of", images_number)

        # defino de que sitio web proviene para luego colocarlo en el json
        if 'ml' in realimage:
            website = 'ml'
        elif 'olx' in realimage:
            website = 'olx'
        elif 'demotores' in realimage:
            website = 'demotores'
        elif 'rosariogarage' in realimage:
            website = 'rosariogarage'
        else:
            website = 'unknown'

        custom_objects = detector.CustomObjects(car=True)
        detections = detector.detectCustomObjectsFromImage(
            input_type="file",
            custom_objects=custom_objects,
            input_image=os.path.join(execution_path, realimage),
            output_image_path=os.path.join("./detections/images/car" + str(imgdet + 1) + ".jpg"),
            output_type="file",
            minimum_percentage_probability=90,
            extract_detected_objects=False)

        if len(detections) == 0:  # no detecto autos
            os.remove("./detections/images/car" + str(imgdet + 1) + ".jpg")  # que borre la foto y continue
            print("No cars detected")
            continue

        else:  # si detecto autos

            # a continuacion el proceso para obtener el auto de mayor relevancia

            wh = []
            sub_image = []

            for y in range(0, len(detections)):
                dots = detections[y]['box_points']
                coords = [dots[2] - dots[0], dots[3] - dots[1]]
                sub_image += [[coords[0] * coords[1], dots]]
                wh += [coords[0] * coords[1]]

            maximo = max(wh)

            for x in range(0, len(sub_image)):
                if maximo == sub_image[x][0]:
                    maximo = sub_image[x][1]

            os.remove("./detections/images/car" + str(imgdet + 1) + ".jpg")  # remuevo la imagen con las detecciones
            print("Image removed")
            shutil.copy(realimage, "./detections/images/car" + str(imgdet + 1) + ".jpg")  # copio la imagen original
            print("Original image saved")

            # JSON:
            # traigo los datos del auto que estan en el .json en la carpeta original para tambien guardarlos en el
            # nuevo json

            realjson = os.path.dirname(os.path.abspath(realimage)) + "/meta.json"  # obtengo el meta.json que esta en
            # en el mismo path que la imagen que estoy analizando

            with open(realjson, 'r') as f:
                car_data = f.read()

            data = json.loads(car_data)

            # agrego un par de datos mas al .json

            data['Web Site'] = website  # guardo sitio web de donde proviene la imagen
            data['boxpoints'] = maximo  # guardo los 4 puntos que forman el cuadrilatero donde se encuentra
            # el auto principal de la imagen en cuestion

            # guardo el .json

            with open("./detections/images/car" + str(imgdet + 1) + ".json", 'w') as fp:
                json.dump(data, fp)

            print("Created .json")

    print("End")


jpg_list = './detections/jpglist.json'  # si no existe la lista de las fotos la creo, sino arranco con las detecciones
# pues la lista de fotos ya existe

if not os.path.exists(jpg_list):
    makelist()
else:
    car_detections()
