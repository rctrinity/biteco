# Utilities
import json, requests
from os import system, name
from queue import Queue

# Package Info
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


# Initialize queue to use as a buffer bewtween dashboard and RPC calls
q = Queue(maxsize = 3)


class GetAssetPrices(object):  
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
        
    def __init__(self, GoldForexURL="https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAU/USD"
                      ,BitcoinURL="https://api.coindesk.com/v1/bpi/currentprice.json"
                      ,Bitcoin_P=None
                      ,Gold_P=None):
        
        self.GoldForexURL = GoldForexURL   
        self.BitcoinURL =  BitcoinURL
        self.Bitcoin_P = self.getBTCUSD()
        self.Gold_P = self.getGLDUSD()
        
    def getBTCUSD(self) -> float:
        self = self._call(self.BitcoinURL)
        if self != None:
            return float(self['bpi']['USD']['rate_float'])
        else:
            return None
    
    def getGLDUSD(self) -> float:
        self = self._call(self.GoldForexURL)
        if self != None:
            for i in self:
                if i['topo']['platform'] == 'AT':
                    for j in i['spreadProfilePrices']:
                        if j['spreadProfile'] == 'standard':
                            return float(j['ask'])
        else:
            return None
    
    def _call(self, url) -> str:
        try:
            self = requests.get(url,timeout=3)
            url_json = self.text
            return json.loads(url_json)  
        except:
            return None  

    def __repr__(self):
        return f'GetAssetPrices({self.Bitcoin_P},{self.Gold_P},"{self.BitcoinURL}", "{self.GoldForexURL}")'             
        

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


__all__ = ('GetAssetPrices'
           ,'clear'
           ,'blockSubsidy'
           ,'PACKAGE_NAME'
           ,'COPYRIGHT'
           ,'GENESIS_REWARD'
           ,'COIN'
           ,'MAX_SUPPLY'
           ,'HALVING_BLOCKS'
           ,'EXAHASH'
           ,'BILLION'
           ,'GIGABIT'
           ,'TRILLION'
           ,'CONVERT_TO_SATS'
           ,'GOLD_OZ_ABOVE_GROUND'
           ,'q'
)


