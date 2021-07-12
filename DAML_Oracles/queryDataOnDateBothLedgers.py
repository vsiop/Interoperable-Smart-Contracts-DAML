
import dazl
from datetime import date
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

def printDataOnDateFabric():
    with dazl.simple_client(networkFabric, observer) as client:
      client.ready()
      contract_dict = client.find(dataTemplateFabric)
      for contract in contract_dict:
        today = date.today()
        if contract.cdata['date'] == today:
           print('The fabric data for date: ', today)
           print(contract.cdata)

def printDataOnDateSawtooth():
    with dazl.simple_client(networkSawtooth, signatory) as client:
      client.ready()
      today = date.today()
      all_contracts = client.find(dataTemplateSawtooth, {"weatherData": {"date": today }})
      if all_contracts:
        print('The sawtooth data for date: ', today)
        print(all_contracts)
      else:
        print ('Data for ', today, ' not found on sawtooth')


if __name__ == '__main__':
 printDataOnDateFabric()
 printDataOnDateSawtooth()