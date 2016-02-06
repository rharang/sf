import argparse, requests, ConfigParser, json
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


p = ConfigParser.ConfigParser()
p.read("SF.ini")
apikey = p.get("SF", "APIkey")
p = argparse.ArgumentParser()

subp = p.add_subparsers(help='commands', dest='command')

start_p = subp.add_parser('start', help="start a level")
start_p.add_argument("name", action='store', type=str, help="Level name to start")
start_p.add_argument('--pp_instructions', action='store_true')
start_p.add_argument('--save', action='store_true')

restart_p = subp.add_parser('restart', help="restart a level")
restart_p.add_argument("ID", action='store', type=str, help="Level ID")

stop_p = subp.add_parser("stop", help="stop a level")
stop_p.add_argument("--ID", action='store', type=str, help="Level ID", default=None)

resume_p = subp.add_parser("resume", help="resume and resend level data")
resume_p.add_argument("ID", action='store', type=str, help="Level ID")

check_p = subp.add_parser("check", help="check to see if the level is active")
check_p.add_argument("ID", action='store', type=str, help="Level ID")

levels_p = subp.add_parser("levels", help="look at levels and instanceids (may not be active)")


a = p.parse_args()

URL="https://www.stockfighter.io/gm"

def do_post(URI, data):
    resp = requests.post(URI, headers={"X-Starfighter-Authorization":apikey}, json=data)
    return resp.content

def do_get(URI):
    resp = requests.get(URI, headers={"X-Starfighter-Authorization":apikey})
    return resp.content

if a.command == 'start':
    resp = do_post(URL+"/levels/"+a.name, data={})
    resp = json.loads(resp)
    if a.pp_instructions: 
        for k in resp['instructions'].keys():
            print resp['instructions'][k]
    del resp['instructions']
    print resp
    if a.save:
        p = ConfigParser.ConfigParser()
        p.add_section("Level")
        p.set(section='Level', option='id', value=resp['instanceId'])
        p.set(section='Level', option='acct', value=resp['account'])
        p.set(section='Level', option='symbol', value=resp['tickers'][0])
        p.set(section='Level', option='exch', value=resp['venues'][0])
        p.write(open('current_level.ini', 'w'))
        print "current level config saved"
        
elif a.command == 'restart':
    print do_post(URL+"/instances/"+a.ID+"/restart", data={})
elif a.command == 'stop':
    if a.ID==None:
        p = ConfigParser.ConfigParser()
        p.read("current_level.ini")
        a.ID = p.get("Level", "id")
    print do_post(URL+"/instances/"+a.ID+"/stop", data={})
elif a.command == 'resume':
    print do_post(URL+"/instances/"+a.ID+"/resume", data={})
elif a.command == 'check':
    print do_get(URL+"/instances/"+a.ID)
elif a.command == 'levels':
    print do_get(URL+"/levels")
