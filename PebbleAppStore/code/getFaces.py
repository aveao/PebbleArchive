import requests
import json
import time

url = 'https://bujatnzd81-dsn.algolia.net/1/indexes/pebble-appstore-production/query?x-algolia-api-key=8dbb11cdde0f4f9d7bf787e83ac955ed&x-algolia-application-id=BUJATNZD81&x-algolia-agent=Algolia%20for%20AngularJS%203.9.2'

headers = {'Origin':'https://apps.getpebble.com', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6', 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2914.3 Safari/537.36', 'content-type':'application/x-www-form-urlencoded', 'accept': 'application/json', 'Referer': 'https://apps.getpebble.com/en_US/search/watchapps/10?native=false&query=z'}

allIds = []

def downloadPage(jsonPage):
	global allIds
	for hit in jsonPage["hits"]:
		allIds.append(hit["id"])
	print "\t " + str(len(jsonPage["hits"]))
	time.sleep(0.01)

def loadAllPages(query):
	global allIds
	global url
	global headers

	currentPage = 1;
	data = '{"params":"query='+query+'&hitsPerPage=300&tagFilters=watchface&page=0&analyticsTags=product-variant-time%2Cbasalt%2Cweb-desktop%2Cwatchapps%2Cappstore-search"}'
	r = requests.post(url, headers=headers, data=data)
#	print r.text
	tobj = json.loads(r.text)
	downloadPage(tobj)
	numberPages = int(tobj["nbPages"])
	print str(currentPage) + " " + query
	while currentPage < numberPages:
		data = '{"params":"query='+query+'&hitsPerPage=300&tagFilters=watchface&page='+str(currentPage)+'&analyticsTags=product-variant-time%2Cbasalt%2Cweb-desktop%2Cwatchapps%2Cappstore-search"}'
		rloop = requests.post(url, headers=headers, data=data)
		pageObj = json.loads(r.text)
		downloadPage(pageObj)
		currentPage = currentPage + 1
		print currentPage

alpha = "abcdefghijklmnopqrstuvwxyz"

for char1 in alpha:
	for char2 in alpha:
		loadAllPages(char1+char2)
		time.sleep(0.1)
	time.sleep(1)


for char1 in alpha:
	loadAllPages(char1)
	time.sleep(1)


fout = open("faces.json", "w")
fout.write(json.dumps(list(set(allIds))))
fout.close()