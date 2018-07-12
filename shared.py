from pdb import set_trace as BP
import inspect
import os
import yaml
from robobrowser import RoboBrowser
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import smtplib
import time
import datetime
import csv
import sys
from collections import OrderedDict
from pprint import pprint
from pprint import pformat

# paths
path_base = os.path.dirname(os.path.abspath(__file__))
path_output = '/output/'
path_input = '/input/'
path_input_main = path_input + 'main/'
path_input_createList = path_input + 'create-stock-lists/'
path_input_monitorProcess = path_input + 'main-process-monitor/'
path_input_template = path_input + 'templates/'
path_input_test = 'test_files/'

# files
glo_file_this = os.path.basename(__file__)
glo_errorLog_file = 'errorLog.csv'

glo_stockInfo_file_raw = 'stock-info-raw.csv'
glo_blacklist_file = 'blacklist.csv'
glo_complimentary_file = 'nn-complimentary-list.csv'
glo_complimentary_file_template = 'nn-complimentary-list-template.csv'
glo_stockInfoUpdated_file = 'stock-info-updated.csv'
glo_stockInfoUpdated_file_template = 'stock-info-updated-template.csv'
glo_stockAfterSb_file_updated = 'stock-info-afterSb.csv'
glo_stockToBuy_allData_file = 'stocks-to-buy-all-data.csv'
glo_stockToBuy_allData_file_template = 'stocks-to-buy-all-data-template.csv'
glo_stockToBuy_file = 'stocks-to-buy.csv'
glo_stockToBuy_file_template = 'stocks-to-buy-template.csv'
glo_orderStatistics_file = 'order-statistics.csv'
glo_orderStatistics_file_template = 'order-statistics-template.csv'

glo_fileToRunIfCrash_main = 'main.py'
glo_pid_file = 'pid.txt'

glo_colName_sbNameshort = 'NAMESHORT_SB'
glo_colName_sbName = 'NAME_SB'
glo_colName_nameShortNordnet = 'NAMESHORT_NORDNET'
glo_colName_nameNordnet = 'NAME_NORDNET'
glo_colName_market_id = 'MARKET_ID'
glo_colName_identifier_id = 'IDENTIFIER_ID'
glo_colName_url_sb = 'URL_SB'
glo_colName_url_nn = 'URL_NN'
glo_colName_active = 'ACTIVE'
glo_colName_activeTemp = 'ACTIVE_TEMP'
glo_colName_amountHeld = 'VOLUME_HELD'
glo_colName_price = 'PRICE'
# glo_colName_priceTemp = 'PRICE_TEMP'

glo_colName_6_percent = 'MONTH_6_PERCENT_CORRECT'
glo_colName_6_value = 'MONTH_6_VALUE'
glo_colName_12_percent = 'MONTH_12_PERCENT_CORRECT'
glo_colName_12_value = 'MONTH_12_VALUE'
glo_colName_24_percent = 'MONTH_24_PERCENT_CORRECT'
glo_colName_24_value = 'MONTH_24_VALUE'
glo_colName_percentAverage = 'AVERAGE_PERCENT_CORRECT'
glo_colName_valueAverage = 'AVERAGE_VALUE'
glo_colName_24_buys_correct_percent = 'BUYS_24_PERCENT_CORRECT'
glo_colName_buysTotal = 'BUYS_TOTAL'
glo_colName_pricePercentChange_average = 'PRICE_CHANGE_PERCENT_AVERAGE'
glo_colName_pricePercentChange_median = 'PRICE_CHANGE_PERCENT_MEDIAN'
glo_colName_buyAverageFailedPerChange = 'BUY_AVERAGE_FAILED_PERCENT_CHANGE'
glo_colName_buyAverageSuccessPerChange = 'BUY_AVERAGE_SUCCESS_PERCENT_CHANGE'
glo_colName_buyMedianFailedPerChange = 'BUY_MEDIAN_FAILED_PERCENT_CHANGE'
glo_colName_buyMedianSuccessPerChange = 'BUY_MEDIAN_SUCCESS_PERCENT_CHANGE'
glo_colName_buyAndFailMedian_keyValue = 'BUYANDFAIL_MEDIAN_KEYVALUE'
glo_colName_buyAndFailAverage_keyValue = 'BUYANDFAIL_AVERAGE_KEYVALUE'
glo_colName_median_sell_intradayClosingChange_percent = 'MEDIAN_SELL_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_average_sell_intradayClosingChange_percent = 'AVERAGE_SELL_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_median_buy_intradayClosingChange_percent = 'MEDIAN_BUY_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_average_buy_intradayClosingChange_percent = 'AVERAGE_BUY_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_median_buyAndFailKeyValue_and_median_sellIntradayClosingPercentChange = 'SUM_BUYANDFAIL_MEDIAN_KEYVALUE_AND_MEDIAN_SELL_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_average_buyAndFailKeyValue_and_average_sellIntradayClosingPercentChange = 'SUM_BUYANDFAIL_AVERAGE_KEYVALUE_AND_AVERAGE_SELL_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_median_buyAndFailKeyValue_and_median_buyAndSellIntradayClosingPercentChange = 'SUM_BUYANDFAIL_MEDIAN_KEYVALUE_AND_MEDIAN_BUY_SELL_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_average_buyAndFailKeyValue_and_average_buyAndSellIntradayClosingPercentChange = 'SUM_BUYANDFAIL_AVERAGE_KEYVALUE_AND_AVERAGE_BUY_SELL_INTRADAY-CLOSING_PERCENT_CHANGE'
glo_colName_percentChange_highestThroughCurrent = 'HIGHEST_THROUGH_CURRENT_PERCENT_CHANGE'

glo_colName_compList = 'COMPLIMENTARY_LIST'
glo_colName_historySignalPrice = 'HISTORY_SIGNAL_PRICE'
glo_colName_stockToBuy_group = 'GROUP_BUY'
glo_value_group_1 = '1_median_buyAndSellIntradayClosing_and_buy_medianCorrectAndFailKeyValue'
glo_value_group_2 = '2_average_buyAndSellIntradayClosing_and_buy_averageCorrectAndFailKeyValue'

# order statistics
glo_colName_trade_time = 'TRADE_TIME'
glo_colName_trade_price = 'TRADE_PRICE'
glo_colName_trade_type = 'TRADE_TYPE'
glo_colName_trade_volume = 'TRADE_VOLUME'
glo_colName_trade_percentChange = 'TRADE_PERCENT_CHANGE'

# mainly trader
glo_stockStatus_list = []
glo_stockStatus_list_name = 'glo_stockStatus_list'

# mainly create lists
# glo_stockInfo_list_name = 'glo_stockInfo_list'
glo_nn_complimentary_list_name = 'glo_nn_complimentary_list'
glo_blacklist_name = 'glo_blacklist'

glo_sbBaseStockPageUrl = 'https://www.swedishbulls.com/SignalPage.aspx?lang=en&Ticker='

glo_complimentary_colNames = {}
glo_stockInfoUpdated_colNames = {}
glo_stockToBuy_colNames = {}
glo_stockToBuy_allData_colNames = {}
glo_orderStatistics_colNames = {}

glo_urlHeader_userAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

glo_credSb = 'credSb'
glo_credNordnet = 'credNordnet'
glo_credGmailAutotrading = 'credGmailAutotrading'

glo_sbLoginFormUser = 'ctl00$MainContent$uEmail'
glo_sbLoginFormPass = 'ctl00$MainContent$uPassword'
glo_sbLoginFormSubmit = 'ctl00$MainContent$btnSubmit'

glo_clearWatchlist = 'ctl00$MainContent$DeleteAll'

glo_counter_error = 0
glo_sellPercentageSubtraction = 7 # max percent change low seems to be 10%

def errorHandler(e_msg):
    try:
        # print ('\nERROR: \n\tFile:', temp_glo_file_this, '\n\tFunction:', calling_function, '\n\tLine:', line_number, '\n\tError:', str(e_msg), '\n')
        print ('\nERROR: \n\tFile:', inspect.stack()[1][1], '\n\tFunction:', inspect.stack()[1][3], '\n\tLine:', format(sys.exc_info()[-1].tb_lineno), '\n\tError:', str(e_msg), '\n')
        writeErrorLog(inspect.stack()[1][3], format(sys.exc_info()[-1].tb_lineno), inspect.stack()[1][1], str(e_msg))
    except Exception as e:
        print ('\nERROR: \n\tFile:', inspect.stack()[0][1], '\n\tFunction:', inspect.stack()[0][3], '\n\tLine:', format(sys.exc_info()[-1].tb_lineno), '\n\tError:', str(e), '\n')
        writeErrorLog(inspect.stack()[0][3], format(sys.exc_info()[-1].tb_lineno), inspect.stack()[0][1], str(e))

def incrCounterError():
    try:
        global glo_counter_error
        glo_counter_error += 1
    except Exception as e:
        mod_shared.errorHandler(e)    

def getCounterError():
    try:
        return glo_counter_error
    except Exception as e:
        mod_shared.errorHandler(e)    

def resetCounterError():
    print(inspect.stack()[0][3])
    try:
        global glo_counter_error
        glo_counter_error += 0
    except Exception as e:
        mod_shared.errorHandler(e)    

def writeErrorLog (callingFunction, errorLine, errorFile, eStr):
    print ('\nSTART', inspect.stack()[0][3])
    try:
        incrCounterError()
        errorDate = 'DATE'
        errorTime = 'TIME'
        errorDay = 'DAY'
        errorCounter = 'ERROR_COUNTER'
        errorCallingFunction = 'CALLING_FUNCTION'
        errorMsg = 'E_MSG'
        colName_errorLine = 'Line'
        colName_errorFile = 'File'
        file_errorLog = path_base + path_output + glo_errorLog_file
        file_exists = os.path.isfile(file_errorLog)
        if getCounterError() <= 100:
            with open (file_errorLog, 'a') as csvFile:
                fieldnames = [errorDate, errorTime, errorDay, errorCounter, colName_errorFile, errorCallingFunction, colName_errorLine, errorMsg]
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter = ';')
                if not file_exists:
                    writer.writeheader()
                writer.writerow({errorDate: getDateToday_customFormat_str('%Y-%m-%d'), 
                    errorTime: getTimestampCustomStr('%H:%M'), 
                    errorDay: getDateToday_customFormat_str('%A'), 
                    errorCounter: str(glo_counter_error),
                    errorCallingFunction: callingFunction,
                    colName_errorLine: errorLine,
                    colName_errorFile: errorFile,
                    errorMsg: eStr})
                # sendEmail('ERROR: ' + callingFunction, eStr)
                sendEmail('ERROR: {}; Line: {}'.format(callingFunction, str(errorLine)), eStr)
    except Exception as e:
        print ('\nERROR: \n\tFile:', glo_file_this, '\n\tFunction:', inspect.stack()[0][3], '\n\tLine:', format(sys.exc_info()[-1].tb_lineno), '\n\tError:', str(e), '\n')

def sendEmail(sbj, body):
    print ('\nSTART', inspect.stack()[0][3])
    try:
        msg = 'Subject: {}\n\n{}'.format(sbj, body)
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.starttls()
        credGmailAutotrading = getCredentials(glo_credGmailAutotrading)
        smtp.login(credGmailAutotrading.get('username'), credGmailAutotrading.get('pwd'))
        smtp.sendmail(credGmailAutotrading.get('username'), credGmailAutotrading.get('username'), msg) # 1 from, 2 to
    except Exception as e:
        print ('\nERROR: \n\tFile:', glo_file_this, '\n\tFunction:', inspect.stack()[0][3], '\n\tLine:', format(sys.exc_info()[-1].tb_lineno), '\n\tError:', str(e), '\n')
    else:
        print('END', inspect.stack()[0][3], '\n')

def getCredentials(domain):
    try:
        if domain == glo_credNordnet:
            conf = yaml.load(open(path_base + path_input + 'credentials.yml'))
            username = conf['nordnet']['username']
            pwd = conf['nordnet']['password']
            return {'username': username, 'password': pwd}
        elif domain == glo_credSb:
            conf = yaml.load(open(path_base + path_input + 'credentials.yml'))
            username = conf['sb']['username']
            pwd = conf['sb']['password']
            return {'username': username, 'pwd': pwd}
        elif domain == glo_credGmailAutotrading:
            conf = yaml.load(open(path_base + path_input + 'credentials.yml'))
            username = conf['gmail_autotrade']['username']
            pwd = conf['gmail_autotrade']['password']
            return {'username': username, 'pwd': pwd}
    except Exception as e:
        mod_shared.errorHandler(e)

def sbLogin():
    # print ('\nSTART', inspect.stack()[0][3])
    try:
        browser = RoboBrowser(history=True)
        browser.open('https://www.swedishbulls.com/Signin.aspx?lang=en')
        form = browser.get_form()
        # SB login
        credSb = getCredentials(glo_credSb)
        form[glo_sbLoginFormUser].value = credSb.get('username')
        form[glo_sbLoginFormPass].value = credSb.get('pwd')
        browser.submit_form(form, submit=form[glo_sbLoginFormSubmit])
    except Exception as e: # catch error
        mod_shared.errorHandler(e)
    else:
        # print('END', inspect.stack()[0][3], '\n')
        return (browser)

def nordnetLogin():
    # print ('\nSTART', inspect.stack()[0][3])    
    try:
        # s = requests.session()
        s = requests_retry_session()
        
        header = {'Accept': 'application/json'}
        # add pre-defined user-agent
        header.update(glo_urlHeader_userAgent)

        urlGetLoginPage = 'https://www.nordnet.se/mux/login/start.html?cmpi=start-loggain&state=signin'
        r = s.get(urlGetLoginPage) 
        if r.status_code != 200:
            print(urlGetLoginPage, 'failed!')

        # Anonymous to get cookie
        urlPostAnonymous = 'https://www.nordnet.se/api/2/login/anonymous'
        r = s.post(urlPostAnonymous, headers=header) 
        if r.status_code != 200:
            print(urlPostAnonymous, 'failed!')

        # Login post
        urlPostLogin = 'https://www.nordnet.se/api/2/authentication/basic/login'
        credNord = getCredentials(glo_credNordnet)
        r = s.post(urlPostLogin, headers=header, data=credNord) 
        if r.status_code != 200:
            print(urlPostLogin, 'failed!')
            print('status_code:', r.status_code)
            print('text:', r.text)
            responseDict = {
            'status_code': str(r.status_code),
            'reason': r.reason,
            'url': r.url
            }
            writeErrorLog(inspect.stack()[0][3], pformat(responseDict))
    except Exception as e: # catch error
        mod_shared.errorHandler(e)
    else:
        # print('END', inspect.stack()[0][3], '\n')
        return (r, header, s)

def getDateToday_customFormat_str(customFormat): #e.g., '%d.%m.%Y' for '30.06.2018'
    return datetime.date.today().strftime(customFormat)

def getDate_deltaToday_customFormat_str(days, customFormat):
    return (datetime.date.today() + datetime.timedelta(days)).strftime(customFormat)

def getTimestampCustomStr(customFormat):
    return datetime.datetime.now().strftime(customFormat)

def getSecondsFromTime(days, hours, minutes, seconds):
    try:
        day_sec = 24*60*60
        hour_sec = 60*60
        min_sec = 60
        
        return days*day_sec + hours*hour_sec + minutes*min_sec + seconds
    except Exception as e:
        mod_shared.errorHandler(e)

def getTimestamp():
    return datetime.datetime.now()

def getTimestampStr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

def getOrderedDictFromDict(dictTemp, order_of_keys_list):
    try:
        list_of_tuples = [(key, dictTemp[key]) for key in order_of_keys_list]
        return OrderedDict(list_of_tuples)
    except Exception as e:
        mod_shared.errorHandler(e) 

def updateListFromListByKeys(list_to_update, list_to_update_from, list_of_key_selectors, list_of_key_overwriters):
    try:
        for rowTo in list_to_update:
            for rowFrom in list_to_update_from:
                for key_selector in list_of_key_selectors:
                    if rowTo[key_selector] == rowFrom[key_selector]:
                        for key_overwriter in list_of_key_overwriters:
                            if key_overwriter in rowFrom: # if key exist in dict
                                rowTo[key_overwriter] = rowFrom[key_overwriter]
                        break
        return list_to_update
    except Exception as e:
        mod_shared.errorHandler(e)

def updateListFromListBy_existingKeys(list_to_update, list_to_update_from, list_of_key_selectors):
    try:
        for dict_to in list_to_update:
            for dict_from in list_to_update_from:
                for key_selector in list_of_key_selectors:
                    if dict_to[key_selector] == dict_from[key_selector]:
                        for k in dict_to:
                            if k in dict_from:
                                dict_to[k] = dict_from[k]
                        break
        return list_to_update
    except Exception as e:
        mod_shared.errorHandler(e) 

def removeListFromListByKey(list_to_keep, list_to_remove, list_of_key_selectors):
    try:
        unique_list = []
        for dict_keep in list_to_keep:
            not_in_list = True
            for dict_remove in list_to_remove:
                for key in list_of_key_selectors:
                    if dict_remove.get(key) == dict_keep.get(key):
                        not_in_list = False
            if not_in_list:
                unique_list.append(dict_keep)
        return unique_list
    except Exception as e:
        mod_shared.errorHandler(e)

def setListGlobal(list_to_set, name_of_list):
    try:
        # if name_of_list == glo_stockInfo_list_name:
        #     global glo_stockInfo_list
        #     glo_stockInfo_list = list_to_set
        if name_of_list == glo_stockStatus_list_name:
            global glo_stockStatus_list
            glo_stockStatus_list = list_to_set
    except Exception as e:
        mod_shared.errorHandler(e)

def getGlobalList(name_of_list):
    try:
        # if name_of_list == glo_stockInfo_list_name:
        #     global glo_stockInfo_list
        #     glo_stockInfo_list = temp_list
        if name_of_list == glo_stockStatus_list_name:
            return glo_stockStatus_list
    except Exception as e:
        mod_shared.errorHandler(e)

def getListFromFile(path_rel, name_of_file):
    try:
        temp_list = []
        path_and_fileName = path_base + path_rel + name_of_file
        if os.path.isfile(path_and_fileName):
            with open (path_and_fileName, encoding='ISO-8859-1') as csvFile:
                records = csv.DictReader(csvFile, delimiter=';') # omitting "fieldnames" - will make file headers fieldnames
                fieldnames = records.fieldnames
                for rowDict in records:
                    order_of_keys = fieldnames
                    temp_list.append(getOrderedDictFromDict(rowDict, order_of_keys))
                return temp_list
        else:
            print('file name and path does not exist:' + path_and_fileName)
            print('returning False')
            return False
    except Exception as e:
        mod_shared.errorHandler(e)

def getColNamesFromFile(rel_path_of_file, file_name):
    try:
        path_full = path_base + rel_path_of_file + file_name
        with open (path_full, encoding='ISO-8859-1') as csvFile:
            records = csv.DictReader(csvFile, delimiter=';') # omitting "fieldnames" - will make file headers fieldnames
            list_of_colNames = records.fieldnames
            ordered_dict = OrderedDict()
            for colName in list_of_colNames:
                ordered_dict[colName] = ''   
            return ordered_dict
    except Exception as e:
        mod_shared.errorHandler(e)

def setListKeys(list_to_set, dict_set_from):
    try:
        # add key-value pairs to list if not existing
        for dict_to_set in list_to_set:
            for key_from, value_from in dict_set_from.items():
                if key_from not in dict_to_set:
                    dict_to_set[key_from] = value_from

        # add key-value which keys exist in dict_set_from to new list (getting rid of the rest)
        new_list = []
        for dict_to_set in list_to_set:
            new_ordered_dict = OrderedDict()
            for key_to, value_to in dict_to_set.items():
                if key_to in dict_set_from:
                    new_ordered_dict[key_to] = value_to
            new_list.append(new_ordered_dict)

        # arrange keys in new list in same order as dict_set_from
        key_order_list = list(dict_set_from.keys())
        new_ordered_list = []
        for dict_temp in new_list:
            new_ordered_list.append(OrderedDict((k, dict_temp[k]) for k in key_order_list))

    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return new_ordered_list

def addKeysNotExisting(list_to_set, dict_set_from):
    try:
        # add keys-value pairs to list if not existing
        for dict_to_set in list_to_set:
            for key_from, value_from in dict_set_from.items():
                if key_from not in dict_to_set:
                    dict_to_set[key_from] = value_from

        # arrange keys in new list in same order as dict_set_from
        key_order_list = list(dict_set_from.keys())
        new_ordered_list = []
        for dict_temp in list_to_set:
            new_ordered_list.append(OrderedDict((k, dict_temp[k]) for k in key_order_list))

    except Exception as e:
        mod_shared.errorHandler(e)
    else:
        return new_ordered_list

def setGlobalColNames():
    try:
        dict_colNames = getColNamesFromFile(path_input_template, glo_complimentary_file_template) # path, file
        global glo_complimentary_colNames
        glo_complimentary_colNames = dict_colNames

        dict_colNames = getColNamesFromFile(path_input_template, glo_stockInfoUpdated_file_template) # path, file
        global glo_stockInfoUpdated_colNames
        glo_stockInfoUpdated_colNames = dict_colNames

        dict_colNames = getColNamesFromFile(path_input_template, glo_stockToBuy_file_template) # path, file
        global glo_stockToBuy_colNames
        glo_stockToBuy_colNames = dict_colNames
        
        dict_colNames = getColNamesFromFile(path_input_template, glo_stockToBuy_allData_file_template) # path, file
        global glo_stockToBuy_allData_colNames
        glo_stockToBuy_allData_colNames = dict_colNames

        dict_colNames = getColNamesFromFile(path_input_template, glo_orderStatistics_file_template) # path, file
        global glo_orderStatistics_colNames
        glo_orderStatistics_colNames = dict_colNames

    except Exception as e:
        mod_shared.errorHandler(e)

def requests_retry_session(retries=3, backoff_factor=0.3, session=None):
    try:
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
        
    except Exception as e:
        mod_shared.errorHandler(e)

def getPercentChange(start_value, end_value):
    try:
        # positive result: end_value is higher than start_value
        return ((end_value - start_value) / start_value)*100
    except Exception as e:
        mod_shared.errorHandler(e)    

def writeListToCsvFile(list_to_write, name_path_file):
    try:
        if list_to_write:
            glo_file_thisPath = path_base + name_path_file
            with open (glo_file_thisPath, 'w', encoding='ISO-8859-1') as csvFile:
                fieldnames = []
                indexWithMaxNumOfKeys = 0
                maxNumOfKeys = 0
                counter = 0
                # get index with most number of keys to get correct fieldnames
                for dictTemp in list_to_write:
                    if len(dictTemp.keys()) > maxNumOfKeys:
                        maxNumOfKeys = len(dictTemp.keys())
                        indexWithMaxNumOfKeys = counter
                    if counter == len(list_to_write)-1:
                        break
                    else:
                        counter += 1
                for key in list_to_write[indexWithMaxNumOfKeys]:
                    fieldnames.append(key)
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter = ';')
                writer.writeheader()
                for row in list_to_write:
                    writer.writerow(row)
        else:
            print('{}: list for file {} was empty: no file being written'.format(inspect.stack()[0][3], name_path_file))
    except Exception as e:
        mod_shared.errorHandler(e)

def getDecimalFromPercentage(percentageNumber):
    try:
        return float(percentageNumber/100)
    except Exception as e:
        errorHandler(e)

def main():
    try:
        setGlobalColNames()
    except Exception as e:
        mod_shared.errorHandler(e)

main()