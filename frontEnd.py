#!/usr/bin/python
from mainCrawler import *
from linkFunctions import *
from searchFunctions import *
from utilityFunctions import *
from rankingFunctions import *


searchKeyword  = raw_input("Enter the keyword to be searched: ")

index, graph = crawl_web('https://theboffinn.wordpress.com',2);
ranks = compute_ranks(graph)
print ordered_search(index, ranks, searchKeyword)