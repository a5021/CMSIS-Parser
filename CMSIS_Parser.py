#!/usr/bin/env python

import re

s=''
with open('stm32f107xc.h') as f:
  s = f.read()

for m in re.finditer(r"#define\s+(\w+)\s+\(\((\w+)\s+\*\)(\w+)", s, re.MULTILINE | re.DOTALL):
  print (m.group(1), m.group(2), m.group(3))

print()

typedef = []

for m in re.finditer(r"typedef struct\s+?\{(.*?)\}(\s+|)(\w+)\s*;", s, re.MULTILINE | re.DOTALL):
  typedef_name = m.group(3)
  #print (typedef_name + ':')
  g = m.group(1)

  #res = re.sub(r"__\w+?\s+uint\d+_t\s*(\w+);", "\\1", g, 0, re.MULTILINE | re.DOTALL)
  res = re.sub(r".*?((uint\d*?_t)|(_TypeDef))\s+?([A-Za-z\d\[\]]+)\s*;\s*(\/\*(!)(<)\s*(.*?)\s*?\*\/|())", "\\4 `%`\\8\\n", g, 0, re.MULTILINE | re.DOTALL)
  y = res.split('\n')



  typedef_item = []
  typedef_item.append(typedef_name)

  for x in y:
    x = x.strip()
    
    #cmnt = re.search(r"\/\*.*\!\<\s*(.*?)\s*\*\/", x, re.MULTILINE | re.DOTALL)
    if x.upper().find('RESERVED') == -1:
      z = x.split('`%`')
      if len(z) == 1:
        #print("  ", z[0])
        typedef_item.append(z[0].strip())
      else:
        typedef_item.append([z[0].strip(), z[1].strip()])
        #print(' ', z[0].ljust(25), z[1])

  for x in typedef_item:
    print(x)    

      #print('  ', z)
      #, z[0], z[1])
      #print(cmnt)
