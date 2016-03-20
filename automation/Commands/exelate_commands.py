import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit

# exelate ad settings page class declarations

GENDER_DIV = "qJ oZ"
AGE_DIV = "qJ cZ"
LANGUAGES_DIV = "qJ uZ"
INTERESTS_DIV = "qJ h0"

OPTIN_DIV = "to Uj kZ"
OPTOUT_DIV = "UZ Uj BL"
EDIT_DIV = "to Uj c-eb-qf c-eb-Jh"
RADIO_DIV = "a-z rJ c0"
SUBMIT_DIV = "c-ba-aa a-b a-b-E ey"
ATTR_SPAN = "Fn"

EDIT_DIV_SIGNIN = "Uj Ks c-eb-qf c-eb-Jh"

LANG_DROPDOWN = "c-ba-aa c-g-f-b a-ra xx"
LANG_DIV = "c-l"

PREF_INPUT = "j0 a-na nU"
PREF_TR = "mU tx f0"
PREF_TD = "qA g0"
CROSS_TD = "rA"
PREF_OK_DIV = "c-ba-aa a-b a-b-E rT yL"

SIGNIN_A = "gb_70"

# strip html

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def exelate___init__(driver):
			self.reset()
			self.fed = []
	def exelate_handle_data(self, d):
			self.fed.append(d)
	def exelate_get_data(driver):
			return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()  


def exelate_set_income(driver, income):
        #"""Set gender on exelate Ad Settings page"""
        #try:
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            etbody = driver.find_element_by_xpath(".//th[@class='RadioButtonCategoryName' and text()='Household Income']/parent::tr[1]")
            time.sleep(3)
            if(income>=150000):
                box = etbody.find_element_by_xpath(".//td/input[1]")
            elif(income>=125000 and income<=149999):  
                box = etbody.find_element_by_xpath(".//td/input[2]")
            elif(income>=100000 and income<=124999):  
                box = etbody.find_element_by_xpath(".//td/input[3]")
            elif(income>=75000 and income<=99999):  
                box = etbody.find_element_by_xpath(".//td/input[4]")
            elif(income>=60000 and income<=74999):
                box = etbody.find_element_by_xpath(".//td/input[5]")
            elif(income>=50000 and income<=59999):  
                box = etbody.find_element_by_xpath(".//td/input[6]")
            elif(income>=40000 and income<=49999):  
                box = etbody.find_element_by_xpath(".//td/input[7]")
            elif(income>=30000 and income<=39999):  
                box = etbody.find_element_by_xpath(".//td/input[8]")
            elif(income>=20000 and income<=29999):
                box = etbody.find_element_by_xpath(".//td/input[5]")
            elif(income<=20000):
                box = etbody.find_element_by_xpath(".//td/input[10]")
            time.sleep(3)
            box.click()


    
def exelate_set_gender(driver, gender):
        #"""Set gender on exelate Ad Settings page"""
        #try:
            etbody = driver.find_element_by_xpath(".//th[@class='RadioButtonCategoryName' and text()='Gender']/parent::tr[1]")
            time.sleep(3)
            if(gender == 'f'):
                box = etbody.find_element_by_xpath(".//input[1]")        # MALE          
            elif(gender == 'm'):
                box = etbody.find_element_by_xpath(".//input[2]")            # FEMALE
            time.sleep(3)
            box.click()
#           #self.log("setGender="+gender+"||"+str(self.treatment_id))
            #self.log('treatment', 'gender', gender)
        #except:
            #print "Could not set gender. Did you opt in?"
            #self.log('error', 'setting gender', gender)
"""
def get_child_with_text(parent, value):
	for node in parent:
		if node.text()"""
        
def exelate_set_age(driver, age):
        #"""Set age on exelate Ad Settings page"""
        #try:
            etbody = driver.find_element_by_xpath(".//th[@class='RadioButtonCategoryName' and text()='Age']/parent::tr[1]")
            print etbody.text
            time.sleep(3)
            if(age>=18 and age<=24):
                box = etbody.find_element_by_xpath(".//td/input[1]")
            elif(age>=25 and age<=34):  
                box = etbody.find_element_by_xpath(".//td/input[2]")
            elif(age>=35 and age<=44):  
                box = etbody.find_element_by_xpath(".//td/input[3]")
            elif(age>=45 and age<=54):  
                box = etbody.find_element_by_xpath(".//td/input[4]")
            elif(age>=55 and age<=64):
                box = etbody.find_element_by_xpath(".//td/input[5]")
            elif(age>=65):
                box = etbody.find_element_by_xpath(".//td/input[6]")

         
            time.sleep(3)
            box.click()
            time.sleep(3)
            #gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
            #self.log('treatment', 'age', age)
#           #self.log("setAge="+str(age)+"||"+str(treatment_id))
        #except:
            #print "Could not set age. Did you opt in?"
            #self.log('error', 'setting age', age)

def exelate_set_language(driver, language):   
        #"""Set language on exelate Ad Settings page"""
        #try:
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            gdiv = driver.find_element_by_xpath(".//div[@class='"+LANGUAGES_DIV+"']")
            gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
            gdiv.find_element_by_xpath(".//div[@class='"+LANG_DROPDOWN+"']").click()
            time.sleep(3)
            gdiv.find_element_by_xpath(".//div[@class='"+LANG_DIV+"'][contains(.,'"+language+"')]").click()
            gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
#           log("setLanguage="+str(language)+"||"+str(self.treatment_id), id, LOG_FILE)
            #self.log('treatment', 'language', language)
        #except:
            #print "Could not set language"
            #self.log('error', 'setting language', language)

def exelate_remove_interest(driver, pref):
        #"""Remove interests containing pref on the exelate Ad Settings page"""
        #try:
            prefs = self.get_interests(text="interests prior to removal")
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            rem = []
            while(1):
                trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
                flag=0
                for tr in trs:
                    td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']")
                    div = tr.find_element_by_xpath(".//td[@class='"+CROSS_TD+"']/div")
                    int = td.get_attribute('innerHTML')
                    if pref.lower() in div.get_attribute('aria-label').lower():
                        flag=1
                        hover = ActionChains(driver).move_to_element(td)
                        hover.perform()
                        time.sleep(1)
                        td.click()
                        div.click()
                        rem.append(int)
                        time.sleep(2)
                        break
                if(flag == 0):
                    break
            driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
            #self.log('treatment', 'remove interest ('+pref+')', "@|".join(rem))
        #except:
         #   print "No interests matched '%s'. Skipping." %(pref)
            #self.log('error', 'removing interest', pref)


def exelate_add_interest_onexelate(driver, pref, count=1, signedin=0):
        """Set interests on Ad Settings"""
#         try:
        driver.set_page_load_timeout(40)
        driver.get("http://exelate.com/privacy/opt-in-opt-out/")
        driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV_SIGNIN+"']")[0].click()
        for i in range(0,count):
            driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(pref)
            driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(Keys.RETURN)
#             driver.find_element_by_xpath(".//div[@class='"+PREF_INPUT_FIRST+"']").click()
            time.sleep(1)
        trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
        print len(trs), "interest(s) added"
        for tr in trs:
            td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']").get_attribute('innerHTML')
            #self.log('treatment', 'add interest ('+pref+')', td)
        time.sleep(2)
        driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
#         except:
#             print "Error setting interests containing '%s'. Maybe no interests match this keyword." %(pref)
#             #self.log('error', 'adding interest', pref)

def exelate_add_interest(driver, pref, count=1, signedin=0):
        """Set interests on Ad Settings"""
#         try:
        driver.set_page_load_timeout(40)
        driver.get("http://exelate.com/privacy/opt-in-opt-out/")
        driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3-signedin].click()
        for i in range(0,count):
            driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(pref)
            driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(Keys.RETURN)
#             driver.find_element_by_xpath(".//div[@class='"+PREF_INPUT_FIRST+"']").click()
            time.sleep(1)
        trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
        print len(trs), "interest(s) added"
        for tr in trs:
            td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']").get_attribute('innerHTML')
            #self.log('treatment', 'add interest ('+pref+')', td)
        time.sleep(2)
        driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
#         except:
#             print "Error setting interests containing '%s'. Maybe no interests match this keyword." %(pref)
#             #self.log('error', 'adding interest', pref)


def exelate_get_gender(driver):
        """Read gender from exelate Ad Settings"""
        inn = "Error reading"
        try:
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            gdiv = driver.find_element_by_xpath(".//div[@class='"+GENDER_DIV+"']")
            inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
            #self.log('measurement', 'gender', inn)
        except:
            print "Could not get gender. Did you opt in?"
            #self.log('error', 'getting gender', inn)
        return inn
    
def exelate_get_age(driver):
        """Read age from exelate Ad Settings"""
        inn = "Error reading"
        try:
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            gdiv = driver.find_element_by_xpath(".//div[@class='"+AGE_DIV+"']")
            inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
            #self.log('measurement', 'age', inn)
        except:
            print "Could not get age. Did you opt in?"
            #self.log('error', 'getting age', inn)
        return inn
    
def exelate_get_language(driver): 
        """Read language from exelate Ad Settings"""
        inn = "Error reading"
        try:
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            gdiv = driver.find_element_by_xpath(".//div[@class='"+LANGUAGES_DIV+"']")
            inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
            #self.log('measurement', 'language', inn)
        except:
            print "Could not get language. Did you opt in?"
            #self.log('error', 'getting language', inn)
#       #self.log("language"+"||"+str(self.treatment_id)+"||"+inn)
        return inn
        
def exelate_get_interests(driver, text="interests"):                                  
        """Returns list of Ad preferences"""
        pref = []
        try:
            driver.set_page_load_timeout(40)
            driver.get("http://exelate.com/privacy/opt-in-opt-out/")
            driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            ints = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']/td[@class='"+PREF_TD+"']")
            for interest in ints:
                pref.append(str(interest.get_attribute('innerHTML')))
            #self.log('measurement', text, "@|".join(pref))
        except:
            print "Error collecting ad preferences. Skipping." %(pref)
            #self.log('error', 'getting '+text, "@|".join(pref))
#       #self.log("pref"+"||"+str(self.treatment_id)+"||"+"@|".join(pref))
        return pref 
