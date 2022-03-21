from pyuseragents import random as random_useragent
from requests import Session
from web3.auto import w3
from time import sleep
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr
from threading import Thread
from gc import collect
from random import randint


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('Carlee Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


threads = int(input('Threads: '))
use_proxy = str(input('Use Tor proxies? (y/N): '))


def create_wallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)


def random_tor_proxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies


def cleaner():
	while True:
		sleep(180)
		clear()
		collect()


def create_ref(ref_id):
	while True:
		try:
			wallet_data = create_wallet()
			ref_session = Session()

			if use_proxy in ('y', 'Y'):
				ref_session.proxies.update(random_tor_proxy())

			ref_session.headers.update({'user-agent': random_useragent(), 'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://www.carlee.info', 'referer': f'https://www.carlee.info/?ref={ref_id}'})

			r = ref_session.post('https://www.carlee.info/register.php', data = f'email={wallet_data[0]}&ref={ref_id}')

			if str(r.text) != 'true':
				raise Exception('wrong_answer')
		
		except Exception as error:
			logger.error(f'Ошибка при регистрации реферального аккаунта: {str(error)}, ответ: {str(r.text)}')

		else:
			break



def create_main():
	while True:
		try:
			main_session = Session()
			
			if use_proxy in ('y', 'Y'):
				main_session.proxies.update(random_tor_proxy())

			main_session.headers.update({'user-agent': random_useragent(), 'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://www.carlee.info', 'referer': 'https://www.carlee.info/'})
			wallet_data = create_wallet()

			r = main_session.post('https://www.carlee.info/register.php', data = f'email={wallet_data[0]}&ref=')

			if str(r.text) != 'true':
				raise Exception('wrong_response')
			else:
				logger.success(f'Основной аккаунт {wallet_data[0]} успешно зарегистрирован')

				for _ in range(35):
					create_ref(wallet_data[0])
				
				with open('accounts.txt', 'a') as file:
					file.write(f'{wallet_data[0]}:{wallet_data[1]}\n')

				logger.success(f'На основной аккаунт {wallet_data[0]} успешно зарегистрировано 35 рефералов')

		except Exception as error:
			logger.error(f'Ошибка при регистрации основного аккаунта: {str(error)}, ответ: {str(r.text)}')

		else:
			pass

if __name__ == '__main__':

	clear()
	Thread(target=cleaner).start()
	
	for _ in range(threads):
		Thread(target=create_main).start()