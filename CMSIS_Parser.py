#!/usr/bin/env python

import re

rgx = r"#define\s+(\w+)\s+\(\((\w+)\s+\*\)(\w+)"

s=''
with open('stm32f103xg.h') as f:
  s = f.read()

m = re.finditer(rgx, s, re.MULTILINE | re.DOTALL)

for n in m:
  print (n.group(1), n.group(2), n.group(3))

print()

rgx = r"typedef struct\s+?\{(.*?)\}(\s+|)(\w+)\s*;"

m = re.finditer(rgx, s, re.MULTILINE | re.DOTALL)
for n in m:
  print (n.group(3) + ':', end='')
  g = n.group(1)
  subst = "\\1"

  res = re.sub(r"__\w+?\s+uint\d+_t\s*(\w+);", subst, g, 0, re.MULTILINE | re.DOTALL)
  y = res.split('\n')

  for x in y:
    if x.find('RESERVED') == -1:
      print(x)
