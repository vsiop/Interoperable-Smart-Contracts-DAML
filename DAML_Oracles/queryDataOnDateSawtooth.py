import dazl
from datetime import date
from configparser import ConfigParser

parser = ConfigParser()
parser.read('configvaluesSawtooth.ini')
network = parser.get('url_value','url')
dataTemplate = parser.get('data_template','template_data')
imagesTemplate = parser.get('images_template','template_images')
observer = parser.get('DAML_observer','observer')



def printDataOnDateSawtooth():
    with dazl.simple_client(network, observer) as client:
      client.ready()
      today = date.today()
      contract_dict = client.find(dataTemplate, {"weatherData": {"date": today }})
      print(contract_dict)

if __name__ == '__main__':
 printDataOnDateSawtooth()
