import re
import json

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