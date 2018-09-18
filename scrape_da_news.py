from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xlsxwriter
import requests
import nltk
import os
import re
import xlsxwriter

#get links for bbc news articles

page=0
#change proxies, might not be valid at the time you are using it
proxies=["154.39.144.247:3128","66.70.147.196:3128","158.69.206.181:8888","66.70.182.205:3128" ]

#here change your path to your chromedriver
path='/Users/maryiahanina/Downloads/chromedriver'

count=1
#here go on the news website and type in your subject in search box
#then put the url here excluding the page number
url="https://www.bbc.co.uk/search?q=adhd#page="+str(count)
with open('news_links.txt','a') as f:
    for i in range(100):
        chrome_options = webdriver.ChromeOptions()
        random.shuffle(proxies)
        chrome_options.add_argument('--proxy-server=%s' % proxies[0])
        print(proxies[0])
        browser = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
        browser.get(url)

        opts = Options()
        #change the user agent however you want
        opts.add_argument("user-agent=nina's macbook")
        browser.set_page_load_timeout(random.randint(0,90))
        
        actions = ActionChains(browser)
        random.shuffle(proxies)
        chrome_options.add_argument('--proxy-server=%s' % proxies[0])
        print(proxies[0])


        def find_between( s, first, last ):
            try:
                start = s.index( first ) + len( first )
                end = s.index( last, start )
                return s[start:end]
            except ValueError:
                return ""

        def find_between_r( s, first, last ):
            try:
                start = s.rindex( first ) + len( first )
                end = s.rindex( last, start )
                return s[start:end]
            except ValueError:
                return ""


        content = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h1')))
        
        time.sleep(3)
        for each in content:

            s=each.get_attribute('innerHTML')
            
            f.write(find_between(s, '<a href="', '">' )+'\n')
                
            print(find_between_r(s, '<a href="', '">' )+'\n')

        count+=1
        print(count)
        url="https://www.bbc.co.uk/search?q=attention+deficit+disorder&sa_f=search-product&scope=#page="+str(count)
        browser.quit()
f.close()

#get article links from fox news

page=0
count=0
#same here, change the url after typing in your subject in the search box
url="http://www.foxnews.com/search-results/search?q=adhd&ss=fn&start="+str(count)
with open('news_links.txt','a') as f:
    for i in range(46):
        chrome_options = webdriver.ChromeOptions()
        random.shuffle(proxies)
        chrome_options.add_argument('--proxy-server=%s' % proxies[0])
        print(proxies[0])
        browser = webdriver.Chrome(executable_path='/Users/maryiahanina/Downloads/chromedriver',chrome_options=chrome_options)
        browser.get(url)

        opts = Options()
        opts.add_argument("user-agent=max's macbook")
        browser.set_page_load_timeout(random.randint(0,90))
        #while browser.find_elements_by_class_name('Search-showMoreWrapper--1Z88y'):
        #for i in range(20):
        actions = ActionChains(browser)
        random.shuffle(proxies)
        chrome_options.add_argument('--proxy-server=%s' % proxies[0])
        print(proxies[0])

        content = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h3')))
        #print(len(content))
        for each in content:

            s=each.get_attribute('innerHTML')
            if 'health' in find_between(s, "href=", ".html" ):
                f.write(find_between(s, 'href="', ".html" )+'\n')
                
            #print(find_between_r( s, "href=", ">" ))
        
        count+=10
        print(count)
        url="http://www.foxnews.com/search-results/search?q=adhd&ss=fn&start="+str(count)
        browser.quit()
f.close()

#now download all the text from the link of the article

avoid=['Hi', 
'Already a subscriber?',
'Subscribe today for full access on your desktop, tablet, and mobile device.',
'''Already a print edition subscriber, but don't have a login?''',
'Manage your account settings.',
'View the E-Newspaper',
'Manage your Newsletters',
'View your Insider deals and more',
'Member ID Card',
'Chat Support',
'Chat Support',
'Support',
'Support',
'Log Out',
'Get the news']

data=open('news_links.txt','r')
linelist = data.readlines() 
data.close()             #read each line
count = len(linelist)                 #count lines

line=0
articlenum=1 
row=0
doc=1
for i in range(count):
    with open ('news_text.txt','a') as f:
    
        base_url = linelist[i]
        print("processing: "+base_url)
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text,'lxml')
        
        articlenum+=1
        print('article: '+str(articlenum))
        #here i just rewrite all the lines 
        for par in soup.find_all("p"): 
            
            f.write(par.text)
            f.write('\n') 
            
f.close()

#now only select the sentences relevant to your subject

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("news_text.txt")
data = fp.read()
data=re.split(r'[\r\n]+',data)
sentences=[]
for i in data:
    one=re.split('(?<=[.!?]) +',i)
    for j in one:
        sentences.append(j)


print(len(sentences))
print(sentences[100])
count=0

#change for the relevant words in your search
words=['psychology', 'mind', 'adhd', 'stress', 'anxiety', 'attention', 'attention deficit','hyperactivity', 'drugs', 'medication', 'meds', 'ADHD','side effects', 'diagnosis', 'diagnosed']

class Sentence:
    def __init__(self,text):
        self.data=text
        self.copied=False

mylist=[]
for i in sentences:
    temp=Sentence(i)
    mylist.append(temp)
with open ('news_parsed.txt','a') as f:

    for sentence in mylist:
        for word in words:
            if word in sentence.data and sentence.copied==False:
                f.write(sentence.data+'\n') 
                sentence.copied=True
                count+=1
            else:
                continue
f.close()

print('found '+str(count)+' relevant sentences') 

#make sure to delete all the duplicates
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("news_parsed.txt")
data = fp.read()
data=re.split(r'[\r\n]+',data)
sentences=[]
for i in data:
    one=re.split('(?<=[.!?]) +',i)
    for j in one:
        sentences.append(j)
print(len(sentences))
print(sentences[100])
count=0

sentences=set(sentences)

with open('news_final.txt','a') as f:
    for i in sentences:
        f.write(i+'\n')

#finally put all your stuff in an excel file

workbook = xlsxwriter.Workbook('merged_nodups.xlsx')        #create file
worksheet = workbook.add_worksheet()           #create worksheet

#here change the path to the final text file news_final.txt
data = open('/Users/maryiahanina/Desktop/merging/news_final.txt','r')                #loaddata

linelist = data.readlines()              #read each line
count = len(linelist)                 #count lines
print(count)                       #check number of lines
row=0

line=0
for num in range (0, count):         #create each line and print in excel
    line = linelist[num]            #load each line in variable
    splitline = line.split("\n")          #split lines
    if not splitline[0]=='':
        worksheet.write(row, 0, row)
        worksheet.write(row, 1, splitline[0]) #write each line in excel
        row+=1         

workbook.close()            #close workbook