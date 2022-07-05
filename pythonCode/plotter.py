from cmath import sqrt
import json
import matplotlib.pyplot as plt
import pprint
import pyproj
import numpy as np
import geopy.distance
import datetime
import matplotlib.dates as mdates

coords_gw = (44.412505, 8.929245)
archivo='plot/e1finalfinal.json'
magnitud='rssi'
over='distance'
tiempos=[]
valores=[]
distancias=[]
altura=20
with open(archivo,'r') as f:
    workingJson = json.load(f)

def lossesovertime(workingJson,colorline,label):
    derivada=True
    tiempos=[]
    valores=[]
    valores2=[]
    total=0
    tiempostotales=[]
    valoresfinales=[]
    for i in range(len(workingJson)):
        tiempostotales.append(workingJson[i]['time'])
        if(i==(len(workingJson)-2)):
            break
        else:
            perdidos=workingJson[i+1]['f_cnt']-workingJson[i]['f_cnt']
            if(perdidos>2):
                total=total+perdidos-2
                valores.append(total)
                valores2.append(perdidos-2)
                tiempos.append(workingJson[i+1]['time'])
    total=0
    print(valores2)
    for i in range(len(tiempostotales)):
        if(len(valores)==0):
            break
        else:
            if(tiempos[0]==tiempostotales[i]):
                total=valores[0]
                valoresfinales.append(total)
                valores.pop(0)
                tiempos.pop(0)
            else:
                valoresfinales.append(total)
    if(len(tiempostotales)!=len(valoresfinales)):
        for i in range(len(tiempostotales)-len(valoresfinales)):
            valoresfinales.append(total)
    for i in range(len(tiempostotales)):
        aux=tiempostotales[i].split('T')
        aux2=aux[1].split('.')
        aux3=aux2[0].split(':')
        tiempostotales[i]=datetime.datetime(year=2022,month=6,day=24,hour=int(aux3[0]),minute=int(aux3[1]),second=int(aux3[2]))
    print('Total paquetes recividos')
    print(len(workingJson))
    print('Total paquetes perdidos')
    print(total)
    print("% de perdida")
    print((total/(total+len(workingJson)))*100)
    print(valores)
    if(derivada):
        derivadas=[]
        for i in range(len(tiempostotales)-1):
            timedif=tiempostotales[i+1]-tiempostotales[i]
            if(timedif.seconds>0):
                slope=(valoresfinales[i+1]-valoresfinales[i])/timedif.seconds
            else:
                slope=0  
            derivadas.append(slope)
        plt.plot(tiempostotales[:-1], derivadas, linestyle="-", color=colorline, label=label)
    else:
        plt.plot(tiempostotales, valoresfinales, linestyle="-", color=colorline, label=label)
    
    
def magnitudovertime(workingJson,magnitud,color,label):
    tiempos=[]
    valores=[]
    sumatotal=0
    for i in range(len(workingJson)):
        tiempos.append(workingJson[i]['time'])
        valores.append(workingJson[i][magnitud])
    for i in range(len(workingJson)):
        sumatotal=sumatotal+workingJson[i][magnitud]
    for i in range(len(tiempos)):
        aux=tiempos[i].split('T')
        aux2=aux[1].split('.')
        aux3=aux2[0].split(':')
        tiempos[i]=datetime.datetime(year=2022,month=6,day=24,hour=int(aux3[0]),minute=int(aux3[1]),second=int(aux3[2]))
    print(magnitud+ "medio:")
    print(sumatotal/len(workingJson))
    plt.plot(tiempos, valores, linestyle="-", color=color, label=label)
    
def magnitudoverdistance(workingJson,magnitud):
    coords_gw = (44.412484774046746, 8.929275010050338)
    valores=[]
    distancias=[]
    for i in range(len(workingJson)):
        coords_2 = (workingJson[i]['lat'], workingJson[i]['lng'])
        distancia=geopy.distance.distance(coords_2,coords_gw).m
        if(distancia<5000):
            if(distancia<5):
                distancias.append(float(distancia))
                valores.append(workingJson[i][magnitud])
            else:
                dist=abs(distancia)   
                hipotenusa=sqrt((dist*dist)+(400))
                distancias.append(np.real(hipotenusa))
                valores.append(workingJson[i][magnitud])
    print('////')
    print(distancias)
    print('////')
###############ARRAY DISTANCIAS Y VALORES##################################
    maximo=max(distancias)
#######################Max Calculado############################3
    i=0
    grupos=[0]
    aux=0
    while(aux<maximo):
        aux=aux+5
        grupos.append(aux)
    agrupados=[]
    aux=[]
    for i in range (len(grupos)):
        agrupados.append([])
    for i in range(len(distancias)):
        for j in range(len(grupos)-1):
            if (distancias[i]>grupos[j] and distancias[i]<grupos[j+1]):
                agrupados[j].append(valores[i])
                break
    for i in range(len(agrupados)):
        if(len(agrupados[i])>0):
            agrupados[i]=np.mean(agrupados[i]) 
        else:
            agrupados[i]=0
    distfinales=[]
    valoresfinales=[]
    for i in range(len(agrupados)):
        if(agrupados[i]!=0):
            distfinales.append(grupos[i])
            valoresfinales.append(agrupados[i])
    resultados=[distfinales,valoresfinales]
    return resultados
    #plt.plot(distfinales, valoresfinales,'o', color='r', label=magnitud)
    #plt.legend()
    #plt.xlabel('Distance (m)')
    #plt.ylabel(magnitud)
    #plt.show()
    
def statse1(workingJson):
    lossesovertime(workingJson)
    magnitudovertime(workingJson,'rssi')
    magnitudovertime(workingJson,'snr')
    
def separadorcoords(workingJson):
    #grupos[0] puerto grupos[1] vicolis
    grupos=[[],[]]
    for i in range(len(workingJson)):
        x=workingJson[i]['lng']
        y=workingJson[i]['lat']
        puntorecta=(x*(-1.4286604361380904))+57.16641699066327
        if(y>puntorecta):
            grupos[1].append(workingJson[i])
        else:
            grupos[0].append(workingJson[i])
    return grupos
    
def separadorsf(workingJson,sf,pw):
    grupo=[]    
    for i in range(len(workingJson)):
        if(workingJson[i]['SF']==sf):
            if(workingJson[i]['powRet']==pw):
                grupo.append(workingJson[i])
    return grupo



"""
total=0
rssisum=0
grupos=separadorcoords(workingJson)
sfs=[7,10,12]
for i in range(len(sfs)):
    for j in range(len(grupos[0])):
        if(grupos[0][j]['SF']==sfs[i]):
            print
            rssisum=grupos[0][j]['rssi']+rssisum
            total+=1
    print(rssisum/total)
    print(total)
    total=0
    rssisum=0

"""
magnitudovertime(workingJson,'rssi','r','rssi ADR')
archivo='plot/e1!ADRtimextra4.json'
with open(archivo,'r') as f:
    workingJson = json.load(f)
magnitudovertime(workingJson,'rssi','b','rssi NO ADR')


plt.legend()
plt.ylabel('rssi')
plt.xlabel('time')
plt.gcf().autofmt_xdate()
myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)
plt.show()