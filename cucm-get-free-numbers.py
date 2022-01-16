# CUCM Get Free Number Numbers Script
# Written by James Hawkins - April 2020
# This script connects to a Cisco Unified Communications Manager system using the AXL API
# It then checks numbers in a range inputted by a user, checks for free numbers and outputs them to a text file

import sys
import os
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

########################################################################################################################

# Make a simple AXL request to CUCM server and retrieve cookies for subsequent connections

def axlgetcookies(serveraddress, version, axluser, axlpassword):

    try:
        # Make AXL query using Requests module
        axlgetcookiessoapresponse = requests.get('https://' + ipaddr + ':8443/axl/', headers=soapheaders, verify=False, auth=(axluser, axlpassword), timeout=3)
        print(axlgetcookiessoapresponse)
        getaxlcookiesresult = axlgetcookiessoapresponse.cookies

        if '200' in str(axlgetcookiessoapresponse):
            # request is successful
            print('AXL Request Successful')
        elif '401' in str(axlgetcookiessoapresponse):
            # request fails due to invalid credentials
            print('Response is 401 Unauthorised - please check credentials')
        else:
            # request fails due to other cause
            print('Request failed! - HTTP Response Code is ' + axlgetcookiessoapresponse)

    except requests.exceptions.Timeout:
        axlgetcookiesresult = 'Error: IP address not found!'

    except requests.exceptions.ConnectionError:
        axlgetcookiesresult = 'Error: DNS lookup failed!'

    if 'JSESSIONIDSSO' in str(getaxlcookiesresult):
        print('Cookies Retrieved')
        return getaxlcookiesresult

    else:
        sys.exit('Program has ended due to error!')



########################################################################################################################

# Connect to CUCM server using AXL and retrieve numbers in numplan table using a SQL query

def axlgetnumberdata(cookies, startnumber, endnumber):
    axlgetnumberdatasoaprequest = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/' + version +'"><soapenv:Header/><soapenv:Body><ns:executeSQLQuery><sql>select np.dnorpattern as Number, rp.name as Partition, np.description as Description, pu.name as type from numplan as np inner join routepartition as rp on np.fkroutepartition = rp.pkid inner join typepatternusage as pu on np.tkpatternusage = pu.enum where dnorpattern between "' + str(startnumber) + '" and "' + str(endnumber) + '" order by dnorpattern</sql></ns:executeSQLQuery></soapenv:Body></soapenv:Envelope>'
    axlgetnumberdatasoapresponse = requests.post('https://' + ipaddr + ':8443/axl/', data=axlgetnumberdatasoaprequest, headers=soapheaders, verify=False, cookies=cookies, timeout=9)

    return axlgetnumberdatasoapresponse.text


########################################################################################################################

def main():
    global ipaddr, version, axluser, axlpassword, soapheaders, cookies, startnumber, endnumber

    print('CUCM Unused Number Finder')
    print('Written by James Hawkins, April 2020')
    print()
    ipaddr = input('Enter IP address of CUCM Publisher: ')
    version = input('Enter CUCM version (Options include: 10.0, 11.0, 11.5, 12.0, 12.5): ')
    axluser = input('Enter AXL username: ')
    axlpassword = input('Enter AXL password: ')
    print()
    soapheaders = {'Content-type': 'text/xml', 'SOAPAction': 'CUCM:DB ver=' + version}

    axlgetcookiesresult = axlgetcookies(ipaddr, version, axluser, axlpassword)
    #print(axlgetcookiesresult)

    startnumber = input('Enter start number for scan: ')
    endnumber = input('Enter end number for scan: ')

    freenumbersfilename = 'freenumbers-'+ startnumber + '-' + endnumber + '.txt'

    filepath = os.getcwd()

    freenumbersfile = open(freenumbersfilename, 'w')

    axlgetnumberused = axlgetnumberdata(axlgetcookiesresult, startnumber, endnumber)

    #pprint.pprint(axlgetnumberused)

    counter = int(startnumber)
    freenumbercounter = 0
    numberrange = int(endnumber) - int(startnumber)
    freenumbers = []

    while counter <= int(endnumber):
        numberused = str(counter) in axlgetnumberused
        #print(str(counter) + " " + str(numberused))
        if str(numberused) == 'False':
            freenumbers.append(counter)
            freenumbersfile.write(str(counter) + '\n')
            freenumbercounter +=1

        counter = counter + 1

    freenumbersfile.close()

    print()
    print(str(freenumbercounter) + ' of ' + str(numberrange) + ' in the range are unused')
    print()
    print('Unused numbers are: ', freenumbers)
    print()
    print('The list of unused numbers has been written to ' + filepath + '\\' + freenumbersfilename)
    print()
    print()

########################################################################################################################

if __name__ == "__main__":
    main()

