
import logging
import time
from datetime import date
import dazl
from configparser import ConfigParser

parserSawtooth = ConfigParser()
parserSawtooth.read('configvaluesSawtooth.ini')
networkSawtooth = parserSawtooth.get('url_value','url')
dataTemplateSawtooth = parserSawtooth.get('data_template','template_data')
signatory = parserSawtooth.get('DAML_signatory', 'signatory')

network = dazl.Network()
network.set_config(url=networkSawtooth)

parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
dataTemplateFabric = parserFabric.get('data_template','template_data')
observer = parserFabric.get('DAML_observer', 'observer')

logging.basicConfig(filename='app.log', level=logging.INFO)


def oracles(network: dazl.Network, data, cid):
  with dazl.simple_client(networkSawtooth, signatory) as client: 
    #Find local time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    #Find date
    today = date.today() 
    logging.info ("Initializing Setup for" + str(cid))
    client.ready()
    all_contracts = client.find(dataTemplateSawtooth, {"fabricInfo": {"cid": str(cid) }})
    if all_contracts:
        print ('Transaction ID exists on both')
    else:
      contract = {'fabricInfo.cid': str(cid),'fabricInfo.date':today,'fabricInfo.time':current_time, 'sawtoothParties.operator':'Operator', 'sawtoothParties.participants': 'User1','weatherData': data,  }
      client.ready()
      client.submit_create(dataTemplateSawtooth, contract)


def dazl_main(network):
  with dazl.simple_client(networkFabric, observer) as client:
    client.ready()
    contract_dict = client.find(dataTemplateFabric)
    for contract in contract_dict:
      today = date.today()
      if contract.cdata['date'] == today:
          print('The fabric transaction ID:')
          print(contract.cid)
          print("Found data:" )
          print(contract.cdata)
          oracles(network, contract.cdata, contract.cid)

def main():
  dazl.run(dazl_main)
    


if __name__ == '__main__':
    main()

