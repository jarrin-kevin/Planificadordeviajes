import json
import urllib.request
import requests
import urllib

import datetime as dt
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Weather:
    def __init__(self):
        self.city='Loja'
        self.url_openweather='http://api.openweathermap.org/data/2.5/forecast?'
        self.api_key_openweather='b14a413b64315656a8433b324e350484'
        self.url_apiop=self.url_openweather+ 'appid=' + self.api_key_openweather +'&q=' + self.city
        self.response=requests.get(self.url_apiop).json()
        self.df_weather=0
        self.hora_actual=0
        self.today=0
        self.textday=0
    def dataframe(self):
        self.df_weather=pd.json_normalize(self.response['list'][0:])
        self.df_weather=self.df_weather.drop(columns=['visibility','pop','main.feels_like','main.temp_min','main.temp_max','main.sea_level','main.grnd_level','main.temp_kf','clouds.all','wind.deg','wind.gust','rain.3h','sys.pod','dt'])
        self.df_weather=self.df_weather.rename(columns={'dt_txt':'fecha','main.temp':'temp','main.pressure':'presion',
                                        'main.humidity':'humedad','wind.speed':'velocidad_aire'})
        self.df_weather['fecha'] = self.df_weather['fecha'].astype('datetime64')
        
        lista_weather=[]
        for i in range(len(self.df_weather)):
            list=self.df_weather['weather'][i]
            lista_weather.extend(list)
        lista_weather=pd.DataFrame(lista_weather)
        lista_weather=lista_weather.drop(columns=['id'])
        self.df_weather=self.df_weather.drop(columns=['weather'])
        self.df_weather=pd.concat([lista_weather,self.df_weather],axis=1)
        self.df_weather=self.df_weather.set_index('fecha')
        self.df_weather['temp']=self.df_weather['temp']-273.15
        df_weather=self.df_weather
        return df_weather

    def horaactual(self):
        self.hora_actual=time.ctime()
        self.hora_actual=self.hora_actual.split()
        return self.hora_actual

    def elegirdia(self,value):
        today=dt.datetime.today()

        if value==1:
            self.day=(today+relativedelta(days=+1)).strftime('%Y-%m-%d')
            self.textday=(today+relativedelta(days=+1)).strftime('%A')
        elif value==2:
            self.day=(today+relativedelta(days=+2)).strftime('%Y-%m-%d')
            self.textday=(today+relativedelta(days=+2)).strftime('%A')
        elif value==3:
            self.day=(today+relativedelta(days=+3)).strftime('%Y-%m-%d')
            self.textday=(today+relativedelta(days=+3)).strftime('%A')
        elif value==4:
            self.day=(today+relativedelta(days=+4)).strftime('%Y-%m-%d')
            self.textday=(today+relativedelta(days=+4)).strftime('%A')

        self.xlim=self.df_weather.loc[self.day]
        xlim=self.xlim

        
        ## texto de nombre de los dias
        self.day1=(today+relativedelta(days=+1)).strftime('%Y-%m-%d')
        textday1=(today+relativedelta(days=+1)).strftime('%A')

        self.day2=(today+relativedelta(days=+2)).strftime('%Y-%m-%d')
        textday2=(today+relativedelta(days=+2)).strftime('%A')

        self.day3=(today+relativedelta(days=+3)).strftime('%Y-%m-%d')
        textday3=(today+relativedelta(days=+3)).strftime('%A')

        self.day4=(today+relativedelta(days=+4)).strftime('%Y-%m-%d')
        textday4=(today+relativedelta(days=+4)).strftime('%A')

        ## obtengo temp dia y noche de los dias en txt
        filtered_uno_day = self.df_weather.loc[self.df_weather.index == f'{self.day1}T09:00:00','temp']
        filtered_uno_night = self.df_weather.loc[self.df_weather.index == f'{self.day1}T21:00:00','temp']
        #filtered_df[0]
        

        filtered_dos_day = self.df_weather.loc[self.df_weather.index == f'{self.day2}T09:00:00','temp']
        filtered_dos_night = self.df_weather.loc[self.df_weather.index == f'{self.day2}T21:00:00','temp']

        filtered_tres_day = self.df_weather.loc[self.df_weather.index == f'{self.day3}T09:00:00','temp']
        filtered_tres_night = self.df_weather.loc[self.df_weather.index == f'{self.day3}T21:00:00','temp']

        filtered_cuatro_day = self.df_weather.loc[self.df_weather.index == f'{self.day4}T09:00:00','temp']
        filtered_cuatro_night = self.df_weather.loc[self.df_weather.index == f'{self.day4}T21:00:00','temp']


        return xlim,textday1,textday2,textday3,textday4,filtered_uno_day,filtered_uno_night,filtered_dos_day,filtered_dos_night,filtered_tres_day,filtered_tres_night,filtered_cuatro_day,filtered_cuatro_night

    
    def graficar(self):
        fig=plt.figure(figsize=(10,4),frameon=False)
        ax = fig.add_subplot()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.plot(self.xlim.temp,color='#ffd700',lw=1)
        ax.fill_between(self.xlim.index,self.xlim.temp,alpha=0.30,color='yellow')
        ax.get_yaxis().set_visible(False)
        ax.set_facecolor('#000000')
        ax.tick_params(axis='x',colors='white')
        for i in range(1, len(self.xlim)+1):
            plt.annotate('%.1f'%self.xlim.temp[i-1],xy=(self.xlim.index[i-1],self.xlim.temp[i-1]),xytext=(0, 0),textcoords='offset points',color='white',fontweight='demibold')

class Weather_hoy:

    def __init__(self):
        self.url_openweather_hoy='http://api.openweathermap.org/data/2.5/weather?'
        self.api_key_openweather_hoy='b14a413b64315656a8433b324e350484'
        self.city_hoy='Loja'
        self.url_apiop_hoy= self.url_openweather_hoy+ 'appid=' + self.api_key_openweather_hoy +'&q=' + self.city_hoy
        self.response_hoy=requests.get(self.url_apiop_hoy).json()
    
    def dataframe_hoy(self):
        self.df_weather_hoy=pd.json_normalize(self.response_hoy)
        lista_weather_hoy=[]
        for i in range(len(self.df_weather_hoy)):
            list_hoy=self.df_weather_hoy['weather'][i]
            lista_weather_hoy.extend(list_hoy)
        lista_weather_hoy=pd.DataFrame(lista_weather_hoy)
        self.df_weather_hoy=self.df_weather_hoy.drop(columns=['weather'])
        self.df_weather_hoy=pd.concat([lista_weather_hoy,self.df_weather_hoy],axis=1)
        self.df_weather_hoy['main.temp']=self.df_weather_hoy['main.temp']-273.15
        return self.df_weather_hoy



hola=Weather_hoy()
data=hola.dataframe_hoy

print(data)




    






