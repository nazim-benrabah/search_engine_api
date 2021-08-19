

from requests import get

from bottle import Bottle, run, request, response, template

app = Bottle()

@app.route("/input")
def input():
	return '''
	<h1>Rechercher les publications d'un auteur</h1>
	<form action="/input" method="post">
	Auteur : <input name="author_pub" type="text" />
	
	<input value="Rechercher" type="submit" />
	</form> 

	<h1>____________</h1>

	<h1>Rechercher les co-auteurs d'un auteur</h1>

	<form action="/input" method="post">
	Auteur : <input name="author_coauthors" type="text" />
	
	<input value="Rechercher" type="submit" />
	</form> 
	<h1>____________</h1>

	<h1>Rechercher la distance de collaboration entre auteurs</h1>
	<form action="/input" method="post">
	Auteur origin: <input name="origin" type="text" />
	Auteur destination: <input name="destination" type="text" />
	<input value="Trouver la distance" type="submit" />
	</form> 
	<h1>____________</h1>

	<h1>Rechercher un auteur</h1>
	<form action="/input" method="post">
	Taper une partie de son nom: <input name="part_of_name" type="text" />
	
	<input value="Rechercher" type="submit" />
	</form> 
	<h1>____________</h1>

	''' 

@app.route("/input", method='POST')
def do_input():
	try:
		auteur_pub = request.forms['author_pub']
	except Exception:
		auteur_pub=''

	try:
		author_coauthors = request.forms['author_coauthors']
	except Exception:
		author_coauthors=''


	try:
		origin = request.forms['origin']
	except Exception:
		origin=''

	try:
		destination = request.forms['destination']
	except Exception:
		destination=''

	try:
		part_of_name = request.forms['part_of_name']
	except Exception:
		part_of_name=''



	if auteur_pub!='':
		r1 = get(f"http://127.0.0.1:8080/authors/{auteur_pub}/publications")
		return r1.text

	
	if author_coauthors!='':
		r2 = get(f"http://127.0.0.1:8080/authors/{author_coauthors}/coauthors")
		return r2.text


	if origin!='' and destination!='':
		r3 = get(f"http://127.0.0.1:8080/authors/{origin}/distance/{destination}")
		return r3.text


	if part_of_name!='':
		r4 = get(f"http://127.0.0.1:8080/search/authors/{part_of_name}")
		return r4.text




run(app, host='localhost', port=8081)