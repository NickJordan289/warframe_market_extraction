from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import time
import json

base_url = "https://warframe.market/items/"
targets = []

# File for urls to search
with open("input.csv", "r") as file:
    for line in file:
        targets.append(line.lower().rstrip()) # rstrip removes the newline stored in the file
    file.close()

print(str(len(targets)) + " entries")
start_time = time.time() # start of timer
for index, target in enumerate(targets): # loop through targets keeping track of index
    try:
        # Make a http request to our target passing in our crawlers agent identifier
        target_url = base_url + target
        q = Request(target_url)
        q.add_header('User-Agent', 'Market Price Crawler')
        url = urlopen(q)
        html_doc = url.read()

        # if the opening and reading is successful
        #print("We're in")

        # parse the html with BeautifulSoup
        soup = BeautifulSoup(html_doc, 'html.parser')
        # find the application-state json from the document and get its contents
        data = soup.find("script", id="application-state").contents

        # File for writing our string json into
        # '[' and ']' on the ends because it wouldn't work without it
        with open('data.json', 'w') as file:
            file.write("[")
            for a in data:
                file.write(a)
            file.write("]")
            file.close()

        # File for retrieving json data
        # reads json dict into data var
        with open('data.json', 'r') as file:
            data = json.load(file)[0]
            file.close()

        # loop through and store all plat values in arrays
        buy_orders = []
        sell_orders = []
        try:
            for i in range(len(data["payload"]["orders"])): # loop through sell and buy orders
                if(data["payload"]["orders"][i]["user"]["status"] == "ingame"): # only go through orders that have online players
                    if(data["payload"]["orders"][i]["order_type"] == "buy"): # seperate buy orders and sell orders into their own arrays
                        buy_orders.append(data["payload"]["orders"][i]["platinum"]) # add to buy order storage
                    else:
                        sell_orders.append(data["payload"]["orders"][i]["platinum"]) # add to sell order storage
        except Exception as e:
            print(str(index) + ": " + str(e))
         
        buy_orders.sort(reverse=True)   # put highest plat value on top
        sell_orders.sort()              # put lowest plat value on top
        #print("Buy: " + str(buy_orders[0]))
        #print("Sell: " + str(sell_orders[0]))

        # File for plat value outputs
        # Appends results into our output.csv
        with open("output.csv", "a") as file:
            file.write(target+",") # item name
            if(len(buy_orders)>0): # if there are any online buyers
                file.write(str(buy_orders[0])+",") # highest buy value
            if(len(sell_orders)>0): #if there are any online sellers
                file.write(str(sell_orders[0])) # lowest sell value
            file.write("\n")
            file.close()
        
        if(index < len(targets)-1): # if there are more entries
            time.sleep(3) # dont want to flood them

        # print(url.headers)
    except HTTPError as e:
        if(e.code == 429):
            print(target + " wants you to slow down")
            print("Waiting for " + str(e.headers).split()
                [6] + " seconds before our next request")
            time.sleep(int(str(e.headers).split()[6]) + 5)  # +5 because why not
        else:
            print(e.code)

# print results of timer
print("Took " + str((time.time()-start_time)/60) + " minutes")
print(str((time.time()-start_time)/len(targets)) + " seconds per entry")