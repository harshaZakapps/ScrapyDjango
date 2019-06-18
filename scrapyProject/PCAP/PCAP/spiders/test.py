import re
numeric = '$1,099.99'
print(re.sub(r"[^0-9.]+", '', numeric))
print(numeric)