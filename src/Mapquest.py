import json
import urllib.request
import requests
import urllib
from geopy.geocoders import Nominatim
import pandas as pd
import folium as fl

class taxi:
    def __init__(self):
        self.api_url_geocoding_ubi='http://www.mapquestapi.com/geocoding/v1/address?'
        self.key='xrX87rGpHC3Rw2GzcM9rbNuYmcWPRdOB'
        self.api_url='http://www.mapquestapi.com/directions/v2/route?'
    
    def ubi_coordenadas(self,value):
        #value='Eplicachima,Loja, 110150, Ecuador'
        url_geocoding=self.api_url_geocoding_ubi+urllib.parse.urlencode({'key':self.key, 'location':value})
        data_geocoding= urllib.request.urlopen(url_geocoding).read().decode()
        ubicacion_json_geocoding=json.loads(data_geocoding) #guardo json
        ubicacion_list=ubicacion_json_geocoding['results'][0]['locations'][0]['latLng']# saco coordenadas
        ubicacion_coordenadas1=ubicacion_list.values()#saco coordenada
        self.ubicacion_coordenadas=list(ubicacion_coordenadas1) #saco coordenada en list
        ub_lng=str(self.ubicacion_coordenadas[0])#saco  str
        ub_lat=str(self.ubicacion_coordenadas[1])#saco lat str
        ubi=ub_lng,ub_lat #tupla
        self.ubi=','.join(ubi)# formato correcto para llamar a la api

        #return self.ubi,self.ubicacion_coordenadas

    def ruta_api(self):
        destino='Regina, Praga, Loja, 110107, Ecuador'
        url=self.api_url+urllib.parse.urlencode({'key':self.key, 'from':self.ubi, 'to':destino})
        data = urllib.request.urlopen(url).read().decode()
        self.obj_json=json.loads(data)

        #return self.obj_json

    def route_map(self):
        ruta=self.obj_json["route"]["legs"][0]['maneuvers'][0:]#extraigo info del json
        df_ruta=pd.DataFrame(ruta) #dataframe con toda la info
        startPoint_list=df_ruta['startPoint'].to_list()# coordenadas de la ruta en lista
        startPoint_df=pd.DataFrame(startPoint_list) # coordenadas de la ruta en dataframe
        df_ruta=pd.concat([df_ruta,startPoint_df],axis=1)

        place_lat = startPoint_df['lat'].astype(float).tolist()
        place_lng = startPoint_df['lng'].astype(float).tolist()

        points=[] #puntos

        for i in range(len(place_lat)):
            points.append([place_lat[i], place_lng[i]])

        #mapa de folium
        ubicacion_mapa = fl.Map(location=self.ubicacion_coordenadas, zoom_start=16)

        #cargo los puntos el mapa destino y ubicacion
        for i in range(0,len(df_ruta)):
            fl.Marker([df_ruta['lat'].iloc[i], df_ruta['lng'].iloc[i]],
                        popup=('calle {} \n '.format(df_ruta['streets'].iloc[i]))
                        ,icon = fl.Icon(color='blue',icon_color='white',prefix='fa', icon='taxi')
                        ).add_to(ubicacion_mapa)
        #cargo la linea de ruta
        fl.PolyLine(points, color='blue',dash_array='5',opacity ='.85',
                        tooltip ='Transit Route 101'
                        ).add_to(ubicacion_mapa)

        ubicacion_mapa.save('ubicacion_mapa.html')

        return df_ruta,ubicacion_mapa



class caminar:
    def __init__(self):
        self.api_url_geocoding_ubi='http://www.mapquestapi.com/geocoding/v1/address?'
        self.key='xrX87rGpHC3Rw2GzcM9rbNuYmcWPRdOB'
        self.api_url='http://www.mapquestapi.com/directions/v2/alternateroutes?'
    
    def ubi_coordenadas(self,value):
        #value='Eplicachima,Loja, 110150, Ecuador'

        url_geocoding=self.api_url_geocoding_ubi+urllib.parse.urlencode({'key':self.key, 'location':value})
        data_geocoding= urllib.request.urlopen(url_geocoding).read().decode()
        ubicacion_json_geocoding=json.loads(data_geocoding) #guardo json
        ubicacion_list=ubicacion_json_geocoding['results'][0]['locations'][0]['latLng']# saco coordenadas
        ubicacion_coordenadas1=ubicacion_list.values()#saco coordenada
        self.ubicacion_coordenadas=list(ubicacion_coordenadas1) #saco coordenada en list
        ub_lng=str(self.ubicacion_coordenadas[0])#saco  str
        ub_lat=str(self.ubicacion_coordenadas[1])#saco lat str
        ubi=ub_lng,ub_lat #tupla
        self.ubi=','.join(ubi)# formato correcto para llamar a la api

        #return self.ubi,self.ubicacion_coordenadas

    def ruta_api(self):
        maxRoutes='2'
        timeOverage='100'
        destino='Regina, Praga, Loja, 110107, Ecuador'
        url=self.api_url+urllib.parse.urlencode({'key':self.key, 'from':self.ubi, 'to':destino, 'maxRoutes':maxRoutes, 'timeOverage':timeOverage})
        data = urllib.request.urlopen(url).read().decode()
        self.obj_json=json.loads(data)

        #return self.obj_json

    def route_map(self):
        ruta=self.obj_json["route"]['alternateRoutes'][0]['route']['legs'][0]['maneuvers']#extraigo info del json
        df_ruta=pd.DataFrame(ruta) #dataframe con toda la info
        startPoint_list=df_ruta['startPoint'].to_list()# coordenadas de la ruta en lista
        startPoint_df=pd.DataFrame(startPoint_list) # coordenadas de la ruta en dataframe
        df_ruta=pd.concat([df_ruta,startPoint_df],axis=1)

        place_lat = startPoint_df['lat'].astype(float).tolist()
        place_lng = startPoint_df['lng'].astype(float).tolist()

        points=[] #puntos

        for i in range(len(place_lat)):
            points.append([place_lat[i], place_lng[i]])

        #mapa de folium
        ubicacion_mapa = fl.Map(location=self.ubicacion_coordenadas, zoom_start=17)

        #cargo los puntos el mapa destino y ubicacion
        for i in range(0,len(df_ruta)):
            fl.Marker([df_ruta['lat'].iloc[i], df_ruta['lng'].iloc[i]],
                        popup=('calle {} \n '.format(df_ruta['streets'].iloc[i]))
                        ,icon = fl.Icon(color='blue',icon_color='white',prefix='fa', icon='fa-solid fa-person')
                        ).add_to(ubicacion_mapa)
        #cargo la linea de ruta
        fl.PolyLine(points, color='blue',dash_array='5',opacity ='.85',
                        tooltip ='Transit Route 101'
                        ).add_to(ubicacion_mapa)

        #ubicacion_mapa.save('ubicacion_mapa11.html')
        #m=str(m)
        
        # html_mapa=open('ubicacion_mapa.html',"w")
        # html_mapa.write(m)
        # html_mapa.close()

        # with open(m, 'w') as user_file_name:
        #     user_file_name.writelines(open('ubicacion_mapa.html'))
        
        return df_ruta,ubicacion_mapa
        




# mapa=caminar()
# mapa.ubi_coordenadas('Avenida Orillas del Zamora ,Loja Ecuador')
# mapa.ruta_api()
# k,l=mapa.route_map()
# l.save('ubicacion_mapa_caminar.html')

