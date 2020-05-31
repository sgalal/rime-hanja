#!/usr/bin/env python3

import os
import re
import sqlite3
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

# Check CJK
# https://ayaka.shn.hk/hanregex/

han_regex = re.compile(r'[\u3006\u3007\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\U0002ceb0-\U0002ebef\U00030000-\U0003134f]')

def is_cjk(c):
	'''Check if a character is CJK'''
	return bool(han_regex.match(c))

# To hangul

to_hangul = Transliter(academic).translit

rom_memo = {}

def rom(c):
	'''Romanize'''
	memoed = rom_memo.get(c, None)
	if memoed:
		return memoed
	else:
		res = to_hangul(c)
		rom_memo[c] = res
		return res

def rom_all(str):
	return ' '.join(rom(ch) for ch in str)

# Main

def main():
	db_path = 'hanjadic.sqlite'

	if not os.path.exists(db_path):
		raise Exception('Please download the database from https://github.com/dbravender/hanja-dictionary')

	conn = sqlite3.connect(db_path)
	cur = conn.cursor()

	with open('1.txt', 'w') as f:
		# Single characters
		for hanjas, hangul in cur.execute('SELECT hanjas, hangul FROM korean_pronunciation;'):
			for hanja in hanjas.split(' '):
				if len(hanja) == 1 and is_cjk(hanja):
					rom(hangul)
					print(hanja + '\t' + hangul, file=f)

		# Words
		for hanja, hangul in cur.execute('SELECT c0hanja, c1hangul FROM hanjas_content;'):
			if ('-' not in hanja) and (len(hanja) == len(hangul)):
				rom_all(hangul)
				print(hanja + '\t' + ' '.join(hangul), file=f)

	conn.close()

	with open('2.txt', 'w') as f:
		for k, v in rom_memo.items():
			print(f'  - xform/{k}/{v}/', file=f)

if __name__ == "__main__":
	main()
