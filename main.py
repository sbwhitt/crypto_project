print("Starting application. Please wait...")

import os
import re
import numpy as np
import helpers.matrix as m
import helpers.attacks as a
import helpers.candidate as cand
import string
from copy import copy
from sys import platform

# loading nltk data
import nltk
res_dir = os.path.dirname(os.path.realpath(__file__)) + '/resources'
nltk.data.path.append(res_dir)
FREQUENT = True
if not os.path.exists(res_dir):
    FREQUENT = False
    nltk.download('words', download_dir=res_dir)
    nltk.download('wordnet', download_dir=res_dir)

comma_list_reg = r'(([0-9]+\,\s*)+([0-9]+))'

# loading hill climb settings
HC_SINGLE_RESULT_AMNT = 25
HC_RANGE_RESULT_AMNT = 10
HC_SINGLE_WAIT_AMNT = 1000
HC_RANGE_WAIT_AMNT = 1000
settings_path = os.path.dirname(os.path.realpath(__file__)) + '/settings.py'
if os.path.exists(settings_path):
    import settings
    HC_SINGLE_RESULT_AMNT = settings.HC_SINGLE_RESULT_AMNT
    HC_RANGE_RESULT_AMNT = settings.HC_RANGE_RESULT_AMNT
    HC_SINGLE_WAIT_AMNT = settings.HC_SINGLE_WAIT_AMNT
    HC_RANGE_WAIT_AMNT = settings.HC_RANGE_WAIT_AMNT

#misc helper functions

def is_valid_key(key):
    for i in range(len(key)):
        if i not in key:
            return False
    return True

def str_to_tuple(s):
    return (int(s.split(',')[0]), int(s.split(',')[1]))

def str_to_list(s):
    return [int(c) for c in s.split(',')]

# builds composite key based on the most common key positions found in promising list
def composite_key(promising, additional=None):
    prom = [[int(c) for c in p.key[1:-1].split(',')] for p in promising]
    if additional:
        prom.append(additional)
    trans = np.array(prom).transpose()
    frequent = []
    for t in trans:
        res = np.unique(t, return_counts=True)
        _, b = zip(*sorted(zip(res[1], res[0]), reverse=True))
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

# main user input loop
def menu(mat, att):
    help_msg = '''\nhelp    Displays help info
m       Display current matrix
t       Display current matrix plaintext
n       Change to next permutation of key and display new matrix
k       Changes current key size
kf      Changes current key to inputted key (comma separated list)
b       Brute force attack for single key size or key size range
h       Hill Climb attack for single key size or key size range
q       Quit program\n'''

    print("Please enter your desired input\n")
    print(help_msg)
    inp = ""
    while inp != "q":
        inp = input(">>")

        if inp == "help":
            print(help_msg)

        elif inp == "n":
            mat.next_permutation()
            print(mat)

        elif inp == "m":
            print(mat)

        elif inp == "t":
            print(mat.text())

        elif inp == "k":
            keysize = input("Enter key size: ")
            try:
                keysize = int(keysize)
                if keysize < 0 or keysize > len(mat.text()):
                    print("Error. Invalid input for key size.")
                    continue
                mat.set_key_size(int(keysize))
            except ValueError:
                print("Error. Invalid input for key size.")
                continue

        elif inp == "kf":
            key = input("enter full key: ")
            res = re.search(comma_list_reg, key)
            if res:
                key_list = str_to_list(res.group(1))
                if is_valid_key(key_list):
                    mat.set_key(key_list)
                    continue
            print("Error. Invalid full key input.")

        elif inp == "b":
            promising = []
            keysize = input("Enter key size (single or range): ")
            res = re.search(comma_list_reg, keysize)
            if res:
                key_range = str_to_tuple(res.group(1))
                for i in range(key_range[0], key_range[1]+1):
                    keysize = i
                    highest = att.brute_force(mat, int(keysize))
                    print("Most promising candidate:")
                    print(highest)
                    print("Total words: " + str(len(highest.words)))
                    print("")
            else:
                highest = att.brute_force(mat, int(keysize))
                print("Most promising candidate:")
                print(highest)
                print("Total words: " + str(len(highest.words)))
                print("")

        elif inp == "h":
            keysize = input("Enter key size (single or range): ")
            res = re.search(comma_list_reg, keysize)
            if res:
                key_range = str_to_tuple(res.group(1))
                results = []
                for i in range(key_range[0], key_range[1]+1):
                    promising = att.hill_climb(mat, i, target=HC_RANGE_WAIT_AMNT, verbose=True, n_results=HC_RANGE_RESULT_AMNT)
                    highest = promising[0]
                    for p in promising:
                        if p.weight > highest.weight:
                            highest = p
                    results.append((highest, i))
                os.system('cls') if platform == "win32" else os.system('clear')
                print("Hill climb search for key sizes " + str(key_range) + " finished.\n")
                for r in results:
                    print("Most promising candidate for key size " + str(r[1]) + ": ")
                    r[0].info()
                continue
            try:
                keysize = int(keysize)
                if keysize < 0 or keysize > len(mat.text()):
                    print("Error. Invalid input for key size.")
                    continue
            except ValueError:
                print("Error. Invalid input for key size.")
                continue

            try:
                promising = att.hill_climb(mat, int(keysize), target=HC_SINGLE_WAIT_AMNT, verbose=True, n_results=HC_SINGLE_RESULT_AMNT)
                os.system('cls') if platform == "win32" else os.system('clear')
            except KeyboardInterrupt:
                os.system('cls') if platform == "win32" else os.system('clear')
                print("Cancelled hill climb search.\n")
                continue
            highest = promising[0]
            print("\nMost Promising Candidates:\n")
            if promising:
                for p in promising:
                    if p.weight > highest.weight:
                        highest = p
                    p.info()
            k = composite_key(promising)
            mat.set_key(k)
            print("\nComposite key built from promising candidates:")
            print(mat)
            print("\nHighest ranked candidate:")
            print(highest.info())

        elif inp != "q":
            print("\nUnknown input.")
            print(help_msg)

if __name__ == '__main__':
    cipher_txt = ''
    os.system('cls') if platform == "win32" else os.system('clear')
    print("Application started successfully.\n")
    if len(os.sys.argv) == 1:
        print("No input file provided for cipher text. Please enter cipher text manually.")
        cipher_txt = input("Enter cipher text: ")
    else:
        try:
            print('Opening provided cipher text file...')
            cipher_txt = ''.join([line for line in open(os.sys.argv[1])])
        except FileNotFoundError:
            print("Error. File, \'" + os.sys.argv[1] + "\' not found.")
            os.sys.exit()

    print("\nInitializing attacks...")
    att = a.attacks(frequent=FREQUENT)
    print("Building cipher matrix...")
    mat = m.matrix(cipher_txt)
    print("Initialization complete\n")
    
    menu(mat, att)
