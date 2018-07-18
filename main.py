import shared as mod_shared
import create_stock_lists as mod_list
import watchlist as mod_watch
from pdb import set_trace as BP
import re
from robobrowser import RoboBrowser
import yaml
import os
import requests
import sys
from bs4 import BeautifulSoup
import inspect
import schedule
import time
import datetime
import csv
import json
import math
from collections import OrderedDict
from pprint import pprint
from pprint import pformat

# Static price update at setStockStatus?
# Only use stop-loss?
glo_file_this = os.path.basename(__file__)

test_overall = False

# --- Global variables

# stock status keys
glo_status_action = 'ACTION'

# stock status values
glo_status_tempValue_ActiveNnSell = 'Sälj'
glo_status_tempValue_ActiveNnBuy = 'Köp'
glo_status_value_activeBuy = 'BUY'
glo_status_value_activeSell = 'SELL'
glo_status_value_heldYes = 'YES'
glo_status_value_heldDefault = glo_status_value_activeDefault = glo_status_value_activeTempDefault = glo_status_value_amountHeldDefault = glo_status_value_priceDefault = glo_status_value_priceTempDefault = ''

# payloadOrder- Keys
glo_orderNn_key_identifier = 'identifier'
glo_orderNn_key_marketId = 'market_id'
glo_orderNn_key_side = 'side'
glo_orderNn_key_price = 'price'
glo_orderNn_key_currency = 'currency'
glo_orderNn_key_volume = 'volume'
glo_orderNn_key_openVolume = 'open_volume'
glo_orderNn_key_orderType = 'order_type'
glo_orderNn_key_smartOrder = 'smart_order'
glo_orderNn_key_validUntil = 'valid_until'

# payloadOrder- Values
glo_orderNn_value_currencySek = 'SEK'
glo_orderNn_value_openVolume = '0'
glo_orderNn_value_orderType = 'LIMIT'
glo_orderNn_value_smartOrder = '0'
glo_orderNn_value_side_buy = 'BUY'
glo_orderNn_value_side_sell = 'SELL'

# whatchlist
glo_sbSignalBuy = 'BUY'
glo_sbSignalSell = 'SELL'
glo_sbSignalShort = 'SHORT'
glo_allowedSignals_list = [glo_sbSignalBuy,
    glo_sbSignalSell,
    glo_sbSignalShort]

# time condition
glo_timeConditionRerunStockFile = {
    'days': 14,
    'hours': 0,
    'minutes': 0,
    'seconds': 0
}

# time
glo_marketOpeningTime = datetime.time(9,0)
glo_marketClosingTime = datetime.time(17,29)
glo_afterMarketHoursOpen = datetime.time(20,30)
glo_afterMarketHoursClosed = datetime.time(21,00)

# amount to deal with
glo_numberOfStocksHeld = glo_maxNumberOfStocks = glo_maxNumberOfActiveAboveMaxHeld = None # saftey reason: will not trade if something goes wrong
glo_numberOfStocksActiveBuy = glo_numberOfStocksActiveSell = glo_activeBuy_temp = glo_activeSell_temp = 0
glo_amountAvailable = glo_amountAvailableStatic = None

# statistics
glo_confStat_fileName_str = 'confirmationStatistics.csv'
glo_stat_key_date = 'DATE'
glo_stat_key_time = 'TIME'
glo_stat_key_day = 'DAY'
glo_stat_key_nameShortSb = mod_shared.glo_colName_sbNameshort
glo_stat_key_signal = 'SIGNAL'
glo_stat_key_confirmation = 'CONFIRMATION'
glo_stat_key_priceLast = 'PRICE_LAST'
glo_stat_key_priceLevel = 'PRICE_LEVEL'
glo_stat_key_priceDifference = 'LAST_LEVEL_DIFFERENCE'

glo_key_errorMsg = 'errMsg'
glo_key_errorLine = 'line'
glo_key_errorFunction = 'function'
glo_key_statusCode = 'status_code'
glo_key_statusText = 'status_text'

glo_scrapeSbForSignalsAfterMarketIsClosed_counter = 0

# red days
glo_redDays = {
    'Mar_29_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Mar 29 13 00', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Mar 29 17 30', '%Y %b %d %H %M')
    },
    'Mar_30_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Mar 30 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Mar 30 17 30', '%Y %b %d %H %M')
    },
    'Apr_02_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Apr 02 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Apr 02 17 30', '%Y %b %d %H %M')
    },
    'May_01_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 May 01 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 May 01 17 30', '%Y %b %d %H %M')
    },
    'May_09_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 May 09 13 00', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 May 09 17 30', '%Y %b %d %H %M')
    },
    'May_10_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 May 10 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 May 10 17 30', '%Y %b %d %H %M')
    },
    'Jun_06_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Jun 06 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Jun 06 17 30', '%Y %b %d %H %M')
    },
    'Jun_22_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Jun 22 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Jun 22 17 30', '%Y %b %d %H %M')
    },
    'Nov_02_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Nov 02 13 00', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Nov 02 17 30', '%Y %b %d %H %M')
    },
    'Dec_24_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Dec 24 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Dec 24 17 30', '%Y %b %d %H %M')
    },
    'Dec_25_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Dec 25 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Dec 25 17 30', '%Y %b %d %H %M')
    },
    'Dec_26_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Dec 26 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Dec 26 17 30', '%Y %b %d %H %M')
    },
    'Dec_31_2018': {
    'CLOSE_START' : datetime.datetime.strptime('2018 Dec 31 08 55', '%Y %b %d %H %M'),
    'CLOSE_END' : datetime.datetime.strptime('2018 Dec 31 17 30', '%Y %b %d %H %M')
    }
}
# --- END Global variables

def getRemovalList(list_to_keep, list_to_remove, key_selector):
    try:
        removal_list = []
        for dict_keep in list_to_keep:
            for dict_remove in list_to_remove:
                if dict_keep.get(key_selector) == dict_remove.get(key_selector):
                    temp_ordered = OrderedDict()
                    temp_ordered[key_selector] = dict_remove.get(key_selector)
                    removal_list.append(temp_ordered)
        return removal_list
    except Exception as e:
        mod_shared.errorHandler(e)

def getStockStatus():
    try:
        r, header, s = mod_shared.nordnetLogin() # login to nordnet

        test = False
        
        # get HELD
        temp_nNHeld_list = []
        if test:
            print('TEST MODE: {}'.format(inspect.stack()[0][3]))
            temp_nNHeld_dict = OrderedDict()
            temp_nNHeld_dict[mod_shared.glo_colName_nameNordnet] = 'Copperstone Resources AB ser. B'
            temp_nNHeld_dict[mod_shared.glo_colName_amountHeld] = '100'
            temp_nNHeld_list.append(temp_nNHeld_dict)
            
            temp_nNHeld_dict = OrderedDict()
            temp_nNHeld_dict[mod_shared.glo_colName_nameNordnet] = 'Biotage AB'
            temp_nNHeld_dict[mod_shared.glo_colName_amountHeld] = '100'
            temp_nNHeld_list.append(temp_nNHeld_dict)
        else:
            soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/web/depa/mindepa/depaoversikt.html', headers=mod_shared.glo_urlHeader_userAgent).content, 'html.parser')
            stockTable = soup.find(id='aktier')
            stockHeldAndAmount = stockTable.find_all('tr', id=re.compile('tr')) # find <tr> where id='tr[x]'
            if stockHeldAndAmount:
                for stock in stockHeldAndAmount:
                    temp_nNHeld_dict = {}
                    nameNordnet = stock.find(class_='truncate18').get_text(strip=True)
                    temp_nNHeld_dict[mod_shared.glo_colName_nameNordnet] = nameNordnet

                    # get number of stocks
                    amountHeld = stock.find_all('td')[3].get_text(strip=True)
                    temp_nNHeld_dict[mod_shared.glo_colName_amountHeld] = amountHeld

                    temp_nNHeld_list.append(temp_nNHeld_dict)

        # get ACTIVE
        temp_nNActive_list = []
        if test:
            temp_nNActive_dict = OrderedDict()
            temp_nNActive_dict[mod_shared.glo_colName_nameNordnet] = 'Old Mutual Plc'
            temp_nNActive_dict[mod_shared.glo_colName_active] = glo_status_value_activeBuy
            temp_nNActive_list.append(temp_nNActive_dict)
            
            temp_nNActive_dict = OrderedDict()
            temp_nNActive_dict[mod_shared.glo_colName_nameNordnet] = 'G5 Entertainment AB'
            temp_nNActive_dict[mod_shared.glo_colName_active] = glo_status_value_activeSell
            temp_nNActive_list.append(temp_nNActive_dict)
        else:
            soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/ajax/trade/orders/auto?accountNumber=18272500', headers=mod_shared.glo_urlHeader_userAgent).content, 'html.parser') # active are placed in "share"
            newDict = json.loads(str(soup))
            newList = newDict.get('share')
            for item in newList:
                temp_nNActive_dict = OrderedDict()
                temp_nNActive_dict[mod_shared.glo_colName_nameNordnet] = item.get('longName')
                temp_nnStockActiveType = item.get('buyOrSell')
                if temp_nnStockActiveType == glo_status_tempValue_ActiveNnBuy: #active BUY
                    temp_nNActive_dict[mod_shared.glo_colName_active] = glo_status_value_activeBuy
                elif temp_nnStockActiveType == glo_status_tempValue_ActiveNnSell: #active SELL
                    temp_nNActive_dict[mod_shared.glo_colName_active] = glo_status_value_activeSell
                temp_nNActive_list.append(temp_nNActive_dict)

        # update held with active if same stock exist in both
        list_of_key_selectors = [mod_shared.glo_colName_nameNordnet]
        list_of_key_overwriters = [mod_shared.glo_colName_active]
        temp_nNHeld_list = mod_shared.updateListFromListByKeys(temp_nNHeld_list, temp_nNActive_list, list_of_key_selectors, list_of_key_overwriters)
        
        key_selector = mod_shared.glo_colName_nameNordnet
        removal_list = getRemovalList(temp_nNHeld_list, temp_nNActive_list, key_selector)

        # add to new list if not existing in ACTIVE list
        list_of_key_selectors = [mod_shared.glo_colName_nameNordnet]
        temp_nNActive_list = mod_shared.removeListFromListByKey(temp_nNActive_list, removal_list, list_of_key_selectors)
        
        nNHeld_nNActive_merged = temp_nNHeld_list + temp_nNActive_list
        
        return nNHeld_nNActive_merged
    except Exception as e:
        mod_shared.errorHandler(e)

def formatStrToFloat(arg_str):
    try:
        # remove spaces and convert ',' to '.'. E.g., '2 245,55' -> 2245.55
        return float(arg_str.replace(",", ".").replace(" ", ""))
    except Exception as e:
        mod_shared.errorHandler(e)

def setAndGetStockStatusFromNn():
    try:
        nNAmountAvailable_str = getAmountAvailableFromNn()
        nNAmountAvailable_float = formatStrToFloat(nNAmountAvailable_str)
        setAmountAvailable(int(nNAmountAvailable_float))
        
        stocksToBuy_list = mod_shared.getListFromFile(mod_shared.path_input_main, mod_shared.glo_stockToBuy_file)
        stocksToBuy_list = resetStockStatus(stocksToBuy_list) # set default values to ACTIVE, AMOUNT_HELD etc

        # get stocks with held and active info
        nNHeldAndActive_list = getStockStatus()

        # set stocks held
        counter_held = 0
        for heldAndActive_dict in nNHeldAndActive_list:
            if mod_shared.glo_colName_amountHeld in heldAndActive_dict:
                counter_held += 1
        if counter_held:
            setNumberOfStocksHeld(counter_held)

        # set stocks active buy
        counter_active_buy = 0
        for heldAndActive_dict in nNHeldAndActive_list:
            if heldAndActive_dict.get(mod_shared.glo_colName_active) == glo_status_value_activeBuy:
                counter_active_buy += 1
        if counter_active_buy:
            setNumberOfStocksActiveBuy(counter_active_buy)

        # set stock active sell
        counter_active_sell = 0
        for heldAndActive_dict in nNHeldAndActive_list:
            if heldAndActive_dict.get(mod_shared.glo_colName_active) == glo_status_value_activeSell:
                counter_active_sell += 1
        if counter_active_sell:
            setNumberOfStocksActiveSell(counter_active_sell)

        # scenarios:
        # - not stocks found
        # - stocks found: non-existing in stocksToBuy_list
        # - stocks found: some existing in stocksToBuy_list
        # - stocks found: all existing in stocksToBuy_list
        if not nNHeldAndActive_list:
            # no stocks found (list is empty). Returning unaltered stocksToBuy_list
            return stocksToBuy_list
        else:
            # stocks found
            # remove any already existing in stocksToBuy_list
            stocks_to_remove = [d.get(mod_shared.glo_colName_nameNordnet) for d in nNHeldAndActive_list]
            stocksToBuy_list = [d for d in stocksToBuy_list if d.get(mod_shared.glo_colName_nameNordnet) not in stocks_to_remove]
            # update nNHeldAndActive_list with keys of stocksToBuy_list
            nNHeldAndActive_list = mod_shared.setListKeys(nNHeldAndActive_list, mod_shared.glo_stockToBuy_colNames)
            # update with data from stocksToBuy_list
            stocksAllUpdated_list = mod_shared.getListFromFile(mod_shared.path_input_createList, mod_shared.glo_stockInfoUpdated_file) 
            list_of_key_selectors = [mod_shared.glo_colName_nameNordnet]
            list_of_key_overwriters = list(mod_shared.glo_stockToBuy_colNames.keys())
            nNHeldAndActive_list = mod_shared.updateListFromListByKeys(nNHeldAndActive_list, stocksAllUpdated_list, list_of_key_selectors, list_of_key_overwriters) # list to overwrite, list to overwrite with, -, -
            # merge the lists
            stocksToBuy_list += nNHeldAndActive_list

            return stocksToBuy_list
    except Exception as e:
        mod_shared.errorHandler(e)

def resetStockStatus(stockStatus_list):
    print ('\n', inspect.stack()[0][3])
    try:
        for row in stockStatus_list:
            row[mod_shared.glo_colName_active] = glo_status_value_activeDefault
            row[mod_shared.glo_colName_activeTemp] = glo_status_value_activeTempDefault
            row[mod_shared.glo_colName_amountHeld] = glo_status_value_amountHeldDefault
            # row[mod_shared.glo_colName_price] = glo_status_value_priceDefault
            # row[mod_shared.glo_colName_priceTemp] = glo_status_value_priceTempDefault
        return stockStatus_list
    except Exception as e:
        mod_shared.errorHandler(e)

def isStockHeld(sbStockNameShort):
    try:
        local_glo_stockStatus_list = mod_shared.getGlobalList(mod_shared.glo_stockStatus_list_name)
        for row in local_glo_stockStatus_list:
            if row.get(mod_shared.glo_colName_sbNameshort) == sbStockNameShort and row.get(mod_shared.glo_colName_amountHeld) != glo_status_value_amountHeldDefault:
                return True
        print('stock NOT held')
        return False # if no match
    except Exception as e:
        mod_shared.errorHandler(e)

def isStockActive(sbStockNameShort, sbActiveType):
    try:
        local_glo_stockStatus_list = mod_shared.getGlobalList(mod_shared.glo_stockStatus_list_name)
        for row in local_glo_stockStatus_list:
            if sbActiveType == glo_sbSignalBuy:
                if row.get(mod_shared.glo_colName_sbNameshort) == sbStockNameShort and row.get(mod_shared.glo_colName_active) == glo_status_value_activeBuy:
                    print('stock is ACTIVE: {}'.format(sbActiveType))
                    return True
            elif sbActiveType == glo_sbSignalSell:
                if row.get(mod_shared.glo_colName_sbNameshort) == sbStockNameShort and row.get(mod_shared.glo_colName_active) == glo_status_value_activeSell:
                    print('stock is ACTIVE: {}'.format(sbActiveType))
                    return True
        return False # if no match
    except Exception as e:
        mod_shared.errorHandler(e)

def setStockActiveTemp(sbStockNameShort, sbActiveType):
    print ('\n', inspect.stack()[0][3])
    try:
        glo_stockStatus_list = mod_shared.getGlobalList(mod_shared.glo_stockStatus_list_name)
        for row in glo_stockStatus_list:
            if row.get(mod_shared.glo_colName_sbNameshort) == sbStockNameShort:
                row.update({mod_shared.glo_colName_activeTemp:sbActiveType})
                print('stock was set ACTIVE_TEMP: {}'.format(sbActiveType))
        mod_shared.setListGlobal(glo_stockStatus_list, mod_shared.glo_stockStatus_list_name)

        # update number of temp active
        if sbActiveType == glo_status_value_activeBuy:
            incrActiveBuy_temp()
        if sbActiveType == glo_status_value_activeSell:
            incrActiveSell_temp()

    except Exception as e:
        mod_shared.errorHandler(e)

def isStockActiveTemp(sb_nameShort, sb_activeType):
    try:
        glo_stockStatus_list = mod_shared.getGlobalList(mod_shared.glo_stockStatus_list_name)
        for dict_stock in glo_stockStatus_list:
            if dict_stock.get(mod_shared.glo_colName_sbNameshort) == sb_nameShort and dict_stock.get(mod_shared.glo_colName_activeTemp) == glo_status_value_activeBuy:
                print('stock {} is ACTIVE_TEMP: {}'.format(sb_nameShort, sb_activeType))
                return True
            if dict_stock.get(mod_shared.glo_colName_sbNameshort) == sb_nameShort and dict_stock.get(mod_shared.glo_colName_activeTemp) == glo_status_value_activeSell:
                print('stock {} is ACTIVE_TEMP: {}'.format(sb_nameShort, sb_activeType))
                return True
        return False # if no match
    except Exception as e:
        mod_shared.errorHandler(e)

def isMaxStockHeldAndActive():
    try:
        maxNumberOfStocks = getMaxNumberOfStocks()
        numberOfStocksHeld = getNumberOfStocksHeld()
        print('numberOfStocksHeld: {}'.format(numberOfStocksHeld))
        numberOfStocksActiveBuy = getNumberOfStocksActiveBuy()
        print('numberOfStocksActiveBuy: {}'.format(numberOfStocksActiveBuy))
        numberOfStocksActiveSell = getNumberOfStocksActiveSell()
        print('numberOfStocksActiveSell: {}'.format(numberOfStocksActiveSell))
        numberOfStocksActiveBuy_temp = getNumberOfActiveBuy_temp()
        print('numberOfStocksActiveBuy_temp: {}'.format(numberOfStocksActiveBuy_temp))
        numberOfStocksActiveSell_temp = getNumberOfActiveSell_temp()
        print('numberOfStocksActiveSell_temp: {}'.format(numberOfStocksActiveSell_temp))

        stockHeldAndActive = numberOfStocksHeld + numberOfStocksActiveBuy + numberOfStocksActiveBuy_temp - numberOfStocksActiveSell - numberOfStocksActiveSell_temp
        print('stockHeldAndActive: {}'.format(stockHeldAndActive))

        if stockHeldAndActive >= maxNumberOfStocks:
            print('Max number of stocks already held or are active buys')
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def setAmountAvailable(amountInt):
    print ('\n', inspect.stack()[0][3])
    try:
        global glo_amountAvailable
        glo_amountAvailable = amountInt
    except Exception as e:
        mod_shared.errorHandler(e)

def setAmountAvailableStatic(amountInt):
    try:
        global glo_amountAvailableStatic
        glo_amountAvailableStatic = amountInt
        print('{}: {}'.format(inspect.stack()[0][3], amountInt))
    except Exception as e:
        mod_shared.errorHandler(e)

def updateAmountAvailable(sbSignalType, payloadOrder):
    print ('\n', inspect.stack()[0][3])
    try:
        global glo_amountAvailable
        global glo_amountAvailableStatic
        if sbSignalType == glo_sbSignalBuy:
            if glo_amountAvailableStatic != None:
                glo_amountAvailableStatic -= int(float(payloadOrder.get(glo_orderNn_key_price)) * float(payloadOrder.get(glo_orderNn_key_volume)))
            else:
                glo_amountAvailable -= int(float(payloadOrder.get(glo_orderNn_key_price)) * float(payloadOrder.get(glo_orderNn_key_volume)))
        elif sbSignalType == glo_sbSignalSell:
            if glo_amountAvailableStatic != None:
                glo_amountAvailableStatic += int(float(payloadOrder.get(glo_orderNn_key_price)) * float(payloadOrder.get(glo_orderNn_key_volume)))
            else:
                glo_amountAvailable += int(float(payloadOrder.get(glo_orderNn_key_price)) * float(payloadOrder.get(glo_orderNn_key_volume)))
    except Exception as e:
        mod_shared.errorHandler(e)

def getAmountAvailable():
    try:
        amountAvailable = glo_amountAvailable
        amountAvailableStatic = glo_amountAvailableStatic
        if amountAvailableStatic is not None:
            return amountAvailableStatic
        else:
            return amountAvailable
    except Exception as e:
        mod_shared.errorHandler(e)

def setNumberOfStocksHeld(numberHeld_int):
    try:
        global glo_numberOfStocksHeld
        glo_numberOfStocksHeld = numberHeld_int
    except Exception as e:
        mod_shared.errorHandler(e)

def getNumberOfStocksHeld():
    try:
        if glo_numberOfStocksHeld:
            return glo_numberOfStocksHeld
        else:
            return 0
    except Exception as e:
        mod_shared.errorHandler(e)

def setNumberOfStocksActiveBuy(numberActiveBuy_int):
    try:
        global glo_numberOfStocksActiveBuy
        glo_numberOfStocksActiveBuy = numberActiveBuy_int
    except Exception as e:
        mod_shared.errorHandler(e)

def getNumberOfStocksActiveBuy():
    try:
        if glo_numberOfStocksActiveBuy:
            return glo_numberOfStocksActiveBuy
        else:
            return 0
    except Exception as e:
        mod_shared.errorHandler(e)

def setNumberOfStocksActiveSell(numberActiveSell_int):
    try:
        global glo_numberOfStocksActiveSell
        glo_numberOfStocksActiveSell = numberActiveSell_int
    except Exception as e:
        mod_shared.errorHandler(e)

def getNumberOfStocksActiveSell():
    try:
        if glo_numberOfStocksActiveSell:
            return glo_numberOfStocksActiveSell
        else:
            return 0
    except Exception as e:
        mod_shared.errorHandler(e)

def incrActiveBuy_temp():
    try:
        global glo_activeBuy_temp
        glo_activeBuy_temp += 1
    except Exception as e:
        mod_shared.errorHandler(e)

def getNumberOfActiveBuy_temp():
    try:
        if glo_activeBuy_temp:
            return glo_activeBuy_temp
        else:
            return 0
    except Exception as e:
        mod_shared.errorHandler(e)

def incrActiveSell_temp():
    try:
        global glo_activeSell_temp
        glo_activeSell_temp += 1
    except Exception as e:
        mod_shared.errorHandler(e)

def getNumberOfActiveSell_temp():
    try:
        if glo_activeSell_temp:
            return glo_activeSell_temp
        else:
            return 0
    except Exception as e:
        mod_shared.errorHandler(e)

def setMaxNumberOfStocks(numberOfStocksInt):
    try:
        global glo_maxNumberOfStocks
        glo_maxNumberOfStocks = numberOfStocksInt
        print('{}: {}'.format(inspect.stack()[0][3], numberOfStocksInt))
    except Exception as e:
        mod_shared.errorHandler(e)

def getMaxNumberOfStocks():
    try:
        return glo_maxNumberOfStocks
    except Exception as e:
        mod_shared.errorHandler(e)

def setMaxNumberOfActiveAboveMaxHeld(numberOfStocksInt):
    try:
        global glo_maxNumberOfActiveAboveMaxHeld
        glo_maxNumberOfActiveAboveMaxHeld = numberOfStocksInt
        print('{}: {}'.format(inspect.stack()[0][3], numberOfStocksInt))
    except Exception as e:
        mod_shared.errorHandler(e)

def getMaxNumberOfActiveAboveMaxHeld():
    try:
        return glo_maxNumberOfActiveAboveMaxHeld
    except Exception as e:
        mod_shared.errorHandler(e)

def getNnStockVolume(orderNnValuePriceStr):
    try:
        # get amount available
        amountAvailableInt = getAmountAvailable()
        maxNumberOfStocksInt = getMaxNumberOfStocks()
        maxNumberOfActiveAboveMaxHeldInt = getMaxNumberOfActiveAboveMaxHeld() # to have loose cash to pay stock if both sell and buy at same time
        currentNumberOfTotalHeldAndActive = getNumberOfStocksHeld() + getNumberOfStocksActiveBuy() - getNumberOfStocksActiveSell()
        orderNnValuePriceFloat = float(orderNnValuePriceStr)
        orderNnValueVolumeStr = str(int(amountAvailableInt / (maxNumberOfStocksInt + maxNumberOfActiveAboveMaxHeldInt - currentNumberOfTotalHeldAndActive) / orderNnValuePriceFloat))

        return orderNnValueVolumeStr
    except Exception as e:
        mod_shared.errorHandler(e)

def getNnStockValidUntil():
    try:
        orderNnStockValidUntil = None
        if isMarketOpenNow():
            orderNnStockValidUntil = mod_shared.getDateToday_customFormat_str('%Y-%m-%d')
        else:
            noMatch = True
            day = 1
            while noMatch:
                dateTodayStr = mod_shared.getDateToday_customFormat_str('%Y-%m-%d')
                timeStr = '10:00' # red day open half day always 9-13
                timestampToday = datetime.datetime.strptime(dateTodayStr + ' ' + timeStr, '%Y-%m-%d %H:%M')
                timestampOtherday = timestampToday + datetime.timedelta(day)
                if isMarketOpenCustom(timestampOtherday):
                    timestampPosix = time.mktime(timestampOtherday.timetuple())
                    dateStr = datetime.date.fromtimestamp(timestampPosix).strftime('%Y-%m-%d')
                    orderNnStockValidUntil = dateStr
                    noMatch = False
                else:
                    day += 1
        return orderNnStockValidUntil
        # if not marketopen, valid until next day open
    except Exception as e:
        mod_shared.errorHandler(e)

def isWeekDay():
    try:
        if 1 <= mod_shared.getTimestamp().isoweekday() <= 5: # mon-fri <-> 1-5
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def isNotRedDay():
    try:
        for date, time in glo_redDays.items():
            if time['CLOSE_START'] < mod_shared.getTimestamp() < time['CLOSE_END']:
                return False # IS red day
        return True # is NOT red day
    except Exception as e:
        mod_shared.errorHandler(e)

def isWeekDayCustom(timestamp):
    try:
        if 1 <= timestamp.isoweekday() <= 5: # mon-fri <-> 1-5
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def isNotRedDayCustom(timestamp):
    try:
        for date, time in glo_redDays.items():
            if time['CLOSE_START'] < timestamp < time['CLOSE_END']:
                return False # IS red day
        return True # is NOT red day
    except Exception as e:
        mod_shared.errorHandler(e)

def isMarketHours():
    try:
        if glo_marketOpeningTime <= mod_shared.getTimestamp().time() < glo_marketClosingTime:
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def isSbHours():
    try:
        if glo_afterMarketHoursOpen <= mod_shared.getTimestamp().time() < glo_afterMarketHoursClosed:
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)    

def isMarketOpenNow():
    try:
        if isMarketHours() and isWeekDay() and isNotRedDay():
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def isMarketOpenCustom(timestamp):
    try:
        if isWeekDayCustom(timestamp) and isNotRedDayCustom(timestamp):
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def createPidFile(path_rel, name_of_file):
    try:
        pidInt = os.getpid()
        file_pid = mod_shared.path_base + path_rel + name_of_file
        with open(file_pid, "w") as file:
            file.write(str(pidInt))
    except Exception as e:
        mod_shared.errorHandler(e)

def resetTempActive():
    print (inspect.stack()[0][3])
    try:
        local_glo_stockStatus_list = mod_shared.getGlobalList(mod_shared.glo_stockStatus_list_name)
        for row in local_glo_stockStatus_list:
            row[mod_shared.glo_colName_activeTemp] = glo_status_value_activeTempDefault
        mod_shared.setListGlobal(local_glo_stockStatus_list, mod_shared.glo_stockStatus_list_name)
    except Exception as e:
        mod_shared.errorHandler(e)   

def resetActiveTrade():
    print (inspect.stack()[0][3])
    try:
        global glo_numberOfStocksActiveBuy
        global glo_numberOfStocksActiveSell
        global glo_activeBuy_temp
        global glo_activeSell_temp

        glo_numberOfStocksActiveBuy = glo_numberOfStocksActiveSell = glo_activeBuy_temp = glo_activeSell_temp = 0

    except Exception as e:
        mod_shared.errorHandler(e)

def resetDaily():
    print (inspect.stack()[0][3])
    print(mod_shared.getTimestampStr())
    try:
        # set tempActive to ''
        resetTempActive()
        # once reset, scrapeSbForSignals_afterMarketIsClosed() will use live data from Nordnet (first run next day)
        reset_scrapeSbForSignalsAfterMarketIsClosed_counter()
        # if stocks-to-buy.csv is older than x, renew by running create_stock_lists.py
        checkIfStockListNeedUpdating()
        # reset error counter
        mod_shared.resetCounterError()
        # reset active buy/sell
        resetActiveTrade()
    except Exception as e:
        mod_shared.errorHandler(e)

def triggerError():
    print(inspect.stack()[0][3])
    try:
        test = test
    except Exception as e:
        mod_shared.errorHandler(e)

def getAmountAvailableFromNn():
    try:
        r, header, s = mod_shared.nordnetLogin() # login to nordnet

        # get amount available
        soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/web/depa/mindepa/depaoversikt.html', headers=mod_shared.glo_urlHeader_userAgent).content, 'html.parser')
        amountAvailable_str = soup.find("td", string="Tillgängligt").next_sibling.next_sibling.get_text().strip(' SEK')
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return amountAvailable_str

def isStockFileOlderThanCondition(time_condition_dict, file_name):
    try:
        epochSecSinceLastModification = os.path.getmtime(mod_shared.path_base + mod_shared.path_input_main + file_name)
        epochSecNow = time.time()

        ageSecDelta = epochSecNow - epochSecSinceLastModification

        # ageOfFile = str(datetime.timedelta(seconds=(epochSecNow - epochSecSinceLastModification)) - datetime.timedelta(microseconds=datetime.timedelta(seconds=(epochSecNow - epochSecSinceLastModification)).microseconds))

        ageConditionSec = mod_shared.getSecondsFromTime(days=time_condition_dict.get('days'), 
            hours=time_condition_dict.get('hours'), 
            minutes=time_condition_dict.get('minutes'), 
            seconds=time_condition_dict.get('seconds'))

        if ageConditionSec < ageSecDelta:
            return True
        else:
            return False
    except Exception as e:
        mod_shared.errorHandler(e)   

def askIfToRerunStockFile():
    try:
        # if ask if to run for for new list
            while True:
                answer = input(mod_shared.glo_stockToBuy_file + ' was older than time condition. Do you wish to create new file? (y/n): ')
                if answer == 'n':
                    break
                elif answer == 'y':
                    mod_list.main()
                    break
                else: 
                    print('"' + answer +'"'+ ' was not recognized. Please only use "y" or "n"')
    except Exception as e:
        mod_shared.errorHandler(e)   

def scrapeSbForSignals_afterMarketIsClosed():
    print('\n',inspect.stack()[0][3])
    try:
        print(mod_shared.getTimestampStr())
        # if first time function is running after resetTempActive, get active and held from Nordnet. Otherwise tempActive applies
        if glo_scrapeSbForSignalsAfterMarketIsClosed_counter == 0:
            print('Getting active and held from Nordnet')
            stockStatus_list = setAndGetStockStatusFromNn()
            mod_shared.setListGlobal(stockStatus_list, mod_shared.glo_stockStatus_list_name)
        else:
            print('glo_scrapeSbForSignalsAfterMarketIsClosed_counter was not zero (it was {}), using tempActive'.format(glo_scrapeSbForSignalsAfterMarketIsClosed_counter))

        glo_stockStatus_list = mod_shared.getGlobalList(mod_shared.glo_stockStatus_list_name)
        stocks_for_action = []
        counter = 1
        dayDelta = 0 # 0 will check signal list date against date of today (-1 date of yesterday and so on)
        signalListTable_delta = 0 # 0 will pick first row in sb signal list table; 1 second row and so on
        breakAtFirstBuy = False
        if dayDelta != 0 or breakAtFirstBuy != False or signalListTable_delta != 0:
            print('TEST MODE: {}'.format(inspect.stack()[0][3]))
            print('dayDelta: {} (date: {})'.format(dayDelta, mod_shared.getDate_deltaToday_customFormat_str(dayDelta, "%d.%m.%Y")))
            print('signalListTable_delta: {}'.format(signalListTable_delta))
            print('breakAtFirstBuy: {}'.format(breakAtFirstBuy))
        
        requests_should_retry = True
        attempts_counter = 0
        max_attempts = 2
        while attempts_counter <= max_attempts and requests_should_retry:
            attempts_counter += 1
            # empty failed stock list before each attempt
            stocks_failed_list = []

            print('scraping for new signals...')
            for dict_stock in glo_stockStatus_list:
                print('\n{}/{}: {}'.format(counter, len(glo_stockStatus_list), dict_stock.get(mod_shared.glo_colName_sbNameshort)))
                counter += 1
                try:
                    r = mod_shared.requests_retry_session().get(dict_stock.get(mod_shared.glo_colName_url_sb))
                    if r.status_code != 200:
                        print('URL request FAILED')
                        print('r.status_code did not return 200')
                        print('status_code:', r.status_code)
                        print('text:', r.text[:150])
                        print('adding to stocks_failed_list')
                        dict_stock[glo_key_statusCode] = r.status_code
                        dict_stock[glo_key_statusText] = r.text[:150]
                        stocks_failed_list.append(dict_stock)
                        # at fail, continue with next stock
                        continue
                except Exception as e:
                    # mod_shared.errorHandler(e)
                    print('Exception raised. Adding to stocks_failed_list')
                    dict_stock[glo_key_errorMsg] = str(e)
                    dict_stock[glo_key_errorLine] = format(sys.exc_info()[-1].tb_lineno)
                    dict_stock[glo_key_errorFunction] = inspect.stack()[0][3]
                    stocks_failed_list.append(dict_stock)
                    # at fail, continue with next stock
                    continue
                else:
                    # stock page html
                    soup = BeautifulSoup(r.content, 'html.parser')
                    # table with 24 months signal list
                    signalList_table_months24 = soup.find_all(id=re.compile("MainContent_signalpagehistory_PatternHistory24_DXDataRow"))
                    if signalList_table_months24:
                        # latest signal date (format return: 'd.m.Y', 30.05.2018)
                        signal_date = signalList_table_months24[signalListTable_delta].find_all('td')[0].get_text()
                        # get signal type (e.g., 'BUY', 'SELL', 'SHORT' or 'QUIT' (NOT allowed))
                        signal_type = signalList_table_months24[signalListTable_delta].find_all('td')[2].get_text()
                        # if signal_date == mod_shared.getDate_deltaToday_customFormat_str(dayDelta, "%d.%m.%Y") and signal_type in glo_allowedSignals_list:
                        if signal_date == mod_shared.getDate_deltaToday_customFormat_str(dayDelta, "%d.%m.%Y") and signal_type in glo_allowedSignals_list:
                            # get signal price (e.g., '14.2200')
                            signal_priceIntraday = signalList_table_months24[signalListTable_delta].find_all('td')[1].get_text()
                            # set 'SHORT' to 'SELL'
                            if signal_type == glo_sbSignalShort:
                                signal_type = glo_sbSignalSell

                            sb_nameShort = dict_stock.get(mod_shared.glo_colName_sbNameshort)
                            nn_nameShort = dict_stock.get(mod_shared.glo_colName_nameShortNordnet)
                            if not isStockActive(sb_nameShort, signal_type) and not isStockActiveTemp(sb_nameShort, signal_type):
                                if signal_type == glo_sbSignalBuy:
                                    if (
                                        # not if already owning stock
                                        not isStockHeld(sb_nameShort) and
                                        isStockFulfillingBuyRequirements(dict_stock, signal_priceIntraday)
                                        ):
                                        print ('{}: adding to {} list'.format(nn_nameShort, glo_sbSignalBuy))
                                        # add what to do with stock
                                        dict_stock[glo_status_action] = glo_sbSignalBuy
                                        # add stock to list of stocks for action (used later)
                                        stocks_for_action.append(dict_stock)
                                        # below break only for testing
                                        if breakAtFirstBuy == True:
                                            break

                                elif signal_type == glo_sbSignalSell:
                                    if (
                                        isStockHeld(sb_nameShort)
                                        ):
                                        print ('{}: {}'.format(nn_nameShort, signal_type))
                                        nordnet_handleOrder_afterClosing(dict_stock, signal_type)
                    else:
                        # no 24 month signal list returned, continuing with next stock.
                        print('- stock', dict_stock.get(mod_shared.glo_colName_sbNameshort), '(', dict_stock.get(mod_shared.glo_colName_url_sb), ') did NOT return a 24 month signal list table: Continuing with next stock.')
                        continue
            # END 'for dict_stock in glo_stockStatus_list'
            # If stocks failed: first attempt
            if stocks_failed_list and attempts_counter < max_attempts:
                print('\nStocks failed:')
                for stock_failed in stocks_failed_list:
                    print(stock_failed.get(mod_shared.glo_colName_sbNameshort))
                print('trying again...')
                # below will make content of stocks_failed_list run in next loop scraping SB 
                glo_stockStatus_list = stocks_failed_list
            # if stocks failed after max attempts
            elif stocks_failed_list and requests_should_retry:
                print('\nStocks failed AGAIN:')
                print('Max attempts exceeded ({}), will NOT try again'.format(max_attempts))
                for stock_failed in stocks_failed_list:
                    print(stock_failed.get(mod_shared.glo_colName_sbNameshort))
                emailBodyInPformat = getStockFailedMessageForEmail(stocks_failed_list)
                emailSbj = 'Stocks failed in function: {}'.format(inspect.stack()[0][3])
                mod_shared.sendEmail(emailSbj, emailBodyInPformat)
                requests_should_retry = False
            # if stocks did NOT fail (either at first or nth attempt)
            else:
                requests_should_retry = False

        # END while loop   
        # buy stocks
        if stocks_for_action:
            # sort list to buy in specific order (will then stop if reaching maxStockHeldAndActive)
            stocks_for_action = sorted(stocks_for_action, 
            key=lambda k: k[mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange], 
            reverse=True) # (list to sort; column to sort on; order)
            print('\nbuy list order:')
            for row in stocks_for_action:
                print(row[mod_shared.glo_colName_sbNameshort],':', 
                    row[mod_shared.glo_colName_stockToBuy_group],':', 'price:',
                    row[mod_shared.glo_colName_price],':',
                    row[mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange]) 

            for dict_stock in stocks_for_action:
                print(dict_stock[mod_shared.glo_colName_sbNameshort]) 
                # check if already owning max amount of stocks
                if not isMaxStockHeldAndActive():
                    nordnet_handleOrder_afterClosing(dict_stock, glo_sbSignalBuy)
        # Usage: if counter is > 1 at start of scrapeSignals-function, use tempActive
        incr_scrapeSbForSignalsAfterMarketIsClosed_counter()
    except Exception as e:
        mod_shared.errorHandler(e)

def isStockFulfillingBuyRequirements(dict_stockStatus, signal_priceIntraday):
    try:
        # Buy only if intraday-closing percent change is less than MEDIAN_BUY_INTRADAY-CLOSING-CHANGE_PERCENT
        if dict_stockStatus.get(mod_shared.glo_colName_stockToBuy_group) == mod_shared.glo_value_group_1:
            # check nordnet for latest price
            nn_priceClosing = getNnStockPrice(dict_stockStatus.get(mod_shared.glo_colName_url_nn))
            intradayClosing_percentChange = mod_shared.getPercentChange(float(signal_priceIntraday), float(nn_priceClosing)) # start value, end value
            if intradayClosing_percentChange <= float(dict_stockStatus.get(mod_shared.glo_colName_median_buy_intradayClosingChange_percent)):
                return True

    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return False

def getNnStockPrice(nn_url):
    try:
        try:
            r = mod_shared.requests_retry_session().get(nn_url)
        except Exception as e:
            mod_shared.errorHandler(e)
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            # check nordnet for "Senast" price
            nn_priceClosing = soup.find(class_='tvaKnapp').parent.find_all('td')[2].get_text()
            nn_priceClosing = nn_priceClosing.replace(',', '.')

            return nn_priceClosing
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return False

def getPayloadOrder_staticValues(dict_stock):
    try:
        # static values
            #     'identifier':'76848',  
            #     'market_id':'11',
            #     'currency':'SEK',
            #     'open_volume':'0',
            #     'order_type': 'LIMIT',
            #     'smart_order':'0',
            #     'valid_until': '2018-02-05' # if after working hours or friday, set next date when open
        payloadOrder_staticValues_dict = {
            glo_orderNn_key_identifier: dict_stock.get(mod_shared.glo_colName_identifier_id),
            glo_orderNn_key_marketId: dict_stock.get(mod_shared.glo_colName_market_id),
            glo_orderNn_key_currency: glo_orderNn_value_currencySek,
            glo_orderNn_key_openVolume: glo_orderNn_value_openVolume,
            glo_orderNn_key_orderType: glo_orderNn_value_orderType,
            glo_orderNn_key_smartOrder: glo_orderNn_value_smartOrder,
            glo_orderNn_key_validUntil: getNnStockValidUntil()
        }
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return payloadOrder_staticValues_dict

def getPayloadOrder_dynamic_buy(dict_stock, nn_priceClosing_str):
    try:
        # dynamic values
            #     'side':'BUY',
            #     'price':'2.10',
            #     'volume':'1',
        nn_volume_str = getNnStockVolume(nn_priceClosing_str)
        payloadOrder_dynamic_dict = {
            glo_orderNn_key_price: nn_priceClosing_str,
            glo_orderNn_key_volume: nn_volume_str,
            glo_orderNn_key_side: glo_orderNn_value_side_buy
        }

    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return payloadOrder_dynamic_dict

def getPayloadOrder_dynamic_sell(dict_stock, nn_priceClosing_str):
    try:
        # dynamic values
            #     'side':'SELL',
            #     'price':'2.10',
            #     'volume':'1',
        sellDecimalSubtraction_float = mod_shared.getDecimalFromPercentage(mod_shared.glo_sellPercentageSubtraction)
        # variable format: 'xx.xx'
        nn_priceClosing_str = formatNnStockPriceForSell_rev(nn_priceClosing_str, sellDecimalSubtraction_float)
        payloadOrder_dynamic_dict = {
            glo_orderNn_key_price: nn_priceClosing_str,
            glo_orderNn_key_volume: dict_stock.get(mod_shared.glo_colName_amountHeld),
            glo_orderNn_key_side: glo_orderNn_value_side_sell
        }
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return payloadOrder_dynamic_dict

def nordnet_handleOrder_afterClosing(dict_stock, sb_signal_type):
    try:
        test_abortOrder = False

        nn_priceClosing_str = getNnStockPrice(dict_stock.get(mod_shared.glo_colName_url_nn))
        # get shared static value for payload order
        payloadOrder_staticValues_dict = getPayloadOrder_staticValues(dict_stock)
        # get dynamic payload order value depending on sell or buy
        if sb_signal_type == glo_sbSignalSell:
            payloadOrder_dynamic_dict = getPayloadOrder_dynamic_sell(dict_stock, nn_priceClosing_str)
            if payloadOrder_dynamic_dict.get(glo_orderNn_key_volume) == '0':
                # should never be zero
                sbj = '{}: {}: payloadOrder_dynamic_dict VOLUME was zero (0) for SELL:'.format(inspect.stack()[0][3], dict_stock.get(mod_shared.glo_colName_sbNameshort))
                body = pformat(payloadOrder_dynamic_dict)
                mod_shared.sendEmail(sbj, body)
                return
        elif sb_signal_type == glo_sbSignalBuy:
            payloadOrder_dynamic_dict = getPayloadOrder_dynamic_buy(dict_stock, nn_priceClosing_str)
            if payloadOrder_dynamic_dict.get(glo_orderNn_key_volume) == '0':
                # will be zero if price of stock is too high (not an error)
                print('VOLUME in payloadOrder_dynamic_dict was 0 (usually due to too high price')
                pprint(payloadOrder_dynamic_dict)
                return
        
        if isDynamicPayloadOrderValid(payloadOrder_dynamic_dict):
            # merge payload
            payloadOrder = {**payloadOrder_staticValues_dict, **payloadOrder_dynamic_dict}
            if test_abortOrder == True:
                print('Test mode: {}'.format(inspect.stack()[0][3]))
                print('aborting nordnet order placement, BUT setting stockActiveTemp')
                setStockActiveTemp(dict_stock.get(mod_shared.glo_colName_sbNameshort), sb_signal_type)
            else:
                nordnet_placeOrder(payloadOrder, dict_stock, sb_signal_type)
        else:
            print('payloadOrder_dynamic_dict was INCORRECT: {}'.format(dict_stock.get(mod_shared.glo_colName_sbNameshort)))
            pprint(payloadOrder_dynamic_dict)
            sbj = '{}: {}: payloadOrder_dynamic_dict was INCORRECT:'.format(inspect.stack()[0][3], dict_stock.get(mod_shared.glo_colName_sbNameshort))
            body = pformat(payloadOrder_dynamic_dict)
            mod_shared.sendEmail(sbj, body)
    except Exception as e:
        mod_shared.errorHandler(e)

    else:
        return

def isDynamicPayloadOrderValid(payloadOrder_dynamic_dict):
    try:
        price = payloadOrder_dynamic_dict.get(glo_orderNn_key_price)
        volume = payloadOrder_dynamic_dict.get(glo_orderNn_key_volume)
        side = payloadOrder_dynamic_dict.get(glo_orderNn_key_side)
        # checking volume is only digits
        if not volume.isdigit():
            print('function {}: {} was not only digits, it was: {}'.format(inspect.stack()[0][3], glo_orderNn_key_volume, volume))
            print('returning False')
            return False

        # checking volume is NOT '0'
        if int(volume) == 0:
            print('function {}: {} was zero, result: {}'.format(inspect.stack()[0][3], glo_orderNn_key_volume, volume))
            print('returning False')
            return False

        # checking if price contains other chars than digits or '.'
        if not price.replace(".", "").isdigit():
            print('function {}: {} contained none allowed chars, it was: {}'.format(inspect.stack()[0][3], glo_orderNn_key_price, price))
            print('returning False')
            return False

        # checking 'BUY' or 'SELL'
        if side != 'BUY' and side != 'SELL':
            print('function {}: {} was not "BUY" or "SELL", it was: {}'.format(inspect.stack()[0][3], glo_orderNn_key_side, side))
            print('returning False')
            return False

    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return True

def nordnet_placeOrder(payloadOrder, dict_stockStatus, sb_signal_type):
    try:
        sb_nameShort = dict_stockStatus.get(mod_shared.glo_colName_sbNameshort)

        r, header, s = mod_shared.nordnetLogin()
        header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        header['ntag'] = r.headers['ntag']
        header['User-Agent'] = mod_shared.glo_urlHeader_userAgent.get('User-Agent')
        urlOrder = 'https://www.nordnet.se/api/2/accounts/18272500/orders'
        r = s.post(urlOrder, headers=header, data=payloadOrder)

        if r.status_code == 200:
            print ('SUCCESS: order placed!')
            print(sb_nameShort)
            pprint(payloadOrder)
            setStockActiveTemp(sb_nameShort, sb_signal_type)
            updateAmountAvailable(sb_signal_type, payloadOrder)
            mod_shared.sendEmail(sb_nameShort + ':' + sb_signal_type, sb_nameShort + '\n'+ pformat(payloadOrder))
        else:
            print('FAILED: order failed!')
            print('status_code:', r.status_code)
            print('text:', r.text)
            responseDict = {
            'status_code': str(r.status_code),
            'reason': r.reason,
            'url': r.url
            }
            mod_shared.sendEmail('Failed order placement in nordnet_placeOrder: ' + sb_nameShort + ':' + sb_signal_type, sb_nameShort + '\n'+ pformat(responseDict))
    except Exception as e:
        mod_shared.errorHandler(e)

def formatNnStockPriceForSell(nn_price_str, sellDecimalSubtraction_float):
    try:
        nn_price_float = float(nn_price_str)
        nn_price_float = nn_price_float * (1-sellDecimalSubtraction_float)
        fraction, decimals = getDecimalsAndPrecision(nn_price_float)

        return rnd(nn_price_float, fraction, decimals, 'down')
    except Exception as e:
        mod_shared.errorHandler(e)

def formatNnStockPriceForSell_rev(nn_price_str, sellDecimalSubtraction_float):
    try:
        nn_price_float_org = float(nn_price_str)
        nn_price_float_rev = nn_price_float_org * (1-sellDecimalSubtraction_float)

        if 20 <= nn_price_float_rev:
            # print('20 <= nn_price_float_rev')
            decimals = 0
            # print('decimals: {}'.format(decimals))
        elif 5 <= nn_price_float_rev < 20:
            # print('5 <= nn_price_float_rev < 20')
            decimals = 1
            # print('decimals: {}'.format(decimals))
        elif 0.2 <= nn_price_float_rev < 5:
            # print('5 <= nn_price_float_rev < 20')
            decimals = 2
            # print('decimals: {}'.format(decimals))
        elif nn_price_float_rev < 0.2:
            # print('5 <= nn_price_float_rev < 20')
            decimals = 3
            # print('decimals: {}'.format(decimals))

        if decimals == 0:
            high = int(math.ceil(nn_price_float_rev*pow(10,decimals))/pow(10,decimals))
            low = int(math.floor(nn_price_float_rev*pow(10,decimals))/pow(10,decimals))
            # return the lowest number of it is larger than the set limit
            if mod_shared.getPercentChange(nn_price_float_org, low) > -(1*mod_shared.glo_sellPercentageSubtraction):
                return str(low)
            else:
                return str(high)
            # return str(int(math.ceil(nn_price_float*pow(10,decimals))/pow(10,decimals)))
        else:
            high = math.ceil(nn_price_float_rev*pow(10,decimals))/pow(10,decimals)
            low = math.floor(nn_price_float_rev*pow(10,decimals))/pow(10,decimals)
            if mod_shared.getPercentChange(nn_price_float_org, low) > -(1*mod_shared.glo_sellPercentageSubtraction):
                return str(low)
            else:
                return str(high)
    except Exception as e:
        mod_shared.errorHandler(e)

def getDecimalsAndPrecision(nn_price_float_sell):
    try:
        # price rules nordnet
            # - +1000: 0 decimals (whole crowns) (e.g., 1001; 1002)
            # - +500: 1 decimals (0.5) (whole crowns) (e.g., 501.5; 502.5)
            # - +200: 1 decimals (0.2) (e.g., 200.2; 201.0)
            # - +100: 1 decimals (0.1) (e.g., 100.1; 100.0)
            # - +50: 2 decimals (0.05) (e.g., 50.10; 50.15)
            # - +20: 2 decimals (0.02) (e.g., 20.02; 20.04)
            # - +10: 2 decimals (0.01) (e.g., 10.01; 10.02)
            # - +5: 3 decimals (0.005) (e.g., 5.015; 5.020)
            # - +2: 3 decimals (0.002) (e.g., 2.004; 2.006)
            # - +1: 3 decimals (0.001) (e.g., 1.001; 1.002)
            # - +0.5: 4 decimals (0.0005) (e.g., 0.5015; 0.5020)
            # - +0.2: 4 decimals (0.0002) (e.g., 0.2002; 0.2004)
            # - +0.0: 4 decimals (0.0001) (e.g., 0.0001; 0.0002)

        f1000 = 1
        d1000 = 0
        f500 = 0.5
        d500 = 1
        f200 = 0.2
        d200 = 1
        f100 = 0.1
        d100 = 1
        f50 = 0.05
        d50 = 2
        f20 = 0.02
        d20 = 2
        f10 = 0.01
        d10 = 2
        f5 = 0.005
        d5 = 3
        f2 = 0.002
        d2 = 3
        f1 = 0.001
        d1 = 3
        f05 = 0.0005
        d05 = 4
        f02 = 0.0002
        d02 = 4
        f00 = 0.0001
        d00 = 4

        if nn_price_float_sell>=1000:
            return f1000, d1000
        
        elif nn_price_float_sell>=500:
            return f500, d500

        elif nn_price_float_sell>=200:
            return f200, d200
            
        elif nn_price_float_sell>=100:
            return f100, d100
            
        elif nn_price_float_sell>=50:
            return f50, d50
            
        elif nn_price_float_sell>=20:
            return f20, d20
            
        elif nn_price_float_sell>=10:
            return f10, d10
            
        elif nn_price_float_sell>=5:
            return f5, d5
            
        elif nn_price_float_sell>=2:
            return f2, d2
            
        elif nn_price_float_sell>=1:
            return f1, d1
            
        elif nn_price_float_sell>=0.5:
            return f05, d05
            
        elif nn_price_float_sell>=0.2:
            return f02, d02
            
        elif nn_price_float_sell>=0.0:
            return f00, d00

    except Exception as e:
        mod_shared.errorHandler(e)

def rnd(price_float,frac,dec,direction=''): #float number; fraction number (e.g., 0.1, 0.2 etc); decimals; down if no argument, up if empty str ('')
    try:
        if direction=='down':
            if dec==0:
                return str(int(price_float))
            return str(round(price_float-math.fmod(price_float,frac),dec))
        elif direction=='up':
            if dec==0:
                return str(int(round(price_float)))
            price_float+=frac
            return str(round(price_float-math.fmod(price_float,frac),dec))
        else:
            n1=int(price_float) if dec==0 else round(price_float-math.fmod(price_float,frac),dec)
            n2=float(int(round(price_float))) if dec==0 else round((price_float+frac)-math.fmod((price_float+frac),frac),dec)
            if isinstance(n1, int):
                return str(int(min((n1,n2), key=lambda e: math.fabs(e-price_float))))
            else:
                return str(min((n1,n2), key=lambda e: math.fabs(e-price_float)))
    except Exception as e:
        mod_shared.errorHandler(e)

def setOrderStatistics():
    print('\n{}'.format(inspect.stack()[0][3]))
    # updates order statistics by using new orders from Nordnet and old order information from order-statistics.csv
    try:
        dailyOrders_nordnet_list = getDailyOrders_nordnet()
        if dailyOrders_nordnet_list:
            # safer than setListKeys which deletes keys. This requires columns to be deleted manually from order-statistics.csv
            dailyOrders_nordnet_list = mod_shared.addKeysNotExisting(dailyOrders_nordnet_list, mod_shared.glo_orderStatistics_colNames) 
            # set keys already existing in dailyOrders_nordnet_list to values of keys from stockToBuy_allData
            stocksToBuy_list = mod_shared.getListFromFile(mod_shared.path_input_main, mod_shared.glo_stockToBuy_file)
            list_of_key_selectors = [mod_shared.glo_colName_nameShortNordnet]
            dailyOrders_nordnet_list = mod_shared.updateListFromListBy_existingKeys(dailyOrders_nordnet_list,
                stocksToBuy_list,
                list_of_key_selectors) # list to update, list to update from

            orderStat_list = mod_shared.getListFromFile(mod_shared.path_output, mod_shared.glo_orderStatistics_file)
            if orderStat_list != False: # Important! Keep as False as longs as getListFromFile returns this for files not found.
                org_len = len(orderStat_list)
                orderStat_list_updated = getUpdatedOrderStatistics(orderStat_list, dailyOrders_nordnet_list)
                rev_len = len(orderStat_list_updated)
                if rev_len > org_len:
                    mod_shared.writeListToCsvFile(orderStat_list_updated, mod_shared.path_output + mod_shared.glo_orderStatistics_file)
                else:
                    sbj = 'Something might have gone wrong in function {}.'.format(inspect.stack()[0][3])
                    body = 'New {} did not have more rows than old. No changes made.'.format(mod_shared.glo_orderStatistics_file)
                    print(sbj, body)
                    mod_shared.sendEmail(sbj, body)
            else:
                print(mod_shared.glo_orderStatistics_file, 'did not exist. Creating new file with dailyOrders_nordnet_list')
                mod_shared.writeListToCsvFile(dailyOrders_nordnet_list, mod_shared.path_output + mod_shared.glo_orderStatistics_file)

    except Exception as e:
        mod_shared.errorHandler(e)

def getDailyOrders_nordnet():
    try:
        test_getDailyOrders_nordnet = False
        dailyOrders_nordnet_list = []
        if test_getDailyOrders_nordnet:
            print('TEST MODE: {}'.format(inspect.stack()[0][3]))
            temp_list = [
            # {'NAMESHORT_NORDNET': 'ARCT',
            #   'TRADE_PRICE': 5,
            #   'TRADE_TIME': '2018-05-27 16:37:37',
            #   'TRADE_TYPE': 'SELL'},
            # {'NAMESHORT_NORDNET': 'SAVOS',
            #   'TRADE_PRICE': 1.44,
            #   'TRADE_TIME': '2018-05-27 16:22:52',
            #   'TRADE_TYPE': 'SELL'},
            {'NAMESHORT_NORDNET': 'SALT B',
              'TRADE_PRICE': 99.8,
              'TRADE_TIME': '2018-05-27 16:22:52',
              'TRADE_TYPE': 'BUY'}
              ]
            for dict_item in temp_list:
                dict_item[mod_shared.glo_colName_trade_time] = dict_item.get(mod_shared.glo_colName_trade_time).split()[0]
                order_of_keys = list(dict_item.keys()) # keys will not retain order, but should not matter.
                dailyOrders_nordnet_list.append(mod_shared.getOrderedDictFromDict(dict_item, order_of_keys))
        else: 
            r, header, s = mod_shared.nordnetLogin() # login to nordnet

            soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/ajax/trade/orders/auto?accountNumber=18272500', headers=mod_shared.glo_urlHeader_userAgent).content, 'html.parser') # active are placed in "share"
            newDict = json.loads(str(soup))
            closedTrade_list = newDict.get('trade')
            if closedTrade_list:
                for dict_item in closedTrade_list:
                    dict_temp = OrderedDict()
                    dict_temp[mod_shared.glo_colName_nameShortNordnet] = dict_item.get('shortName')
                    dict_temp[mod_shared.glo_colName_trade_price] = str(dict_item.get('price')) # ex: 0.59 (int) -> '0.59'
                    dict_temp[mod_shared.glo_colName_trade_volume] = str(dict_item.get('volume')) # ex: 2 (int) -> '2'
                    dict_temp[mod_shared.glo_colName_trade_time] = dict_item.get('time') # ex: '2018-05-17 16:22:52'
                    # remove time
                    dict_temp[mod_shared.glo_colName_trade_time] = dict_temp.get(mod_shared.glo_colName_trade_time).split()[0] # ex: '2018-05-17'
                    dict_temp[mod_shared.glo_colName_trade_type] = dict_item.get('type') # ex: 'Köpt' or 'Sålt'
                    
                    if dict_temp.get(mod_shared.glo_colName_trade_type) == 'Köpt':
                        dict_temp[mod_shared.glo_colName_trade_type] = 'BUY'
                    else:
                        dict_temp[mod_shared.glo_colName_trade_type] = 'SELL'

                    dailyOrders_nordnet_list.append(dict_temp)
            else:
                print('No new order found in ' + inspect.stack()[0][3])
                return False
                    # dict_item contains
                        # {'identifier': '108026',
                        #  'market': 'NasdaqOMX Stockholm',
                        #  'marketplace': '11',
                        #  'name': 'Savosolar Plc',
                        #  'orderId': '138749253',
                        #  'price': 0.59,
                        #  'priceText': '0,59 SEK',
                        #  'shortName': 'SAVOS',
                        #  'time': '2018-05-17 16:22:52',
                        #  'timeText': '16:22:52',
                        #  'type': 'Köpt',
                        #  'volume': 1,
                        #  'volumeText': '1'}

    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return dailyOrders_nordnet_list

def getUpdatedOrderStatistics(orderStat_list, dailyOrders_nordnet_list):
    try:
        temp_list = []
        # calc percent change
        for dict_trade in dailyOrders_nordnet_list:
            # get all stock dicts which matches a stock name in dailyOrders_nordnet_list and where it is SELL and where the other stock is BUY
            onlyOneStockName_list = [item for item in orderStat_list if dict_trade.get('NAMESHORT_NORDNET') in item['NAMESHORT_NORDNET'] and 
            'BUY' in item['TRADE_TYPE'] and
            'SELL' in dict_trade.get('TRADE_TYPE')]
            if onlyOneStockName_list:
                # get the stock dict with the highest date
                onlyOneStockName_maxDate_dict = max(onlyOneStockName_list, key=lambda item:item['TRADE_TIME'])
                # calc percent change
                start_value = float(onlyOneStockName_maxDate_dict.get(mod_shared.glo_colName_trade_price))
                end_value = float(dict_trade.get(mod_shared.glo_colName_trade_price))
                percentage_change = round(mod_shared.getPercentChange(start_value, end_value), 2)
                dict_trade[mod_shared.glo_colName_trade_percentChange] = percentage_change
                # modify percent change with courtage cost
                percentage_change -= mod_list.glo_costOfCourtage
                
                excluded_keys_list = [mod_shared.glo_colName_trade_percentChange,
                    mod_shared.glo_colName_trade_price,
                    mod_shared.glo_colName_trade_type,
                    mod_shared.glo_colName_trade_time
                ]
                
                # below in order to retain all values already existing from previous buys
                # get key-values from onlyOneStockName_maxDate_dict, except keys from dailyOrders_nordnet_list
                dict_trade_1 = {key:value for (key,value) in onlyOneStockName_maxDate_dict.items() if key not in excluded_keys_list}
                # get key-values from dict_trade that are given from Nordnet
                dict_trade_2 = {key:value for (key,value) in dict_trade.items() if key in excluded_keys_list}
                dict_trade = {**dict_trade_1, **dict_trade_2}
                temp_list.append(dict_trade)
            else:
                temp_list.append(dict_trade)

        for dict_trade in temp_list:
            orderStat_list.append(dict_trade)
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return orderStat_list

def checkIfStockListNeedUpdating():
    print(inspect.stack()[0][3])
    try:
        if isStockFileOlderThanCondition(glo_timeConditionRerunStockFile, mod_shared.glo_stockToBuy_file):
            mod_list.main()
    except Exception as e:
        mod_shared.errorHandler(e)

def getStockFailedMessageForEmail(stocks_failed_list):
    try:
        stock_failed_email_list = []
        for stock_failed in stocks_failed_list:
            stock_failed_email_dict = {}
            stock_failed_email_dict[mod_shared.glo_colName_sbNameshort] = stock_failed.get(mod_shared.glo_colName_sbNameshort)
            if glo_key_errorFunction in stock_failed:
                stock_failed_email_dict[glo_key_errorFunction] = stock_failed.get(glo_key_errorFunction)
            if glo_key_errorLine in stock_failed:
                stock_failed_email_dict[glo_key_errorLine] = stock_failed.get(glo_key_errorLine)
            if glo_key_errorMsg in stock_failed:
                stock_failed_email_dict[glo_key_errorMsg] = stock_failed.get(glo_key_errorMsg)

            if glo_key_statusCode in stock_failed:
                stock_failed_email_dict[glo_key_statusCode] = stock_failed.get(glo_key_statusCode)
                stock_failed_email_dict[glo_key_statusText] = stock_failed.get(glo_key_statusText)
            stock_failed_email_list.append(stock_failed_email_dict)

        return pformat(stock_failed_email_list)

    except Exception as e:
        mod_shared.errorHandler(e)

def reset_scrapeSbForSignalsAfterMarketIsClosed_counter():
    print(inspect.stack()[0][3])
    try:
        global glo_scrapeSbForSignalsAfterMarketIsClosed_counter
        glo_scrapeSbForSignalsAfterMarketIsClosed_counter = 0
    except Exception as e:
        mod_shared.errorHandler(e)

def incr_scrapeSbForSignalsAfterMarketIsClosed_counter():
    try:
        global glo_scrapeSbForSignalsAfterMarketIsClosed_counter
        glo_scrapeSbForSignalsAfterMarketIsClosed_counter += 1
    except Exception as e:
        mod_shared.errorHandler(e)

schedule.every().day.at("19:45").do(scrapeSbForSignals_afterMarketIsClosed) 
schedule.every().day.at("20:30").do(scrapeSbForSignals_afterMarketIsClosed)
# get and set stats of closed orders
schedule.every().day.at("21:30").do(setOrderStatistics)
schedule.every().day.at("22:00").do(resetDaily)

# triggerError()

# for surverying script (in case of crash)
createPidFile(mod_shared.path_input_monitorProcess, mod_shared.glo_pid_file)

setMaxNumberOfStocks(10)
setMaxNumberOfActiveAboveMaxHeld(2)

# Comment out to use real value
# setAmountAvailableStatic(800)

# Equivalent is also executed in runtime (resetDaily)
if isStockFileOlderThanCondition(glo_timeConditionRerunStockFile, mod_shared.glo_stockToBuy_file):
    askIfToRerunStockFile()

while True and test_overall == False:
    # needed to run scheduled events
    schedule.run_pending()

if test_overall:
    print('TEST MODE: {}'.format(inspect.stack()[0][1]))
    BP()
    # scrapeSbForSignals_afterMarketIsClosed()
    # resetDaily()
    setAndGetStockStatusFromNn()
    getAmountAvailable()
    # isMaxStockHeldAndActive()
    BP()
    # scrapeSbForSignals_afterMarketIsClosed() 
    # scrapeSbForSignals_afterMarketIsClosed()
    # get and set stats of closed orders
    # setOrderStatistics()
    # resetDaily()