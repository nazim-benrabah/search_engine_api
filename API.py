
from bs4 import BeautifulSoup as bs

import re
from requests import *
from re import *



file_name="dblp_light.xml"

N_dernieres_annees=10


def collect(N): # une fonction qui parcours le fichier XML et crée un dictionnaire des publications des N dernieres années

## ETAPE 1 : Transformer le fichier XML en SOUP

	content = []
	
	with open(file_name, "r") as file:
	    
	    content = file.readlines() 
	    
	    content = "".join(content)
	    bs_content = bs(content, "lxml")

#ETAPE 2: Parcourir tout le fichier et detecter les publications des N dernieres annees

	elements=['article','book','incollection','inproceedings','phdthesis','mastersthesis','proceedings']
	keys=[]


	for elem in elements:

		for i in bs_content.find_all(elem):
			for p in i.find_all('year'):
				try:
					if int(p.text)>2020-N:
						keys.append(i['key']) ## Si l'année est superieur a 2015 par exemple on récolte l'attribut 'key' de la publication qui est unique pour chacune
				except Exception:
					print('')

	keys = list(dict.fromkeys(keys)) ## s'assurer qu'il n'y a pas eu de repetition de certain 'key' recolté

#ETAPE 3: Creation du dictionnaire

	dic={}


	for elem in elements:

		for p in bs_content.find_all(elem):
			try:
				for k in keys:

					if p['key']==k:
						dic[k]={'title':[], 'authors':[],'year':[], 'journal':[],'booktitle':[]} # Chaque 'key' est un indice du grand dictionnaire dic, et chaque indice on lui crée un dictionnaire contenant les information (titre, auteurs,...)
						for t in p.find_all('title'):
							dic[k]['title'].append(t.text)
							break
						for a in p.find_all('author'):
							dic[k]['authors'].append(a.text)
						for y in p.find_all('year'):
							dic[k]['year'].append(y.text)
							break
						for j in p.find_all('journal'):
							dic[k]['journal'].append(j.text)
							break
						for b in p.find_all('booktitle'):
							dic[k]['booktitle'].append(b.text)
							break
			except Exception:
				print('')

	return keys,dic


def co_authors_of_authors(list_of_authors):
	keys,dic=collect(10)
	co_authors_of_authors=[]

	for k in keys:
		for a in dic[k]['authors']:
			for l in list_of_authors:
				if a==l:
					co_authors_of_authors.append(dic[k]['authors'])

	#co_authors_of_authors= list(dict.fromkeys(co_authors_of_authors[0]))

	result=[]
	for sublist in co_authors_of_authors:
		for item in sublist:
			result.append(item)
	return list(dict.fromkeys(result))


def distance(name_origin,name_destination,ttl):

	t=True
	list_of_authors=[name_origin]
	i=0

	while(t==True):
		i+=1
		ttl-=1

		for c in co_authors_of_authors(list_of_authors):
			if c==name_destination:
				result=i
				t=False
			else:
				list_of_authors=co_authors_of_authors(list_of_authors)

		if ttl==0:
			result='Author destination inreachable...TTL expired'
			break
	return result



from bottle import Bottle, run, request, response, template

app = Bottle()

@app.route('/publications/<n:int>') #Exemple : http://localhost:8080/publications/1

def pub(n):

	pub=[]

	keys,dic=collect(N_dernieres_annees)

	for k in keys:
		pub.append((dic[k]['title'][0]))

	return pub[n] ### le resultat obtenu est un string

@app.route('/publications') #Exemple : http://localhost:8080/publications  Affiche par defaut les 100 premieres publications
							#Exemple : #Exemple : http://localhost:8080/publications?limit=9   Affiche les 9 premieres publications

def pub_100():

	pub=[]
	

	keys,dic=collect(N_dernieres_annees)
	i=0
	l=request.query.limit

	for k in keys:
		#print(i+1)

		pub.append(('<p>'+str(i+1)+' - '+dic[k]['title'][0]+'</p>'))
		i=i+1
		if l!='':
			if i==int(l):
				break
		else:
			if i==100:
				break
	return pub   # le resultat retourné est une liste de strings



@app.route('/authors/<name>/publications')
def pub_of_author(name):
	i=0

	keys,dic=collect(N_dernieres_annees)
	author_publication=[]

	for k in keys:
		for a in dic[k]['authors']:
			if a==name:
				author_publication.append('<p>'+' - '+dic[k]['title'][0]+'</p>')
				i+=1

	return author_publication



@app.route('/authors/<name>')
def info_author(name):

	keys,dic=collect(N_dernieres_annees)

	author_publication=[]
	co_authors_of_authors=[]

	for k in keys:
		for a in dic[k]['authors']:
			if a==name:
				author_publication.append(dic[k]['title'][0])
				co_authors_of_authors.append(dic[k]['authors'])

	co_authors_of_authors= list(dict.fromkeys(co_authors_of_authors[0]))

	return '<p> le nombre de publication = '+str(len(author_publication))+' \n Le nombre de co-autheurs = '+str(len(co_authors_of_authors)-1)+'</p>'



@app.route('/authors/<name>/coauthors')
def co_authors(name):


	keys,dic=collect(N_dernieres_annees)

	start=request.query.start
	count=request.query.count

	co_authors_of_authors=[]

	for k in keys:
		for a in dic[k]['authors']:
			if a==name:
				co_authors_of_authors.append(dic[k]['authors'])

	co_authors_of_authors= list(dict.fromkeys(co_authors_of_authors[0]))

	co_authors_of_authors.remove(name)
	
	if start!='' and count!='':
		return str(co_authors_of_authors[int(start):int(start)+int(count)+1])
	
	elif len(co_authors_of_authors)<100:
		return str(co_authors_of_authors)
	else:
		return str(co_authors_of_authors[0:100])



@app.route('/search/authors/<searchString>')
def search_author(searchString):

	start=request.query.start
	count=request.query.count

	keys,dic=collect(N_dernieres_annees)
	authors=[]
	for k in keys:
		for a in dic[k]['authors']:
			if a.startswith(searchString.capitalize()):
				authors.append(a)

	authors=list(dict.fromkeys(authors))

	#return str(list(dict.fromkeys(authors)))

	if start!='' and count!='':
		return str(authors[int(start):int(start)+int(count)+1])
	
	elif len(authors)<100:
		return str(authors)
	else:
		return str(authors[0:100])




@app.route('/search/publications/<searchString>')
def search_author(searchString):

	start=request.query.start
	count=request.query.count

	keys,dic=collect(N_dernieres_annees)
	search_result=[]
	for k in keys:
		for t in dic[k]['title']:
			if t.startswith(searchString.capitalize()):
				search_result.append(t)

	search_result=list(dict.fromkeys(search_result))

	#return str(list(dict.fromkeys(search_result)))
	if start!='' and count!='':
		return str(search_result[int(start):int(start)+int(count)+1])
	
	elif len(search_result)<100:
		return str(search_result)
	else:
		return str(search_result[0:100])


@app.route('/authors/<name_origin>/distance/<name_destination>')
def distance_authors(name_origin,name_destination):

	result=distance(name_origin=name_origin,name_destination=name_destination,ttl=30)

	return str(result)


run(app, host='localhost', port=8080)
