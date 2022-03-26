# Instructions
#		python va_download.py --out="Downloads" --id="O9138"
# Reference
#		https://developers.vam.ac.uk/guide/v2/results/object-fields-brief.html
#		https://framemark.vam.ac.uk/collections/2006AN7529/info.json
#		https://iiif.vam.ac.uk/collections/O9138/manifest.json
#		https://api.vam.ac.uk/v2/museumobject/O1288719
#		https://iiif.vam.ac.uk/collections/O1288719/manifest.json

import getopt
import json
from multiprocessing import Pool
import os
import sys
import requests

def saveImagePairToFile(data):
	saveImageToFile(data["path"], data["url"])

def saveImageToFile(path, imageUrl):
	extension = os.path.splitext(imageUrl)[1]

	#print("Get Image: {}".format(imageUrl))
	image = requests.get(imageUrl).content
	print("Writing {}".format(path+extension))
	with open(path+extension, 'wb') as file:
		file.write(image)


def saveMetadata(path, metadata):
	with open(path, 'wt') as file:
		file.write(json.dumps(metadata, indent=4))


def getItemMetadata(id):
	url = "https://api.vam.ac.uk/v2/museumobject/{}".format(id)
	metadata = requests.get(url).json()
	
	artist = "Unknown"
	artists = metadata["record"]["artistMakerPerson"]
	for artistContainer in artists:
		foundArtist = artistContainer["name"]["text"]
		if len(foundArtist) > 0:
			artist = foundArtist
			break
	if artist == "unknown":
		artist = "Unknown"
			
	#title = "Unknown"
	#titles = metadata["record"]["titles"]
	#for titleContainer in titles:
	#	foundTitle = titleContainer["title"]
	#	if len(foundTitle) > 0:
	#		title = foundTitle
	#		break
			
	imageLink = metadata["meta"]["see_also"]["_iiif_pres"]
	imageMetadata = requests.get(imageLink).json()
	title = imageMetadata["label"]
	imageUrls = []
	for sequence in imageMetadata["sequences"]:
		for canvas in sequence["canvases"]:
			for image in canvas["images"]:
				imageUrl = image["resource"]["@id"]
				#print(imageUrl)
				imageUrls.append(imageUrl)
	return metadata, imageMetadata, imageUrls, artist, title
	

def download(outDir, id):
	metadata, imageMetadata, imageUrls, artist, title = getItemMetadata(id)
	#print(imageUrls)
	#print(len(imageUrls))
	
	print("{} - {}: Downloading {} Images".format(artist, title, len(imageUrls)))
	
	outDir = "{}/{}".format(outDir, artist)
	if not os.path.exists(outDir):
		os.makedirs(outDir)
	baseName = "{}/{} - {} ({})".format(outDir, artist, title, id)
	print(baseName)
	

	if os.path.isfile(baseName + " - Object.json"):
		print("Already Downloaded")
		return
	saveMetadata(baseName + " - Object.json", metadata)
	saveMetadata(baseName + " - Images.json", imageMetadata)
	#id = 0
	#for imageUrl in imageUrls:
		#saveImageToFile(baseName + " [{:03}]".format(id), imageUrl)
		#id = id + 1

	id = 0
	imagePairs = []
	for imageUrl in imageUrls:
		imagePair = { "path":baseName + " [{:03}]".format(id), "url":imageUrl }
		imagePairs.append(imagePair)
		id = id + 1
	with Pool(5) as p:
		p.map(saveImagePairToFile, imagePairs)
		


def main(argv):
	opts, args = getopt.getopt(argv, "i:o", ["out=", "id="])

	outDir = ""
	ids = []

	for opt, arg in opts:
		if opt in ("--out", "-o"):
			outDir = arg
		elif opt in ("--id", "-i"):
			ids = arg.split(':')

	for id in ids:
		download(outDir, id)


if __name__ == "__main__":
	main(sys.argv[1:])


























