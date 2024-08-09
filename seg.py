import urllib.request
import json
import os
import ssl

import base64
from PIL import Image
from io import BytesIO
def base64_to_image(base64_string):
    # Remove the data URI prefix if present
    if "data:image" in base64_string:
        base64_string = base64_string.split(",")[1]

    # Decode the Base64 string into bytes
    image_bytes = base64.b64decode(base64_string)
    return image_bytes
def create_image_from_bytes(image_bytes):
    # Create a BytesIO object to handle the image data
    image_stream = BytesIO(image_bytes)

    # Open the image using Pillow (PIL)
    image = Image.open(image_stream)
    return image
def create_image_from_bytes(image_bytes):
    # Create a BytesIO object to handle the image data
    image_stream = BytesIO(image_bytes)

    # Open the image using Pillow (PIL)
    image = Image.open(image_stream)
    return image


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
#with open('31.txt') as fp:
#  image = fp.read()

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

import base64
import json

image = os.path.join(".", "images", "31.png")

data =  {
  "input_data": {
    "columns": [
      "image",
      "input_points",
      "input_boxes",
      "input_labels",
      "multimask_output"
    ],
    "index": [0],
    "data": [[base64.encodebytes(read_image(image)).decode("utf-8"), "", "[[50, 50, 300, 300]]", "", False]]
  },
  "params": {}
}

body = str.encode(json.dumps(data))

url = 'https://dchoi-1845-insny.eastus.inference.ml.azure.com/score'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = 'my_primary_key'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
print("Hello")
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'facebook-sam-vit-base-4' }

req = urllib.request.Request(url, body, headers)
print(body)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
    from contextlib import redirect_stdout
    with open('out.txt', 'w') as f:
      with redirect_stdout(f):
        print(result)
    
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
