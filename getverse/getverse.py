from pyuseragents import random as random_useragent
from requests import Session
from random import choice, randint
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
windll.kernel32.SetConsoleTitleW('GetVerse Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


threads = int(input('Threads: '))
use_proxy = str(input('Использовать Proxy? (y/N): '))


if use_proxy in ('y', 'Y'):
    proxy_source = int(input('Откуда брать прокси? (1 - из текствого файла; 2 - использовать tor proxy): '))


    if proxy_source == 1:
        proxy_type = str(input('Введите тип прокси (http; https; socks4; socks5): '))
        proxy_folder = str(input('Перетяните TXT файл с прокси: '))


mail_option = int(input('Выберите тип загрузки почт (1 - генерация на основе введенной gmail почты; 2 - из текстового документа): '))


if mail_option == 1:
    user_mail = str(input('Введите вашу Gmail почту: '))
else:
    emails_folder = str(input('Перетяните TXT файл с почтами: '))


    with open (emails_folder, 'r') as file:
        emails_list = [row.strip() for row in file]


def random_mail_from_user(user_mail):
	randstring = ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' if i != 15 else 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(15)])
	email = user_mail.split('@')[0]+'+'+randstring+'@'+user_mail.split('@')[1]
	return (email)


def random_proxy(proxy_folder):
    with open(proxy_folder, 'r') as file:
        proxies = file.readlines()
    

    return(choice(proxies))


def random_tor_proxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies


def cleaner():
	while True:
		sleep(60)
		clear()
		collect()


def mainth(email):
    try:
        if mail_option == 1:
            email = random_mail_from_user(email)

        session = Session()
        session.headers.update({'user-agent': random_useragent(), 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'content-type' : 'application/json', 'origin': 'https://www.getverse.com', 'referer': 'https://www.getverse.com/'})


        if use_proxy in ('y', 'Y'):
            if proxy_source == 1:
                proxy_str = random_proxy(proxy_folder)
                session.proxies.update({'http': f'{proxy_type}://{proxy_str}', 'https': f'{proxy_type}://{proxy_str}'})
            else:
                session.proxies.update(random_tor_proxy())


        r = session.post('https://activecampaign.prod.cloud.bitcoin.com/', json = {"segment":"149","email":email})


        if str(r.text) != '{"success":1}':
            raise Exception('wrong_response')


    except Exception as error:
        logger.error(f'Непредвиденная ошибка: {str(error)}, ответ: {str(r.text)}')
    else:
        with open ('registered.txt', 'a') as file:
            file.write(f'{email}\n')
        

        logger.success(f'Email {str(email)} успешно зарегистрирован')


if __name__ == '__main__':
    clear()
    
    if mail_option == 1:
        Thread(target=cleaner).start
        while True:
            if active_count() < threads:
                Thread(target=mainth, args = (user_mail,)).start()
    else:
        while emails_list:
            if active_count() < threads:
                Thread(target=mainth, args=(emails_list.pop(0),)).start()

    while active_count() != 1:
        pass

    
    logger.success('Работа успешно завершена!')
    print('\nPress Any Key To Exit..')
    getch()
    exit()
