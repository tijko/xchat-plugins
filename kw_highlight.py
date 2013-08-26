#!/usr/bin/env python
# -*- coding: utf-8 -*-

__module_name__ = 'kw_highlight'
__module_version__ = '0.1'
__module_description__ = 'Highlight key-words.'

'''
This is a xchat-plugin to highlight keywords that show up in a channel.
'''

import xchat
import os
import imp
from string import punctuation


KEYWORDS = [i for i in dir(__builtins__) if not i.startswith('_')] 

def load_modkw():
    path = '/usr/lib/python2.7/'
    modules = [i for i in os.listdir(path) if i.endswith('.py') and
               not i.startswith('_') and i != 'this.py' and i != 'gzip.py' and
               i != 'antigravity.py']
    for module in modules:
            try:
                mod = module.strip('.py')
                import_mod = imp.load_source(mod, path + module)
                for kw in dir(import_mod):
                    if kw not in KEYWORDS and not i.startswith('_'):
                        KEYWORDS.append(kw)
                if mod not in KEYWORDS:
                    KEYWORDS.append(mod)
                del(mod)
            except TypeError or ImportError:
                pass
    return

def keyword_highlight(privmsg, privmsg_slice, xchat_data):
    privmsg[3] = privmsg[3][1:]
    msg = privmsg[3:]
    for word in enumerate(msg):
        if word[1].strip(punctuation) in KEYWORDS: 
            msg[word[0]] = '\002' + word[1] + '\002'
    xchat.prnt(' '.join(i for i in msg))
    return xchat.EAT_XCHAT

def add_keyword(cmd_msg, cmd_slice, xchat_data):
    if len(cmd_msg) < 2:
        xchat.prnt('Usage: /ADD <keyword>, adds a keyword to highlight.')
    else:
        for kw in cmd_msg[1:]:
            KEYWORDS.append(kw)
    return xchat.EAT_ALL
    
def show_keywords(cmd_msg, cmd_slice, xchat_data):
    xchat.prnt(str(KEYWORDS))
    return xchat.EAT_ALL

load_modkw()

xchat.hook_server('PRIVMSG', keyword_highlight)

xchat.hook_command('ADD', add_keyword, 
                   help='Usage: /ADD <keyword>, adds a keyword to highlight.')

xchat.hook_command('SHOWKW', show_keywords, 
                   help='Usage: /SHOWKW, prints all the keywords that are looked for.')
