#!/usr/bin/python

from linkFunctions import *
from searchFunctions import *
from utilityFunctions import *
from rankingFunctions import *


            
# The main function that crawls the web pages starting with the seed fucntion
# It also constructs a dictionary with url as the key and the links in the page as the values

def crawl_web(seed, max_depth):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}
    next_depth = []
    depth = 0
    
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            outlinks = get_all_links(content)
            union(next_depth, outlinks)
            graph[page] = outlinks
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth = depth + 1
            
    return index, graph


# Adds word to the index
#Appends to the list of urls for the keyword if keyword is present
# If keyword is not found, adds new entry for the keyword to the dictionary
def add_to_index(index,keyword,url):
    if keyword in index:                     
        index[keyword].append(url)
    else:
        index[keyword] = [url]

# Help function that search the index for the keyword
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

# Takes the page details as input and updates the index
def add_page_to_index(index,url,content):
    words = content.split()
    for keyword in words:
        add_to_index(index,keyword,url)



################################################################################################################################

index, graph = crawl_web('https://theboffinn.wordpress.com',2);
ranks = compute_ranks(graph)
print ordered_search(index, ranks, 'something')
