from automation import TaskManager
import multiprocessing.pool
import sys
import time
import json
import os
from random import randint

# Runs a basic crawl which simply runs through a list of websites
g_sites = {}
manager = None
dump_location = None



class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess
    
 

def load_sites(site_path):
    """ loads a list of websites from a text file """
    sites = []
    i = 0
    f = open(site_path)
    for site in f:
		if i == 50:
			f.close()
			return sites
		cleaned_site = site.strip() if site.strip().startswith("http") else "http://" + site.strip()
		sites.append(cleaned_site)
		i+=1
    f.close()

    return sites


def create_profile(age, s, interest,  browser_index) :
	#print "Browser " + str(browser_index) +" run command profile_"+s+"_"+str(age)+"_"+interest+"_"+str(shop)
	manager.load_profile("default_profile",browser_index,6000)
	manager.google_settings(True,browser_index)
	time.sleep(2)
	manager.exelate_settings(age,s,browser_index)
	for site in g_sites[interest]:
		manager.browse(site,2, browser_index, 60000)
	manager.buying_intent(interest,browser_index)
		
		
def get_prices(browser_index):
	for site in g_sites["rtb"]:
		manager.get(site,browser_index, 60000)

def toggle_interest(interest) :
	if interest == "sport":
		return "shopping"
	elif interest == "shopping":
		return "computers"
	elif interest == "computers":
		return "sport"
	else:
		print "Unkonwn interest"
		return None

def create_chock(interest, chock, browser_index):
	new_intrest = ""
	if chock == "privacy":
		manager.do_optout(browser_index)
	elif chock == "new_interest":
		new_interest = toggle_interest(interest)
		for site in g_sites[new_interest]:
			manager.browse(site,2, browser_index, 60000)
	

def do_exp(age, s, interest,  chock, browser_index):
	#print "Browser " + str(browser_index) +" run command profile_"+s+"_"+str(age)+"_"+interest+"_"+str(shop)
	create_profile(age, s, interest, browser_index)
	get_prices(browser_index)
	create_chock(interest, chock, browser_index)
	get_prices(browser_index)
	dump_location = "experimentation_2/profile_"+s+"_"+str(age)+"_"+interest+"_chock_"+str(chock)
	manager.dump_profile(dump_location,False,browser_index,60000)
	manager.delete_all_cookies(browser_index)
	time.sleep(60)
	#manager.load_profile("default_profile",browser_index,6000)

def do_serialized_exp(params):
	print params
	tasks = params[0]
	browser_index = params[1]
	for task in tasks:
		print "Run experiment with settings: " + str(task[0]) +task[1] +task[2]+str(task[3])+ " on browser "+ str(browser_index)
		do_exp(task[0],task[1],task[2],task[3], browser_index)



def run_site_crawl(db_path,  preferences, dnt):
    """
    runs the crawl itself
    <db_path> is the absolute path of crawl database
    <preferences> is a dictionary of preferences to initialize the crawler
    """
    global manager 
    num_browser = 4
    if dnt:
		preferences["donottrack"] = True
    manager = TaskManager.TaskManager(db_path, preferences, num_browser)
    tasks = []
    index = 0
    params = []
    for i in range(0,num_browser):
		tasks.append([])
    for s in ["f","m"]:
		for age in [20,30,40]:
			for interest in ["sport","shopping","computers"]:
				print interest
				for chock in ["privacy","new_interest","none"]:
					dump_location = "experimentation_2/profile_"+s+"_"+str(age)+"_"+interest+"_chock_"+str(chock)
					if os.path.isdir(dump_location):
						continue
					browser_index = index % num_browser
					tasks[browser_index].append([age, s, interest, chock])
					index +=1
    for i in range(0,num_browser):
		params.append([tasks[i],i])
    print params
    pool = MyPool(num_browser )
    pool.map(do_serialized_exp,params)


    #manager.close()


def print_help_message():
    """ prints out the help message in the case that too few arguments are mentioned """
    print "\nMust call simple crawl script with at least one arguments: \n" \
          "The absolute directory path of the new crawl DB\n" \
          "Other command line argument flags are:\n" \
          "-browser: specifies type of browser to use (firefox or chrome)\n" \
          "-donottrack: True/False value as to whether to use the Do Not Track flag\n" \
          "-tp_cookies: string designating third-party cookie preferences: always, never or just_visted\n" \
          "-proxy: True/False value as to whether to use proxy-based instrumentation\n" \
          "-headless: True/False value as to whether to run browser in headless mode\n" \
          "-timeout: timeout (in seconds) for the TaskManager to default time out loads\n" \
          "-profile_tar: absolute path of folder in which to load tar-zipped user profile\n" \
          "-dump_location: absolute path of folder in which to dump tar-zipped user profile\n" \
          "-bot_mitigation: True/False value as to whether to enable bot-mitigation measures"


def main(argv):
    """ main helper function, reads command-line arguments and launches crawl """
    # filters out bad arguments
    if len(argv) < 1 :
        print_help_message()
        return

    db_path = argv[1]  # absolute path for the database
    g_sites["sport"] =load_sites(os.path.join(os.path.dirname(__file__),"top_sports"))
    g_sites["shopping"] = load_sites("top_shopping")
    g_sites["computers"] = load_sites("top_computers")
    g_sites["rtb"] = load_sites("liste_rtb")
    # loads up the default preference dictionary
    fp = open(os.path.join(os.path.dirname(__file__), 'automation/default_settings.json'))
    preferences = json.load(fp)
    fp.close()


    # overwrites the default preferences based on command-line inputs
    for i in xrange(2, len(argv), 2):
        if argv[i] == "-browser":
            preferences["browser"] = "chrome" if argv[i+1].lower() == "chrome" else "firefox"
        elif argv[i] == "-donottrack":
            preferences["donottrack"] = True if argv[i+1].lower() == "true" else False
        elif argv[i] == "-tp_cookies":
            preferences["tp_cookies"] = argv[i+1].lower()
        elif argv[i] == "-proxy":
            preferences["proxy"] = True if argv[i+1].lower() == "true" else False
        elif argv[i] == "-headless":
            preferences["headless"] = True if argv[i+1].lower() == "true" else False
        elif argv[i] == "-watch_rtb":
            preferences["watch_rtb"] = True if argv[i+1].lower() == "true" else False
        elif argv[i] == "-bot_mitigation":
            preferences["bot_mitigation"] = True if argv[i+1].lower() == "true" else False
        elif argv[i] == "-timeout":
            preferences["timeout"] = float(argv[i+1]) if float(argv[i]) > 0 else 30.0
        elif argv[i] == "-profile_tar":
            preferences["profile_tar"] = argv[i+1]
        elif argv[i] == "-disable_flash":
            preferences["disable_flash"] = True if argv[i+1].lower() == "true" else False
        elif argv[i] == "-dump_location":
            dump_location = argv[i+1]
    

    # launches the crawl with the updated preferences
    run_site_crawl(db_path,  preferences,True)
    run_site_crawl(db_path,  preferences,False)


if __name__ == "__main__":
    main(sys.argv)
