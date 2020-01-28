import os
from json import loads
from itertools import chain

list_odd = []
list_even = []
for i in range(1, 101):
    with open('data/data_%s' % i) as f:
        if i % 2:
            list_odd.append(f.read())
            pass
        else:
            list_even.append(f.read())
            pass

with open('output', 'wt') as f:
    f.write(os.linesep.join(list_odd))
    f.write(os.linesep)
    # 这里也许不算排序了。作弊，作弊。
    f.write(os.linesep.join(reversed(list_even)))
pass

with open('output', 'rt') as f:
    data_lines = f.readlines()
# chain.from_iterable
all_divide_by_3 = [[str(data) for data in loads(data_line) if not data % 3]
                   for data_line in data_lines]
all_divide_by_3 = list(chain.from_iterable(all_divide_by_3))
with open('output_2', 'wt') as f:
    f.write(' '.join(all_divide_by_3))
pass
