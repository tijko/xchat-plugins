#!/usr/bin/env python
# -*- coding: utf-8 -*-

__module_name__ = 'utube_qw'
__module_version__ = '0.1'
__module_description__ = 'Look up youtube videos'

'''
This is a xchat-plugin to find Youtube videos that return from a query parameter.

The 'utube_qw' plugin will query Youtube looking for any videos on the 'query' 
parameter passed.  Using Youtube's api, this plugin will create a request and 
return links to matching videos.

Usage: /TUBE <query>

If the <query> request returns results, they will be supplied through xchat in
hyperlink form.

'''
import xchat
import requests


DEVELOPER_KEY = "YOUR_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def tube_query(cmd_req, query, xchat_data=None):
    if len(cmd_req) < 2:
        xchat.prnt('Usage: /TUBE <query>, finds youtube videos on <query>.')
    else:
        query = '+'.join(query[1].split())
        query = ("https://www.googleapis.com/youtube/v3/search?part=id"
                 "&q=%s&type=video&maxResults=10&key=%s"
                 % (query, DEVELOPER_KEY))
        make_request(query)
    return xchat.EAT_ALL

def make_request(query):
    req = requests.get(query)
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
    page_data = page_data.json()
    for video in page_data['items']:
        xchat.prnt("<https://www.youtube.com/watch?v=%s>" % video['id']['videoId'])

xchat.hook_command('TUBE', tube_query,
                    help='Usage: /TUBE <query>, finds youtube videos on <query>.')

