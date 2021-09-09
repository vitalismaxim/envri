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
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import random
#from utils import cleaner
#from rules import *
import importlib


#nltk.download('stopwords')
parser = English()
en_stop = set(nltk.corpus.stopwords.words('english'))



# Semantic language model
nlp = spacy.load('en_core_web_lg')


def cleaner(lst):
    cleaned_list = []
    for feature in lst:
        #print(feature)
        if ":" in feature:
            clean = re.split(':(.*)', feature)
            if len(clean) > 1:
                clean = clean[1]
            else:
                clean = clean[0][1:]
        else:
            clean = feature
        
        #clean = clean.replace("_", " ")
        clean = re.sub("([a-z])([A-Z])","\g<1> \g<2>",clean)
        clean = clean.lower()
        clean = ''.join([i for i in clean if i.isalpha() or i.isspace()])
        if len(clean) <= 3:
            cleaned_list.append(clean)
        elif clean[2] == '_':
            #print(feature, clean[3:])
            cleaned_list.append(clean[3:])
        else:
            cleaned_list.append(clean)
        
    return cleaned_list


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

def write_file(write_path, metadict):
    with open(write_path, 'w') as f:
        json.dump(metadict, f, indent=1, ensure_ascii=False)

    
def write_file(write_path, metadict):
    with open(write_path, 'w') as f:
        json.dump(metadict, f, indent=1, ensure_ascii=False)

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

def topic_miner(data, lda_passes = 50):
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

    if len(value_list) == 0 or len(text_data) == 0:
        return []

    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    try:
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 10, id2word=dictionary, passes=lda_passes)
    except:
        return []

    topics = ldamodel.print_topics(num_words=1)
    for topic in topics:
        topic_list.append(topic[1][7:-1])

    data['info'] = list(set(topic_list))
    return data


domain_vars = open_file('C:/Users/xiemp/Documents/afstudeer/features/domain_variables.json')


def domain(data, threshold = 0):
    domain_variables = domain_vars['ocean']
    value_list = []
    try: value_list.append(data['description']) 
    except: pass
    try: value_list.append(data['abstract'])
    except: pass
    try: value_list.append(data['headline'])
    except: pass
    try:
        for keyword in data['keyword']:
            value_list.append(keyword)
    except: pass

    all_matches = mapper(value_list, domain_variables)
    domain_match = {}
    for key in all_matches:
        best_match = max(all_matches[key], key = all_matches[key].get)
        sim_score = all_matches[key][best_match]
        domain_match[key] = [best_match, sim_score]

    for key, value in domain_match.items():
        if value[1] > threshold:
            data['info'].append(value[0])

    data['info'] = list(set(data['info']))
    return data

def biggest(files):
    file_stats = {}
    for file in files:
        file_stats[file] = os.stat(file).st_size

    #biggest file is most representive of keys in all metadata
    biggest_file = max(file_stats, key=file_stats.get)
    return biggest_file


def choose_folder_metadata(self):
    self.metadata_directory.set(askdirectory())
    file_path = self.metadata_directory.get() + '/*.json'
    self.found_files = glob.glob(file_path)
    #print('location:', file_path)
    #print('files:', found_files)
    for file in self.found_files:
        self.file_box.insert(-1, file)
    
    self.files = tk.Listbox(self.window, listvariable = self.found_files, height = 20, width = 200, selectmode = 'extended')
    self.number_of_files.set(len(self.found_files))
    self.biggest_file = biggest(self.found_files)
    
def choose_folder_save(self):
    self.save_directory.set(askdirectory())

def choose_folder_config(self):
    self.feature_config_file.set(askopenfilename(
    filetypes=[("JSON", "*.json")]))
    
def choose_folder_domain(self):
    self.domain_vars_file.set(askopenfilename(
    filetypes=[("JSON", "*.json")]))

def changeText(self):
    self.metadata_directory.set("Updated Text")

def extract_and_map(self, data, config_file):
    feature_syn_dict = open_file(config_file)
    feature_syn_list = [item for sublist in list(feature_syn_dict.values()) for item in sublist]
    data = open_file(self.biggest_file)
    key_list = key_zip(data)
    dict_of_keys = key_dict(data)
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
    return feature_match
    
     