import json
import os
import dazl
from datetime import date
import base64
import sys
import argparse
from configparser import ConfigParser

parser = ConfigParser()
parser.read('configvaluesSawtooth.ini')
network = parser.get('url_value','url')
dataTemplate = parser.get('data_template','template_data')
imagesTemplate = parser.get('images_template','template_images')


def queryDataTempRangeSawtooth():
    parser = argparse.ArgumentParser(description='Range temperature')
    parser.add_argument('--DAMLParty', help='Type DAML user', type=str, required=True)
    parser.add_argument('--min', help='Type the minimum temperature', type=float, required=True)
    parser.add_argument('--max', help='Type the maximum temperature', type=float, required=True)
    args = vars(parser.parse_args())  
    daml_client = args ['DAMLParty']
    minTemp = args['min']
    maxTemp = args['max']
    with dazl.simple_client(network, daml_client) as client:
      
    # wait for the ACS to be fully read
      client.ready()
      contract_dict = client.find(dataTemplate)
      for contract in contract_dict:
        
        if float(contract.cdata['temperature']) > minTemp and float(contract.cdata['temperature']) < maxTemp :
           print("The data on range temperature:")
           print(contract.cdata)

if __name__ == '__main__':
 queryDataTempRangeSawtooth()
