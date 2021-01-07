import re

regex = r"[/][*][*][^*].{,10}?@addtogroup Peripheral_registers_structures.{,15}@{.{,10}?[*][/]\s+(.*?)\s+[/][*][*][^*].{,10}?@}.{,10}?[*][/]"

# with open('stm32l053xx.h') as f:
# with open('stm32f103xb.h') as f:

with open('stm32f479xx.h') as f:
    s = f.read()

m = re.findall(regex, s, re.MULTILINE | re.DOTALL)
for x in m:
    print(x)

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
