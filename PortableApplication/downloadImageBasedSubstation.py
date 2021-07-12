import json
import os.path
import dazl
from datetime import date
import base64
import argparse
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
      parser = argparse.ArgumentParser(description='Download images based on signatory substation')
      parser.add_argument('--station', help='Type a signatory station', type=str, required=True)
      args = vars(parser.parse_args())  
      substation = args ['station']
      if not os.path.exists('dowloadedImages'):
        os.makedirs('dowloadedImages')
      counter = 0
      client.ready()
      contract_dict = client.find(imagesTemplateFabric)
      for contract in contract_dict:
        today = date.today()
        if contract.cdata['station'] == substation:
          counter = counter + 1
          b64string = contract.cdata['image'] 

          filename =  contract.cdata['station'] 

          finaFilename = filename + str(counter) + '.png'

          if not os.path.exists('dowloadedImages/'+ '/' +substation + '/' + str(today)):
            os.makedirs('dowloadedImages/'+'/' + substation + '/' + str(today))
          plt.text(0,0,b64string)
          plt.savefig('dowloadedImages/'+ '/' + substation + '/' +str(today) + '/' +finaFilename, dpi=100)


if __name__ == '__main__':
 downloadFabricImage()
