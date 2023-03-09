# Generate tables for termonal dashboard
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
from util import GetAssetPrices, BlockSubsidy, marketCapitalization, PrevBTCPrice, HALVING_BLOCKS, GIGABIT, GENESIS_REWARD, COIN, PACKAGE_NAME, EXAHASH, COPYRIGHT, TRILLION

INITIALIZE = False

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
    
    return Panel(layout, title=PACKAGE_NAME, box=box.SIMPLE,  expand=False, subtitle=None, width=50, height=65)

def generateTable() -> Table:
    # Initialize variables ###############################################################################
    global PrevBTCPrice, INITIALIZE
    nTargetTimespan = 14 * 24 * 60 * 60                     # two weeks - 1,209,600
    nTargetSpacing = 10 * 60                                # 1 Hour 600
    nSecsHour = 60 * 60                                     # 3600 
    nBlocksHour = (nSecsHour / nTargetSpacing)              # 6 blocks
    nInterval = nTargetTimespan / nTargetSpacing            # 2,016 blocks
    if PrevBTCPrice == None:
        PrevBTCPrice = 0      
    
    if not INITIALIZE:
        brk = 0.1
        INITIALIZE = True
    else:
        brk = 0.2
    
    proxy = rpc.Proxy()
    # End initialization #################################################################################

    
    # Collect tx metrics #################################################################################
    currentInfo = proxy.call('gettxoutsetinfo', 'muhash')  
    sleep(brk)
    UNSPENDABLE = float(currentInfo['total_unspendable_amount'])
    coinsMined = float(currentInfo['total_amount'])                # Excludes unspendable
    totalTXs = currentInfo['txouts']    
    chainTxStats = proxy.call('getchaintxstats')   
    sleep(brk)
    totalTXs = chainTxStats['txcount']
    # Last 30 days
    txRatePerSec = chainTxStats['txrate']
    txCount = chainTxStats['window_tx_count']
    # End tx metrics #####################################################################################
    
    
    # Collect chain / network info / Market Cap ##########################################################
    getBlockChainInfo = proxy.call('getblockchaininfo')   
    sleep(brk)
    chainSize = getBlockChainInfo['size_on_disk'] / GIGABIT
    MAX_HEIGHT = getBlockChainInfo['blocks']
    satusd, blockSubsidyValue, MarketCap, BTCvsGOLDMarketCap, BTCPricedInGold, PctIssued, IssuanceRemaining, BTCPrice = marketCapitalization(coinsMined, BlockSubsidy(MAX_HEIGHT), UNSPENDABLE)
    if PrevBTCPrice == 0 and BTCPrice != 0:
        PrevBTCPrice = BTCPrice     
    getNetworkInfo = proxy.call('getnetworkinfo')  
    sleep(brk)
    bestBlockHeader = proxy.getblockheader(proxy.getbestblockhash())
    sleep(brk)
    bestBlockTimeUnix = time.mktime(datetime.datetime.utcfromtimestamp(bestBlockHeader.nTime).timetuple())
    bestBlockAge = str(datetime.timedelta(seconds=(round(time.mktime(datetime.datetime.utcnow().timetuple()) - bestBlockTimeUnix, 0)))).lstrip("0:")
    # End chain / network info ###########################################################################
    
    
    # Epoch and rolling 2016 block calculations ##########################################################
    # Calculate average block time for past rolling 2016 blocks
    start_2016_block = int(1 + (MAX_HEIGHT - nInterval))
    blockHead = proxy.getblockheader(proxy.getblockhash(start_2016_block))   
    sleep(brk)
    avg_2016_blockTime = str(datetime.timedelta(seconds=(round( (bestBlockTimeUnix - blockHead.nTime) / nInterval,0)))).lstrip("0:")

    # Calculate average block time in current diff. epoch
    epochStartBlock = int(MAX_HEIGHT - (MAX_HEIGHT % nInterval))
    epochHead = proxy.getblockheader(proxy.getblockhash(epochStartBlock))   
    sleep(brk)
    avgEpochBlockTime = str(datetime.timedelta(seconds=(round( (bestBlockHeader.nTime - epochHead.nTime) / int(MAX_HEIGHT % nInterval),0)))).lstrip("0:")
     # End epoch / 2016 calculations ######################################################################
     

    # Estimate retarget change pct. #######################################################################
    nEpochTargetTimespan = int(( MAX_HEIGHT % nInterval ) * nTargetSpacing)
    nEpochActualTimespan = int(bestBlockHeader.nTime - epochHead.nTime)

    if (nEpochActualTimespan < nEpochTargetTimespan/4):
        nEpochActualTimespan = nEpochTargetTimespan/4
    if (nEpochActualTimespan > nEpochTargetTimespan*4):
        nEpochActualTimespan = nEpochTargetTimespan*4
    
    bnNew = uint256_from_compact(bestBlockHeader.nBits)
    bnNew *= nEpochActualTimespan
    bnNew //= nEpochTargetTimespan
    bnNew = compact_from_uint256(bnNew)
     
    estDiffChange = (1-(nEpochActualTimespan / nEpochTargetTimespan)) * 100
    epochBlocksRemain = int(nInterval - (MAX_HEIGHT % nInterval))
    secsToAdd = (epochBlocksRemain  / nBlocksHour) * nSecsHour
    RetargetDate = datetime.datetime.fromtimestamp(bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
    # End retarget estimations ############################################################################
    
    
    # Calculate halving event #############################################################################
    nBlocksToHalving = int(HALVING_BLOCKS - (MAX_HEIGHT % HALVING_BLOCKS))
    secsToAdd = (nBlocksToHalving / nBlocksHour) * nSecsHour
    halvingDate = datetime.datetime.fromtimestamp(bestBlockTimeUnix + secsToAdd).strftime('%B %d, %Y')
    # End halving calculation #############################################################################
    
    
    # Collext hash rates, different intervals #############################################################
    getNtwrkHashps = proxy.call('getnetworkhashps',-1)                      # Since last retarget
    sleep(brk)
    get7DNtwrkHashps = proxy.call('getnetworkhashps', int(nInterval) >> 1)  # 1 Week
    sleep(brk)
    get4WNtwrkHashps = proxy.call('getnetworkhashps', int(nInterval) << 1)  # 4 weeks
    sleep(brk)
    get1DNtwrkHashps = proxy.call('getnetworkhashps', int(nInterval) // 14) # 1 day
    sleep(brk)
    # End hash rate collection ############################################################################
              
    
    ####### Table creation below ##########################################################################
    #Market
    tblMarket = Table(title_justify='left', title=' Market', show_header=False, min_width = 45, show_footer=False, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblMarket.add_column("", style='bright_black')
    tblMarket.add_column("", justify='right', style='bright_white')
    if int(round(BTCPrice)) > int(round(PrevBTCPrice)):
        tblMarket.add_row(
        Text(f"{'Price'}"),
        Text(f"${BTCPrice:,.0f}", style='dim bold green'),
        )
    elif int(round(BTCPrice)) < int(round(PrevBTCPrice)):
        tblMarket.add_row(
        Text(f"{'Price'}"),
        Text(f"${BTCPrice:,.0f}", style='dim bold red')
        )
    else:
        tblMarket.add_row(
        Text(f"{'Price'}"),
        Text(f"${BTCPrice:,.0f}", style='bright_white')
        )
    
    PrevBTCPrice = BTCPrice
    
    tblMarket.add_row(
        Text(f"{'Sats per Dollar'}"),
        Text(f"{satusd:,.0f}"),
    )
    tblMarket.add_row(
        Text(f"{'Market Capitalization'}"),
        Text(f"${MarketCap:.1f}B")
    )
    #Gold
    tblGold = Table(title=' Gold', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblGold.add_column("", style='bright_black')
    tblGold.add_column("", justify='right', style='bright_white')
    tblGold.add_row(
        Text(f"{'Bitcoin priced in Gold'}"),
        Text(f"{BTCPricedInGold:.1f} oz"),
    )
    tblGold.add_row(
        Text(f"{'Bitcoin vs. Gold Market Cap'}"),
        Text(f"{BTCvsGOLDMarketCap:.2f}%")
    )
    #Supply
    tblSupply = Table(title=' Supply', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblSupply.add_column("", style='bright_black')
    tblSupply.add_column("", justify='right', style='bright_white')
    tblSupply.add_row(
        Text(f"{'Money Supply'}"),
        Text(f"{coinsMined:,.2f}"),
    )
    tblSupply.add_row(
        Text(f"{'Percentage Issued'}"),
        Text(f"{PctIssued:.2f}%"),
    )
    tblSupply.add_row(
        Text(f"{'Issuance Remaining'}"),
        Text(f"{IssuanceRemaining:,.2f}"),
    )
    tblSupply.add_row(
        Text(f"{'Unspendable'}"),
        Text(f"{UNSPENDABLE:.2f}")
    )
    # Mining Economics
    tblMining = Table(title=' Mining Economics', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblMining.add_column("", style='bright_black')
    tblMining.add_column("", justify='right', style='bright_white')
    tblMining.add_row(
        Text(f"{'Block Subsidy'}"),
        Text(f"{BlockSubsidy(MAX_HEIGHT):.2f} BTC"),
    )
    tblMining.add_row(
        Text(f"{'Subsidy value'}"),
        Text(f"${blockSubsidyValue:,.0f}")
    )
    #Best Block Summary
    tblBestBlock = Table(title=' Best Block Summary', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblBestBlock.add_column("", style='bright_black')
    tblBestBlock.add_column("", justify='right', style='bright_white')
    tblBestBlock.add_row(
        Text(f"{'Block Height'}"),
        Text(f"{MAX_HEIGHT:,.0f}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Chain size'}"),
        Text(f"{chainSize:.1f} GB"),
    )
    tblBestBlock.add_row(
        Text(f"{'nNonce'}"),
        Text(f"{bestBlockHeader.nNonce:.0f}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Difficulty'}"),
        Text(f"{bestBlockHeader.difficulty/TRILLION:.1f}×10\N{SUPERSCRIPT ONE}\N{SUPERSCRIPT TWO}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Target in nBits'}"),
        Text(f"{bestBlockHeader.nBits}"),
    )
    tblBestBlock.add_row(
        Text(f"{'Time'}"),
        Text(f"{bestBlockAge} ago")
    )
    #Network Summary
    tblNetwork = Table(title=' Network Summary', title_justify='left', show_header=False, show_footer=False, min_width = 45, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblNetwork.add_column("", style='bright_black')
    tblNetwork.add_column("", justify='right', style='bright_white')
    tblNetwork.add_row(
        Text(f"{'Connections'}"),
        Text(f"{getNetworkInfo['connections']}"),
    )
    tblNetwork.add_row(
        Text(f"{'  Inbound'}"),
        Text(f"{getNetworkInfo['connections_in']}"),
    )
    tblNetwork.add_row(
        Text(f"{'Verification Progress'}"),
        Text(f"{getBlockChainInfo['verificationprogress']*100:,.04f}%"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, Epoch'}"),
        Text(f"{getNtwrkHashps / EXAHASH:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, 7-day'}"),
        Text(f"{get7DNtwrkHashps / EXAHASH:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, 4 weeks'}"),
        Text(f"{get4WNtwrkHashps / EXAHASH:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Hash Rate, 1-day'}"),
        Text(f"{get1DNtwrkHashps / EXAHASH:.1f} EH/s"),
    )
    tblNetwork.add_row(
        Text(f"{'Chain Work'}"),
        Text(f"{math.log2(int(getBlockChainInfo['chainwork'], 16)):.1f} bits"),
    )
    tblNetwork.add_row(
        Text(f"{'Total Transactions'}"),
        Text(f"{totalTXs:,.0f}"),
    )
    tblNetwork.add_row(
        Text(f"{'  Rate, 30 Days'}"),
        Text(f"{txRatePerSec:.1f} tx/s"),
    )
    tblNetwork.add_row(
        Text(f"{'  Count, 30 Days'}"),
        Text(f"{txCount:,.0f}")
    )
    #Metrics / Events
    tblMetricEvents = Table(title=' Metrics / Events', title_justify='left', show_header=False, show_footer=False, min_width = 45, caption=COPYRIGHT, box=box.HORIZONTALS, highlight=True, border_style='dim bold red', style='white') #
    tblMetricEvents.add_column("", style='bright_black')
    tblMetricEvents.add_column("", justify='right', style='bright_white')
    tblMetricEvents.add_row(
        Text(f"{'Difficulty Epoch'}"),
        Text(f"{1+(MAX_HEIGHT // nInterval):.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'Block time, 2016 blocks'}"),
        Text(f"{avg_2016_blockTime}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'Block time, Diff. Epoch'}"),
        Text(f"{avgEpochBlockTime}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Blocks to Retarget'}"),
        Text(f"{epochBlocksRemain:,.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Retarget Date'}"),
        Text(f"{RetargetDate}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Estimated Change'}"),
        Text(f"{estDiffChange:.01f}%"), 
    )
    tblMetricEvents.add_row(
        Text(f"{'  Retarget in nBits'}"),
        Text(f"{bnNew:.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'Blocks to Halving'}"),
        Text(f"{nBlocksToHalving:,.0f}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Estimate Halving on'}"),
        Text(f"{halvingDate}"),
    )
    tblMetricEvents.add_row(
        Text(f"{'  Subsidy Epoch'}"),
        Text(f"{1 +(MAX_HEIGHT // HALVING_BLOCKS)}")  
    )
    
    return tblMarket, tblGold, tblSupply, tblMining, tblBestBlock, tblNetwork, tblMetricEvents 
