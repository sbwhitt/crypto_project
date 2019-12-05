class candidate:
    def __init__(self, key, text):
        self.key = key
        self.text = text
        self.hits = 0
        #self.lengths = 0
        self.weight = 0
        self.words = []

    def __str__(self):
        return str(self.key) + ": " + self.text
    
    def add_hit(self, word, frequent=False):
        self.words.append(word)
        self.hits += 1
        if frequent:
            self.weight = float((self.weight*(self.hits-1 if self.hits > 1 else 1) + len(word)+1)) / float(self.hits)
            #self.lengths += len(word)+1
        else:
            self.weight = float((self.weight*(self.hits-1 if self.hits > 1 else 1) + len(word))) / float(self.hits)
            #self.lengths += len(word)
        #self.weight = self.hits + self.lengths
    
    # def add_miss(self):
    #     self.hits -= 1
    #     self.weight = self.hits + self.lengths

    def get_text(self):
        return self.text
    
    def get_key(self):
        return self.key
    
    def info(self):
        print("Weight: " + str(self.weight))
        print(self)
        print("Discovered Words:")
        print(self.words)
        print("")
