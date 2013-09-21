#!/usr/bin/env python
# -*- coding: utf-8 -*-

__module_name__ = 'kw_highlight'
__module_version__ = '0.1'
__module_description__ = 'Highlight key-words.'

'''
This is a xchat-plugin to highlight keywords that show up in a channel.

When loaded 'kw_highlight' creates a list of 'keywords' to check a 
channel for and make bold if found.

The list is created from python 2.7 __builtins__ and most of the modules
in /usr/lib/python2.7.  

If you want to see which words are listed use:

Usage: /SHOWKW

This will print out the list to your xchat screen.
If you'd like to add some other keywords to track:

Usage: /ADD <keyword> 

Now, the supplied <keyword> will be also checked for.
'''

import xchat
import os
import pkgutil 
from string import punctuation


KEYWORDS = list() 
NONKEYWORDS = ['copy', 'email', 'keyword', 'mailbox', 'new', 'numbers',
               'platform', 'profile', 'sets', 'site', 'stat', 'test',
               'tempfile', 'this', 'traceback', 'types', 'trace', 'user',
               'code', 'string', 'compiler', 'commands', 'random']

def load_modkw():
    path = '/usr/lib/python2.7/'
    for mod in pkgutil.iter_modules([path]):
        if mod[1] not in NONKEYWORDS:
            KEYWORDS.append(mod[1])
    return

def keyword_highlight(privmsg, privmsg_slice, xchat_data):
    user = privmsg[0].split('!')[0][1:]
    privmsg[3] = privmsg[3][1:]
    msg = privmsg[3:]
    for word in enumerate(msg):
        if word[1].strip(punctuation) in KEYWORDS: 
            msg[word[0]] = '\002' + word[1] + '\002'
    xchat.emit_print('Channel Message', user, ' '.join(i for i in msg))
    return xchat.EAT_XCHAT

def add_keyword(cmd_msg, cmd_slice, xchat_data):
    if len(cmd_msg) < 2:
        xchat.prnt('Usage: /ADDKW <keyword>, adds a keyword to highlight.')
    else:
        for kw in cmd_msg[1:]:
            KEYWORDS.append(kw)
    return xchat.EAT_ALL

def remove_keyword(cmd_msg, cmd_slice, xchat_data):
    if len(cmd_msg) < 2:
        xchat.prnt('Usage: /RMKW <keyword>, removes a keyword from list of highlighted keywords.')
    else:
        if cmd_msg[1] in KEYWORDS:
            KEYWORDS.remove(cmd_msg[1])
    return xchat.EAT_ALL
    
def show_keywords(cmd_msg, cmd_slice, xchat_data):
    xchat.prnt(str(KEYWORDS))
    return xchat.EAT_ALL

load_modkw()

xchat.hook_server('PRIVMSG', keyword_highlight)

xchat.hook_command('ADDKW', add_keyword, 
                   help='Usage: /ADDKW <keyword>, adds a keyword to highlight.')

xchat.hook_command('RMKW', remove_keyword,
                   help='Usage: /RMKW <keyword>, removes a keyword from list of highlighted keywords.')

xchat.hook_command('SHOWKW', show_keywords, 
                   help='Usage: /SHOWKW, prints all the keywords that are looked for.')
