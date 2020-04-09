'''
Created on 1 abr. 2020

https://selenium-python.readthedocs.io/getting-started.html
'''
import sys, os
from bs4.element import NavigableString, Comment
sys.path.append("\\".join(os.path.realpath(__file__).split('\\')[:-1]))
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import time
from helpers.XmlManagement import printElement

#===============================================================================
#     GETTING STARTED
#===============================================================================

#------------------------------------------------------------------------------ 
## Importing the webdriver and instancing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CHROME_PATH = "C:\\Users\\Miguel\\Anaconda3\\Lib\\chromedriver.exe"

driver = webdriver.Chrome(CHROME_PATH)

#------------------------------------------------------------------------------ 
# Accessing to a web
# driver.get("http://www.python.org")
# 
# print(driver.current_url)
# print(driver.title)
#sourcePage = BeautifulSoup(driver.page_source, features="html5lib")

## Search in a web,
# <input id="id-search-field" name="q" type="search" role="textbox" 
#     class="search-field" placeholder="Search" value="" tabindex="1">
# for str_ in ("pycon", "abfhdkk0001dd"):
#     elem = driver.find_element_by_name("q")
#     elem.clear()
#     elem.send_keys(str_)
#     elem.send_keys(Keys.RETURN)
#     
#     if "No results found." not in driver.page_source:
#         print(str_, "-> No results found.")

#===============================================================================
# ITERATE IN A PAGE
#===============================================================================

driver.get("https://www.worldometers.info/coronavirus/country/spain/")
html_ = driver.page_source
print(driver.title)
# all_divs = driver.find_elements_by_xpath('/html/body/div')
# print(all_divs)
# for elem in all_divs:
#     print(elem.__class__.__name__, type(elem), elem)
#     print(elem.text)
    

bs = BeautifulSoup(html_, features='html5lib')
matchs = bs.find_all('script')
html_dict = {}
TEMPLATE = "Highcharts.chart({}, "
GRAPHS = {'Total Cases' : "'coronavirus-cases-{}'", 
          'Daily New Cases': "'graph-cases-daily'", 
          'Active Cases': "graph-active-cases-total'",
          'Total Deaths': "'coronavirus-deaths-{}'", 
          'Daily Deaths': "'graph-deaths-daily'"}
for match in matchs:
    if match.attrs and match.attrs.get('type') == 'text/javascript':
        for title in GRAPHS:
            if title in match.text:
                html_dict[title] = str(match.text)

import re
## Processing the text
dict_values = {}
import datetime

def getDateFromStr(date_str):
    date_str = date_str.replace('"', '')
    date = datetime.datetime.strptime(date_str+' 2020', '%b %d %Y')
    return date.date()
    
for title, text in html_dict.items():
    text = text.replace('\n', '')
    text = text.replace('\\', '')
    text = text.replace(');', '')
    
    if '{' in GRAPHS[title]:
        text = text.split(TEMPLATE.format(GRAPHS[title].format('log')))[0]
        text = text.split(TEMPLATE.format(GRAPHS[title].format('linear')))[1]
    else:
        text = text.split(TEMPLATE.format(GRAPHS[title]))
        text = text[-1]
    
    x_values = re.search('categories: \[(.+?)\]', text).group(1).split(',')
    y_values = re.search('data: \[(.+?)\]', text).group(1).split(',')
    y_values = [int(y) if y!='null' else 0 for y in y_values]
    
    assert len(x_values) == len(y_values), f"length of x [{len(x_values)}] doesn't match y[{len(y_values)}]"
    x_values = list(map(getDateFromStr, x_values))
    
    dict_values[title] = (x_values, y_values)
    

def is_jscript(child):
    if (child.name == 'script'):
        if (hasattr(child, 'attrs') and isinstance(child.attrs, dict)):
            if child.attrs.get('type') == 'text/javascript' :
                return True
    return False

def listChilds(children, level=0):
    if not isinstance(children, str):
        i = 0
        aux_dict = {}
        script_found = False
        for child in children:
            return_ = listChilds(child, level=level+1)
            if return_ in (None, {}):
                continue
            if is_jscript(child):
                aux_dict['js/txt'+str(i)] = return_
            else:
                if isinstance(return_, dict):
                    aux_dict[str(i)] = return_
#                 elif isinstance(child, (NavigableString, Comment)):
#                     continue
                else:
                    if not script_found:
                        aux_dict[str(i)] = return_
#             elif isinstance(return_, dict):
#                 aux_dict[str(i)] = return_
            i += 1
        return aux_dict
    else:
        if children.strip() != '':
            return children

#html_dict = listChilds(bs.children)
import json
with open('html_dict.json', 'w') as jf:
    json.dump(html_dict, jf) 

driver.close()
