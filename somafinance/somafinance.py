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
from gc import collect
from random import randint
from threading import Thread
from names import get_first_name, get_last_name

disable_warnings()
system("cls")
def clear(): return system('cls')
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('SomaFinance Auto Reger | by NAZAVOD')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

ref_link = str(input('Ref link: '))
ref_id = ref_link.split('referral=')[-1].split('&')[0]
use_proxy = str(input('Use Tor Proxy? (y/N): '))
threads = int(input('Threads: '))

def genproxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies

def mainth():
	while True:
		try:
			scraper = cfscrape.create_scraper()
			session = requests.Session()
			session.headers.update({'user-agent': random_useragent(), 'Accept': '*/*', 'Accept-Language': 'ru,en;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://www.soma.finance', 'Referer': 'https://www.soma.finance/'})
			if use_proxy in ('y', 'Y'):
				session.proxies.update(genproxy())

			r = scraper.post('https://api.temprmail.com/v1/emails')
			email = loads(r.text)['email']
			checkmailsurl = loads(r.text)['emails_json_url']
			logger.info(f'Email {email} successfully received')

			r = session.get(ref_link)
			public_token = r.text.split('(document,"script","vrlps-js","')[-1].split('"')[0]

			r = session.post('https://app.viral-loops.com/api/v2/events', json={"params":{"event":"registration","user":{"firstname":get_first_name(),"lastname":get_last_name(),"email":email,"extraData":{},"consents":{},"refSource":"copy"},"referrer":{"referralCode":ref_id},"refSource":"copy","acquiredFrom":"popup"},"publicToken":public_token})

			if int(r.status_code) != 200:
				raise Exception('wrong_code')

			for i in range(13):
				r = scraper.get(checkmailsurl)
				if 'Verify your email address' in r.text:
					msgid = loads(r.text)[0]['hash_id']
					logger.success(f'The code was successfully received for {email}')
					break
				else:
					if i == 12:
						raise Exception('email_timeout')
					else:
						sleep(5)

			r = scraper.get(f'https://tempremail-assets.s3.us-east-1.amazonaws.com/emails/{msgid}.json')
			verify_url = r.text.split(';\\"><a href=\\"')[-1].split('\\" target=\\"')[0].replace('\\/', '/')

			r = session.get(verify_url)
			if int(r.status_code) != 200:
				raise Exception('wrong_code')
		except Exception as error:
			if str(error) == 'wrong_code':
				logger.error(f'Error, response: {str(r.text)}')
			elif str(error) == 'email_timeout':
				logger.error(f'Error, email timeout')
			else:
				if '<pre>Internal Server Error</pre>' in str(r.text) or '<title>Access denied | app.viral-loops.com used Cloudflare to restrict access</title>' in str(r.text) or '<title>Attention Required! | Cloudflare</title>' in str(r.text):
					logger.error('CloudFlare')
				else:
					logger.error(f'Unexpected error: {str(error)}, response: {str(r.text)}')
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
