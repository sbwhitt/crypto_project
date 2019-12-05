'''
this test allows the comparison of hill climb attack performance
used to compare different parameters
plaintext is provided to score results of attacks
'''
import sys
sys.path.append("/mnt/c/users/sbw98/Documents/Visual_Studio_2017/crypto/project/")

import string
from difflib import SequenceMatcher
import helpers.matrix as m
import helpers.attacks as a

plain = "This project will be implemented using python as its driving languageMultiple python classeswill be made to represent and utilize different types of cryptanalysis. The base functionality willconsist of an interface for the user to cycle through permutations of a given key while alsosuggesting potential candidates through the examination of the cipher text for common patterns.For low key sizes (number of columns less than 10), all keys will be tries and analyzed forcommon patterns. For larger keys, hill climbing will be used in an attempt to reach a potentialcandidate for a correct key. Additionally, n-gram frequency and english word similarities will beused to help the user in deciphering the text"
plain = plain.replace(" ", "")
plain = plain.lower().translate(str.maketrans('', '', string.punctuation))

cipher = "EhaserylnciaititnhsnyuceiyaeitlsuwtttwfeosaxrnelatlioaleihhEuiydiruihpknsockmlflnmckfoedimttlnpelchagdmefokarcaeoygsuttightepcturyphomysbrrwTnyedscsesildeblerggiixofelnlnnrnlwsejdvpalcfsthnieirwuidrieltmwbnwnloodttosmworfmslecgitdaqseibtuarelaiotethcasteoeeattclhrpamsntsyrlsoceerbadtidpradtttheiliayhiatfunatsrlnelntclneeEcsntezynseeegtnoenloagpaerrueiogssesityolahptuaapsshfoarlnpndpbusacfoiedntrcyysiatRgiiexiganriaifeuhtotoietoeloiduidpoeiemifenrgetttoolweobtacahlilyglpfanntalngepesimkbEainioemneeenitecnslehemnnaheaonnipgrtrletosoouvsaafloszfmtierslrtlpncefnoartieuhnzsrmrlrddemth"

print("base similarity between plain and cipher text: ")
print(SequenceMatcher(None, cipher, plain).ratio())
print("")

mat = m.matrix(cipher)
att = a.attacks(frequent=False)

keysize = 10
# trials = 10000

first_res = []
second_res = []
for i in range(3):
    print("starting round " + str(i))
    print("finding candidates for hill climb attack with target trials: " + str(1000))
    first = att.hill_climb(mat, int(keysize), target=1000)
    print("finding candidates for hill climb attack with target trials: " + str(10000))
    second = att.hill_climb(mat, int(keysize), target=10000)

    first_rank = 0.0
    for r in first:
        first_rank += SequenceMatcher(None, r.text, plain).ratio()

    second_rank = 0.0
    for r in second:
        second_rank += SequenceMatcher(None, r.text, plain).ratio()
    
    first_res.append((first_rank, float(first_rank/len(first))))
    second_res.append((second_rank, float(second_rank/len(second))))
    print("round finished\n")

print("")
print("total similarity for first hill climb trials (trial total, trial avg): ")
for t in first_res:
    print(t)
print("")
print("total similarity for second hill climb trials (trial total, trial avg): ")
for t in second_res:
    print(t)
