# src/fetch/api_fetch.py
from dotenv import load_dotenv
    load_dotenv()
import pandas as pd
from datetime import date
import finnhub as fh
import yfinance as yf
from yahooquery import Ticker as yq
import time

#Notes
#YahooQuery vs yfinance 
#   Yahoo Query is better than yfinance as it is a more stable public API 
#   rather than the webscraping of yfinance which fall over from time to time

def fn_yqratios(lst_tickers,v_sleep):
    time.sleep(v_sleep)
    yq_tckrs = yq(lst_tickers,asynchronous = True)
    lst_df_ratio = []
    lst_ratios_order = ["RunDate","CurrentRatio","QuickRatio","NPM","OPM","GPM","ROA","ROE","EPS","PE","ForwardPE","DividendYield","InsiderShareNet"]
    lst_ratio_numbers = ["CurrentRatio","QuickRatio","NPM","OPM","GPM","ROA","ROE","EPS","PE","ForwardPE","DividendYield","InsiderShareNet"]
    for lp_tck in lst_tickers:
        dct_key = yq_tckrs.key_stats.get(lp_tck,{})
        dct_finandata = yq_tckrs.financial_data.get(lp_tck,{})
        dct_insiders = yq_tckrs.share_purchase_activity.get(lp_tck,{})#[lp_tck]
        dct_summary = yq_tckrs.summary_detail.get(lp_tck,{})#[lp_tck]
        lst_yq_dct = [dct_key,dct_finandata,dct_insiders,dct_summary]
        check_dictionary = all(isinstance(lp_dct,dict) for lp_dct in lst_yq_dct)
        if check_dictionary:		
            dct_ratios = {
            #"Ticker": lp_tck,
            #"PriceDate": dct_key.get("lastFiscalYearEnd"),
            #"Price": dct_finandata.get("currentPrice"),
            "CurrentRatio": dct_finandata.get("currentRatio"),
            "QuickRatio": dct_finandata.get("quickRatio"),
            "NPM": dct_finandata.get("profitMargins"),
            "OPM": dct_finandata.get("operatingMargins"),
            "GPM": dct_finandata.get("grossMargins"),
            "ROA": dct_finandata.get("returnOnAssets"),
            "ROE": dct_finandata.get("returnOnEquity"),
            #"ROCE": dct_finandata.get("returnOnCapitalEmployed"),
            #"InventoryTurnover": dct_finandata.get("inventoryTurnover"),
            #"AssetTurnover": dct_finandata.get("totalAssetsPerShare"),
            #"ReceivablesTurnover": dct_finandata.get("receivablesTurnover"),
            #"PayablesTurnover": dct_finandata.get("payablesTurnover"),
            "EPS": dct_key.get("trailingEps"),
            "PE": dct_summary.get("trailingPE"),
            "ForwardPE": dct_summary.get("forwardPE"),
            "DividendYield": dct_summary.get("dividendYield"),
            "InsiderShareNet": dct_insiders.get("netPercentInsiderShares"),
            }		
            df_lp = pd.DataFrame([dct_ratios.values()],columns=dct_ratios.keys())
            df_lp["Ticker"] = lp_tck
            df_lp["RunDate"] = date.today().strftime("%Y-%m-%d")
            df_lp_set = df_lp.set_index("Ticker").reindex(columns=lst_ratios_order)
            df_lp_set[lst_ratio_numbers] = df_lp_set[lst_ratio_numbers].apply(pd.to_numeric,errors="coerce")
            lst_df_ratio.append(df_lp_set)
        else:
            pass
    try:
        df_ratio = pd.concat(lst_df_ratio)
    except:#If all tickers are not found. Create a blank df
        df_ratio = "BLANK"
        print("No dictionaries found in batch")		
    return df_ratio

def fn_testfhfinancials(lst_tickers):
    
    # Setup client
    v_fh_api_key = 'd1oilv9r01quemd98tc0d1oilv9r01quemd98tcg'
    v_fhclient = fh.Client(api_key=v_fh_api_key)

    # Function to get financial statements
    def get_financials(ticker):
        try:
            data = v_fhclient.financials_reported(symbol=ticker, freq='annual')
            reports = data.get('data', [])
            return reports
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    # Fetch and display current ratios
    for ticker in lst_tickers:
        v_financials = get_financials(ticker)
        if v_financials is not None:
            print(v_financials)
        else:
            print(f"{ticker}: Financials not found.")

def fn_fhratios(lst_tickers):
    
    # Setup client
    v_fh_api_key = 'd1oilv9r01quemd98tc0d1oilv9r01quemd98tcg'  # Replace with your actual API key
    v_fhclient = fh.Client(api_key=v_fh_api_key)
    dct_ratios = {}
    # Fetch and display ratios
    for ticker in lst_tickers:
        try:
            time.sleep(1)#sleep to make sure the API does not overload
            data = v_fhclient.company_basic_financials(symbol=ticker, metric='all')
            #Insider sentiment v_fhclient.stock_insider_sentiment()
            metrics = data.get('metric', {})
            v_current = metrics.get('currentRatioQuarterly')
            v_quick = metrics.get('quickRatioQuarterly')
            v_eps = metrics.get('epsTTM')
            v_pe = metrics.get('peTTM')
            v_npm = metrics.get('netProfitMarginTTM')
            v_gpm = metrics.get('grossMarginTTM')
            v_opm = metrics.get('operatingMarginTTM')
            v_roa = metrics.get('roaTTM')
            v_roe = metrics.get('roeTTM')
            v_divyield = metrics.get('currentDividendYieldTTM')
            dct_ratio = {'CurrentRatio':v_current,'QuickRatio':v_quick,
                          'EPS':v_eps,'PE':v_pe,
                          'NetProfitMargin':v_npm,'GrossProfitMargin':v_gpm,'OperatingProfitMargin':v_opm,
                          'ReturnOnAssets':v_roa,'ReturnOnEquity':v_roe,
                          'DividendYield':v_divyield
                          }
            dct_ratios[ticker] = dct_ratio
            
        except Exception as e:
            print(f"Error fetching ratios for {ticker}: {e}")
    return dct_ratios

def fn_fhtickers(v_exch,v_output):
    # Setup client
    v_fh_api_key = 'd1oilv9r01quemd98tc0d1oilv9r01quemd98tcg'
    v_fhclient = fh.Client(api_key=v_fh_api_key)

    #Gat ticker list from exchange
    lst_tickers = v_fhclient.stock_symbols(v_exch)
    df_tickers = pd.DataFrame(lst_tickers)
    df_tickers.to_csv(v_output,index=False)
    print("Run Function: fn_fhtickers")
    