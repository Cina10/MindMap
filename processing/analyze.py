from textacy import preprocessing
import textacy.ke.textrank
import numpy as np
import spacy

# Deprecated
# Preprocess text
def preprocess(text):
    return preprocessing.normalize_whitespace(preprocessing.remove_punctuation(text))

# Make a SpaCy doc given text
def make_doc(text):
    return textacy.make_spacy_doc(text)

# Perform TextRank analysis
# c.f. Mihalcea, R., Tarau, P.: "Textrank: Bringing order into texts". In: Lin, D., Wu, D. (eds.) Proceedings of EMNLP 2004. pp. 404–411. Association for Computational Linguistics, Barcelona, Spain. July 2004.
def textrank(text, topn):
    return textacy.ke.textrank(make_doc(text), normalize="lemma", window_size=10, edge_weighting="count", position_bias=False, topn=topn)

# Find pairwise similarity between keywords. Assumes a [(kw, weight), ...] structure
def similarity(kw_w_pairs):
    nlp = spacy.load("en_core_web_lg")
    keywords = [p[0] for p in kw_w_pairs]
    n = len(keywords)
    adj_mat = np.full((n, n), None)
    for i in range(n):
        for j in range(i, n):
            doc_i = nlp(keywords[i])
            doc_j = nlp(keywords[j])
            adj_mat[i, j] = doc_i.similarity(doc_j)
    
    return adj_mat