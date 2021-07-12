
import dazl
from configparser import ConfigParser

parserSawtooth = ConfigParser()
parserSawtooth.read('configvaluesSawtooth.ini')
networkSawtooth = parserSawtooth.get('url_value','url')
dataTemplateSawtooth = parserSawtooth.get('data_template','template_data')
signatory = parserSawtooth.get('DAML_signatory', 'signatory')

parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')
observer = parserFabric.get('DAML_observer', 'observer')

def printActiveDataFabric():
    with dazl.simple_client(networkFabric, observer) as client:
      client.ready()
      contract_dict = client.find_active(dataTemplateFabric)
      print('The fabric data:')
      print(contract_dict)

def printActiveDataSawtooth():
    with dazl.simple_client(networkSawtooth, signatory) as client:
      client.ready()
      all_contracts = client.find_active(dataTemplateSawtooth)
      if all_contracts:
        print('The sawtooth data')
        print(all_contracts)
      else:
        print ('Data for not found on sawtooth')


if __name__ == '__main__':
 printActiveDataFabric()
 printActiveDataSawtooth()