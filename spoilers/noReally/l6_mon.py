# load the API key
import ConfigParser
p = ConfigParser.ConfigParser()
p.read("SF.ini")
apikey = p.get("SF", "APIkey")

# Shut up the SSL warnings
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# For non-blocking URL dispatching
import requests_futures
from requests_futures.sessions import FuturesSession

session = FuturesSession()

# queue to get the incoming messages from the ticker
import zmq
context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.bind("ipc:///tmp/quotes")
sock.setsockopt(zmq.SUBSCRIBE, '')



orders = {}
while 1:
    message = sock.recv()
    print message
    
    
