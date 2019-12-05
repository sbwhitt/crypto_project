import os
import random as r
import helpers.candidate as c
from nltk.corpus import words as english
from nltk.stem import WordNetLemmatizer
from difflib import SequenceMatcher
from copy import copy
from sys import platform

lem = WordNetLemmatizer()

class attacks:
    def __init__(self, frequent=True):
        self.vocab = set(w.lower() for w in english.words())
        self.freq_exists = frequent
        if self.freq_exists:
            self.frequent = self.__build_frequent()
    
    # builds frequent word dict if frequent.txt provided
    def __build_frequent(self):
        words = [line.strip().lower() for line in open("./resources/frequent.txt", "r")]
        frequent = {}
        for w in words:
            word = w[:w.find("\t")]
            frequent[word] = word
        return frequent

    # searches through nltk corpus for matching words
    # splits given candidate plaintext into all ngrams in range start, end inclusive
    # lemmatizes found words to prevent false inflation of candidate weight
    def __dict_search(self, candidate, start=3, end=10):
        text = ""
        text = candidate.get_text()
        n = start
        while n <= end:
            for i in range(len(text)-n+1):
                sub = text[i:i+n]
                if sub in self.vocab:
                    l = lem.lemmatize(sub)
                    if l not in candidate.words:
                        candidate.add_hit(l, True if self.freq_exists and self.frequent.get(l) else False)
            n += 1

    # mutates provided key, more change based on entropy value
    def __mutate_key(self, key, entropy=1):
        choice = r.randint(0, 3)
        choice = 2
        if choice == 0:
            #rotate by one
            rot_amount = r.randint(1, entropy)
            key = key[rot_amount:] + key[:rot_amount]
        elif choice == 1:
            #slice on random index
            for i in range(entropy):
                i = r.randint(0, len(key)-1)
            key = key[i:] + key[:i]
        elif choice == 2:
            #swap 2 random elements
            for i in range(entropy):
                i = r.randint(0, int((len(key)-1)/2))
                j = r.randint(int((len(key)-1)/2+1), len(key)-1)
                key[i], key[j] = key[j], key[i]
        elif choice == 1:
            #move element to random destination
            target = r.randint(0, int((len(key)-1)/2))
            dest = r.randint(int((len(key)-1)/2+1), len(key)-1)
            for i in range(entropy):
                moved = key[target]
                key = key[:target] + key[target+1:]
                key = key[:dest] + [moved] + key[dest:]
        return key

    # brute force attack that cycles through all keys for given key size
    # returns highest weighted candidate
    def brute_force(self, mat, keysize):
        mat.set_key_size(keysize)
        can = c.candidate(mat.current_key(), mat.text())
        highest = can
        while mat.key_size() < keysize+1:
            self.__dict_search(can)
            if can.weight > highest.weight:
                highest = can
            mat.next_permutation()
            can = c.candidate(mat.current_key(), mat.text())
        return highest

    # hill climb attack, continues finding candidates until it collects <n_results> promising candidates
    # if no improvement in candidate weight after <target> iterations, process restarts with new random key
    def hill_climb(self, mat, keysize, target=1000, n_results=10, verbose=False):
        mat.set_key_size(keysize)
        mat.shuffle_key()
        initial = c.candidate(mat.current_key(), mat.text())
        self.__dict_search(initial)
        if verbose:
            print("Starting Hill Climb Search for key size " + str(keysize))
            print("Initial Candidate:")
            initial.info()
        max_weight = 0
        promising = []
        last = current = initial
        trials = 0
        while 1:
            trials += 1
            entropy = int((max_weight-current.weight)*10)
            key_copy = self.__mutate_key(copy(mat.key), entropy+1 if entropy > 0 else 1)
            mat.set_key(key_copy)
            current = c.candidate(mat.current_key(), mat.text())
            self.__dict_search(current)
            if current.weight > last.weight and len(current.words) > len(last.words):
                last = current
                if last.weight > max_weight:
                    max_weight = last.weight
                if verbose:
                    os.system('cls') if platform == "win32" else os.system('clear')
                    print("Current Candidate:")
                    current.info()
                    print("\nPromising candidates found for keysize " + str(keysize) + ": (" + str(len(promising)) + "/" + str(n_results) + ")")
                    print("Current entropy: " + str(entropy))
            if trials > target and current.weight < last.weight:
                promising.append(last)
                if len(promising) == n_results:
                    if verbose:
                        os.system('cls') if platform == "win32" else os.system('clear')
                    return promising
                trials = 0
                mat.shuffle_key()
                current = c.candidate(mat.current_key(), mat.text())
                last = current
