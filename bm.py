import os
import glob
import json

brand_folders = os.listdir("./download/olx/")

print("MAKING LIST...")
jsonlist = glob.glob("/home/laboratorio/Descargas/downloaders/download/olx/*/*/meta.json")

for x in jsonlist:
    print(x)
    with open(x, 'r') as f:
        car_data = f.read()

    data = json.loads(car_data)

    if 'Marca / Modelo:' not in data:
        print("'Marca / Modelo:' not in json")
        continue

    else:
        for i in brand_folders:
            if i in data['Marca / Modelo:'].lower():
                data['Marca:'] = i.capitalize()
                data['Marca / Modelo:'] = data['Marca / Modelo:'][len(i)+1:]

        data['Modelo:'] = data.pop('Marca / Modelo:')

        with open(x, 'w') as fp:
            json.dump(data, fp)

        print("saved new .json")