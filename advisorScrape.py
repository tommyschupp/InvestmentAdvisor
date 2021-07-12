import csv
import re
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

import concurrent
from random import *
import pandas
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CRDData = pandas.read_csv(r'C:/Users/d/Desktop/Programming/2021/BrokerCheck/investmentAdvisors.csv')
CRDList = CRDData['Organization CRD#'].values.tolist() 

numFiles = 13 #change this to change number of files being created 
x = 1 + (14240 // numFiles)
chunkRows = pandas.read_csv(r'C:/Users/d/Desktop/Programming/2021/BrokerCheck/investmentAdvisors.csv', chunksize = x)
for i, chunk in enumerate(chunkRows):
    chunk.to_csv('out{}.csv'.format(i))
    code = "print('scrape"+str(i)+" has been opened')\nfrom bs4 import BeautifulSoup\nimport pandas\nfrom selenium import webdriver\nfrom selenium.webdriver.chrome.options import Options\nimport csv\nimport time\ndata = pandas.read_csv('out" + str(i) + ".csv')\nCRDList = data['Organization CRD#'].values.tolist() \ndef scrape():\n    resultList = []\n    chromeOptions = Options()\n    #chromeOptions.add_argument('--headless')\n    driver=webdriver.Chrome(options =chromeOptions, executable_path = 'C:/Users/d/Desktop/Programming/Chromedriver/chromedriver.exe')\n    url = 'https://brokercheck.finra.org/firm/summary/'\n    for crd in CRDList:\n        driver.get(url)\n        driver.maximize_window()\n        time.sleep(4)\n        driver.implicitly_wait(5)\n        driver.find_element_by_id('tab-item-2').click()\n        driver.implicitly_wait(3)\n        driver.find_element_by_id('firmtab-input').send_keys(crd)\n        driver.find_element_by_xpath('//button[@aria-label=\\'FirmSearch\\']').click()\n        driver.implicitly_wait(3)\n        try: \n            cardXpath = '//a[@href=\\\"/firm/summary/' + str(crd) + '\\\"]'\n            driver.find_element_by_xpath(cardXpath).click()\n        except Exception as e:\n            print(str(crd) + 'is unlisted')\n            resultList.append('Unlisted')\n            continue\n        time.sleep(2)\n        soup = BeautifulSoup(driver.page_source, 'html.parser')\n        results = []\n        for div in soup.find_all('div'):\n            if div.get('ng-if') == '!vm.isValidLink(item.crdNumber)':\n                if not '(CRD#' in div.string: \n                    results.append(div.string)\n        if len(results) == 0:\n            results.append('Empty/Individuals Only')\n        resultList.append(results)\n        print('a site from scrape" + str(i) + " has been scraped')\n    finalResults = pandas.DataFrame(list(zip(CRDList, resultList)), columns=['CRD#', 'Name(s)'])\n    finalAddress = r'C:/Users/d/Desktop/Programming/2021/BrokerCheck/resultSet" + str(i) + ".csv'\n    finalResults.to_csv(finalAddress, index = False)\nscrape()"
    name = "scrape" + str(i)
    newScrape = open(name+".py", "wt")
    newScrape.write(code)
    newScrape.close()

#execute each file using multithreading
#timne for the hard part
files = []
def importFiles(curFileName):
    files.append(__import__(curFileName))

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=13) as executor:
        for j in range(numFiles):
            curFileName = 'scrape' + str(j)
            executor.submit(importFiles, curFileName)
        

allNames = []
for i in range(numFiles):
    curFileName = 'resultSet' + str(i) + '.csv'
    curFile = pandas.read_csv(curFileName)
    curFileList = curFile['Name(s)'].values.tolist()
    for item in curFileList:
        allNames.append(item)

results = pandas.DataFrame(list(zip(CRDList, allNames)), columns=['CRD#', 'Name(s)'])
results.to_csv(r'C:/Users/d/Desktop/Programming/2021/BrokerCheck/finalResults.csv', index=False, header=True)


