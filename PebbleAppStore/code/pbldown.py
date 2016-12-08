import json
import requests
import codecs
import os
#This isn't invoked directly, though it could be.
#Instead, use an rqworker to run a ton of workers on a bunch of machines. 
def downloadArray(arrayToDownload):
	headers = {'Origin':'https://apps.getpebble.com', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6', 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2914.3 Safari/537.36', 'content-type':'application/x-www-form-urlencoded', 'accept': 'application/json'}
	arr = list(json.loads(arrayToDownload))
	print arr
	# We're going to download the main JSON description, the PBW file, the search images, and now the backdrop and the screenshots. 
	# Ideally, we want all of the data that we possibly can get, in order to reconstruct as much of the store as possible.
	#https://appstore-api.getpebble.com/v2/apps/id/583e4226ca30949f47000337?image_ratio=1&hardware=basalt&firmware_version=3
	for app in arr:
		print app
		try:
			try:
				os.mkdir(app)
			except:
				pass
			os.chdir(app)
			jsonR = requests.get("https://appstore-api.getpebble.com/v2/apps/id/"+app+"?image_ratio=1")
			jsonDat = json.loads(jsonR.text)

			#Main JSON
			output=codecs.open(app+".json", "w", "utf-8")
			output.write(jsonR.text)
			output.close()

			# PBW
			if "latest_release" in jsonDat["data"][0]:
				pbw_url = jsonDat["data"][0]["latest_release"]["pbw_file"]
				r = requests.get(pbw_url, stream=True)
				with open(app+".pbw", 'wb') as f:
					for chunk in r.iter_content(chunk_size=1024): 
						if chunk:
							f.write(chunk)
					f.close()


			#list images (search results)
			if "list_image" in jsonDat["data"][0]:
				limage = ""
				if "144x144" in jsonDat["data"][0]["list_image"]:
					limage = jsonDat["data"][0]["list_image"]["144x144"]
				elif "80x80" in jsonDat["data"][0]["list_image"]:
					limage = jsonDat["data"][0]["list_image"]["80x80"]
				try:
					splitted = limage.split("/")
					if splitted[2]=="assets.getpebble.com" and splitted[3] == "api" and splitted[4] == "file":
						limage = "https://assets.getpebble.com/api/file/"+splitted[5]+"/convert?cache=true"
				except:
					pass
				r = requests.get(limage, stream=True)
				with open(app+"-list.png", 'wb') as f:
					for chunk in r.iter_content(chunk_size=1024): 
						if chunk:
							f.write(chunk)
					f.close()
			# Screenshot images
			if "screenshot_images" in jsonDat["data"][0]:
				savedIms=0
				for image in jsonDat["data"][0]["screenshot_images"]:
					limage = ""
					if "144x168" in image:
						limage = image["144x168"]
					else:
						if len(image.keys()) > 0:
							limage = image[image.keys()[0]]
					try:
						splitted = limage.split("/")
						if splitted[2]=="assets.getpebble.com" and splitted[3] == "api" and splitted[4] == "file":
							limage = "https://assets.getpebble.com/api/file/"+splitted[5]+"/convert?cache=true"
					except:
						pass
					r = requests.get(limage, stream=True)
					with open(app+"-screen-"+str(savedIms)+".png", 'wb') as f:
						for chunk in r.iter_content(chunk_size=1024): 
							if chunk:
								f.write(chunk)
						f.close()
					savedIms = savedIms+1
			#Icon image (because you never know what you might need....)
			if "icon_image" in jsonDat["data"][0]:
				image = jsonDat["data"][0]["icon_image"]
				limage = ""
				if not isinstance(image, basestring):
					if "48x48" in image:
						limage = image["48x48"]
					else:
							if len(image.keys()) > 0:
								limage = image[image.keys()[0]]
					try:
						splitted = limage.split("/")
						if splitted[2]=="assets.getpebble.com" and splitted[3] == "api" and splitted[4] == "file":
							limage = "https://assets.getpebble.com/api/file/"+splitted[5]+"/convert?cache=true"
					except:
						pass
					r = requests.get(limage, stream=True)
					with open(app+"-icon.png", 'wb') as f:
						for chunk in r.iter_content(chunk_size=1024): 
							if chunk:
								f.write(chunk)
						f.close()
			if "header_images" in jsonDat["data"][0]:
				image = jsonDat["data"][0]["header_images"]
				limage = ""
				if not isinstance(image, basestring):
					image = image[0]
					if "orig" in image:
						limage = image["orig"]
					else:
						if len(image.keys()) > 0:
							limage = image[image.keys()[0]]
					try:
						splitted = limage.split("/")
						if splitted[2]=="assets.getpebble.com" and splitted[3] == "api" and splitted[4] == "file":
							limage = "https://assets.getpebble.com/api/file/"+splitted[5]+"/convert?cache=true"
					except:
						pass
					r = requests.get(limage, stream=True)
					with open(app+"-header.png", 'wb') as f:
						for chunk in r.iter_content(chunk_size=1024): 
							if chunk:
								f.write(chunk)
						f.close()
		except:
			filErrors = open("errors.txt", "a")
			filErrors.write(app)
			filErrors.write("\n")
			filErrors.close()
		finally:
			os.chdir("..")