import csv
import pandas as pd
import numpy
import json
import logging
import os
import sys
import time
from datetime import date
from os.path import dirname, join

import dazl
from dazl.model.reading import ReadyEvent, ContractCreateEvent

from configparser import ConfigParser


parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')
observer = parserFabric.get('DAML_observer', 'observer')

network = dazl.Network()
network.set_config(url=networkFabric)



logging.basicConfig(filename='app.log', level=logging.INFO)

#Set the variables according to Smart Contract
def init_setup (network: dazl.Network, station, operator, idDevice, humidity, temperature, RainIntensityvalue, WindDirectionvalue, WindSpeedvalue, MaxWindSpeedvalue, SolarRadiationvalue, BatteryLifevalue, today, current_time ):
  #This if statement check about the name of the weather station and use the roadmap.csv the hash signature 
  print(station, operator, idDevice, humidity, temperature, RainIntensityvalue, WindDirectionvalue, WindSpeedvalue, MaxWindSpeedvalue, SolarRadiationvalue, BatteryLifevalue, today, current_time)
  if station == 'Oak Street Weather Station':
  	station ='OakStreetWeatherStation'
  elif 	station == 'Foster Weather Station':
  	station ='FosterWeatherStation'
  elif station == '63rd Street Weather Station':
  	station ='63rdStreetWeatherStation'
  else:
  	print ('Wrong weather station')
  #print(station)
  #Create smart contract
  with dazl.simple_client(networkFabric, station) as client:  
    logging.info ("Initializing Setup for" + station)
    contract = { 'station' : station, 'nameStation': 'toronto', 'operator': operator, 'time' : current_time, 'date' : today,
                 'measurementID': idDevice, 'humidity': humidity, 
                 'temperature' : temperature, 'rainIntensidy' : RainIntensityvalue, 'windDirection': WindDirectionvalue,
                   'windSpeed' : WindSpeedvalue, 'maxwindSpeed' : MaxWindSpeedvalue,
                   'solarRadiation' : SolarRadiationvalue, 'batteryLife' : BatteryLifevalue }
    client.ready()
    client.submit_create(dataTemplateFabric, contract)

#Load data from csv         
def dazl_main(network):
  data = pd.read_csv('../../Data/RawData/weather.csv')
  Humidity = data[['Humidity']].values.tolist()
  Temperature = data[['Wet Bulb Temperature']].values.tolist()
  IdDevice = data[['Measurement ID']].values.tolist()
  WeatherSation = data[['Station Name']].values.tolist()
  RainIntensity = data[['Rain Intensity']].values.tolist()
  WindDirection = data[['Wind Direction']].values.tolist()
  WindSpeed = data[['Wind Speed']].values.tolist()
  MaxWindSpeed = data[['Maximum Wind Speed']].values.tolist()
  SolarRadiation = data[['Solar Radiation']].values.tolist()
  BatteryLife = data[['Battery Life']].values.tolist()
  #Convert lists to strings
  for x in range(1000, 1010):
    BatteryLifevalue = ''.join(str(e) for e in BatteryLife[x])
    SolarRadiationvalue = ''.join(str(e) for e in SolarRadiation[x])
    MaxWindSpeedvalue = ''.join(str(e) for e in MaxWindSpeed[x])
    WindSpeedvalue = ''.join(str(e) for e in WindSpeed[x])
    WindDirectionvalue = ''.join(str(e) for e in WindDirection[x])
    RainIntensityvalue = ''.join(str(e) for e in RainIntensity[x])
    NameofStation = ''.join(WeatherSation[x])
    Tempvalue = ''.join(str(e) for e in Temperature[x])
    IoTdevice = ''.join(IdDevice[x])
    Humidvalue = ''.join(str(e) for e in Humidity[x])
    #Find local time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    #Find date
    today = date.today()
    #Call init_setup to pass the arguments
    init_setup(network, NameofStation, observer, IoTdevice, Humidvalue, Tempvalue, RainIntensityvalue, WindDirectionvalue, WindSpeedvalue, MaxWindSpeedvalue, SolarRadiationvalue, BatteryLifevalue, today, current_time)  
    print('Data send')
    sleeptime()

#Add a delay for more realistic data 
def sleeptime():
  time.sleep(5)

#Interact with the ledger 
def main():
  dazl.run(dazl_main)
    


if __name__ == '__main__':
    main()

