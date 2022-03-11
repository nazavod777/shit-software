from requests import get
from pyuseragents import random as random_useragent
from json import loads
from loguru import logger
from sys import stderr
from urllib3 import disable_warnings
from ctypes import windll
from os import system
from threading import Thread, active_count
from msvcrt import getch
from sys import exit


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('TheDustland Check Results | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


accounts_folder = str(input('Drop TXT with format (wallet:privatekey): '))
threads = int(input('Threads: '))


with open(accounts_folder, 'r') as file:
    wallet_datas = [row.strip() for row in file]


def mainth(wallet_data):
    try:
        address = wallet_data.split(':')[0]
        r = get(f'https://hn0tygvxl1.execute-api.ap-southeast-1.amazonaws.com/prod-v1/users/wallet/whitelisted/{address}', headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'origin': 'https://www.thedustland.com', 'referer': 'https://www.thedustland.com/', 'user-agent': random_useragent(), 'x-api-key': 'CNyRtS5eiL8CkQsWz0mvz59aZfbNT62R63J8fll8'})
        

        if loads(r.text)['body']['whitelisted'] == False:
            raise Exception('not_whitelisted')
    except Exception as error:
        if str(error) == 'not_whitelisted':
            logger.error(f'{address} is not whitelisted')
        elif 'body' in str(error):
            mainth(wallet_data)
        else:
            logger.error(f'Unexpected error: {str(error)}')

    else:
        logger.success(f'{address} is whitelisted!')
        with open('whitelisted.txt', 'a') as file:
            file.write(f'{wallet_data}\n')

if __name__ == '__main__':
    clear()
    while wallet_datas:
        if active_count() <= threads:
            wallet_data = wallet_datas.pop(0)
            Thread(target=mainth, args=(wallet_data,)).start()


while active_count() != 1:
    pass


logger.success('Work completed successfully')
print('\nНажмите любую клавишу для выхода...')
getch()
exit()