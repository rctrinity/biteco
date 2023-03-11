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
from util import GetAssetPrices, PrevBTCPrice, blockSubsidy, HALVING_BLOCKS, GIGABIT, GENESIS_REWARD, COIN, PACKAGE_NAME, EXAHASH, COPYRIGHT, TRILLION, CONVERT_TO_SATS, GOLD_OZ_ABOVE_GROUND, MAX_SUPPLY, BILLION


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
                 
         getAssetPrices = GetAssetPrices()
        self.nTargetTimespan = 14 * 24 * 60 * 60                     
        self.nTargetSpacing = 10 * 60                                
        self.nSecsHour = 60 * 60                                     
        self.nBlocksHour = (self.nSecsHour / self.nTargetSpacing)              
        self.nInterval = self.nTargetTimespan / self.nTargetSpacing
        # Proxy calls
        self.proxy=rpc.Proxy()
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
        return ((self.coinsMined + self.UNSPENDABLE) * self.BTCPrice) / BILLION
    
    def blocksToHalving(self) -> int:
        return int(HALVING_BLOCKS - (self.MAX_HEIGHT % HALVING_BLOCKS))
        
    def AvgBlockTimePrevEpoch(self) -> str:
        start_2016_block = int((self.MAX_HEIGHT - (self.MAX_HEIGHT % self.nInterval)) - self.nInterval)
        end_2016_block = int((self.MAX_HEIGHT - (self.MAX_HEIGHT % self.nInterval))-1)
        startBlockTime = self.proxy.getblockheader(self.proxy.getblockhash(start_2016_block))
        endBlockTime = self.proxy.getblockheader(self.proxy.getblockhash(end_2016_block)) 
        
        return str(datetime.timedelta(seconds=(round( (endBlockTime.nTime - startBlockTime.nTime) / self.nInterval,0)))).lstrip("0:")
        
    
    def AvgBlockTimeEpoch(self) -> str:
        epochStartBlock = int(self.MAX_HEIGHT - (self.MAX_HEIGHT % self.nInterval))
        epochHead = self.proxy.getblockheader(self.proxy.getblockhash(epochStartBlock))  
        
        return str(datetime.timedelta(seconds=(round( (self.bestBlockHeader.nTime - epochHead.nTime) / int(self.MAX_HEIGHT % self.nInterval),0)))).lstrip("0:"), epochHead
    
    
    def bestBlockAge(self) -> str:
        r = str(datetime.timedelta(seconds=(round(time.mktime(datetime.datetime.utcnow().timetuple()) - self.bestBlockTimeUnix, 0)))).lstrip("0:")
        return r
        
    def Retarget(self):
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
        
        return datetime.datetime.fromtimestamp(self.bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
        

    
def generateLayout() -> Panel:
    tblMarket, tblGold, tblSupply, tblMining, tblBestBlock, tblNetwork, tblMetricEvents = generateTable()
    layout = Layout()
    layout.split_column(
        Layout(name="market"),
        Layout(name="gold"),
        Layout(name="supply"),
        Layout(name="mining"),
        Layout(name="bestblock"),
        Layout(name="network"),
        Layout(name="metricevents")
    )
    layout["market"].update(tblMarket)
    layout["gold"].update(tblGold)
    layout["supply"].update(tblSupply)
    layout["mining"].update(tblMining)
    layout["bestblock"].update(tblBestBlock)
    layout["network"].update(tblNetwork)
    layout["metricevents"].update(tblMetricEvents)
    
    layout["market"].size = 6
    layout["gold"].size = 5
    layout["supply"].size = 7
    layout["mining"].size = 5
    layout["bestblock"].size = 9
    layout["network"].size = 14
    layout["metricevents"].size = 20
    
    return Panel(layout, title=PACKAGE_NAME, box=box.SIMPLE,  expand=False, subtitle=None, width=50, height=65, border_style='white')  


def generateTable() -> Table:
    global PrevBTCPrice
    
    tblData = generateDataForTables()   
    
    if PrevBTCPrice == None:
        PrevBTCPrice = tblData.BTCPrice      
    

    #Market
    tblMarket = Table(title_justify='left', title=' Market', show_header=False, min_width = 45, show_footer=False, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblMarket.add_column("", style='bright_black')
    tblMarket.add_column("", justify='right', style='bright_white')
    if int(round(tblData.BTCPrice)) > int(round(PrevBTCPrice)):
        tblMarket.add_row(
        Text(f"{'Price'}"),
        Text(f"${tblData.BTCPrice:,.0f}", style='dim bold green')
        )
    elif int(round(tblData.BTCPrice)) < int(round(PrevBTCPrice)):
        tblMarket.add_row(
        Text(f"{'Price'}"),
        Text(f"${tblData.BTCPrice:,.0f}", style='dim bold red')  
        )
    else:
        tblMarket.add_row(
        Text(f"{'Price'}"),
        Text(f"${tblData.BTCPrice:,.0f}", style='bright_white')
        )
    
    PrevBTCPrice = tblData.BTCPrice
    
    tblMarket.add_row(
        Text(f"{'Sats per Dollar'}"),
        Text(f"{tblData.satusd:,.0f}"),
    )
    tblMarket.add_row(
        Text(f"{'Market Capitalization'}"),
        Text(f"${tblData.MarketCap:.1f}B")
    )
    
    #Gold
    tblGold = Table(title=' Gold', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblGold.add_column("", style='bright_black')
    tblGold.add_column("", justify='right', style='bright_white')
    tblGold.add_row(
        Text(f"{'Bitcoin priced in Gold'}"),
        Text(f"{tblData.BTCPricedInGold:.1f} oz"),
    )
    tblGold.add_row(
        Text(f"{'Bitcoin vs. Gold Market Cap'}"),
        Text(f"{tblData.BTCvsGOLDMarketCap:.2f}%")
    )
    #Supply
    tblSupply = Table(title=' Supply', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblSupply.add_column("", style='bright_black')
    tblSupply.add_column("", justify='right', style='bright_white')
    tblSupply.add_row(
        Text(f"{'Money Supply'}"),
        Text(f"{tblData.coinsMined:,.2f}"),
    )
    tblSupply.add_row(
        Text(f"{'Percentage Issued'}"),
        Text(f"{tblData.PctIssued:.2f}%"),
    )
    tblSupply.add_row(
        Text(f"{'Unspendable'}"),
        Text(f"{tblData.UNSPENDABLE:.2f}")
   
    )
    tblSupply.add_row(
        Text(f"{'Issuance Remaining'}"),
        Text(f"{tblData.IssuanceRemaining:,.2f}"),
    )
    
    # Mining Economics
    tblMining = Table(title=' Mining Economics', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblMining.add_column("", style='bright_black')
    tblMining.add_column("", justify='right', style='bright_white')
    tblMining.add_row(
        Text(f"{'Block Subsidy'}"),
        Text(f"{tblData.BlockSubsidy:.2f} BTC"),
    )
    tblMining.add_row(
        Text(f"{'Subsidy value'}"),
        Text(f"${tblData.blockSubsidyValue:,.0f}")
    )
    
    #Best Block Summary
    tblBestBlock = Table(title=' Best Block Summary', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblBestBlock.add_column("", style='bright_black')
    tblBestBlock.add_column("", justify='right', style='bright_white')
    tblBestBlock.add_row(
        Text(f"{'Block Height'}"),
        Text(f"{tblData.MAX_HEIGHT:,.0f}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Chain size'}"),
        Text(f"{tblData.chainSize:.1f} GB"),
    )
    tblBestBlock.add_row(
        Text(f"{'nNonce'}"),
        Text(f"{tblData.bestNonce:.0f}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Difficulty'}"),
        Text(f"{tblData.difficulty:.1f}×10\N{SUPERSCRIPT ONE}\N{SUPERSCRIPT TWO}"), 
    )
    tblBestBlock.add_row(
        Text(f"{'Target in nBits'}"),
        Text(f"{tblData.targetBits}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Time'}"),
        Text(f"{tblData.BestBlockAge} ago")
    )
    
    #Network Summary
    tblNetwork = Table(title=' Network Summary', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblNetwork.add_column("", style='bright_black')
    tblNetwork.add_column("", justify='right', style='bright_white')
    tblNetwork.add_row(
        Text(f"{'Connections'}"),
        Text(f"{tblData.Connections}"),
    )
    tblNetwork.add_row(
        Text(f"{'  Inbound'}"),
        Text(f"{tblData.ConnectionsIn}"),
    )
    
    tblNetwork.add_row(
        Text(f"{'Verification Progress'}"),
        Text(f"{tblData.verification:,.04f}%"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, Epoch'}"),
        Text(f"{tblData.getNtwrkHashps:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, 7-day'}"),
        Text(f"{tblData.get7DNtwrkHashps:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, 4 weeks'}"),
        Text(f"{tblData.get4WNtwrkHashps:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, 1-day'}"),
        Text(f"{tblData.get1DNtwrkHashps:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Chain Work'}"),
        Text(f"{tblData.chainwork:.1f} bits"),
    )
    tblNetwork.add_row(
        Text(f"{'Total Transactions'}"),
        Text(f"{tblData.totalTXs:,.0f}"),
    )
    tblNetwork.add_row(
        Text(f"{'  Rate, 30 Days'}"),
        Text(f"{tblData.txRatePerSec:.1f} tx/s"),
    )
    tblNetwork.add_row(
        Text(f"{'  Count, 30 Days'}"),
        Text(f"{tblData.txCount:,.0f}")
    )
    
    #Metrics / Events
    tblMetricEvents = Table(title=' Metrics / Events', title_justify='left', show_header=False, show_footer=False, min_width = 45, caption=COPYRIGHT, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') # 
    tblMetricEvents.add_column("", style='bright_black')
    tblMetricEvents.add_column("", justify='right', style='bright_white')
    tblMetricEvents.add_row(
        Text(f"{'Difficulty Epoch'}"),
        Text(f"{tblData.diffEpoch:.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'Block time, Prev Epoch'}"),
        Text(f"{tblData.avg_2016_blockTime}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'Block time, Diff. Epoch'}"),
        Text(f"{tblData.avgEpochBlockTime}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Blocks to Retarget'}"),
        Text(f"{tblData.epochBlocksRemain:,.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Retarget Date'}"),
        Text(f"{tblData.RetargetDate}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Estimated Change'}"),
        Text(f"{tblData.estDiffChange:.01f}%"), 
    )
    tblMetricEvents.add_row(
        Text(f"{'  Retarget in nBits'}"),
        Text(f"{tblData.bnNew:.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'Blocks to Halving'}"),
        Text(f"{tblData.nBlocksToHalving:,.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Estimate Halving on'}"),
        Text(f"{tblData.halvingDate}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Subsidy Epoch'}"),
        Text(f"{tblData.subsidyEpoch}")  
    )
    
    return tblMarket, tblGold, tblSupply, tblMining, tblBestBlock, tblNetwork, tblMetricEvents 

