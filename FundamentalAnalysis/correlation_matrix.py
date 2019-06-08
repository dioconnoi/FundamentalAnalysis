def correlation_matrix(stock_data, symbol = 0, graph = False):

    import lxml
    from lxml import html
    import requests
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    correlation_matrix = pd.DataFrame()
    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')
    
    if type(symbol) == list:
        for s in symbol:
            try:
                correlation_matrix[s] = stock_data['Return', s]
        
            except KeyError:
                print('Could not add ' + s + ' to Matrix')

        if len(correlation_matrix) == 0:
            print('Please set "include_returns" to True in stock_data function.')
            return
        
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