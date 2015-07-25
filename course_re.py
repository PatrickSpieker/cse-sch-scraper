import re

p = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
print(p.findall("' BIOEN 401, BIOEN 423, E E 423, or CSE 486. ',"))
