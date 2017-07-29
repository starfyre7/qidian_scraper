# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

#Grab URL and provide it instead of hard coding it
url = "https://www.webnovel.com/book/6838665602003405/21799251029848595"


def url_to_title_content(url_string):
    page = requests.get(url_string)
    soup = BeautifulSoup(page.text)
    title_div = soup.find(class_='cha-tit')
    title = title_div.find('h3').string
    
    
    content_div = soup.find(class_='cha-content')
    
    content_p = content_div.find_all('p')
    content_strings = [c.string for c in content_p]
    
    return title, content_strings
    
#url_to_title_content(url)   
    
toc_url = "https://www.webnovel.com/book/7141993106000405"


re_book_id = re.compile(r'webnovel.com/book/(\d*)/?.*')
def table_of_contents_scraper(toc_url):
    match = re.search(re_book_id, toc_url)
    if not match:
        print "Table of contents URL %s is invalid" %toc_url
    book_id = match.group(1)
    chapter_info = requests.get('https://www.webnovel.com/apiajax/chapter/GetChapterList?bookId=%s' %book_id)
    js_ch = json.loads(chapter_info.text)
    print js_ch['data']['bookInfo'] #temp print
    
    #May need to take in chapter index and sort if urls are not outputted in order as JSON is order agnostic
    chapter_urls = ["https://www.webnovel.com/book/%s/%s" %(book_id, ch['chapterId']) for ch in js_ch['data']['chapterItems']]
    return chapter_urls
    

print table_of_contents_scraper(toc_url)