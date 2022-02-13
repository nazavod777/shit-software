import threading
from threading import Thread
from web3 import Web3
from eth_account.messages import encode_defunct
from eth_account import Account
from loguru import logger
from sys import stderr
from random import choice
from os import system
from ctypes import windll
from time import time, sleep
from datetime import timedelta
from msvcrt import getch
from requests import get
from os import system
from ctypes import windll
from sys import stderr
from urllib3 import disable_warnings

disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
clear = lambda: system('cls')
clear()
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('MetaPass Sender | by NAZAVOD')
lock = threading.Lock() 

wallets_folder = str(input('Drop your txt with privatekeys: '))
with open(wallets_folder, 'r') as file:
	wallets = [row.strip() for row in file]
gas_price = int(input('Gas price: '))
selected_option = int(input('Enter your choice (1 - claim nft; 2 - send nft to main wallet): '))
if selected_option == 2:
	main_wallet = str(input('Main address: '))
threads = int(input('Threads: '))
wait_tx_result = str(input('Wait TX result? (y/N): '))

def claim_nft(privatekey, address, nonce):
	try:
		transaction = contract.functions.claim(address, 2, 1, [web3.toBytes(hexstr='0x0000000000000000000000000000000000000000000000000000000000000000')]).buildTransaction({
			'gas': 119518,
			'gasPrice': web3.toWei(str(gas_price), 'gwei'),
			'from': address,
			'nonce': nonce
			})

		signed_tx = web3.eth.account.signTransaction(transaction, private_key=privatekey)

		tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
		logger.info('TX id: '+web3.toHex(tx_hash))
		if wait_tx_result in ('y', 'Y'):
			txstatus = web3.eth.waitForTransactionReceipt(tx_hash).status
			if txstatus == 1:
				logger.success(f'TX status: {txstatus}')
			else:
				logger.error(f'TX status: {txstatus}')
	except Exception as error:
		if 'Too Many Requests for url' in str(error):
			mainth(privatekey)
		else:
			logger.error(f'Error: {str(error)}')
	else:
		return True

def transfer_nft(privatekey, main_wallet, address, nonce):
	try:
		transaction = contract.functions.safeTransferFrom(address, main_wallet, 2, 1, web3.toBytes(hexstr='')).buildTransaction({
					'gas': 66685,
					'gasPrice': web3.toWei(gas_price, 'gwei'),
					'from': address,
					'nonce': nonce
					})

		signed_tx = web3.eth.account.signTransaction(transaction, private_key=privatekey)

		tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
		logger.info('TX id: '+web3.toHex(tx_hash))
		if wait_tx_result in ('y', 'Y'):
			txstatus = web3.eth.waitForTransactionReceipt(tx_hash).status
			if txstatus == 1:
				logger.success(f'TX status: {txstatus}')
			else:
				logger.error(f'TX status: {txstatus}')
	except Exception as error:
		if 'Too Many Requests for url' in str(error):
			mainth(privatekey, main_wallet)
		else:
			logger.error(f'Error: {str(error)}')
	else:
		return True

if __name__ == '__main__':
	clear()
	abi = open('ABI.json','r').read().replace('\n','')
	web3 = Web3(Web3.HTTPProvider('https://matic-mainnet.chainstacklabs.com'))
	contract = web3.eth.contract(address=web3.toChecksumAddress('0x4867f7ACb9078d2b462442c5ca3DBa01456844B5'), abi=abi)
	while wallets:
		if threading.active_count() <= threads:
			for _ in range(threads):
				privatekey = wallets.pop(0)
				address = web3.eth.account.privateKeyToAccount(privatekey).address
				nonce = web3.eth.get_transaction_count(address)
				if selected_option == 1:
					Thread(target=claim_nft, args=(privatekey, address, nonce,)).start()
				else:
					Thread(target=transfer_nft, args=(privatekey, main_wallet, address, nonce,)).start()
