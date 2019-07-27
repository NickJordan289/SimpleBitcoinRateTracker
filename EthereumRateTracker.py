import requests
import time
import json
from datetime import datetime
import calendar
from colorama import Fore, Style
import os
from win10toast import ToastNotifier
from pathlib import Path
from dotenv import load_dotenv

# load env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# One-time initialization
toaster = ToastNotifier()

# set globals
api_key = os.getenv('crypto_compare_key')

# ensures that balance is in env file
try:
	eth_bal = float(os.getenv('eth_bal'))
except Exception as e:
	with open('.env', 'w') as file:
		file.write('eth_bal=0.2')
	eth_bal = 0.2 # default value
		
# if value escapes out of these bounds a toast will display
threshold = (300, 400)

# toast display title
APP_TITLE = 'Ethereum Tracker'

def countdown(n):
    while n > 0:
		# zfill pads seconds and minutes with 0 if less than 10
		# carriage return is important so the price feed isnt blocked by each timer
        print(f'{str(n//60).zfill(2)}:{str(n%60).zfill(2)}s', end='\r')
        time.sleep(1)
        n -= 1

if __name__ == '__main__':
	os.system('color')
	old_price = None
	while True:
		q = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=AUD&api_key={api_key}').json()
		new_price = q['AUD']
		
		if old_price is not None:
			diff = new_price - old_price
			if diff > 0:
				diff = f'+{diff}'
				print(f'({Fore.GREEN}{diff}{Style.RESET_ALL}) {new_price} AUD - ${eth_bal*new_price}')
			else:	
				print(f'({Fore.RED}{diff}{Style.RESET_ALL}) {new_price} AUD - ${eth_bal*new_price}')
		else:
			print(f'${new_price} AUD - ${eth_bal*new_price}')
			
		if new_price <= threshold[0]:
			toaster.show_toast(f'{APP_TITLE} - Threshold Alert', f"Ethereum is now worth less than ${threshold[0]} AUD", threaded=True, icon_path=None, duration=3)
		elif new_price >= threshold[1]:
			toaster.show_toast(f'{APP_TITLE} - Threshold Alert', f"Ethereum is now worth more than ${threshold[1]} AUD", threaded=True, icon_path=None, duration=3)
		
		
		old_price = new_price
		
		#date_str = q['time']['updated']
		#date_obj = datetime.strptime(date_str, '%b %d, %Y %H:%M:%S UTC')
		#date_unix = calendar.timegm(date_obj.timetuple()) + 90
		#cur_date_unix = calendar.timegm(time.gmtime())
		
		#sleep_time = date_unix-cur_date_unix
		#print(f'Sleeping for {sleep_time}s')
		#if(sleep_time <= 0): # cant have negative values
		#	sleep_time = 0.1 # play it safe with small delay
		sleep_time = 61
		countdown(sleep_time)