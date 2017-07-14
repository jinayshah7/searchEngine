

# Returns a string with the content of the web page
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

# Extracts the url and returns it along with the index position of the end quote of url
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

# p is union of p and q
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

# Returns all links in the web page
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

# The main function that crawls the web pages starting with the seed fucntion
# Currently, if. started on the web, it will keep crawling becuase of the endless chain of links
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


# Function that add word to the index
def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        # not found, add new keyword to index
        index[keyword] = [url]

# Help function that search the index for the keyword
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

# Function that splits page into words and adds them to index
def add_page_to_index(index,url,content):
    words = content.split()
    for keyword in words:
        add_to_index(index,keyword,url)

# Function for recording cliks on a particular link
def record_user_click(index,keyword,url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] += 1

#
# Functions required for ranking
#

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
            #Loop throught all pages
            for node in graph:
                #check if node links to page
                if page in graph[node]:
                    #Add to new rank based on this node
                    newrank += d * ranks[node] / len(graph[node])
            newranks[page] = newrank
        ranks = newranks
    return ranks

# Function that returns the one URL most likely to be the best site for that
# keyword. If the keyword does not appear in the index return None
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

# Help function that uses quick sort algorithm to order array
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


index, graph = crawl_web('https://theboffinn.wordpress.com',2);


ranks = compute_ranks(graph)

print ordered_search(index, ranks, 'something')
