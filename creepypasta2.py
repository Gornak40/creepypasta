#!/bin/python3
from tldextract import extract
from requests import get
from fake_useragent import UserAgent
from pprint import pprint
from bs4 import BeautifulSoup
from os import chdir
from termcolor import cprint


def get_bs(data):
	return BeautifulSoup(data, features='lxml')


def get_data(url):
	req = get(url, headers={'fake-useragent': UserAgent().random})
	return req.content


def get_domain(url):
	return extract(url).domain + '.' + extract(url).suffix


def fix_url(url, main):
	if (url[:2] == '//'):
		return 'https:' + url
	if (url[:1] == '/'):
		return 'https://' + get_domain(main) + url
	return url


def go(bs, css):
	return bs.select(css)[0]


def get_text(bs):
	return bs.text.strip()


def print_story(url):
	bs = get_bs(get_data(url))
	bs = go(bs, 'body > div.main > div.center-block-all > div > div > div > div.center-content-block.light-block')
	title = get_text(bs.h1)
	bs.h1.decompose()
	bs.script.decompose() if bs.script else None
	bs.script.decompose() if bs.script else None
	return title, get_text(bs)


def final():
	with open('links.txt') as file:
		links = file.read().strip().split('\n')
		file.close()
	chdir('stories2')
	M = set()
	for ind, link in enumerate(links):
		if ind < 89:
			continue
		title, text = print_story(link)
		title = ''.join([x for x in title if x.isalnum() or x == ' ' or x == '.' or x == '-']).title()
		while title in M:
			title += '(analog)'
		M.add(title)
		print(title)
		with open(title + '.txt', 'w') as file:
			file.write(text)
			file.close()



def brute():
	links = list()
	for i in range(1, 105 + 1):
		url = 'https://kripipasta.com/story/page{}.html'.format(i)
		bs = get_bs(get_data(url))
		bs = bs.select('#yw0 > div.items > div > div.center-content-block.light-block > h2 > a')
		arr = ['https://kripipasta.com' + x.get('href') for x in bs]
		links.extend(arr.copy())
		print(*arr, sep='\n')


if __name__ == '__main__':
	final()
