def rss_feed(symbol = 0, write_pickle = True, read_pickle = False):  

    import lxml
    from lxml import html
    import requests
    import numpy as np
    import pandas as pd
    import feedparser as fp
    import pickle 

    if read_pickle == True:
        news_feed = pd.read_pickle('newsfeed')
        return news_feed
    
    else:
        news_feed = {}

        if symbol == 0:
            page = requests.get('https://finance.yahoo.com/trending-tickers')
            tree = html.fromstring(page.content)
            table = tree.xpath('//table')
            symbol = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]['Symbol'].to_list()
            print('No input is given thus using the Trending Tickers from Yahoo Finance: https://finance.yahoo.com/trending-tickers')
    
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
        
        if write_pickle == True:
            news_feed.to_pickle('newsfeed')

    except ValueError as e:
        print('Could not convert news_feed to a DataFrame due to: ', e)

    return news_feed