#import modules to do API requests
import requests

## DATABASE CALL
def database_call(target, reaction, quantity):
    #check if the reaction is a number (MT code) or a string (explicit reaction name)
    if type(reaction) == int:
        reaction = "&MT=" + str(reaction)
    else:
        reaction = "&Reaction=" + reaction

    #check if the quantity is a number (MF code) or a string (explicit quantity name)
    if type(quantity) == int:
        quantity = "&MF=" + str(quantity)
    else:
        quantity = "&Quantity=" + quantity

    url = "https://nds.iaea.org/exfor/e4list?Target="+target + reaction + quantity + "&json"
    return url

## DATABASE INFO
def database_info(target, reaction, quantity):
    #produce the url for the call to the database
    url = database_call(target, reaction, quantity)
    #call the database
    response = requests.get(url)
    data = response.json()
    data = data["sections"]

    Authors_list = [item['AUTH'] for item in data]
    Year_list = [item['DATE'] for item in data]
    Sec_IDs_list = [item['PenSectID'] for item in data]

    for i in range(len(Authors_list)):
        print([Sec_IDs_list[i], Year_list[i], Authors_list[i] ])

    return (data, Authors_list, Year_list, Sec_IDs_list)

## GET DATA
def data_get(Sec_ID, *args):
    url = 'https://nds.iaea.org/exfor/e4sig?PenSectID='+str(Sec_ID)+'&json'
    response = requests.get(url)
    data = response.json()

    if args == 1: #if the user wants to see all the raw data
        print(data) 
        
    elif args == 2: #if the user wants to see the columns and the number of points
        cols = data["datasets"][0]["COLUMNS"]
        print(f"Data columns and units of measurments {cols}")

        nPts = data["datasets"][0]["nPts"]
        print(f"Number of data points: {nPts}")

    #otherwise the functions runs silently
    dataset = data["datasets"][0]["pts"]
    E_values = [item['E'] for item in dataset]
    Sig_values = [item['Sig'] for item in dataset]
    
    return (E_values, Sig_values)







