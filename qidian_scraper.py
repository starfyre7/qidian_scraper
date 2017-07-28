# -*- coding: utf-8 -*-


import urllib2
from bs4 import BeautifulSoup

#Grab URL and provide it instead of hard coding it
url = "https://www.webnovel.com/book/6838665602003405/21799251029848595"


def url_to_title_content(url_string):
    page = urllib2.urlopen(url_string)
    soup = BeautifulSoup(page)
    title_div = soup.find(class_='cha-tit')
    title = title_div.find('h3').string
    
    
    content_div = soup.find(class_='cha-content')
    
    content_p = content_div.find_all('p')
    content_strings = [c.string for c in content_p]
    
    return title, content_strings
    
#url_to_title_content(url)   
    
toc_url = "https://www.webnovel.com/book/7141993106000405"
def table_of_contents_scraper(toc_url):
    page = urllib2.urlopen(toc_url)
    soup = BeautifulSoup(page)
    #print soup
    pt = soup.find('div', class_='det-info')
    print pt
    title = soup.find("h2", class_=["mb10", "lh1d2", "oh"])
    print title
    toc = soup.find("ul", class_="g_mod_bd content-list")
    print toc
    
    details = soup.find(class_='book-detail')
    print details

table_of_contents_scraper(toc_url)