import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit

# Google ad settings page class declarations



OPTIN_SPAN = "ll hI"
OPTOUT_SPAN = "ll jI"


# strip html

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def google___init__(driver):
			self.reset()
			self.fed = []
	def google_handle_data(self, d):
			self.fed.append(d)
	def google_get_data(driver):
			return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()  




def google_opt_in(driver):
        #"""Opt in to behavioral advertising on Google"""
     #   try:
            print "Opting in to google ads"
            driver.set_page_load_timeout(60)
            driver.get("https://www.google.com/settings/u/0/ads/anonymous")
            driver.find_element_by_xpath("//span[@class='"+OPTIN_SPAN+"']/div").click()
            time.sleep(2)
    #       if(self.unit_id != -1):
            #self.log('treatment', 'optin', 'True')
    #    except:
            #self.log('error', 'opting in', 'True')
        
def google_opt_out(driver):
        #"""Opt out of behavioral advertising on Google"""
        #try:
            driver.set_page_load_timeout(60)
            driver.get("https://www.google.com/settings/u/0/ads/anonymous")
            driver.find_element_by_xpath("//span[@class ='"+OPTOUT_SPAN+"']/div").click()
            time.sleep(2)
            driver.execute_script("document.getElementsByName('ok')[1].click();")  
    #       if(self.unit_id != -1):
            #self.log('treatment', 'optout', 'True')
        #except:
            #self.log('error', 'opting out', 'True')

