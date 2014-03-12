## getfood.py

import urllib2, re, string
from bs4 import BeautifulSoup

class Dish(object):
	def __init__(self, name):
		self.name = name
		self.star = ""
		self.entries = []
		self.allergens =[]

def getfood():
	dishnames = []
	soup = BeautifulSoup(urllib2.urlopen('http://www.campusdish.com/en-US/CSMW/UnivofChicago/#').read())

	dishes = soup.find_all(class_='item2')
	for d in dishes:
		dishnames.append(d.get_text())
	print soup.prettify()
	return dishnames



# parse webpage:
def getfood2(dhall):
	times = {'All Day':{}, 'Breakfast':{}, 'Lunch':{} ,'Dinner':{},'Late Night':{}, 'Brunch':{}, 'Night Snack':{}}
	dishnames = []
	if dhall=="Cathey":
		url='http://www.campusdish.com/en-US/CSMW/UnivofChicago/#'
	else:
		url='http://www.campusdish.com/en-US/CSMW/UnivofChicago/Home.htm?LocationID=292'
# get html:
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	for dishes in soup.find_all(id="lcGrad"):
		for d in dishes:
			img = d.find("img")	
			if img != None:
				timeofday = img['alt']
			else:
				station = d.a
				stationname =  letters_only(station.get_text()).upper()
				times[timeofday][stationname] = []
				for s in station.next_siblings:
				#set new station name:
					if s['class'] == [u'item1']:
						stationname = letters_only(s.get_text())
						times[timeofday][stationname] = []
					else:
						for c in s.contents:
						 	if c['class'] == [u'item2']:
						 		dishname = remove_trailing_spaces(c.get_text())
						 		times[timeofday][stationname].append(dishname.replace("/", "-"))

	return times

	
def letters_only(uni):
	return uni.replace("\r", "").replace("\t","").replace(">","").replace("\n","")

def remove_trailing_spaces(st):
	while st[-1] == ' ':
		st = st[0:len(st)-1]
	return st



