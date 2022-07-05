import json
import csv

with open('datosGPS28-06.json') as json_file:
    jsondata = json.load(json_file)

data_file = open('datosGPS28-06.csv', 'w', newline='')
csv_writer = csv.writer(data_file)

count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    if data['lat'] == 0:
        continue
    csv_writer.writerow(data.values())

data_file.close()
