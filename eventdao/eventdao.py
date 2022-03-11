from requests import Session
from pyuseragents import random as random_useragent
from random import randint
from web3.auto import w3
from json import loads
from time import sleep
from msvcrt import getch
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr
from threading import Thread
from names import get_first_name


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('EventDAO Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


threads = int(input('Threads: '))
use_proxy = str(input('Use Tor proxies? (y/N): '))
ref_link = 'https://wait.eventdao.io/?hdfhdfh24ec4'
ref_id = ref_link.split('eventdao.io/?')[-1]


def gen_proxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return proxies

def create_wallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)


def mainth():
    while True:
        try:
            wallet_data = create_wallet()
            session = Session()
            session.headers.update({'user-agent': random_useragent(), 'Accept': '*/*', 'Accept-Language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'Origin': 'https://wait.eventdao.io', 'Referer': 'https://wait.eventdao.io/'})
            

            if use_proxy in ('y', 'Y'):
                session.proxies.update(gen_proxy())


            rand_nums = []


            for _ in range(4):
                rand_nums.append(randint(0,1))


            twitter_username = get_first_name()
            discord_username = get_first_name()


            if rand_nums[0] == 1:
                twitter_username = str(randint(0,1000))+twitter_username

            if rand_nums[1] == 1:
                twitter_username = twitter_username+str(randint(0,1000))


            if rand_nums[2] == 1:
                discord_username = str(randint(0,1000))+discord_username

            if rand_nums[3] == 1:
                discord_username = discord_username+str(randint(0,1000))


            r = session.post(f'https://www.eventdao.io/php_helpers/create_payment.php?WalletAddress={wallet_data[0]}&TwitterUserName={twitter_username}&DiscorduserName={discord_username}&Referer={ref_id}')


            if f'True#{twitter_username}' not in r.text:
                raise Exception('wrong_response')


        except Exception as error:
            if str(error) == 'wrong_response' or 'Expecting value: line 1 column 1 (char 0)' in r.text:
                logger.error(f'Wrong response, code: {str(r.status_code)}, response: {str(r.text)}')
            elif str(error) == 'error_generate_username':
                logger.error(f'Error when generate username, status code: {str(r.status_code)}')
            else:
                logger.error(f'Unexcepted error: {str(error)}')
        else:
            with open('accounts.txt', 'a') as file:
                file.write(f'{wallet_data[0]}:{wallet_data[1]}:{twitter_username}:{discord_username}\n')
            logger.success(f'Address {wallet_data[0]} successfully registered')


if __name__ == '__main__':
    clear()
    for _ in range(threads):
        Thread(target=mainth).start()