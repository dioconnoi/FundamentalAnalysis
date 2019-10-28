# FundamentalAnalysis
This package can scrape financial data from Yahoo Finance for multiple companies. This includes the ratios, balance sheets, income statements, cashflows and stock data. Furthermore, the analysis functions are able identify the state of the companies over the last years and how they are performing against each other.

**NOTE: This library currently is not able to retrieve Fundamentals data (balance sheets, income statements and cashflows) due to a large overhaul of the Yahoo Fundamentals page. Suggestions how to fix this are highly appreciated.**

**NOTE2: I plan to fix the package at the end of the year.**

## Functions
A short description of the available functions within the package. Please see the docstrings for further explanation.

- `summary()`
   - Scapes data from the 'homepage' of a ticker ([example](https://finance.yahoo.com/quote/TSLA?p=TSLA)), alters text (%, k, M, B) to ensure everything is seen as a float or integer and puts everything in a DataFrame for comparison.
- `balance_sheet()`
   - Scrapes data from the Financials > Balance Sheet page and orders it in a DataFrame.
- `income_statement()`
   - Scrapes data from the Financials > Income Statement page and orders it in a DataFrame. 
- `cashflows()`
   - Scrapes data from the Financials > Cash Flows page and orders it in a DataFrame.
- `ratios()`
   - Scrapes data from the Statistics page, alters text (%, k, M, B) to ensure everything is seen as a float or integer and puts everything in a DataFrame for comparison.
- `balance_sheet_analysis()`
   - Uses data from `balance_sheet()` to create several graphs that show the trend over time.
- `income_statement_analysis()`
   - Uses data from `income_statement()` to create several graphs that show the trend over time.
- `cashflow_analysis()`
   - Uses data from `cashflows()` to create several graphs that show the trend over time.
- `ratio_analysis()`
   - Uses data from `ratios()` to create several graphs that show the ratios right now.
- `stock_data()`
   - Retrieves stock data based on the `pandas_datareader` library. Extras include the recognition of private companies to prevent a sudden stop as well as the calculation of returns.
- `correlation_matrix()`
   - A matrix that uses input from `stock_data()` to calculate correlations between the symbols as well as visually show this in a graph when `graph=True`.
- `rss_feed()`
   - News obtained from Yahoo Finance RSS for each chosen ticker. Can potentially be useful to read more about a company without leaving Python.
   
Addition: leaving the ticker field blank will cause the functions to download the [most trending tickers](https://finance.yahoo.com/trending-tickers/) according to Yahoo Finance.

## Installation
1. Install Package
   - Command Prompt: `pip install FundamentalAnalysis`
   - Jupyter Notebook: `!pip install FundamentalAnalysis`
2. `import FundamentalAnalysis as fa`

## Example usage
Collect data from Yahoo Finance including balance sheets, income statements, cashflows, ratios and stock data of all selected tickers.

```
import FundamentalAnalysis as fa

symbol = ['TSLA','AAPL','MSFT']

balance_sheet = fa.balance_sheet(symbol)
income_statement = fa.income_statement(symbol)
cashflows = fa.cashflows(symbol)
ratios = fa.ratios(symbol)
stock_data = fa.stock_data(2015, 2019, symbol, include_returns=True)
```

Afterwards you can compare the numbers between companies or plot them to see posible growth/decline. Next to that, by using one of the analysis functions, you can quickly see most of the important metrics. (i.e. `ratio_analysis(ratios, symbol)`)
