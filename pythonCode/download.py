# %%
import json
import requests
from sqlalchemy import true
from util import cadenaDeBien
import time
import dateutil.parser
import glob
import os
#-------------------CONFIG----------------------#
puertoAFiltrar = 42
tienePayload = True
descargarDatos = True
# None para parsear el último archivo, si quieres
# parsear uno en particular escribir path (no testeado)
# no tiene uso si descargarDatos = True
archivoAParsear = None
# None si quieres descargar de todos los devices
device = "andocirculando"
coordenadas = True
guardarDatosLimpios = True
guardarDatos = True
apiKey = 'input api key'
appName = 'input app name'
# -----------------------------------------
# Open file and read the contents

workingJson = None
path = os.getcwd()
if descargarDatos:
    enlaceBaseIdTipo = "https://eu1.cloud.thethings.network/api/v3/as/applications/{appName}/devices/{device_id}/packages/storage/{type}"
    enlaceTodos = 'https://eu1.cloud.thethings.network/api/v3/as/applications/{appName}/packages/storage/uplink_message'
    if device:
        enlaceTTN = enlaceBaseIdTipo.format(
            device_id=device, type="uplink_message")
        strDevice = device
    else:
        enlaceTTN = enlaceTodos
        strDevice = ""
    recivido = '[' + requests.get(enlaceTTN, headers={
        'Authorization': '{apiKey}'}).text.replace('\n', ',')[:-1] + ']'
    timestr = time.strftime("%Y-%m-%d_%H:%M")
    descargadoYenJson = json.loads(recivido)
    if guardarDatos:
        with open(timestr + strDevice + '.json', 'w') as f:
            f.write(json.dumps(descargadoYenJson))
    workingJson = descargadoYenJson
    if not workingJson:
        raise("""❌  No data on TTN servers, or not parseable ❌""")
if not descargarDatos:
    print("""
    ⚠️    Getting last local file...    ⚠️
        """)
    if not archivoAParsear:
        archivoAParsear = max(glob.glob(path + '/2022-0*.json'))
    with open(archivoAParsear) as f:
        workingJson = json.load(f)
    if not workingJson:
        raise("""No data on the local file""")


estan = cadenaDeBien(
    ['result', 'uplink_message', 'f_cnt'], filtrador=None)
gson = filter(estan, workingJson)
estan = cadenaDeBien(
    ['result', 'uplink_message', 'f_port'], filtrador=puertoAFiltrar)
gson = filter(estan, gson)
gson = [x['result'] for x in gson]

org = []
for elem in gson:
    try:
        tmp = {}
        try:
            tmp['powRet'] = (elem['uplink_message']
                             ['decoded_payload']['pow'])
        except:
            tmp['powRet'] = None
        tmp['f_port'] = (elem['uplink_message']['f_port'])
        tmp['f_cnt'] = (elem['uplink_message']['f_cnt'])
        tmp['rssi'] = (elem['uplink_message']['rx_metadata'][0]['rssi'])
        tmp['rssi_ch'] = (elem['uplink_message']
                          ['rx_metadata'][0]['channel_rssi'])
        tmp['snr'] = (elem['uplink_message']['rx_metadata'][0]['snr'])
        tmp['bw'] = (elem['uplink_message']['settings']
                     ['data_rate']['lora']['bandwidth'])
        tmp['SF'] = (elem['uplink_message']['settings']
                     ['data_rate']['lora']['spreading_factor'])
        tmp['f(MHz)'] = int(elem['uplink_message']
                            ['settings']['frequency'])/1000000
        tmp['time'] = dateutil.parser.parse(
            elem['uplink_message']['received_at'])
        if coordenadas:
            tmp['lat'] = (elem['uplink_message']['decoded_payload']['lat'])
            tmp['lng'] = (elem['uplink_message']['decoded_payload']['lng'])
        org.append(tmp)
    except:
        pass
if guardarDatosLimpios:
    with open(timestr + strDevice + "limpio" + '.json', 'w') as f:
        tmp = []
        for item in org:
            tras = item
            tras['time'] = tras['time'].isoformat()
            tmp.append(item)
        f.write(json.dumps(tmp))
# %%
