d = {40: 'a', 20: 'c', 30: 'b'}

d = dict([(key, d[key]) for key in sorted(d.keys(), reverse=True)])

print(d)
