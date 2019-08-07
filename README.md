# Compound Watcher
 A python bot that watches potential liquidations on Compound Finance and sends notifications through pushbullet

![Image of Bot](https://i.imgur.com/MN6e8m4.png)

## How it works
Compound Watcher uses Compound's official api from https://compound.finance to import the lists of addresses at risk of liquidation.
The bot shows further information about every address : 
* Health
* On Chain Liquidity *(Free https://infura.io api keys are required to interact with the smart contracts)*
* Supplied assets
* Borrowed assets 
* Estimated profit if liquidated

In the case an address can be liquidited, the bot sends a notification through pushbullet.

*A pushbullet free api is needed to run the bot*

## Install the bot
To install the bot, you need to have:
 * Python 3+
 * pip3

Start by installing the required python modules
> pip3 install web3

> pip3 install termcolor

> pip3 install git+https://github.com/Azelphur/pyPushBullet.git

Fill in your pushbullet and infura keys  and you're ready to start the bot!
> python3 app.py

To make the bot reboot automatically when it crashes due to api errors, use the forever.py script provided:
> chmod +x forever.py

> ./forever.py app.py
