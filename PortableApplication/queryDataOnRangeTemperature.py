
import dazl
import argparse
from configparser import ConfigParser

parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')


def queryDataTempRange():
    parser = argparse.ArgumentParser(description='Range temperature')
    parser.add_argument('--DAMLParty', help='Type DAML user', type=str, required=True)
    parser.add_argument('--min', help='Type the minimum temperature', type=float, required=True)
    parser.add_argument('--max', help='Type the maximum temperature', type=float, required=True)
    args = vars(parser.parse_args())  
    daml_client = args ['DAMLParty']
    minTemp = args['min']
    maxTemp = args['max']
    with dazl.simple_client(networkFabric, daml_client) as client:
      
    # wait for the ACS to be fully read
      client.ready()
      contract_dict = client.find(dataTemplateFabric)
      for contract in contract_dict:
        
        if float(contract.cdata['temperature']) > minTemp and float(contract.cdata['temperature']) < maxTemp :
           print('The transaction ID:')
           print(contract.cid)
           print("The data on range temperature:")
           print(contract.cdata)

if __name__ == '__main__':
 queryDataTempRange()
