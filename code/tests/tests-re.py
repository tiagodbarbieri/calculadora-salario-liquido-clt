# Tests with regular expressions
import re

numbers = """
----int iso----
1234
256.684
56.569
7.989.584
----int usa----
1967
2,698
98,957
9,568,69
---float iso---
9875.523
1,777.5
1,987,234.5
---float usa---
1234,5
1.234,536
1.987.234,5
--not ok numbers--
1234.
1234.123.12
1234,
.123
,123
um
dois
"""
# For int numbers
print(re.findall(r"^\d+$", numbers, re.MULTILINE))
print(re.findall(r"^[0-9]+$", numbers, re.MULTILINE))

# For float numbers
print(re.findall(r"^\d+[\.|,]\d+$", numbers, re.MULTILINE))
print(re.findall(r"^[0-9]+[\.|,][0-9]+$", numbers, re.MULTILINE))
