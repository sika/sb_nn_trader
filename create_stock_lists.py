import shared as mod_shared
from pdb import set_trace as BP
import os
import inspect
import csv
import requests
from bs4 import BeautifulSoup
import re
from statistics import median
from  more_itertools import unique_everseen
import time
import json
import datetime
import ast
import sys
from collections import OrderedDict
from pprint import pprint
from pprint import pformat

glo_file_this = os.path.basename(__file__)

# nordnet courtage (mini). https://www.nordnet.se/tjanster/prislista/oversikt.html#/
glo_costOfCourtage = 0.25

glo_nn_history_time = 'time'
glo_nn_history_closing = 'last'

glo_sb_history_date = 'date'
glo_sb_history_price = 'price'
glo_sb_history_signal = 'signal'

glo_colValue_notAvailable = 'N/A'

glo_test_bool = True
glo_test_str = 'test-'
glo_stockInfo_test_file = 'stock-info-raw-1.csv'

glo_runGetStocksFromSb_bool = True
glo_runSetAllStockLists_bool = True

def setFilteredStockList(rowDict):
    try:
        global glo_filteredStockInfo_list
        glo_filteredStockInfo_list.append(rowDict)
    except Exception as e:
        mod_shared.errorHandler(e)  

def filterFilteredStockInfo(column_key, criteria, temp_glo_filteredStockInfo_list):
    try:
        temp_list= []
        if column_key == mod_shared.glo_colName_buysTotal: #total buys
            for row in temp_glo_filteredStockInfo_list:
                if row.get(column_key) != '':
                    if row.get(column_key) >= criteria:
                        temp_list.append(row)
        elif column_key == mod_shared.glo_colName_24_buys_correct_percent: # percent correct buys
            for row in temp_glo_filteredStockInfo_list:
                if row.get(column_key) != '':
                    if row.get(column_key) >= criteria:
                        temp_list.append(row)
        elif column_key == mod_shared.glo_colName_buyAndFailMedian_keyValue:
            for row in temp_glo_filteredStockInfo_list:
                if row.get(column_key) != '':
                    if row.get(column_key) >= criteria:
                        temp_list.append(row)
        elif column_key == mod_shared.glo_colName_buyAndFailAverage_keyValue:
            for row in temp_glo_filteredStockInfo_list:
                if row.get(column_key) != criteria:
                    temp_list.append(row)
        temp_glo_filteredStockInfo_list = temp_list
        return temp_glo_filteredStockInfo_list
    except Exception as e:
        mod_shared.errorHandler(e)     

def getNnStockPageData(url_stock):
    try:
        result = re.search('identifier=(.*)&', url_stock)
        identifier_id = result.group(1)
        result = re.search('marketid=(.*)', url_stock)
        market_id = result.group(1)
        try:
            r = mod_shared.requests_retry_session().get(url_stock)
        except Exception as e:
            mod_shared.errorHandler(e)
            return False
        else:
            soup = BeautifulSoup(r.content, 'html.parser')

            # Note: below line throws error if not finding searched title (e.g., when Nordnet page requires login to view content). Can be ignored
            stock_heading_sentence = soup.find('h1', class_="title").get_text(strip=True)
            # get nordnet name
            nnName = re.search(r'Kursdata för (.*?) \(', stock_heading_sentence).group(1)
            
            # get nordnet shortname
            # if more than one match (e.g.: (publ) (aroc) ), get the last one
            nnNameshort_list = re.findall(r'\((.*?)\)', stock_heading_sentence)
            nnNameshort = nnNameshort_list[-1]

            list_of_tuples = [(mod_shared.glo_colName_nameNordnet, nnName),
            (mod_shared.glo_colName_nameShortNordnet, nnNameshort),
            (mod_shared.glo_colName_market_id, market_id),
            (mod_shared.glo_colName_identifier_id, identifier_id),
            (mod_shared.glo_colName_url_nn, url_stock)]
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return list_of_tuples
        
def getMultiplicationValue(soup_str, soup):
    try:
        value_6 = soup.find(id=re.compile(soup_str)).parent.parent.next_sibling.get_text()
        return int(float(value_6.replace(",", "")))             
    except Exception as e:
        mod_shared.errorHandler(e)

def getPercentCorrect(soup_str, soup):
    try:
        all_imgTags_6_month = soup.find_all(id=re.compile(soup_str))
        total_checks = len(all_imgTags_6_month)
        counter_uncheck = 0
        if all_imgTags_6_month and total_checks != 0:
            for imgtag in all_imgTags_6_month:
                srcName = imgtag['src'].lower() #'img/Uncheck.gif' in lower case 
                if srcName.find('uncheck') != -1: # "uncheck" spelling more reliable than "check"
                    counter_uncheck += 1
            counter_check = total_checks-counter_uncheck
            
            return round(100*(float(counter_check)/float(total_checks)), 1)                     
    except Exception as e:
        mod_shared.errorHandler(e)

def getStocksFromSb(stockInfo_list):
    print ('\nSTART', inspect.stack()[0][3])
    try:
        if glo_test_bool:
            print(inspect.stack()[0][3], 'in TEST MODE!')

        counter = 2
        stockInfo_request_success = []
        requests_should_retry = True
        attempts_counter = 0
        max_attempts = 2
        while attempts_counter != max_attempts and requests_should_retry:
            attempts_counter += 1
            list_of_stocks_failed = []
            for stock in stockInfo_list:
                sbNameshort = stock.get(mod_shared.glo_colName_sbNameshort)
                print (counter, ':' ,sbNameshort)
                counter += 1

                # get sb shortname (e.g., ANOT.ST)
                url_postfix = sbNameshort
                # add sb shortname (e.g., ANOT.ST) to sb base url (e.g., https://www.swedishbulls.com/SignalPage.aspx?lang=en&Ticker=) ->  https://www.swedishbulls.com/SignalPage.aspx?lang=en&Ticker=ANOT.ST
                url_sb = mod_shared.glo_sbBaseStockPageUrl + url_postfix

                try:
                    r = mod_shared.requests_retry_session().get(url_sb)
                except Exception as e:
                    list_of_stocks_failed.append(stock)
                    continue
                else:
                    url_response = r.url
                    if url_response.find('SignalPage') == -1:
                        print('NOT FOUND, skipping:', r.url)
                        continue

                    # shared soup for whole SB stock page
                    soup = BeautifulSoup(r.content, 'html.parser')

                    # Continue on next stock if stock page returned no list
                    rows_months_24 = soup.find_all(id=re.compile("MainContent_signalpagehistory_PatternHistory24_DXDataRow"))
                    if not rows_months_24: # page returned contained no stock list
                        print('page returned contained no stock list - skipping')
                        continue
                    
                    # Continue on next stock if stock's last signal is QUIT
                    signal_quit = rows_months_24[0].find_all('td')[2].get_text() # stock is QUIT
                    if signal_quit == 'QUIT':
                        print('Stock list last signal was', signal_quit ,'- skipping')
                        continue

                    percent_correct_6 = percent_correct_12 = percent_correct_24 = percent_average = value_average = price_last_close = ''

                    try:
                        price_last_close = float(soup.find(id='MainContent_lastpriceboxsub').get_text(strip=True).replace(',', ''))
                    except Exception as e:
                        print('price_last_close FAILED')
                        mod_shared.errorHandler(e)

                    soup_str_6 = 'MainContent_signalpagehistory_PatternHistory6_cell'
                    value_6 = getMultiplicationValue(soup_str_6, soup)
                    percent_correct_6 = getPercentCorrect(soup_str_6, soup)

                    soup_str_12 = 'MainContent_signalpagehistory_PatternHistory12_cell'
                    value_12 = getMultiplicationValue(soup_str_12, soup)
                    percent_correct_12 = getPercentCorrect(soup_str_12, soup)

                    soup_str_24 = 'MainContent_signalpagehistory_PatternHistory24_cell'
                    value_24 = getMultiplicationValue(soup_str_24, soup)
                    percent_correct_24 = getPercentCorrect(soup_str_24, soup)

                    # average percent
                    percent_list = [percent_correct_6, percent_correct_12, percent_correct_24]
                    percent_average = round(sum(percent_list)/len(percent_list),1)

                    # average value
                    value_list = [value_6, value_12, value_24]
                    value_average = int(sum(value_list)/len(value_list))

                    # get dates with signal with price
                    list_of_dicts_priceHistory = []
                    rows_months_24 = soup.find_all(id=re.compile("MainContent_signalpagehistory_PatternHistory24_DXDataRow"))
                    for stock_date in rows_months_24:
                        # date
                        date_history = stock_date.contents[1].get_text()
                        # price
                        price_history = stock_date.contents[2].get_text()
                        # signal
                        signal_history = stock_date.contents[3].get_text()

                        list_of_dicts_priceHistory.append({'date': date_history, 'price': price_history, 'signal': signal_history})

                    # buy percentage correct
                    rows_months_24 = soup.find_all(id=re.compile("MainContent_signalpagehistory_PatternHistory24_DXDataRow"))
                    array_length_24 = len(rows_months_24)
                    counter_buys = 0
                    counter_buys_uncheck = 0
                    for i in range(0,array_length_24-1):
                        srcName = rows_months_24[i].find_all('td')[3].img['src'].lower()
                        if srcName.find('boschecked') != -1: # signal result not yet confirmed
                            continue
                        signal = rows_months_24[i].find_all('td')[2].get_text()
                        # total buys
                        if signal == 'BUY':
                            counter_buys +=1
                        if signal == 'BUY' and srcName.find('uncheck') != -1: # "uncheck" spelling more reliable than "check"
                            counter_buys_uncheck += 1

                    counter_buys_check = counter_buys - counter_buys_uncheck
                    buys_correct_percent_24 = round(100*(float(counter_buys_check)/float(counter_buys)), 1)

                    # average buy percentage change and median value for success and failed results
                    buy_failed_change = []
                    buy_success_change = []
                    # get all stock rows of 24 months
                    rows_months_24 = soup.find_all(id=re.compile("MainContent_signalpagehistory_PatternHistory24_DXDataRow"))
                    array_length_24 = len(rows_months_24)
                    for i in range(0, array_length_24-1):
                        signal_confirmation_current = rows_months_24[i].find_all('td')[3].img['src'].lower()
                        if signal_confirmation_current.find('boschecked') != -1: # signal result not yet confirmed
                            continue
                        signal_confirmation_former = rows_months_24[i+1].find_all('td')[3].img['src'].lower() 
                        current_signal = rows_months_24[i].find_all('td')[2].get_text()
                        current_price = float(rows_months_24[i].find_all('td')[1].get_text().replace(',', ''))
                        former_signal = rows_months_24[i+1].find_all('td')[2].get_text()
                        former_price = float(rows_months_24[i+1].find_all('td')[1].get_text().replace(',', ''))
                        if current_signal == 'SHORT' or current_signal == 'SELL' and former_signal == 'BUY':
                            if signal_confirmation_former.find('uncheck') != -1: # failed buy
                                buy_failed_change.append(mod_shared.getPercentChange(former_price, current_price))
                            else:
                                buy_success_change.append(mod_shared.getPercentChange(former_price, current_price))

                    # the AVERAGE percentage change of failed buys (incorrect signals)
                    average_buy_failed_change = round(sum(buy_failed_change)/len(buy_failed_change), 2)
                    # the AVERAGE percentage change of successful buys (correct signals)
                    average_buy_success_change = round(sum(buy_success_change)/len(buy_success_change), 2)
                    # the MEDIAN percentage change of failed buys (incorrect signals)
                    median_buy_failed_change = round(median(buy_failed_change), 2)
                    # the MEDIAN percentage of successful buys (correct signals)
                    median_buy_success_change = round(median(buy_success_change), 2)

                    # median and average gain per buys (considering failed buys and cost of trade (e.g., courtage))
                    buys_correct_decimal_24 = buys_correct_percent_24/100
                    median_buyAndFail_keyValue = round(((median_buy_success_change - glo_costOfCourtage)*buys_correct_decimal_24) + ((median_buy_failed_change + glo_costOfCourtage)*(1-buys_correct_decimal_24)), 2)
                    average_buyAndFail_keyValue = round(((average_buy_success_change - glo_costOfCourtage)*buys_correct_decimal_24) + ((average_buy_failed_change + glo_costOfCourtage)*(1-buys_correct_decimal_24)), 2)

                    # total number of buys
                    buys_total = len(buy_success_change) + len(buy_failed_change)
                    
                    # current price compared to highest price percentage change
                    array_length_24 = len(rows_months_24)
                    price_high = 0
                    price_current = 0
                    for i in range(0, array_length_24-1):
                        if i == 0:
                            price_current = float(rows_months_24[i].find_all('td')[1].get_text().replace(',', ''))
                        temp_price = float(rows_months_24[i].find_all('td')[1].get_text().replace(',', ''))
                        if temp_price > price_high:
                            price_high = temp_price

                    price_highest_through_current = round((price_high/price_current), 2) # 4/2 = (2-1)*100

                    # MEDIAN and AVERAGE percent change between signals (neutral +- sign) (sign of volatility)
                    percent_change_list = []
                    percent_change_total = 0
                    for i in range(0, array_length_24-1):
                        price_end = float(rows_months_24[i].find_all('td')[1].get_text().replace(',', ''))
                        price_start = float(rows_months_24[i+1].find_all('td')[1].get_text().replace(',', ''))
                        price_change = abs(mod_shared.getPercentChange(price_start, price_end)) #start value, end value
                        percent_change_total += price_change
                        percent_change_list.append(price_change)

                    percent_change_price_average = round(percent_change_total/(array_length_24-1), 2)
                    percent_change_price_median = round(median(percent_change_list), 2)

                    list_of_tuples = [(mod_shared.glo_colName_url_sb, url_sb),
                        (mod_shared.glo_colName_price, price_last_close),
                        (mod_shared.glo_colName_6_percent, percent_correct_6),
                        (mod_shared.glo_colName_6_value, value_6),
                        (mod_shared.glo_colName_12_percent, percent_correct_12),
                        (mod_shared.glo_colName_12_value, value_12),
                        (mod_shared.glo_colName_24_percent, percent_correct_24),
                        (mod_shared.glo_colName_24_value, value_24),
                        (mod_shared.glo_colName_percentAverage, percent_average),
                        (mod_shared.glo_colName_valueAverage, value_average),
                        (mod_shared.glo_colName_buysTotal, buys_total),
                        (mod_shared.glo_colName_24_buys_correct_percent, buys_correct_percent_24),
                        (mod_shared.glo_colName_pricePercentChange_average, percent_change_price_average),
                        (mod_shared.glo_colName_pricePercentChange_median, percent_change_price_median),
                        (mod_shared.glo_colName_buyAverageFailedPerChange, average_buy_failed_change),
                        (mod_shared.glo_colName_buyMedianFailedPerChange, median_buy_failed_change),
                        (mod_shared.glo_colName_buyAverageSuccessPerChange, average_buy_success_change),
                        (mod_shared.glo_colName_buyMedianSuccessPerChange, median_buy_success_change),
                        (mod_shared.glo_colName_buyAndFailMedian_keyValue, median_buyAndFail_keyValue),
                        (mod_shared.glo_colName_buyAndFailAverage_keyValue, average_buyAndFail_keyValue),
                        (mod_shared.glo_colName_percentChange_highestThroughCurrent, price_highest_through_current),
                        (mod_shared.glo_colName_historySignalPrice, list_of_dicts_priceHistory)]

                    stock.update(OrderedDict(list_of_tuples))
                    stockInfo_request_success.append(stock)
           
            if list_of_stocks_failed and attempts_counter < max_attempts:
                print('\nstock url requests failed:')
                stock_counter=1
                for stock_failed in list_of_stocks_failed:
                    print(str(stock_counter)+': '+stock_failed.get(mod_shared.glo_colName_sbNameshort))
                    stock_counter += 1
                stockInfo_list = list(list_of_stocks_failed)
                print('\nRetrying...')
            else:
                requests_should_retry = False

        if list_of_stocks_failed:
            print('\nStocks failed after '+ str(max_attempts) +' - discarding')
            stock_counter=1
            body = []
            for stock_failed in list_of_stocks_failed:
                body.append(stock_failed.get(mod_shared.glo_colName_sbNameshort))
                print(str(stock_counter)+': '+stock_failed.get(mod_shared.glo_colName_sbNameshort))
                stock_counter += 1
            sbj = 'Failed stock requests inside '+inspect.stack()[0][3]
            mod_shared.sendEmail(sbj, body)

        return stockInfo_request_success
    except Exception as e:
        mod_shared.errorHandler(e)

def getStocksFromNn(stockInfo_list):
    print ('\nSTART', inspect.stack()[0][3])
    try:
        if glo_test_bool:
            print(inspect.stack()[0][3], 'in TEST MODE!')
        
        counter = 2
        stockInfo_request_success = []
        stocks_not_matched = []
        requests_should_retry = True
        attempts_counter = 0
        max_attempts = 2
        while attempts_counter <= max_attempts and requests_should_retry:
            attempts_counter += 1
            list_of_stockRequests_failed = []
            for stock in stockInfo_list:
                sbNameshort = stock.get(mod_shared.glo_colName_sbNameshort)
                print(counter,':',sbNameshort)
                counter += 1

                if not stock.get(mod_shared.glo_colName_url_sb):
                    print(mod_shared.glo_colName_url_sb, 'was None or empty - skipping')
                    continue

                # checking complimentary list
                if stock.get(mod_shared.glo_colName_compList):
                    url_stock = stock[mod_shared.glo_colName_url_nn]
                    list_of_tuples = getNnStockPageData(url_stock)
                    if list_of_tuples:
                        stock.update(OrderedDict(list_of_tuples))
                    # check for duplicates
                    elif not any(d[mod_shared.glo_colName_sbNameshort] == stock.get(mod_shared.glo_colName_sbNameshort) for d in list_of_stockRequests_failed):
                        list_of_stockRequests_failed.append(stock)
                        continue
                    # if failed getNnStockPageData and stock already added to list_of_stockRequests_failed - continue with next stock
                    else:
                        continue
                else:
                    # split on NOT [a-zA-Z0-9_] (letters, digits, and underscores). Example: SAGA-B.ST -> ['SAGA', 'B', 'ST']
                    sbNameshort_split_list = re.findall(r"[\w']+", sbNameshort)
                    
                    # remove last item. Example: ['SAGA', 'B', 'ST'] -> ['SAGA', 'B']
                    sbNameshort_split_list = sbNameshort_split_list[:-1]
                    
                    # join list with space for alternative sb->nnNameShort match (SB might be SAGA-B while NN SAGA B)
                    sb_nn_nameShort_match = " ".join(sbNameshort_split_list)
                    
                    # join list with a '+'-sign between words for query. exaple: ['SAGA', 'B'] -> SAGA+B
                    query = "+".join(sbNameshort_split_list)
                    
                    urlNn = 'https://www.nordnet.se'
                    urlNnSearch = 'https://www.nordnet.se/search/load.html'
                    payload = {
                    'query': query,
                    'type': 'instrument'
                    }
                    try:
                        # Initial stock search
                        r = mod_shared.requests_retry_session().post(urlNnSearch, data=payload)
                    except Exception as e:
                        if not any(d[mod_shared.glo_colName_sbNameshort] == stock.get(mod_shared.glo_colName_sbNameshort) for d in list_of_stockRequests_failed):
                            list_of_stockRequests_failed.append(stock)
                        continue
                    else:
                        soup = BeautifulSoup(r.content, 'html.parser') # active are placed in "share"
                        urlNnStock_rel_list = soup.find(id=re.compile('search-results-container')).find_all('div', class_='instrument-name') # all divs (containing a tags) in search result
                        if urlNnStock_rel_list:
                            stock_was_found = False
                            for i in range(0,len(urlNnStock_rel_list)):
                                url_stock = urlNn + urlNnStock_rel_list[i].a['href']
                                list_of_tuples = getNnStockPageData(url_stock)
                                if list_of_tuples:
                                    dict_temp = dict(list_of_tuples)
                                    if dict_temp.get(mod_shared.glo_colName_nameShortNordnet) == sb_nn_nameShort_match:
                                        stock.update(OrderedDict(list_of_tuples))
                                        stock_was_found = True
                                        break
                            if not stock_was_found:
                                list_of_stockRequests_failed.append(stock)

                # get intraday-closing price percent changes
                market_id = stock.get(mod_shared.glo_colName_market_id)
                identifier_id = stock.get(mod_shared.glo_colName_identifier_id)
                # if market_id and identifier_id was previously found 
                if market_id and identifier_id:
                    dateYesterdayStr = mod_shared.getDate_deltaToday_customFormat_str(-1, '%Y-%m-%d') # today's date only works when Nordnet has had time to updated historic figures
                    url = 'https://www.nordnet.se/graph/instrument/'+ market_id +'/'+identifier_id+'?from=1970-01-01&to='+dateYesterdayStr+'&fields=last,open,high,low,volume'
                    try:
                        r = mod_shared.requests_retry_session().get(url)
                    except Exception as e:
                        list_of_stockRequests_failed.append(stock)
                        continue
                    else:
                        soup = BeautifulSoup(r.content, 'html.parser') # active are placed in "share"
                        list_of_dicts_nn = json.loads(str(soup))
                        list_of_dicts_sb = stock.get(mod_shared.glo_colName_historySignalPrice)
                        
                        intraday_closing_buy_percent_changes = []
                        intraday_closing_sellAndShort_percent_changes = []

                        # for each signal in history from SB 
                        for dict_sb in list_of_dicts_sb:
                            # '%d.%m.%Y' -> '%Y-%m-%d'
                            date_sb = datetime.datetime.strptime(dict_sb.get(glo_sb_history_date), '%d.%m.%Y').strftime('%Y-%m-%d')
                            price_sb_str = dict_sb.get(glo_sb_history_price).replace(",", "")
                            price_sb = float(price_sb_str)
                            signal_sb = dict_sb.get(glo_sb_history_signal)
                            for dict_date_nn in list_of_dicts_nn:
                                # microsec -> sec + 1 (to ensure ends at correct side of date)
                                epoch_sec = int(dict_date_nn.get(glo_nn_history_time)/1000)+1
                                # epoch_sec -> 'YYYY-MM-DD'
                                date_nn = time.strftime('%Y-%m-%d', time.localtime(epoch_sec))
                                price_nn = dict_date_nn.get(glo_nn_history_closing)

                                # if dates of sb and nn match
                                if date_sb == date_nn:
                                    # positive result: end_value (closing price) is higher than start_value (intraday price)
                                    if dict_sb.get(glo_sb_history_signal) == 'BUY':
                                        percentChange = mod_shared.getPercentChange(price_sb, price_nn) # start value; end value
                                        intraday_closing_buy_percent_changes.append(percentChange)
                                    elif dict_sb.get(glo_sb_history_signal) == 'SELL' or dict_sb.get(glo_sb_history_signal) == 'SHORT':
                                        percentChange = mod_shared.getPercentChange(price_sb, price_nn) # start value; end value
                                        intraday_closing_sellAndShort_percent_changes.append(percentChange)

                        # delete data of historic prices after usage
                        stock.pop(mod_shared.glo_colName_historySignalPrice, None)

                        median_intraday_closing_sellAndShort = round(median(intraday_closing_sellAndShort_percent_changes),2)
                        average_intraday_closing_sellAndShort = round(sum(intraday_closing_sellAndShort_percent_changes)/float(len(intraday_closing_sellAndShort_percent_changes)), 2)
                        
                        median_intraday_closing_buy = round(median(intraday_closing_buy_percent_changes), 2)
                        average_intraday_closing_buy = round(sum(intraday_closing_buy_percent_changes)/float(len(intraday_closing_buy_percent_changes)), 2)
                        
                        sum_median_buyAndFailKeyValue_and_intraday_closing_sellAndShort = round(stock.get(mod_shared.glo_colName_buyAndFailMedian_keyValue) + median_intraday_closing_sellAndShort, 2)
                        sum_average_buyAndFailKeyValue_and_intraday_closing_sellAndShort = round(stock.get(mod_shared.glo_colName_buyAndFailAverage_keyValue) + average_intraday_closing_sellAndShort, 2)
                        
                        sum_median_buyAndFailKeyValue_and_intraday_closing_sellAndBuy = round(stock.get(mod_shared.glo_colName_buyAndFailMedian_keyValue) + median_intraday_closing_sellAndShort - median_intraday_closing_buy, 2)
                        sum_average_buyAndFailKeyValue_and_intraday_closing_sellAndBuy = round(stock.get(mod_shared.glo_colName_buyAndFailAverage_keyValue) + average_intraday_closing_sellAndShort - average_intraday_closing_buy, 2)

                        list_of_tuples = [(mod_shared.glo_colName_median_sell_intradayClosingChange_percent, median_intraday_closing_sellAndShort),
                            (mod_shared.glo_colName_average_sell_intradayClosingChange_percent, average_intraday_closing_sellAndShort),
                            (mod_shared.glo_colName_median_buy_intradayClosingChange_percent, median_intraday_closing_buy),
                            (mod_shared.glo_colName_average_buy_intradayClosingChange_percent, average_intraday_closing_buy),
                            (mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_sellIntradayClosingPercentChange, sum_median_buyAndFailKeyValue_and_intraday_closing_sellAndShort),
                            (mod_shared.glo_colName_average_buyAndFailKeyValue_and_average_sellIntradayClosingPercentChange, sum_average_buyAndFailKeyValue_and_intraday_closing_sellAndShort),
                            (mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange, sum_median_buyAndFailKeyValue_and_intraday_closing_sellAndBuy),
                            (mod_shared.glo_colName_average_buyAndFailKeyValue_and_average_buyAndSellIntradayClosingPercentChange, sum_average_buyAndFailKeyValue_and_intraday_closing_sellAndBuy)]

                        stock.update(OrderedDict(list_of_tuples))

                        stockInfo_request_success.append(stock)
                else:
                    if stock.get(mod_shared.glo_colName_sbNameshort) not in stocks_not_matched:
                    # if not any(d[mod_shared.glo_colName_sbNameshort] == stock.get(mod_shared.glo_colName_sbNameshort) for d in stocks_not_matched):
                        print('no Nordnet match for', stock.get(mod_shared.glo_colName_sbNameshort), 'with query:', query)
                        stocks_not_matched.append(stock.get(mod_shared.glo_colName_sbNameshort))
            
            if list_of_stockRequests_failed and attempts_counter < max_attempts:
                print('\nstock url requests failed:')
                stock_counter=1
                for stock_failed in list_of_stockRequests_failed:
                    print(str(stock_counter)+': '+stock_failed.get(mod_shared.glo_colName_sbNameshort))
                    stock_counter += 1
                stockInfo_list = list(list_of_stockRequests_failed)
                print('\nRetrying...')
            else:
                requests_should_retry = False

        if stocks_not_matched:
            print('\nstocks not matched on Nordnet:')
            pprint(stocks_not_matched)
            sbj = 'stocks not matched on Nordnet inside '+inspect.stack()[0][3]
            mod_shared.sendEmail(sbj, stocks_not_matched)

        if list_of_stockRequests_failed:
            print('\nStocks failed after '+ str(max_attempts) +' attempts - discarding')
            stock_counter=1
            body = []
            for stock_failed in list_of_stockRequests_failed:
                body.append(stock_failed.get(mod_shared.glo_colName_sbNameshort))
                print(str(stock_counter)+': '+stock_failed.get(mod_shared.glo_colName_sbNameshort))
                stock_counter += 1
            sbj = 'Failed stock requests inside '+inspect.stack()[0][3]
            mod_shared.sendEmail(sbj, body)

        return stockInfo_request_success
    except Exception as e:
        mod_shared.errorHandler(e)

def stringToFLoat(list_to_convert, list_of_key_exceptions):
    try:
        for row in list_to_convert:
            for key in row:
                if key not in list_of_key_exceptions:
                    try:
                        row[key] = float(row[key])
                    except ValueError:
                        pass
        return list_to_convert
    except Exception as e:
        mod_shared.errorHandler(e)   

def filterStocksToWatch(stockInfoUpdated_list):
    try:
        # Groups:
            # * 1: 
            # - name: 1_median_buyAndSellIntradayClosing_and_buy_medianCorrectAndFailKeyValue
            # - Conditions to select: buys_total: + 30; sort by SUM_BUYANDFAIL_MEDIAN_KEYVALUE_AND_MEDIAN_BUY_SELL_INTRADAY-CLOSING-CHANGE_PERCENT 
            # (high); select from value 1%
            # - Conditions to buy: Buy only if intraday-closing is less than MEDIAN_BUY_INTRADAY-CLOSING-CHANGE_PERCENT; 
            # (if multiple stocks fit selection, prioritize highest value or biggest diff in conditions above) 

            # * 2:
            # - name: 2_average_buyAndSellIntradayClosing_and_buy_averageCorrectAndFailKeyValue
            # - Conditions to select: buys_total: + 30; sort by SUM_BUYANDFAIL_AVERAGE_KEYVALUE_AND_AVERAGE_BUY_SELL_INTRADAY-CLOSING-CHANGE_PERCENT
            # (high); select from value 1%
            # - Conditions to buy: Buy only if intraday-closing is less than AVERAGE_BUY_INTRADAY-CLOSING-CHANGE_PERCENT; 
            # (if multiple stocks fit selection, prioritize highest value or biggest diff in conditions above 

        list_of_key_exceptions = [
            mod_shared.glo_colName_market_id,
            mod_shared.glo_colName_identifier_id
        ]
        stockInfoUpdated_list = stringToFLoat(stockInfoUpdated_list, list_of_key_exceptions)
        
        # --- GROUP1 ---
        # filter minimum amount of buys
        group_1_list = [d for d in stockInfoUpdated_list if d.get(mod_shared.glo_colName_buysTotal) >= 30]
        group_1_list = [d for d in group_1_list if d.get(mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange) >= 1]
        group_1_list = sorted(group_1_list, 
            key=lambda k: k[mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange], 
            reverse=True) # (list to sort; column to sort on; order)
        for dict_item in group_1_list:
            dict_item[mod_shared.glo_colName_stockToBuy_group] = mod_shared.glo_value_group_1

        print('\nGROUP 1')
        for row in group_1_list:
            print(row[mod_shared.glo_colName_sbNameshort],':', 
                row[mod_shared.glo_colName_buysTotal],':', 
                row[mod_shared.glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange], ':', 
                row[mod_shared.glo_colName_median_buy_intradayClosingChange_percent], ':', 
                row[mod_shared.glo_colName_stockToBuy_group])

        # # --- GROUP2 ---
            # group_2_list = [d for d in stockInfoUpdated_list if d.get(mod_shared.glo_colName_buysTotal) >= 30]
            # group_2_list = [d for d in group_2_list if d.get(mod_shared.glo_colName_average_buyAndFailKeyValue_and_average_buyAndSellIntradayClosingPercentChange) >= 0.5]
            # group_2_list = sorted(group_2_list, 
            #     key=lambda k: k[mod_shared.glo_colName_average_buyAndFailKeyValue_and_average_buyAndSellIntradayClosingPercentChange], 
            #     reverse=True) # (list to sort; column to sort on; order); only doing for estetics
            # for dict_item in group_2_list:
            #     dict_item[mod_shared.glo_colName_stockToBuy_group] = mod_shared.glo_value_group_2

            # print('\nGROUP 2')
            # for row in group_2_list:
            #     print(row[mod_shared.glo_colName_sbNameshort],':', 
            #         row[mod_shared.glo_colName_buysTotal],':', 
            #         row[mod_shared.glo_colName_average_buyAndFailKeyValue_and_average_buyAndSellIntradayClosingPercentChange], ':', 
            #         row[mod_shared.glo_colName_stockToBuy_group])

            # print('len group1:', len(group_1_list))
            # print('len group2:', len(group_2_list))

        # merge lists 
        stocksToBuy_list = group_1_list
        # stocksToBuy_list = group_1_list + group_2_list # merging

        # stocksToBuy_list = list(unique_everseen(stocksToBuy_list)) # remove duplicates

        return stocksToBuy_list
    except Exception as e:
        mod_shared.errorHandler(e)    

def deleteKeyValuesFromOrderedDict(list_to_update, list_of_keys):
    try:
        for row1 in list_to_update:
            for keyRow in list_of_keys:
                del row1[keyRow]
        return list_to_update
    except Exception as e:
        mod_shared.errorHandler(e)  

def addKeyToOrderedDict(list_to_update, list_of_keys):
    try:
        for row1 in list_to_update:
            for keyRow in list_of_keys:
                row1[keyRow] = ''
        return list_to_update
    except Exception as e:
        mod_shared.errorHandler(e)      

def setAllStockLists():
    print ('\nSTART', inspect.stack()[0][3])
    try:
        if glo_runGetStocksFromSb_bool:
            if glo_test_bool:
                print(inspect.stack()[0][3], 'in TEST MODE!')
                stockInfo_list = mod_shared.getListFromFile(mod_shared.path_input_createList+mod_shared.path_input_test, glo_stockInfo_test_file)
            else:
                stockInfo_list = mod_shared.getListFromFile(mod_shared.path_input_createList,  mod_shared.glo_stockInfo_file_raw)
            print('stockInfo_list:', len(stockInfo_list))
            
            blacklist = mod_shared.getListFromFile(mod_shared.path_input_createList, mod_shared.glo_blacklist_file)
            print('blacklist:', len(blacklist))

            # remove rows blacklist from stockInfo list
            stockInfo_list = [dict_item for dict_item in stockInfo_list if dict_item not in blacklist]
            print('stockInfo_list after blacklist removal:', len(stockInfo_list))

            stockInfo_list = getStocksFromSb(stockInfo_list)

            if glo_test_bool:
                mod_shared.writeListToCsvFile(stockInfo_list, mod_shared.path_input_createList+mod_shared.path_input_test + glo_test_str+mod_shared.glo_stockAfterSb_file_updated)
            else:
                mod_shared.writeListToCsvFile(stockInfo_list, mod_shared.path_input_createList + mod_shared.glo_stockAfterSb_file_updated)

        if not glo_runGetStocksFromSb_bool:
            print('glo_runGetStocksFromSb_bool was', glo_runGetStocksFromSb_bool, '- NOT running getStocksFromSb')
            if glo_test_bool:
                stockInfo_list = mod_shared.getListFromFile(mod_shared.path_input_createList+mod_shared.path_input_test, glo_test_str+mod_shared.glo_stockAfterSb_file_updated)
            else:
                stockInfo_list = mod_shared.getListFromFile(mod_shared.path_input_createList, mod_shared.glo_stockAfterSb_file_updated)

            # convert strings to float
            stockInfo_list = stringToFLoat(stockInfo_list, [])
            # convert string list to list
            for stock in stockInfo_list:
                if stock[mod_shared.glo_colName_historySignalPrice]:
                    stock[mod_shared.glo_colName_historySignalPrice] = ast.literal_eval(stock.get(mod_shared.glo_colName_historySignalPrice))

        complimentary_list = mod_shared.getListFromFile(mod_shared.path_input_createList, mod_shared.glo_complimentary_file)

        # updating items from complimentary list to stockInfo_list
        list_of_key_selectors = [mod_shared.glo_colName_sbNameshort]
        list_of_key_overwriters = list(mod_shared.glo_complimentary_colNames.keys())
        stockInfo_list = mod_shared.updateListFromListByKeys(stockInfo_list,
            complimentary_list,
            list_of_key_selectors, 
            list_of_key_overwriters) # list to update, list to update from
        
        stockInfo_list = getStocksFromNn(stockInfo_list)
        if stockInfo_list:
            stockInfo_list = mod_shared.setListKeys(stockInfo_list, mod_shared.glo_stockInfoUpdated_colNames)
            if glo_test_bool:
                mod_shared.writeListToCsvFile(stockInfo_list, mod_shared.path_input_createList+mod_shared.path_input_test + glo_test_str+mod_shared.glo_stockInfoUpdated_file)
            else:
                mod_shared.writeListToCsvFile(stockInfo_list, mod_shared.path_input_createList + mod_shared.glo_stockInfoUpdated_file)
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        print('END', inspect.stack()[0][3], '\n')

def setStockToBuyList():
    print ('\nSTART', inspect.stack()[0][3])
    try:
        if glo_test_bool:
            print(inspect.stack()[0][3], 'in TEST MODE!')
            stockInfoUpdated_list = mod_shared.getListFromFile(mod_shared.path_input_createList+mod_shared.path_input_test, glo_test_str+mod_shared.glo_stockInfoUpdated_file)
        else:
            stockInfoUpdated_list = mod_shared.getListFromFile(mod_shared.path_input_createList, mod_shared.glo_stockInfoUpdated_file)
    
        if stockInfoUpdated_list:
            stocksToBuy_list = filterStocksToWatch(stockInfoUpdated_list)
            # BP()

            # stockToBuy_allData_list = mod_shared.setListKeys(stocksToBuy_list, mod_shared.glo_stockToBuy_allData_colNames)
            stocksToBuy_list = mod_shared.setListKeys(stocksToBuy_list, mod_shared.glo_stockToBuy_colNames)

            if glo_test_bool:
                # mod_shared.writeListToCsvFile(stockToBuy_allData_list, mod_shared.path_input_createList + glo_test_str+mod_shared.glo_stockToBuy_allData_file)
                mod_shared.writeListToCsvFile(stocksToBuy_list, mod_shared.path_input_createList+mod_shared.path_input_test + glo_test_str+mod_shared.glo_stockToBuy_file)
            else:
                # mod_shared.writeListToCsvFile(stockToBuy_allData_list, mod_shared.path_input_main+mod_shared.glo_stockToBuy_allData_file)
                mod_shared.writeListToCsvFile(stocksToBuy_list, mod_shared.path_input_main+mod_shared.glo_stockToBuy_file)
    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        print('END', inspect.stack()[0][3], '\n')

def main():
    try:
        if glo_runSetAllStockLists_bool:
            setAllStockLists()
        time.sleep(3)
        setStockToBuyList()
    except Exception as e:
        mod_shared.errorHandler(e)

# only run when script explicitly called
if __name__ == "__main__":
   main()

# todo
# - handle error in getStocksFromNn: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
# - make it possible to not having to start over getStocksFromSb and getStocksFromNn from beginning in case of error/fail