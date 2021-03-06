from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from google_commands import *
from exelate_commands import *
from intentions import *
import random
import time

from ..SocketInterface import clientsocket
from ..MPLogger import loggingclient
from utils.lso import get_flash_cookies
from utils.firefox_profile import get_cookies  # todo: add back get_localStorage,
from utils.webdriver_extensions import scroll_down, wait_until_loaded, get_intra_links

# Library for core WebDriver-based browser commands

NUM_MOUSE_MOVES = 10  # number of times to randomly move the mouse as part of bot mitigation
RANDOM_SLEEP_LOW = 1  # low end (in seconds) for random sleep times between page loads (bot mitigation)
RANDOM_SLEEP_HIGH = 7  # high end (in seconds) for random sleep times between page loads (bot mitigation)


def bot_mitigation(webdriver):
    """ performs three optional commands for bot-detection mitigation when getting a site """

    # bot mitigation 1: move the randomly around a number of times
    window_size = webdriver.get_window_size()
    num_moves = 0
    num_fails = 0
    while num_moves < NUM_MOUSE_MOVES + 1 and num_fails < NUM_MOUSE_MOVES:
        try:
            if num_moves == 0: #move to the center of the screen
                x = int(round(window_size['height']/2))
                y = int(round(window_size['width']/2))
            else: #move a random amount in some direction
                move_max = random.randint(0,500)
                x = random.randint(-move_max, move_max)
                y = random.randint(-move_max, move_max)
            action = ActionChains(webdriver)
            action.move_by_offset(x, y)
            action.perform()
            num_moves += 1
        except MoveTargetOutOfBoundsException:
            num_fails += 1
            #print "[WARNING] - Mouse movement out of bounds, trying a different offset..."
            pass

    # bot mitigation 2: scroll in random intervals down page
    scroll_down(webdriver)

    # bot mitigation 3: randomly wait so that page visits appear at irregular intervals
    time.sleep(random.randrange(RANDOM_SLEEP_LOW, RANDOM_SLEEP_HIGH))


def tab_restart_browser(webdriver):
    """
    kills the current tab and creates a new one to stop traffic
    note: this code if firefox-specific for now
    """
    if webdriver.current_url.lower() == 'about:blank':
        return

    switch_to_new_tab = ActionChains(webdriver)
    switch_to_new_tab.key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL)
    switch_to_new_tab.key_down(Keys.CONTROL).send_keys(Keys.PAGE_UP).key_up(Keys.CONTROL)
    switch_to_new_tab.key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL)
    switch_to_new_tab.perform()
    time.sleep(0.5)


def get_website(url, webdriver, proxy_queue, browser_params, extension_socket):
    """
    goes to <url> using the given <webdriver> instance
    <proxy_queue> is queue for sending the proxy the current first party site
    """

    tab_restart_browser(webdriver)
    main_handle = webdriver.current_window_handle

    # sends top-level domain to proxy and extension (if enabled)
    # then, waits for it to finish marking traffic in proxy before moving to new site
    if proxy_queue is not None:
        proxy_queue.put(url)
        while not proxy_queue.empty():
            time.sleep(0.001)
    if extension_socket is not None:
        extension_socket.send(url)

    # Execute a get through selenium
    try:
        webdriver.get(url)
    except TimeoutException:
        pass

    # Close modal dialog if exists
    try:
        WebDriverWait(webdriver, .5).until(EC.alert_is_present())
        alert = webdriver.switch_to_alert()
        alert.dismiss()
        time.sleep(1)
    except TimeoutException:
        pass

    # Close other windows (popups or "tabs")
    windows = webdriver.window_handles
    if len(windows) > 1:
        for window in windows:
            if window != main_handle:
                webdriver.switch_to_window(window)
                webdriver.close()
        webdriver.switch_to_window(main_handle)

    if browser_params['bot_mitigation']:
        bot_mitigation(webdriver)

def extract_links(webdriver, browser_params, manager_params):
    link_elements = webdriver.find_elements_by_tag_name('a')
    link_urls = set(element.get_attribute("href") for element in link_elements)

    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])
    create_table_query = ("""
    CREATE TABLE IF NOT EXISTS links_found (
      found_on TEXT,
      location TEXT
    )
    """, ())
    sock.send(create_table_query)

    if len(link_urls) > 0:
        current_url = webdriver.current_url
        insert_query_string = """
        INSERT INTO links_found (found_on, location)
        VALUES (?, ?)
        """
        for link in link_urls:
            sock.send((insert_query_string, (current_url, link)))

    sock.close()
    
    
def optOutYOC(webdriver):
    webdriver.get("http://www.youronlinechoices.com/fr/controler-ses-cookies/")
    time.sleep(60)
    webdriver.execute_script("window.scrollBy(0,1450)")
    opt_out_link = webdriver.find_element_by_id("allOptOutButton");
    opt_out_link.click();
    time.sleep(60)

def browse_website(url, num_links, webdriver, proxy_queue, browser_params, manager_params, extension_socket):
    """
    calls get_website before visiting <num_links> present on the page
    NOTE: top_url will NOT be properly labeled for requests to subpages
          these will still have the top_url set to the url passed as a parameter
          to this function.
    """
    # First get the site
    get_website(url, webdriver, proxy_queue, browser_params, extension_socket)

    # Connect to logger
    logger = loggingclient(*manager_params['logger_address'])

    # Then visit a few subpages
    for i in range(num_links):
        links = get_intra_links(webdriver, url)
        links = filter(lambda x: x.is_displayed() == True, links)
        if len(links) == 0:
            break
        r = int(random.random()*len(links)-1)
        logger.info("BROWSER %i: visiting internal link %s" % (browser_params['crawl_id'], links[r].get_attribute("href")))

        try:
            links[r].click()
            wait_until_loaded(webdriver, 300)
            time.sleep(1)
            if browser_params['bot_mitigation']:
                bot_mitigation(webdriver)
            webdriver.back()
        except Exception, e:
            pass
            
def buying_intent( shope, webdriver, browser_params):
	print "Called buying intent " + shope
	if shope == "sport":
		crawler_Sport(webdriver)
	if shope == "computer":
		crawler_Comp(webdriver)
	if shope == "shopping":
		crawler_Clothes(webdriver)

def dump_flash_cookies(top_url, start_time, webdriver, browser_params, manager_params):
    """ Save newly changed Flash LSOs to database
    We determine which LSOs to save by the `start_time` timestamp.
    This timestamp should be taken prior to calling the `get` for
    which creates these changes.
    """
    # Set up a connection to DataAggregator
    tab_restart_browser(webdriver)  # kills traffic so we can cleanly record data
    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    # Flash cookies
    flash_cookies = get_flash_cookies(start_time)
    for cookie in flash_cookies:
        query = ("INSERT INTO flash_cookies (crawl_id, page_url, domain, filename, local_path, \
                  key, content) VALUES (?,?,?,?,?,?,?)", (browser_params['crawl_id'], top_url, cookie.domain,
                                                          cookie.filename, cookie.local_path,
                                                          cookie.key, cookie.content))
        sock.send(query)

    # Close connection to db
    sock.close()

def set_exelate_settings(age, gender, language, interests, webdriver, browser_params):
	print "Called set\exelate\setting "+  gender
	webdriver.set_page_load_timeout(40)
	webdriver.get("http://exelate.com/privacy/opt-in-opt-out/")
	if age is not None:
		exelate_set_age(webdriver, age)
	if gender is not None:
		exelate_set_gender(webdriver, gender)
	if language is not None:
		exelate_set_language(webdriver, language)
	if interests is not None:
		exelate_add_interest(webdriver, interests)

def set_google_settings(optin, webdriver, browser_params):
	print "Called set\google\setting: "
	if optin:
		google_opt_in(webdriver) 
	else :
		google_opt_out(webdriver) 
		
def delete_cookies(webdriver):
	print "Deleting all cokies"
	#webdriver.delete_all_cookies()
	#webdriver.reset()

def dump_storage_vectors(top_url, start_time, webdriver, browser_params):
    """ Grab the newly changed items in supported storage vectors """

    # Set up a connection to DataAggregator
    tab_restart_browser(webdriver)  # kills traffic so we can cleanly record data
    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    # Flash cookies
    flash_cookies = get_flash_cookies(start_time)
    for cookie in flash_cookies:
        query = ("INSERT INTO flash_cookies (crawl_id, page_url, domain, filename, local_path, \
                  key, content) VALUES (?,?,?,?,?,?,?)", (browser_params['crawl_id'], top_url, cookie.domain,
                                                          cookie.filename, cookie.local_path,
                                                          cookie.key, cookie.content))
        sock.send(query)

    # Close connection to db
    sock.close()

def dump_profile_cookies(top_url, start_time, webdriver, browser_params, manager_params):
    """ Save changes to Firefox's cookies.sqlite to database

    We determine which cookies to save by the `start_time` timestamp.
    This timestamp should be taken prior to calling the `get` for
    which creates these changes.

    Note that the extension's cookieInstrument is preferred to this approach,
    as this is likely to miss changes still present in the sqlite `wal` files.
    This will likely be removed in a future version.
    """
    # Set up a connection to DataAggregator
    tab_restart_browser(webdriver)  # kills traffic so we can cleanly record data
    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    # Cookies
    rows = get_cookies(browser_params['profile_path'], start_time)
    if rows is not None:
        for row in rows:
            query = ("INSERT INTO profile_cookies (crawl_id, page_url, baseDomain, name, value, \
                      host, path, expiry, accessed, creationTime, isSecure, isHttpOnly) \
                      VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (browser_params['crawl_id'], top_url) + row)
            sock.send(query)
    
    # localStorage - TODO this doesn't have a modified time support
    #rows = get_localStorage(profile_dir, start_time)
    #if rows is not None:
    #    for row in rows:
    #        query = ("INSERT INTO localStorage (crawl_id, page_url, scope, KEY, value) \
    #                  VALUES (?,?,?,?)",(crawl_id, top_url) + row)
    #        sock.send(query)

    # Close connection to db
    sock.close()
