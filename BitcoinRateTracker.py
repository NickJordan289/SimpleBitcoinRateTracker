import requests
import time
import json
from datetime import datetime
import calendar
from colorama import Fore, Style
import os
from win10toast import ToastNotifier

# One-time initialization
toaster = ToastNotifier()

my_bal = 0.00169907
threshold = (14000, 15000)
APP_TITLE = 'Bitcoin Tracker'

if __name__ == '__main__':
	os.system('color')
	old_price = None
	while True:
		q = requests.get('https://api.coindesk.com/v1/bpi/currentprice/aud.json').json()
		new_price = q['bpi']['AUD']['rate_float']
		
		if old_price is not None:
			diff = new_price - old_price
			if diff > 0:
				diff = f'+{diff}'
				print(f'({Fore.GREEN}{diff}{Style.RESET_ALL}) {new_price} AUD - ${my_bal*new_price}')
			else:	
				print(f'({Fore.RED}{diff}{Style.RESET_ALL}) {new_price} AUD - ${my_bal*new_price}')
		else:
			print(f'${new_price} AUD - ${my_bal*new_price}')
			
		if new_price <= threshold[0]:
			toaster.show_toast(f'{APP_TITLE} - Threshold Alert', "Bitcoin is now worth less than {threshold[0]} AUD", threaded=True, icon_path=None, duration=3)
		elif new_price >= threshold[1]:
			toaster.show_toast(f'{APP_TITLE} - Threshold Alert', "Bitcoin is now worth more than {threshold[1]} AUD", threaded=True, icon_path=None, duration=3)
		
		
		old_price = new_price
		
		date_str = q['time']['updated']
		date_obj = datetime.strptime(date_str, '%b %d, %Y %H:%M:%S UTC')
		date_unix = calendar.timegm(date_obj.timetuple()) + 90
		cur_date_unix = calendar.timegm(time.gmtime())
		
		sleep_time = date_unix-cur_date_unix
		#print(f'Sleeping for {sleep_time}s')
		if(sleep_time <= 0):
			sleep_time = 1
		time.sleep(sleep_time)