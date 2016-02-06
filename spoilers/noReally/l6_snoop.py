import sys, json, zmq
import argparse, ConfigParser, requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
def do_post(URI, data):
    resp = requests.post(URI, headers={"X-Starfighter-Authorization":apikey}, json=data)
    return resp.json()

def do_get(URI):
    resp = requests.get(URI, headers={"X-Starfighter-Authorization":apikey})
    return resp.json()


from dateutil.parser import parse

from twisted.internet import reactor
from twisted.python import log
import time, sys

import requester as r

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS
from twisted.internet.protocol import ReconnectingClientFactory

import warnings
warnings.filterwarnings("ignore", category=r.requests.packages.urllib3.exceptions.InsecurePlatformWarning)


class ClientProtocol(WebSocketClientProtocol):
    def onOpen(self):
        self.factory.resetDelay()
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.PUB)
        self.sock.connect("ipc:///tmp/quotes")
        self.msg_ct = 0

    def onClose(self, wasClean, code, reason):
        print wasClean, code, reason

    def onMessage(self, payload, isBinary):
        #self.msg_ct+=1
        #sys.stdout.write("\r"+str(self.msg_ct)); sys.stdout.flush()
        if not isBinary:
            data = payload.decode('utf8')
            self.ts = time.time()
            self.sock.send(str(self.ts) +" "+str(args.venue)+" "+str(args.acct)+" "+str(data))

        else:
            print("Binary message")
    
    def onPing(self, payload):
        self.sendPong(payload)

class ClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol=ClientProtocol
    
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed:", reason
        print "Retrying..."
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        print "Dropped:", reason
        print "Reconnecting..."
        self.retry(connector)


if __name__ == '__main__':

    p = ConfigParser.ConfigParser()
    p.read("SF.ini")
    apikey = p.get("SF", "APIkey")

    p = argparse.ArgumentParser()
    p.add_argument('venue', action='store', type=str)
    p.add_argument('acct', action='store', type=str)
    p.add_argument('--ticker', action='store_true')
    p.add_argument('--use_config', action='store_true')
    args = p.parse_args()

    #log.startLogging(sys.stdout)
    if args.use_config:
        p = ConfigParser.ConfigParser()
        p.read('current_level.ini')
        args.acct = p.get("Level", 'acct')
        args.venue = p.get("Level", 'exch')


    ticker_exuri = "wss://api.stockfighter.io/ob/api/ws/{:s}/venues/{:s}/tickertape".format(args.acct, args.venue)
    exec_exuri = "wss://api.stockfighter.io/ob/api/ws/{:s}/venues/{:s}/executions".format(args.acct, args.venue)
        
    if args.ticker:
        factory_exec = ClientFactory(ticker_exuri, debug=False)
    else:
        factory_exec = ClientFactory(exec_exuri, debug=False)
    connectWS(factory_exec)

    reactor.run()
