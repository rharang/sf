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

#import json 
#
#from blessings import Terminal
#T = Terminal()
#
#import time, random, copy, math, sys
#
#import numpy as np
#from dateutil import parser
#
#def status_str(q):
#    quote = copy.deepcopy(q)
#    if 'lastSize' not in quote:
#        quote['lastSize']=0
#        quote['last']=0
#        quote['lastTrade']=''
#    else:quote['lastTrade']=quote['lastTrade'].split("T")[1]
#    if 'bid' not in quote:
#        quote['bid']=0
#        quote['bidSize']=0
#        quote['bidDepth']=0
#    if 'ask' not in quote:
#        quote['ask']=0
#        quote['askSize']=0
#        quote['askDepth']=0
#    quote['quoteTime'] = quote['quoteTime'].split("T")[1]
#    return "{quoteTime:18.18s} {symbol:5.5s}//L:{lastSize:9.0f}@{last:9.0f}: {lastTrade}; [{bidDepth:6.0f}] b:{bidSize:9.0f}@{bid:9.0f} - a:{askSize:9.0f}@{ask:9.0f} [{askDepth:6.0f}]".format(**quote)
#
#def bg_cb(sess, resp):
#    # parse the json storing the result on the response object
#    resp.data = resp.json()
#
#def placeorder(stock, qty, venue, acct, price, direction, orderType='limit'):
#    order_uri = 'https://api.stockfighter.io/ob/api/venues/{:s}/stocks/{:s}/orders' 
#    def build_dict(qty, price, direction):
#        od = { 
#            'account':acct,'venue':venue,'stock':stock,'orderType':orderType,
#            'price':price,'qty':qty,'direction':direction,
#            }
#        return od
#    bid = build_dict(qty, price, direction)
#    order = session.post(
#                        order_uri.format(venue, stock), 
#                        json=bid, background_callback=bg_cb,
#                        headers={"X-Starfighter-Authorization":apikey}
#                        ) 
#    return order 
#
#def killorders(idlist, stock, venue):
#    delete_uri = 'https://api.stockfighter.io/ob/api/venues/{:s}/stocks/{:s}/orders/{:s}' 
#    orders = [session.delete(delete_uri.format(venue, stock, str(orderid)), 
#                headers={"X-Starfighter-Authorization":apikey}, 
#                background_callback=bg_cb) 
#              for orderid in idlist]
#    return orders
#
#def checkorders(idlist, stock, venue):
#    get_uri = 'https://api.stockfighter.io/ob/api/venues/{:s}/stocks/{:s}/orders/{:s}'  
#    orders = [session.get(get_uri.format(venue, stock, str(orderid)), 
#                headers={"X-Starfighter-Authorization":apikey}, 
#                background_callback=bg_cb) 
#              for orderid in idlist]
#    return orders
#
#def reap(orderlist):
#    "This is where all the blocking happens, really"
#    responses = [x.result() for x in orderlist]
#    return [x.data for x in responses]
#
#



orders = {}
while 1:
    message = sock.recv()
    print message
    
    
