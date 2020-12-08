#!/usr/bin/env python

import re

s=''
with open('stm32f103xb.h') as f:
  s = f.read()

peripheral = []

for m in re.finditer(r"#define\s+(\w+)\s+\(\((\w+)\s+\*\)(\w+)", s, re.MULTILINE | re.DOTALL):
  peripheral.append([m.group(1), m.group(2), m.group(3)])

register_set = []

for m in re.finditer(r"typedef struct\s+?\{(.*?)\}(\s+|)(\w+)\s*;", s, re.MULTILINE | re.DOTALL):
  type_name = m.group(3)
  g = m.group(1)

  res = re.sub(r".*?((uint\d*?_t)|(_TypeDef))\s+?([A-Za-z\d\[\]]+)\s*;\s*(\/\*\s*(.*?)\s*?\*\/|())", "\\4 `%`\\6\\n", g, 0, re.MULTILINE | re.DOTALL)
  y = res.split('\n')

  register = []
  register.append(type_name)

  for x in y:
    x = x.strip()
    
    if x.upper().find('RESERVED') == -1:
      z = x.split('`%`')
      if len(z) == 1:
        register.append(z[0].strip())
      else:
        k1 = z[1].strip().strip('!<').strip()
        register.append([z[0].strip(), k1])

  register_set.append(register)

for x in peripheral:
  for y in register_set:
     if x[1] == y[0]:
       print(('  /* =================================================================== [' + str(x[0]) + ' initialization block ] ').ljust(186,'=') + '*/')
       for z in y:
         if z != y[0] and z != '':
           rname = re.sub(r'(.*?)\d+', "\\1", x[0], 0, re.DOTALL)
           rgx = '#define\s+(' + rname + '_' + z[0] + '_\S*?)\s+(.*?)((.*)|())'
           init_str = x[0] + '_' + z[0] + '_INIT'
           print(('  #define ' + init_str + '   (').ljust(54) + '\\', end='') 
           def_list = []
           for c in re.finditer(rgx, s, re.MULTILINE):
             txt_comment = ''
             if c.group(4):
               txt_comment = c.group(4);
               txt_comment = txt_comment.replace('/*', '').replace('*/', '').replace('!<', '').strip()

             def_list.append([c.group(1), txt_comment])

             #print('\n    0 * ' + c.group(1).ljust(45), '|  /*', txt_comment.ljust(125), '*/\\', end='')

           for c in def_list:
             #print(def_list[-1][1])
             print('\n    0 * ' + c[0].ljust(45), '|' if def_list[-1][0] != c[0] else " ", ' /*',  c[1].ljust(125), '*/\\', end='')
           print('\n  )')
           #print('\n    0   '.ljust(55) + '\\' + '\n  )')
           print('  #if ' + init_str + ' != 0') 
           print('    ' + x[0] + '->' + z[0] + ' = ' + init_str + ';')
           print('  #endif')
           print('  #undef', init_str, end = '\n\n\n')

           

       print()

#for x in register_set:
#  for y in x:
#    print(y)

#  for x in typedef_item:
#    print(x)    

      #print('  ', z)
      #, z[0], z[1])
      #print(cmnt)
