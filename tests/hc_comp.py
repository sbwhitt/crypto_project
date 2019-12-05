import sys
sys.path.append("/mnt/c/users/sbw98/Documents/Visual_Studio_2017/crypto/project/")

import numpy as np
import helpers.matrix as m
import helpers.attacks as a

def composite_key(promising):
    prom = [[int(c) for c in p.key[1:-1].split(',')] for p in promising]
    trans = np.array(prom).transpose()
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

cipher_txt = input("Enter cipher text: ")
att = a.attacks()
mat = m.matrix(cipher_txt)

keysize = input("Enter keysize: ")
for i in range(10):
    promising = att.hill_climb_full(mat, int(keysize), target=1000, verbose=False)
    mat.set_key(composite_key(promising))
    print(mat)
    print("")
