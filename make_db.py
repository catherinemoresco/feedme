## generate food database from csv

import sqlite3, csv
conn = sqlite3.connect('feedme.db')
conn.text_factory = str

csvfile = open('ingredient_data.csv', "rU")
reader = csv.reader(csvfile)

c = conn.cursor()
c.execute('''CREATE TABLE food (
	id text not null,
	ingredients text,
	fish text,
	shellfish text,
	peanut text,
	tree_nut text,
	egg text,
	milk text,
	soy text,
	wheat text,
	gluten text
	)''')

for line in reader:
	for entry in line:
		if entry == " ":
			line[line.index(entry)] = " "
	c.execute('INSERT INTO food VALUES (?,?,?,?,?,?,?,?,?,?,?)', line)

conn.commit()

