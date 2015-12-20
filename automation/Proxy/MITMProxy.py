from ..SocketInterface import clientsocket
from libmproxy import controller
import sys
import Queue
import mitm_commands


from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, Float
from bulbs.neo4jserver import Graph
import sys
from urlparse import urlparse, parse_qs
from math import log, sqrt
import cProfile as profile


# Neo4j models
class Host(Node):
    """ Example:
        name = "example.com"
        origin = 1 # Sets a cookie. 0 if host doesn't set a cookie.
    """
    element_type = "host"
    name = String()
    origin = Integer(default=0)
    incrawl = Integer(default=0)
    known_tracker = Integer(default=0)
    
class Refers(Relationship):
    """ cookie-[:refers]->domain
    Indicates that the cookie is send with domain in the referer. 
    """
    label = "refers"

class Uses(Relationship):
    """ cookie-[:uses]->host
    Indicates that the cookie is send directly to the host. 
    """
    label = "uses"
    key = String()

class Cookie(Node):
    """ Example:
        value = "bufeguifsgfyegufg34gr4i2gfy"
        session = 1 # This is a session cookie. 0 if it's not.
    """
    element_type = "cookie"
    value = String()
    entropy = String()
    session = Integer(default=0)
    inurl = Integer(default=0)
    inetag = Integer(default=0)

class Sets(Relationship):
    """ host-[:sets]->cookie
    """
    label = "sets"
    key = String()

hostcache = dict()
cookiecache = dict()
setscache = set()
usescache = set()
referscache = set()

def entropy(s):
    return -len(s)*sum([log(float(s.count(c))/len(s),2)*float(s.count(c))/len(s) for c in set(s)])

def get_host_str(urlstring):
    """Retrieve the host from a url string"""
    try:
        netloc = urlparse(urlstring).netloc
    except:
        print urlstring
        return ""
    if not netloc:
        return ""
    if len(netloc.split(".")) > 2:
        if netloc.endswith("co.uk"): # Hack for co.uk domains
            return ".".join(netloc.split(".")[-3:])
        return ".".join(netloc.split(".")[-2:])
    return netloc

# Lookup host in the database.
# Create a node for the given hostname if it doesn't exist.
# Return the node for the given hostname
def get_or_create_host(name, origin=0):
    global g
    global hostcache
    if hostcache.has_key(name):
        return hostcache[name]
    #hosts = list(g.host.index.lookup("name", name))
    #if len(hosts) > 0:
    #    hostcache[name] = hosts[0]
    #    return hosts[0]
    hostcache[name] = g.host.get_or_create("name", name, {"name":name, "origin":origin})
    return hostcache[name]

# Lookup cookie in the database.
# Create a node for the given cookie if it doesn't exist.
# Return the node for the given cookie
def get_or_create_cookie(value):
    global g
    global cookiecache
    if cookiecache.has_key(value):
        return cookiecache[value]
    #cookies = list(g.cookie.index.lookup("value", value))
    #if len(cookies) > 0:
    #    cookiecache[value] = cookies[0]
    #    return cookies[0]
    cookiecache[value] = g.cookie.get_or_create("value", value, {"value":value, "entropy":str(entropy(value))})
    return cookiecache[value]
    
    # At the start of mitmproxy connect to the Neo4j database
def start():
    global g
    g = Graph()
    g.add_proxy("host", Host)
    g.add_proxy("uses", Uses)
    g.add_proxy("cookie", Cookie)
    g.add_proxy("sets", Sets)
    g.add_proxy("refers", Refers)
    
      
# Called when a http response is received. 
#def response(context, flow):
#    profile.runctx("response_profile(context, flow)", globals(), locals())

def response(flow):
    global g
    # Get the hostname from the corresponding request
    host = flow.request.host
    if len(host.split(".")) > 2:
        if host.endswith("co.uk"): # Hack for co.uk domains
            host = ".".join(host.split(".")[-3:])
        else:
            host = ".".join(host.split(".")[-2:])
    host = get_or_create_host(host)
    # Store parameters in the url as session cookies
    for (key, val) in flow.request.get_query().lst:
        cookie = get_or_create_cookie(value=val)
        if not cookie.inurl:
            cookie.inurl=1
            cookie.save()
        if not (host._id, cookie._id) in usescache:
            g.uses.create(host, cookie)
            usescache.add((host._id, cookie._id))
    # Get the referer from the request
    referer = None
    if flow.request.headers["Referer"]:
        if len(flow.request.headers["Referer"]) > 0:
            referer = get_host_str(flow.request.headers["Referer"][0])
        if referer:
            referer = get_or_create_host(referer)
    # Store all cookies that are set in the response
    for cookiestr in flow.response.headers["Set-Cookie"]:
        key, value = cookiestr.split("; ")[0].split("=", 1 )
        if not value:
            continue
        cookie = get_or_create_cookie(value=value)
        if cookiestr.find("Expires=") > -1:
            cookie.session = 0
            cookie.save()
        if not (host._id, cookie._id) in setscache:
            g.sets.create(host, cookie)
            setscache.add((host._id, cookie._id))
    # Store all cookies that are send in the request
    for cookiestr in flow.request.headers["Cookie"]:
        for subcookie in cookiestr.split("; "):
            key, value = subcookie.split("=",1)
            if not value: continue
            cookie = get_or_create_cookie(value=value)
            if host.outV("uses") is None or cookie not in host.outV("uses"):
                g.uses.create(host, cookie)
            if referer:
                if not (cookie._id, referer._id) in referscache:
                    g.refers.create(cookie, referer)
                    referscache.add((cookie._id, referer._id))
    # Store the ETag as a cookie
    for etag in flow.response.headers["ETag"]:
        cookie = get_or_create_cookie(value=etag)
        if not cookie.inetag:
            cookie.inetag=1
            cookie.save() 
        if host.outV("uses") is None or cookie not in host.outV("uses"):
                g.uses.create(host, cookie)
        if referer:
                if not (cookie._id, referer._id) in referscache:
                    g.refers.create(cookie, referer)
                    referscache.add((cookie._id, referer._id))
        




class InterceptingMaster (controller.Master):
    """
    Customized MITMProxy
    Extends the proxy controller to add some additional
    functionality for handling /logging requests and responses

    Inspired by the following example. Note the gist has a lot of bugs.
    https://gist.github.com/dannvix/5285924
    """
    
    def __init__(self, server, crawl_id, url_queue, db_socket_address):
        self.crawl_id = crawl_id
        #start()
        
        # Attributes used to flag the first-party domain
        self.url_queue = url_queue  # first-party domain provided by BrowserManager
        self.prev_top_url, self.curr_top_url = None, None  # previous and current top level domains
        self.prev_requests, self.curr_requests = set(), set()  # set of requests for previous and current site

        # Open a socket to communicate with DataAggregator
        self.db_socket = clientsocket()
        self.db_socket.connect(*db_socket_address)

        controller.Master.__init__(self, server)

    def load_process_message(self, q, timeout):
        """ Tries to read and process a message from the proxy queue, returns True iff this succeeds """
        try:
            msg = q.get(timeout=timeout)
            controller.Master.handle(self, *msg)
            return True
        except Queue.Empty:
            return False

    def tick(self, q, timeout=0.01):
        """ new tick function used to label first-party domains and avoid race conditions when doing so """
        if self.curr_top_url is None:  # proxy is fresh, need to get first-party domain right away
            self.curr_top_url = self.url_queue.get()
        elif not self.url_queue.empty():  # new FP has been visited
            # drains the queue to get rid of stale messages from previous site
            while self.load_process_message(q, timeout):
                pass

            self.prev_requests, self.curr_requests = self.curr_requests, set()
            self.prev_top_url, self.curr_top_url = self.curr_top_url, self.url_queue.get()

        self.load_process_message(q, timeout)

    def run(self):
        """ Light wrapper around run with error printing """
        try:
            controller.Master.run(self)
        except KeyboardInterrupt:
            print 'KeyboardInterrupt received. Shutting down'
            self.shutdown()
            sys.exit(0)
        except Exception as ex:
            print str(ex)
            print 'Exception. Shutting down proxy!'
            self.shutdown()
            raise

    def handle_request(self, msg):
        """ Receives HTTP request, and sends it to logging function """
        msg.reply()
        self.curr_requests.add(msg.request)
        mitm_commands.process_general_mitm_request(self.db_socket, self.crawl_id, self.curr_top_url, msg)

    # Record data from HTTP responses
    def handle_response(self, msg):
        """ Receives HTTP response, and sends it to logging function """
        msg.reply()

        # attempts to get the top url, based on the request object
        if msg.request in self.prev_requests:
            top_url = self.prev_top_url
            self.prev_requests.remove(msg.request)
        elif msg.request in self.curr_requests:
            top_url = self.curr_top_url
            self.curr_requests.remove(msg.request)
        else:  # ignore responses for which we cannot match the request
            return

        mitm_commands.process_general_mitm_response(self.db_socket, self.crawl_id, top_url, msg)
        
        #response(msg)
