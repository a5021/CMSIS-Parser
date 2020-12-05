#!/usr/bin/env python

import re

s=''
with open('stm32f107xc.h') as f:
  s = f.read()

for m in re.finditer(r"#define\s+(\w+)\s+\(\((\w+)\s+\*\)(\w+)", s, re.MULTILINE | re.DOTALL):
  print (m.group(1), m.group(2), m.group(3))

print()

for m in re.finditer(r"typedef struct\s+?\{(.*?)\}(\s+|)(\w+)\s*;", s, re.MULTILINE | re.DOTALL):
  print (m.group(3) + ':', end='')
  g = m.group(1)

  res = re.sub(r"__\w+?\s+uint\d+_t\s*(\w+);", "\\1", g, 0, re.MULTILINE | re.DOTALL)
  y = res.split('\n')

  for x in y:
    if x.upper().find('RESERVED') == -1:
      print(x)
