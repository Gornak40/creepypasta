#!/bin/python3
from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent
from pprint import pprint
from termcolor import cprint
from os import chdir, listdir, rename, system
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


agent = UserAgent().random


def get_data(url):
	req = get(url, headers={'user-agent': agent})
	return req.content


def check(url, good, bad):
	if not all([x in url for x in good]):
		return False
	if any([x in url for x in bad]):
		return False
	return True


def get_links(bs):
	res = list(filter(bool, [x.get('href') for x in bs.find_all('a')]))
	return res


def to_file(name, arr):
	with open(name, 'a') as file:
		[file.write(x + '\n') for x in arr]
		file.close()


def load_links():
	for num in reversed(range(1, 105 + 1)):
		url = 'https://kripipasta.com/story/page{}.html'.format(num)
		data = get_data(url)
		bs = BeautifulSoup(data, features='lxml')
		bs2 = bs.select('body > div.main > div.center-block-all > div > div > div > div > div')[0]
		links = get_links(bs2)
		links = list(set([x for x in links if check(x, ['story'], ['page', '#', '//'])]))
		links = list(map(lambda x: 'https://kripipasta.com' + x, links))
		to_file('links.txt', links)
		print(num)


def print_story(url):
	data = get_data(url)
	bs = BeautifulSoup(data, features='lxml')
	css = 'body > div.main > div.center-block-all > div > div > div > div.center-content-block.light-block'
	bs2 = bs.select(css)[0]
	title = bs2.select('h1')[0].text
	text = bs2.text
	text = text[text.find('\t'):]
	text = text[:text.rfind('\n\n')]
	return text.strip(), title.strip()


def loader():
	with open('links.txt') as file:
		links = file.read().strip().split('\n')
		file.close()
	chdir('stories')
	M = set()
	for ind, x in enumerate(links):
		text, title = print_story(x)
		title = title.replace('/', '-').replace(':', '-')
		while title in M:
			title += ' (аналог)'
		title = title.title()
		M.add(title)
		print(ind + 1, title)
		with open('{}.txt'.format(title), 'w') as file:
			file.write(text)
			file.close()


def modify():
	chdir('stories')
	for x in listdir():
		rename(x, x.title()[:-4] + '.txt')


def show(title):
	system('clear')
	with open(title + '.txt') as file:
		cprint(title, 'red', attrs=['bold'])
		print(file.read())
		file.close()


def main():
	chdir('stories')
	arr = sorted([x[:-4] for x in listdir()])
	comp = WordCompleter(arr, ignore_case=True, match_middle=True)
	while True:
		try:
			s = prompt('>> ', completer=comp)
			try:
				show(s)
			except FileNotFoundError:
				cprint('История Не Найдена', 'red')
		except KeyboardInterrupt:
			break


if __name__ == '__main__':
	main()