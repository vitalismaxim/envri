from dateutil.parser import parse

def iterate_all(iterable, returned="key"):
    
    """Returns an iterator that returns all keys or values
       of a (nested) iterable.
       
       Arguments:
           - iterable: <list> or <dictionary>
           - returned: <string> "key" or "value"
           
       Returns:
           - <iterator>
    
    if type(iterable) is list:
        if len(iterable) == 1:
            if type(iterable[0]) is list:
                iterable = iterable[0]
            yield iterable[0]
    """

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


def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except:
        return False

def is_url(string):
    try:
        if 'http' in string.lower() or 'www' in string.lower():
            return True
        else:
            return False
    except:
        return False

def description(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            value_list.append(value.split())
        except: continue

    if len(value_list) > 0: return ' '.join(max(value_list, key = len))
    else: return "N/A"


def identifier(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            value = value.split()
            if "." not in value and "#" not in value and "@" not in value:
                value_list.append(value)
            else: continue
        except: continue
    if len(value_list) > 0: return max(value_list, key = len)[0]
    else: return "N/A"

def keyword(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if "." not in value and "/" not in value and "#" not in value and "@" not in value:
                if is_date(value) is False:
                    value_list.append(value)
            else: continue
        except: continue
    return list(set(value_list))

def language(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        value_list.append(value)
    
    if len(value_list) > 0: return min(value_list, key = len)
    else: return "N/A"


def accessibility(values):
    return description(values)


def accountablePerson(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        if value is None:
            continue             
        if len(value.split()) == 2:
            value_list.append(value)
    if len(value_list) > 0: return value_list
    else: return "N/A"

def version(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try: 
            value_list.append(float(value))
        except: continue
    if len(value_list) > 0: return min(value_list)
    else: return "N/A"

def period(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try: 
            if is_date(value) is True:
                value_list.append(value)
        except: continue
    if len(value_list) > 0: return [min(value_list), max(value_list)]
    else: return "N/A"


def publisher(values):
    return description(values)

def spatial(values):
    return "N/A"
            
def longitude(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if float(value):
                return float(value)
            else: continue
        except: continue
    return "N/A"

def latitude(values):
    return longitude(values)

def License(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try: 
            if 'licence' in value.lower() or "CC" in value:
                value_list.append(value)
            else: continue
        except: continue
    if len(value_list) > 0: return value_list
    else: return "N/A"

        
def citation(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try: 
            if "citation" in value.lower or "bib" in value.lower():
                value_list.append(value)
            else: continue
        except: continue
    if len(value_list) > 0: return value_list
    else: return "N/A"

def genre(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            else:
                value_list.append(value)
        except: continue
    if len(value_list) > 0: return value_list
    else: return "N/A"
    
def creator(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_url(value) is False:
                value_list.append(value)
            else: continue
        except: continue
    if len(value_list) > 0: return value_list[0]
    else: return "N/A"

def modification(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_date(value) is True:
                return value
        except: continue
    return "N/A"

def distribution(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_url(value) is True:
                if '.rar' in value or '.zip' in value or 'file' in value:
                    value_list.append(value)
                else: continue
            else: continue
        except: continue
    if len(value_list) > 0: return value_list[0]
    else: return "N/A"

def image(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_url(value) is True:
                if '.png' in value or '.jpeg' in value or '.jpg' in value or '.gif' in value or '.tiff' in value or '.raw' in value:
                    value_list.append(value)
        except: continue
    if len(value_list) > 0: return value_list[0]
    else: return "N/A"

def thumbnail(values):
    return image(values)

def headline(values):
    return description(values)

def abstract(values):
    return description(values)

def category(values):
    return genre(values)[0]

def created(values):
    return modification(values)

def credit(values):
    return creator(values)

def published(values):
    return modification(values)

def producer(values):
    return creator(values)

def author(values):
    return accountablePerson(values)

def space(values):
    return 'N/A'

def url2(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_url(value) is True:
                value_list.append(value)
        except: continue
    if len(value_list) > 0: return max(value_list, key = len)
    else: return "N/A"

def url(values):
    value_list = []
    for value in values:
        if value is not None: 
            value_list.append(value)
    if len(value_list) > 0: return max(value_list, key = len)
    else: return "N/A"

def temporal(values):
    return period(values)

def sponsor(values):
    return "N/A"

def size(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            return int(value)
        except: continue
    return "N/A"

def publisher(values):
    return producer(values)

def Licence(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif "licence" in value.lower() or 'cc' in value.lower():
                return values
        except: continue
    return "N/A"

def similar(values):
    return "N/A"

def publication(values):
    return description(values)

def provider(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_url(value) is True and value.count('/') < 5:
                value_list.append(value)
        except: continue
    if len(value_list) > 0: return list(set(value_list))
    else: return "N/A"
    
def position(values):
    return "N/A"

def name(values):
    try: return list(iterate_all(values, "value"))[0]
    except: return "N/A"

def measurement(values):
    return "N/A"

def material(values):
    return "N/A"
    
def maintainer(values):
    return "N/A"
    
def location(values):
    return "N/A"
    
def issn(values):
    return "N/A"

def ispartof(values):
    return "N/A"
    
def isbasedon(values):
    return "N/A"
    
def free(values):
    return "N/A"

def include(values):
    return "N/A"

def editor(values):
    return "N/A"
    
def editeidr(values):
    return "N/A"
    
def copyrightyear(values):
    return "N/A"

def copyrightnotice(values):
    return "N/A"

def copyrightholder(values):
    return "N/A"

def contributor(values):
    return "N/A"

def contentreferencetime(values):
    return "N/A"
    
def character(values):
    return "N/A"

def acquirelicensepage(values):
    return "N/A"

def access(values):
    return "N/A"

def about(values):
    return description(values)
     
def rights(values):
    return "N/A"

def relation(values):
    return "N/A"
     
def attribution(values):
    return "N/A"
    
def previous(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif is_url(value) is True:
                return values[value]
        except: continue
    return "N/A"

def landing_page(value):
    return "N/A"

def referenced(value):
    return "N/A"

def series(values):
    return "N/A"

def policy(values):
    return description(values)

def current(values):
    return "N/A"

def constraints(values):
    return description(values)

def status(values):
    return 'N/A'

def spatialrepresentationtype(values):
    return "N/A"

def spatialrepresentationinfo(values):
    return "N/A"
    
def scope(values):
    return "N/A"
    
def party(values):
    return description(values)
    
def releasability(values):
    return "N/A"
    
def reference(values):
    return "N/A"
    
def purpose(values):
    return "N/A"
    
def locale(values):
    return "N/A"
    
def metadataprofile(values):
    return description(values)

def metadatalinkage(values):
    return "N/A"
    
def metadataidentifier(values):
    return "N/A"

def md_legalconstraints(values):
    return "N/A"
    
def md_identification(values):
    return "N/A"

def environmentdescription(values):
    return "N/A"
    
def distributor(values):
    return provider(values)

def distribution(values):
    return "N/A"

def quality(values):
    return "N/A"
    
def info(values):
    return "N/A"
    
def contact(values):
    values = list(iterate_all(values, "value"))
    value_list = []
    for value in values:
        try:
            if value is None:
                continue
            elif "@" in value:
                return
        except: continue
    return "N/A"

def included(values):
    return "N/A"

def run_funcs(data):
    data['description'] = description(data['description'])
    data['identifier'] = identifier(data['identifier'])
    data['keyword'] = keyword(data['keyword'])
    data['language'] = language(data['language'])
    data['accessibility'] = accessibility(data['accessibility'])
    data['accountable Person'] = accountablePerson(data['accountable Person'])
    data['version'] = version(data['version'])
    data['period'] = period(data['period'])
    data['publisher'] = publisher(data['publisher'])
    data['spatial'] = spatial(data['spatial'])
    data['longitude'] = longitude(data['longitude'])
    data['latitude'] = latitude(data['latitude'])
    data['license'] = License(data['license'])
    data['citation'] = citation(data['citation'])
    data['genre'] = genre(data['genre'])
    data['creator'] = creator(data['creator'])
    data['modification'] = modification(data['modification'])
    data['distribution'] = distribution(data['distribution'])
    data['image'] = image(data['image'])
    data['thumbnail'] = thumbnail(data['thumbnail'])
    data['headline'] = headline(data['headline'])
    data['abstract'] = abstract(data['abstract'])
    data['created'] = created(data['created'])
    data['category'] = category(data['category'])
    data['modification'] = modification(data['modification'])
    data['credit'] = credit(data['credit'])
    data['published'] = published(data['published'])
    data['producer'] = producer(data['producer'])
    data['author'] = author(data['author'])
    data['space'] = space(data['space'])
    data['url'] = url(data['url'])
    data['temporal'] = temporal(data['temporal'])
    data['sponsor'] = sponsor(data['sponsor'])
    data['size'] = size(data['size'])
    data['publisher'] = publisher(data['publisher'])
    data['license'] = License(data['license'])
    data['similar'] = similar(data['similar'])
    data['publication'] = publication(data['publication'])
    data['provider'] = provider(data['provider'])
    data['position'] = position(data['position'])
    data['name'] = name(data['name'])
    data['measurement'] = measurement(data['measurement'])
    data['material'] = material(data['material'])
    data['maintainer'] = maintainer(data['maintainer'])
    data['location'] = location(data['location'])
    data['issn'] = issn(data['issn'])
    data['is Part Of'] = ispartof(data['is Part Of'])
    data['is Based On'] = isbasedon(data['is Based On'])
    data['free'] = free(data['free'])
    data['included'] = included(data['included'])
    data['editor'] = editor(data['editor'])
    data['editEIDR'] = editeidr(data['editEIDR'])
    data['copyright Year'] = copyrightyear(data['copyright Year'])
    data['copyright Notice'] = copyrightnotice(data['copyright Notice'])
    data['copyright Holder'] = copyrightholder(data['copyright Holder'])
    data['contributor'] = contributor(data['contributor'])
    data['content Reference Time'] = contentreferencetime(data['content Reference Time'])
    data['character'] = character(data['character'])
    data['acquire License Page'] = acquirelicensepage(data['acquire License Page'])
    data['access'] = access(data['access'])
    data['about'] = about(data['about'])
    data['rights'] = rights(data['rights'])
    data['relation'] = relation(data['relation'])
    data['attribution'] = attribution(data['attribution'])
    data['previous'] = previous(data['previous'])
    data['landing page'] = landing_page(data['landing page'])
    data['referenced'] = referenced(data['referenced'])
    data['series'] = series(data['series'])
    data['version'] = version(data['version'])
    data['policy'] = policy(data['policy'])
    data['current'] = current(data['current'])
    data['constraints'] = constraints(data['constraints'])
    data['status'] = status(data['status'])
    data['status'] = status(data['status'])
    data['spatialRepresentationInfo'] = spatialrepresentationinfo(data['spatialRepresentationInfo'])
    data['spatialRepresentationType'] = spatialrepresentationtype(data['spatialRepresentationType'])
    data['scope'] = scope(data['scope'])
    data['party'] = party(data['party'])
    data['releasability'] = releasability(data['releasability'])
    data['reference'] = reference(data['reference'])
    data['purpose'] = purpose(data['purpose'])
    data['locale'] = locale(data['locale'])
    data['metadata Profile'] = metadataprofile(data['metadata Profile'])
    data['metadata Linkage'] = metadatalinkage(data['metadata Linkage'])
    data['metadata Identifier'] = metadataidentifier(data['metadata Identifier'])
    data['MD LegalConstraints'] = md_legalconstraints(data['MD LegalConstraints'])
    data['MD Identification'] = md_identification(data['MD Identification'])
    data['environment Description'] = environmentdescription(data['environment Description'])
    data['distributor'] = distributor(data['distributor'])
    data['distribution'] = distribution(data['distribution'])
    data['quality'] = quality(data['quality'])
    data['info'] = info(data['info'])
    data['contact'] = contact(data['contact'])

    for value in data.values():
        if value is None: value = 'N/A'
    return data