#!/usr/bin/python

from urllib2 import urlopen
from lxml import html
import sys


def main(argv):
	""" main helper function, reads command-line arguments and launches crawl """
	# filters out bad arguments
	if len(argv) < 2:
		print "Please add a category"
		return
	for n in range(5):
		#d = html.fromstring(urlopen("http://www.alexa.com/topsites/countries;%d/FR" % (n, )).read())
		d = html.fromstring(urlopen("http://www.alexa.com/topsites/category;%d/Top/%s" % (n,argv[1], )).read())
		for site in d.cssselect("div.desc-container p a"):
			domain = site.get("href").split("/")[-1]
			if domain != "":
				print site.get("href").split("/")[-1]


if __name__ == "__main__":
    main(sys.argv)

