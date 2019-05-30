# Fundamental Analysis with Yahoo Finance (WIP)
By scraping data from Yahoo Finance, a full fundamental analysis can be done on a sector with just the click of a few buttons.

## Functions
A short description of the available functions within the package:

- `summary()`
   - Scapes data from the 'homepage' of a ticker ([example](https://finance.yahoo.com/quote/TSLA?p=TSLA)), alters text (%, k, M, B) and puts everything in a neat DataFrame for comparison.
- `balance_sheet()`
   - Scrapes data from the Financials --> Balance Sheet page and order it in a DataFrame. Allows for comparison of multiple companies.
- `income_statement()`
   - Scrapes data from the Financials --> Income Statement page and order it in a DataFrame. Allows for comparison of multiple companies.
- `cashflows()`
   - Scrapes data from the Financials --> Cash Flows page and order it in a DataFrame. Allows for comparison of multiple companies.
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

## To-Do
- [ ] Add Docstrings.
- [ ] Test, Test, TEST!
- [ ] Run an actual analysis and see what is missing
- [ ] Create a fully fledged package that can be used with pip
- [ ] Sort out the description.

*Note: This is very much a work-in-progess but currently quite operational already. Suggestions are much appreciated.*

## Examples
[Balance Sheet](Examples/Balance\Sheet\TSLA.PNG)
