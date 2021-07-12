import dazl
from configparser import ConfigParser

parser = ConfigParser()
parser.read('configvaluesSawtooth.ini')
network = parser.get('url_value','url')
dataTemplate = parser.get('data_template','template_data')
imagesTemplate = parser.get('images_template','template_images')
observer = parser.get('DAML_observer','observer')

def printActiveDataSawtooth():
    with dazl.simple_client(network, observer) as client: 
      client.ready()
      contract_dict = client.find(dataTemplate)
      for contract in contract_dict:
          print(contract)
          print(type(contract))
        

if __name__ == '__main__':
 printActiveDataSawtooth()
