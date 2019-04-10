# Yahoo Financial Statement Collector
A procedure to relatively quickly collect all Financial Data (Balance Sheet, Income Statement &amp; Cashflows) of pre-selected companies. It makes use of Yahoo Finance that collects data over the last four years. Therefore, this script is also limited to that. Potential optimizations can and should be done when working with hundreds of companies at the same time. 

The script leaves a lot of room to perform a quantitative industry analysis. By also gathering Stock Data via pandas-datareader, the analysis can be further extended. There is something to say about that these statistics are also given within Yahoo Finance. Thus, you could also scrape them from there via similar methods.

## Ticker Collection
Financial Statements of some S&P500 companies are also included as Excel files (output from script). These tickers are collected via a similar method as the main file. The code for this can be found below and is based on a codesnippet from Sentdex's tutorials: 

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

##  Stock Data Fetching
With the script below, also the Stock Data can be retrieved. There is no need to set the symbol variable again if you run this code after the main file. Next to that, by adding a column like _['Close']_ after the yf.download function, you can filter out columns like Volumes, High, Low and such.

```
import fix_yahoo_finance as yf  

symbol = ['AMZN','TSLA','GOOGL', 'MSFT', 'AAPL']
begin_time = '2015-01-01'
end_time = '2019-01-01'

data = yf.download(symbol, begin_time, end_time)
````
