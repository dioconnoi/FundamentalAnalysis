# Yahoo Financial Statement Collector
A procedure to relatively quickly collect all Financial Data (Balance Sheet, Income Statement &amp; Cashflows) of pre-selected companies. It makes use of Yahoo Finance that collects data over the last four years. Therefore, this script is also limited to that. Potential optimizations can and should be done when working with hundreds of companies at the same time. 

The script leaves a lot of room to perform a quantitative industry analysis. Next to that, by also gathering Stock Data, the analysis can be further extended. There is something to say about that these statistics are also given within Yahoo Finance. Thus, you could also scrape them from there via similar methods.

Financial Statements of (most) S&P500 companies also included as Excel files. These tickers are collected via a similar method as the main file. The code for this can be found here and is based on the code from Sentdex: 

```
def save_sp500_tickers():
  resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  soup = bs.BeautifulSoup(resp.text, 'lxml') # Don't need to add LXML (but it will show error)

  # If there are more tables, you need to specify the class
  table = soup.find('table', {'class':'wikitable sortable'})
  tickers = []
  
  for row in table.findAll('tr') [1:]: # tr is table row
    ticker = row.findAll('td')[0].text # td is table column
    mapping = str.maketrans(".","-")
    ticker = ticker.translate(mapping)
    tickers.append(ticker)
  
  return tickers

save_sp500_tickers()
```
