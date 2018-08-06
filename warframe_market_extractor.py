
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import time
import json

base_url = 'https://warframe.market/items/'
targets = [] # Items to search for

# File for items to search
with open('input.csv', 'r') as file:
    for line in file:
        targets.append(line.lower().rstrip()) # rstrip removes the newline stored in the file
    file.close()

print(str(len(targets)) + ' entries')
start_time = time.time() # Start of stopwatch
for index, target in enumerate(targets): # Loop through targets keeping track of index
    try:
        # Make a http request to our target passing in our crawlers agent identifier
        target_url = base_url + target
        q = Request(target_url)
        q.add_header('User-Agent', 'Market Price Crawler')
        url = urlopen(q)
        html_doc = url.read()

        # Parse the html with BeautifulSoup
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Find the application-state json from the document and get its contents
        data = soup.find('script', id='application-state').contents

        # File for writing our string json into
        # '[' and ']' on the ends because it wouldn't work without it
        with open('data.json', 'w') as file:
            file.write('[')
            for a in data:
                file.write(a)
            file.write(']')
            file.close()

        # File for retrieving json data
        # Reads json dict into data var
        with open('data.json', 'r') as file:
            data = json.load(file)[0]
            file.close()

        # Loop through and store all plat values in arrays
        buy_orders = []
        sell_orders = []
        try:
            for order in data['payload']['orders']: # Loop through sell and buy orders
                if(order['user']['status'] == 'ingame'): # Only go through orders that have online players
                    if(order['order_type'] == 'buy'): # Seperate buy orders and sell orders into their own arrays
                        buy_orders.append(order['platinum']) # Add to buy order storage
                    else:
                        sell_orders.append(order['platinum']) # Add to sell order storage
        except Exception as e:
            print(str(index) + ': ' + str(e))
         
        buy_orders.sort(reverse=True)   # Put highest plat value on top
        sell_orders.sort()              # Put lowest plat value on top

        # File for plat value outputs
        # Appends results into our output.csv
        with open('output.csv', 'a') as file:
            file.write(target + ',') # Item name
            if(len(buy_orders) > 0):
                file.write(str(buy_orders[0]) + ',') # Highest buy value
            if(len(sell_orders) > 0):
                file.write(str(sell_orders[0])) # Lowest sell value
            file.write('\n')
            file.close()
        
        if(index < len(targets) - 1): # If there are more entries to go through
            time.sleep(3) # Wait for seconds before next search (Feel free to decrease)

        # print(url.headers)
    except HTTPError as e:
        if(e.code == 429):
            print(target + ' wants you to slow down')
            print('Waiting for ' + str(e.headers).split()[6] + ' seconds before our next request')
            time.sleep(int(str(e.headers).split()[6]) + 3)  # +3 to slowdown after too many requests
        else:
            print(e.code)

# Print results of stopwatch
print('Took ' + str((time.time() - start_time) / 60) + ' minutes')
print(str((time.time() - start_time) / len(targets)) + ' seconds per entry')
