from pyuseragents import random as random_useragent
from requests import Session
from urllib.parse import quote
from random import choice
from threading import Thread, active_count
from time import sleep
from msvcrt import getch
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr
from gc import collect
from sys import exit


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('Alice Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


threads = int(input('Threads: '))
use_proxy = str(input('Use Proxy? (y/N): '))


if use_proxy in ('y', 'Y'):
	proxy_type = str(input('Enter proxy type (http; https; socks4; socks5): '))
	proxy_folder = str(input('Drop TXT file with proxies (user:pass@ip:port // ip:port): '))

mail_folder = str(input('Drop TXT with mails: '))

with open(mail_folder, 'r') as file:
	emails_list = [row.strip() for row in file]


def random_proxy(proxy_folder):
    with open(proxy_folder, 'r') as file:
        proxies = file.readlines()
    

    return(choice(proxies))


def mainth(email):
	try:
		for _ in range(3):

			session = Session()
			session.headers.update({'user-agent': random_useragent(), 'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'referer': 'https://www.alice.co/'})

			if use_proxy in ('y', 'Y'):
				proxy_str = random_proxy(proxy_folder)
				session.proxies.update({'http': f'{proxy_type}://{proxy_str}', 'https': f'{proxy_type}://{proxy_str}'})

			r = session.get(f'https://alice.us1.list-manage.com/subscribe/post-json?u=bc7fe71d0534010272c9bdd3a&amp;id=748f6d5b35&EMAIL={quote(email)}&c=__jp0')

			if 'Thank you for reserving your spot! Stay tuned for email updates.' not in str(r.text):
				raise Exception('wrong_answer')

	except Exception as error:

		if str(error) == 'wrong_answer':
			logger.error(f'Unexpected error: {str(error)}, response: {str(r.text)}')
		else:
			logger.error(f'Unexpected error: {str(error)}')
	
	else:
		with open('registered.txt', 'a') as file:
			file.write(f'{str(email)}\n')

		logger.success(f'{str(email)} has been successfully registered')


def cleaner():
	while True:
		sleep(60)
		clear()
		collect()


if __name__ == '__main__':
	clear()

	while emails_list:
		if active_count() < threads:
			Thread(target=mainth, args=(emails_list.pop(0),)).start()

	while active_count() != 1:
		pass

	
	logger.success('The work has been completed successfully!')
	print('\nPress Any Key To Exit..')
	getch()
	exit()