import sys
from PyQt5.QtWidgets import QMainWindow, QApplication 
from Ui_Gui import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime 
from weather import Weather
from weather import Weather_hoy
from Mapquest import taxi
from Mapquest import caminar
from matplotlib.axis import Axis
import io
from PIL import Image




class DialogoSaludoAplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.W=0
        self.dataframe=0
        self.value=1

        self.window = Ui_MainWindow()
        self.window.setupUi(self)
        self.window.pushButtonbuscar.clicked.connect(self.capturardire)
        self.window.pushButtonbuscar.clicked.connect(self.info_hoy)
        
        self.window.pushButtondiauno.clicked.connect(self.value1)
        self.window.pushButtondia2.clicked.connect(self.value2)
        self.window.pushButtondia3.clicked.connect(self.value3)
        self.window.pushButtondia4.clicked.connect(self.value4)

        # self.Opcionviaje = [
        #     self.window.radioButtonAuto,
        #     self.window.radioButtoncaminar,
        #     self.window.radioButtonbici
        # ]

        # for radioButton in self.Opcionviaje:
        self.window.radioButtonAuto.clicked.connect(self.auto)
        self.window.radioButtoncaminar.clicked.connect(self.caminar)
        self.window.radioButtonbici.clicked.connect(self.bicicleta)
        

    def value1(self):
        self.value1=1
        self.grafico(self.value1)
        self.window.labeltemperatura.setText(f'{self.textday1}')
    def value2(self):
        self.value2=2
        self.grafico(self.value2)
        self.window.labeltemperatura.setText(f'{self.textday2}')
    def value3(self):
        self.value3=3
        self.grafico(self.value3)
        self.window.labeltemperatura.setText(f'{self.textday3}')
    def value4(self):
        self.value4=4
        self.grafico(self.value4)
        self.window.labeltemperatura.setText(f'{self.textday4}')
    #funcion para graficar
    def grafico(self,value):
        self.W=Weather()
        self.dataframe=self.W.dataframe()
        xlim,self.textday1,self.textday2,self.textday3,self.textday4,self.filtered_uno_day,self.filtered_uno_night,self.filtered_dos_day,self.filtered_dos_night,self.filtered_tres_day,self.filtered_tres_night,self.filtered_cuatro_day,self.filtered_cuatro_night=self.W.elegirdia(value)
        
        #limpiar grafica area
        for x in self.window.figure.axes:
            x.clear()
        
        self.window.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.plot(xlim.temp,color='#ffd700',lw=1,)
        plt.fill_between(xlim.index,xlim.temp,alpha=0.30,color='yellow')
        for i in range(1, len(xlim)+1):
            plt.annotate('%.1f'%xlim.temp[i-1],xy=(xlim.index[i-1],xlim.temp[i-1]),xytext=(0, 0),textcoords='offset points',color='white',fontweight='demibold')
        
        self.window.canvas.draw()

    #fcuncion para poner la informacion del clima
    def info_hoy(self):

        grafico=self.grafico(1)

        W_hoy=Weather_hoy()
        dataframe_hoy=W_hoy.dataframe_hoy()
        
        temp_num=round(dataframe_hoy['main.temp'][0])
        temp_num=repr(temp_num)
        self.window.label_temphoy.setText(f' {temp_num}°c')
        
        pressure=repr(dataframe_hoy['main.pressure'][0])
        humedad=repr(dataframe_hoy['main.humidity'][0])
        viento=repr(dataframe_hoy['wind.speed'][0])
        self.window.listWidgetcaracteristicasdeldia.clear()
        self.window.listWidgetcaracteristicasdeldia.addItem(f' Presion atmosferica: {pressure}hPa')
        #self.window.listWidget_clima.setHeight()
        self.window.listWidgetcaracteristicasdeldia.addItem(f'  Humedad: {humedad}%')
        self.window.listWidgetcaracteristicasdeldia.addItem(f'  Velocidad aire: {viento}m/s')

        city_txt=dataframe_hoy['name'][0]
        self.window.labelciudad.setText(f'       {city_txt}')

        hoy=self.W.horaactual()
        self.window.listhoradeldia.clear()
        self.window.listhoradeldia.addItem(f'       {hoy[0]} {hoy[3]}')
        
        description=dataframe_hoy['description'][0]
        self.window.listhoradeldia.addItem(f'       {description}')

        self.window.pushButtondiauno.setText(f'{self.textday1}')
        self.window.pushButtondia2.setText(f'{self.textday2}')
        self.window.pushButtondia3.setText(f'{self.textday3}')
        self.window.pushButtondia4.setText(f'{self.textday4}')

        self.window.labeltemperatura.setText(f'{self.textday1}')
        
        filtered_uno_day=round(self.filtered_uno_day[0])
        filtered_uno_night=round(self.filtered_uno_night[0])

        filtered_dos_day=round(self.filtered_dos_day[0])
        filtered_dos_night=round(self.filtered_dos_night[0])

        filtered_tres_day=round(self.filtered_tres_day[0])
        filtered_tres_night=round(self.filtered_tres_night[0])

        filtered_cuatro_day=round(self.filtered_cuatro_day[0])
        filtered_cuatro_night=round(self.filtered_cuatro_night[0])

        self.window.tempdia1.setText(f'{filtered_uno_night}°c / {filtered_uno_day}°c')
        self.window.tempdia2.setText(f'{filtered_dos_night}°c / {filtered_dos_day}°c')
        self.window.tempdia3.setText(f'{filtered_tres_night}°c / {filtered_tres_day}°c')
        self.window.tempdia4.setText(f'{filtered_cuatro_night}°c / {filtered_cuatro_day}°c')
        return dataframe_hoy
    #funcion para mapquest auto
    def auto(self):
        self.auto=taxi()
        ubi_coordenadas=self.auto.ubi_coordenadas(self.capturardire())
        ruta_api=self.auto.ruta_api()
        df_route,img_route=self.auto.route_map()

        self.window.listcaracteristicasdelviaje.clear()
        tiempo_seg=df_route['time'].sum()
        tiempo_min=tiempo_seg*0.0166667
        tiempo_min=round(tiempo_min)
        self.window.listcaracteristicasdelviaje.addItem(f'El viaje durara {tiempo_min} min')

        distance_millas=df_route['distance'].sum()
        distance_km=distance_millas*1.609344
        distance_km=round(distance_km)
        self.window.listcaracteristicasdelviaje.addItem(f'La distancia del viaje es {distance_km} km')

        costoviaje=round(0.40+(tiempo_min*0.07)+(distance_km*0.28))

        if costoviaje>1.25:
            self.window.listcaracteristicasdelviaje.addItem(f'El costo del viaje es {costoviaje}$')
        else:
            self.window.listcaracteristicasdelviaje.addItem('El costo del viaje es 1.25$')

        img_route.save('routecarro.html')
        img_data=img_route._to_png(1)
        img=Image.open(io.BytesIO(img_data))
        img.save('taxirecorrido1.png')

        #self.window.mapaweb.setUrl(QtWidgets.setHtml("file:///C:/Users/jarri/OneDrive/Documentos/Python Scripts/RepositorioPYTHONINTERM_Estudiantes/routecarro.html.html"))

        self.window.label_mapaimg.setPixmap(QtGui.QPixmap("c:\\Users\\jarri\\OneDrive\\Documentos\\Python Scripts\\RepositorioPYTHONINTERM_Estudiantes\\taxirecorrido1.png"))
        self.window.label_mapaimg.setScaledContents(True)

        self.window.label_imgopcionrecomendada.setPixmap(QtGui.QPixmap("c:\\Users\\jarri\\OneDrive\\Documentos\\Python Scripts\\RepositorioPYTHONINTERM_Estudiantes\\proyecto final\\imagene/taxi.png"))
        self.window.label_imgopcionrecomendada.setScaledContents(True)

        self.window.labelradiobottom.setText('Taxi')
        return distance_km

    def caminar(self):
        self.caminar=caminar()
        ubi_coordenadas_caminar=self.caminar.ubi_coordenadas(self.capturardire())
        ruta_api_caminar=self.caminar.ruta_api()
        df_route_caminar,img_route_caminar=self.caminar.route_map()

        self.window.listcaracteristicasdelviaje.clear()

        tiempo_seg=df_route_caminar['time'].sum()
        tiempo_min=(tiempo_seg+1200)*0.0166667
        tiempo_min=round(tiempo_min)
        self.window.listcaracteristicasdelviaje.addItem(f'El viaje durara {tiempo_min} min')

        distance_millas=df_route_caminar['distance'].sum()
        distance_km=distance_millas*1.609344
        distance_km=round(distance_km)
        self.window.listcaracteristicasdelviaje.addItem(f'La distancia del viaje es {distance_km} km')

        img_route_caminar.save('routecaminar.html')
        img_data=img_route_caminar._to_png(1)
        img=Image.open(io.BytesIO(img_data))
        img.save('caminar.png')

        #self.window.mapaweb.setUrl(QtCore.QUrl("file:///C:/Users/jarri/OneDrive/Documentos/Python Scripts/RepositorioPYTHONINTERM_Estudiantes/routecaminar.html.html"))
        self.window.label_mapaimg.setPixmap(QtGui.QPixmap("c:\\Users\\jarri\\OneDrive\\Documentos\\Python Scripts\\RepositorioPYTHONINTERM_Estudiantes\\caminar.png"))
        self.window.label_mapaimg.setScaledContents(True)

        self.window.label_imgopcionrecomendada.setPixmap(QtGui.QPixmap("c:\\Users\\jarri\\OneDrive\\Documentos\\Python Scripts\\RepositorioPYTHONINTERM_Estudiantes\\proyecto final\\imagene/caminar.png"))
        self.window.label_imgopcionrecomendada.setScaledContents(True)

        self.window.labelradiobottom.setText('Caminar')
        return distance_km

    def bicicleta(self):
        self.bicicleta=caminar()
        ubi_coordenadas_caminar=self.bicicleta.ubi_coordenadas(self.capturardire())
        ruta_api_caminar=self.bicicleta.ruta_api()
        df_route_caminar,img_route_caminar=self.bicicleta.route_map()

        self.window.listcaracteristicasdelviaje.clear()

        tiempo_seg=df_route_caminar['time'].sum()
        tiempo_min=(tiempo_seg+600)*0.0166667
        tiempo_min=round(tiempo_min)
        self.window.listcaracteristicasdelviaje.addItem(f'El viaje durara {tiempo_min} min')

        distance_millas=df_route_caminar['distance'].sum()
        distance_km=distance_millas*1.609344
        distance_km=round(distance_km)
        self.window.listcaracteristicasdelviaje.addItem(f'La distancia del viaje es {distance_km} km')

        img_data=img_route_caminar._to_png(1)
        img=Image.open(io.BytesIO(img_data))
        img.save('bicicleta.png')

        self.window.label_mapaimg.setPixmap(QtGui.QPixmap("c:\\Users\\jarri\\OneDrive\\Documentos\\Python Scripts\\RepositorioPYTHONINTERM_Estudiantes\\bicicleta.png"))
        self.window.label_mapaimg.setScaledContents(True)

        self.window.label_imgopcionrecomendada.setPixmap(QtGui.QPixmap("c:\\Users\\jarri\\OneDrive\\Documentos\\Python Scripts\\RepositorioPYTHONINTERM_Estudiantes\\proyecto final\\imagene/caminar.png"))
        self.window.label_imgopcionrecomendada.setScaledContents(True)

        self.window.labelradiobottom.setText('Bicicleta')
        return distance_km

    def capturardire(self):
        self.text=self.window.lineEdit_insertubi.text()
        hora_actual = datetime.datetime.now()
        hora_formateada = hora_actual.strftime('%H:%M')
        self.window.lineEdit_inserthorasalida.setText(hora_formateada)
        self.text_hora=self.window.lineEdit_inserthorallegada.text()
        self.text_hora=int(self.text_hora)

        if self.text_hora <10:
            self.window.lineEdit_opcionrecomendada.setText('Tu mejor opcion es ir en taxi')
        elif self.text_hora <=20:
            self.window.lineEdit_opcionrecomendada.setText('Tu mejor opcion es ir en bicicleta')
        elif self.text_hora >20:
            self.window.lineEdit_opcionrecomendada.setText('Tu mejor opcion es ir en caminar')
        return self.text



if __name__ == '__main__':
    # Crea entorno de tipo QApplication y pasa como parámetro las lista de parametros, linea de comandos
    app = QApplication(sys.argv)
    
    # Crea dialogo
    dialogo = DialogoSaludoAplicacion()
    
    # Muestra el dialogo
    dialogo.show()

    # Para el evento de salida, invocamos el método exec. 
    sys.exit(app.exec_())


        
        
        



