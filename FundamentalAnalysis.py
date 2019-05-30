# Import Dependencies
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf  
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader as pdr
import feedparser as fp
from pandas_datareader._utils import RemoteDataError
import time
import pickle

def summary(symbol):
    
    summary = {}
    dummy = 0

    if len(str(symbol)) > 6:
        for s in symbol:
            summary_url = 'https://finance.yahoo.com/quote/' + s + '?p=' + s

            data = {}

            page = requests.get(summary_url)
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')

            data[0] = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]
            data[1] = pd.read_html(lxml.etree.tostring(table[1], method='html'))[0]

            data[0] = data[0].append(data[1])

            data = data[0].set_index(0)
            data = pd.DataFrame(data[1].fillna(0))

            summary[s] = data[1]
                
    else:
            summary_url = 'https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol

            data = {}

            page = requests.get(summary_url)
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')

            data[0] = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]
            data[1] = pd.read_html(lxml.etree.tostring(table[1], method='html'))[0]

            data[0] = data[0].append(data[1])

            data = data[0].set_index(0)
            data = pd.DataFrame(data[1].fillna(0))

            summary[symbol] = data[1]
        

    summary = pd.DataFrame(summary).fillna(0)
    
    for x in summary.columns:
        for i in range(0,len(summary)):
            if 'M' in str(summary[x][i]):
                try:
                    summary[x][i] = float(summary[x][i].replace('M', '')) * 1000000

                except:
                    continue

            elif 'B' in str(summary[x][i]):
                try:
                    summary[x][i] = float(summary[x][i].replace('B', '')) * 1000000000

                except:
                    continue

            elif '%' in str(summary[x][i]):
                try:
                    summary[x][i] = float(summary[x][i].replace('%', '')) / 100

                except:
                    continue

            else:
                try:
                    summary[x][i] = float(summary[x][i])

                except:
                    continue
    
    return summary
    
def balance_sheet(symbol = 0, read_pickle = False):
    
    if read_pickle == True:
        print('Reading last created Pickle')
        balance_sheet = pd.read_pickle('balance_sheet')
        return balance_sheet
    
    else:
        balance_sheet = {}
        dummy = 0
    
        if symbol == 0:
            page = requests.get('https://finance.yahoo.com/trending-tickers')
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
            print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

        else:
            print('Using Manual Input.')

    if len(str(symbol)) > 6:
        for s in symbol:
            balance_sheet_url = 'https://finance.yahoo.com/quote/' + s + '/balance-sheet?p=' + s

            page = requests.get(balance_sheet_url)
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0].set_index(0).transpose()

            if len(data) == 0:
                continue

            if 'Volume' in data.columns:
                print('Other entity than a company detected therefore not adding data for: ' + s)

            else:
                for d in data.columns.unique():
                    try:
                        data[d].astype('int64')

                    except ValueError:
                        if '-' in data[d].values:
                            continue

                        elif dummy == 0:
                            index = data['Period Ending']
                            data = data.drop('Period Ending', axis = 1)
                            dummy = 1
                            dates = []

                            for y in index:
                                dates.append(y[-4:])   
                        else:
                            data = data.drop(d, axis=1)

                for c in data.columns: 
                    balance_sheet[s, c] = data[c]
        
    else:
        balance_sheet_url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol

        page = requests.get(balance_sheet_url)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0].set_index(0).transpose()

        if len(data) == 0:
            print('Not data available for' + symbol)

        if 'Volume' in data.columns:
            print('Other entity than a company detected therefore not adding data for: ' + symbol)

        else:
            for d in data.columns.unique():
                try:
                    data[d].astype('int64')

                except ValueError:
                    if '-' in data[d].values:
                        continue

                    elif dummy == 0:
                        index = data['Period Ending']
                        data = data.drop('Period Ending', axis = 1)
                        dummy = 1
                        dates = []

                        for y in index:
                            dates.append(y[-4:])   
                    else:
                        data = data.drop(d, axis=1)

            for c in data.columns: 
                balance_sheet[symbol, c] = data[c]

    try: 
        balance_sheet = pd.DataFrame(balance_sheet).set_index([dates])
        balance_sheet = balance_sheet.replace('-','0').astype(float).fillna(0)
        balance_sheet = balance_sheet.sort_index()
        balance_sheet.to_pickle('balance_sheet')

    except ValueError as e:
        print('Could not convert to a DataFrame due to: ', e)

    return balance_sheet

def income_statement(symbol = 0, read_pickle = False):
    
    if read_pickle == True:
        print('Reading last created Pickle')
        financials = pd.read_pickle('income_statement')
        return financials
    
    else:
        financials = {}
        dummy = 0

        if symbol == 0:
            page = requests.get('https://finance.yahoo.com/trending-tickers')
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
            print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

        else:
            print('Using Manual Input.')

        
    if len(str(symbol)) > 6:
        for s in symbol:
            financials_url = 'https://finance.yahoo.com/quote/' + s + '/financials?p=' + s

            page = requests.get(financials_url)
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0].set_index(0).transpose()

            if len(data) == 0:
                continue

            if 'Volume' in data.columns:
                print('Other entity than a company detected therefore not adding data for: ' + s)

            else:
                for d in data.columns.unique():
                    try:
                        data[d].astype('int64')

                    except ValueError:
                        if '-' in data[d].values:
                            continue

                        elif dummy == 0:
                            index = data['Revenue']
                            data = data.drop('Revenue', axis = 1)
                            dummy = 1
                            dates = []

                            for y in index:
                                dates.append(y[-4:])   
                        else:
                            data = data.drop(d, axis=1)

                for c in data.columns:
                    financials[s, c] = data[c]
                    
    else:
        financials_url = 'https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol

        page = requests.get(financials_url)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0].set_index(0).transpose()

        if len(data) == 0:
            print('Not data available for' + symbol)

        if 'Volume' in data.columns:
            print('Other entity than a company detected therefore not adding data for: ' + symbol)

        else:
            for d in data.columns.unique():
                try:
                    data[d].astype('int64')

                except ValueError:
                    if '-' in data[d].values:
                        continue

                    elif dummy == 0:
                        index = data['Revenue']
                        data = data.drop('Revenue', axis = 1)
                        dummy = 1
                        dates = []

                        for y in index:
                            dates.append(y[-4:])   
                    else:
                        data = data.drop(d, axis=1)

            for c in data.columns:
                financials[symbol, c] = data[c]

    try:
        financials = pd.DataFrame(financials).set_index([dates])
        financials = financials.replace('-','0').astype(float).fillna(0)
        financials = financials.sort_index()
        financials.to_pickle('income_statement')

    except ValueError as e:
        print('Could not convert to a DataFrame due to: ', e)

    return financials

def cashflows(symbol = 0, read_pickle = False):
    
    if read_pickle == True:
        print('Reading last created Pickle')
        cashflows = pd.read_pickle('cashflows')
        return cashflows
    
    else:
        cashflows = {}
        dummy = 0

        if symbol == 0:
            page = requests.get('https://finance.yahoo.com/trending-tickers')
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
            print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

        else:
            print('Using Manual Input.')
    
    if len(str(symbol)) > 6:
        for s in symbol:
            cashflows_url = 'https://finance.yahoo.com/quote/' + s + '/cash-flow?p=' + s
            
            page = requests.get(cashflows_url)
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0].set_index(0).transpose()

            if len(data) == 0:
                continue

            if 'Volume' in data.columns:
                print('Other entity than a company detected therefore not adding data for: ' + s)

            else:
                for d in data.columns.unique():
                    try:
                        data[d].astype('int64')

                    except ValueError:
                        if '-' in data[d].values:
                            continue

                        elif dummy == 0:
                            index = data['Period Ending']
                            data = data.drop('Period Ending', axis = 1)
                            dummy = 1
                            dates = []

                            for y in index:
                                dates.append(y[-4:])   
                        else:
                            data = data.drop(d, axis=1)

                for c in data.columns:
                    cashflows[s, c] = data[c]
        
    else:
        cashflows_url = 'https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol

        page = requests.get(cashflows_url)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0].set_index(0).transpose()

        if len(data) == 0:
            print('Not data available for' + symbol)

        if 'Volume' in data.columns:
            print('Other entity than a company detected therefore not adding data for: ' + symbol)

        else:
            for d in data.columns.unique():
                try:
                    data[d].astype('int64')

                except ValueError:
                    if '-' in data[d].values:
                        continue

                    elif dummy == 0:
                        index = data['Period Ending']
                        data = data.drop('Period Ending', axis = 1)
                        dummy = 1
                        dates = []

                        for y in index:
                            dates.append(y[-4:])   
                    else:
                        data = data.drop(d, axis=1)

            for c in data.columns:
                cashflows[symbol, c] = data[c]

    try:
        cashflows = pd.DataFrame(cashflows).set_index([dates])
        cashflows = cashflows.replace('-','0').astype(float).fillna(0)
        cashflows = cashflows.sort_index()
        cashflows.to_pickle('cashflows')

    except ValueError as e:
        print('Could not convert to a DataFrame due to: ', e)

    return cashflows

def ratios(symbol = 0, read_pickle = False):
    
    if read_pickle == True:
        print('Reading last created Pickle')
        ratios = pd.read_pickle('ratios')
        return ratios
    
    else:
        ratios = {}
        dummy = 0

    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

    else:
        print('Using Manual Input.')

    if len(str(symbol)) > 6:
        for s in symbol:
            ratios_url = 'https://finance.yahoo.com/quote/' + s + '/key-statistics?p=' + s

            data = {}

            page = requests.get(ratios_url)
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')

            for i in range(0,len(table)-1,1):
                data[i] = pd.read_html(lxml.etree.tostring(table[i], method='html'))[0]

            for d in range(1,len(table)-1,1):
                data[0] = data[0].append(data[d])

            data = data[0].set_index(0)
            data = pd.DataFrame(data[1].fillna(0))

            if 'Volume' in data.T.columns:
                print('Other entity than a company detected therefore not adding ratios for: ' + s)

            else:
                ratios[s] = data[1]
    
    else:
        ratios_url = 'https://finance.yahoo.com/quote/' + symbol + '/key-statistics?p=' + symbol

        data = {}

        page = requests.get(ratios_url)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')

        for i in range(0,len(table)-1,1):
            data[i] = pd.read_html(lxml.etree.tostring(table[i], method='html'))[0]

        for d in range(1,len(table)-1,1):
            data[0] = data[0].append(data[d])

        data = data[0].set_index(0)
        data = pd.DataFrame(data[1].fillna(0))

        if 'Volume' in data.T.columns:
            print('Other entity than a company detected therefore not adding ratios for: ' + s)

        else:
            ratios[symbol] = data[1]        

    try:
        ratios = pd.DataFrame(ratios).fillna(0)
        ratios.replace([np.inf, -np.inf], 0)
        ratios.to_pickle('ratios')

    except ValueError as e:
        print('Could not convert to a DataFrame due to: ', e)
        
    for x in ratios.columns:
        for i in range(0,len(ratios)):

            if '∞' in str(ratios[x][i]):
                try:
                    ratios[x][i] = ratios[x][i].replace('∞', '0')

                except:
                    continue

            if 'M' in str(ratios[x][i]):
                try:
                    ratios[x][i] = float(ratios[x][i].replace('M', '')) * 1000000

                except:
                    continue

            if 'B' in str(ratios[x][i]):
                try:
                    ratios[x][i] = float(ratios[x][i].replace('B', '')) * 1000000000

                except:
                    continue

            if '%' in str(ratios[x][i]):
                try:
                    ratios[x][i] = float(ratios[x][i].replace('%', '')) / 100

                except:
                    continue

            if 'k' in str(ratios[x][i]):
                try:
                    ratios[x][i] = float(ratios[x][i].replace('k', '')) / 100

                except:
                    continue

            else:
                try:
                    ratios[x][i] = float(ratios[x][i])

                except:
                    continue

    return ratios
    
def balance_sheet_analysis(balance_sheet, symbol = 0):
    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

    else:
        print('Using Manual Input.')
    
    cash = pd.DataFrame(index=balance_sheet.index)
    inventory = pd.DataFrame(index=balance_sheet.index)
    accounts_receivable = pd.DataFrame(index=balance_sheet.index)
    short_term_investments = pd.DataFrame(index=balance_sheet.index)
    property_plant_equipment = pd.DataFrame(index=balance_sheet.index)
    total_current_assets = pd.DataFrame(index=balance_sheet.index)
    accounts_payable = pd.DataFrame(index=balance_sheet.index)
    long_term_debt = pd.DataFrame(index=balance_sheet.index)
    other_current_liabilities = pd.DataFrame(index=balance_sheet.index)
    total_current_liabilities = pd.DataFrame(index=balance_sheet.index)
    common_stock = pd.DataFrame(index=balance_sheet.index)
    preferred_stock = pd.DataFrame(index=balance_sheet.index)
    retained_earnings = pd.DataFrame(index=balance_sheet.index)
    total_stockholder_equity = pd.DataFrame(index=balance_sheet.index)
    
    
    if len(str(symbol)) > 6:
        for x in symbol:
            if x in balance_sheet:
                # Assets
                cash[x] = balance_sheet[x, 'Cash And Cash Equivalents']
                inventory[x] = balance_sheet[x, 'Inventory']
                accounts_receivable[x] = balance_sheet[x, 'Net Receivables']
                short_term_investments[x] = balance_sheet[x, 'Short Term Investments']
                property_plant_equipment[x] = balance_sheet[x, 'Property Plant and Equipment']
                total_current_assets[x] = balance_sheet[x, 'Total Current Assets']

                # Liabilities
                accounts_payable[x] = balance_sheet[x, 'Accounts Payable']
                long_term_debt[x] = balance_sheet[x, 'Long Term Debt']
                other_current_liabilities[x] = balance_sheet[x, 'Other Current Liabilities']
                total_current_liabilities[x] = balance_sheet[x, 'Total Current Liabilities']

                # Equity
                common_stock[x] = balance_sheet[x,'Common Stock']
                preferred_stock[x] = balance_sheet[x,'Preferred Stock']
                retained_earnings[x] = balance_sheet[x, 'Retained Earnings']
                total_stockholder_equity[x] = balance_sheet[x, 'Total Stockholder Equity']

        print('Assets')
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15,15))
        cash.plot.bar(ax=axes[0,0], rot=0).set_title('Cash And Cash Equivalents')
        inventory.plot.bar(ax=axes[0,1], rot=0).set_title('Inventory')
        accounts_receivable.plot.bar(ax=axes[1,0], rot=0).set_title('Accounts Receivables')
        short_term_investments.plot.bar(ax=axes[1,1], rot=0).set_title('Short Term Investments')
        property_plant_equipment.plot.bar(ax=axes[2,0], rot=0).set_title('Property Plant and Equipment')
        total_current_assets.plot.bar(ax=axes[2,1], rot=0).set_title('Total Current Assets')
        plt.show()

        print('Liabilities')
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        accounts_payable.plot.bar(ax=axes[0,0], rot=0).set_title('Accounts Payable')
        long_term_debt.plot.bar(ax=axes[0,1], rot=0).set_title('Long Term Debt')
        other_current_liabilities.plot.bar(ax=axes[1,0], rot=0).set_title('Other Current Liabilities')
        total_current_liabilities.plot.bar(ax=axes[1,1], rot=0).set_title('Total Current Liabilities')
        plt.show()

        print('Equity')
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        common_stock.plot.bar(ax=axes[0,0], rot=0).set_title('Common Stock')
        preferred_stock.plot.bar(ax=axes[0,1], rot=0).set_title('Preferred Stock')
        retained_earnings.plot.bar(ax=axes[1,0], rot=0).set_title('Retained Earnings')
        total_stockholder_equity.plot.bar(ax=axes[1,1], rot=0).set_title('Total Stockholder Equity')
        plt.show()

    else:
        # Assets
        cash[symbol] = balance_sheet[symbol,'Cash And Cash Equivalents']
        inventory[symbol] = balance_sheet[symbol,'Inventory']
        accounts_receivable[symbol] = balance_sheet[symbol,'Net Receivables']
        short_term_investments[symbol] = balance_sheet[symbol,'Short Term Investments']
        property_plant_equipment[symbol] = balance_sheet[symbol,'Property Plant and Equipment']
        total_current_assets[symbol] = balance_sheet[symbol,'Total Current Assets']

        # Liabilities
        accounts_payable[symbol] = balance_sheet[symbol,'Accounts Payable']
        long_term_debt[symbol] = balance_sheet[symbol,'Long Term Debt']
        other_current_liabilities[symbol] = balance_sheet[symbol,'Other Current Liabilities']
        total_current_liabilities[symbol] = balance_sheet[symbol,'Total Current Liabilities']

        # Equity
        common_stock[symbol] = balance_sheet[symbol,'Common Stock']
        preferred_stock[symbol] = balance_sheet[symbol,'Preferred Stock']
        retained_earnings[symbol] = balance_sheet[symbol,'Retained Earnings']
        total_stockholder_equity[symbol] = balance_sheet[symbol,'Total Stockholder Equity']
        
        print('Assets')
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15,15))
        cash.plot.bar(ax=axes[0,0], rot=0).set_title('Cash And Cash Equivalents')
        inventory.plot.bar(ax=axes[0,1], rot=0).set_title('Inventory')
        accounts_receivable.plot.bar(ax=axes[1,0], rot=0).set_title('Accounts Receivables')
        short_term_investments.plot.bar(ax=axes[1,1], rot=0).set_title('Short Term Investments')
        property_plant_equipment.plot.bar(ax=axes[2,0], rot=0).set_title('Property Plant and Equipment')
        total_current_assets.plot.bar(ax=axes[2,1], rot=0).set_title('Total Current Assets')
        plt.show()
        
        print('Liabilities')
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        accounts_payable.plot.bar(ax=axes[0,0], rot=0).set_title('Accounts Payable')
        long_term_debt.plot.bar(ax=axes[0,1], rot=0).set_title('Long Term Debt')
        other_current_liabilities.plot.bar(ax=axes[1,0], rot=0).set_title('Other Current Liabilities')
        total_current_liabilities.plot.bar(ax=axes[1,1], rot=0).set_title('Total Current Liabilities')
        plt.show()
        
        print('Equity')
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        common_stock.plot.bar(ax=axes[0,0], rot=0).set_title('Common Stock')
        preferred_stock.plot.bar(ax=axes[0,1], rot=0).set_title('Preferred Stock')
        retained_earnings.plot.bar(ax=axes[1,0], rot=0).set_title('Retained Earnings')
        total_stockholder_equity.plot.bar(ax=axes[1,1], rot=0).set_title('Total Stockholder Equity')
        plt.show()

def income_statement_analysis(financials, symbol = 0, log=False):
    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

    else:
        print('Using Manual Input.')
        
    total_revenue = pd.DataFrame(index=financials.index)
    cost_of_revenue = pd.DataFrame(index=financials.index)
    general_expenses = pd.DataFrame(index=financials.index)
    research_development = pd.DataFrame(index=financials.index)
    operating_profit = pd.DataFrame(index=financials.index)
    net_income = pd.DataFrame(index=financials.index)
        
    
    if len(str(symbol)) > 6:
        if log == True:
            for x in symbol:
                if x in financials:
                    try:
                        total_revenue[x] = np.log(financials[x,'Total Revenue'])
                        cost_of_revenue[x] = np.log(financials[x,'Cost of Revenue'])
                        general_expenses[x] = np.log(financials[x, 'Selling General and Administrative'])
                        research_development[x] = np.log(financials[x,'Research Development'])
                        operating_profit[x] = np.log(financials[x,'Operating Income or Loss'])
                        net_income[x] = np.log(financials[x,'Net Income From Continuing Ops'])
                
                    except KeyError:
                        continue
                    

            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15,15))
            total_revenue.plot.bar(ax=axes[0,0], rot=0).set_title('Total Revenue')
            cost_of_revenue.plot.bar(ax=axes[0,1], rot=0).set_title('Cost of Revenue (COGS)')
            general_expenses.plot.bar(ax=axes[1,0], rot=0).set_title('Selling, General and Administrative Expenses (SG&A)')
            research_development.plot.bar(ax=axes[1,1], rot=0).set_title('Research Development')
            operating_profit.plot.bar(ax=axes[2,0], rot=0).set_title('Operating Income or Loss')
            net_income.plot.bar(ax=axes[2,1], rot=0).set_title('Net Income From Continuing Ops')
            plt.show()

        else:
            for x in symbol:
                if x in financials:
                    try:
                        total_revenue[x] = financials[x,'Total Revenue']
                        cost_of_revenue[x] = financials[x,'Cost of Revenue']
                        general_expenses[x] = financials[x, 'Selling General and Administrative']
                        research_development[x] = financials[x,'Research Development']
                        operating_profit[x] = financials[x,'Operating Income or Loss']
                        net_income[x] = financials[x,'Net Income From Continuing Ops']

                    except KeyError:
                        continue

            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15,15))
            total_revenue.plot.bar(ax=axes[0,0], rot=0).set_title('Total Revenue')
            cost_of_revenue.plot.bar(ax=axes[0,1], rot=0).set_title('Cost of Revenue (COGS)')
            general_expenses.plot.bar(ax=axes[1,0], rot=0).set_title('Selling, General and Administrative Expenses (SG&A)')
            research_development.plot.bar(ax=axes[1,1], rot=0).set_title('Research Development')
            operating_profit.plot.bar(ax=axes[2,0], rot=0).set_title('Operating Income or Loss')
            net_income.plot.bar(ax=axes[2,1], rot=0).set_title('Net Income From Continuing Ops')
            plt.show()
        
    else:
        total_revenue[symbol] = financials[symbol,'Total Revenue']
        cost_of_revenue[symbol] = financials[symbol,'Cost of Revenue']
        general_expenses[symbol] = financials[symbol, 'Selling General and Administrative']
        research_development[symbol] = financials[symbol,'Research Development']
        operating_profit[symbol] = financials[symbol,'Operating Income or Loss']
        net_income[symbol] = financials[symbol,'Net Income From Continuing Ops']

        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15,15))
        total_revenue.plot.bar(ax=axes[0,0], rot=0).set_title('Total Revenue')
        cost_of_revenue.plot.bar(ax=axes[0,1], rot=0).set_title('Cost of Revenue (COGS)')
        general_expenses.plot.bar(ax=axes[1,0], rot=0).set_title('Selling, General and Administrative Expenses (SG&A)')
        research_development.plot.bar(ax=axes[1,1], rot=0).set_title('Research Development')
        operating_profit.plot.bar(ax=axes[2,0], rot=0).set_title('Operating Income or Loss')
        net_income.plot.bar(ax=axes[2,1], rot=0).set_title('Net Income From Continuing Ops')
        plt.show()

def cashflow_analysis(cashflows, symbol=0, log=False):    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

    else:
        print('Using Manual Input.')
        
    net_income = pd.DataFrame(index=cashflows.index)
    total_operating_activities = pd.DataFrame(index=cashflows.index)
    total_investing_activities = pd.DataFrame(index=cashflows.index)
    total_financing_activities = pd.DataFrame(index=cashflows.index)
    operating_profit = pd.DataFrame(index=cashflows.index)
    net_income = pd.DataFrame(index=cashflows.index)
        
    
    if len(str(symbol)) > 6:
        if log == True:
            for x in symbol:
                if x in cashflows:
                    try:
                        net_income[x] = np.log(cashflows[x,'Net Income'])
                        total_operating_activities[x] = np.log(cashflows[x,'Total Cash Flow From Operating Activities'])
                        total_investing_activities[x] = np.log(cashflows[x, 'Total Cash Flows From Investing Activities'])
                        total_financing_activities[x] = np.log(cashflows[x,'Total Cash Flows From Financing Activities'])
                
                    except KeyError:
                        continue
                    

            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
            net_income.plot.bar(ax=axes[0,0], rot=0).set_title('Net Income')
            total_operating_activities.plot.bar(ax=axes[0,1], rot=0).set_title('Total Cash Flow From Operating Activities')
            total_investing_activities.plot.bar(ax=axes[1,0], rot=0).set_title('Total Cash Flows From Investing Activities')
            total_financing_activities.plot.bar(ax=axes[1,1], rot=0).set_title('Total Cash Flows From Financing Activities')
            plt.show()

        else:
            for x in symbol:
                if x in cashflows:
                    try:
                        net_income[x] = cashflows[x,'Net Income']
                        total_operating_activities[x] = cashflows[x,'Total Cash Flow From Operating Activities']
                        total_investing_activities[x] = cashflows[x, 'Total Cash Flows From Investing Activities']
                        total_financing_activities[x] = cashflows[x,'Total Cash Flows From Financing Activities']

                    except KeyError:
                        continue

            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
            net_income.plot.bar(ax=axes[0,0], rot=0).set_title('Net Income')
            total_operating_activities.plot.bar(ax=axes[0,1], rot=0).set_title('Total Cash Flow From Operating Activities ')
            total_investing_activities.plot.bar(ax=axes[1,0], rot=0).set_title('Total Cash Flows From Investing Activities')
            total_financing_activities.plot.bar(ax=axes[1,1], rot=0).set_title('Total Cash Flows From Financing Activities')
            plt.show()
        
    else:
        net_income[symbol] = cashflows[symbol,'Net Income']
        total_operating_activities[symbol] = cashflows[symbol,'Total Cash Flow From Operating Activities']
        total_investing_activities[symbol] = cashflows[symbol, 'Total Cash Flows From Investing Activities']
        total_financing_activities[symbol] = cashflows[symbol,'Total Cash Flows From Financing Activities']

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        net_income.plot.bar(ax=axes[0,0], rot=0).set_title('Net Income')
        total_operating_activities.plot.bar(ax=axes[0,1], rot=0).set_title('Total Cash Flow From Operating Activities ')
        total_investing_activities.plot.bar(ax=axes[1,0], rot=0).set_title('Total Cash Flows From Investing Activities')
        total_financing_activities.plot.bar(ax=axes[1,1], rot=0).set_title('Total Cash Flows From Financing Activities')
        plt.show()

def ratio_analysis(ratios, symbol = 0, rotation = False):
    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

    else:
        print('Using Manual Input.')
        
    # Price Ratios
    pe_trailing = pd.DataFrame(index=symbol)
    pe_forward = pd.DataFrame(index=symbol)
    peg_ratio = pd.DataFrame(index=symbol)
    price_sales = pd.DataFrame(index=symbol)
    price_book = pd.DataFrame(index=symbol)
    book_value_per_share = pd.DataFrame(index=symbol)
    
    # Profitability Ratios
    return_on_assets = pd.DataFrame(index=symbol)
    return_on_equity = pd.DataFrame(index=symbol)
    profit_margin = pd.DataFrame(index=symbol)
    beta = pd.DataFrame(index=symbol)
    
    # Liquidity
    current_ratio = pd.DataFrame(index=symbol)
    debt_to_equity = pd.DataFrame(index=symbol)
    
    pe_trailing = ratios.T['Trailing P/E']
    pe_forward = ratios.T['Forward P/E 1']
    peg_ratio = ratios.T['PEG Ratio (5 yr expected) 1']
    price_sales = ratios.T['Price/Sales (ttm)']
    price_book = ratios.T['Price/Book (mrq)']
    book_value_per_share = ratios.T['Book Value Per Share (mrq)']
    return_on_assets = ratios.T['Return on Assets (ttm)']
    return_on_equity = ratios.T['Return on Equity (ttm)']
    profit_margin = ratios.T['Profit Margin']
    beta = ratios.T['Beta (3Y Monthly)']
    current_ratio = ratios.T['Current Ratio (mrq)']
    debt_to_equity = ratios.T['Total Debt/Equity (mrq)']
    
    if rotation == False:
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        pe_trailing.sort_values().plot.bar(ax=axes[0,0], rot=0).set_title('P/E Trailing')    
        pe_forward.sort_values().plot.bar(ax=axes[0,1], rot=0).set_title('P/E Forward')
        peg_ratio.sort_values().plot.bar(ax=axes[1,0], rot=0).set_title('PEG Ratio')
        price_sales.sort_values().plot.bar(ax=axes[1,1], rot=0).set_title('Price/Sales')
        plt.show()

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        price_book.sort_values().plot.bar(ax=axes[0,0], rot=0).set_title('Price/Book')
        book_value_per_share.sort_values().plot.bar(ax=axes[0,1], rot=0).set_title('Book Value per Share')
        return_on_assets.sort_values().plot.bar(ax=axes[1,0], rot=0).set_title('Return on Assets (ROA)')
        return_on_equity.sort_values().plot.bar(ax=axes[1,1], rot=0).set_title('Return on Equity (ROE)')
        plt.show()

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        profit_margin.sort_values().plot.bar(ax=axes[0,0], rot=0).set_title('Net Profit Margin')
        beta.sort_values().plot.bar(ax=axes[0,1], rot=0).set_title('Beta')
        current_ratio.sort_values().plot.bar(ax=axes[1,0], rot=0).set_title('Current Ratio')
        debt_to_equity.sort_values().plot.bar(ax=axes[1,1], rot=0).set_title('Debt to Equity')
        
        
    else:
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        pe_trailing.sort_values().plot.bar(ax=axes[0,0]).set_title('P/E Trailing')    
        pe_forward.sort_values().plot.bar(ax=axes[0,1]).set_title('P/E Forward')
        peg_ratio.sort_values().plot.bar(ax=axes[1,0]).set_title('PEG Ratio')
        price_sales.sort_values().plot.bar(ax=axes[1,1]).set_title('Price/Sales')
        plt.show()

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        price_book.sort_values().plot.bar(ax=axes[0,0]).set_title('Price/Book')
        book_value_per_share.sort_values().plot.bar(ax=axes[0,1]).set_title('Book Value per Share')
        return_on_assets.sort_values().plot.bar(ax=axes[1,0]).set_title('Return on Assets (ROA)')
        return_on_equity.sort_values().plot.bar(ax=axes[1,1]).set_title('Return on Equity (ROE)')
        plt.show()

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15,15))
        profit_margin.sort_values().plot.bar(ax=axes[0,0]).set_title('Net Profit Margin')
        beta.sort_values().plot.bar(ax=axes[0,1]).set_title('Beta')
        current_ratio.sort_values().plot.bar(ax=axes[1,0]).set_title('Current Ratio')
        debt_to_equity.sort_values().plot.bar(ax=axes[1,1]).set_title('Debt to Equity')
        
    plt.show()

def stock_data(begin_time, end_time, symbol = 0, read_pickle = False, include_returns = False):
    if read_pickle == True:
        print('Reading last created Pickle')
        stockdata = pd.read_pickle('stockdata')
        return stockdata
    
    else:
        if symbol == 0:
            page = requests.get('https://finance.yahoo.com/trending-tickers')
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
            print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

        else:
            print('Using Manual Input.')

        stockdata = {}

        for s in symbol:

            try:
                if include_returns == True:
                    stockdata['Close', s] = pdr.DataReader(s, 'yahoo', begin_time, end_time)['Close']
                    stockdata['Return', s] = stockdata['Close', s].pct_change(1).round(4).fillna(0)

                else:
                    stockdata[s] = pdr.DataReader(s, 'yahoo', begin_time, end_time)['Close']

            except:
                print('Can not download ' + s + ' ticker data.')

        stockdata = pd.DataFrame(stockdata)
        stockdata = stockdata.fillna(method='ffill', limit=2)
        stockdata = stockdata.fillna(method='bfill', limit=2)
        stockdata = stockdata.fillna(0)
        stockdata = stockdata[~ stockdata.index.duplicated()]
        stockdata = stockdata.reindex(sorted(stockdata.columns), axis=1)

        stockdata.to_pickle('stockdata')
                        
        return stockdata

def correlation_matrix(stock_data, symbol = 0, graph = False):
    correlation_matrix = pd.DataFrame()
    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')
    
    if len(str(symbol)) > 6:
        for s in symbol:
            try:
                correlation_matrix[s] = stock_data['Return', s]
        
            except KeyError:
                print('Could not add ' + s + ' to Matrix')

        if len(correlation_matrix) == 0:
            print('Please set "include_returns" to True in stockdata function.')
        
        correlation_matrix = round(correlation_matrix.corr(), 2)
    
        if graph == True:
            plt.figure(figsize=(20,20))
            sns.heatmap(correlation_matrix,
                    annot = True,
                    cmap = "Reds",
                    annot_kws = {'size':8})

            plt.xticks(rotation = 90)
            plt.yticks(rotation = 0)
            plt.show()
            
        return correlation_matrix
        
    else:
        print('Selected only one company therefore can not create a matrix.')

def rss_feed(symbol = 0, read_pickle = False):    
    if read_pickle == True:
        print('Reading last created Pickle')
        cashflows = pd.read_pickle('cashflows')
        return cashflows
    
    else:
        news_feed = {}

    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

    else:
        print('Using Manual Input.')

    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)
    
    if len(str(symbol)) > 6:
        for s in symbol:
            news_feed[s,'Title'] = []
            news_feed[s,'Link'] = []

            feed = fp.parse('http://finance.yahoo.com/rss/headline?s=' + s)


            # RSS Feed Data
            for post in feed['entries']:
                try:
                    news_feed[s,'Title'].append(post.title)
                    news_feed[s,'Link'].append(post.link)

                except KeyError:
                    continue
    else:
        news_feed[symbol,'Title'] = []
        news_feed[symbol,'Link'] = []

        feed = fp.parse('http://finance.yahoo.com/rss/headline?s=' + symbol)


        # RSS Feed Data
        for post in feed['entries']:
            try:
                news_feed[symbol,'Title'].append(post.title)
                news_feed[symbol,'Link'].append(post.link)

            except KeyError:
                continue
    try:
        news_feed = pd.DataFrame(news_feed.values(), index=news_feed.keys()).transpose()
        news_feed.to_pickle('newsfeed')

    except ValueError as e:
        print('Could not convert news_feed to a DataFrame due to: ', e)

    return news_feed