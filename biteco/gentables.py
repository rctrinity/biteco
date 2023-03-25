# Generate data and tables for terminal dashboard
from rich.table import Table
from rich import box
from rich.text import Text
from rich.layout import Layout
from rich.panel import Panel
from bitcoin import rpc
from bitcoin.core.serialize import uint256_from_compact, compact_from_uint256
import datetime, time
from time import sleep
import math
from typing import Tuple
import biteco.util
from biteco.util import GetAssetPrices, PrevBTCPrice, blockSubsidy, PrevBlockHeight, HALVING_BLOCKS, GIGABIT, GENESIS_REWARD, COIN, PACKAGE_NAME, EXAHASH, \
COPYRIGHT, TRILLION, CONVERT_TO_SATS, GOLD_OZ_ABOVE_GROUND, MAX_SUPPLY, BILLION, q

# Dashboard attributes
panelBox = box.SIMPLE
dashBox = box.HORIZONTALS
tblBrdrStyle = 'dim bold deep_sky_blue1'
tblTtlStyle = 'white'
colDescStyle = 'bright_black'
colValStyle = 'bright_white'
tblwidth = 45

# Initializing a queue 


class generateDataForTables(object):
    def __init__(self, 
                 proxy=None, 
                 nBlocksToHalving=0, 
                 BTCPrice=0, 
                 GLDPrice=0, 
                 satusd=0, 
                 MarketCap=0, 
                 BTCPricedInGold=0, 
                 BTCvsGOLDMarketCap=0, 
                 coinsMined=0, 
                 PctIssued=0,  
                 UNSPENDABLE=0, 
                 IssuanceRemaining=0, 
                 BlockSubsidy=0, 
                 blockSubsidyValue=0, 
                 MAX_HEIGHT=0, 
                 chainSize=0,
                 bestNonce=0, 
                 difficulty=0, 
                 targetBits=0, 
                 bestBlockAge=0, 
                 Connections=0, 
                 ConnectionsIn=0, 
                 verification=0, 
                 getNtwrkHashps=0, 
                 get7DNtwrkHashps=0, 
                 get4WNtwrkHashps=0, 
                 get1DNtwrkHashps=0, 
                 chainwork=0, 
                 totalTXs=0, 
                 txRatePerSec=0, 
                 txCount=0, 
                 diffEpoch=0, 
                 avg_2016_blockTime=0, 
                 avgEpochBlockTime=0, 
                 epochBlocksRemain=0, 
                 RetargetDate=None, 
                 estDiffChange=0, 
                 bnNew=0, 
                 halvingDate=None, 
                 subsidyEpoch=0, 
                 BestBlockHash=0, 
                 nTargetTimespan=0, 
                 nTargetSpacing=0, 
                 nSecsHour=0, 
                 nBlocksHour=0, 
                 nInterval=0, 
                 EpochHead = 0, 
                 bestBlockTimeUnix=0, 
                 bestBlockHeader = None): 
        global PrevBlockHeight
        self.proxy=proxy
        if self.proxy == None:
            self.proxy=rpc.Proxy()

        getAssetPrices = GetAssetPrices()
        self.nTargetTimespan = 14 * 24 * 60 * 60                     
        self.nTargetSpacing = 10 * 60                                
        self.nSecsHour = 60 * 60                                     
        self.nBlocksHour = (self.nSecsHour / self.nTargetSpacing)              
        self.nInterval = self.nTargetTimespan / self.nTargetSpacing
        # Proxy calls
        self.bestBlockHash = self.proxy.getbestblockhash()
        self.bestBlockHeader = self.proxy.getblockheader(self.bestBlockHash)
        currentInfo = self.proxy.call('gettxoutsetinfo', 'muhash')
        chainTxStats = self.proxy.call('getchaintxstats')  
        getBlockChainInfo = self.proxy.call('getblockchaininfo')
        getNetworkInfo = self.proxy.call('getnetworkinfo') 
        self.Connections = getNetworkInfo['connections'] 
        self.ConnectionsIn = getNetworkInfo['connections_in']
        self.getNtwrkHashps = self.proxy.call('getnetworkhashps',-1)  / EXAHASH                    
        self.get7DNtwrkHashps = self.proxy.call('getnetworkhashps', int(self.nInterval) >> 1) / EXAHASH    
        self.get4WNtwrkHashps = self.proxy.call('getnetworkhashps', int(self.nInterval) << 1) / EXAHASH    
        self.get1DNtwrkHashps = self.proxy.call('getnetworkhashps', int(self.nInterval) // 14) / EXAHASH        
        
        self.bestNonce = self.bestBlockHeader.nNonce
        self.difficulty = self.bestBlockHeader.difficulty/TRILLION
        self.targetBits = self.bestBlockHeader.nBits
        self.bestBlockTimeUnix = time.mktime(datetime.datetime.utcfromtimestamp(self.bestBlockHeader.nTime).timetuple())
        self.coinsMined = float(currentInfo['total_amount'])
        self.UNSPENDABLE = float(currentInfo['total_unspendable_amount'])
        
        self.BTCPrice = getAssetPrices.getBTCUSD()
        if self.BTCPrice == None:
            self.BTCPrice = 0
        self.GLDPrice = getAssetPrices.getGLDUSD()
        if self.GLDPrice == None:
            self.GLDPrice = 0
        try:
            self.BTCPricedInGold = self.BTCPrice / self.GLDPrice
        except:
            self.BTCPricedInGold = 0
        try:
            self.BTCvsGOLDMarketCap = ((self.coinsMined + self.UNSPENDABLE) * self.BTCPrice) / (self.GLDPrice * GOLD_OZ_ABOVE_GROUND) * 100
        except:
            self.BTCvsGOLDMarketCap = 0
        
        self.totalTXs = chainTxStats['txcount']
        self.txRatePerSec = chainTxStats['txrate']
        self.txCount = chainTxStats['window_tx_count']         
        self.chainSize = getBlockChainInfo['size_on_disk'] / GIGABIT
        self.MAX_HEIGHT = getBlockChainInfo['blocks']
        if PrevBlockHeight == None:
            PrevBlockHeight = self.MAX_HEIGHT
        self.chainwork = math.log2(int(getBlockChainInfo['chainwork'], 16))
        self.verification = getBlockChainInfo['verificationprogress'] * 100        
        self.diffEpoch = 1+(self.MAX_HEIGHT // self.nInterval)
        self.BlockSubsidy = blockSubsidy(self.MAX_HEIGHT)
        self.blockSubsidyValue = self.BlockSubsidy * self.BTCPrice
        self.subsidyEpoch = 1 +(self.MAX_HEIGHT // HALVING_BLOCKS)                        
        self.BestBlockAge = self.bestBlockAge()    
        self.avg_2016_blockTime = self.AvgBlockTimePrevEpoch()
        self.avgEpochBlockTime, self.EpochHead = self.AvgBlockTimeEpoch()       
        self.nBlocksToHalving = self.blocksToHalving()
        self.halvingDate = self.HalvingDate() 
        self.PctIssued = ((self.coinsMined + self.UNSPENDABLE) / MAX_SUPPLY) * 100
        self.IssuanceRemaining = MAX_SUPPLY - self.coinsMined - self.UNSPENDABLE
        try:
            self.satusd = (1/(self.BTCPrice * CONVERT_TO_SATS))
        except:
            self.satusd = 0    
        self.MarketCap = self.marketCap()
        
        self.estDiffChange, self.epochBlocksRemain, self.RetargetDate, self.bnNew = self.Retarget()
    
    
    def marketCap(self) -> float:
        self = ((self.coinsMined + self.UNSPENDABLE) * self.BTCPrice) / BILLION
        return self
    
    def blocksToHalving(self) -> int:
        return int(HALVING_BLOCKS - (self.MAX_HEIGHT % HALVING_BLOCKS))
        
    def AvgBlockTimePrevEpoch(self) -> str:
        start_2016_block = int((self.MAX_HEIGHT - (self.MAX_HEIGHT % self.nInterval)) - self.nInterval)
        end_2016_block = int((self.MAX_HEIGHT - (self.MAX_HEIGHT % self.nInterval))-1)
        try:
            startBlockTime = self.proxy.getblockheader(self.proxy.getblockhash(start_2016_block))
            endBlockTime = self.proxy.getblockheader(self.proxy.getblockhash(end_2016_block)) 
            self = str(datetime.timedelta(seconds=(round( (endBlockTime.nTime - startBlockTime.nTime) / self.nInterval,0)))).lstrip("0:")
            return self
        except:
            return '0:00' 
        
    
    def AvgBlockTimeEpoch(self) -> str:
        epochStartBlock = int(self.MAX_HEIGHT - (self.MAX_HEIGHT % self.nInterval))
        
        try:
            epochHead = self.proxy.getblockheader(self.proxy.getblockhash(epochStartBlock)) 
            return str(datetime.timedelta(seconds=(round( (self.bestBlockHeader.nTime - epochHead.nTime) / int(self.MAX_HEIGHT % self.nInterval),0)))).lstrip("0:"), epochHead
        except:
            return '0:00', 0
    
    
    def bestBlockAge(self) -> str:
        self = str(datetime.timedelta(seconds=(round(time.mktime(datetime.datetime.utcnow().timetuple()) - self.bestBlockTimeUnix, 0)))).lstrip("0:")
        return self
        
    def Retarget(self) -> tuple[float, int, str, int]:
        nEpochTargetTimespan = int(( self.MAX_HEIGHT % self.nInterval ) * self.nTargetSpacing)
        nEpochActualTimespan = int(self.bestBlockHeader.nTime - self.EpochHead.nTime)

        if (nEpochActualTimespan < nEpochTargetTimespan/4):
            nEpochActualTimespan = nEpochTargetTimespan/4
        if (nEpochActualTimespan > nEpochTargetTimespan*4):
            nEpochActualTimespan = nEpochTargetTimespan*4
    
        bnnew = uint256_from_compact(self.bestBlockHeader.nBits)
        bnnew *= nEpochActualTimespan
        bnnew //= nEpochTargetTimespan
        bnnew = compact_from_uint256(bnnew)
     
        diffchange = (1-(nEpochActualTimespan / nEpochTargetTimespan)) * 100
        blocksremain = int(self.nInterval - (self.MAX_HEIGHT % self.nInterval))
        secsToAdd = (blocksremain  / self.nBlocksHour) * self.nSecsHour
        retargetdate = datetime.datetime.fromtimestamp(self.bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
        
        return diffchange, blocksremain, retargetdate, bnnew
        
        
    def HalvingDate(self) -> str:
        secsToAdd = (self.nBlocksToHalving / self.nBlocksHour) * self.nSecsHour
        self = datetime.datetime.fromtimestamp(self.bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
        return self
        
class dashboard(object):
    def __init__(self,
                layout=None,
                tblData=None,
                tblMarket=None, 
                tblGold=None, 
                tblSupply=None, 
                tblMining=None, 
                tblBestBlock=None, 
                tblNetwork=None, 
                tblMetricEvents=None):
        self.layout=layout
    
    def generateLayout(self) -> Panel:        
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="market"),
            Layout(name="gold"),
            Layout(name="supply"),
            Layout(name="mining"),
            Layout(name="bestblock"),
            Layout(name="network"),
            Layout(name="metricevents")
            )
          
        self.layout["market"].size = 6
        self.layout["gold"].size = 5
        self.layout["supply"].size = 7
        self.layout["mining"].size = 5
        self.layout["bestblock"].size = 9
        self.layout["network"].size = 14
        self.layout["metricevents"].size = 20
        
        r = self.updateLayout()        
        return r
        
        
    def updateLayout(self) -> Panel:
        self.tblMarket, self.tblGold, self.tblSupply, self.tblMining, self.tblBestBlock, self.tblNetwork, self.tblMetricEvents = self.generateTable()
        
        self.layout["market"].update(self.tblMarket)
        self.layout["gold"].update(self.tblGold)
        self.layout["supply"].update(self.tblSupply)
        self.layout["mining"].update(self.tblMining)
        self.layout["bestblock"].update(self.tblBestBlock)
        self.layout["network"].update(self.tblNetwork)
        self.layout["metricevents"].update(self.tblMetricEvents)
        self = Panel(self.layout, title=PACKAGE_NAME, box=panelBox,  highlight=True, expand=False, subtitle=None, width=50, height=65) 
        return self 

    
    def generateTable(self) -> tuple[Table, Table, Table, Table, Table, Table, Table]:
        global PrevBTCPrice, PrevBlockHeight, q
        
        try:
            self = q.get()   # Grab from our queue, first in, first out method
        except q.Empty:
            pass   # We should never have an empty queue
    
        if PrevBTCPrice == None:
            PrevBTCPrice = self.BTCPrice      

        #Market
        self.tblMarket = Table(title_justify='left', title=' Market', show_header=False, width = tblwidth, show_footer=False, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblMarket.add_column("", style=colDescStyle)
        self.tblMarket.add_column("", justify='right', style=colValStyle)
        if int(round(self.BTCPrice)) > int(round(PrevBTCPrice)):
            self.tblMarket.add_row(
            Text(f"{'Price'}"),
            Text(f"${self.BTCPrice:,.0f}", style='dim bold green')
            )
        elif int(round(self.BTCPrice)) < int(round(PrevBTCPrice)):
            self.tblMarket.add_row(
            Text(f"{'Price'}"),
            Text(f"${self.BTCPrice:,.0f}", style='dim bold red')  
            )
        else:
            self.tblMarket.add_row(
            Text(f"{'Price'}"),
            Text(f"${self.BTCPrice:,.0f}", style=colValStyle)
            )
    
        PrevBTCPrice = self.BTCPrice
    
        self.tblMarket.add_row(
            Text(f"{'Sats per Dollar'}"),
            Text(f"{self.satusd:,.0f}"),
        )
        self.tblMarket.add_row(
            Text(f"{'Market Capitalization'}"),
            Text(f"${self.MarketCap:.1f}B")
        )
    
        #Gold
        self.tblGold = Table(title=' Gold', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblGold.add_column("", style=colDescStyle)
        self.tblGold.add_column("", justify='right', style=colValStyle)
        self.tblGold.add_row(
            Text(f"{'Bitcoin priced in Gold'}"),
            Text(f"{self.BTCPricedInGold:.1f} oz"),
        )
        self.tblGold.add_row(
            Text(f"{'Bitcoin vs. Gold Market Cap'}"),
            Text(f"{self.BTCvsGOLDMarketCap:.2f}%")
        )
    
        #Supply
        self.tblSupply = Table(title=' Supply', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblSupply.add_column("", style=colDescStyle)
        self.tblSupply.add_column("", justify='right', style=colValStyle)
        self.tblSupply.add_row(
            Text(f"{'Money Supply'}"),
            Text(f"{self.coinsMined:,.2f}"),
        )
        self.tblSupply.add_row(
            Text(f"{'Percentage Issued'}"),
            Text(f"{self.PctIssued:.2f}%"),
        )
        self.tblSupply.add_row(
            Text(f"{'Unspendable'}"),
            Text(f"{self.UNSPENDABLE:.2f}")
   
        )
        self.tblSupply.add_row(
            Text(f"{'Issuance Remaining'}"),
            Text(f"{self.IssuanceRemaining:,.2f}"),
        )
    
        # Mining Economics
        self.tblMining = Table(title=' Mining Economics', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblMining.add_column("", style=colDescStyle)
        self.tblMining.add_column("", justify='right', style=colValStyle)
        self.tblMining.add_row(
            Text(f"{'Block Subsidy'}"),
            Text(f"{self.BlockSubsidy:.2f} BTC"),
        )
        self.tblMining.add_row(
            Text(f"{'Subsidy value'}"),
            Text(f"${self.blockSubsidyValue:,.0f}")
        )
    
        #Best Block Summary
        self.tblBestBlock = Table(title=' Best Block Summary', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle) 
        self.tblBestBlock.add_column("", style=colDescStyle)
        self.tblBestBlock.add_column("", justify='right', style=colValStyle)
        if self.MAX_HEIGHT > PrevBlockHeight:  
            self.tblBestBlock.add_row(
                Text(f"{'Block Height'}"),
                Text(f"{self.MAX_HEIGHT:,.0f}", style='dim bold green'),
                )
        else:
            self.tblBestBlock.add_row(
               Text(f"{'Block Height'}"),
               Text(f"{self.MAX_HEIGHT:,.0f}", style=colValStyle),
               )
        PrevBlockHeight = self.MAX_HEIGHT
        self.tblBestBlock.add_row(
            Text(f"{'Chain size'}"),
            Text(f"{self.chainSize:.1f} GB"),
        )
        self.tblBestBlock.add_row(
            Text(f"{'nNonce'}"),
            Text(f"{self.bestNonce:.0f}"),
        )
        self.tblBestBlock.add_row(
            Text(f"{'Difficulty'}"),
            Text(f"{self.difficulty:.1f}×10\N{SUPERSCRIPT ONE}\N{SUPERSCRIPT TWO}"), 
        )
        self.tblBestBlock.add_row(
            Text(f"{'Target in nBits'}"),
            Text(f"{self.targetBits}"),
        )
        self.tblBestBlock.add_row(
            Text(f"{'Time'}"),
            Text(f"{self.BestBlockAge} ago")
        )
    
        #Network Summary
        self.tblNetwork = Table(title=' Network Summary', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle) 
        self.tblNetwork.add_column("", style=colDescStyle)
        self.tblNetwork.add_column("", justify='right', style=colValStyle)
        self.tblNetwork.add_row(
            Text(f"{'Connections'}"),
            Text(f"{self.Connections}"),
        )
        self.tblNetwork.add_row(
            Text(f"{'  Inbound'}"),
            Text(f"{self.ConnectionsIn}"),
        )
    
        self.tblNetwork.add_row(
            Text(f"{'Verification Progress'}"),
            Text(f"{self.verification:,.04f}%"),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, Epoch'}"),
            Text(f"{self.getNtwrkHashps:.1f} EH/s"),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, 7-day'}"),
            Text(f"{self.get7DNtwrkHashps:.1f} EH/s"),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, 4 weeks'}"),
            Text(f"{self.get4WNtwrkHashps:.1f} EH/s"),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, 1-day'}"),
            Text(f"{self.get1DNtwrkHashps:.1f} EH/s"),
        )
        self.tblNetwork.add_row(
            Text(f"{'Chain Work'}"),
            Text(f"{self.chainwork:.1f} bits"),
        )
        self.tblNetwork.add_row(
            Text(f"{'Total Transactions'}"),
            Text(f"{self.totalTXs:,.0f}"),
        )
        self.tblNetwork.add_row(
            Text(f"{'  Rate, 30 Days'}"),
            Text(f"{self.txRatePerSec:.1f} tx/s"),
        )
        self.tblNetwork.add_row(
            Text(f"{'  Count, 30 Days'}"),
            Text(f"{self.txCount:,.0f}")
        )
    
        #Metrics / Events
        self.tblMetricEvents = Table(title=' Metrics / Events', title_justify='left', show_header=False, show_footer=False, width = tblwidth, caption=COPYRIGHT, box=dashBox, 
                                highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle) 
        self.tblMetricEvents.add_column("", style=colDescStyle)
        self.tblMetricEvents.add_column("", justify='right', style=colValStyle)
        self.tblMetricEvents.add_row(
            Text(f"{'Difficulty Epoch'}"),
            Text(f"{self.diffEpoch:.0f}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'Block time, Prev Epoch'}"),
            Text(f"{self.avg_2016_blockTime}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'Block time, Diff. Epoch'}"),
            Text(f"{self.avgEpochBlockTime}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Blocks to Retarget'}"),
            Text(f"{self.epochBlocksRemain:,.0f}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Retarget Date'}"),
            Text(f"{self.RetargetDate}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Estimated Change'}"),
            Text(f"{self.estDiffChange:.01f}%"), 
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Retarget in nBits'}"),
            Text(f"{self.bnNew:.0f}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'Blocks to Halving'}"),
            Text(f"{self.nBlocksToHalving:,.0f}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Estimate Halving on'}"),
            Text(f"{self.halvingDate}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Subsidy Epoch'}"),
            Text(f"{self.subsidyEpoch}")  
        )
    
        return self.tblMarket, self.tblGold, self.tblSupply, self.tblMining, self.tblBestBlock, self.tblNetwork, self.tblMetricEvents 


__all__ = ('generateDataForTables'
           ,'dashboard'
)



