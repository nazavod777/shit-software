import cfscrape
import requests
from fake_useragent import UserAgent
from loguru import logger
from sys import stderr
from time import sleep
from gc import collect
from urllib3 import disable_warnings
from os import system
from ctypes import windll
from json import loads
from random import randint
from threading import Thread

disable_warnings()
system("cls")
clear = lambda: system('cls')
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('FintMoney Auto Reger | by NAZAVOD')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

reflink = str(input('Введите вашу реферальную ссылку: '))
refcode = reflink.split('?code=')[-1]
useproxy = str(input('Использовать TorProxy? (y/N): '))
threadscount = int(input('Количество потоков: '))

scraper = cfscrape.create_scraper()
session = requests.Session()
session.headers.update({'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'authorization': 'Bearer', 'content-type': 'application/json', 'origin': reflink, 'referer': reflink})

def genproxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies

def mainth():
	while True:
		try:
			if useproxy in ('y', 'Y'):
				proxies = genproxy()
				session.proxies.update(proxies)
			session.headers.update({'user-agent': UserAgent().random})
			r = scraper.post('https://api.temprmail.com/v1/emails')
			email = loads(r.text)['email']
			checkmailsurl = loads(r.text)['emails_json_url']
			logger.info(f'Email {email} успешно зарегистрирован')

			randnum = ''.join(["%s" % randint(0, 9) for num in range(0, 9)])

			r = session.post('https://app.stg.eugenix.io/auth-service/api/v1/auth/web/login-multi-channel', json={"phone_number":f"+79{str(randnum)}","email_address":email})

			try:
				fint_id = loads(r.text)['id']
			except:
				if 'Invalid phone number' in r.text:
					raise Exception('invalid_phone')
				else:
					raise Exception('error_when_register')
			else:
				logger.success(f'Аккаунт {email} начал процесс регистрации, жду OTP-код')

			for i in range(13):
				r = scraper.get(checkmailsurl)
				if 'Confirm your email address' in r.text:
					msgid = loads(r.text)[0]['hash_id']
					logger.success(f'Код успешно получен для {email}')
					break
				else:
					if i == 12:
						raise Exception('email_timeout')
					else:
						sleep(5)

			r = scraper.get(f'https://tempremail-assets.s3.us-east-1.amazonaws.com/emails/{msgid}.json')
			otp_code = r.text.split('<span style=\\"mso-text-raise: 16px;\\">')[-1].split('<\\')[0]

			r = session.post('https://app.stg.eugenix.io/auth-service/api/v1/auth/web/verify?is_waitlist=true', json={"id":fint_id,"otp":otp_code})
			if r.status_code != 200:
				raise Exception('error_resp_code_otp')

			r = session.post('https://app.stg.eugenix.io/referral-service/api/v1/web', json={"waitlist_campaign_id":"5fa4589d-a0e3-4e74-beb7-5211253a386c","referral_campaign_id":"9a289141-93be-453e-bb45-721e8efdb71b","referral_code":refcode,"email_address":email,"preference":"USDT"})
			if r.status_code != 200:
				raise Exception('error_resp_code_final')
		except Exception as error:
			if str(error) == 'invalid_phone':
				logger.error(f'Ошибка во время генерации номера телефона {email}')
			elif str(error) == 'error_when_register':
				logger.error(f'Неизестная ошибка во время регистрации номера {email}')
			elif str(error) == 'email_timeout':
				logger.error(f'Не удалось дождаться кода на почту {email}')
			elif str(error) == 'error_resp_code_otp':
				logger.error(f'Ошибка при вводе OTP-кода для {email}')
			elif str(error) == 'error_resp_code_final':
				logger.error(f'Ошибка во время завершения регистрации {email}')
			else:
				logger.error(f'Неизвестная ошибка: {str(error)}')
		else:
			logger.success(f'Аккаунт {email} успешно зарегистрирован')

def cleaner():
	while True:
		sleep(60)
		clear()
		collect()

clear()

for _ in range(threadscount):
	d = Thread(target=mainth)
	d.start()

t = Thread(target=cleaner, daemon=True)
t.start()