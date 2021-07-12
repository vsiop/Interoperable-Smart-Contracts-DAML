
import os.path
import dazl
from datetime import date
import matplotlib.pyplot as plt
from configparser import ConfigParser

parserSawtooth = ConfigParser()
parserSawtooth.read('configvaluesSawtooth.ini')
networkSawtooth = parserSawtooth.get('url_value','url')
imagesTemplateSawtooth = parserSawtooth.get('images_template','template_images')
signatory = parserSawtooth.get('DAML_signatory', 'signatory')

parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
imagesTemplateFabric= parserFabric.get('images_template','template_images')
observer = parserFabric.get('DAML_observer', 'observer')

def getImagesBasedOnDateFabric():
    with dazl.simple_client(networkFabric, observer) as client:
      client.ready()
      if not os.path.exists('dowloadedImages'):
        os.makedirs('dowloadedImages')
      counter = 0
      contract_dict = client.find(imagesTemplateFabrics)
      for contract in contract_dict:
        today = date.today()
        if contract.cdata['date'] == today:
          counter = counter + 1
          b64string = contract.cdata['image'] 
          filename =  contract.cdata['station'] 
          finaFilename = filename + str(counter) + '.png'
          if not os.path.exists('dowloadedImages/Fabric/'+ str(today)):
            os.makedirs('dowloadedImages/Fabric/'+ str(today))
          plt.text(0,0,b64string)
          plt.savefig('dowloadedImages/Fabric/' + finaFilename, dpi=100)


def getImagesBasedOnDateBothSawtooth():
    with dazl.simple_client(networkFabric, observer) as client:
      if not os.path.exists('dowloadedImages'):
        os.makedirs('dowloadedImages')
      counter = 0
    # wait for the ACS to be fully read
      client.ready()
      today = date.today
      contract_dict = client.find(dataTemplate, {"weatherData": {"date": today }})
      for contract in contract_dict:
        today = date.today
        counter = counter + 1
        b64string = contract.cdata['image'] 
        filename =  contract.cdata['station'] 
        finaFilename = filename + str(counter) + '.png'
        if not os.path.exists('dowloadedImages/Sawtooth/'+ str(today)):
          os.makedirs('dowloadedImages/Sawtooth/'+ str(today))
        plt.text(0,0,b64string)
        plt.savefig('dowloadedImages/Sawtooth/' + finaFilename, dpi=100)


if __name__ == '__main__':
 getImagesBasedOnDateFabric()
 getImagesBasedOnDateBothSawtooth()
