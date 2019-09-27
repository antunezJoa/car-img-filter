from PIL import Image
from imageai.Detection import ObjectDetection
import os
import shutil

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

custom_objects = detector.CustomObjects(car=True)
detections, objects_path = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path, "image.jpg"), output_image_path=os.path.join(execution_path, "imagenew.jpg"), minimum_percentage_probability=30,  extract_detected_objects=True)

for eachObject, eachObjectPath in zip(detections, objects_path):
    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
    print("Object's image saved in " + eachObjectPath)
    print("--------------------------------")

path = "./imagenew.jpg-objects/"

image_file = "image.jpg"
img = Image.open(image_file)
width, height = img.size
image_o_size = width * height

data = []
percens = []
cont = 0

for i in range(1, len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]) + 1):
    image_file = "./imagenew.jpg-objects/car-" + str(i) + ".jpg"
    img = Image.open(image_file)
    width, height = img.size
    data += [[(width * height * 100) / image_o_size, image_file]]
    percens += [data[cont][0]]
    cont += 1

max_per = max(percens)

route = "./download/images"

if not os.path.exists(route):
    os.makedirs(route)

for i in range(0, len(data)):
    if data[i][0] == max_per:
        os.rename(data[i][1], "./download/images/image.jpg")
        shutil.rmtree("./imagenew.jpg-objects/")
        os.remove("imagenew.jpg")
