# load the API key
import ConfigParser
p = ConfigParser.ConfigParser()
p.read("SF.ini")
apikey = p.get("SF", "APIkey")
p.read("current_level.ini")
venue = p.get("Level", "exch")
stock = p.get("Level", "symbol")

# Shut up the SSL warnings
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# For non-blocking URL dispatching
import requests_futures
from requests_futures.sessions import FuturesSession

session = FuturesSession()
def bg_cb(sess, resp):
    # parse the json storing the result on the response object
    resp.data = resp.json()

def lookuporders(idlist):
    lookup_uri = "https://api.stockfighter.io/ob/api/venues/{:s}/stocks/{:s}/orders/{:s}"
    orders = [session.delete(lookup_uri.format(venue, stock, str(orderid)), 
                headers={"X-Starfighter-Authorization":apikey}, 
                background_callback=bg_cb) 
              for orderid in idlist]
    return orders
    
def reap(orderlist):
    #This is where all the blocking happens, really
    responses = [x.result() for x in orderlist]
    return [x.data for x in responses]


import sys, json

orders = {}
orders_to_lookup = []
pending_lookups = []
for line in sys.stdin:
    data = json.loads(''.join(line.split()[3:]))
    order_id = data['order']['id']
    order_acct = data['order']['account']
    standing_id = data['standingId']
    incoming_id = data['incomingId']

    # we can always assign the order_id to its account, so do that
    orders[order_id] = order_acct
    if standing_id not in orders:
        if standing_id not in orders_to_lookup:orders_to_lookup.append(standing_id)
    if incoming_id not in orders:
        if incoming_id not in orders_to_lookup:orders_to_lookup.append(incoming_id)

    if len(orders_to_lookup) >= 10:
        if len(pending_lookups)>0:
            newdata = reap(pending_lookups)
            for oid, data in zip(pending_ids, newdata):
                acct = data['error'].split()[-1].strip('.')
                orders[oid] = acct
                print oid, acct, data
        pending_lookups = lookuporders(orders_to_lookup)
        pending_ids = list(orders_to_lookup)
        orders_to_lookup = []

