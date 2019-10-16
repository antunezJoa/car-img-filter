from PIL import Image
from imageai.Detection import ObjectDetection
import os
import shutil
import time

image_file = "image.jpg"
path = "./download/"
route = path + "images/"

if not os.path.exists(route):
    os.makedirs(route)

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

custom_objects = detector.CustomObjects(car=True)
detections = detector.detectCustomObjectsFromImage(
                                                input_type="file",
                                                custom_objects=custom_objects,
                                                input_image=os.path.join(execution_path, "image.jpg"),
                                                output_image_path=os.path.join(route, "image.jpg"),
                                                minimum_percentage_probability=30,
                                                extract_detected_objects=False)

wh = []
subimage = []

for i in range(0, len(detections)):
    dots = detections[i]['box_points']
    coords = [dots[2]-dots[0], dots[3]-dots[1]]
    subimage += [[coords[0] * coords[1], dots]]
    wh += [coords[0] * coords[1]]

maximo = max(wh)

for x in range(0, len(subimage)):
    if maximo == subimage[x][0]:
        maximo = subimage[x][1]

img = Image.open(image_file)

im = img.crop((maximo[0], maximo[1], maximo[2], maximo[3]))

im.save(route + "image.jpg")
