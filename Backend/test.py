from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

dog=wn.synsets('dog', pos=wn.NOUN)[0] #get the first noun synonym of the word "dog"
cat=wn.synsets('cat', pos=wn.NOUN)[0]
rose=wn.synsets('rose', pos=wn.NOUN)[0]
flower=wn.synsets('flower', pos=wn.NOUN)[0]

brown_ic = wordnet_ic.ic('ic-brown.dat') #load the brown corpus to compute the IC

# print(rose.res_similarity(flower, brown_ic))
# print(rose.res_similarity(dog, brown_ic))
# print(cat.res_similarity(dog, brown_ic))
