import numpy as np

promising = [[int(c) for c in line[1:-2].split(',')] for line in open('promising.txt', 'r')]

def composite_key(promising):
    trans = np.array(promising).transpose()
    frequent = []
    for t in trans:
        res = np.unique(t, return_counts=True)
        a, b = zip(*sorted(zip(res[1], res[0]), reverse=True))
        frequent.append(b)

    key = []
    for f in frequent:
        i = 0
        current = f[i]
        while current in key:
            i += 1
            if i < len(f):
                current = f[i]
            else:
                break
        if i >= len(f):
            for i in range(len(frequent)):
                if i not in key:
                    key.append(i)
        else:
            key.append(current)
    return key

print(composite_key(promising))