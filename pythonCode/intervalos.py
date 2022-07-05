import dateutil.parser
import os
import json

#------------CONFIG-----------------#
file = "2022-06-28_13:55eui-70b3d57ed004e320limpio.json"
inicio = dateutil.parser.parse("2022-06-24T13:26:17.431384+00:00")
fin = dateutil.parser.parse("2022-06-24T13:49:17.431384+00:00")
saveOn = 'portiempo'+file

# -----------------------------
path = os.getcwd() + '/'
path = path + file
with open(path) as f:
    workingJson = json.load(f)
if not workingJson:
    raise("""No data on local file""")


def changeDate(dict):
    dict['time'] = dateutil.parser.parse(dict['time'])
    return dict


workingJson = map(changeDate, workingJson)
workingJson = sorted(
    workingJson, key=lambda x: x['time'])

indexInicio = None
indexFinal = None
a = 0
for i in workingJson:
    if i['time'] > inicio:
        indexInicio = a
        break
    a += 1

a = 0
for i in workingJson:
    if i['time'] > fin:
        indexFinal = a
        break
    a += 1


def changeBackDate(dic):
    dic['time'] = dic['time'].isoformat()
    return dic


workingJson = list(map(changeBackDate, workingJson))

with open(saveOn, 'w') as f:
    json.dump(workingJson[indexInicio:indexFinal], f)
