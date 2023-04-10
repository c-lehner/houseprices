'''
File: scrape_z.py
Author: C. Lehner
Scraping Zillow.com for real estate data
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time
import random
from urllib.request import urlopen
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#import towns from towns.py in my directory
from towns import nhtowns, vttowns, nhtowns_2, mainetowns
session = requests.Session()
#requests headers to avoid recaptcha
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
colnames = ('zpid', 'id', 'providerListingId', 'imgSrc', 'hasImage', 'detailUrl',
       'statusType', 'statusText', 'countryCurrency', 'soldPrice',
       'unformattedPrice', 'address', 'addressStreet', 'addressCity',
       'addressState', 'addressZipcode', 'isUndisclosedAddress', 'beds',
       'baths', 'area', 'latLong', 'isZillowOwned', 'variableData',
       'badgeInfo', 'hdpData', 'isSaved', 'isUserClaimingOwner',
       'isUserConfirmedClaim', 'pgapt', 'sgapt', 'zestimate',
       'shouldShowZestimateAsPrice', 'has3DModel', 'hasVideo', 'isHomeRec',
       'info2String', 'hasAdditionalAttributions', 'isFeaturedListing',
       'availabilityDate', 'list', 'relaxed', 'streetViewMetadataURL',
       'streetViewURL')
#set towns to scrape
towns = mainetowns[200:]
#create empty dataframe with column names
df = pd.DataFrame(columns=colnames)
# town = "albany-nh"
#loop through towns
for town in towns:
    #loop through pages, max 20 because that's the max number of pages zillow has
    for i in range(1,20):
        print(town,i)
        url = str("https://www.zillow.com/"+town + "/sold/" + str(i)+"_p/")
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print("Error:", response.status_code)
            time.sleep(2.2 + random.random())
            response = session.get(url, headers=headers)
            if response.status_code != 200:
                print("didn't work:", response.status_code)
                break
        page = json.loads(re.search(r'!--(\{"queryState".*?)-->', response.text).group(1))
        df_temp = pd.DataFrame(page['cat1']['searchResults']['listResults'])
        #check if it's the last page, a full page is 40 results, if it's not, append df_temp to df and break
        if len(df) > 0 and i > 1 and len(df_temp) < 40:
            #if so, break out of loop
            print("Last page reached:", town, i)
            df = df.append(df_temp, ignore_index=True)
            break
        else:
            #if not, append df_temp to df
            df = df.append(df_temp, ignore_index=True)
            print(len(df))
            #wait 1-3 seconds
            time.sleep(1.2 + random.random())

#keys to extract keys = {'streetAddress': '127 Brook Hollow', 'zipcode': '03755', 'city': 'Hanover', 'state': 'NH', 'latitude': 43.707325, 'longitude': -72.27512, 'price': 476000.0, 'dateSold': 1676620800000, 'bathrooms': 2.0, 'bedrooms': 3.0, 'livingArea': 1664.0, 'homeType': 'CONDO', 'homeStatus': 'RECENTLY_SOLD', 'daysOnZillow': -1, 'isFeatured': False, 'shouldHighlight': False, 'zestimate': 462900, 'rentZestimate': 3074, 'listing_sub_type': {}, 'isUnmappable': False, 'isPreforeclosureAuction': False, 'homeStatusForHDP': 'RECENTLY_SOLD', 'priceForHDP': 476000.0, 'isNonOwnerOccupied': True, 'isPremierBuilder': False, 'isZillowOwned': False, 'currency': 'USD', 'country': 'USA', 'taxAssessedValue': 289200.0}
keys = ['streetAddress', 'zipcode', 'city', 'state', 'latitude', 'longitude', 'price', 'dateSold', 'bathrooms', 'bedrooms', 'livingArea', 'homeType', 'homeStatus', 'daysOnZillow', 'isFeatured', 'shouldHighlight', 'zestimate', 'rentZestimate', 'listing_sub_type', 'isUnmappable', 'isPreforeclosureAuction', 'homeStatusForHDP', 'priceForHDP', 'isNonOwnerOccupied', 'isPremierBuilder', 'isZillowOwned', 'currency', 'country', 'taxAssessedValue']
#get state
for i in keys:
    df[str(i)] = df['hdpData'].str.get('homeInfo').str.get(i)

#check if zpids are unique
df['zpid'].nunique()

#save to csv
df.to_csv("mezillow2.csv")

#write me a program that checks if a number is prime

#write me a program that checks if a number is prime
#check if a string is a palindrome

