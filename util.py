# Utilities

import json, requests
from os import system, name
from queue import Queue

# Package Info
VERSION = 101
SUB_VERSION = 'v0.1.1'
SUB_SUB_VERSION = 'Stable'
PACKAGE_NAME = 'Bitcoin Economics'
COPYRIGHT = '© Farley'

# Bitcoin Hard-Code Info
GENESIS_REWARD = 50
COIN = 100000000
CENT = 1000000
MAX_SUPPLY = 21000000
HALVING_BLOCKS = 210000

# Format Conversions
EXAHASH = 1000000000000000000
BILLION = 1000000000
GIGABIT = BILLION
CONVERT_TO_SATS = 0.00000001
TRILLION = 1000000000000

# Gold Info
OUNCES_IN_METRIC_TON = 32150.75
 # https://www.gold.org/goldhub/data/how-much-gold 2/8/2023
GOLD_SUPPLY_METRIC_TON = 208874
GOLD_OZ_ABOVE_GROUND = OUNCES_IN_METRIC_TON * GOLD_SUPPLY_METRIC_TON

PrevBTCPrice = None
PrevGLDPrice = None
PrevBlockHeight = None

q = Queue(maxsize = 0)

class GetAssetPrices(object):  
    def __init__(self, GoldForexURL="https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAU/USD",
                 getBTCURL="https://api.coindesk.com/v1/bpi/currentprice.json"):
        
        self.GoldForexURL = GoldForexURL   
        self.getBTCURL =  getBTCURL
        
    def getBTCUSD(self):
        global PrevBTCPrice
        
        try:
            r = self._call(self.getBTCURL)
            return r['bpi']['USD']['rate_float']
        except:
            return PrevBTCPrice
    
    def getGLDUSD(self):
        global PrevGLDPrice
        
        try:
            r = self._call(self.GoldForexURL)[1]
            prevGLDPrice = r['spreadProfilePrices'][0]['ask']
            return r['spreadProfilePrices'][0]['ask']
        except:
            return PrevGLDPrice
    
    def _call(self, url):
        self = requests.get(url)
        url_json = self.text
        return json.loads(url_json)       
        

# Clear screen between refresh
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def blockSubsidy(MAX_HEIGHT):
    bs = GENESIS_REWARD * COIN
    bs >>= int(MAX_HEIGHT / HALVING_BLOCKS)
    bs /= COIN
    return bs 

