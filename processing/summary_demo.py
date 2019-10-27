from summa.summarizer import summarize
from summa import keywords

with open("../resources/how_trees_bend_the_law_of_physics.txt") as f:
    text = f.read()

print(text)
print(keywords.keywords(text))
print(summarize(text, language='english'))
