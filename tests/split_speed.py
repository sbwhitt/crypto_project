import time

def split_orig(text, start=3, end=8):
    segments = []
    n = start
    while n <= end:
        for i in range(len(text)-n+1):
            sub = text[i:i+n]
            segments.append(sub)
            # if sub in self.vocab:
            #     l = lem.lemmatize(sub)
            #     if l not in candidate.words:
            #         candidate.add_hit(l, True if self.frequent.get(l) else False)
        n += 1
    return segments

def split_new(text, start=3, end=8):
    segments = []
    for i in range(len(text)):
        for n in range(start, end+1):
            if i+n < len(text):
                sub = text[i:i+n]
                segments.append(sub)
    return segments

alph = 'abcdefghijklmnopqrstuvwxyz'

start_orig = time.time()
orig = split_orig(alph)
end_orig = time.time() - start_orig
print('original split method results:')
print(orig)
print('time elapsed: ' + str(end_orig))
print('')

start_new = time.time()
new = split_new(alph)
end_new = time.time() - start_new
print('new split method results:')
print(new)
print('time elapsed: ' + str(end_new))
print('')


