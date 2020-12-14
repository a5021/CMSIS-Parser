#!/usr/bin/env python

import re, sys, os, urllib.request

def split_def(s):
    a = s[0]
    b = s[1].split('/*')
    c = b[1].strip('!<').strip('*/').strip() if len(b) > 1 else ''
    b = b[0].strip()
    return [a, b, c]

def replace_def(a, b):
  for x in a:
    for y in b:
      x[1] = x[1].replace(y[0].strip(), y[1].strip())
  return a


def get_register_bitset(src, register):

  rgx=r'#define\s+(' + register + '\S+)\s+(.*)'

  pos  = []
  msk  = []
  defs = []

  kc = re.findall(rgx, src, re.MULTILINE)
  for x in kc:
    if x[0].endswith('_Pos'):
      pos.append([x[0].strip(), x[1].strip()])
    elif x[0].endswith('_Msk'):
      msk.append(split_def(x))
    else:
      defs.append(split_def(x))

  replace_def(msk, pos)  
  replace_def(defs, pos)

  res = [[x[0], '', x[1], x[2]] for x in defs]

  for x in res:
    for y in msk:
      p = x[2].replace(y[0].strip(), y[1].strip())
      if p != x[2]:
        x[1] = y[2] if len(y) > 2 else ''
      x[2] = p

  return res

def make_init_block(src, register_name):
  reg = register_name.split("->")
  reg[0] = re.sub(r"([a-zA-Z]+)(\S*)", "\\1", reg[0], 1)
  r = get_register_bitset(src, reg[0] + '_' + reg[1] + '_')

  def_name = reg[0] + '_' + reg[1] + "_INIT"

  str_out = ("  #define " + def_name + "  (").ljust(42) + " \\\n"

  for x in r:
    str_out += "    0 * " + (x[0].ljust(35) + (' ' if x[0] == r[-1][0] else '|') + '  /* ' + ' ' + x[1] + ' ' + x[2].ljust(18) + ' ' + x[3].ljust(60)).ljust(137) + '  */\\\n'

  str_out += "  )\n"
  str_out += "  #if " + def_name + " != 0\n"
  str_out += "    " + register_name + " = " + def_name + ";\n"
  str_out += "  #endif\n"
  str_out += "  #undef " + def_name + "\n"
  return str_out

def get_registers(s, peripheral):
  for x in re.findall(r'typedef struct\s+{\s+(.*?)}\s*(\S+)\s*;', s, re.MULTILINE | re.DOTALL):
    if x[1] == peripheral:
      res = re.sub(r".*?((uint\d*?_t)|(_TypeDef))\s+?([A-Za-z\d\[\]]+)\s*;\s*(\/\*\s*(.*?)\s*?\*\/|())", "\\4 `%`\\6\\n", x[0], 0, re.MULTILINE | re.DOTALL)
      r_list = res.split('\n')
      res = [x.split('`%`') for x in r_list if len(x) > 1]
      return [[x[0].strip(), x[1].strip('!<').strip()] for x in res if not 'RESERVED' in x[0].upper() and len(x) > 1]
     
peripherals    = lambda s: re.findall('#define\s+?(\w+)\s+\(\((\w+(?:_TypeDef|_GlobalTypeDef))\s+\*.*?(\w+_BASE.*)\)', s, re.MULTILINE)
register_block = lambda s: [[x[0], get_registers(s, x[1])] for x in peripherals(s)]

def init_peripheral(src, peripheral):
  str_out = ''
  for x in register_block(src):
    if x[0] == peripheral:
      for y in x[1]:
        str_out += make_init_block(s, x[0] + '->' + y[0]) + '\n'
      str_out += '\n'
      return str_out

def init_all(src):
  str_out = ''
  for x in register_block(src):
    for y in x[1]:
      str_out += make_init_block(s, x[0] + '->' + y[0]) + '\n'
    str_out += '\n'
  return str_out

if __name__ == "__main__":

  if len(sys.argv) < 2:
    print(f"Parameters missing.\n\nUSAGE: {os.path.split(sys.argv[0])[1]} <header_file> <register_name>")
    exit()

  s = ''
  buf = ''
  src_file_name = sys.argv[1]
  url = 'https://raw.githubusercontent.com/STMicroelectronics/STM32Cube' + src_file_name[5:7].upper() + '/master/Drivers/CMSIS/Device/ST/STM32' + src_file_name[5:7].upper() + 'xx/Include/' + src_file_name

  while True:
    try:
      with open(src_file_name) as f:
        s = f.read()
        break
    except:
      web_file = urllib.request.urlopen(url)
      try:
        buf = web_file.read()
      except:
        print('unable to open %s' % url)
        exit()
      try:
        open(src_file_name, 'wb').write(buf)
      except:
        print("unable to create local copy of %s" % src_file_name)
        exit()

  if sys.argv[2].upper() == "ALL":
    print(init_all(s))
  elif not '->' in sys.argv[2]:
    print(init_peripheral(s, sys.argv[2]))
  else:
    print(make_init_block(s, sys.argv[2]))
