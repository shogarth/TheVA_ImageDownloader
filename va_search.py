# Instructions
#		python va_search.py --collection=THES48597 --type=Commode --yearto=1799
#		python va_search.py --collection=THES48597 --yearto=1799 --type=Commode --out="Commode" > Commode.py
# Collections
# 		THES48597: Furniture and Woodwork Collection
# Reference
#		https://developers.vam.ac.uk/guide/v2/results/object-fields-brief.html
#		https://collections.vam.ac.uk/search/


import getopt
import json
import os
import sys
import requests


def writeNumbers(outDir, objectNumbers):
	print("import os")
	print("")
	for num in objectNumbers:
		print("os.system('python va_download.py --out=\"{}\" --id=\"{}\"')".format(outDir, num))


def search(params):
	objectNumbers = []

	searchUrl = "https://api.vam.ac.uk/v2/objects/search" #q="china
	prefix = "?"
	for key in params:
		val = str(params[key])
		if(len(val)):
			searchUrl = "{}{}{}={}".format(searchUrl, prefix, key, val)
			prefix = "&"
	#print(searchUrl)		
	searchJson = requests.get(searchUrl).json()
	#print(json)
	numSearchPages = searchJson["info"]["pages"]
	searchPage = 1
	while searchPage <= numSearchPages:
		#print("Searching Page {}".format(searchPage))
		recordsJson = requests.get("{}{}page={}".format(searchUrl, prefix, searchPage)).json()
		for record in recordsJson["records"]:
			objectNumbers.append(record["systemNumber"])
		searchPage = searchPage + 1
	#print("Found {} objects".format(len(objectNumbers)))
	return objectNumbers


def main(argv):
	opts, args = getopt.getopt(argv, "c:o:t:y:z", ["out=", "collection=", "type=", "yearfrom=", "yearto="])

	collection = ""
	type = ""
	yearFrom = -800
	yearTo = 2000
	
	outDir = ""
	ids = []

	for opt, arg in opts:
		if opt in ("--out", "-o"):
			outDir = arg
		elif opt in ("--collection", "-c"):
			collection = arg
		elif opt in ("--type", "-t"):
			type = arg
		elif opt in ("--yearfrom", "-y"):
			yearFrom = arg
		elif opt in ("--yearto", "-z"):
			yearTo = arg

	objectNumbers = search({"page_size":100, "id_collection":collection, "kw_object_type":type, "year_made_from":yearFrom, "year_made_to":yearTo})
	writeNumbers(outDir, objectNumbers)


if __name__ == "__main__":
	main(sys.argv[1:])


























