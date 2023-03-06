# Utility

import json, requests
from os import system, name

VERSION = 101
SUB_VERSION = 'v0.01'
SUB_SUB_VERSION = 'BETA'
PACKAGE_NAME = 'Bitcoin Economics'
COPYRIGHT = '© Farley\nInspiration from https://bitcoin.clarkmoody.com/dashboard'

# Bitcoin hardcoded info
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

class GetAssetPrices(object):  
    def __init__(self, GoldForexURL="https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAU/USD",
                 getBTCURL="https://api.coindesk.com/v1/bpi/currentprice.json"):
        
        self.GoldForexURL = GoldForexURL   
        self.getBTCURL =  getBTCURL
        
    def getBTCUSD(self):
        try:
            r = self._call(self.getBTCURL)
            return r['bpi']['USD']['rate_float']
        except:
            return None
    
    def getGLDUSD(self):
        try:
            r = self._call(self.GoldForexURL)[1]
            return r['spreadProfilePrices'][0]['ask']
        except:
            return None
    
    def _call(self, url):
        try:
            self = requests.get(url)
            url_json = self.text
            return json.loads(url_json)       
        except:
            return None


def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def BlockSubsidy(MAX_HEIGHT):
    bs = GENESIS_REWARD * COIN
    bs >>= int(MAX_HEIGHT / HALVING_BLOCKS)
    bs /= COIN
    return bs 


def marketCapitalization(coinsMined, blockSubsidy, UNSPENDABLE):
    getAssetPrices = GetAssetPrices()
    BTCPrice = getAssetPrices.getBTCUSD()
    GLDPrice = getAssetPrices.getGLDUSD()
    
    if BTCPrice != None:
        satusd = (1/(BTCPrice * CONVERT_TO_SATS))
        blockSubsidyValue =  blockSubsidy * BTCPrice
        MarketCap = ((coinsMined + UNSPENDABLE) * BTCPrice) / BILLION  # Format in Billions
    else:
        satusd = 0
        blockSubsidyValue = 0
        MarketCap = 0
    
    if BTCPrice != None and GLDPrice != None:
        BTCvsGOLDMarketCap = ((coinsMined + UNSPENDABLE) * BTCPrice) / (GLDPrice * GOLD_OZ_ABOVE_GROUND) * 100
        BTCPricedInGold = BTCPrice/GLDPrice
    else:
        BTCvsGOLDMarketCap = 0
        BTCPricedInGold = 0

    if BTCPrice == None:
        BTCPrice = 0        
    
    PctIssued = ((coinsMined + UNSPENDABLE) / MAX_SUPPLY) * 100
    IssuanceRemaining = MAX_SUPPLY - coinsMined - UNSPENDABLE
    
    return satusd, blockSubsidyValue, MarketCap, BTCvsGOLDMarketCap, BTCPricedInGold, PctIssued, IssuanceRemaining, BTCPrice

