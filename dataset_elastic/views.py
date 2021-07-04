from django.forms.widgets import Widget
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from urllib.request import urlopen
from datetime import datetime
from elasticsearch import Elasticsearch
from glob import glob
from elasticsearch_dsl import Search, Q

es = Elasticsearch("http://localhost:9200")

def rest(request):
	try:
		term = request.GET['term']
	except:
		term = ''
	try:
		year_from = request.GET['year_from']
	except:
		year_from = 0
	try:
		year_to = request.GET['year_to']
	except:
		year_to = 3000

	result = esearch(all_fields = term, year_from=year_from, year_to=year_to)
	return JsonResponse(result, safe = False, json_dumps_params={'ensure_ascii': False})

def home(request):
    index_elastic()
    context = {}
    #context['form'] = SelectionForm()
    #context['result'] = SelectionForm.fields
    return render(request, "home.html", context)

def result(request):
    context = {}
    #context['result'] = SelectionForm()
    return render(request, "result.html")

#-------------------------------------------------------------------------

def search_index(request):
	results = []
	keywords_term = ""
	abstract_term = ""
	all_fields_term = ""
	year_from_term = ""
	year_to_term = ""

	"""
	if request.GET.get('keywords') and request.GET.get('abstract'):
		keywords_term = request.GET['keywords']
		abstract_term = request.GET['abstract']
	elif request.GET.get('keywords'):
		keywords_term = request.GET['keywords']
	elif request.GET.get('abstract'):
		abstract_term = request.GET['abstract']
	elif request.GET.get('all_fields'):
		all_fields_term = request.GET['all_fields']
	"""

	try:
		keywords_term = request.GET['keywords']
	except:
		pass
	try:
		abstract_term = request.GET['abstract']
	except:
		pass
	try:
		all_fields_term = request.GET['all_fields']
	except:
		pass
	try:
		year_from_term = request.GET['year_from']
	except:
		pass
	try:
		year_to_term = request.GET['year_to' ]
	except:
		pass

	search_term = keywords_term or abstract_term or all_fields_term or year_from_term or year_to_term
	
	#print(search_term)
	#results = esearch(keywords = keywords_term, abstract=abstract_term, all_terms = all_fields_term)
	results = esearch(keywords = keywords_term,
					  abstract = abstract_term, 
					  all_fields = all_fields_term, 
					  year_from = year_from_term, 
					  year_to = year_to_term)

	#print(results)
	context = {'results': results, 'count': len(results), 'search_term': search_term }
	return render(request, 'search.html', context) 

#----------------------------------------------------------------

#----------------------------------------------------------------

def esearch(keywords = "", abstract = "", all_fields = "", year_from = "0", year_to = "3000"):
	client = Elasticsearch("http://localhost:9200")
	print(year_from, year_to)

	q = Q("bool", should=[
		Q("match", keywords=keywords), 
		Q("match", abstract = abstract),
		Q("match", keywords=all_fields), 
		Q("match", abstract = all_fields),
		Q("match", name = all_fields),
		Q("match", material = all_fields),
		Q("match", publisher = all_fields),
		Q("match", description = all_fields),
		Q("match", provider = all_fields),
		Q("match", distributionInfo = all_fields),
		Q("match", about = all_fields),
		Q("match", author = all_fields),
		Q("match", citation = all_fields),
		Q("match", responsibleParty = all_fields),
		Q("match", creator = all_fields),
		Q("match", distributor = all_fields),
		],
		minimum_should_match=1)

	s = Search(using = client, index = "envri")\
			.filter("range", temporal = {'gte': year_from, 'lte': year_to})\
			.query(q)[:10000]
			#.filter('range', temporal={'from': year_from, 'to' : year_to })\
			#[:10000]

	#s = Search(using = client, index = "envri").filter("range", temporal = {'gte': year_from, 'lte': year_to})[:10000]
	response = s.execute()
	#print("%d hits found." % response.hits.total)
	search = get_results_rest(response)
	return search

def get_results_rest(response):
	results = {}
	for hit in response:
		result = {
			'identifier': hit.identifier,
			'name' : hit.name,
			'temporal' : hit.temporal,
			'author' : [name for name in hit.author],
			'landing_page' : hit.landing_page,
			'keywords' : [keyword for keyword in hit.keywords],
			'distributor' : hit.distributor
		}
		results[hit.identifier] = result
	return results

def get_results(response):
	results = []
	for hit in response:
		result_tuple = (hit.identifier, hit.landing_page, hit.name)
		results.append(result_tuple)
	return results



#-------------------------------------------------------------

#-------------------------------------------------------------

INDEX = "envri"

folders = glob("envri_json/*")
#print(folders)

filelist = []

for i in range(len(folders)):
    folder = folders[i] + "/*"
    filelist.append(glob(folder))

#print(len(filelist))

#flatten
filelist = [file for folder in filelist for file in folder]
#rint(len(filelist))
#print(filelist)

sample = filelist
#print(sample)
completed = len(sample)

#print(filelist)



def open_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data


def index_elastic():
    indexed = 0
    for i in range(len(sample)):
        doc = open_file(sample[i])
        id = doc["identifier"]
        #print(id)
        print((i / completed * 100), "%", sample[i])
        indexed += 1
        res = es.index(index = "envri", id = doc["identifier"], body=doc)
        es.indices.refresh(index = "envri")


#print(doc)

#id = doc["identifier"]
#print(id)
#res = es.index(index = "envri", id = doc["identifier"], body=doc)

#print(res['result'])

#res = es.get(index = "envri", id = doc["identifier"])
#print(res['_source'])

#es.indices.refresh(index = "envri")

"""
res = es.search(INDEX, body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
"""

"""
def esearch(keywords="", abstract=""):
	client = Elasticsearch("http://localhost:9200")
	q = Q("bool", should=[Q("match", keywords=keywords), 
	Q("match", abstract = abstract)], minimum_should_match=1)
	s = Search(using=client, index="envri").query(q)[:10000]
	response = s.execute()
	#print("%d hits found." % response.hits.total)
	search = get_results(response)
	return search
"""