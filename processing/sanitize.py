import spacy
import nltk
import re

# Deprecated
# Truecasing, from https://stackoverflow.com/questions/7706696/how-can-i-best-determine-the-correct-capitalization-for-a-word
# c.f. http://en.wikipedia.org/wiki/Truecasing
def truecase(text):
    # apply POS-tagging
    tagged_sent = nltk.pos_tag([word.lower() for word in nltk.word_tokenize(text)])
    # infer capitalization from POS-tags
    normalized_sent = [w.capitalize() if t in ["NN","NNS"] else w for (w,t) in tagged_sent]
    # capitalize first word in sentence
    normalized_sent[0] = normalized_sent[0].capitalize()
    # use regular expression to get punctuation right
    pretty_string = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
    return pretty_string

# Sentence segmentation with custom separator
def segment(raw_text, capitalize_firsts=True):
    nlp_model = spacy.load("en_core_web_sm")
    doc = nlp_model(raw_text)

    sent_array = []
    for sent in doc.sents:
        if capitalize_firsts:
            processed_sent = sent.text[0].capitalize() + sent.text[1:]
        else:
            processed_sent = sent.text
        sent_array.append(processed_sent)

    return sent_array


# Merge sent_array into segmented text blob
def merge_sent_array(sent_array, separator):
    merged_sent_txt = separator.join(sent_array) + separator
    return merged_sent_txt

# Blanket function for text sanitizing
def sanitize(raw_text):
    return merge_sent_array(segment(raw_text, True), '. ')
 