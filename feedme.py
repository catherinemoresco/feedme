from flask import Flask, render_template, g
import sqlite3
import os
from getfood import getfood
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'feedme.db'),
	DEBUG=True
))

@app.route('/')
def show_entries():
	food = getfood()
	placeholder = '?'
	placeholders= ", ".join(placeholder for unused in food)
	db = get_db()
	query = 'SELECT * FROM food WHERE id IN (%s) AND gluten=" " AND milk=" "' % placeholders
	cur = db.execute(query, food)
	entries = cur.fetchall()
	query = 'SELECT * FROM food WHERE id IN (%s) AND gluten!=" " AND milk!=" "' % placeholders
	cur = db.execute(query, food)
	canthave = cur.fetchall()
	return render_template('hello.html', entries=entries, canthave=canthave)

# def show_entries():
# 	entries = get_entries()
# 	entries = entries['Brunch']
# 	print entries
# 	return render_template('hello.html', entries=entries)

# def get_entries():
# 	db = get_db()
# 	food = getfood()
# 	time = 'All Day'
# 	for station in food[time].keys():
# 		dishes = food[time][station]
# 		placeholder = '?'
# 		placeholders= ", ".join(placeholder for unused in dishes)
# 		query = 'SELECT * FROM food WHERE id IN (%s) AND gluten=" " AND milk=" "' % placeholders
# 		cur = db.execute(query, dishes)
# 		entries = cur.fetchall()
# 		food[time][station] = entries
# 	return food

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
	print startletter
	return render_template('browse.html', entries=entries, startletter=startletter)

def get_not_found(found, food):
	found = []
	not_found = []
	for e in found:
		found.append(e.id)
	for f in food:
		if f not in found:
			not_found.append(f)
	return not_found

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