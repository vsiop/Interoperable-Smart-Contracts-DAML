import json
import os
import dazl
from datetime import date
import base64
import sys
import argparse
from configparser import ConfigParser


parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')

def queryDataOnSubstation():
    parser = argparse.ArgumentParser(description='Range temperature')
    parser.add_argument('--DAMLParty', help='Type DAML user', type=str, required=True)
    parser.add_argument('--station', help='Type station', type=str, required=True)
    args = vars(parser.parse_args())  
    daml_client = args ['DAMLParty']
    station = args ['station']

    with dazl.simple_client(networkFabric, daml_client) as client:
      client.ready()
      contract_dict = client.find(dataTemplateFabric)
      for contract in contract_dict:
        if contract.cdata['station'] == station:
           print("The data from the station %s" % station)
           print(contract.cdata)

if __name__ == '__main__':
 queryDataOnSubstation()
