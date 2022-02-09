import requests
import cfscrape
from pyuseragents import random as random_useragent
from urllib3 import disable_warnings
from ctypes import windll
from loguru import logger
from sys import stderr
from json import loads
from os import system
from time import sleep
from web3.auto import w3
from gc import collect
from random import randint
from threading import Thread

disable_warnings()
system("cls")
def clear(): return system('cls')
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('HarmonyLauncher Auto Reger | by NAZAVOD')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

ref_link = str(input('Ref link: '))
ref_id = ref_link.split('?ref=')[-1]
use_proxy = str(input('Use Tor Proxy? (y/N): '))
threads = int(input('Threads: '))

def createwallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)

def genproxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies

def mainth():
	while True:
		try:
			wallet_data = createwallet()
			scraper = cfscrape.create_scraper()
			session = requests.Session()
			session.headers.update({'user-agent': random_useragent(), 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'Content-Type': 'application/json', 'Origin': 'https://referral.harmonylauncher.io', 'Referer': 'https://referral.harmonylauncher.io/'})
			if use_proxy in ('y', 'Y'):
				session.proxies.update(genproxy())

			r = scraper.post('https://api.temprmail.com/v1/emails')
			email = loads(r.text)['email']
			checkmailsurl = loads(r.text)['emails_json_url']
			logger.info(f'Email {email} successfully received')

			r = session.post('https://api.harmonylauncher.io/otp', json={"email":email})
			if loads(r.text)['success'] != True:
				raise Exception('wrong_code')
			else:
				logger.info(f'Successfully sent OTP to {email}, waiting')

			login_id = loads(r.text)['id']

			for i in range(13):
				r = scraper.get(checkmailsurl)
				if 'Login OTP' in r.text:
					msgid = loads(r.text)[0]['hash_id']
					logger.success(f'The code was successfully received for {email}')
					break
				else:
					if i == 12:
						raise Exception('email_timeout')
					else:
						sleep(5)

			r = scraper.get(f'https://tempremail-assets.s3.us-east-1.amazonaws.com/emails/{msgid}.json')
			otp_code = str(loads(r.text)['message'].split('Your OTP for login: ')[-1].split('.')[0])

			r = session.post('https://api.harmonylauncher.io/login', json={"id":login_id,"otp":otp_code,"projectCode":"harmony-launcher","walletAddress":wallet_data[0],"referrerCode":ref_id})
			if loads(r.text)['success'] != True:
				raise Exception('wrong_code')
		except Exception as error:
			if str(error) == 'wrong_code':
				logger.error(f'Error, response: {str(r.text)}')
			elif str(error) == 'email_timeout':
				logger.error(f'Error, email timeout')
			else:
				logger.error(f'Unexpected error: {str(error)} response: {str(r.text)}')
		else:
			logger.success(f'Account {email} successfully registered')

def cleaner():
	while True:
		sleep(60)
		clear()
		collect()

clear()
for _ in range(threads):
	Thread(target=mainth).start()

Thread(target=cleaner, daemon=True).start()