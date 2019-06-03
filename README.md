# Fundamental Analysis Library
By scraping data from Yahoo Finance, a full fundamental analysis can be done on a sector with just the click of a few buttons. Some example images can be found in the 'Examples' folder to understand what the script produces.

*Note: This is a work-in-progess but currently fully operational already. Suggestions are much appreciated.*

## Functions
A short description of the available functions within the package:

- `summary()`
   - Scapes data from the 'homepage' of a ticker ([example](https://finance.yahoo.com/quote/TSLA?p=TSLA)), alters text (%, k, M, B) and puts everything in a neat DataFrame for comparison.
- `balance_sheet()`
   - Scrapes data from the Financials > Balance Sheet page and order it in a DataFrame. Allows for comparison of multiple companies.
- `income_statement()`
   - Scrapes data from the Financials > Income Statement page and order it in a DataFrame. Allows for comparison of multiple companies.
- `cashflows()`
   - Scrapes data from the Financials > Cash Flows page and order it in a DataFrame. Allows for comparison of multiple companies.
- `ratios()`
   - Scrapes data from the Statistics page, , alters text (%, k, M, B) and puts everything in a neat DataFrame for comparison.
- `balance_sheet_analysis()`
   - Uses data from `balance_sheet()` to create several graphs that show the trend over time. Useful to visually indentify the succes/failure of the company without needing to look extensively at the numbers.
- `income_statement_analysis()`
   - Uses data from `income_statement()` to create several graphs that show the trend over time. Useful to visually indentify the succes/failure of the company without needing to look extensively at the numbers.
- `cashflow_analysis()`
   - Uses data from `cashflows()` to create several graphs that show the trend over time. Useful to visually indentify the succes/failure of the company without needing to look extensively at the numbers.
- `ratio_analysis()`
   - Uses data from `ratios()` to create several graphs that show the current ratios. Useful to visually indentify the performance between companies.
- `stock_data()`
   - Retrieves stock data based on the `pandas_datareader` library. Extras include the recognition of private companies to prevent a sudden stop as well as the calculation of returns.
- `correlation_matrix()`
   - A matrix that uses input from `stock_data()` to calculate correlations between the symbols as well as visually show this in a graph when `graph=True`.
- `rss_feed()`
   - News obtained from Yahoo Finance RSS for each chosen symbol. Can potentially be useful to read more about a company without leaving Python.
   
Addition: leaving the symbol field blank will let the function download the [most trending tickers](https://finance.yahoo.com/trending-tickers/) according to Yahoo Finance.

## Installation
1. Download the libary 'FundamentalAnalysis.py'
2. Place it in the same folder as you are working in (or install it in the core)
3. Import the package (`import FundamentalAnalysis as fa`)

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

## To-Do
- [ ] Add Docstrings.
- [ ] Test, Test, TEST!
- [ ] Run an actual analysis and see what is missing
- [ ] Create a fully fledged package that can be used with pip
- [ ] Sort out the description.
