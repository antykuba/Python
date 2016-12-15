from bs4 import BeautifulSoup
import urllib2
import re
import time
import multiprocessing 
import sys
import csv


CSVfile = open('dane.csv', 'a')
writer = csv.writer(CSVfile, delimiter="|")


mainPageUrl = 'http://www.....html'
mainPage = urllib2.urlopen(mainPageUrl)
mainSoup = BeautifulSoup(mainPage.read())
mainUrls = mainSoup.findAll("a", attrs={"class": "PaginationLink"})
mainSubpages = int(mainUrls[len(mainUrls)-2].get_text())


mainSubpageUrlsList = [mainPageUrl]
for i in range(2, mainSubpages+1):
	mainSubpageUrl = 'http://www.....html'
	iteration = "-p%s.html" % i
	mainSubpageUrl = mainSubpageUrl[0:-5] + iteration
	mainSubpageUrlsList.append(mainSubpageUrl)
#lista podstron ze strony glownej


firmSubpages = []
for j in range(0, len(mainSubpageUrlsList)):
	try:
		req2 = urllib2.Request(mainSubpageUrlsList[j], 'Mozilla/5.0')
		handle2 = urllib2.urlopen(req2)
	except urllib2.HTTPError, e:
		print("error")
	#mainPage2 = urllib2.urlopen(mainSubpageUrlsList[j])
	mainSoup2 = BeautifulSoup(handle2.read())
	firmUrlsEarly = mainSoup2.findAll("div", attrs={"class": "SecondSection"})
	for el in firmUrlsEarly:
		firmRevNum = el.findAll("p")
		revNum = re.findall(r'\d+', firmRevNum[0].get_text())
		revNum = int(revNum[0])
		if revNum >= 50:
			firmUrls = el.findAll("a", attrs={"href": re.compile("http://www.....html")})
			for el2 in firmUrls:
				firmSubpages.append(el2.get('href')[0:-8])
				print(el2.get('href'))
# DO TEGO MOMENTU POBIERANE SA ADRESY PODSTRON KAZDEJ FIRMY, KTORA MA WIECEJ NIZ 50 WPISOW NA SWOJ TEMAT. ADRESY TE SA W LISCIE O NAZWIE: firmSubpages
	
id = 1
i = 0
for i in range(0, len(firmSubpages)):
	try:
		req = urllib2.Request(firmSubpages[i], 'Mozilla/5.0')
		req_h = urllib2.urlopen(req)
		firmNumSoup = BeautifulSoup(req_h.read())
		firmNum = firmNumSoup.findAll("div", attrs={"class": "Pagination"})
		firmName = firmNumSoup.find("h1", attrs={"id": "PageTitle"}).text
		firmNum = firmNum[0].findAll("a")
		firmSubpageUrl = firmNum[0].get('href')
		firmNum = int(firmNum[len(firmNum)-2].get_text())
		i += 1
		firmSubpages2 = []
		for k in range(1, firmNum+1):
			firmSubpageUrl2 = re.sub(r'_2_+', '_'+str(k)+'_', firmSubpageUrl)
			firmSubpages2.append(firmSubpageUrl2)
			#print firmSubpageUrl2
		it = 0
	except:
		print("error - powtarzam")
	while it < len(firmSubpages2):
		try:
			el2 = firmSubpages2[it]
			firmSubpage = urllib2.urlopen(el2)
			firmSubpageSoup = BeautifulSoup(firmSubpage.read())
			firmRevs = firmSubpageSoup.findAll("a")
			powt = 0
			while powt < len(firmRevs):
				try:
					if "Read Full Review" in str(firmRevs[powt]):
						req3 = urllib2.Request(firmRevs[powt].get('href'), 'Mozilla/5.0')
						handle3 = urllib2.urlopen(req3)
						firmRevSoup = BeautifulSoup(handle3.read())
						if '\xc2\xa3' in firmRevSoup:
							firmRevSoup = firmRevSoup.replace("\xc2\xa3", "GBP")
						firmRev = firmRevSoup.find("span", attrs={"property": "v:description"}).text
						firmRev = firmRev.encode('utf-8')
						writer.writerow([id,firmRev,firmName[0:-7]])
						#print(str(id) + firmName + firmRev[0:30])
						print("ID: " + str(id) + " dla firmy: " + firmName)
						id += 1
					powt += 1
				except:
					print("error")
			it += 1
		except:
			print("error")