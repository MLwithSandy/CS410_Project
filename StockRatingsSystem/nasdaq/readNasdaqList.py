import pandas as pd


def read_NASDAQ_List():
    column_name = ['Nasdaq Traded', 'Symbol', 'Security Name',
                   'Listing Exchange', 'Market Category', 'ETF',
                   'Round Lot Size', 'Test Issue', 'Financial Status',
                   'CQS Symbol', 'NASDAQ Symbol', 'NextShares']
    list_nsdq_stock = pd.read_table('nasdaqtraded.txt', sep='|', header=0, engine='python')
    print(list_nsdq_stock.sample(5))
    return list_nsdq_stock


def read_NASDAQ_Sector_List():
    list_stock_sector = pd.read_csv('nasdaq-companies.csv', sep=';', header=0, engine='python')
    print(list_stock_sector.sample(5))
    return list_stock_sector


def read_fin_data_2018():
    column_name = ['Symbol', 'Revenue', 'Revenue Growth', 'Cost of Revenue', 'Gross Profit',
                   'R&D Expenses', 'SG&A Expense', 'Operating Expenses', 'Operating Income',
                   'Interest Expense', 'Earnings before Tax', 'Income Tax Expense',
                   'Net Income - Non-Controlling int', 'Net Income - Discontinued ops',
                   'Net Income', 'Preferred Dividends', 'Net Income Com', 'EPS', 'EPS Diluted',
                   'Weighted Average Shs Out', 'Weighted Average Shs Out (Dil)', 'Dividend per Share',
                   'Gross Margin', 'EBITDA Margin', 'EBIT Margin', 'Profit Margin', 'Free Cash Flow margin',
                   'EBITDA', 'EBIT', 'Consolidated Income', 'Earnings Before Tax Margin', 'Net Profit Margin',
                   'Cash and cash equivalents', 'Short-term investments', 'Cash and short-term investments',
                   'Receivables', 'Inventories', 'Total current assets', '"Property, Plant & Equipment Net"',
                   'Goodwill and Intangible Assets', 'Long-term investments', 'Tax assets',
                   'Total non-current assets', 'Total assets', 'Payables', 'Short-term debt',
                   'Total current liabilities', 'Long-term debt', 'Total debt', 'Deferred revenue',
                   'Tax Liabilities', 'Deposit Liabilities', 'Total non-current liabilities',
                   'Total liabilities', 'Other comprehensive income', 'Retained earnings (deficit)',
                   'Total shareholders equity', 'Investments', 'Net Debt', 'Other Assets',
                   'Other Liabilities', 'Depreciation & Amortization', 'Stock-based compensation',
                   'Operating Cash Flow', 'Capital Expenditure', 'Acquisitions and disposals',
                   'Investment purchases and sales', 'Investing Cash flow', 'Issuance (repayment) of debt',
                   'Issuance (buybacks) of shares', 'Dividend payments', 'Financing Cash Flow',
                   'Effect of forex changes on cash', 'Net cash flow / Change in cash',
                   'Free Cash Flow', 'Net Cash/Marketcap', 'priceBookValueRatio',
                   'priceToBookRatio', 'priceToSalesRatio', 'priceEarningsRatio',
                   'priceToFreeCashFlowsRatio', 'priceToOperatingCashFlowsRatio',
                   'priceCashFlowRatio', 'priceEarningsToGrowthRatio', 'priceSalesRatio', 'dividendYield',
                   'enterpriseValueMultiple', 'priceFairValue', 'ebitperRevenue', 'ebtperEBIT', 'niperEBT',
                   'grossProfitMargin', 'operatingProfitMargin', 'pretaxProfitMargin', 'netProfitMargin',
                   'effectiveTaxRate', 'returnOnAssets', 'returnOnEquity', 'returnOnCapitalEmployed', 'nIperEBT',
                   'eBTperEBIT', 'eBITperRevenue', 'payablesTurnover', 'inventoryTurnover', 'fixedAssetTurnover',
                   'assetTurnover', 'currentRatio', 'quickRatio', 'cashRatio', 'daysOfSalesOutstanding',
                   'daysOfInventoryOutstanding', 'operatingCycle', 'daysOfPayablesOutstanding', 'cashConversionCycle',
                   'debtRatio', 'debtEquityRatio', 'longtermDebtToCapitalization', 'totalDebtToCapitalization',
                   'interestCoverage', 'cashFlowToDebtRatio', 'companyEquityMultiplier', 'operatingCashFlowPerShare',
                   'freeCashFlowPerShare', 'cashPerShare', 'payoutRatio', 'operatingCashFlowSalesRatio',
                   'freeCashFlowOperatingCashFlowRatio', 'cashFlowCoverageRatios', 'shortTermCoverageRatios',
                   'capitalExpenditureCoverageRatios', 'dividendpaidAndCapexCoverageRatios',
                   'dividendPayoutRatio', 'Revenue per Share', 'Net Income per Share', 'Operating Cash Flow per Share',
                   'Free Cash Flow per Share',
                   'Cash per Share', 'Book Value per Share', 'Tangible Book Value per Share',
                   'Shareholders Equity per Share',
                   'Interest Debt per Share', 'Market Cap', 'Enterprise Value', 'PE ratio', 'Price to Sales Ratio',
                   'POCF ratio', 'PFCF ratio', 'PB ratio', 'PTB ratio', 'EV to Sales',
                   'Enterprise Value over EBITDA', 'EV to Operating cash flow', 'EV to Free cash flow',
                   'Earnings Yield', 'Free Cash Flow Yield', 'Debt to Equity', 'Debt to Assets', 'Net Debt to EBITDA',
                   'Current ratio', 'Interest Coverage', 'Income Quality', 'Dividend Yield',
                   'Payout Ratio', 'SG&A to Revenue', 'R&D to Revenue', 'Intangibles to Total Assets',
                   'Capex to Operating Cash Flow', 'Capex to Revenue', 'Capex to Depreciation',
                   'Stock-based compensation to Revenue', 'Graham Number', 'ROIC', 'Return on Tangible Assets',
                   'Graham Net-Net', 'Working Capital', 'Tangible Asset Value', 'Net Current Asset Value',
                   'Invested Capital', 'Average Receivables', 'Average Payables', 'Average Inventory',
                   'Days Sales Outstanding', 'Days Payables Outstanding', 'Days of Inventory on Hand',
                   'Receivables Turnover', 'Payables Turnover', 'Inventory Turnover',
                   'ROE', 'Capex per Share', 'Gross Profit Growth', 'EBIT Growth', 'Operating Income Growth',
                   'Net Income Growth', 'EPS Growth',
                   'EPS Diluted Growth', 'Weighted Average Shares Growth', 'Weighted Average Shares Diluted Growth',
                   'Dividends per Share Growth', 'Operating Cash Flow growth', 'Free Cash Flow growth',
                   '10Y Revenue Growth (per Share)', '5Y Revenue Growth (per Share)',
                   '3Y Revenue Growth (per Share)', '10Y Operating CF Growth (per Share)',
                   '5Y Operating CF Growth (per Share)',
                   '3Y Operating CF Growth (per Share)', '10Y Net Income Growth (per Share)',
                   '5Y Net Income Growth (per Share)', '3Y Net Income Growth (per Share)',
                   '10Y Shareholders Equity Growth (per Share)', '5Y Shareholders Equity Growth (per Share)',
                   '3Y Shareholders Equity Growth (per Share)', '10Y Dividend per Share Growth (per Share)',
                   '5Y Dividend per Share Growth (per Share)',
                   '3Y Dividend per Share Growth (per Share)', 'Receivables growth', 'Inventory Growth', 'Asset Growth',
                   'Book Value per Share Growth', 'Debt Growth', 'R&D Expense Growth',
                   'SG&A Expenses Growth', 'Sector', '2019 PRICE VAR [%]', 'Class']
    fin_data = pd.read_table('2018_Financial_Data.csv', sep=',', header=0, engine='python')
    fin_data.columns = column_name
    print(fin_data.head(5))
    return fin_data


def main():
    list_nsdq_stock = read_NASDAQ_List();
    list_nsdq_stock_symbol = list_nsdq_stock[['Symbol', 'Security Name']]
    fin_data = read_fin_data_2018()
    fin_data_symbol = fin_data['Symbol']

    stock_sector = read_NASDAQ_Sector_List();
    stock_sector_symbol = stock_sector[['Symbol', 'Sector']].fillna('')
    # print(stock_sector_symbol.head(20))

    # common stocks in fin_data and list_nsdq_stock

    list_nsdq_stock_symbol_sector = pd.merge(list_nsdq_stock_symbol, stock_sector_symbol
                                             , how='inner'
                                             , on=['Symbol', 'Symbol'])
    list_nsdq_fin_data_symbol = pd.merge(fin_data_symbol, list_nsdq_stock_symbol_sector, how='inner', on=['Symbol', 'Symbol'])

    print(list_nsdq_fin_data_symbol.head(20))
    print(len(list_nsdq_fin_data_symbol))
    list_nsdq_fin_data_symbol.to_csv(r'nasdaq_result_list.csv', index=False)
    return


if __name__ == '__main__':
    main()
