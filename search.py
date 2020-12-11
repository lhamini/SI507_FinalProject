import json
import nltk
import query
import pandas as pd
from flask import request
from nltk.corpus import stopwords
from nltk.stem import 	WordNetLemmatizer
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi, BM25L, BM25Plus
CACHE_FILENAME = "doc_cache.json"
S = set(stopwords.words('english'))

wordnet_lemmatizer = WordNetLemmatizer()
ps =PorterStemmer()

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = dict(query.crash_documents())
        save_cache(cache_dict)
    return cache_dict


def remove_stopwords(tokens):
    tokens_stop_removed = []
    for token in tokens:
        #token = wordnet_lemmatizer.lemmatize(token)
        token = ps.stem(token)
        if not token.lower() in S:
            tokens_stop_removed.append(token)
    return tokens_stop_removed

def corpus_index():
    cache_dict = open_cache()
    corpus = list(cache_dict.values())
    tokenized_corpus = [remove_stopwords(str(doc).split(" ")) for doc in corpus]
    bm25plus = BM25Okapi(tokenized_corpus)
    return corpus, bm25plus, cache_dict
