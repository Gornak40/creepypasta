#!/bin/python3
from pprint import pprint
from termcolor import cprint
from os import chdir, listdir, rename, system
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


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