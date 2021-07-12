import dazl
import argparse
from configparser import ConfigParser

parser = ConfigParser()
parser.read('configvaluesSawtooth.ini')
network = parser.get('url_value','url')
dataTemplate = parser.get('data_template','template_data')



def queryDataOnSubstationSawtooth():
    parser = argparse.ArgumentParser(description='Range temperature')
    parser.add_argument('--DAMLParty', help='Type DAML user', type=str, required=True)
    parser.add_argument('--station', help='Type station', type=str, required=True)
    args = vars(parser.parse_args())  
    daml_client = args ['DAMLParty']
    station = args ['station']

    with dazl.simple_client(network, daml_client) as client:
      client.ready()
      contract_dict = client.find(dataTemplate)
      for contract in contract_dict:
        if contract.cdata['station'] == station:
           print("The data from the station %s" % station)
           print(contract.cdata)

if __name__ == '__main__':
 queryDataOnSubstationSawtooth()
