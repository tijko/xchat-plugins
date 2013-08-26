#!/usr/bin/env python
# -*- coding: utf-8 -*-

__module_name__ = 'chk_wiki'
__module_version__ = '0.1'
__module_description__ = 'Lookup data on wikipedia.'

'''
This is a xchat-plugin to find any information on an item from wikipedia.

The 'chk_wiki' plugin will scrape wikipedia looking for any information on 
the 'query' parameter passed.  Using wikipedia's api, this plugin will
create a request and print out the parsed results.  

Usage: /WIKI <query>

If the <query> request returns results showing multiple pages, those
pages will be show/printed.  You can then use:

/WIKI <listed_uery> (listed_query being one of specific names listed) 

To check for a specific meaning. 
'''
   
import xchat
import requests
from BeautifulSoup import BeautifulSoup


def chk_wiki(cmd_req, query, xchat_data=None):
    if len(cmd_req) < 2:
        xchat.prnt('Usage: /WIKI <query>, checks wikipedia for information on <query>.')
    else:
        query = '_'.join(i for i in query[1].split())
        make_request(query)
    return xchat.EAT_ALL        

def make_request(query):
    wiki_api = 'http://en.wikipedia.org/w/index.php?action=render&title='
    req_addr = wiki_api + query
    req = requests.get(req_addr)
    if not req.ok:
        bad_request(req)
    else:
        parse_response(req)

def bad_request(error):
    xchat.prnt('Bad Request!')
    xchat.prnt('Reason: ' + error.reason)
    xchat.prnt('Error Code: ' + str(error.status_code))
    xchat.prnt('Address: ' + error.url)

def parse_response(page_data):
    page = page_data.content
    page_soup = BeautifulSoup(page)  
    p_tags = page_soup.findAll('p')
    if (any(i.text == 'It may also refer to:' for i in p_tags) or 
        len(p_tags) < 4):     
        multi_page(page_soup)
    else:
        for p in p_tags:
            paragraph = p.text.encode('ascii', 'ignore') 
            xchat.prnt(paragraph)               

def multi_page(page_soup):
    xchat.prnt('Multiple Entries:')
    entries = page_soup.findAll('a')
    entries = [i['href'].split('/')[-1] for i in entries]  
    entries = [i for i in entries if 'Help:' not in i and 
               'File:' not in i and '&namespace=0' not in i and
               'index.php' not in i]
    for link in entries:
        xchat.prnt('[%d] %s' % (entries.index(link) + 1, link))


xchat.hook_command('wiki', chk_wiki, 
                    help='Usage: /WIKI <query>, checks wikipedia for information on <query>.')
