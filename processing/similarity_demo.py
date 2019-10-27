import spacy

nlp = spacy.load("en_core_web_lg")  # make sure to use larger model!
dog = nlp("dog")
cat = nlp("cat")
banana = nlp("banana")

print(dog.similarity(cat))
