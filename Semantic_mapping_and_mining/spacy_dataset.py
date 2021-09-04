# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import glob
import os
import uuid
import spacy
from spacy.lang.en import English
import json
import gensim
from nltk.corpus import wordnet as wn
from gensim.utils import simple_preprocess
from gensim import corpora
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
import random
from utils import cleaner
from rules import *

nltk.download('stopwords')

# Semantic language model
nlp = spacy.load('en_core_web_lg')

def write_file(write_path, metadict):
    with open(write_path, 'w') as f:
        json.dump(metadict, f, indent=1, ensure_ascii=False)

def open_file(read_path):
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data

# Metadata config file
feature_syn_dict = open_file("C:/Users/xiemp/Documents/afstudeer/features/envri_config.json")

# Domain variable config file
domain_vars = open_file('C:/Users/xiemp/Documents/afstudeer/features/domain_variables.json')

# Metadata folder to process, right now I have SeaDataNet applied.
# Please change the path for your system
files = glob.glob("C:/Users/xiemp/Documents/afstudeer/features/metadata/sdn_json/*.json")

# Intermediate save location for mapped files
write_path = "C:/Users/xiemp/Documents/afstudeer/features/processed_spacy/"


# Save location for finalised index files
write_path_nested = 'C:/Users/xiemp/Documents/afstudeer/features/remove_nested_spacy/'


feature_syn_list = [item for sublist in list(feature_syn_dict.values()) for item in sublist]
standard_features = feature_syn_dict.keys()


# %%
def open_file(read_path):
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)

def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x


# %%
#data = open_file(read_path)

def key_dict(data):
    keys = []
    for key, value in recursive_items(data):
        keys.append(key)
    clean_keys = cleaner(keys)
    key_dict= {}
    for i in range(len(clean_keys)):
        clean_key = clean_keys[i]
        key = keys[i]
        key_dict[clean_key] = key
    return key_dict

def key_zip(data):
    keys = []
    for key, value in recursive_items(data):
        keys.append(key)
    clean_keys = cleaner(keys)
    return list(zip(clean_keys,keys))


# %%


file_stats = {}
for file in files:
    file_stats[file] = os.stat(file).st_size

#biggest file is most representive of keys in all metadata
biggest_file = max(file_stats, key=file_stats.get)


# %%
data = open_file(biggest_file)
key_list = key_zip(data)
dict_of_keys = key_dict(data)
#print(list(dict_of_keys))
nlp('id').similarity(nlp('ID'))


# %%
def mapper(feature_syn_dict, dict_of_keys):
    all_matches = {}
    for word in feature_syn_dict:
        matches = {}
        token1 = nlp(word)
        for word2 in list(dict_of_keys):
            token2 = nlp(word2)
            matches[word2] = token1.similarity(token2)
        all_matches[word] = matches
    return all_matches

all_matches = mapper(feature_syn_list, dict_of_keys)


feature_match = {}
for key in all_matches:
    best_match = max(all_matches[key], key = all_matches[key].get)
    sim_score = all_matches[key][best_match]
    best_key = dict_of_keys[best_match]
    feature_match[key] = [best_key, sim_score]


condensed_dict = {}
for key, values in feature_syn_dict.items():
    condensed_dict[key] = [None, 0]
    for value in values:
        if feature_match[value][1] > condensed_dict[key][1] and feature_match[value][1] <= 1:
            condensed_dict[key] = feature_match[value]
              
feature_match = condensed_dict
feature_match

# %%




for file in files:
    data = open_file(file)
    value_dict = dict.fromkeys(standard_features, "N/A")
    for key in value_dict.keys():
        content = list(findkeys(data, feature_match[key][0]))
        value_dict[key] = content
    write_file(write_path + str(uuid.uuid4()) + ".json", value_dict)
   


# %%
def iterate_all(iterable, returned="key"):

    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if returned == "key":
                yield key
            elif returned == "value":
                if not (isinstance(value, dict) or isinstance(value, list)):
                    yield value
            else:
                raise ValueError("'returned' keyword only accepts 'key' or 'value'.")
            for ret in iterate_all(value, returned=returned):
                yield ret
    elif isinstance(iterable, list):
        for el in iterable:
            for ret in iterate_all(el, returned=returned):
                yield ret



# %%

spacy.load('en_core_web_sm')

parser = English()

en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def topic_miner(data):
    value_list = []
    text_data = []
    topic_list = []
    value_list.append(data['description'])
    value_list.append(data['abstract'])
    value_list.append(data['headline'])
    for keyword in data['keyword']:
        value_list.append(keyword)

    for line in value_list:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)

    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 10, id2word=dictionary, passes=50)

    topics = ldamodel.print_topics(num_words=1)
    for topic in topics:
        topic_list.append(topic[1][7:-1])

    data['info'] = list(set(topic_list))
    return data


# %%
def domain(data):
    domain_variables = domain_vars['ocean']
    value_list = []
    value_list.append(data['description'])
    value_list.append(data['abstract'])
    value_list.append(data['headline'])
    for keyword in data['keyword']:
        value_list.append(keyword)

    all_matches = mapper(value_list, domain_variables)
    domain_match = {}
    for key in all_matches:
        best_match = max(all_matches[key], key = all_matches[key].get)
        sim_score = all_matches[key][best_match]
        domain_match[key] = [best_match, sim_score]

    for key, value in domain_match.items():
        if value[1] > 0.75:
            data['info'].append(value[0])

    data['info'] = list(set(data['info']))
    return data



# List of files with paths in intermediate save location
processed_files = glob.glob("C:/Users/xiemp/Documents/afstudeer/features/processed_spacy/*.json")


for file in processed_files:
    #print(file)
    data = open_file(file)
    data = run_funcs(data)
    data = topic_miner(data)
    data = domain(data)
    write_file(write_path_nested + str(uuid.uuid4()) + ".json", data)
