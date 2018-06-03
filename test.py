import shared as mod_shared
import create_stock_lists as mod_list
from pdb import set_trace as BP
from bs4 import BeautifulSoup
import json
import time
import datetime
import inspect
import collections
from statistics import median
from pprint import pprint
from pprint import pformat
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import os    

glo_file_this = os.path.basename(__file__)
glo_file_orderStatistics = 'order-statistics.csv'
glo_file_orderStatistics_test = 'test-order-statistics.csv'
glo_file_noFile = 'no-file.csv'

glo_test = True

def getDailyOrderStatistics():
    try:
        trade_list = []
        if glo_test:
            temp_list = [
            {'NAMESHORT_NORDNET': 'SALT B',
              'TRADE_PRICE': 10,
              'TRADE_TIME': '2018-05-19 16:37:37',
              'TRADE_TYPE': 'SELL'},
            {'NAMESHORT_NORDNET': 'COPP B',
              'TRADE_PRICE': 5,
              'TRADE_TIME': '2018-05-19 16:22:52',
              'TRADE_TYPE': 'SELL'},
            {'NAMESHORT_NORDNET': 'STAR A',
              'TRADE_PRICE': 100,
              'TRADE_TIME': '2018-05-19 16:22:52',
              'TRADE_TYPE': 'SELL'}
              ]
            for dict_item in temp_list:
                dict_item[mod_shared.glo_colName_trade_time] = dict_item.get(mod_shared.glo_colName_trade_time).split()[0]
                order_of_keys = list(dict_item.keys()) # keys will not retain order, but should not matter.
                trade_list.append(mod_shared.getOrderedDictFromDict(dict_item, order_of_keys))
        else: 
            r, header, s = mod_shared.nordnetLogin() # login to nordnet

            soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/ajax/trade/orders/auto?accountNumber=18272500', headers=mod_shared.glo_urlHeader).content, 'html.parser') # active are placed in "share"
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

                    trade_list.append(dict_temp)
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
        print ("ERROR in file", glo_file_this, 'and function' ,inspect.stack()[0][3], ':', str(e))
        # mod_shared.writeErrorLog(inspect.stack()[0][3], str(e))
    else:
        return trade_list

def getUpdatedOrderStatistics(orderStat_list, trade_list):
    try:
        # calc percent change
        for dict_trade in trade_list:
            # get all stock dicts which matches a stock name in trade_list and where it is SELL and where the other stock is BUY
            onlyOneStockName_list = [item for item in orderStat_list if dict_trade.get('NAMESHORT_NORDNET') in item['NAMESHORT_NORDNET'] and 
            'BUY' in item['TRADE_TYPE'] and
            'SELL' in dict_trade.get('TRADE_TYPE')]
            if onlyOneStockName_list:
                # get the stock dict with the highest date
                onlyOneStockName_maxDate_dict = max(onlyOneStockName_list, key=lambda item:item['TRADE_TIME'])
                # calc percent change
                start_value = float(onlyOneStockName_maxDate_dict.get(mod_shared.glo_colName_trade_price))
                end_value = dict_trade.get(mod_shared.glo_colName_trade_price)
                percentage_change = round(mod_shared.getPercentChange(start_value, end_value), 2)
                dict_trade[mod_shared.glo_colName_trade_percentChange] = percentage_change

        for dict_trade in trade_list:
            orderStat_list.append(dict_trade)
    except Exception as e:
        print ("ERROR in file", glo_file_this, 'and function' ,inspect.stack()[0][3], ':', str(e))

    else:
        return orderStat_list


trade_list = getDailyOrderStatistics()
if trade_list:
    # safer than setListKeys which deletes keys. This requires columns to be deleted manually from order-statistics.csv
    trade_list = mod_shared.addKeysNotExisting(trade_list, mod_shared.glo_orderStatistics_colNames) 
    # set keys already existing in trade_list to values of keys from stockToBuy_allData
    stockToBuy_allData_list = mod_shared.getListFromFile(mod_shared.path_input_main, mod_shared.glo_stockToBuy_allData_file)
    list_of_key_selectors = [mod_shared.glo_colName_nameShortNordnet]
    trade_list = mod_shared.updateListFromListBy_existingKeys(trade_list,
        stockToBuy_allData_list,
        list_of_key_selectors) # list to update, list to update from
    # BP()

    # orderStat_list = mod_shared.getListFromFile(mod_shared.path_output, glo_file_noFile)

    orderStat_list = mod_shared.getListFromFile(mod_shared.path_output, glo_file_orderStatistics)
    if orderStat_list != False: # Important! Keep as False as longs as getListFromFile returns this for files not found.
        org_len = len(orderStat_list)
        orderStat_list_updated = getUpdatedOrderStatistics(orderStat_list, trade_list)
        rev_len = len(orderStat_list_updated)
        if rev_len > org_len:
            mod_shared.writeListToCsvFile(orderStat_list_updated, mod_shared.path_output + glo_file_orderStatistics)
        else:
            print('Something might have gone wrong in', inspect.stack()[0][3], ': New', glo_file_orderStatistics, 'did not have more rows than old. No changes made.')
    else:
        print(glo_file_orderStatistics, 'did not exist. Creating new file with trade_list')
        mod_shared.writeListToCsvFile(trade_list, mod_shared.path_output + glo_file_orderStatistics)

# def test():
#     try:
#         test = 'shit'
#         [][2]
#     except Exception as e:
#         # print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
#         # print ('Error on line', format(sys.exc_info()[-1].tb_lineno), ':', str(e))
#         # print ('\nERROR: \n\tFile:', glo_file_this, '\n\tFunction:', inspect.stack()[0][3], '\n\tLine:', format(sys.exc_info()[-1].tb_lineno), '\n\tError:', str(e), '\n')
#         print ('\nERROR: \n\tFile:', glo_file_this, '\n\tFunction:', inspect.stack()[0][3], '\n\tLine:', format(sys.exc_info()[-1].tb_lineno), '\n\tError:', str(e), '\n')

# test()


# # def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
# def requests_retry_session(retries=3, backoff_factor=0.3, session=None):
#     try:
#         session = session or requests.Session()
#         retry = Retry(
#             total=retries,
#             read=retries,
#             connect=retries,
#             backoff_factor=backoff_factor,
#             # status_forcelist=status_forcelist,
#         )
#         adapter = HTTPAdapter(max_retries=retry)
#         session.mount('http://', adapter)
#         session.mount('https://', adapter)
#         return session
        
#     except Exception as e:
#         print ('ERROR in function' ,inspect.stack()[0][3], ':', str(e))

# try:
#     url1 = 'http://localhost:9999'
#     url2 = 'https://www.swedishbulls.com/Default.aspx?lang=en'
#     urls = [url1, url2]
#     list_of_stocks_failed = []
#     stock_requests_retry = False
#     while urls:
#         list_of_stocks_to_retry = []
#         for url in urls:
#             t0 = time.time()
#             try:
#                 print('\nrequesting', url)
#                 response = requests_retry_session().get(url)
#             except Exception as x:
#                 print('It failed :(', str(x))
#                 if stock_requests_retry:
#                     list_of_stocks_failed.append(url)
#                     pass
#                 else:
#                     list_of_stocks_to_retry.append(url)
#                 continue
#             else:
#                 print('It eventually worked', response.status_code)
#             finally:
#                 t1 = time.time()
#                 print('Took', t1 - t0, 'seconds')
#         if list_of_stocks_to_retry:
#             print('\nstock url requests failed:')
#             pprint(list_of_stocks_to_retry)
#             pprint('trying one more time')
#             urls = list(list_of_stocks_to_retry)
#             stock_requests_retry = True
#         else:
#             urls = False

#     print('\nurls still failed after retry:')
#     pprint(list_of_stocks_failed)
#     # sendEmail

# except Exception as x:
#     print('outer Exception')
#     pass


        #     pprint(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_sec)))
        #     pprint(dict_date.get('time'))
        #     BP()
        #     pass
        # epoch_sec = int(epoch_sec/1000)

# {'high': 0.54,
#   'last': 0.515,
#   'low': 0.515,
#   'open': 0.54,
#   'time': 1487286000000,
#   'volume': 35935.0},

    # time.strftime('%Y-%m-%d', time.localtime(epoch_sec))
    # soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/ajax/trade/orders/auto?accountNumber=18272500', headers=mod_shared.glo_urlHeader).content, 'html.parser') # active are placed in "share"
    # newList = newDict.get('share')
    
    # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))

    # 13.04.2018  
    # 0.6920  
    # SHORT

# (median_buy_success_change - glo_costOfBuy)*buys_correct_decimal_24
# + 
# (median_buy_failed_change + glo_costOfBuy)*(1-buys_correct_decimal_24)


# (median_buy_success_change - x)*y + (median_buy_failed_change + x)*(-y+1)

# <->
# (y * (median_buy_success_change - x)*1) + (-y(median_buy_failed_change + x)*1

# <->
# y ((median_buy_success_change - x) + (-(median_buy_failed_change + x)) )

# yx (median_buy_success_change -1 ) + (-median_buy_failed_change)