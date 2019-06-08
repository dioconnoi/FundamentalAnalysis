def income_statement_analysis(financials, symbol = 0, log=False):

    import lxml
    from lxml import html
    import requests
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    if symbol == 0:
        page = requests.get('https://finance.yahoo.com/trending-tickers')
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
        print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')
        
    total_revenue = pd.DataFrame(index=financials.index)
    cost_of_revenue = pd.DataFrame(index=financials.index)
    general_expenses = pd.DataFrame(index=financials.index)
    research_development = pd.DataFrame(index=financials.index)
    operating_profit = pd.DataFrame(index=financials.index)
    net_income = pd.DataFrame(index=financials.index)
        
    
    if type(symbol) == list:
        if log == True:
            import warnings
            warnings.filterwarnings('ignore', category=RuntimeWarning)
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