import re

import itertools

'''
def find_delimiters(lst):
    candidates = list(itertools.islice(find_longest_common_substrings(lst), 3))
    if len(candidates) == 3 and len(candidates[1]) == len(candidates[2]):
        raise ValueError("Unable to find useful delimiters")
    if candidates[1] in candidates[0]:
        raise ValueError("Unable to find useful delimiters")
    return candidates[0:2]

def find_longest_common_substrings(lst):
    for i in range(min_length(lst), 0, -1):
        for substring in common_substrings(lst, i):
            yield substring

def min_length(lst):
    return min(len(item) for item in lst)

def common_substrings(lst, length):
    assert length <= min_length(lst)
    returned = set()
    for i, item in enumerate(lst):
        for substring in all_substrings(item, length):
            in_all_others = True
            for j, other_item in enumerate(lst):
                if j == i:
                    continue
                if substring not in other_item:
                    in_all_others = False
            if in_all_others:
                if substring not in returned:
                    returned.add(substring)
                    yield substring

def all_substrings(item, length):
    for i in range(len(item) - length + 1):
        yield item[i:i+length]

def split_strings(lst, delimiters):
    for item in lst:
        parts = re.split("|".join(delimiters), item)
        yield tuple(part for part in parts if part != '')

def clean(lst):
    delimiters = find_delimiters(lst)
    return delimiters, list(split_strings(lst, delimiters))
'''

write_path = "C:/Users/xiemp/Documents/afstudeer/features/sdn_features_clean.txt"
extracted_feature_path = "C:/Users/xiemp/Documents/afstudeer/features/sdn_features.txt"
extracted_features = []

for line in open(extracted_feature_path, "r"):
    line = line.replace(' ', '_')
    extracted_features.append(line.strip())

#print(clean(extracted_features))
def cleaner(lst):
    cleaned_list = []
    for feature in lst:
        #print(feature)
        clean = re.split(':(.*)',feature)
        if len(clean) > 1:
            clean = clean[1]
        else:
            clean = clean[0][1:]

        
        clean = clean.replace("_", " ")
        clean = re.sub("([a-z])([A-Z])","\g<1> \g<2>",clean)
        clean = clean.lower()
        cleaned_list.append(clean)
    return cleaned_list

cleaned_features = cleaner(extracted_features)
print(cleaned_features)


sdn_features_clean = open(write_path, "w")
for element in cleaned_features:
    sdn_features_clean.write(element + "\n")
sdn_features_clean.close()
        
          



    