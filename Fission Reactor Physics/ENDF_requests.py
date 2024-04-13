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

def xsec(target, reaction):
    dataIDs = database_info(target, reaction, 'SIG')
    # average over all data sets
    E_values = []
    Sig_values = []
    count = []

    print("Processing ", len(dataIDs[3]) ," data sets, this might take a while...")

    for dataID in dataIDs[3]:
        # Temp variables to store the E and Sig values of the current data set
        E_values_temp = data_get(dataID)[0]
        Sig_values_temp = data_get(dataID)[1]
        print("Now processing data set:", dataID, " (", dataIDs[3].index(dataID)+1, "/", len(dataIDs[3]),") it has", len(E_values_temp), " data points")

        for ii in range(len(E_values_temp)):
            Ene = E_values_temp[ii]
            if Ene not in E_values:
                E_values.append(Ene)
                Sig_values.append(Sig_values_temp[ii])
                count.append(1)
            else:
                jj = E_values.index(Ene)
                Sig_values[jj] += Sig_values_temp[ii]
                count[jj] += 1


    print("Averaging the data")
    for jj in range(len(Sig_values)):
        Sig_values[jj] /= count[jj]
    print("Done!")

    #order the data by energy
    print("Ordering the data by Energy")
    E_values, Sig_values = zip(*sorted(zip(E_values, Sig_values)))

    return E_values, Sig_values
    
    













