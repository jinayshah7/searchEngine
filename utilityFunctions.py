#!/usr/bin/python

# Sorts the pages according to their ranks before displaying results
# Quick sort is currently the fastest known sorting alogrithm

def quick_sort(pages, ranks):
	if not pages or len(pages) <= 1:
		return pages
	else:
		pivot = ranks[pages[0]] #find pivot
		worse = []
		better = []
		for page in pages[1:]:
			if ranks[page] <= pivot:
				worse.append(page)
			else:
				better.append(page)
	return quick_sort(better, ranks) + [pages[0]] + quick_sort(worse, ranks)




# p is union of p and q
def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)