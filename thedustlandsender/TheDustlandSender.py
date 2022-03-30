from web3 import Web3
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from requests import get
from json import loads
from threading import Thread, active_count
from msvcrt import getch


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('TheDustland Auto Sender | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')

addresses_folder = str(input('TXT with Accounts (address:privatekey): '))
main_address = str(input('Main Address: '))
threads = int(input('Threads: '))


with open (addresses_folder, 'r') as file:
	addresses = [row.strip() for row in file]


def send_token(main_address, wallet_data):

	for _ in range(3):

		while True:
			try:
				r = get('https://gpoly.blockscan.com/gasapi.ashx?apikey=key&method=pendingpooltxgweidata')
				gas_price = loads(r.text)['result']['fastgaspricegwei'] + 30
			except Exception as error:
				logger.error(f'Ошибка при получении газа: {str(error)}')

			else:
				break


		try:
			address = (web3.toChecksumAddress(wallet_data.split(':')[0].lower()))
			private_key = wallet_data.split(':')[-1]

			balanceOf = contract.functions.balanceOf(address, 1).call()

			if balanceOf > 0:

				transaction = contract.functions.safeTransferFrom(address, main_address, 1, balanceOf, '').buildTransaction({
					'gas': 100000,
					'gasPrice': web3.toWei(gas_price, 'gwei'),
					'from': address,
					'nonce': web3.eth.getTransactionCount(address)
					})


				signed_txn = web3.eth.account.signTransaction(transaction, private_key=private_key)

				tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
				logger.info(f'[{address}] TX id: '+web3.toHex(tx_hash))

		except Exception as error:
			logger.error(f'[{address}] Неизвестная ошибка: {str(error)}')

		else:
			return True

	with open('errors.txt', 'a') as file:
		file.write(f'{wallet_data}\n')
	




if __name__ == '__main__':

	clear()
	web3 = Web3(Web3.HTTPProvider('https://matic-mainnet.chainstacklabs.com'))
	abi = open('ABI','r').read().replace('\n','')
	contract = web3.eth.contract(address=web3.toChecksumAddress('0xC65fD3945e26c15E03176810d35506956B036f39'), abi=abi)

	while addresses:
		if active_count() < threads:

			Thread(target=send_token, args = (web3.toChecksumAddress(main_address.lower()),  addresses.pop(0), )).start()

	while active_count() != 1:
		pass


	logger.success('Work completed successfully')
	print('\nPress Any Key To Exit...')
	getch()
	exit()