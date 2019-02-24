#!/usr/bin/env python3.exe
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

transliter = Transliter(academic)

hangul = range(0xAC00, 0xD7A3 + 1)

for i in hangul:
  ch = chr(i)
  print(f'{ch}\t{transliter.translit(ch)}')
