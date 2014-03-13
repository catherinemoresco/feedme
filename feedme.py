from flask import Flask, render_template, g, request, redirect
import sqlite3
import os
import string
from getfood import getfood2, Dish
from forms import AllergyForm
app = Flask(__name__)
app.config.from_object('config')

app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'feedme.db'),
	DEBUG=False,
	CSRF_ENABLED=False,
	secret_key="you-will-never-guess"
))


@app.route('/select/<dhall>/<selectallergens>')
def show_selective_entries(selectallergens, dhall):
# identical to main function, but passes list of unavailable and allergic foods to template
	db = get_db()
	foods = getfood2(dhall)
	for time, stations in foods.iteritems():
		for station, dishes in stations.iteritems():
			for dish in dishes:
				d = Dish(dish)
				cur = db.execute('SELECT * FROM food WHERE id=?', (dish,))
				entries = cur.fetchall()
				if entries != []:
				# add asterisk if more than one entry found
					if len(entries) > 1:
						d.star = '*'
					d.entries = entries[0]
					d.allergens = get_allergens(entries)
					for sa in selectallergens.split("+"):
						if sa in d.allergens:
							d.entries="allergic"
					foods[time][station][foods[time][station].index(dish)] = d
				else:
					if len(list(set(selectallergens.split("+")).intersection(set(['Gluten','Wheat','Milk','Egg','Soy','Fish','Shellfish','Peanut','Tree Nut'])))) != 0:
						d.entries = "unavailable"
					foods[time][station][foods[time][station].index(dish)] = d
	foodslist = [("All Day", foods["All Day"]), ("Breakfast", foods['Breakfast']), ('Brunch', foods['Brunch']), ("Lunch", foods['Lunch']), ("Dinner", foods['Dinner']), ("Late Night", foods['Late Night']), ("Night Snack", foods["Night Snack"])]
	foodslist = remove_empties(foodslist)
	return render_template('hello2.html', entries=foodslist, dhall=dhall, selectallergens=selectallergens, other_dhall=get_other_dhall(dhall))

def get_other_dhall(d):
	if d == 'Cathey':
		return 'Bartlett'
	return'Cathey'


#remove keys in "foods" dictionary with no values
def remove_empties(foods):
	trimmed =[]
	for food in foods:
		if food[1] != {}:
			trimmed.append(food)
	return trimmed

#extract a list of unique allergens in all entries from list of entries
def get_allergens(entries):
	alist = []
	for e in entries:
		for allergen in [e['gluten'], e['milk'], e['wheat'], e['soy'], e['fish'], e['shellfish'], e['peanut'], e['tree_nut'], e['egg']]:
			if allergen != " ":
				alist.append(allergen)
	return list(set(alist))


@app.route('/', methods=['POST','GET'])
def choose():
	form=AllergyForm(request.form)
	if form.validate_on_submit():
		dhall = 'Cathey'
		# if form.data['dhall'] == 'Bartlett':
		# 	dhall='Bartlett'
		return redirect('/select/' + dhall + '/' + datatourl(form.data))
	return render_template('welcome.html', form=form)

@app.route('/info')
def show_info():
	return render_template('info.html')

def datatourl(data):
	allergens =[]
	if data['gluten']:
		allergens.append('Gluten')
	if data['wheat']:
		allergens.append('Wheat')
	if data['egg']:
		allergens.append('Egg')
	if data['soy']:
		allergens.append('Soy')
	if data['peanut']:
		allergens.append('Peanut')
	if data['treenut']:
		allergens.append('Tree Nut')
	if data['fish']:
		allergens.append('Fish')
	if data['shellfish']:
		allergens.append('Shellfish')
	if data['milk']:
		allergens.append('Milk')
	if len(allergens) != 0:
		return '+'.join(allergens)
	else:
		return('None')



@app.route('/browse')
def browse():
	db = get_db()
	cur = db.execute('SELECT * FROM food WHERE id!="#N/A" ORDER BY id')
	entries = cur.fetchall()
	letters = list(string.lowercase)
	return render_template('browse.html', entries=entries, letters=letters)

@app.route('/browse/<startletter>')
def browseletter(startletter):
	db = get_db()
	cur = db.execute('SELECT * FROM food WHERE id LIKE (? || "%")' , startletter)
	entries = cur.fetchall()
	letters = list(string.lowercase)
	return render_template('browse.html', entries=entries, startletter=startletter, letters=letters)

@app.route('/lookup/<dishname>')
def lookup(dishname):
	db = get_db()
	cur = db.execute('SELECT * FROM food WHERE id=?', (dishname,))
	entries = cur.fetchall()
	return render_template('lookupdish.html', entries=entries)

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = connect_db()
	return db

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv 

@app.teardown_appcontext
def close_db(exception):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

if __name__ == '__main__':
	app.run()