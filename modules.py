import os
import time
import importlib
import json
import prettytable
import urllib.request 
from modules import *
from http.cookiejar import CookieJar
from web3.auto.infura import w3
from urllib.request import build_opener
from termcolor import colored
from urllib.error import HTTPError
from pushbullet.pushbullet import PushBullet

with open('keys.txt', 'r') as myfile:
    keys=json.load(myfile)
    
if w3.isConnected() == True:
    print("The bot is connected to the ethereum network")
    time.sleep(1)
else:
    print("The bot can't connect to the eth network")
    quit()
  
unitroller = keys["unitroller"]

abisite= keys["abi"]
with urllib.request.urlopen(abisite) as url:
    abi = json.loads(url.read())

contract = w3.eth.contract(address=unitroller, abi=abi)


apiKey = keys["pushbullet-api"]
p = PushBullet(apiKey)
devices = p.getDevices()

site= "https://api.compound.finance/api/v2/account?page_size=20"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib.request.Request(site, headers=hdr)
cj = CookieJar()
opener = build_opener(urllib.request.HTTPCookieProcessor(cj))



def getAccountLiquidity(addy):
    caddress = w3.toChecksumAddress(addy)
    result = contract.functions.getAccountLiquidity(caddress).call()
    if result[0] != 0:
        return "There is an error Whoops"
    elif result[1] != 0:
        return colored("SAFU", 'green')
    elif result[2] != 0:
        return colored("NOT SAFU", 'red', attrs=['bold'])

def token_symbol(tokenname):
        if tokenname == "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e":
            return "BAT"
        if tokenname == "0xf5dce57282a584d2746faf1593d3121fcac444dc":
            return "DAI"
        if tokenname == "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5":
            return "Ξ"
        if tokenname == "0x158079ee67fce2f58472a96584a73c7ab9ac95c1":
            return "REP"
        if tokenname == "0x39aa39c021dfbae8fac545936693ac917d5e7563":
            return "USDC"
        if tokenname == "0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407":
            return "ZRX"        
        if tokenname == "0xc11b1268c1a384e55c48c2391d8d480264a3a7f4":
            return "wBTC"
        
def api():
    global response
    try:
        req=urllib.request.Request(site, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'})
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        response = opener.open(req)
    except urllib.request.HTTPError as inst:
        output = format(inst)
        print(output)
        time.sleep(10)
        parse()
        
def parse():
    x = prettytable.PrettyTable()
    x.field_names = ["Address", "Health", "B. ETH","B.Tokens", "Supply", "Estimated profit", "On Chain Liquidity"]

    eth_price = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")

    api()

    obj = json.load(response)
    ethpr = json.load(eth_price)
    usdeth = float(ethpr["USD"])
    
    for account in obj["accounts"]:
        balance2 = ''
        balance3 = ''
        address = account["address"]
        onchainliquidity = getAccountLiquidity(address)
        health = float(account["health"]["value"])
        beth = float(account["total_borrow_value_in_eth"]["value"])
        beth_format = "{:.8f} Ξ".format(round(beth, 8)) + "\n" + colored("{:.3f}".format(round(usdeth*beth, 3)) + "$", 'green')
        estimated_p = "{:.3f}".format(((usdeth*beth)/2)*0.05) + "$"
        tokens = account["tokens"]
        for token in tokens:
            balance_borrow = token["borrow_balance_underlying"]["value"]
            balance_supply = token["supply_balance_underlying"]["value"]
            token_address = token["address"]
            if float(balance_supply) > 0:
                bresult_supply = "{:.8f} ".format(round(float(balance_supply), 8)) + token_symbol(token_address)
                balance3 += bresult_supply + "\n"
            if float(balance_borrow) > 0:
                bresult_borrow = "{:.8f} ".format(round(float(balance_borrow), 8)) + token_symbol(token_address)
                balance2 += bresult_borrow + "\n"
        x.add_row([address, round(health, 3), beth_format, balance2, balance3, colored(estimated_p, 'green', attrs=['bold']), onchainliquidity])
        if (((usdeth*beth)/2)*0.05 > 10) and (onchainliquidity == colored("NOT SAFU", 'red', attrs=['bold'])):
            p.pushNote(devices[0]["iden"], 'Urgent', 'EP ${0} \n{1} \nNOT SAFU \nSend {2}/2 \nReceive {3}'.format(estimated_p, address, balance2, balance3))

    print(x)
    time.sleep(20)

