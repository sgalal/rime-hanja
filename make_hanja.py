#!/usr/bin/env python3.exe
import sqlite3
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

###################################
### Check if a character is CJK ###
###################################

# https://stackoverflow.com/a/52837006
cjk_ranges = \
  [ ( 0x4E00,  0x62FF), ( 0x6300,  0x77FF), ( 0x7800,  0x8CFF), ( 0x8D00,  0x9FCC)
  , ( 0x3400,  0x4DB5), (0x20000, 0x215FF), (0x21600, 0x230FF), (0x24600, 0x260FF)
  , (0x26100, 0x275FF), (0x27600, 0x290FF), (0x29100, 0x2A6DF), (0x2A700, 0x2B734)
  , (0x2B740, 0x2B81D), (0x2B820, 0x2CEAF), (0x2CEB0, 0x2EBEF), (0x2F800, 0x2FA1F)
  ]

def is_cjk(ch):
  char = ord(ch)
  return any(char in range(bottom, top + 1) for bottom, top in cjk_ranges)

################
### Romanize ###
################

transliter = Transliter(academic)

rom_memo = {}

def rom(ch):
  memoed = rom_memo.get(ch, None)
  if memoed:
    return memoed
  else:
    res = transliter.translit(ch)
    rom_memo[ch] = res
    return res

def rom_all(str):
  return ' '.join(rom(ch) for ch in str)

###############
### Process ###
###############

conn = sqlite3.connect('hanjadic.sqlite')
cur = conn.cursor()

# Single character
for i in cur.execute('SELECT hanjas, hangul FROM korean_pronunciation;'):
  hanjas, hangul = i[0].split(' '), i[1]
  for hanja in hanjas:
    if len(hanja) == 1 and is_cjk(hanja):
      rom(hangul)
      print(f'{hanja}\t{hangul}')

# Words
for i in cur.execute('SELECT c0hanja, c1hangul FROM hanjas_content;'):
  hanja, hangul = i[0], i[1]
  if ('-' not in hanja) and (len(hanja) == len(hangul)):
    rom_all(hangul)
    print(f"{hanja}\t{' '.join(hangul)}")

conn.close()

for k, v in rom_memo.items():
  print(f'    - xform/{k}/{v}/')
