import os
import glob
import json

brand_folders = os.listdir("./download/olx/")
count = 0

print("MAKING meta.json LIST...")
jsonlist = glob.glob("/home/laboratorio/Descargas/downloaders/download/olx/*/*/meta.json")

for json in jsonlist:
    print(json, "/", count + 1, "of", len(jsonlist))
    with open(json, 'r') as f:
        car_data = f.read()

    data = json.loads(car_data)

    if 'Marca / Modelo:' not in data:
        print("'Marca / Modelo:' NOT IN JSON")
        count += 1
        continue

    else:
        for brand in brand_folders:
            if brand in data['Marca / Modelo:'].lower():
                data['Marca:'] = brand.capitalize()
                data['Marca / Modelo:'] = data['Marca / Modelo:'][len(brand)+1:]

        data['Modelo:'] = data.pop('Marca / Modelo:')

        with open(json, 'w') as fp:
            json.dump(data, fp)

        print("saved new .json")
        count += 1
