from requests import post
from web3.auto import w3
from threading import Thread
from ctypes import windll
from sys import stderr
from loguru import logger
from urllib3 import disable_warnings
from random import randint
from time import sleep
from gc import collect
from os import system

disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
clear = lambda: system('cls')
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('TheDustland Auto Reger | by NAZAVOD')

useproxy = str(input('Use tor proxy? (y/N): '))
threads = int(input('Threads: '))

def genproxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies

def createwallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)

def mainth():
	while True:
		try:
			walletdata = createwallet()
			if useproxy in ('y', 'Y'):
				r = post('https://hn0tygvxl1.execute-api.ap-southeast-1.amazonaws.com/dev-v1/users/wallet/connect', json={"chain_id":"0x89","wallet_id":walletdata[0]}, proxies=genproxy(), verify=False)
			else:
				r = post('https://hn0tygvxl1.execute-api.ap-southeast-1.amazonaws.com/dev-v1/users/wallet/connect', json={"chain_id":"0x89","wallet_id":walletdata[0]}, verify=False)
			if r.text == '{"status_code":200}':
				with open('wallets.txt', 'a') as file:
					file.write(f'{walletdata[0]}:{walletdata[1]}\n')
				logger.success(f'Wallet {walletdata[0]} successfully registered')
		except Exception as error:
			logger.error(f'Error: {str(error)}')

def cleaner():
	while True:
		sleep(60)
		clear()
		collect()

clear()
for _ in range(threads):
	Thread(target=mainth).start()

Thread(target=cleaner, daemon=True).start()
