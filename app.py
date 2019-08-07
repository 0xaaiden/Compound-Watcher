import os
import json 
with open('keys.txt', 'r') as myfile:
    keys=json.load(myfile)
os.environ['WEB3_INFURA_API_KEY'] = keys["infura-api"]
os.environ['WEB3_INFURA_API_SECRET'] = keys["infura-private"]

from modules import *


while True:
    print("\n\n\n")
    parse()
