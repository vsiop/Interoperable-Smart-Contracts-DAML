import json
import os
import dazl
from datetime import date
import base64
import sys
from configparser import ConfigParser

parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')
observer = parserFabric.get('DAML_observer', 'observer')


def printDataOnDate():
    with dazl.simple_client(networkFabric, 'Operator') as client:
      client.ready()
      contract_dict = client.find(networkFabric)
      for contract in contract_dict:
        today = date.today()
        if contract.cdata['date'] == today:
           print("data:" )
           print(contract.cdata)

if __name__ == '__main__':
 printDataOnDate()
