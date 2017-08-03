# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
import drive
from unidecode import unidecode
from apiclient.errors import HttpError
import time

re_chapter_title = re.compile(r'Chapter (\d*): (.*)')
def url_to_title_content(url_string):
    for i in range(3):   
        page = requests.get(url_string)
        soup = BeautifulSoup(page.text)
        title_div = soup.find(class_='cha-tit')
        read_title = unidecode(title_div.find('h3').string)
        if read_title is not None:
            break
    match = re.match(re_chapter_title, read_title)
    title = "{0:04} {1}".format(int(match.group(1)), match.group(2))
    
    content_div = soup.find(class_='cha-content')
    
    content_p = content_div.find_all('p')
    content_strings = [c.string.encode('utf-8') for c in content_p if c.string is not None]
    
    return title, content_strings
    

re_book_id = re.compile(r'webnovel.com/book/(\d*)/?.*')
def table_of_contents_scraper(toc_url):
    match = re.search(re_book_id, toc_url)
    if not match:
        print "Table of contents URL %s is invalid" %toc_url
    book_id = match.group(1)
    chapter_info = requests.get('https://www.webnovel.com/apiajax/chapter/GetChapterList?bookId=%s' %book_id)
    js_ch = json.loads(chapter_info.text)    
    #May need to take in chapter index and sort if urls are not outputted in order as JSON is order agnostic
    chapter_urls = ["https://www.webnovel.com/book/%s/%s" %(book_id, ch['chapterId']) for ch in js_ch['data']['chapterItems']]
    return js_ch['data']['bookInfo'], chapter_urls
    
    


def upload_chapters_from_toc(toc_url):    
    bookinfo, urls = table_of_contents_scraper(toc_url)
    book_name = unidecode(bookinfo['bookName'])
    print("Uploading: {0}".format(book_name))
    service = drive.create_service()
    q_folder_id = drive.get_Qidian_Novels_folder(service)['id']
    n_folder_id = drive.create_novel_folder_if_not_exist(service, q_folder_id, book_name)['id']
    for url in urls:
        for i in range(3):
            try:
                title, content = url_to_title_content(url)
                drive.add_string_as_docs_file_to_folder(service, n_folder_id, title, '\n'.join(content))
                break
            except HttpError as err:
                print("Error: {0}".format(err))
                time.sleep(2)
    
if __name__ == '__main__':
    with open('toc_list.txt') as f:
        for url in f:
            upload_chapters_from_toc(url)
    #ch_url = 'https://www.webnovel.com/book/7141993106000405/19175781926224608'
    #title, content = url_to_title_content(ch_url)
    #print content
    #print '\n'.join(content)