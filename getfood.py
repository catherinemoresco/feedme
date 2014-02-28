## getfood.py

import urllib2, re, string
from bs4 import BeautifulSoup

def getfood():
	dishnames = []
	soup = BeautifulSoup(urllib2.urlopen('http://www.campusdish.com/en-US/CSMW/UnivofChicago/#').read())

	dishes = soup.find_all(class_='item2')
	for d in dishes:
		dishnames.append(d.get_text())
	print soup.prettify()
	return dishnames

times = {'All Day':{}, 'Breakfast':{}, 'Brunch':{}, 'Lunch':{} ,'Dinner':{},}
def getfood2():
	dishnames = []
	soup = BeautifulSoup(urllib2.urlopen('http://www.campusdish.com/en-US/CSMW/UnivofChicago/#').read())
	for dishes in soup.find_all(id="lcGrad"):
		for d in dishes:
			img = d.find("img")	
			if img != None:
				timeofday = img['alt']
			else:
				station = d.a
				stationname =  letters_only(station.get_text())
				times[timeofday][stationname] = []
				for s in station.next_siblings:
					if s['class'] == [u'item1']:
						stationname = letters_only(s.get_text())
						times[timeofday][stationname] = []
					else:
						for c in s.contents:
						 	if c['class'] == [u'item2']:
						 		dishname = c.get_text()
						 		times[timeofday][stationname].append(dishname)

	return times

	
def letters_only(uni):
	return uni.replace("\r", "").replace("\t","").replace(">","").replace("\n","")

print getfood()

# food = getfood()
# for time in food:
# 	print time
# 	for station in food[time]:
# 		print station
# 		dishes = food[time][station]
# 		for dish in dishes:
# 			print dish
