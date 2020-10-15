# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:21:32 2019

@author: DerJo
"""

# Collect links from the wikipedia page on hillary clinton


# Makes the plots appear within the notebook
#%matplotlib inline

# Two packages for doing data manipulation
import numpy as np                   # http://www.numpy.org/
import pandas as pd                  # http://pandas.pydata.org/

#  for plotting data
import matplotlib.pyplot as plt      # http://matplotlib.org/

# Package to save/load Python structures in the "Pickle" format
import pickle
import requests

# Some setup for display, helper libs, etc.
from copy import deepcopy
pd.options.display.max_columns = 100
pd.options.display.max_rows = 110
pd.options.mode.chained_assignment = None 


# whole page
#hillary = requests.get(url="https://en.wikipedia.org/w/api.php?action=parse&page=Hillary_Clinton&format=json").json()
#links
#S = requests.Session()

api_url = "https://en.wikipedia.org/w/api.php"

#parameters
some_params={'action': 'query', # could also use this API to change content (make an edit) or put in information
            "format": "json",
            'titles': 'Hillary_Clinton',
            'pllimit': 'max',
            'continue': '',
            'prop': 'links'}
# json link adress
p = ''
for key, value in some_params.items():
    p = p + key +'='+value+'&'
print(api_url+'?'+p)

# request data

result = requests.get(url=api_url, params=some_params, timeout=30).json() #set up the query and retrieve the results, interpret them as json
        
pages = result['query']['pages'] # go and get the content of the sub-element 'pages' from the element 'query'

pages

pages['5043192']

pages.keys()

def get_page_data_from_wp_api_simple(our_params):
        
    result = requests.get(url=api_url, params=our_params, timeout=30).json() #set up the query and retrieve the results
        
    pages = result['query']['pages'] # go and get the content of the sub-element 'pages' from the element 'query'
    
    for page_id in pages: # only 1 if called with only one article title
        page_data = pages[page_id] # content of the page/article element
        for link_data in page_data['links']: #iterate over the entries in the "revisions" list
                yield link_data  #"yield" works like "return", with one important exception: "return" would end the for loop once it has something to return, while "yield" returns the value and keeps on running the loop. 
      
for link_data in get_page_data_from_wp_api_simple(some_params):
    print(link_data)
    
page_link_list = [] # an emtpy list

for link_data in get_page_data_from_wp_api_simple(some_params): #here we catch all these "yield" outputs
    page_link_list.append(link_data)

len(page_link_list)

#understanding of this extended function...

def get_page_data_from_wp_api_extended(params):
  
    params = deepcopy(params)
          
    plcontinue = params.get('plcontinue')
    
    session = requests.session()
 
    while True:
        # continue downloading until we reach the last / current revision
        if plcontinue is not None:
            params['plcontinue'] = plcontinue
        result = session.get(url=api_url, params=params, timeout=30).json()
        
        # if 'query' in result:
        pages = result['query']['pages']
        
        _, page = result['query']['pages'].popitem()
        for link_data in page.get('links', []):
            yield link_data
        if 'continue' not in result:
            break
        plcontinue = result['continue']['plcontinue']
        
page_link_list2 = [] 

for link_data in get_page_data_from_wp_api_extended(some_params):
    page_link_list2.append(link_data)
    
len(page_link_list2)

pr_df = pd.DataFrame(page_link_list2)

pr_df.head(10)