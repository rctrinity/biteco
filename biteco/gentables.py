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
from biteco import __version__
from biteco.util import GetAssetPrices, blockSubsidy, HALVING_BLOCKS, GIGABIT, GENESIS_REWARD, COIN, PACKAGE_NAME, EXAHASH, \
COPYRIGHT, TRILLION, CONVERT_TO_SATS, GOLD_OZ_ABOVE_GROUND, MAX_SUPPLY, BILLION, q

# Dashboard attributes
panelBox = box.SQUARE
dashBox = box.HORIZONTALS
tblBrdrStyle = 'dim bold deep_sky_blue1'
pnlBrdrStyle = 'white'
tblTtlStyle = 'white'
colDescStyle = 'bright_black'
colValStyle = 'bright_white'
colValPosChg = 'dim bold green'
colValNegChg = 'dim bold red'
tblwidth = 45

nTargetTimespan = 14 * 24 * 60 * 60                     
nTargetSpacing = 10 * 60                                
nSecsHour = 60 * 60                                     
nBlocksHour = (nSecsHour / nTargetSpacing)              
nInterval = nTargetTimespan / nTargetSpacing

PreviousSelf = None

def addToQueue():
    global q
    try:
        t = generateDataForTables()
        if t.proxy_error:
            pass
        else:
            q.put(t)
    
    except KeyboardInterrupt:
        raise

    except:
        sleep(5)
        try:
            t = generateDataForTables()
            if t.proxy_error:
                pass
            else:
                q.put(t)
            
        except:
            pass


# Determine value color based on if changes from previous. 
def ValueColor(current, previous):
    if current > previous:
        return colValPosChg
    elif current < previous:
        return colValNegChg
    else:
        return colValStyle 


class generateDataForTables(object):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
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
                 EpochHead = 0, 
                 bestBlockTimeUnix=0, 
                 bestBlockHeader = None,
                 total_fee = 0,
                 mempool_txs = 0,
                 mempool_minfee = 0,
                 mempool_bytes = 0,
                 pct_rbf = 0,
                 proxy_error = False): 
        
        global PreviousSelf
        self.proxy_error = proxy_error
        self.proxy=proxy
        if self.proxy == None:
            self.proxy=rpc.Proxy()
        
        try:    
            getAssetPrices = GetAssetPrices()
            
            # Proxy calls
            self.bestBlockHash = self.proxy.getbestblockhash()
            self.bestBlockHeader = self.proxy.getblockheader(self.bestBlockHash)
            currentInfo = self.proxy.call('gettxoutsetinfo', 'muhash')
            chainTxStats = self.proxy.call('getchaintxstats')  
            getBlockChainInfo = self.proxy.call('getblockchaininfo')
            getNetworkInfo = self.proxy.call('getnetworkinfo') 
            self.getNtwrkHashps = self.proxy.call('getnetworkhashps',-1)  / EXAHASH                    
            self.get7DNtwrkHashps = self.proxy.call('getnetworkhashps', int(nInterval) >> 1) / EXAHASH    
            self.get4WNtwrkHashps = self.proxy.call('getnetworkhashps', int(nInterval) << 1) / EXAHASH    
            self.get1DNtwrkHashps = self.proxy.call('getnetworkhashps', int(nInterval) // 14) / EXAHASH 
            mempoolinfo = self.proxy.call('getmempoolinfo')
            #rawmempool = self.proxy.getrawmempool(verbose=True)
            self.pct_rbf = pct_rbf
            #rbf = 0
            #for i in rawmempool:
            #    if rawmempool[i]['bip125-replaceable']:
            #        rbf +=1
            #self.pct_rbf = (rbf/len(rawmempool))*100
            
            self.Connections = getNetworkInfo['connections'] 
            self.ConnectionsIn = getNetworkInfo['connections_in']
            self.total_fee = float(mempoolinfo['total_fee'])
            self.mempool_minfee = mempoolinfo['mempoolminfee'] * COIN
            self.mempool_bytes = mempoolinfo['bytes']
            self.mempool_txs = mempoolinfo['size']
            self.bestNonce = self.bestBlockHeader.nNonce
            self.difficulty = self.bestBlockHeader.difficulty/TRILLION
            self.targetBits = self.bestBlockHeader.nBits
            self.bestBlockTimeUnix = time.mktime(datetime.datetime.utcfromtimestamp(self.bestBlockHeader.nTime).timetuple())
            self.coinsMined = float(currentInfo['total_amount'])
            self.UNSPENDABLE = float(currentInfo['total_unspendable_amount'])
            self.BTCPrice = getAssetPrices.Bitcoin_P
            if self.BTCPrice == None:
                self.BTCPrice = max(PreviousSelf.BTCPrice, 0)     # Work on this and Gold to show last good known price if waiting on server
            self.GLDPrice = getAssetPrices.Gold_P
            if self.GLDPrice == None:
                self.GLDPrice = max(PreviousSelf.GLDPrice, 0)
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
            self.diffEpoch = 1+(self.MAX_HEIGHT // nInterval)
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
        
        except:
            self.proxy_error = True 

    
    def marketCap(self) -> float:
        self = ((self.coinsMined + self.UNSPENDABLE) * self.BTCPrice) / BILLION
        return self

    
    def blocksToHalving(self) -> int:
        return int(HALVING_BLOCKS - (self.MAX_HEIGHT % HALVING_BLOCKS))
    
    
    def AvgBlockTimePrevEpoch(self) -> str:
        start_2016_block = int((self.MAX_HEIGHT - (self.MAX_HEIGHT % nInterval)) - nInterval)
        end_2016_block = int((self.MAX_HEIGHT - (self.MAX_HEIGHT % nInterval))-1)
        try:
            startBlockTime = self.proxy.getblockheader(self.proxy.getblockhash(start_2016_block))
            endBlockTime = self.proxy.getblockheader(self.proxy.getblockhash(end_2016_block)) 
            self = str(datetime.timedelta(seconds=(round( (endBlockTime.nTime - startBlockTime.nTime) / nInterval,0)))).lstrip("0:")
            return self
        except:
            self.proxy_error = True
            return '0:00' 
    

    def AvgBlockTimeEpoch(self) -> str:
        epochStartBlock = int(self.MAX_HEIGHT - (self.MAX_HEIGHT % nInterval))
    
        try:
            epochHead = self.proxy.getblockheader(self.proxy.getblockhash(epochStartBlock)) 
            return str(datetime.timedelta(seconds=(round( (self.bestBlockHeader.nTime - epochHead.nTime) / int(self.MAX_HEIGHT % nInterval),0)))).lstrip("0:"), epochHead
        except:
            self.proxy_error = True
            return '0:00', 0


    def bestBlockAge(self) -> str:
        self = str(datetime.timedelta(seconds=(round(time.mktime(datetime.datetime.utcnow().timetuple()) - self.bestBlockTimeUnix, 0)))).lstrip("0:")
        return self
    
    
    def Retarget(self) -> tuple[float, int, str, int]:
        nEpochTargetTimespan = int(( self.MAX_HEIGHT % nInterval ) * nTargetSpacing)
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
        blocksremain = int(nInterval - (self.MAX_HEIGHT % nInterval))
        secsToAdd = (blocksremain  / nBlocksHour) * nSecsHour
        retargetdate = datetime.datetime.fromtimestamp(self.bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
    
        return diffchange, blocksremain, retargetdate, bnnew
    
    
    def HalvingDate(self) -> str:
        secsToAdd = (self.nBlocksToHalving / nBlocksHour) * nSecsHour
        self = datetime.datetime.fromtimestamp(self.bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
        return self

        
class dashboard(object):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __init__(self,
                layout=None,
                tblData=None,
                tblMarket=None, 
                tblGold=None, 
                tblSupply=None, 
                tblMining=None, 
                tblBestBlock=None, 
                tblNetwork=None, 
                tblMetricEvents=None,
                tblMempoolInfo=None):
        self.layout=layout
    
    
    def generateLayout(self) -> Panel:        
        self.layout = Layout()
        
        self.layout.split_row(
            Layout(name='left'),
            Layout(name='right')
            )
        self.layout['left'].split_column(
            Layout(name="market"),
            Layout(name="gold"),
            Layout(name="supply"),
            Layout(name="mining"),
            Layout(name="metricevents")
            )
        self.layout['right'].split_column(
            Layout(name="bestblock"),
            Layout(name="network"),
            Layout(name='mempoolinfo')
            )
        
        self.layout['left']["market"].size = 6
        self.layout['left']["gold"].size = 5
        self.layout['left']["supply"].size = 7
        self.layout['left']["mining"].size = 5
        self.layout['right']["bestblock"].size = 9
        self.layout['right']["network"].size = 14
        self.layout['left']["metricevents"].size = 17
        self.layout['right']["mempoolinfo"].size = 10
        
        r = self.updateLayout()        
        return r
        
        
    def updateLayout(self) -> Panel:
        addToQueue()
        self.tblMarket, self.tblGold, self.tblSupply, self.tblMining, self.tblBestBlock, self.tblNetwork, self.tblMetricEvents, self.tblMempoolInfo = self.generateTable()
        
        self.layout["left"]["market"].update(self.tblMarket)
        self.layout["left"]["gold"].update(self.tblGold)
        self.layout["left"]["supply"].update(self.tblSupply)
        self.layout["left"]["mining"].update(self.tblMining)
        self.layout["right"]["bestblock"].update(self.tblBestBlock)
        self.layout["right"]["network"].update(self.tblNetwork)
        self.layout["left"]["metricevents"].update(self.tblMetricEvents)
        self.layout["right"]["mempoolinfo"].update(self.tblMempoolInfo)
        self = Panel(self.layout, title=PACKAGE_NAME, box=panelBox,  highlight=True, expand=False, subtitle='v'+__version__, style=pnlBrdrStyle, width=96, height=40, padding=(1,1)) 
        return self 

    
    def generateTable(self) -> tuple[Table, Table, Table, Table, Table, Table, Table, Table]:
        global q, PreviousSelf
    
        if not q.empty():
            self = q.get()   # Grab from our queue, first in, first out method
        else:
            while not q.full():
                addToQueue()   
            self = q.get()

        if PreviousSelf == None:
            PreviousSelf = self      

        #Market
        self.tblMarket = Table(title_justify='left', title=' Market', show_header=False, width = tblwidth, show_footer=False, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblMarket.add_column("", style=colDescStyle)
        self.tblMarket.add_column("", justify='right', style=colValStyle)
    
        self.tblMarket.add_row(
            Text(f"{'Price'}"),
            Text(f"${self.BTCPrice:,.0f}", style=ValueColor(round(self.BTCPrice), round(PreviousSelf.BTCPrice)))
        )
                
        self.tblMarket.add_row(
            Text(f"{'Sats per Dollar'}"),
            Text(f"{self.satusd:,.0f}", style=ValueColor(round(self.satusd), round(PreviousSelf.satusd))),
        )
        self.tblMarket.add_row(
            Text(f"{'Market Capitalization'}"),
            Text(f"${self.MarketCap:.1f}B", style=ValueColor(round(self.MarketCap,1), round(PreviousSelf.MarketCap,1)))
        )

        #Gold
        self.tblGold = Table(title=' Gold', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblGold.add_column("", style=colDescStyle)
        self.tblGold.add_column("", justify='right', style=colValStyle)
        self.tblGold.add_row(
            Text(f"{'Bitcoin priced in Gold'}"),
            Text(f"{self.BTCPricedInGold:.1f} oz", style=ValueColor(round(self.BTCPricedInGold,1), round(PreviousSelf.BTCPricedInGold,1))),
        )
        self.tblGold.add_row(
            Text(f"{'Bitcoin vs. Gold Market Cap'}"),
            Text(f"{self.BTCvsGOLDMarketCap:.2f}%", style=ValueColor(round(self.BTCvsGOLDMarketCap,2), round(PreviousSelf.BTCvsGOLDMarketCap,2)))
        )

        #Supply
        self.tblSupply = Table(title=' Supply', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblSupply.add_column("", style=colDescStyle)
        self.tblSupply.add_column("", justify='right', style=colValStyle)
        self.tblSupply.add_row(
            Text(f"{'Money Supply'}"),
            Text(f"{self.coinsMined:,.2f}", style=ValueColor(round(self.coinsMined,2), round(PreviousSelf.coinsMined,2))),
        )
        self.tblSupply.add_row(
            Text(f"{'Percentage Issued'}"),
            Text(f"{self.PctIssued:.2f}%", style=ValueColor(round(self.PctIssued,2), round(PreviousSelf.PctIssued,2))),
        )
        self.tblSupply.add_row(
            Text(f"{'Unspendable'}"),
            Text(f"{self.UNSPENDABLE:.2f}", style=ValueColor(round(self.UNSPENDABLE,2), round(PreviousSelf.UNSPENDABLE,2)))

        )
        self.tblSupply.add_row(
            Text(f"{'Issuance Remaining'}"),
            Text(f"{self.IssuanceRemaining:,.2f}", style=ValueColor(round(self.IssuanceRemaining,2), round(PreviousSelf.IssuanceRemaining,2))),
        )

        # Mining Economics
        self.tblMining = Table(title=' Mining Economics', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle)  
        self.tblMining.add_column("", style=colDescStyle)
        self.tblMining.add_column("", justify='right', style=colValStyle)
        self.tblMining.add_row(
            Text(f"{'Block Subsidy'}"),
            Text(f"{self.BlockSubsidy:.2f} BTC", style=ValueColor(round(self.BlockSubsidy,2), round(PreviousSelf.BlockSubsidy,2))),
        )
        self.tblMining.add_row(
            Text(f"{'Subsidy value'}"),
            Text(f"${self.blockSubsidyValue:,.0f}", style=ValueColor(round(self.blockSubsidyValue), round(PreviousSelf.blockSubsidyValue)))
        )

        #Best Block Summary
        self.tblBestBlock = Table(title=' Best Block Summary', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle) 
        self.tblBestBlock.add_column("", style=colDescStyle)
        self.tblBestBlock.add_column("", justify='right', style=colValStyle)
        self.tblBestBlock.add_row(
            Text(f"{'Block Height'}"),
            Text(f"{self.MAX_HEIGHT:,.0f}", style=ValueColor(self.MAX_HEIGHT, PreviousSelf.MAX_HEIGHT)),
        )
    
        self.tblBestBlock.add_row(
            Text(f"{'Chain size'}"),
            Text(f"{self.chainSize:.1f} GB", style=ValueColor(round(self.chainSize,1), round(PreviousSelf.chainSize,1))),
        )
        self.tblBestBlock.add_row(
            Text(f"{'nNonce'}"),
            Text(f"{self.bestNonce:.0f}"),
        )
        self.tblBestBlock.add_row(
            Text(f"{'Difficulty'}"),
            Text(f"{self.difficulty:.1f}×10\N{SUPERSCRIPT ONE}\N{SUPERSCRIPT TWO}", style=ValueColor(round(self.difficulty,1), round(PreviousSelf.difficulty,1))), 
        )
        self.tblBestBlock.add_row(
            Text(f"{'Target in nBits'}"),
            Text(f"{self.targetBits}", style=ValueColor(self.targetBits, PreviousSelf.targetBits)),
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
            Text(f"{self.Connections}", style=ValueColor(self.Connections, PreviousSelf.Connections)),
        )
        self.tblNetwork.add_row(
            Text(f"{'  Inbound'}"),
            Text(f"{self.ConnectionsIn}", style=ValueColor(self.ConnectionsIn, PreviousSelf.ConnectionsIn)),
        )

        self.tblNetwork.add_row(
            Text(f"{'Verification Progress'}"),
            Text(f"{self.verification:,.04f}%", style=ValueColor(round(self.verification,4), round(PreviousSelf.verification,4))),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, Epoch'}"),
            Text(f"{self.getNtwrkHashps:.1f} EH/s", style=ValueColor(self.getNtwrkHashps, PreviousSelf.getNtwrkHashps)),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, 7-day'}"),
            Text(f"{self.get7DNtwrkHashps:.1f} EH/s", style=ValueColor(self.get7DNtwrkHashps, PreviousSelf.get7DNtwrkHashps)),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, 4 weeks'}"),
            Text(f"{self.get4WNtwrkHashps:.1f} EH/s", style=ValueColor(self.get4WNtwrkHashps, PreviousSelf.get4WNtwrkHashps)),
        )
        self.tblNetwork.add_row(
            Text(f"{'Hash Rate, 1-day'}"),
            Text(f"{self.get1DNtwrkHashps:.1f} EH/s", style=ValueColor(self.get1DNtwrkHashps, PreviousSelf.get1DNtwrkHashps)),
        )
        self.tblNetwork.add_row(
            Text(f"{'Chain Work'}"),
            Text(f"{self.chainwork:.1f} bits", style=ValueColor(round(self.chainwork,1), round(PreviousSelf.chainwork,1))),
        )
        self.tblNetwork.add_row(
            Text(f"{'Total Transactions'}"),
            Text(f"{self.totalTXs:,.0f}", style=ValueColor(self.totalTXs, PreviousSelf.totalTXs)),
        )
        self.tblNetwork.add_row(
            Text(f"{'  Rate, 30 Days'}"),
            Text(f"{self.txRatePerSec:.1f} tx/s", style=ValueColor(self.txRatePerSec, PreviousSelf.txRatePerSec)),
        )
        self.tblNetwork.add_row(
            Text(f"{'  Count, 30 Days'}"),
            Text(f"{self.txCount:,.0f}", style=ValueColor(self.txCount, PreviousSelf.txCount))
        )

        #Metrics / Events
        self.tblMetricEvents = Table(title=' Metrics / Events', title_justify='left', show_header=False, show_footer=False, width = tblwidth,  box=dashBox, 
                                highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle) 
        self.tblMetricEvents.add_column("", style=colDescStyle)
        self.tblMetricEvents.add_column("", justify='right', style=colValStyle)
        self.tblMetricEvents.add_row(
            Text(f"{'Difficulty Epoch'}"),
            Text(f"{self.diffEpoch:.0f}", style=ValueColor(self.diffEpoch, PreviousSelf.diffEpoch)),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'Block time, Prev Epoch'}"),
            Text(f"{self.avg_2016_blockTime}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'Block time, Diff. Epoch'}"),
            Text(f"{self.avgEpochBlockTime}", style=ValueColor(self.avgEpochBlockTime, PreviousSelf.avgEpochBlockTime)),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Blocks to Retarget'}"),
            Text(f"{self.epochBlocksRemain:,.0f}", style=ValueColor(self.epochBlocksRemain, PreviousSelf.epochBlocksRemain)),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Retarget Date'}"),
            Text(f"{self.RetargetDate}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Estimated Change'}"),
            Text(f"{self.estDiffChange:.01f}%", style=ValueColor(round(self.estDiffChange,1), round(PreviousSelf.estDiffChange,1))), 
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Retarget in nBits'}"),
            Text(f"{self.bnNew:.0f}", style=ValueColor(round(self.bnNew), round(PreviousSelf.bnNew))),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'Blocks to Halving'}"),
            Text(f"{self.nBlocksToHalving:,.0f}", style=ValueColor(self.nBlocksToHalving, PreviousSelf.nBlocksToHalving)),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Estimate Halving on'}"),
            Text(f"{self.halvingDate}"),
        )
        self.tblMetricEvents.add_row(
            Text(f"{'  Subsidy Epoch'}"),
            Text(f"{self.subsidyEpoch}", style=ValueColor(self.subsidyEpoch, PreviousSelf.subsidyEpoch))  
        )
    
        #MempoolInfo
        self.tblMempoolInfo = Table(title=' Mempool Info', title_justify='left', show_header=False, show_footer=False, width = tblwidth, box=dashBox, 
                                highlight=True, border_style=tblBrdrStyle, style=tblTtlStyle) 
        self.tblMempoolInfo.add_column("", style=colDescStyle)
        self.tblMempoolInfo.add_column("", justify='right', style=colValStyle)
        self.tblMempoolInfo.add_row(
            Text(f"{'Transactions'}"),
            Text(f"{self.mempool_txs:,.0f}", style=ValueColor(self.mempool_txs, PreviousSelf.mempool_txs)),
        )
    
        self.tblMempoolInfo.add_row(
            Text(f"{'Total Fee'}"),
            Text(f"{self.total_fee:.2f} BTC", style=ValueColor(round(self.total_fee,2), round(PreviousSelf.total_fee,2))),
            )
        self.tblMempoolInfo.add_row(
            Text(f"{'Total Fee value'}"),
            Text(f"${self.total_fee*self.BTCPrice:,.0f}", style=ValueColor(round((self.total_fee*self.BTCPrice),0), round((PreviousSelf.total_fee*PreviousSelf.BTCPrice),0))),
            )

        self.tblMempoolInfo.add_row(
            Text(f"{'Minimum Fee, sats/KB'}"),
            Text(f"{self.mempool_minfee:,.0f}", style=ValueColor(self.mempool_minfee, PreviousSelf.mempool_minfee))
            )
        self.tblMempoolInfo.add_row(
            Text(f"{'Size in bytes'}"),
            Text(f"{self.mempool_bytes/1000000:,.1f} MB", style=ValueColor(round((self.mempool_bytes/1000000),1), round((PreviousSelf.mempool_bytes/1000000),1)))
            )
        self.tblMempoolInfo.add_row(
            Text(f"{'Blocks to Clear'}"),
            Text(f"{1+((self.mempool_bytes/1000000)//1):,.0f}", style=ValueColor(round((1+((self.mempool_bytes/1000000)//1)),0), round((1+((PreviousSelf.mempool_bytes/1000000)//1)),1)))
            )
        self.tblMempoolInfo.add_row(
            Text(f"{'Percent RBF (Disabled)'}"),
            Text(f"{self.pct_rbf:.1f}%", style=ValueColor(round(self.pct_rbf,1), round(PreviousSelf.pct_rbf,1)))
            )
    

        PreviousSelf = self

        return self.tblMarket, self.tblGold, self.tblSupply, self.tblMining, self.tblBestBlock, self.tblNetwork, self.tblMetricEvents, self.tblMempoolInfo 


__all__ = ('generateDataForTables'
           ,'dashboard'
)










