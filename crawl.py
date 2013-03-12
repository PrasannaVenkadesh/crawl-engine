'''
By: Prasanna Venkadesh
Licence: GPL V3.0
Program: An Internet Web-crawler that keeps crawling pages on Internt starting from a root or seed URL. The aim of this script is to extract URL's found in a page and the chain continues.
'''

import urllib2

'''
Type: Function
Input: URL
Output: Content of the page or nothing if invalid URL
'''
def get_page(url):
	try:
		url = urllib2.unquote(url)
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Compatible)')
		return urllib2.urlopen(req).read()
	except:
		return ""

'''
Type: Function
Input: Two sets
Output: returns nothing but adds content of set 2 to set 1 if not present
'''
def union(p,q):
	for e in q:
		if e not in p:
			p.add(e)

'''
Type: Function
Input: Selective content of a webpage
Output: 1 url at a time & End position of url found
'''
def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"',start_link)
	end_quote = page.find('"',start_quote+1)
	url = page[start_quote+1 : end_quote]
	return url, end_quote

'''
Type: Function
Input: content of a web page
Output: set of all url link found on the page
'''
def get_all_links(page):
	links = set()
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.add(url)
			page = page[endpos:]
		else:
			break
	return links

'''
Type: Function
Input: URL of a page, set of crawled pages, set of pages to crawl
Output: Prints the set of crawled url(s) with number of crawled pages
'''
def goahead(page, crawled, tocrawl):
	if page not in crawled:
		union(tocrawl, get_all_links(get_page(page)))
		crawled.add(page)
		print crawled, '\n\n', len(crawled)

'''
Type: Function
Input: A root URL to start crawling with, number of URL(s) to crawl
Output: Set of crawled URL(s) for further processing and set of URL(s) tocrawl
'''
def crawl_web(seed,limit):
	tocrawl = {seed}
	crawled = set()
	while tocrawl:
		page = tocrawl.pop()
		
		if limit == 'a':
			goahead(page, crawled, tocrawl)
		else:
			goahead(page, crawled, tocrawl)
			
			if str(len(crawled)) == limit:
				break

	return crawled, tocrawl

'''
Program execution starts here by getting 2 inputs
1. A URL to start crawling
2. Number of URL(s) to crawl
'''
print "Enter a URL", "\nEg: http://www.python.org"
root_url = raw_input('@> ')
print "\nHow many URL to crawl ?", "\nEg: 10 - to crawl 10 URL(s)\n", "Eg: a or leave empty - to crawl all the links (this may take long time to finish)"
limit = raw_input('#> ')

'''
Type: Function call
Parameters: Root URL and Limit of crawling URL(s)
'''
crawl_web(root_url, limit)
