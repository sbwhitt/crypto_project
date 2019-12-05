import math
import random as r

class matrix:
    def __init__(self, plaintext, key=[0,1]):
        self.plaintext = plaintext.lower().strip().replace(" ", "")
        self.key = key
        self.matrix = self.__build_matrix()

    def __str__(self):
        string = ""
        for k in self.key:
            string += str(k) + " "
        string += "\n"
        for i in range(len(self.matrix[0])):
            for j in self.key:
                if i < len(self.matrix[j]):
                    string += self.matrix[j][i]
            string += "\n"
        return string

    def __build_matrix(self):
        n = len(self.plaintext)
        cols = len(self.key)
        rows = int(n / cols)
        full_rows = n % cols
        columns = {}
        for k in self.key:
            columns[k] = rows+1 if full_rows > 0 else rows
            full_rows -= 1
        pos = 0
        mat = ["" for i in range(cols)]
        for i in range(cols):
            l = int(columns.get(i))
            mat[i] = (self.plaintext[pos:pos+l] if l == rows+1 else self.plaintext[pos:pos+l]+" ")
            pos += l
        return mat
    
    def __base_key(self, n):
        return [i*1 for i in range(n)]

    def __next_key(self):
        self.key = self.__base_key(len(self.key)+1)
        self.matrix = self.__build_matrix()

    def next_permutation(self):
        i = len(self.key)-2
        while not (i < 0 or self.key[i] < self.key[i+1]):
            i -= 1
        if i < 0:
            self.__next_key()
            return False
        j = len(self.key)-1
        while not (self.key[j] > self.key[i]):
            j -= 1
        self.key[i], self.key[j] = self.key[j], self.key[i]
        self.key[i+1:] = reversed(self.key[i+1:])
        self.matrix = self.__build_matrix()
        return True

    def text(self):
        ret = ""
        for i in range(len(self.matrix[0])):
            for j in self.key:
                if i < len(self.matrix[j]) and self.matrix[j][i] != " ":
                    ret += self.matrix[j][i]
        return ret
    
    def key_size(self):
        return len(self.key)
    
    def current_key(self):
        return str(self.key)
    
    def set_key_size(self, keysize):
        self.key = self.__base_key(keysize)
        self.matrix = self.__build_matrix()
    
    def set_key(self, key):
        self.key = key
        self.matrix = self.__build_matrix()
    
    def shuffle_key(self):
        r.shuffle(self.key)
        self.matrix = self.__build_matrix()
    
    def get_matrix(self):
        return self.matrix
