#!/bin/env python

#-*- coding: UTF-8 -*-


from __future__ import print_function
from collections import Counter

ips = []
c = Counter()
d = {}
sum_requests = 0
error_requests = 0

with open('/root/xm/access.log') as f:
    for line in f:
        ips.append(line.split()[0])
        c[line.split()[6]] += 1
        key = line.split()[8]
        d.setdefault(key,0)
        d[key] += 1
d.pop('"-"')
for key, val in d.items():
    if int(key) >= 400:
        error_requests += val
    sum_requests += val

print("PV is {0}".format(len(ips)))
print("UV is {0}".format(len(set(ips))))
print('error rate: {0:.2f}%'.format(error_requests * 100.0 / sum_requests))
print("Popular resources: {0}".format(c.most_common(10)))
