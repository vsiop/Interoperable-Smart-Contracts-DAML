import json
import os
import dazl
from configparser import ConfigParser
parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')
observer = parserFabric.get('DAML_observer', 'observer')

def printActiveData():
    with dazl.simple_client(networkFabric, observer) as client: 
    # wait for the ACS to be fully read
      client.ready()
      contract_dict = client.find(dataTemplateFabric)
      for contract in contract_dict:
          print(contract)

if __name__ == '__main__':
 printActiveData()
