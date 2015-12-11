from automation import TaskManager
import tempfile
import time
import os
import copy
import json

# The list of sites that we wish to crawl
sites = ['http://www.example.com','https://princeton.edu','https://citp.princeton.edu/']

# Creates a temporary directory, where we will save the crawl DB
db_loc  = tempfile.mkdtemp() + '/openwpm_demo.sqlite'

# loads up the default preference dictionary
fp = open(os.path.join(os.path.dirname(__file__), 'automation/default_settings.json'))
preferences = json.load(fp)


browser_params = [copy.deepcopy(preferences) for i in xrange(0, 3)]

# Instantiates the measurement platform
# Launches two (non-headless) Firefox instances which log data using mitmproxy
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(db_loc, browser_params, 3)

# Visits the sites with both browsers simultaneously, 5 seconds between visits
for site in sites:
    manager.get(site, index='**') # ** = synchronized browsers
    time.sleep(5)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
