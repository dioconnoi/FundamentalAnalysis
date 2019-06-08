def income_statement(symbol = 0, write_pickle = False, read_pickle = False):
    
    import lxml
    from lxml import html
    import requests
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import pickle
    
    if read_pickle == True:
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
        
    if type(symbol) == list:
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
        
        if write_pickle == True:
            financials.to_pickle('income_statement')

    except ValueError as e:
        print('Could not convert to a DataFrame due to: ', e)

    return financials