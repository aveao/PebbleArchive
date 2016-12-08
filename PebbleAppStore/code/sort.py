import glob
import os
import json
import re

allJsons = glob.glob("*.json")

erroredFile = open("sorterror.txt", "a")

for jsonFile in allJsons:
	jsFile = open(jsonFile)
	try:
		jsonData = json.loads(jsFile.read())
		jsFile.close()
	except:
		erroredFile.write(jsonFile+"nothing\n")
		continue
	appId = jsonData["data"][0]["id"]
	appName = jsonData["data"][0]["title"]
	appName = appName.replace("/", "")
	appName = re.sub(r'[^\x00-\x7F]+',' ', appName)
	print appName
	fChar = appName[0].upper()
	sChar = ""
	try:
		sChar = appName[1].upper()
	except:
		sChar = "SP"
	if not sChar.isalnum():
		sChar = "SP"
	if not fChar.isalnum():
		fChar = "SP"
	if not os.path.isfile(appId+".pbw"):
		erroredFile.write(appId+" no pbw\n")
		continue
	if not os.path.isfile(appId+".png"):
		erroredFile.write(appId+" no image\n")
		continue
	try:
		os.mkdir("data/"+fChar+"/"+sChar+"/"+appName)
	except:
		print "\t Folder already exists"
		pass
	try:
		os.rename(appId+".pbw", "data/"+fChar+"/"+sChar+"/"+appName+"/"+appId+".pbw")
		os.rename(appId+".png", "data/"+fChar+"/"+sChar+"/"+appName+"/"+appId+".png")
		os.rename(appId+".json", "data/"+fChar+"/"+sChar+"/"+appName+"/"+appId+".json")
	except Exception,e:
		erroredFile.write(appId+" failed to move:\n")
		erroredFile.write(str(e))
		pass
erroredFile.close()