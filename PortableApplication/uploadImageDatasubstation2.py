import csv
import pandas as pd
import numpy
import json
import logging
import os
import sys
import time
import base64
from datetime import date
from os.path import dirname, join
import cv2
import numpy as np

import dazl
from dazl.model.reading import ReadyEvent, ContractCreateEvent

from configparser import ConfigParser


parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
imagesTemplateFabric = parserFabric.get('images_template','template_images')
station = parserFabric.get('Stations', 'station2')
observer = parserFabric.get('DAML_observer', 'observer')

network = dazl.Network()
network.set_config(url=networkFabric)



logging.basicConfig(filename='app.log', level=logging.INFO)

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

#Set the variables according to Smart Contract
def init_setup (network: network, operator,today, current_time, image ):
  with dazl.simple_client(networkFabric, station) as client:
    
    logging.info ("Initializing Setup for" + station)
    contract = { 'station' : station, 'operator': operator, 'time' : current_time, 'date' : today, 'image':image}
    client.ready()
    client.submit_create(imagesTemplateFabric, contract)

#Load data      
def dazl_main(network):
    for x in range(8,  9):
      imageName = 'rain' +  str(x) + '.jpg'
      path = '/../../Data/ImagesData/dataset/rainy/'
      current_directory = os.getcwd()
      with open( current_directory + path + imageName, "rb") as image:
        b64string = base64.b64encode(image.read())

        image = b64string
        #Find local time
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        #Find date
        today = date.today()
        #Call ini_setup to pass the arguments
        init_setup(network, observer,today, current_time, image)  

#Interact with the ledger 
def main():
  dazl.run(dazl_main)
    


if __name__ == '__main__':
    main()

