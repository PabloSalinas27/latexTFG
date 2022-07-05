import time
import dateutil.parser
import glob
import os
import json
import bisect
archivo="plot\e1ADR.json"
inicio='2022-06-22T16:51:25'
fin="2022-06-22T17:50:00"
salida="plot\e1finalfinal.json"
intervalo=[]
with open(archivo,'r') as f:
    workingJson = json.load(f)

for i in range(len(workingJson)):
    if (workingJson[i]['time']>inicio and workingJson[i]['time']<fin):
        intervalo.append(workingJson[i])

with open(salida,'w') as f:
    f.write(json.dumps(intervalo))