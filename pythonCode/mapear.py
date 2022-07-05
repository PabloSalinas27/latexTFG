from itertools import chain, cycle
import json
from math import log
import pandas as pd
import folium

dfa = pd.read_csv('datosGPS28-06.csv')
# change to your column names, assume the columns are sorted by time
df = dfa[['lat', 'lng']]
points = [tuple(x) for x in df.to_numpy()]

ave_lat = sum(p[0] for p in points)/len(points)
ave_lon = sum(p[1] for p in points)/len(points)

# Load map centred on average coordinates
my_map = folium.Map(location=[ave_lat, ave_lon],
                    zoom_start=17, tiles='CartoDB positron')


with open('datosGPS28-06.json') as f:
    jsondata = json.load(f)
    points = [(x['lat'], x['lng']) for x in jsondata]
ciclo = cycle([(3, 7), (3, 10), (3, 12),
               (10, 7), (10, 10), (10, 12),
               (17, 7), (17, 10), (17, 12), ])
losses = []
last = jsondata[0]
while next(ciclo) != (last['powRet'], last['SF']):
    pass
ciclo = chain([(last['powRet'], last['SF'])], ciclo)

folium.Marker(
    (44.412484774046746, 8.929275010050338),
    popup="Gateway" + str((44.412484774046746, 8.929275010050338)),
    icon=folium.Icon(icon="cloud-upload",
                     icon_color="blue", prefix='fa')

).add_to(my_map)


# separation line for vicoli and port

folium.PolyLine(((44.437052504672884, 8.91), (44.40847929595013, 8.93)),
                popup="Separation line ",
                weight=12,
                color="black",
                opacity=1).add_to(my_map)


# add a markers
racha = 0
for i in range(2, len(points)):
    # packetsLost = dfa['f_cnt'][i-1] - dfa['f_cnt'][i]
    packetsLost = jsondata[i-1]['f_cnt'] - jsondata[i]['f_cnt']
    interLoss = 0
    racha += 1
    while next(ciclo) != (jsondata[i]['powRet'], jsondata[i]['SF']):
        interLoss += 1
        racha = 0

    if packetsLost > 9:
        interLoss += 9

    if jsondata[i]['lat'] == 0 or jsondata[i-1]['lat'] == 0 or packetsLost > 200:
        continue
    folium.Marker(
        points[i],
        # popup="Lost till next point: " + packetsLost
    ).add_to(my_map)
    # if interLoss > 0:
    #     folium.PolyLine((points[i], points[i-1]),
    #                     popup="Lost packets in this line: " + str(interLoss),
    #                     weight=(interLoss),
    #                     color="red",
    #                     opacity=1).add_to(my_map)
    # else:
    #     folium.PolyLine((points[i], points[i-1]),
    #                     weight=min(racha+1, 10),
    #                     color="green",
    #                     popup=str(racha) + " consecutive packets",
    #                     opacity=0.3).add_to(my_map)

# add lines

# Save map
my_map.save("./out.html")
