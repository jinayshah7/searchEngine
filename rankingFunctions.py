#!/usr/bin/python

# Function that computes page ranks
#
# Formula to count rank:
#
# rank(page, 0) = 1/npages 
# rank(page, t) = (1-d)/npages
#                 + sum (d * rank(p, t - 1) / number of outlinks from p)
#                 over all pages p that link to this page
#
def compute_ranks(graph):
	d = 0.8 #dumping constant
	numloops = 40

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages

	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1 - d) / npages
			#Loop through all pages
			for node in graph:
				#check if node links to page
				if page in graph[node]:
					#Add to new rank based on this node
					newrank += d * ranks[node] / len(graph[node])
			newranks[page] = newrank
		ranks = newranks
	return ranks