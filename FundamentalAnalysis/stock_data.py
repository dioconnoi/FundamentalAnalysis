def stock_data(begin_time, end_time, symbol = 0, write_pickle = False, read_pickle = False, include_returns = False):
    
    import lxml
    from lxml import html
    import requests
    import numpy as np
    import pandas as pd
    import pandas_datareader as pdr
    from pandas_datareader._utils import RemoteDataError
    import pickle

    if read_pickle == True:
        stockdata = pd.read_pickle('stockdata')
        return stockdata
    
    else:
        if symbol == 0:
            page = requests.get('https://finance.yahoo.com/trending-tickers')
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
            print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')

        stockdata = {}
        
        if type(symbol) == list:
            for s in symbol:
                try:
                    if include_returns == True:
                        stockdata['Close', s] = pdr.DataReader(s, 'yahoo', begin_time, end_time)['Close']
                        stockdata['Return', s] = stockdata['Close', s].pct_change(1).round(4).fillna(0)

                    else:
                        stockdata[s] = pdr.DataReader(s, 'yahoo', begin_time, end_time)['Close']

                except:
                    print('Can not download ' + s + ' ticker data.')
                    
        else:
            try:
                if include_returns == True:
                    stockdata['Close', symbol] = pdr.DataReader(symbol, 'yahoo', begin_time, end_time)['Close']
                    stockdata['Return', symbol] = stockdata['Close', symbol].pct_change(1).round(4).fillna(0)

                else:
                    stockdata[symbol] = pdr.DataReader(symbol, 'yahoo', begin_time, end_time)['Close']

            except:
                print('Can not download ' + symbol + ' ticker data.')

        stockdata = pd.DataFrame(stockdata)
        stockdata = stockdata.fillna(method='ffill', limit=2)
        stockdata = stockdata.fillna(method='bfill', limit=2)
        stockdata = stockdata[~ stockdata.index.duplicated()]
        stockdata = stockdata.reindex(sorted(stockdata.columns), axis=1)

        if write_pickle == True:
            stockdata.to_pickle('stockdata')
                        
        return stockdata