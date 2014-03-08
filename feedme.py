from flask import Flask, render_template, g, request
import sqlite3
import os
from getfood import getfood2
app = Flask(__name__)
app.config.from_object('config')

app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'feedme.db'),
	DEBUG=True
))

@app.route('/')

def show_entries():
	db = get_db()
	foods = getfood2()
	for time, stations in foods.iteritems():
		for station, dishes in stations.iteritems():
			for dish in dishes:
				cur = db.execute('SELECT * FROM food WHERE id=?', (dish,))
				entries = cur.fetchall()
				if entries != []:
					if len(entries) > 1:
						star = '*'
					else:
						star = ''
					foods[time][station][foods[time][station].index(dish)] = (dish, entries[0], star)

				else:
					foods[time][station][foods[time][station].index(dish)] = (dish, "nodata")
	foodslist = [("All Day", foods["All Day"]), ("Breakfast", foods['Breakfast']), ('Brunch', foods['Brunch']), ("Lunch", foods['Lunch']), ("Dinner", foods['Dinner']), ("Late Night", foods['Late Night'])]
	remove_empties(foodslist)
	return render_template('hello2.html', entries=foodslist)

def remove_empties(foods):
	for food in foods:
		if food[1] == {}:
			foods.remove(food)
	return foods


@app.route('/welcome')
def choose():
	return render_template('welcome.html')

@app.route('/browse')
def browse():
	db = get_db()
	cur = db.execute('SELECT * FROM food WHERE id!="#N/A" ORDER BY id')
	entries = cur.fetchall()
	return render_template('browse.html', entries=entries)

@app.route('/browse/<startletter>')
def browseletter(startletter):
	db = get_db()
	cur = db.execute('SELECT * FROM food WHERE id LIKE (? || "%")' , startletter)
	entries = cur.fetchall()
	return render_template('browse.html', entries=entries, startletter=startletter)

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