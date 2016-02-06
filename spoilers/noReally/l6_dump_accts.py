import ConfigParser, json, argparse, subprocess, time, sys
from collections import Counter
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

uri = "https://api.stockfighter.io/ob/api"

p = ConfigParser.ConfigParser()
p.read("SF.ini")
apikey = p.get("SF", "APIkey")
p.read("current_level.ini")
venue = p.get("Level", "exch")
stock = p.get("Level", "symbol")

def do_post(URI, data={}):
    resp = requests.post(URI, headers={"X-Starfighter-Authorization":apikey}, json=data)
    return resp.content

def do_get(URI):
    resp = requests.post(URI, headers={"X-Starfighter-Authorization":apikey})
    return resp.content

t0 = time.time()

#get the last trade number 
data = json.loads(do_get(uri+"/venues/{:s}/stocks/{:s}/orders/{:s}/cancel".format(venue, stock, str(2**64-1))))
print data
last = int(data['error'].split()[-1].strip(")"))

found_accts = Counter()
onum = max(0, last-50)
data = {'error':""}
consec_refusals = 0
subprocesses = []
try:
    while 1:
        onum +=1 
        sys.stdout.write('\r'+str(onum));sys.stdout.flush()
        try:
            data = json.loads(do_get(uri+"/venues/{:s}/stocks/{:s}/orders/{:s}/cancel".format(venue, stock, str(onum))))
            consec_refusals = 0
        except requests.exceptions.ConnectionError:
            consec_refusals+=1
            print 'oops, got refused...', consec_refusals
        if 'error' not in data:
            time.sleep(.25)
            continue
        new_acct = data['error'].split()[-1].strip('.')
        found_accts[new_acct]+=1
        if found_accts[new_acct]==3:
            # for some reason there's a bunch of accounts that just place one order for like 20 shares
            # and are never heard from again, which chews up websocket resources.  So ignore them.  We'll lose some
            # but hopefully not enough to make much of a difference if we collect for a while
            print new_acct, time.time()-t0
            subprocesses.append(subprocess.Popen(["/usr/bin/python", "./l6_snoop.py", venue, new_acct]))
except KeyboardInterrupt:
    #This should kill all of the subprocesses somehow...
    for p in subprocesses:
        p.kill()
