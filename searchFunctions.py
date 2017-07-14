#!/usr/bin/python

from utilityFunctions import *

# Returns the one URL most likely to be the best site for that
# keyword. Returns None if the keyword does not appear in the index,
def best_search(index, ranks, keyword):
	return_url = '';
	if keyword not in index:
		return None
	for url in index[keyword]:
		if url in ranks:
			if return_url != '':
				if ranks[url] > ranks[return_url]:
					return_url = url
			else:
				return_url = url
	return return_url

# Function that returns the list of all URLs for that keyword. Ordered by page
# rank. If the keyword does not appear in the index return None
def ordered_search(index, ranks, keyword):
	pages = lookup(index, keyword)
	return quick_sort(pages, ranks)


# Help function that search the index for the keyword
def lookup(index,keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None