# -*- coding: utf-8 -*-
import selenium
from selenium.webdriver.common.keys import Keys
import time
import csv
import os 
from stat import ST_CTIME
import os
import sys
import json
import socket
import re
from shutil import copyfile, copytree, rmtree
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.support.wait import *
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import *
from selenium.webdriver.support.expected_conditions import *
import time, logging
#from  pype import *
import hashlib
import random
import datetime
import urllib2
import urllib
import copy
import random 



def wait_and_get_element(driver, selector) :
	print (selector)
	wait = WebDriverWait(driver,15).until(presence_of_element_located(((By.XPATH,selector[0]))))
	time.sleep(random.randint(2,10))
	elt = random.choice(driver.find_elements(By.XPATH,selector[0]))
	print elt
	if len(selector) is 1:
		return elt
	else :
		return random.choice(elt.find_elements(By.XPATH,selector[1]))

	
def visite_site(driver,crawled):
    site = random.choice(crawled["sites"])
    print site
    driver.get(site)
    """for i in range(3):  
		wait_and_get_element(driver,crawled["link_selector"]).click()
		driver.back()"""
    wait_and_get_element(driver,crawled["link_selector"]).click()


def simulate_shopping(driver,store_ ) :
	try:
		visite_site(driver,store_)
		for selector in store_["selectors"] :
			wait_and_get_element(driver,selector).click()
	except:
		pass
    
def crawler_Sport(driver): 
	# crawler les vélos de routes au hasard
	crawled=[{"name":"gosport","sites":["http://www.go-sport.com/sport/cycle/velo/l-7300003.html","http://www.go-sport.com/sport/running/chaussures/homme/l-730050101.html","http://www.go-sport.com/chaussures/femme/montagne/l-7320100.html"],"link_selector":["//a[@class='plPrName']"],"selectors":[["//select[@class='fpSizeSelect']",".//option"],["//button[@id='fpAddToBasket']"],["//button[@type='submit']"]]},\
	{"name":"cdiscount","sites":["http://www.cdiscount.com/le-sport/vetements-de-sport/vetements-homme/chaussures/l-121020528.html#_his_","http://www.cdiscount.com/le-sport/vetements-de-sport/vetements-homme/l-1210205.html#_his_","http://www.cdiscount.com/le-sport/vetements-de-sport/vetements-femme/l-1210206.html#_his_"],"link_selector":["//img[@class='prdtBImg']"],"selectors":[["//select[@class='jsSltSize']",".//option[position()>1]"],["//input[@id='fpAddBsk']"]]},\
	{"name":"decathlon","sites":["http://www.decathlon.fr/C-532933-chaussures-randonnee","http://www.decathlon.fr/F-10018-velos-route","http://www.decathlon.fr/C-674413-chaussures-running-homme"],"link_selector":["//img[@class='product_visuel']"],"selectors":[["//div[@class='product-size float']",".//li[@class='enabled']"],["//div[@class='add_to_cart_image_button']"]]}]
	print crawled[0]
	simulate_shopping(driver,crawled[0])
	simulate_shopping(driver,crawled[1])
	simulate_shopping(driver,crawled[2])

    

####### CDISCOUNT SPORT ########

    
    
def crawler_Comp(driver): 
#########UBALDI########    
	crawled = [{"name":"ubaldi", "sites":["http://www.ubaldi.com/informatique-telephone/ordinateur/ordinateur-portable/ordinateur-portable.php","http://www.ubaldi.com/tv/televiseur-lcd/televiseur-lcd.php","http://www.ubaldi.com/son/hi-fi-stereo/micro-chaine/micro-chaine.php"],"link_selector":['//div[@class="titre_desc_logo"]/*/a'],"selectors":[["//form[@id='ajouter_panier']"]]},\
	{"name":"fnac","sites":["http://www.fnac.com/Tous-les-ordinateurs-portables/Ordinateur-portable/nsh154425/w-4#","http://www.fnac.com/Tous-les-Reflex/Appareil-photo-numerique-reflex/nsh93998/w-4#bl=PECAppareil-photo-num%C3%A9rique-reflexBLO5","http://www.fnac.com/Tous-les-televiseurs/Televiseur/nsh75822/w-4#bl=MMtvh"],"link_selector":["//div[@class='Article-itemVisual']/img"],"selectors":[['//a[@id="addBasket"]'],["//a[@class='btn BasketPopin-actionButton']"]]},\
	{"name":"grosbill","sites":["http://www.grosbill.com/3-ordinateur_portable-ordi_portable-type-ordinateurs","http://www.grosbill.com/2-video_projecteur-type-tv_video","http://www.grosbill.com/3-televiseur_led-_televiseur_led-type-tv_video"],"link_selector":['//td[@class="img_product"]/div/a'],"selectors":[['//a[@id="lightbox_ajout_panier"]'],['//a[@class="btn_css3 btn_css3_orange btn_css3_medium"]']]}]
	simulate_shopping(driver,crawled[0])
	simulate_shopping(driver,crawled[1])
	simulate_shopping(driver,crawled[2])


def crawler_Clothes(driver):
    crawled=[{"name":"sarenza","sites":["http://www.sarenza.com/chaussures-nouveautes-mode-femme","http://www.sarenza.com/bottines-et-boots-homme","http://www.sarenza.com/escarpins-femme"],"link_selector":['//div[@class="img-content"]'],"selectors":[['//span[@class="select-content"]'],['.//a[@class="shoesize "]'],['//a[@id="add-to-basket"]']]},\
    {"name":"zalendo","sites":["http://www.zalando.fr/pantalons-homme/","http://www.zalando.fr/jeans-femme/","http://www.zalando.fr/chemisiers-tuniques-femme/"],"link_selector":['//div[@class="catalogArticlesList_content"]/a'],"selectors":[['//div[@id="sizeSelect"]/span'],['.//li[@class="available sizeLine"]'],['//button[@id="ajaxAddToCartBtn"]']]},\
    {"name":"kiabi", "sites":["http://www.kiabi.com/chemise-tunique-femme_201486","http://www.kiabi.com/chaussures-femme_201566","http://www.kiabi.com/pull-gilet-homme_200756"],"link_selector":['//span[@name="urlProduct"]'],"selectors":[['//div[@class="sizes_section block"]/span[@class="available"]'],['//input[@id="addToCartSubmit-0"]']]}] 
    simulate_shopping(driver,crawled[0])
    simulate_shopping(driver,crawled[1])
    simulate_shopping(driver,crawled[2])


