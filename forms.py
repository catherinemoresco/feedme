from flask.ext.wtf import Form
from wtforms import BooleanField, RadioField


class AllergyForm(Form):
	gluten = BooleanField('Gluten')
	milk = BooleanField('Milk')
	soy = BooleanField('Soy')
	wheat = BooleanField('Wheat')
	fish = BooleanField('Fish')
	shellfish = BooleanField('Shellfish')
	treenut = BooleanField('Tree Nut')
	peanut = BooleanField('Peanut')
	egg = BooleanField('Egg')
	# dhall = RadioField('Dining Hall', choices=[('Bartlett', 'Bartlett'), ('Cathey','Cathey')])
