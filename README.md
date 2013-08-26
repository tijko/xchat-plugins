xchat-plugins
=============

A couple of plugins for xchat clients.

####chk_wiki
This is a xchat-plugin to find any information on an item from wikipedia.

The 'chk_wiki' plugin will scrape wikipedia looking for any information on 
the 'query' parameter passed.  Using wikipedia's api, this plugin will
create a request and print out the parsed results.  

    Usage: /WIKI <query>

If the <query> request returns results showing multiple pages, those
pages will be show/printed.  You can then use:

    /WIKI <listed_uery> (listed_query being one of specific names listed) 

To check for a specific meaning.

####kw_highlight
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
