import re

output = '''Port   | Name                             Type       | Group Type
  ------ + -------------------------------- ---------- + ----- --------
  1/1    |                                  100/1000T  | Trk1  LACP
  3/1    |                                  100/1000T  | Trk4  LACP
  3/1    |                                  100/1000T  | Trk2  LACP'''

# Split the output into lines
lines = output.split('\n')

# Get TRK groups from the output
data = []
for line in lines:
    match = re.search(r'(\S+)\s+LACP', line)
    if match:
        data.append(match.group(1))

# Remove duplicates from data
data = list(set(data))

print(data)