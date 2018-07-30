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
import math

glo_file_this = os.path.basename(__file__)

# START print methods-------------

# def cpr(str):
#     """Returns the current line number in our program."""
#     line = inspect.currentframe().f_back.f_lineno
#     return print('\t{}: {}'.format(line, str))

# cpr('some shitty output a´la kuk')

# print('we are back')
# # START file modification time -------------

# ts_str = os.path.getmtime(src_path_and_file)
# # convert ts_str to date and time string
# time_lastModification = mod_shared.getDateFromTimestamp(int(ts_str), '%Y-%m-%d %H-%M')
# extraString = '-backup {}'.format(time_lastModification)
# dest_path_and_file = mod_shared.path_base+mod_shared.path_input_main+mod_shared.glo_stockToBuy_file_noExtension+extraString+'.csv'

# START copy file-------------

from shutil import copyfile
import glob

# copyfile(mod_shared.path_base+mod_shared.path_input_main+mod_shared.glo_stockToBuy_file, '{}{}{}_backup'.format(mod_shared.path_base+mod_shared.path_input_main+mod_shared.glo_stockToBuy_file))
src_path_and_file = mod_shared.path_base+mod_shared.path_input_main+mod_shared.glo_stockToBuy_backup_noExtension_file
BP()


# dest_path_and_file = mod_shared.path_base+mod_shared.path_input_main+mod_shared.glo_stockToBuy_file_noExtension+'_backup.csv'
# file_exists = os.path.isfile(src_path_and_file)
# if file_exists:
#     print('making copy of: '.format(src_path_and_file))
#     copyfile(src_path_and_file, dest_path_and_file)
# else:
#     print('no file existing: {}'.format(src_path_and_file))
#     print('action: no backup copy made')



# START evaluating selling price change-------------
# import decimal
# from operator import itemgetter

# def formatNnStockPriceForSell_rev(nn_price_str, sellDecimalSubtraction_float):
#     try:
#         nn_price_float_org = float(nn_price_str)
#         nn_price_float_rev = nn_price_float_org * (1-sellDecimalSubtraction_float)

#         if 20 <= nn_price_float_rev:
#             # print('20 <= nn_price_float_rev')
#             decimals = 0
#             # print('decimals: {}'.format(decimals))
#         elif 5 <= nn_price_float_rev < 20:
#             # print('5 <= nn_price_float_rev < 20')
#             decimals = 1
#             # print('decimals: {}'.format(decimals))
#         elif 0.2 <= nn_price_float_rev < 5:
#             # print('5 <= nn_price_float_rev < 20')
#             decimals = 2
#             # print('decimals: {}'.format(decimals))
#         elif nn_price_float_rev < 0.2:
#             # print('5 <= nn_price_float_rev < 20')
#             decimals = 3
#             # print('decimals: {}'.format(decimals))

#         if decimals == 0:
#             high = int(math.ceil(nn_price_float_rev*pow(10,decimals))/pow(10,decimals))
#             low = int(math.floor(nn_price_float_rev*pow(10,decimals))/pow(10,decimals))
#             if mod_shared.getPercentChange(nn_price_float_org, low) > -(1*mod_shared.glo_sellPercentageSubtraction):
#                 return str(low)
#             else:
#                 return str(high)
#             # return str(int(math.ceil(nn_price_float*pow(10,decimals))/pow(10,decimals)))
#         else:
#             high = math.ceil(nn_price_float_rev*pow(10,decimals))/pow(10,decimals)
#             low = math.floor(nn_price_float_rev*pow(10,decimals))/pow(10,decimals)
#             if mod_shared.getPercentChange(nn_price_float_org, low) > -(1*mod_shared.glo_sellPercentageSubtraction):
#                 return str(low)
#             else:
#                 return str(high)

#             # return str(math.ceil(nn_price_float*pow(10,decimals))/pow(10,decimals))
#     except Exception as e:
#         mod_shared.errorHandler(e)

# def frange(start, stop, step):
#     i = start
#     while i < stop:
#         yield i
#         i += step

# result_list = []
# counter = 0
# counter_break = 100
# counter_bool = False
# start = 20
# end = 1001
# step = 0.1
# # mod_shared.glo_decimals_20
# for i in frange (start, end, step):

#     if counter_bool and counter >= counter_break:
#         break
#     else:
#         decimal_int = abs(decimal.Decimal(str(step)).as_tuple().exponent)
#         # to prevent long, weired values
#         stockPrice_begin = round(i, decimal_int)
#         print(stockPrice_begin)
#         sellDecimalSubtraction_float = mod_shared.getDecimalFromPercentage(mod_shared.glo_sellPercentageSubtraction)

#         stockPrice_end = formatNnStockPriceForSell_rev(str(stockPrice_begin), sellDecimalSubtraction_float)
#         stockPrice_perChange = round(mod_shared.getPercentChange(float(stockPrice_begin), float(stockPrice_end)), 2)
        
#         # print('{}:\t {}:\t {}'.format(stockPrice_begin, stockPrice_end, stockPrice_perChange))

#         result_dict = {'stockPrice_begin':stockPrice_begin, 'stockPrice_end': stockPrice_end, 'stockPrice_perChange': stockPrice_perChange}
#         # print(result_dict)
#         result_list.append(result_dict)

#         counter += 1

# # for dict_result in result_list:
# #     print(dict_result)

# # print('\n')
# print('DECENDING')
# result_list_perChange_decending = sorted(result_list, key=itemgetter('stockPrice_perChange'), reverse=True)
# range_stop = 30
# # # for dict_result in result_list_perChange_decending:
# # #     print(dict_result)
# for i in range (0, range_stop):
#     print(result_list_perChange_decending[i])

# print('\n')
# print('ACENDING')
# result_list_perChange_acending = sorted(result_list, key=itemgetter('stockPrice_perChange'))
# # for dict_result in result_list_perChange_acending:
# #     print(dict_result)
# range_stop = 30

# for i in range (0, range_stop):
#     print(result_list_perChange_acending[i])

# print(result_list)

# START testing headers -----------------------------------------------

# s = requests.session()

# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
# r = s.get('http://1337x.to/search/ufc+225/1/', headers=header)
# if r.status_code != 200:
#     print('FAIL')
#     print(r.status_code)

# soup = BeautifulSoup(r.content, 'html.parser')
# print(soup)
# BP()

# END testing headers -----------------------------------------------



# start True/False --------------------------------

# def isStockActive():
#     return False


# def isStockActiveTemp():
#     return True

# if not isStockActive() and not isStockActiveTemp():
#     print('TRUE')
# else:
#     print('False')

# END True/False --------------------------------


# start rnd --------------------------------------

# #float number; fraction number (e.g., 0.1, 0.2 etc); decimals; down if no argument, up if empty str ('')
# def rnd(n,f,prec,direction=''): 
#     if direction=='down':
#         if prec==0:
#             return str(int(n))
#         return str(round(n-math.fmod(n,f),prec))
#     elif direction=='up':
#         if prec==0:
#             return str(int(round(n)))
#         n+=f
#         return str(round(n-math.fmod(n,f),prec))
#     else:
#         n1=int(n) if prec==0 else round(n-math.fmod(n,f),prec)
#         n2=float(int(round(n))) if prec==0 else round((n+f)-math.fmod((n+f),f),prec)
#         if isinstance(n1, int):
#             return str(int(min((n1,n2), key=lambda e: math.fabs(e-n))))
#         else:
#             return str(min((n1,n2), key=lambda e: math.fabs(e-n)))


# def rnd2(n,f,prec):
#     n1=int(n) if prec==0 else round(n-math.fmod(n,f),prec)
#     n2=float(int(round(n))) if prec==0 else round((n+f)-math.fmod((n+f),f),prec)
#     if isinstance(n1, int):
#         return str(int(min((n1,n2), key=lambda e: math.fabs(e-n))))
#     else:
#         return str(min((n1,n2), key=lambda e: math.fabs(e-n)))

# plus500 = 501.59492
# plus200 = 210.3
# plus100 = 105.89584929
# plus50 = 55.57829
# plus20 = 22.340021
# plus10 = 10.109
# plus5 = 5.758492
# plus2 = 2.4541
# plus1 = 1.003235
# plus05 = 0.552234
# plus02 = 0.23455
# plus01 = 0.159902
# plus00 = 0.0012331

# #float number; fraction number (e.g., 0.1, 0.2 etc); decimals; down if no argument, up if empty str ('')
# print('plus500 Original:{}'.format(plus500))
# print('up: {}'.format(rnd(plus500, 1,0,'up')))
# print('down: {}'.format(rnd(plus500, 1,0,'down')))
# print('closest: {}'.format(rnd(plus500, 1,0,'closest')))

# print('\nplus200, up:{}'.format(plus200))
# print(rnd(plus200, 0.5,1,'up'))
# print('plus200, down:{}'.format(plus200))
# print(rnd(plus200, 0.5,1,'down'))
# print(rnd(plus200, 0.5,1))

# print('\nplus100, up:{}'.format(plus100))
# print(rnd(plus100, 0.2,1,'up'))
# print('plus100, down:{}'.format(plus100))
# print(rnd(plus100, 0.2,1,'down'))
# print(rnd(plus100, 0.2,1))

# print('\nplus50, up:{}'.format(plus50))
# print(rnd(plus50, 0.1,1,'up'))
# print('plus50, down:{}'.format(plus50))
# print(rnd(plus50, 0.1,1,'down'))
# print(rnd(plus50, 0.1,1))

# print('\nplus20, up:{}'.format(plus20))
# print(rnd(plus20, 0.05,2,'up'))
# print('plus20, down:{}'.format(plus20))
# print(rnd(plus20, 0.05,2,'down'))
# print(rnd(plus20, 0.05,2))

# print('\nplus10, up:{}'.format(plus10))
# print(rnd(plus10, 0.02,2,'up'))
# print('plus10, down:{}'.format(plus10))
# print(rnd(plus10, 0.02,2,'down'))
# print(rnd(plus10, 0.02,2))

# print('\nplus5, up:{}'.format(plus5))
# print(rnd(plus5, 0.01,2,'up'))
# print('plus5, down:{}'.format(plus5))
# print(rnd(plus5, 0.01,2,'down'))
# print(rnd(plus5, 0.01,2))

# print('\nplus2, up:{}'.format(plus2))
# print(rnd(plus2, 0.005,3,'up'))
# print('plus2, down:{}'.format(plus2))
# print(rnd(plus2, 0.005,3,'down'))
# print(rnd(plus2, 0.005,3))

# print('\nplus1, up:{}'.format(plus1))
# print(rnd(plus1, 0.002,3,'up'))
# print('plus1, down:{}'.format(plus1))
# print(rnd(plus1, 0.002,3,'down'))
# print(rnd(plus1, 0.002,3))

# print('\nplus05, up:{}'.format(plus05))
# print(rnd(plus05, 0.001,3,'up'))
# print('plus05, down:{}'.format(plus05))
# print(rnd(plus05, 0.001,3,'down'))
# print(rnd(plus05, 0.001,3))

# print('\nplus02, up:{}'.format(plus02))
# print(rnd(plus02, 0.0005,4,'up'))
# print('plus02, down:{}'.format(plus02))
# print(rnd(plus02, 0.0005,4,'down'))
# print(rnd(plus02, 0.0005,4))

# print('\nplus01, up:{}'.format(plus01))
# print(rnd(plus01, 0.0002,4,'up'))
# print('plus01, down:{}'.format(plus01))
# print(rnd(plus01, 0.0002,4,'down'))
# print(rnd(plus01, 0.0002,4))

# print('\nplus00, up:{}'.format(plus00))
# print(rnd(plus00, 0.0001,4,'up'))
# print('plus00, down:{}'.format(plus00))
# print(rnd(plus00, 0.0001,4,'down'))
# print(rnd(plus00, 0.0001,4))

#         # price rules nordnet
#         # - +500: 0 decimals (whole crowns) (e.g., 501; 502)
#         # - +200: 1 decimals (0.5) (e.g., 200.5; 201)
#         # - +100: 1 decimals (0.2) (e.g., 100.2; 100.4)
#         # - +50: 1 decimals (0.1) (e.g., 50.1; 50.2)
#         # - +20: 2 decimals (0.05) (e.g., 20.05; 20.10)
#         # - +10: 2 decimals (0.02) (e.g., 10.02; 10.04)
#         # - +5: 2 decimals (0.01) (e.g., 5.01; 5.02)
#         # - +2: 3 decimals (0.005) (e.g., 2.005; 2.010)
#         # - +1: 3 decimals (0.002) (e.g., 1.002; 1.004)
#         # - +0.5: 3 decimals (0.001) (e.g., 0.501; 0.502)
#         # - +0.2: 4 decimals (0.0005) (e.g., 0.2005; 0.2010)
#         # - +0.1: 4 decimals (0.0002) (e.g., 0.1002; 0.1004)
#         # - +0.0: 4 decimals (0.0001) (e.g., 0.0001; 0.0002)


# end rnd --------------------------------------

# glo_file_orderStatistics = 'order-statistics.csv'
# glo_file_orderStatistics_test = 'test-order-statistics.csv'
# glo_file_noFile = 'no-file.csv'

# glo_test = True

# def getDailyOrderStatistics():
#     try:
#         trade_list = []
#         if glo_test:
#             temp_list = [
#             {'NAMESHORT_NORDNET': 'SALT B',
#               'TRADE_PRICE': 10,
#               'TRADE_TIME': '2018-05-19 16:37:37',
#               'TRADE_TYPE': 'SELL'},
#             {'NAMESHORT_NORDNET': 'COPP B',
#               'TRADE_PRICE': 5,
#               'TRADE_TIME': '2018-05-19 16:22:52',
#               'TRADE_TYPE': 'SELL'},
#             {'NAMESHORT_NORDNET': 'STAR A',
#               'TRADE_PRICE': 100,
#               'TRADE_TIME': '2018-05-19 16:22:52',
#               'TRADE_TYPE': 'SELL'}
#               ]
#             for dict_item in temp_list:
#                 dict_item[mod_shared.glo_colName_trade_time] = dict_item.get(mod_shared.glo_colName_trade_time).split()[0]
#                 order_of_keys = list(dict_item.keys()) # keys will not retain order, but should not matter.
#                 trade_list.append(mod_shared.getOrderedDictFromDict(dict_item, order_of_keys))
#         else: 
#             r, header, s = mod_shared.nordnetLogin() # login to nordnet

#             soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/ajax/trade/orders/auto?accountNumber=18272500', headers=mod_shared.glo_urlHeader_userAgent).content, 'html.parser') # active are placed in "share"
#             newDict = json.loads(str(soup))
#             closedTrade_list = newDict.get('trade')
#             if closedTrade_list:
#                 for dict_item in closedTrade_list:
#                     dict_temp = OrderedDict()
#                     dict_temp[mod_shared.glo_colName_nameShortNordnet] = dict_item.get('shortName')
#                     dict_temp[mod_shared.glo_colName_trade_price] = str(dict_item.get('price')) # ex: 0.59 (int) -> '0.59'
#                     dict_temp[mod_shared.glo_colName_trade_volume] = str(dict_item.get('volume')) # ex: 2 (int) -> '2'
#                     dict_temp[mod_shared.glo_colName_trade_time] = dict_item.get('time') # ex: '2018-05-17 16:22:52'
#                     # remove time
#                     dict_temp[mod_shared.glo_colName_trade_time] = dict_temp.get(mod_shared.glo_colName_trade_time).split()[0] # ex: '2018-05-17'
#                     dict_temp[mod_shared.glo_colName_trade_type] = dict_item.get('type') # ex: 'Köpt' or 'Sålt'
                    
#                     if dict_temp.get(mod_shared.glo_colName_trade_type) == 'Köpt':
#                         dict_temp[mod_shared.glo_colName_trade_type] = 'BUY'
#                     else:
#                         dict_temp[mod_shared.glo_colName_trade_type] = 'SELL'

#                     trade_list.append(dict_temp)
#             else:
#                 print('No new order found in ' + inspect.stack()[0][3])
#                 return False
#                     # dict_item contains
#                         # {'identifier': '108026',
#                         #  'market': 'NasdaqOMX Stockholm',
#                         #  'marketplace': '11',
#                         #  'name': 'Savosolar Plc',
#                         #  'orderId': '138749253',
#                         #  'price': 0.59,
#                         #  'priceText': '0,59 SEK',
#                         #  'shortName': 'SAVOS',
#                         #  'time': '2018-05-17 16:22:52',
#                         #  'timeText': '16:22:52',
#                         #  'type': 'Köpt',
#                         #  'volume': 1,
#                         #  'volumeText': '1'}

#     except Exception as e:
#         print ("ERROR in file", glo_file_this, 'and function' ,inspect.stack()[0][3], ':', str(e))
#         # mod_shared.writeErrorLog(inspect.stack()[0][3], str(e))
#     else:
#         return trade_list

# def getUpdatedOrderStatistics(orderStat_list, trade_list):
#     try:
#         # calc percent change
#         for dict_trade in trade_list:
#             # get all stock dicts which matches a stock name in trade_list and where it is SELL and where the other stock is BUY
#             onlyOneStockName_list = [item for item in orderStat_list if dict_trade.get('NAMESHORT_NORDNET') in item['NAMESHORT_NORDNET'] and 
#             'BUY' in item['TRADE_TYPE'] and
#             'SELL' in dict_trade.get('TRADE_TYPE')]
#             if onlyOneStockName_list:
#                 # get the stock dict with the highest date
#                 onlyOneStockName_maxDate_dict = max(onlyOneStockName_list, key=lambda item:item['TRADE_TIME'])
#                 # calc percent change
#                 start_value = float(onlyOneStockName_maxDate_dict.get(mod_shared.glo_colName_trade_price))
#                 end_value = dict_trade.get(mod_shared.glo_colName_trade_price)
#                 percentage_change = round(mod_shared.getPercentChange(start_value, end_value), 2)
#                 dict_trade[mod_shared.glo_colName_trade_percentChange] = percentage_change

#         for dict_trade in trade_list:
#             orderStat_list.append(dict_trade)
#     except Exception as e:
#         print ("ERROR in file", glo_file_this, 'and function' ,inspect.stack()[0][3], ':', str(e))

#     else:
#         return orderStat_list


# trade_list = getDailyOrderStatistics()
# if trade_list:
#     # safer than setListKeys which deletes keys. This requires columns to be deleted manually from order-statistics.csv
#     trade_list = mod_shared.addKeysNotExisting(trade_list, mod_shared.glo_orderStatistics_colNames) 
#     # set keys already existing in trade_list to values of keys from stockToBuy_allData
#     stockToBuy_allData_list = mod_shared.getListFromFile(mod_shared.path_input_main, mod_shared.glo_stockToBuy_allData_file)
#     list_of_key_selectors = [mod_shared.glo_colName_nameShortNordnet]
#     trade_list = mod_shared.updateListFromListBy_existingKeys(trade_list,
#         stockToBuy_allData_list,
#         list_of_key_selectors) # list to update, list to update from
#     # BP()

#     # orderStat_list = mod_shared.getListFromFile(mod_shared.path_output, glo_file_noFile)

#     orderStat_list = mod_shared.getListFromFile(mod_shared.path_output, glo_file_orderStatistics)
#     if orderStat_list != False: # Important! Keep as False as longs as getListFromFile returns this for files not found.
#         org_len = len(orderStat_list)
#         orderStat_list_updated = getUpdatedOrderStatistics(orderStat_list, trade_list)
#         rev_len = len(orderStat_list_updated)
#         if rev_len > org_len:
#             mod_shared.writeListToCsvFile(orderStat_list_updated, mod_shared.path_output + glo_file_orderStatistics)
#         else:
#             print('Something might have gone wrong in', inspect.stack()[0][3], ': New', glo_file_orderStatistics, 'did not have more rows than old. No changes made.')
#     else:
#         print(glo_file_orderStatistics, 'did not exist. Creating new file with trade_list')
#         mod_shared.writeListToCsvFile(trade_list, mod_shared.path_output + glo_file_orderStatistics)




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
    # soup = BeautifulSoup(s.get('https://www.nordnet.se/mux/ajax/trade/orders/auto?accountNumber=18272500', headers=mod_shared.glo_urlHeader_userAgent).content, 'html.parser') # active are placed in "share"
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