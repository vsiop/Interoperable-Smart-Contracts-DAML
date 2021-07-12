
import dazl
import argparse
from configparser import ConfigParser

parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')

parserSawtooth = ConfigParser()
parserSawtooth.read('configvaluesSawtooth.ini')
networkSawtooth = parserSawtooth.get('url_value','url')
dataTemplateSawtooth = parserSawtooth.get('data_template','template_data')

parser = argparse.ArgumentParser(description='Range temperature')
parser.add_argument('--DAMLParty', help='Type DAML user', type=str, required=True)
parser.add_argument('--station', help='Type station', type=str, required=True)
args = vars(parser.parse_args())  
daml_client = args ['DAMLParty']
station = args ['station']

def queryDataOnSubstationFabric():
    with dazl.simple_client(networkFabric, daml_client) as client:
      client.ready()
      contract_dict = client.find(dataTemplateFabric)
      for contract in contract_dict:
        if contract.cdata['station'] == station:
           print("The data from the station %s" % station)
           print(contract.cdata)

def queryDataOnSubstationSawtooth():
    with dazl.simple_client(networkSawtooth, daml_client) as client:
      client.ready()
      all_contracts = client.find(dataTemplateSawtooth, {"weatherData": {"station": station }})
      if all_contracts:
        print('The sawtooth data')
        print(all_contracts)
      else:
        print ('Data for station', station, 'not found on sawtooth')


if __name__ == '__main__':
 queryDataOnSubstationFabric()
 queryDataOnSubstationSawtooth()

