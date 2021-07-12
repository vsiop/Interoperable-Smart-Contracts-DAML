import json
import os.path
import dazl
from datetime import date
import base64
from io import BytesIO
from PIL import Image
import base64
import matplotlib.pyplot as plt
from configparser import ConfigParser


parserFabric = ConfigParser()
parserFabric.read('configvaluesFabric.ini')
networkFabric = parserFabric.get('url_value','url')
imagesTemplateFabric = parserFabric.get('images_template','template_images')
observer = parserFabric.get('DAML_observer', 'observer')



def downloadFabricImage():
    with dazl.simple_client(networkFabric, observer) as client:
      if not os.path.exists('dowloadedImages'):
        os.makedirs('dowloadedImages')
      counter = 0
      client.ready()
      contract_dict = client.find(imagesTemplateFabric)
      for contract in contract_dict:
        today = date.today()
        if contract.cdata['date'] == today:
          counter = counter + 1
          b64string = contract.cdata['image'] 

          filename =  contract.cdata['station'] 

          finaFilename = filename + str(counter) + '.png'

          if not os.path.exists('dowloadedImages/'+ str(today)):
            os.makedirs('dowloadedImages/'+ str(today))
          plt.text(0,0,b64string)
          plt.savefig('dowloadedImages/'+ str(today) + '/' +finaFilename, dpi=100)


if __name__ == '__main__':
 downloadFabricImage()
