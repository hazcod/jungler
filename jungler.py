#!/usr/bin/python3

# https://github.com/HazCod/jungler

import urllib.request
import re
import sys
import os.path

tracks = 'tracks'
cookies = ''

def get(url_, isfile=False):
	global cookies
	req = urllib.request.Request(url=url_, headers={ 'Cookie' : cookies, 'Referer' : 'http://junglevibe1.net/', 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' })
	f = urllib.request.urlopen(req)
	cookies += getCookies(str(f.info()))
	if isfile is True:
		return f.read()
	else:
		return f.read().decode("UTF-8")

def getCookies(h):
	result = ''
	for setcookie in re.findall('Set-Cookie:.*', h):
		result += 'Cookie: ' + setcookie[setcookie.index(' ')+1:setcookie.index(';')] + '; '
	return result

def encodeSearch(search):
	return 'https://junglevibe1.net' + '/' + tracks + '/' + re.sub(r'[^A-Za-z0-9\s]+', '', search).replace(' ','_') + ".html"

def getResults(page):
	return re.findall('https*://junglevibe1\.net' + '/track/[0-9]+/[0-9]+/[A-z_-]+\.mp3\?dl=1', page)

def search(title):
	return getResults(get(encodeSearch(title)))

def extractTitle(url):
	title = re.search('[A-z_-]+\.mp3', url).group(0)
	return title.replace('_',' ').replace('-', ' - ')

def showOptions(results):
	link = None
	if len(results) > 1:
		while (link is None):
			print("Pick your result: ")
			print("-----------------")
			i = 0
			for result in results:
				print(str(i) + ' : ' + extractTitle(result))
				i += 1
			chosen = input('Option number: ')
			if chosen.isdigit() and int(chosen) >= 0 and int(chosen) < len(results):
				return results[int(chosen)]
	elif len(results) == 1:
		return results[0]
	else:
		print("Not found")
		sys.exit(1)

def main(userinput):
	results = search(userinput)
	link = showOptions(results)

	print("Saving to " + extractTitle(link))
	mp3 = None
	tries = 10
	while (mp3 is None or '404 Not Found' in str(mp3)) and tries > 0:
		print("Trying to fetch.. (" + str(tries) + " tries left)")
		mp3 = get(link.replace('dl=1', 'dl=2').replace("http://", "https://"), True)
		tries = tries - 1

	if '404 Not Found' in str(mp3):
		print("Failed to download. Pick another one or retry")
		main(userinput)

	filename = extractTitle(link)
	if os.path.isfile(filename):
		filename += '-1'
	with open(filename, "wb") as f:
		f.write(mp3)
	print("Downloaded to " + filename)

if __name__ == "__main__":
	main(sys.argv[1])
