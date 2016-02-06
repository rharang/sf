import argparse, ConfigParser, requests, json

p = ConfigParser.ConfigParser()
p.read("/home/ubuntu/stockfighter/SF.ini")
apikey = p.get("SF", "APIkey")

p = argparse.ArgumentParser()
p.add_argument('acct', action='store', type=str)
args = p.parse_args()

def do_post(URI, data):
    resp = requests.post(URI, headers={"X-Starfighter-Authorization":apikey}, json=data)
    return resp


answer = {
    "account":args.acct,
    "explanation_link":"https://github.com/rharang/sf",
    "executive_summary":"""Visual analysis of trading patterns shows three classes of accounts:\n1. Large, presumably institutional, accounts that move huge amounts of stock and cash around with apparent indifference to losses.\n2. Market makers, whose accumulated positions over time have a high-frequency (in the Fourier transform sense of the word) sawtooth appearance, driven by their rapid alternation between modest buy and sell orders.\n3. The suspect, who makes very large and fairly regular buy and sell orders at approximately 30 day staggered intervals, and frequenty makes long sequences of smaller buys, leading to a more square-wave appearance in accumulated position.\n\nGithub code may take me a little while to clean up and post the final evidence file."""
}

URL="https://www.stockfighter.io/gm/instances/19795/judge"

print json.dumps(answer)
#do_post(URI, json.dumps(answer))
r = do_post(URL, answer)
print r
