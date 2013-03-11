'''
By: Prasanna Venkadesh
Licence: GPL V3.0
Program: An Internet Web-crawler that keeps crawling pages on Internt starting from a root or seed URL. The aim of this script is to extract URL's found in a page and the chain continues.
'''

import urllib2

def get_page(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Compatible)')
		return urllib2.urlopen(req).read()
	except:
		return ""

def union(p,q):
	for e in q:
		if e not in p:
			p.add(e)

def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"',start_link)
	end_quote = page.find('"',start_quote+1)
	url = page[start_quote+1 : end_quote]
	return url, end_quote

def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links

def crawl_web(seed):
	tocrawl = {seed}
	crawled = set()
	while tocrawl:
		page = tocrawl.pop()
		if page not in crawled:
			union(tocrawl, get_all_links(get_page(page)))
			crawled.add(page)
			print crawled, '\n\n', len(crawled)
	return crawled

crawl_web(raw_input('URL Please (Eg:- http://en.wikipedia.org): '))
