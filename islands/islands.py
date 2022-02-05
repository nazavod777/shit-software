from requests import post
from web3.auto import w3
from eth_account.messages import encode_defunct
from json import loads
from random_username.generate import generate_username
from names import get_full_name
from loguru import logger
from sys import stderr
from threading import Thread
from gc import collect
from time import sleep
from ctypes import windll
from os import system

system("cls")
clear = lambda: system('cls')
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('Islands Auto Reger | by NAZAVOD')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

threadscount = int(input('How much threads?: '))

def createwallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)

def mainth():
	while True:
		try:
			walletdata = createwallet()
			r = post('https://server.islands.xyz/graphql', headers={'content-type': 'application/json', 'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'origin': 'https://islands.xyz', 'referer': 'https://islands.xyz/'}, json={"query":"\n    mutation CreateUserAndWallet($input: CreateUserAndWalletInput!) {\n  createUserAndWallet(input: $input) {\n    nonce\n  }\n}\n    ","variables":{"input":{"address": walletdata[0].lower(),"metadata":{"provider":"META_MASK","type":"MetaMask wallet"},"invitationId":"null"}}})
			if int(r.status_code) != 200:
				raise Exception(f'Wrong status code: {r.status_code}')

			r = post('https://server.islands.xyz/graphql', headers={'content-type': 'application/json', 'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'origin': 'https://islands.xyz', 'referer': 'https://islands.xyz/'}, json={"query":"\n    query getUserNonce($input: GetUserInput!) {\n  getUser(input: $input) {\n    nonce\n  }\n}\n    ","variables":{"input":{"address":walletdata[0].lower()}}})

			nonce = str(loads(r.text)['data']['getUser']['nonce'])

			signed_message =  w3.eth.account.sign_message(encode_defunct(text=f'I am signing my one-time nonce: {nonce}'), private_key=walletdata[1])
			sign = signed_message.signature.hex()

			r = post('https://server.islands.xyz/auth/login/web3', json={"address":walletdata[0].lower(),"signature":sign,"invitationId":None})
			if int(r.status_code) != 201:
				raise Exception(f'Wrong status code: {r.status_code}')

			accessToken = str(loads(r.text)['accessToken'])
			username = str(generate_username()[0].lower())
			full_name = str(get_full_name().lower())

			r = post('https://server.islands.xyz/graphql', headers={'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'content-type': 'application/json', 'origin': 'https://islands.xyz', 'referer': 'https://islands.xyz/',  'authorization': f'Bearer {accessToken}'}, json={"query":"\n    mutation UpdateUser($user: UpdateUserInput!) {\n  updateUser(input: $user) {\n    id\n    username\n  }\n}\n    ","variables":{"user":{"username":username,"fullName":full_name,"email":f"{username}@gmail.com"}}})
			if int(r.status_code) != 200:
				raise Exception(f'Wrong status code: {r.status_code}')

			r = post('https://server.islands.xyz/graphql', headers={'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'content-type': 'application/json', 'origin': 'https://islands.xyz', 'referer': 'https://islands.xyz/',  'authorization': f'Bearer {accessToken}'}, json={"query":"\n    query onboardingState {\n  getUserMe {\n    profile {\n      onboardingState\n    }\n  }\n}\n    "})
			if int(r.status_code) != 200:
				raise Exception(f'Wrong status code: {r.status_code}')

			r = post('https://server.islands.xyz/graphql', headers={'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'content-type': 'application/json', 'origin': 'https://islands.xyz', 'referer': 'https://islands.xyz/',  'authorization': f'Bearer {accessToken}'}, json={"query":"\n    query Me {\n  getUserMe {\n    avatar {\n      id\n      mimeType\n      serveUrl\n      type\n      metadata {\n        ...AvatarMetadata\n      }\n    }\n    coverPhoto {\n      mimeType\n      serveUrl\n    }\n    email\n    fullName\n    id\n    profile {\n      notificationsEnabled\n      onboardingState\n      description\n    }\n    username\n    wallets {\n      address\n    }\n  }\n}\n    \n    fragment AvatarMetadata on AssetMetadata {\n  nft\n  backgroundColor\n  onboardingAvatar\n}\n    "})
			if int(r.status_code) != 200:
				raise Exception(f'Wrong status code: {r.status_code}')

			with open('wallets.txt', 'a') as file:
				file.write(f'{walletdata[0]}:{walletdata[1]}\n')
		except Exception as error:
			logger.error(f'Error: {str(error)}')
			continue
		else:
			logger.success(f'Wallet {walletdata[0]} successfully registered')

def cleaner():
	while True:
		sleep(60)
		clear()
		collect()

clear()
for _ in range(threadscount):
	Thread(target=mainth).start()

Thread(target=cleaner, daemon=True).start()