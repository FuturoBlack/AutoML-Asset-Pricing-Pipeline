#==============================================================================
# Copyright (C) 2025 Mohammad Rasoul Mostafavi Marian
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#==============================================================================

#==============================================================================
#                  --- MOSTAFAVI'S THESIS PIPELINE SCRIPT ---
#
# Author: Mohammad Rasoul Mostafavi Marian
# Email: m.rasoulmostafavi@gmail.com
# Last Edited: 2025 October 15
# Version: 1.0
#==============================================================================

#==============================================================================
# STEP 1: INITIALIZE ENVIRONMENT
#==============================================================================
print("===========================================================================================")
print("STEP 1: Installing and Importing Required Libraries...")
print("===========================================================================================")
try:
    import subprocess
    import sys

    #--> Sub-step 1.1: Installing Required Libraries:
    print("--> Sub-step 1.1: Installing Required Libraries...")
    software_to_install = sorted([
        'h2o','java','matplotlib','numpy','pandas','pandas-datareader','polars',
        'psutil','pyarrow','scikit-learn','scipy','shap','statsmodels','ta','yfinance'
    ])
    installation_failed = False
    for software in software_to_install:
        try:
            if software == 'java':
                try:
                    subprocess.check_call(['java', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"[SUCCESS] Installed '{software}' (Pre-installed)")
                except:
                    subprocess.check_call(['apt-get', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.check_call(['apt-get', 'install', '-y', 'default-jre'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"[SUCCESS] Installed '{software}'")
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", software, "-q"])
                print(f"[SUCCESS] Installed '{software}'")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"[ERROR] Failed to Install '{software}'")
            installation_failed = True
    if installation_failed:
        raise Exception("One or More Packages Failed to Install.")
    print("[SUCCESS] Sub-step 1.1: Installing Required Libraries Completed Successfully.")

    #--> Sub-step 1.2: Importing Required Libraries:
    print("\n--> Sub-step 1.2: Importing Required Libraries...")
    libraries_to_import = {
        'google.colab': 'from google.colab import files',
        'h2o': 'import h2o',
        'h2o.automl': 'from h2o.automl import H2OAutoML',
        'io': 'import io',
        'logging': 'import logging',
        'matplotlib.colors': 'import matplotlib.colors as mcolors',
        'matplotlib.pyplot': 'import matplotlib.pyplot as plt',
        'numpy': 'import numpy as np',
        'os': 'import os',
        'pandas': 'import pandas as pd',
        'pandas_datareader': 'from pandas_datareader import data as pdr',
        'psutil': 'import psutil',
        'scipy.stats': 'from scipy.stats import norm',
        'shap': 'import shap',
        'sklearn': 'import sklearn',
        'sklearn.linear_model': 'from sklearn.linear_model import LinearRegression',
        'sklearn.metrics': 'from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score',
        'sklearn.preprocessing': 'from sklearn.preprocessing import StandardScaler',
        'statsmodels.tsa.stattools': 'from statsmodels.tsa.stattools import adfuller',
        'ta': 'import ta',
        'time': 'import time',
        'yfinance': 'import yfinance as yf'
    }
    import_failed = False
    for name, statement in sorted(libraries_to_import.items()):
        try:
            exec(statement, globals())
            print(f"[SUCCESS] Imported '{name}'")
        except ImportError as e:
            if name == 'google.colab':
                print(f"[INFO] Skipped Importing '{name}' (Likely Not in a Colab Environment).")
            else:
                print(f"[ERROR] Failed to Import '{name}'. Reason: {e}")
                import_failed = True
    if import_failed:
        raise Exception("One or More Libraries Failed to Import.")
    print("[SUCCESS] Sub-step 1.2: Importing Required Libraries Completed Successfully.")

    IS_ENVIRONMENT_READY = True
    print("\n[SUCCESS] Step 1: Installing and Importing Required Libraries Completed Successfully.")
except Exception as e:
    print(f"\n[ERROR] Library Setup Failed: {e}")
    IS_ENVIRONMENT_READY = False
finally:
    print("===========================================================================================")

#==============================================================================
# STEP 2: VERIFY LOCAL DATA ASSETS
#==============================================================================
print("\n===========================================================================================")
print("STEP 2: Defining Required Internal Data...")
print("===========================================================================================")
try:
    print("Defining Internal Company Data...")
    TICKER_INFO_CSV = """Symbol,   StartDate,   EndDate,   Company
AA,     1995-09-09,   2013-09-23,   Alcoa
AAPL,   2015-03-19,   2025-09-28,   "Apple Inc."
AIG,    2004-04-08,   2008-09-22,   American International Group
ALD,    1995-09-09,   2020-08-31,   AlliedSignal
AMGN,   2020-08-31,   2025-09-28,   Amgen
AMZN,   2024-02-26,   2025-09-28,   Amazon
AXP,    1995-09-09,   2025-09-28,   American Express
BA,     1995-09-09,   2025-09-28,   Boeing
BAC,    2008-02-19,   2013-09-23,   Bank of America
BS,     1995-09-09,   1997-03-17,   Bethlehem Steel
CAT,    1995-09-09,   2025-09-28,   Caterpillar
CRM,    2020-08-31,   2025-09-28,   Salesforce
CSCO,   2009-06-08,   2025-09-28,   Cisco Systems
CVX,    1995-09-09,   1999-11-01,   Chevron
CVX,    2008-02-19,   2025-09-28,   Chevron
DD,     1995-09-09,   2017-09-01,   DuPont
DIS,    1995-09-09,   2025-09-28,   Disney
DOW,    2019-04-02,   2024-11-08,   "Dow Inc."
DWDP,   2017-09-01,   2019-04-02,   DowDuPont
GE,     1995-09-09,   2018-06-26,   General Electric
GS,     2013-09-23,   2025-09-28,   "Goldman Sachs Group, Inc."
GT,     1995-09-09,   1999-11-01,   Goodyear Tire
HD,     1999-11-01,   2025-09-28,   Home Depot
HON,    2020-08-31,   2025-09-28,   Honeywell
HWP,    1997-03-17,   2013-09-23,   Hewlett-Packard
IBM,    1995-09-09,   2025-09-28,   IBM
INTC,   1999-11-01,   2024-11-08,   Intel
IP,     1995-09-09,   2004-04-08,   International Paper
JNJ,    1997-03-17,   2025-09-28,   Johnson & Johnson
JPM,    1995-09-09,   2025-09-28,   JPMorgan Chase
KFT,    2008-09-22,   2012-09-24,   "Kraft Foods Inc."
KO,     1995-09-09,   2025-09-28,   Coca-Cola
MCD,    1995-09-09,   2025-09-28,   McDonald's
MMM,    1995-09-09,   2025-09-28,   3M
MRK,    1995-09-09,   2025-09-28,   Merck
MSFT,   1999-11-01,   2025-09-28,   Microsoft
NKE,    2013-09-23,   2025-09-28,   "Nike, Inc."
NVDA,   2024-11-08,   2025-09-28,   Nvidia
PFE,    2004-04-08,   2020-08-31,   Pfizer
PG,     1995-09-09,   2025-09-28,   Procter & Gamble
RTX,    2020-04-06,   2020-08-31,   Raytheon Technologies
S,      1995-09-09,   1999-11-01,   Sears Roebuck
SBC,    1999-11-01,   2015-03-19,   SBC Communications
SHW,    2024-11-08,   2025-09-28,   Sherwin-Williams
T,      1995-09-09,   2015-03-19,   AT&T
TRV,    1997-03-17,   2009-06-08,   "Travelers Inc."
TRV,    2009-06-08,   2025-09-28,   "The Travelers Companies, Inc."
TX,     1995-09-09,   1997-03-17,   Texaco
UK,     1995-09-09,   1999-11-01,   Union Carbide
UNH,    2012-09-24,   2025-09-28,   UnitedHealth Group
UTX,    1995-09-09,   2020-04-06,   United Technologies
V,      2013-09-23,   2025-09-28,   "Visa Inc."
VZ,     2004-04-08,   2025-09-28,   Verizon Communications
WBA,    2018-06-26,   2024-02-26,   Walgreens Boots Alliance
WMT,    1997-03-17,   2025-09-28,   Walmart
WX,     1995-09-09,   1997-03-17,   Westinghouse Electric
XON,    1995-09-09,   2020-08-31,   Exxon
Z,      1995-09-09,   1997-03-17,   "F. W. Woolworth Company"
"""
    ticker_info_df = pd.read_csv(io.StringIO(TICKER_INFO_CSV), skipinitialspace=True)
    print("[SUCCESS] Internal Company Data Defined.")

    print("Defining Company Name Map...")
    SYMBOL_TO_NAME_MAP = {
        'AA':    'Alcoa',                     'AAPL':  'AppleInc.',           'AIG':   'AmericanInternationalGroup','ALD':   'AlliedSignal',
        'AMGN':  'Amgen',                     'AMZN':  'Amazon',              'AXP':   'AmericanExpress',           'BA':    'Boeing',
        'BAC':   'BankofAmerica',             'BS':    'BethlehemSteel',      'CAT':   'Caterpillar',               'CRM':   'Salesforce',
        'CSCO':  'CiscoSystems',              'CVX':   'Chevron',             'DD':    'DuPont',                    'DIS':   'Disney',
        'DOW':   'DowInc.',                   'DWDP':  'DowDuPont',           'GE':    'GeneralElectric',           'GS':    'GoldmanSachsGroup,Inc.',
        'GT':    'GoodyearTire',              'HD':    'HomeDepot',           'HON':   'Honeywell',                 'HWP':   'HewlettPackard',
        'IBM':   'IBM',                       'INTC':  'Intel',               'IP':    'InternationalPaper',        'JNJ':   'JohnsonJohnson',
        'JPM':   'JPMorganChase',             'KFT':   'KraftFoodsInc.',      'KO':    'CocaCola',                  'MCD':   'McDonalds',
        'MMM':   '3M',                        'MRK':   'Merck',               'MSFT':  'Microsoft',                 'NKE':   'Nike,Inc.',
        'NVDA':  'Nvidia',                    'PFE':   'Pfizer',              'PG':    'ProcterGamble',             'RTX':   'RaytheonTechnologies',
        'S':     'SearsRoebuck',              'SBC':   'SBCCommunications',   'SHW':   'SherwinWilliams',           'T':     'ATT',
        'TRV':   'TheTravelersCompanies,Inc.','TX':    'Texaco',              'UK':    'UnionCarbide',              'UNH':   'UnitedHealthGroup',
        'UTX':   'UnitedTechnologies',        'V':     'VisaInc.',            'VZ':    'VerizonCommunications',     'WBA':   'WalgreensBootsAlliance',
        'WMT':   'Walmart',                   'WX':    'WestinghouseElectric','XON':   'Exxon',                     'Z':     'FWWoolworthCompany',
    }
    print("[SUCCESS] Company Name Map Defined.")

    print("Defining FRED Macroeconomic Data Map...")
    FRED_TICKERS_MAP = {
        '_CPIAUCSL':  'CPIAUCSL',   '_FEDFUNDS':  'FEDFUNDS',   '_GDPC1':    'GDPC1',     '_INDPRO':  'INDPRO',
        '_PPIACO':    'PPIACO',     '_RSAFS':     'RSAFS',      '_UMCSENT':  'UMCSENT',   '_UNRATE':  'UNRATE',
    }
    print("[SUCCESS] FRED Macroeconomic Data Map Defined.")

    print("Defining Global Market Data Map...")
    YFINANCE_TICKERS_MAP = {
        '_Daily_Close_VIX':             '^VIX',    '_Daily_Log_Return_DAX40':        '^GDAXI',   '_Daily_Log_Return_DXY':     'DX-Y.NYB',
        '_Daily_Log_Return_FTSE100':    '^FTSE',   '_Daily_Log_Return_Gold':         'GC=F',     '_Daily_Log_Return_NASDAQ':  '^IXIC',
        '_Daily_Log_Return_Nikkei225':  '^N225',   '_Daily_Log_Return_Russell2000':  '^RUT',     '_Daily_Log_Return_SP500':   '^GSPC',
        '_Daily_Log_Return_WTI':        'CL=F',
    }
    print("[SUCCESS] Global Market Data Map Defined.")

    print("Defining Internal Event Data...")
    EVENTS_DATA_CSV = """Variable,   StartDate,   EndDate,   Event
_EO,    1996-11-05,   1996-11-05,   US Presidential Election 1996
_EO,    2000-11-07,   2000-11-07,   US Presidential Election 2000
_EO,    2004-11-02,   2004-11-02,   US Presidential Election 2004
_EO,    2008-11-04,   2008-11-04,   US Presidential Election 2008
_EO,    2012-11-06,   2012-11-06,   US Presidential Election 2012
_EO,    2016-11-08,   2016-11-08,   US Presidential Election 2016
_EO,    2020-11-03,   2020-11-03,   US Presidential Election 2020
_EO,    2024-11-05,   2024-11-05,   US Presidential Election 2024
_ND,    1995-07-12,   1995-07-16,   Chicago Heat Wave
_ND,    1995-10-04,   1995-10-04,   Hurricane Opal
_ND,    1996-01-06,   1996-01-12,   North American Blizzard of 1996
_ND,    1997-04-17,   1997-05-01,   Red River Flood
_ND,    1998-09-21,   1998-09-29,   Hurricane Georges
_ND,    1999-05-03,   1999-05-03,   Bridge Creek-Moore Tornado Outbreak
_ND,    1999-09-14,   1999-09-16,   Hurricane Floyd
_ND,    2002-01-01,   2003-12-31,   Widespread Drought Period
_ND,    2003-08-14,   2003-08-15,   Northeast Blackout of 2003
_ND,    2004-08-13,   2004-08-14,   Hurricane Charley
_ND,    2004-09-04,   2004-09-24,   Hurricane Ivan
_ND,    2005-08-23,   2005-08-31,   Hurricane Katrina
_ND,    2005-09-20,   2005-09-24,   Hurricane Rita
_ND,    2005-10-18,   2005-10-24,   Hurricane Wilma
_ND,    2008-09-01,   2008-09-15,   Hurricane Ike
_ND,    2010-02-05,   2010-02-06,   North American Blizzard (Snowmageddon)
_ND,    2011-04-25,   2011-04-28,   Super Outbreak of Tornadoes
_ND,    2011-05-21,   2011-05-26,   Joplin Tornado Outbreak
_ND,    2011-08-22,   2011-08-29,   Hurricane Irene
_ND,    2012-01-01,   2012-12-31,   Widespread Drought Period
_ND,    2012-10-22,   2012-11-02,   Hurricane Sandy
_ND,    2013-09-11,   2013-09-15,   Colorado Floods
_ND,    2016-08-12,   2016-08-16,   Louisiana Floods
_ND,    2017-08-17,   2017-09-02,   Hurricane Harvey
_ND,    2017-09-06,   2017-09-12,   Hurricane Irma
_ND,    2017-09-16,   2017-10-02,   Hurricane Maria
_ND,    2017-10-08,   2017-10-31,   Northern California Wildfires
_ND,    2018-09-11,   2018-09-19,   Hurricane Florence
_ND,    2018-10-10,   2018-10-11,   Hurricane Michael
_ND,    2018-11-08,   2018-11-25,   Camp Fire (California)
_ND,    2019-03-13,   2019-04-01,   Midwestern US Floods
_ND,    2019-08-28,   2019-09-06,   Hurricane Dorian
_ND,    2020-08-10,   2020-08-10,   Midwest Derecho
_ND,    2020-08-16,   2020-12-31,   August Complex Fire (California)
_ND,    2020-08-22,   2020-08-29,   Hurricane Laura
_ND,    2021-02-13,   2021-02-17,   Texas Power Crisis (Major Winter Storm)
_ND,    2021-06-26,   2021-07-23,   Western North American Heat Wave
_ND,    2021-08-29,   2021-09-01,   Hurricane Ida
_ND,    2021-12-10,   2021-12-11,   Quad-State Tornado Outbreak
_ND,    2022-09-23,   2022-10-02,   Hurricane Ian
_ND,    2022-12-21,   2022-12-26,   North American winter storm (Elliott)
_PSI,   1995-04-19,   1995-04-19,   Oklahoma City Bombing
_PSI,   1995-11-14,   1995-11-19,   US Government Shutdown
_PSI,   1995-12-16,   1996-01-06,   US Government Shutdown
_PSI,   1998-08-17,   1998-10-15,   Russian Financial Crisis & LTCM Collapse
_PSI,   1998-12-19,   1999-02-12,   Impeachment of President Bill Clinton
_PSI,   1999-07-01,   1999-12-31,   Y2K Scare Peak Period
_PSI,   2000-03-10,   2002-10-09,   Dot-com Bubble Burst Period
_PSI,   2001-09-11,   2001-09-11,   September 11th Terrorist Attacks
_PSI,   2001-10-07,   2001-10-07,   Start of War in Afghanistan
_PSI,   2001-12-02,   2002-07-21,   Enron & WorldCom Corporate Scandals
_PSI,   2003-03-19,   2003-03-19,   Start of Iraq War
_PSI,   2008-09-15,   2009-06-30,   Global Financial Crisis Peak Instability
_PSI,   2010-04-27,   2012-12-31,   European Sovereign Debt Crisis Impact Period
_PSI,   2011-01-14,   2011-10-23,   Arab Spring Peak Impact
_PSI,   2011-07-01,   2011-08-08,   US Debt Ceiling Crisis & Credit Rating Downgrade
_PSI,   2013-05-22,   2013-08-31,   Fed Taper Tantrum
_PSI,   2013-10-01,   2013-10-17,   US Government Shutdown
_PSI,   2014-08-09,   2014-11-30,   Ferguson Unrest Period
_PSI,   2016-06-23,   2016-06-23,   Brexit Referendum
_PSI,   2018-01-20,   2018-01-22,   US Government Shutdown
_PSI,   2018-02-09,   2018-02-09,   US Government Shutdown (Short)
_PSI,   2018-05-08,   2018-05-08,   US Withdrawal from Iran Nuclear Deal
_PSI,   2018-12-22,   2019-01-25,   US Government Shutdown (Longest)
_PSI,   2019-12-18,   2020-02-05,   First Impeachment of President Donald Trump
_PSI,   2020-02-20,   2020-04-07,   COVID-19 Stock Market Crash
_PSI,   2020-03-11,   2020-03-13,   WHO Declares Pandemic & US Declares National Emergency
_PSI,   2020-05-25,   2020-08-31,   George Floyd Protests Peak Period
_PSI,   2021-01-06,   2021-01-06,   January 6th Capitol Attack
_PSI,   2021-01-13,   2021-02-13,   Second Impeachment of President Donald Trump
_PSI,   2021-08-15,   2021-08-31,   Fall of Kabul & Afghanistan Withdrawal
_PSI,   2022-02-24,   2022-02-24,   Start of Russia-Ukraine Invasion
_PSI,   2023-03-10,   2023-05-01,   US Regional Banking Crisis (SVB Collapse)
_PSI,   2023-05-15,   2023-06-03,   US Debt Ceiling Crisis 2023
_TWI,   2018-03-22,   2020-01-15,   Main Period of US-China Trade War and Tariffs
"""
    print("[SUCCESS] Internal Event Data Defined.")

    print("Defining Color Palette...")
    COLOR_PALETTE = {
        'Color1': '#FFFFFF',   # White
        'Color2': '#000000',   # Black
        'Color3': '#E7E6E6',   # Light Gray
        'Color4': '#4472C4',   # Blue
        'Color5': '#70AD47',   # Green
        'Color6': '#5B9BD5',   # Light Blue
        'Color7': '#92D050',   # Light Green
        'Color8': '#264478',   # Dark Blue
        'Color9': '#006400',   # Dark Green
    }
    print("[SUCCESS] Color Palette Defined.")

    ARE_DATA_ASSETS_READY = True
    print("\n[SUCCESS] Step 2: Defining Required Internal Data Completed Successfully.")
except Exception as e:
    print(f"\n[ERROR] Internal Data Setup Failed: {e}")
    ARE_DATA_ASSETS_READY = False
finally:
    print("===========================================================================================")

#==============================================================================
# STEP 3: CREATE BASE TIME-INDEXED DATAFRAME
#==============================================================================
def create_base_dataframe(start_date, end_date):
    print("\n===========================================================================================")
    print("STEP 3: Creating Base DataFrame with Time Features...")
    print("===========================================================================================")
    try:
        #--> Sub-step 3.1: Creating Base DataFrame:
        print("--> Sub-step 3.1: Creating Base DataFrame...")
        date_index = pd.to_datetime(pd.date_range(start=start_date, end=end_date, freq='D'))
        df = pd.DataFrame(index=date_index)
        df['_Date'] = df.index
        print(f"[SUCCESS] Base DataFrame with '_Date' Column Created for the Range {start_date} to {end_date}.")
        print("[SUCCESS] Sub-step 3.1: Creating Base DataFrame Completed Successfully.")

        #--> Sub-step 3.2: Generating Time Features:
        print("\n--> Sub-step 3.2: Generating Time Features...")
        features_to_create = {
            '_Year': lambda d: d.index.year, 
            '_Month': lambda d: d.index.month, 
            '_Day': lambda d: d.index.day,
            '_WeekOfYear': lambda d: d.index.isocalendar().week.astype(int), 
            '_DayOfWeek': lambda d: d.index.dayofweek
        }
        for name, func in features_to_create.items():
            df[name] = func(df)
            print(f"[SUCCESS] Time Feature Column '{name}' Created.")
        df.reset_index(drop=True, inplace=True)
        print("[SUCCESS] Sub-step 3.2: Generating Time Features Completed Successfully.")

        print("\n[SUCCESS] Step 3: Creating Base DataFrame with Time Features Completed Successfully.")
        return df
    except Exception as e:
        print(f"\n[ERROR] Failed to Create the Base DataFrame: {e}")
        return None
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 4: BATCH DOWNLOAD CORPORATE OHLCV DATA - WARM-UP
#==============================================================================
def download_ohlcv_data_batch(ticker_info_df, start_date, end_date):
    print("\n===========================================================================================")
    print("STEP 4: Batch Downloading Corporate OHLCV Data Using Warm-Up...")
    print("===========================================================================================")
    try:
        symbol_to_company_map = pd.Series(ticker_info_df.Company.values, index=ticker_info_df.Symbol).to_dict()
        unique_symbols = sorted(ticker_info_df['Symbol'].unique().tolist())
        logging.getLogger('yfinance').setLevel(logging.CRITICAL)
        warm_up_start_date = pd.to_datetime(start_date) - pd.Timedelta(days=110)
        downloaded_data = yf.download(unique_symbols, start=warm_up_start_date, end=end_date, progress=False, auto_adjust=True)
        logging.getLogger('yfinance').setLevel(logging.WARNING)
        success_count, incomplete_count, failure_count = 0, 0, 0
        for symbol in unique_symbols:
            company_name = symbol_to_company_map.get(symbol, "Unknown Company")
            if isinstance(downloaded_data.columns, pd.MultiIndex) and symbol in downloaded_data['Close'].columns and not downloaded_data['Close'][symbol].isnull().all():
                symbol_entries = ticker_info_df[ticker_info_df['Symbol'] == symbol]
                requested_start, requested_end = pd.to_datetime(symbol_entries['StartDate'].min()), pd.to_datetime(symbol_entries['EndDate'].max())
                actual_start, actual_end = downloaded_data['Close'][symbol].first_valid_index(), downloaded_data['Close'][symbol].last_valid_index()
                if actual_start <= requested_start and actual_end >= requested_end:
                    print(f"[SUCCESS] Downloaded Corporate OHLCV Data for Symbol: {symbol} ({company_name}). Full Period Covered.")
                    success_count += 1
                else:
                    missing_at_start, missing_at_end = max(0, (actual_start - requested_start).days), max(0, (requested_end - actual_end).days)
                    print(f"[SUCCESS] Downloaded Incomplete Corporate OHLCV Data for Symbol: {symbol} ({company_name}). Missing {missing_at_start} Days at Start and {missing_at_end} Days at End.")
                    incomplete_count += 1
            else:
                print(f"[ERROR] Failed to Download Any Corporate OHLCV Data for Symbol: {symbol} ({company_name}).")
                failure_count += 1

        print(f"\n[SUCCESS] Step 4: Batch Downloading Corporate OHLCV Data Completed Successfully. (Summary: {success_count} Symbols Fully Downloaded, {incomplete_count} Symbols Incompletely Downloaded, {failure_count} Symbols Failed).")
        return downloaded_data
    except Exception as e:
        logging.getLogger('yfinance').setLevel(logging.WARNING)
        print(f"\n[ERROR] A Critical Error Occurred During the Batch Download Process: {e}")
        return None
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 5: ENGINEER AND INTEGRATE CORPORATE OHLCV FEATURES
#==============================================================================
def calculate_features_for_one_stock(df: pd.DataFrame):
    try:
        df = df.resample('D').asfreq()
        price_cols = [c for c in df.columns if 'Volume' not in c]
        df[price_cols] = df[price_cols].ffill()
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].fillna(0)
        features = pd.DataFrame(index=df.index)
        safe_open = df['Open'].clip(lower=1e-9)
        safe_high = df['High'].clip(lower=1e-9)
        safe_low = df['Low'].clip(lower=1e-9)
        safe_close = df['Close'].clip(lower=1e-9)
        safe_volume = df['Volume'].clip(lower=1e-9)
        features['_Daily_Log_Open'] = np.log(safe_open)
        features['_Daily_Log_High'] = np.log(safe_high)
        features['_Daily_Log_Low'] = np.log(safe_low)
        features['_Daily_Log_Close'] = np.log(safe_close)
        features['_Daily_Log_Volume'] = np.log(safe_volume)
        features['_Daily_Log_Return'] = np.log(safe_close / safe_close.shift(1))
        features['_SMA_20'] = ta.trend.sma_indicator(df['Close'], 20)
        features['_SMA_50'] = ta.trend.sma_indicator(df['Close'], 50)
        features['_EMA_20'] = ta.trend.ema_indicator(df['Close'], 20)
        features['_EMA_50'] = ta.trend.ema_indicator(df['Close'], 50)
        features['_ADX_14'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], 14).adx()
        features['_RSI_14'] = ta.momentum.rsi(df['Close'], 14)
        macd = ta.trend.MACD(df['Close'], 26, 12, 9)
        features['_MACD_line'] = macd.macd()
        features['_MACD_signal'] = macd.macd_signal()
        features['_MACD_hist'] = macd.macd_diff()
        bb = ta.volatility.BollingerBands(df['Close'], 20, 2)
        features['_BB_upper'] = bb.bollinger_hband()
        features['_BB_mid'] = bb.bollinger_mavg()
        features['_BB_lower'] = bb.bollinger_lband()
        features['_ATR_14'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], 14)
        features['_OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
        features['_MFI_14'] = ta.volume.money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'], 14)
        features['_HV_5'] = features['_Daily_Log_Return'].rolling(5).std()
        features['_HV_21'] = features['_Daily_Log_Return'].rolling(21).std()
        features['_HV_63'] = features['_Daily_Log_Return'].rolling(63).std()
        return features
    except Exception:
        return None

def process_and_merge_stock_features(master_df, multi_level_df, ticker_info_df, name_map):
    print("\n===========================================================================================")
    print("STEP 5: Engineering and Merging Corporate OHLCV Features...")
    print("===========================================================================================")
    try:
        final_df = master_df.copy()
        if multi_level_df is None: raise ValueError("Input Data for Corporate Features is Invalid: None Object Received.")
        symbols_to_process = sorted(multi_level_df.columns.get_level_values(1).unique())
        success_count, failure_count, skipped_count = 0, 0, 0
        for symbol in symbols_to_process:
            company_name = name_map.get(symbol, symbol)
            single_stock_df = multi_level_df.xs(symbol, axis=1, level=1)
            single_stock_df_filtered = single_stock_df.dropna(subset=['Close'])
            if single_stock_df_filtered.empty:
                print(f"[INFO] Skipped Symbol {symbol} ({company_name}) Due to No Valid Data in its Date Range.")
                skipped_count += 1
                continue
            features_df = calculate_features_for_one_stock(single_stock_df_filtered)
            if features_df is not None:
                final_df = pd.merge(final_df, features_df.add_suffix(f"_{company_name}"), left_on='_Date', right_index=True, how='left')
                print(f"[SUCCESS] Engineered and Merged Corporate OHLCV Features for Symbol: {symbol} ({company_name}).")
                success_count += 1
            else:
                print(f"[ERROR] Failed to Engineer Corporate OHLCV Features for Symbol: {symbol} ({company_name}).")
                failure_count += 1

        print(f"\n[SUCCESS] Step 5: Engineering and Merging Corporate OHLCV Features Completed Successfully. (Summary: {success_count} Symbols Processed, {failure_count} Failed, {skipped_count} Skipped).")
        return final_df
    except Exception as e:
        print(f"\n[ERROR] A Critical Error Occurred During the Feature Engineering and Merging Process: {e}")
        return master_df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 6: FETCH AND MERGE FRED MACROECONOMIC DATA - WARM-UP
#==============================================================================
def fetch_and_merge_fred_data(master_df, fred_tickers_map):
    print("\n===========================================================================================")
    print("STEP 6: Fetching and Merging FRED Macroeconomic Data Using Warm-Up...")
    print("===========================================================================================")
    processed_df = master_df.copy()
    try:
        #--> Sub-step 6.1: Fetching Macroeconomic Data:
        print("--> Sub-step 6.1: Fetching Macroeconomic Data...")
        warm_up_start_date = '1994-01-01'
        end_date = processed_df['_Date'].max()
        fred_data = pdr.DataReader(sorted(list(fred_tickers_map.values())), 'fred', warm_up_start_date, end_date)
        if fred_data.empty: raise ValueError("Downloaded FRED Data is Empty.")
        fred_data.rename(columns={v: k for k, v in fred_tickers_map.items()}, inplace=True)
        for key in fred_tickers_map.keys():
            print(f"[SUCCESS] Fetched Macroeconomic Variable '{key}'.")
        print("[SUCCESS] Sub-step 6.1: Fetching Macroeconomic Data Completed Successfully.")

        #--> Sub-step 6.2: Merging Macroeconomic Data using merge_asof:
        print("\n--> Sub-step 6.2: Merging Macroeconomic Data...")
        fred_data.index = pd.to_datetime(fred_data.index)
        fred_data = fred_data.sort_index()
        temp_df = processed_df.sort_values('_Date')
        merged_df = pd.merge_asof(temp_df, fred_data, left_on='_Date', right_index=True, direction='backward')
        for key in sorted(fred_tickers_map.keys()):
            print(f"[SUCCESS] Merged Macroeconomic Variable '{key}'.")
        print("[SUCCESS] Sub-step 6.2: Merging Macroeconomic Data Completed Successfully.")

        #--> Sub-step 6.3: Handling Missing Values in Macroeconomic Data:
        print("\n--> Sub-step 6.3: Handling Missing Values in Macroeconomic Data...")
        merged_df[list(fred_tickers_map.keys())] = merged_df[list(fred_tickers_map.keys())].ffill()
        print("[SUCCESS] Missing Values for Macroeconomic Data Have Been Forward-Filled.")
        print("[SUCCESS] Sub-step 6.3: Handling Missing Values in Macroeconomic Data Completed Successfully.")

        print("\n[SUCCESS] Step 6: Fetching and Merging FRED Macroeconomic Data Completed Successfully.")
        return merged_df
    except Exception as e:
        print(f"[ERROR] An Error Occurred During FRED Data Integration: {e}")
        return processed_df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 7: FETCH AND MERGE GLOBAL MARKET DATA - WARM-UP
#==============================================================================
def fetch_and_merge_yfinance_indices(master_df, yfinance_tickers_map):
    print("\n===========================================================================================")
    print("STEP 7: Fetching and Merging Global Market Data Using Warm-Up...")
    print("===========================================================================================")
    try:
        df = master_df.copy()
        warm_up_start_date = df['_Date'].min() - pd.Timedelta(days=10)
        end_date = df['_Date'].max()
        ordered_keys = sorted(list(yfinance_tickers_map.keys()))

        #--> Sub-step 7.1: Fetching Global Market Data:
        print("--> Sub-step 7.1: Fetching Global Market Data...")
        logging.getLogger('yfinance').setLevel(logging.CRITICAL)
        downloaded_data = yf.download(list(yfinance_tickers_map.values()), start=warm_up_start_date, end=end_date, progress=False, auto_adjust=True)
        logging.getLogger('yfinance').setLevel(logging.WARNING)
        processed_data = pd.DataFrame()
        fetch_success_count = 0
        fetch_failure_list = []
        for key in ordered_keys:
            ticker = yfinance_tickers_map[key]
            if downloaded_data.empty or not isinstance(downloaded_data.columns, pd.MultiIndex) or ticker not in downloaded_data['Close'].columns or downloaded_data['Close'][ticker].isnull().all():
                print(f"[ERROR] Failed to Fetch Global Market Data for Variable '{key}'.")
                fetch_failure_list.append(key)
                continue
            close_price = downloaded_data['Close'][ticker].clip(lower=1e-9)
            if '_Daily_Log_Return' in key:
                series = np.log(close_price / close_price.shift(1))
                series = series.resample('D').asfreq().fillna(0)
            elif '_Daily_Close' in key:
                series = close_price
                series = series.resample('D').ffill()
            processed_data[key] = series
            print(f"[SUCCESS] Fetched Global Market Data for Variable '{key}'.")
            fetch_success_count += 1
        if fetch_failure_list: raise Exception(f"Failed to Fetch the Following Required Variables: {fetch_failure_list}")
        print("[SUCCESS] Sub-step 7.1: Fetching Global Market Data Completed Successfully.")

        #--> Sub-step 7.2: Merging Global Market Data:
        print("\n--> Sub-step 7.2: Merging Global Market Data...")
        merged_df = pd.merge(df, processed_data, left_on='_Date', right_index=True, how='left')
        for key in ordered_keys:
            print(f"[SUCCESS] Merged Global Market Data for Variable '{key}'.")
        print("[SUCCESS] Sub-step 7.2: Merging Global Market Data Completed Successfully.")

        print(f"\n[SUCCESS] Step 7: Fetching and Merging Global Market Data Completed Successfully.")
        return merged_df
    except Exception as e:
        print(f"\n[ERROR] A Critical Error Occurred During the Global Market Data Fetching and Merging Process: {e}")
        return master_df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 8: FILL QUALITATIVE DATA
#==============================================================================
def add_qualitative_variables(master_df, events_csv_string):
    print("\n===========================================================================================")
    print("STEP 8: Filling Qualitative Data...")
    print("===========================================================================================")
    try:
        df_with_events = master_df.copy()
        events_df = pd.read_csv(io.StringIO(events_csv_string), skipinitialspace=True)
        events_df['StartDate'] = pd.to_datetime(events_df['StartDate'])
        events_df['EndDate'] = pd.to_datetime(events_df['EndDate'])
        variable_columns = ['_EO', '_ND', '_PSI', '_TWI']
        success_count = 0
        for col in variable_columns:
            try:
                df_with_events[col] = 0
                col_events = events_df[events_df['Variable'] == col]
                for _, row in col_events.iterrows():
                    mask = (df_with_events['_Date'] >= row['StartDate']) & (df_with_events['_Date'] <= row['EndDate'])
                    df_with_events.loc[mask, col] = 1
                print(f"[SUCCESS] Filled Qualitative Data for Variable '{col}'.")
                success_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to Fill Qualitative Data for Variable '{col}'. Reason: {e}")
        if success_count != len(variable_columns):
            raise Exception("One or More Qualitative Variables Failed to be Filled.")

        print(f"\n[SUCCESS] Step 8: Filling Qualitative Data Completed Successfully.")
        return df_with_events
    except Exception as e:
        print(f"\n[ERROR] A Critical Error Occurred During the Qualitative Data Filling Process: {e}")
        return master_df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 9: FETCH AND MERGE DEPENDENT VARIABLE DATA - WARM-UP
#==============================================================================
def calculate_dependent_variable(master_df):
    print("\n===========================================================================================")
    print("STEP 9: Fetching and Merging Dependent Variable Data Using Warm-Up...")
    print("===========================================================================================")
    dependent_variable_name = '_Daily_Log_Return_DJI'
    final_df = master_df.copy()
    try:
        #--> Sub-step 9.1: Fetching Dependent Variable Data:
        print("--> Sub-step 9.1: Fetching Dependent Variable Data...")
        warm_up_start_date = master_df['_Date'].min() - pd.Timedelta(days=10)
        end_date = master_df['_Date'].max()
        dji_data = yf.download('^DJI', start=warm_up_start_date, end=end_date, auto_adjust=True, progress=False)
        if isinstance(dji_data.columns, pd.MultiIndex):
            dji_data.columns = dji_data.columns.droplevel(1)
        if dji_data.empty or 'Close' not in dji_data.columns or dji_data['Close'].isnull().all():
            raise ValueError("Downloaded DJI Data is Empty, Missing 'Close' Column, or Has No Valid Close Prices.")
        safe_close = dji_data['Close'].clip(lower=1e-9)
        log_return_series = np.log(safe_close / safe_close.shift(1))
        log_return_series.name = dependent_variable_name
        print(f"[SUCCESS] Fetched Dependent Variable Data for '{dependent_variable_name}'.")
        print("[SUCCESS] Sub-step 9.1: Fetching Dependent Variable Data Completed Successfully.")

        #--> Sub-step 9.2: Merging Dependent Variable Data:
        print("\n--> Sub-step 9.2: Merging Dependent Variable Data...")
        final_df = master_df.merge(log_return_series, left_on='_Date', right_index=True, how='left')
        print(f"[SUCCESS] Merged Dependent Variable Data into the Master DataFrame.")
        print("[SUCCESS] Sub-step 9.2: Merging Dependent Variable Data Completed Successfully.")

        print(f"\n[SUCCESS] Step 9: Fetching and Merging Dependent Variable Data Completed Successfully.")
        return final_df
    except Exception as e:
        print(f"\n[ERROR] A Critical Error Occurred During the Dependent Variable Data Fetching and Merging Process: {e}")
        final_df[dependent_variable_name] = np.nan
        return final_df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 10: PRE-PROCESS - HANDLE MISSING VALUES - FORWARD FILL
#==============================================================================
def handle_missing_values(df, ticker_info_df, name_map):
    print("\n===========================================================================================")
    print("STEP 10: Pre-processing - Handling Missing Values Using Forward Fill...")
    print("===========================================================================================")
    processed_df = df.copy()
    try:
        #--> Sub-step 10.1: Identifying Initial Statistics for Missing Values:
        print("--> Sub-step 10.1: Identifying Initial Statistics for Missing Values...")
        total_cells = processed_df.size
        initial_missing_cells = processed_df.isnull().sum().sum()
        print(f"[SUCCESS] Identified {initial_missing_cells} Missing Cells out of {total_cells} Total Cells.")
        print("[SUCCESS] Sub-step 10.1: Identifying Initial Statistics Completed Successfully.")

        #--> Sub-step 10.2: Applying Fill Rules for Missing Values:
        print("\n--> Sub-step 10.2: Applying Fill Rules for Missing Values...")
        print("Applying Out-of-Index Rule...")
        unique_symbols = ticker_info_df['Symbol'].unique()
        for symbol in unique_symbols:
            company_name_suffix = name_map.get(symbol, symbol)
            company_cols = [col for col in processed_df.columns if col.endswith(f"_{company_name_suffix}")]
            if not company_cols: continue
            symbol_periods = ticker_info_df[ticker_info_df['Symbol'] == symbol]
            active_mask = pd.Series(False, index=processed_df.index)
            for _, row in symbol_periods.iterrows():
                active_mask |= (processed_df['_Date'] >= pd.to_datetime(row['StartDate'])) & (processed_df['_Date'] <= pd.to_datetime(row['EndDate']))
            processed_df.loc[~active_mask, company_cols] = 0
        print("[SUCCESS] Out-of-Index Rule Applied.")
        print("Applying Forward-Fill Rule...")
        exclude_from_ffill = {col for col in processed_df.columns if 'Volume' in col or '_Daily_Log_Return' in col}
        exclude_from_ffill.update(['_Date', '_Year', '_Month', '_Day', '_WeekOfYear', '_DayOfWeek', '_EO', '_ND', '_PSI', '_TWI'])
        ffill_cols = [col for col in processed_df.columns if col not in exclude_from_ffill]
        processed_df[ffill_cols] = processed_df[ffill_cols].ffill()
        print("[SUCCESS] Forward-Fill Rule Applied.")
        print("Applying Zero-Fill Rule...")
        processed_df.fillna(0, inplace=True)
        print("[SUCCESS] Zero-Fill Rule Applied.")
        print("[SUCCESS] Sub-step 10.2: Applying Fill Rules Completed Successfully.")

        #--> Sub-step 10.3: Calculating and Reporting Final Statistics:
        print("\n--> Sub-step 10.3: Calculating and Reporting Final Statistics...")
        final_missing_cells = processed_df.isnull().sum().sum()
        close_price_cols = [col for col in processed_df.columns if '_Daily_Log_Close' in col]
        mean_price_after, std_dev_price_after = 0, 0
        if close_price_cols:
            non_zero_log_prices = processed_df[close_price_cols].values.flatten()
            non_zero_log_prices = non_zero_log_prices[non_zero_log_prices != 0]
            if non_zero_log_prices.size > 0:
                actual_prices = np.exp(non_zero_log_prices)
                mean_price_after, std_dev_price_after = actual_prices.mean(), actual_prices.std()
        initial_missing_percentage = (initial_missing_cells / total_cells) * 100 if total_cells > 0 else 0
        final_missing_percentage = (final_missing_cells / total_cells) * 100 if total_cells > 0 else 0
        print("--- Missing Value Handling Statistics ---")
        print(f"1. Initial Missing Cells: {initial_missing_cells} ({initial_missing_percentage:.2f}%)")
        print(f"2. Final Missing Cells: {final_missing_cells} ({final_missing_percentage:.2f}%)")
        print(f"3. Mean Price (Post-Handling): ${mean_price_after:.2f}")
        print(f"4. Price Std Dev (Post-Handling): {std_dev_price_after:.2f}")
        print("[SUCCESS] Sub-step 10.3: Calculating and Reporting Final Statistics Completed Successfully.")

        print("\n[SUCCESS] Step 10: Pre-processing - Handling Missing Values Completed Successfully.")
        return processed_df
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Missing Value Handling: {e}")
        return df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 11: PRE-PROCESS - HANDLE OUTLIERS - WINSORIZATION
#==============================================================================
def handle_outliers(df):
    print("\n===========================================================================================")
    print("STEP 11: Pre-processing - Handling Outliers Using Winsorization...")
    print("===========================================================================================")
    outlier_handling_df = df.copy()
    try:
        #--> Sub-step 11.1: Identifying Return Variables for Outlier Detection:
        print("--> Sub-step 11.1: Identifying Return Variables for Outlier Detection...")
        outlier_target_cols = [col for col in outlier_handling_df.columns if '_Daily_Log_Return' in col]
        if not outlier_target_cols:
            print("[INFO] No Return Variables Found for Outlier Handling. Skipping Step.")
            print("===========================================================================================")
            return outlier_handling_df
        total_data_points = outlier_handling_df[outlier_target_cols].size
        print(f"[SUCCESS] Identified {len(outlier_target_cols)} Return Variables with {total_data_points} Total Data Points.")
        print("[SUCCESS] Sub-step 11.1: Identifying Return Variables Completed Successfully.")

        #--> Sub-step 11.2: Applying Winsorization Rule to Return Variables:
        print("\n--> Sub-step 11.2: Applying Winsorization Rule to Return Variables...")
        total_adjusted_points = 0
        for col in outlier_target_cols:
            if (outlier_handling_df[col] == 0).all(): continue
            lower_bound, upper_bound = outlier_handling_df[col].quantile(0.005), outlier_handling_df[col].quantile(0.995)
            if lower_bound < upper_bound:
                outliers_mask = (outlier_handling_df[col] < lower_bound) | (outlier_handling_df[col] > upper_bound)
                total_adjusted_points += outliers_mask.sum()
                outlier_handling_df[col] = outlier_handling_df[col].clip(lower_bound, upper_bound)
                print(f"[SUCCESS] Applied Winsorization to Column '{col}'.")
        print("[SUCCESS] Sub-step 11.2: Applying Winsorization Rule Completed Successfully.")

        #--> Sub-step 11.3: Calculating and Reporting Final Statistics:
        print("\n--> Sub-step 11.3: Calculating and Reporting Final Statistics...")
        adjustment_percentage = (total_adjusted_points / total_data_points) * 100 if total_data_points > 0 else 0
        print("--- Outlier Handling Statistics ---")
        print(f"1. Data Points Processed: {total_data_points}")
        print(f"2. Data Points Adjusted: {total_adjusted_points}")
        print(f"3. Adjustment Percentage: {adjustment_percentage:.4f}%")
        print("[SUCCESS] Sub-step 11.3: Calculating and Reporting Final Statistics Completed Successfully.")

        print("\n[SUCCESS] Step 11: Pre-processing - Handling Outliers Completed Successfully.")
        return outlier_handling_df
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Outlier Handling: {e}")
        return df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 12: PERFORM STATIONARITY ANALYSIS - AUGMENTED DICKEY-FULLER
#==============================================================================
def perform_stationarity_analysis(ohlcv_data, df, name_map, fred_map, dependent_var):
    print("\n===========================================================================================")
    print("STEP 12: Performing Stationarity Analysis Using Augmented Dickey-Fuller...")
    print("===========================================================================================")
    try:
        #--> Sub-step 12.1: Identifying Key Variables for Analysis:
        print("--> Sub-step 12.1: Identifying Key Variables for Analysis...")
        all_names = list(name_map.values())
        stock_return_vars = [col for col in df.columns if col.startswith('_Daily_Log_Return_') and col.split('_')[-1] in all_names]
        macro_vars = list(fred_map.keys())
        all_key_vars = stock_return_vars + macro_vars
        if dependent_var in df.columns:
            all_key_vars.append(dependent_var)
        print(f"[SUCCESS] Identified {len(all_key_vars)} Key Variables for Stationarity Analysis.")
        print("[SUCCESS] Sub-step 12.1: Identifying Key Variables Completed Successfully.")

        #--> Sub-step 12.2: Performing ADF Test on Key Variables:
        print("\n--> Sub-step 12.2: Performing ADF Test on Key Variables...")
        stationarity_results = []
        for return_col in stock_return_vars:
            symbol_name = return_col.split('_')[-1]
            symbol = next((s for s, n in name_map.items() if n == symbol_name), None)
            if not symbol or symbol not in ohlcv_data['Close'].columns: continue
            price_series = ohlcv_data['Close'][symbol].dropna()
            return_series = df[return_col].replace(0, np.nan).dropna()
            if not price_series.empty:
                stationarity_results.append({'Variable_Name': symbol, 'ADF_p_value': adfuller(price_series)[1], 'Series_Type': 'Price'})
            if not return_series.empty:
                stationarity_results.append({'Variable_Name': return_col, 'ADF_p_value': adfuller(return_series)[1], 'Series_Type': 'Log_Return'})
            print(f"[SUCCESS] Performed ADF Test for Price and Return Series of '{symbol_name}'.")
        for macro_col in macro_vars:
            macro_series = df[macro_col].dropna()
            if not macro_series.empty:
                stationarity_results.append({'Variable_Name': macro_col, 'ADF_p_value': adfuller(macro_series)[1], 'Series_Type': 'Level'})
                print(f"[SUCCESS] Performed ADF Test for Macro Variable '{macro_col}'.")
        if dependent_var in df.columns:
            dependent_series = df[dependent_var].replace(0, np.nan).dropna()
            if not dependent_series.empty:
                stationarity_results.append({'Variable_Name': dependent_var, 'ADF_p_value': adfuller(dependent_series)[1], 'Series_Type': 'Log_Return'})
                print(f"[SUCCESS] Performed ADF Test for Dependent Variable '{dependent_var}'.")
        print("[SUCCESS] Sub-step 12.2: Performing ADF Test Completed Successfully.")

        #--> Sub-step 12.3: Reporting Statistics and Generating Output File:
        print("\n--> Sub-step 12.3: Reporting Statistics and Generating Output File...")
        results_df = pd.DataFrame(stationarity_results)
        price_stats = results_df[results_df['Series_Type'] == 'Price']
        return_stats = results_df[results_df['Series_Type'] == 'Log_Return']
        macro_stats = results_df[results_df['Series_Type'] == 'Level']
        pct_price_non_stationary = (price_stats['ADF_p_value'] >= 0.05).mean() * 100 if not price_stats.empty else 0
        pct_return_stationary = (return_stats['ADF_p_value'] < 0.05).mean() * 100 if not return_stats.empty else 0
        pct_macro_non_stationary = (macro_stats['ADF_p_value'] >= 0.05).mean() * 100 if not macro_stats.empty else 0
        print("--- Stationarity Analysis Statistics ---")
        print(f"1. Pct. of Price Series That Were Non-Stationary: {pct_price_non_stationary:.2f}%")
        print(f"2. Pct. of Log-Return Series That Were Stationary: {pct_return_stationary:.2f}%")
        print(f"3. Pct. of Macroeconomic Series That Were Non-Stationary: {pct_macro_non_stationary:.2f}%")
        results_df['Row'] = [to_persian_numerals(i) for i in range(1, len(results_df) + 1)]
        results_df.to_csv('Stationarity_Results.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Variable_Name', 'ADF_p_value', 'Series_Type'])
        print("[SUCCESS] Generated Output File: 'Stationarity_Results.csv'.")
        files.download('Stationarity_Results.csv')
        print("[SUCCESS] Sub-step 12.3: Reporting Statistics and Generating Output File Completed Successfully.")

        print("\n[SUCCESS] Step 12: Performing Stationarity Analysis Completed Successfully.")
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Stationarity Analysis: {e}")
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 13: PERFORM CORRELATION ANALYSIS - PEARSON
#==============================================================================
def perform_correlation_analysis(df, dependent_var, name_map, fred_map):
    print("\n===========================================================================================")
    print("STEP 13: Performing Correlation Analysis Using Pearson...")
    print("===========================================================================================")
    try:
        #--> Sub-step 13.1: Identifying Key Variables for Analysis:
        print("--> Sub-step 13.1: Identifying Key Variables for Analysis...")
        stock_vars = [f"_Daily_Log_Return_{name}" for name in name_map.values()]
        macro_vars = list(fred_map.keys())
        independent_vars = [col for col in stock_vars + macro_vars if col in df.columns]
        print(f"[SUCCESS] Identified 1 Dependent Variable and {len(independent_vars)} Key Independent Variables.")
        print("[SUCCESS] Sub-step 13.1: Identifying Key Variables Completed Successfully.")

        #--> Sub-step 13.2: Performing Pearson Correlation Analysis:
        print("\n--> Sub-step 13.2: Performing Pearson Correlation Analysis...")
        correlation_results = []
        for var in independent_vars:
            subset_df = df[[dependent_var, var]][(df[dependent_var] != 0) & (df[var] != 0)]
            if not subset_df.empty:
                correlation = subset_df[dependent_var].corr(subset_df[var], method='pearson')
                correlation_results.append({'Variable_Name': var, 'Pearson_Correlation': correlation})
                print(f"[SUCCESS] Calculated Correlation between Dependent Variable and '{var}'.")
        print("[SUCCESS] Sub-step 13.2: Performing Pearson Correlation Analysis Completed Successfully.")

        #--> Sub-step 13.3: Generating Output File:
        print("\n--> Sub-step 13.3: Generating Output File...")
        results_df = pd.DataFrame(correlation_results).sort_values(by='Pearson_Correlation', ascending=False)
        results_df['Row'] = [to_persian_numerals(i) for i in range(1, len(results_df) + 1)]
        results_df.to_csv('Correlation_Results.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Variable_Name', 'Pearson_Correlation'])
        print("[SUCCESS] Generated Output File: 'Correlation_Results.csv'.")
        files.download('Correlation_Results.csv')
        print("[SUCCESS] Sub-step 13.3: Generating Output File Completed Successfully.")

        print("\n[SUCCESS] Step 13: Performing Correlation Analysis Completed Successfully.")
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Correlation Analysis: {e}")
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 14: OPTIMIZE DATA TYPES FOR MEMORY EFFICIENCY
#==============================================================================
def optimize_data_types(df):
    print("\n===========================================================================================")
    print("STEP 14: Optimizing Data Types for Memory Efficiency...")
    print("===========================================================================================")
    optimization_df = df.copy()
    try:
        #--> Sub-step 14.1: Calculating Initial Memory Usage:
        print("--> Sub-step 14.1: Calculating Initial Memory Usage...")
        initial_memory = optimization_df.memory_usage(deep=True).sum() / (1024**2)
        print(f"[SUCCESS] Initial DataFrame Memory Usage is {initial_memory:.2f} MB.")
        print("[SUCCESS] Sub-step 14.1: Calculating Initial Memory Usage Completed Successfully.")

        #--> Sub-step 14.2: Optimizing Data Types:
        print("\n--> Sub-step 14.2: Optimizing Data Types...")
        inf_count = np.isinf(optimization_df.select_dtypes(include=np.number)).sum().sum()
        if inf_count > 0: optimization_df.replace([np.inf, -np.inf], 0, inplace=True)
        for col in optimization_df.columns:
            if optimization_df[col].dtype == 'float64': optimization_df[col] = optimization_df[col].astype('float32')
            elif optimization_df[col].dtype == 'int64':
                c_min, c_max = optimization_df[col].min(), optimization_df[col].max()
                if c_min >= 0:
                    if c_max < 256: optimization_df[col] = optimization_df[col].astype('uint8')
                    elif c_max < 65536: optimization_df[col] = optimization_df[col].astype('uint16')
                else:
                    if c_min > -128 and c_max < 128: optimization_df[col] = optimization_df[col].astype('int8')
            print(f"[SUCCESS] Optimized Data Type for Column '{col}'.")
        print("[SUCCESS] Sub-step 14.2: Optimizing Data Types Completed Successfully.")

        #--> Sub-step 14.3: Calculating and Reporting Final Statistics:
        print("\n--> Sub-step 14.3: Calculating and Reporting Final Statistics...")
        final_memory = optimization_df.memory_usage(deep=True).sum() / (1024**2)
        reduction_pct = (initial_memory - final_memory) / initial_memory * 100 if initial_memory > 0 else 0
        print("--- Memory Optimization Statistics ---")
        print(f"1. Initial Memory Usage: {initial_memory:.2f} MB")
        print(f"2. Final Memory Usage: {final_memory:.2f} MB")
        print(f"3. Memory Reduction: {(initial_memory - final_memory):.2f} MB ({reduction_pct:.2f}%)")
        print("[SUCCESS] Sub-step 14.3: Calculating and Reporting Final Statistics Completed Successfully.")

        print("\n[SUCCESS] Step 14: Optimizing Data Types Completed Successfully.")
        return optimization_df
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Data Type Optimization: {e}")
        return df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 15: FINALIZE DATA STRUCTURE AND COLUMN ORDER
#==============================================================================
def finalize_data_structure(df, company_info_df, name_map, fred_map, yfinance_map, dependent_var):
    print("\n===========================================================================================")
    print("STEP 15: Finalizing Data Structure and Column Order...")
    print("===========================================================================================")
    try:
        #--> Sub-step 15.1: Finalizing Column Order:
        print("--> Sub-step 15.1: Finalizing Column Order...")
        final_column_order = ['_Date', '_Year', '_Month', '_Day', '_WeekOfYear', '_DayOfWeek']
        feature_names = [
            '_Daily_Log_Open', '_Daily_Log_High', '_Daily_Log_Low', '_Daily_Log_Close', '_Daily_Log_Volume', 
            '_Daily_Log_Return', '_SMA_20', '_SMA_50', '_EMA_20', '_EMA_50', '_ADX_14', '_RSI_14', 
            '_MACD_line', '_MACD_signal', '_MACD_hist', '_BB_upper', '_BB_mid', '_BB_lower', '_ATR_14', 
            '_OBV', '_MFI_14', '_HV_5', '_HV_21', '_HV_63'
        ]
        unique_symbols = sorted(company_info_df['Symbol'].unique())
        for symbol in unique_symbols:
            company_name_suffix = f"_{name_map.get(symbol, symbol)}"
            for feature in feature_names: final_column_order.append(f"{feature}{company_name_suffix}")
        final_column_order.extend(sorted(list(fred_map.keys())))
        final_column_order.extend(sorted(list(yfinance_map.keys())))
        final_column_order.extend(sorted(['_EO', '_ND', '_PSI', '_TWI']))
        if dependent_var in df.columns: final_column_order.append(dependent_var)
        existing_columns_in_order = [col for col in final_column_order if col in df.columns]
        final_df = df[existing_columns_in_order]
        print("[SUCCESS] Final Column Order Has Been Applied.")
        print("[SUCCESS] Sub-step 15.1: Finalizing Column Order Completed Successfully.")

        #--> Sub-step 15.2: Reporting Final DataFrame Statistics:
        print("\n--> Sub-step 15.2: Reporting Final DataFrame Statistics...")
        num_rows = len(final_df)
        num_cols = len(final_df.columns)
        total_data_points = num_rows * num_cols
        numeric_df = final_df.select_dtypes(include=[np.number])
        num_empty_rows = (numeric_df == 0).all(axis=1).sum()
        num_empty_cols = (numeric_df == 0).all(axis=0).sum()
        print("--- Final DataFrame Statistics ---")
        print(f"1. Total Number of Rows: {num_rows}")
        print(f"2. Total Number of Columns: {num_cols}")
        print(f"3. Total Data Points: {total_data_points}")
        print(f"4. Completely Empty Rows (All Zeros): {num_empty_rows}")
        print(f"5. Completely Empty Columns (All Zeros): {num_empty_cols}")
        print("[SUCCESS] Sub-step 15.2: Reporting Final DataFrame Statistics Completed Successfully.")

        #--> Sub-step 15.3: Generating Final Data File:
        print("\n--> Sub-step 15.3: Generating Final Data File...")
        final_df.to_csv('Thesis_Data_File.csv', sep=',', index=False, date_format='%Y-%m-%d')
        print("[SUCCESS] Generated Final Data File: 'Thesis_Data_File.csv'.")
        files.download('Thesis_Data_File.csv')
        print("[SUCCESS] Sub-step 15.3: Generating Final Data File Completed Successfully.")

        print("\n[SUCCESS] Step 15: Finalizing Data Structure and Column Order Completed Successfully.")
        return final_df
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Data Structure Finalization: {e}")
        return df
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 16: GENERATE DESCRIPTIVE STATISTICS FOR KEY VARIABLES
#==============================================================================
def generate_descriptive_statistics(df, dependent_var, name_map, fred_map):
    print("\n===========================================================================================")
    print("STEP 16: Generating Descriptive Statistics for Key Variables...")
    print("===========================================================================================")
    try:
        def get_stats(series, name):
            series = series[series != 0]
            if series.empty: return None
            return {'Variable_Name': name, 'Mean': series.mean(), 'Median': series.median(), 
                    'Std_Dev': series.std(), 'Skewness': series.skew(), 'Kurtosis': series.kurt(), 
                    'Min': series.min(), 'Max': series.max(), 'Count': series.count()}

        #--> Sub-step 16.1: Generating Statistics for Dependent Variable:
        print("--> Sub-step 16.1: Generating Statistics for Dependent Variable...")
        dep_stats = get_stats(df[dependent_var], dependent_var) if dependent_var in df.columns else None
        if dep_stats: print(f"[SUCCESS] Generated Statistics for '{dependent_var}'.")
        print("[SUCCESS] Sub-step 16.1: Generating Statistics for Dependent Variable Completed Successfully.")

        #--> Sub-step 16.2: Generating Statistics for Key Independent Variables:
        print("\n--> Sub-step 16.2: Generating Statistics for Key Independent Variables...")
        stock_vars = [f"_Daily_Log_Return_{name}" for name in name_map.values()]
        macro_vars = list(fred_map.keys())
        independent_vars = [col for col in stock_vars + macro_vars if col in df.columns]
        indep_stats_list = []
        for col in independent_vars:
            stats = get_stats(df[col], col)
            if stats is not None:
                indep_stats_list.append(stats)
                print(f"[SUCCESS] Generated Statistics for '{col}'.")
        print("[SUCCESS] Sub-step 16.2: Generating Statistics for Key Independent Variables Completed Successfully.")

        #--> Sub-step 16.3: Generating Output Files:
        print("\n--> Sub-step 16.3: Generating Output Files...")
        if dep_stats:
            dep_df = pd.DataFrame([dep_stats])
            dep_df['Row'] = to_persian_numerals(1)
            dep_df.to_csv('Dependent_Variable_Statistics.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row'] + [c for c in dep_df.columns if c != 'Row'])
            print("[SUCCESS] Generated Output File: 'Dependent_Variable_Statistics.csv'.")
            files.download('Dependent_Variable_Statistics.csv'); time.sleep(1)
        if indep_stats_list:
            indep_df = pd.DataFrame(indep_stats_list)
            indep_df['Row'] = [to_persian_numerals(i) for i in range(1, len(indep_df) + 1)]
            indep_df.to_csv('Independent_Variables_Statistics.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row'] + [c for c in indep_df.columns if c != 'Row'])
            print("[SUCCESS] Generated Output File: 'Independent_Variables_Statistics.csv'.")
            files.download('Independent_Variables_Statistics.csv')
        print("[SUCCESS] Sub-step 16.3: Generating Output Files Completed Successfully.")

        print("\n[SUCCESS] Step 16: Generating Descriptive Statistics Completed Successfully.")
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Descriptive Statistics Generation: {e}")
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 17: SPLIT DATASET INTO CHRONOLOGICAL SETS
#==============================================================================
def split_dataset(df):
    print("\n===========================================================================================")
    print("STEP 17: Splitting Dataset into Chronological Sets...")
    print("===========================================================================================")
    try:
        #--> Sub-step 17.1: Performing Chronological Data Split:
        print("--> Sub-step 17.1: Performing Chronological Data Split...")
        n_total = len(df)
        train_end_idx = int(n_total * 0.70)
        val_end_idx = train_end_idx + int(n_total * 0.15)
        train_df = df.iloc[:train_end_idx].copy()
        val_df = df.iloc[train_end_idx:val_end_idx].copy()
        test_df = df.iloc[val_end_idx:].copy()
        print("[SUCCESS] Chronological Data Split Has Been Performed.")
        print("[SUCCESS] Sub-step 17.1: Performing Chronological Data Split Completed Successfully.")

        #--> Sub-step 17.2: Reporting Split Statistics:
        print("\n--> Sub-step 17.2: Reporting Split Statistics...")
        print("--- Data Split Statistics ---")
        print(f"1. Training Set (70%):   {train_df['_Date'].min().date()} to {train_df['_Date'].max().date()} ({len(train_df)} Rows)")
        print(f"2. Validation Set (15%): {val_df['_Date'].min().date()} to {val_df['_Date'].max().date()} ({len(val_df)} Rows)")
        print(f"3. Test Set (15%):       {test_df['_Date'].min().date()} to {test_df['_Date'].max().date()} ({len(test_df)} Rows)")
        print("[SUCCESS] Sub-step 17.2: Reporting Split Statistics Completed Successfully.")

        print("\n[SUCCESS] Step 17: Splitting Dataset into Time-Based Sets Completed Successfully.")
        return train_df, val_df, test_df
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Dataset Splitting: {e}")
        return None, None, None
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 18: PERFORM DATA STANDARDIZATION - Z-SCORE
#==============================================================================
def perform_data_standardization(train_df, val_df, test_df, dependent_var):
    print("\n===========================================================================================")
    print("STEP 18: Performing Data Standardization Using Z-Score...")
    print("===========================================================================================")
    try:
        #--> Sub-step 18.1: Identifying Variables for Standardization:
        print("--> Sub-step 18.1: Identifying Variables for Standardization...")
        feature_cols = train_df.columns.drop(['_Date', dependent_var])
        print(f"[SUCCESS] Identified {len(feature_cols)} Variables for Standardization.")
        print("[SUCCESS] Sub-step 18.1: Identifying Variables Completed Successfully.")

        #--> Sub-step 18.2: Performing Standardization on Data Sets:
        print("\n--> Sub-step 18.2: Performing Standardization on Data Sets...")
        scaler = StandardScaler()
        train_scaled = train_df.copy(); val_scaled = val_df.copy(); test_scaled = test_df.copy()
        train_scaled[feature_cols] = scaler.fit_transform(train_df[feature_cols])
        print("[SUCCESS] Standardized Training Set.")
        val_scaled[feature_cols] = scaler.transform(val_df[feature_cols])
        print("[SUCCESS] Standardized Validation Set.")
        test_scaled[feature_cols] = scaler.transform(test_df[feature_cols])
        print("[SUCCESS] Standardized Test Set.")
        print("[SUCCESS] Sub-step 18.2: Performing Standardization on Data Sets Completed Successfully.")

        print("\n[SUCCESS] Step 18: Performing Data Standardization Completed Successfully.")
        return train_scaled, val_scaled, test_scaled
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Data Standardization: {e}")
        return None, None, None
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 19: BUILD BASELINE MODEL - MULTIVARIATE LINEAR REGRESSION
#==============================================================================
def build_baseline_model(train_df, test_df, dependent_var, name_map, fred_map):
    print("\n===========================================================================================")
    print("STEP 19: Building Baseline Model...")
    print("===========================================================================================")
    try:
        #--> Sub-step 19.1: Identifying Model Variables:
        print("--> Sub-step 19.1: Identifying Model Variables...")
        stock_vars = [f"_Daily_Log_Return_{name}" for name in name_map.values()]
        macro_vars = list(fred_map.keys())
        independent_vars = [col for col in stock_vars + macro_vars if col in train_df.columns]
        print(f"[SUCCESS] Identified 1 Dependent Variable and {len(independent_vars)} Key Independent Variables.")
        print("[SUCCESS] Sub-step 19.1: Identifying Model Variables Completed Successfully.")

        #--> Sub-step 19.2: Building and Evaluating Model:
        print("\n--> Sub-step 19.2: Building and Evaluating Model...")
        X_train, y_train = train_df[independent_vars], train_df[dependent_var]
        X_test, y_test = test_df[independent_vars], test_df[dependent_var]
        baseline_model = LinearRegression()
        baseline_model.fit(X_train, y_train)
        y_pred = baseline_model.predict(X_test)
        print("[SUCCESS] Baseline Model Has Been Built and Evaluated.")
        print("[SUCCESS] Sub-step 19.2: Building and Evaluating Model Completed Successfully.")

        #--> Sub-step 19.3: Reporting Performance and Generating Output File:
        print("\n--> Sub-step 19.3: Reporting Performance and Generating Output File...")
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / np.where(y_test == 0, 1e-9, y_test))) * 100
        da = np.mean(np.sign(y_test) == np.sign(y_pred)) * 100
        print("--- Baseline Model Performance ---")
        print(f"1. RMSE: {rmse:.4f}")
        print(f"2. MAE: {mae:.4f}")
        print(f"3. R2_Score: {r2:.4f}")
        print(f"4. MAPE: {mape:.2f}%")
        print(f"5. Directional_Accuracy: {da:.2f}%")
        results_df = pd.DataFrame([{'Model_Name': 'Baseline_Linear_Regression', 'RMSE': rmse, 'MAE': mae, 'R2_Score': r2, 'MAPE': mape, 'Directional_Accuracy': da}])
        results_df.insert(0, 'Row', to_persian_numerals(1))
        results_df.to_csv('Baseline_Model_Performance.csv', sep=',', index=False, encoding='utf-8-sig')
        print("[SUCCESS] Generated Output File: 'Baseline_Model_Performance.csv'.")
        files.download('Baseline_Model_Performance.csv')
        print("[SUCCESS] Sub-step 19.3: Reporting Performance and Generating Output File Completed Successfully.")

        print("\n[SUCCESS] Step 19: Building Baseline Model Completed Successfully.")
        return baseline_model
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Baseline Model Building: {e}")
        return None
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 20: DISCOVER OPTIMAL MODEL WITH H2O AUTOML
#==============================================================================
def discover_optimal_model_with_h2o(train_df, val_df, test_df, dependent_var):
    print("\n===========================================================================================")
    print("STEP 20: Discovering Optimal Model with H2O AutoML...")
    print("===========================================================================================")
    try:
        h2o.init(nthreads=-1, max_mem_size=None, log_level="ERRR")
        excluded_algos = ["StackedEnsemble", "DeepLearning"]
        test_max_runtime_secs = 3600

        #--> Sub-step 20.1: Reporting AutoML Configuration and Resources:
        print("--> Sub-step 20.1: Reporting AutoML Configuration and Resources...")
        print("\n--- AutoML Configuration (TEST RUN) ---")
        print(f"1. Max Runtime: {test_max_runtime_secs} seconds ({test_max_runtime_secs//60} minutes)")
        print("2. Max Models: Unlimited (Stops by Time or Early Stopping)")
        print("3. Stopping Metric: RMSE")
        print("4. Stopping Rounds: 10")
        print(f"5. Excluded Algorithms: {excluded_algos}")
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        h2o_ram_gb = h2o.cluster().nodes[0]['free_mem'] / (1024**3)
        print("\n--- Computational Resource Statistics ---")
        print(f"1. Total System CPU Cores: {psutil.cpu_count(logical=True)}")
        print(f"2. Total System RAM: {total_ram_gb:.2f} GB")
        print(f"3. Memory Allocated to H2O: {h2o_ram_gb:.2f} GB")
        print("[SUCCESS] Sub-step 20.1: Reporting AutoML Configuration and Resources Completed Successfully.")

        #--> Sub-step 20.2: Discovering Optimal Model via AutoML Training:
        print("\n--> Sub-step 20.2: Discovering Optimal Model via AutoML Training...")
        train_h2o = h2o.H2OFrame(train_df); val_h2o = h2o.H2OFrame(val_df); test_h2o = h2o.H2OFrame(test_df)
        independent_vars = [col for col in train_df.columns if col not in [dependent_var, '_Date']]
        aml = H2OAutoML(nfolds=0, max_runtime_secs=test_max_runtime_secs, max_models=0, stopping_metric="RMSE", stopping_rounds=10, sort_metric="RMSE", seed=1, exclude_algos=excluded_algos)
        aml.train(x=independent_vars, y=dependent_var, training_frame=train_h2o, validation_frame=val_h2o)
        print("[SUCCESS] AutoML Training Has Completed.")
        print("[SUCCESS] Sub-step 20.2: Discovering Optimal Model via AutoML Training Completed Successfully.")

        #--> Sub-step 20.3: Evaluating All Models and Generating Leaderboard File:
        print("\n--> Sub-step 20.3: Evaluating All Models and Generating Leaderboard File...")
        leaderboard = aml.leaderboard.as_data_frame(use_multi_thread=True)
        all_models_perf = []
        y_test_pd = test_df[dependent_var].values
        for model_id in leaderboard['model_id']:
            model = h2o.get_model(model_id)
            perf_test = model.model_performance(test_h2o)
            preds = model.predict(test_h2o).as_data_frame(use_multi_thread=True)['predict'].values
            rmse = perf_test.rmse()
            mae = perf_test.mae()
            r2 = perf_test.r2()
            mape = np.mean(np.abs((y_test_pd - preds) / np.where(y_test_pd == 0, 1e-9, y_test_pd))) * 100
            da = np.mean(np.sign(y_test_pd) == np.sign(preds)) * 100
            all_models_perf.append({'Model_Name': model_id, 'RMSE': rmse, 'MAE': mae, 'R2_Score': r2, 'MAPE': mape, 'Directional_Accuracy': da})
        leaderboard_df = pd.DataFrame(all_models_perf)
        leaderboard_df['Row'] = [to_persian_numerals(i) for i in range(1, len(leaderboard_df) + 1)]
        leaderboard_df.to_csv('H2O_AutoML_Leaderboard.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Model_Name', 'RMSE', 'MAE', 'R2_Score', 'MAPE', 'Directional_Accuracy'])
        print("[SUCCESS] Generated Output File: 'H2O_AutoML_Leaderboard.csv'.")
        files.download('H2O_AutoML_Leaderboard.csv')
        print("[SUCCESS] Sub-step 20.3: Evaluating All Models and Generating Leaderboard File Completed Successfully.")

        #--> Sub-step 20.4: Evaluating Best Model and Generating Output Files:
        print("\n--> Sub-step 20.4: Evaluating Best Model and Generating Output Files...")
        best_model = aml.leader
        perf_test = best_model.model_performance(test_h2o)
        y_true_test = test_df[dependent_var].values
        y_pred_test = best_model.predict(test_h2o).as_data_frame(use_multi_thread=True)['predict'].values
        mape = np.mean(np.abs((y_true_test - y_pred_test) / np.where(y_true_test == 0, 1e-9, y_true_test))) * 100
        da = np.mean(np.sign(y_true_test) == np.sign(y_pred_test)) * 100
        best_model_perf = pd.DataFrame([{'Model_Name': best_model.model_id, 'RMSE_Test': perf_test.rmse(), 'MAE_Test': perf_test.mae(), 'R2_Test': perf_test.r2(), 'MAPE_Test': mape, 'Directional_Accuracy_Test': da}])
        best_model_perf.insert(0, 'Row', to_persian_numerals(1))
        best_model_perf.to_csv('H2O_Best_Model_Test_Performance.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Model_Name', 'RMSE_Test', 'MAE_Test', 'R2_Test', 'MAPE_Test', 'Directional_Accuracy_Test'])
        print("[SUCCESS] Generated Output File: 'H2O_Best_Model_Test_Performance.csv'.")
        files.download('H2O_Best_Model_Test_Performance.csv')
        plt.figure(figsize=(8, 8))
        plt.scatter(y_true_test, y_pred_test, alpha=0.6, color=COLOR_PALETTE['Color4'])
        plt.plot([y_true_test.min(), y_true_test.max()], [y_true_test.min(), y_true_test.max()], color=COLOR_PALETTE['Color2'], linestyle='--')
        plt.title('Actual vs. Predicted Values'); plt.xlabel('Actual Values'); plt.ylabel('Predicted Values'); plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.gca().set_facecolor(COLOR_PALETTE['Color3'])
        plt.savefig('Scatter_Plot_Actual_vs_Predicted.png', dpi=300)
        print("[SUCCESS] Generated Output File: 'Scatter_Plot_Actual_vs_Predicted.png'.")
        files.download('Scatter_Plot_Actual_vs_Predicted.png')
        print("[SUCCESS] Sub-step 20.4: Evaluating Best Model and Generating Output Files Completed Successfully.")

        print("\n[SUCCESS] Step 20: Discovering Optimal Model with H2O AutoML Completed Successfully.")
        return best_model, leaderboard
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During H2O AutoML Process: {e}")
        return None, None
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 21: PERFORM STATISTICAL SIGNIFICANCE - DIEBOLD-MARIANO
#==============================================================================
def diebold_mariano_test(actuals, preds1, preds2):
    loss_diff = np.square(actuals - preds1) - np.square(actuals - preds2)
    d_mean = np.mean(loss_diff)
    d_var = np.var(loss_diff, ddof=0)
    if d_var == 0: return 0, 1.0
    dm_statistic = d_mean / np.sqrt(d_var / len(actuals))
    p_value = 2 * (1 - norm.cdf(np.abs(dm_statistic)))
    return dm_statistic, p_value

def perform_statistical_significance_test(baseline_model, best_h2o_model, h2o_leaderboard, train_df, test_df, dependent_var, independent_vars):
    print("\n===========================================================================================")
    print("STEP 21: Performing Statistical Significance Using Diebold-Mariano...")
    print("===========================================================================================")
    try:
        #--> Sub-step 21.1: Preparing Predictions for All Models:
        print("--> Sub-step 21.1: Preparing Predictions for All Models...")
        y_true = test_df[dependent_var].values
        baseline_model.fit(train_df[independent_vars], train_df[dependent_var])
        baseline_preds = baseline_model.predict(test_df[independent_vars])
        best_h2o_preds = best_h2o_model.predict(h2o.H2OFrame(test_df)).as_data_frame(use_multi_thread=True)['predict'].values
        print("[SUCCESS] All Model Predictions Are Ready.")
        print("[SUCCESS] Sub-step 21.1: Preparing Predictions for All Models Completed Successfully.")

        #--> Sub-step 21.2: Performing Diebold-Mariano Test: Baseline vs. H2O Models:
        print("\n--> Sub-step 21.2: Performing Diebold-Mariano Test: Baseline vs. H2O Models...")
        dm_results_baseline = []
        for model_id in h2o_leaderboard['model_id']:
            h2o_model = h2o.get_model(model_id)
            h2o_preds = h2o_model.predict(h2o.H2OFrame(test_df)).as_data_frame(use_multi_thread=True)['predict'].values
            dm_stat, p_val = diebold_mariano_test(y_true, baseline_preds, h2o_preds)
            comparison_name = f"Baseline_vs_{model_id}"
            dm_results_baseline.append({'Comparison': comparison_name, 'DM_Statistic': dm_stat, 'P_Value': p_val})
            print(f"[SUCCESS] Performed Diebold-Mariano Test for Comparison: '{comparison_name}'.")
        print("[SUCCESS] Sub-step 21.2: Performing Diebold-Mariano Test: Baseline vs. H2O Models Completed Successfully.")
        
        #--> Sub-step 21.3: Performing Diebold-Mariano Test: Best H2O vs. Other H2O Models:
        print("\n--> Sub-step 21.3: Performing Diebold-Mariano Test: Best H2O vs. Other H2O Models...")
        dm_results_best = []
        best_model_id = best_h2o_model.model_id
        for model_id in h2o_leaderboard['model_id']:
            if model_id == best_model_id: continue
            other_model = h2o.get_model(model_id)
            other_preds = other_model.predict(h2o.H2OFrame(test_df)).as_data_frame(use_multi_thread=True)['predict'].values
            dm_stat, p_val = diebold_mariano_test(y_true, other_preds, best_h2o_preds)
            comparison_name = f"{best_model_id}_vs_{model_id}"
            dm_results_best.append({'Comparison': comparison_name, 'DM_Statistic': dm_stat, 'P_Value': p_val})
            print(f"[SUCCESS] Performed Diebold-Mariano Test for Comparison: '{comparison_name}'.")
        print("[SUCCESS] Sub-step 21.3: Performing Diebold-Mariano Test: Best H2O vs. Other H2O Models Completed Successfully.")

        #--> Sub-step 21.4: Generating Output Files:
        print("\n--> Sub-step 21.4: Generating Output Files...")
        results_baseline_df = pd.DataFrame(dm_results_baseline)
        results_baseline_df['Row'] = [to_persian_numerals(i) for i in range(1, len(results_baseline_df) + 1)]
        results_baseline_df.to_csv('Diebold_Mariano_Baseline_vs_H2O.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Comparison', 'DM_Statistic', 'P_Value'])
        print("[SUCCESS] Generated Output File: 'Diebold_Mariano_Baseline_vs_H2O.csv'.")
        files.download('Diebold_Mariano_Baseline_vs_H2O.csv')
        results_best_df = pd.DataFrame(dm_results_best)
        results_best_df['Row'] = [to_persian_numerals(i) for i in range(1, len(results_best_df) + 1)]
        results_best_df.to_csv('Diebold_Mariano_Best_vs_Others.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Comparison', 'DM_Statistic', 'P_Value'])
        print("[SUCCESS] Generated Output File: 'Diebold_Mariano_Best_vs_Others.csv'.")
        files.download('Diebold_Mariano_Best_vs_Others.csv')
        print("[SUCCESS] Sub-step 21.4: Generating Output Files Completed Successfully.")

        #--> Sub-step 21.5: Reporting Final Statistics:
        print("\n--> Sub-step 21.5: Reporting Final Statistics...")
        best_vs_baseline_pval = results_baseline_df[results_baseline_df['Comparison'] == f"Baseline_vs_{best_model_id}"]['P_Value'].iloc[0]
        best_vs_others_count = (results_best_df['P_Value'] < 0.05).sum()
        print("\n--- Diebold-Mariano Test Statistics ---")
        print(f"1. Best H2O Model Statistically Superior to Baseline: {'Yes' if best_vs_baseline_pval < 0.05 else 'No'} (p-value: {best_vs_baseline_pval:.4f})")
        print(f"2. Best H2O Model Statistically Superior to {best_vs_others_count} out of {len(h2o_leaderboard)-1} other H2O models.")
        print("[SUCCESS] Sub-step 21.5: Reporting Final Statistics Completed Successfully.")

        print("\n[SUCCESS] Step 21: Performing Statistical Significance Completed Successfully.")
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Statistical Significance Analysis: {e}")
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 22: GENERATE FEATURE IMPORTANCE REPORT FOR KEY VARIABLES
#==============================================================================
def generate_feature_importance_report(best_model, name_map, fred_map):
    print("\n===========================================================================================")
    print("STEP 22: Generating Feature Importance Report for Key Variables...")
    print("===========================================================================================")
    try:
        #--> Sub-step 22.1: Calculating Feature Importance:
        print("--> Sub-step 22.1: Calculating Feature Importance...")
        algo = best_model.algo
        feature_importance = None
        if algo == 'glm':
            coef_dict = best_model.coef_norm()
            coef_df = pd.DataFrame(coef_dict.items(), columns=['variable', 'scaled_importance'])
            coef_df['scaled_importance'] = coef_df['scaled_importance'].abs()
            feature_importance = coef_df
        elif algo in ['gbm', 'drf', 'xgboost'] and hasattr(best_model, 'varimp'):
            feature_importance = best_model.varimp(use_pandas=True)
        else:
            print(f"[ERROR] Feature Importance is not implemented for the '{algo}' model. Skipping This Step.")
            print("===========================================================================================")
            return
        print("[SUCCESS] Feature Importance Has Been Calculated.")
        print("[SUCCESS] Sub-step 22.1: Calculating Feature Importance Completed Successfully.")

        #--> Sub-step 22.2: Preparing Report Data:
        print("\n--> Sub-step 22.2: Preparing Report Data...")
        stock_vars = [f"_Daily_Log_Return_{name}" for name in name_map.values()]
        macro_vars = list(fred_map.keys())
        key_independent_vars = stock_vars + macro_vars
        report_data = feature_importance[feature_importance['variable'].isin(key_independent_vars)].sort_values('scaled_importance', ascending=False)
        print(f"[SUCCESS] Data for {len(report_data)} Key Independent Variables Has Been Prepared.")
        print("[SUCCESS] Sub-step 22.2: Preparing Report Data Completed Successfully.")

        #--> Sub-step 22.3: Generating Feature Importance File:
        print("\n--> Sub-step 22.3: Generating Feature Importance File...")
        csv_df = report_data[['variable', 'scaled_importance']].copy()
        csv_df.columns = ['Variable_Name', 'Importance']
        csv_df['Row'] = [to_persian_numerals(i) for i in range(1, len(csv_df) + 1)]
        csv_df.to_csv('Feature_Importance_Results.csv', sep=',', index=False, encoding='utf-8-sig', columns=['Row', 'Variable_Name', 'Importance'])
        print("[SUCCESS] Generated Output File: 'Feature_Importance_Results.csv'.")
        files.download('Feature_Importance_Results.csv')
        print("[SUCCESS] Sub-step 22.3: Generating Feature Importance File Completed Successfully.")

        #--> Sub-step 22.4: Generating Feature Importance Plot:
        print("\n--> Sub-step 22.4: Generating Feature Importance Plot...")
        plot_data = report_data.sort_values('scaled_importance', ascending=True)
        plot_data['cleaned_variable'] = plot_data['variable'].str.replace('_Daily_Log_Return_', '').str.lstrip('_')
        palette_cycle = [COLOR_PALETTE['Color4'], COLOR_PALETTE['Color5'], COLOR_PALETTE['Color6']]
        colors = [palette_cycle[i % len(palette_cycle)] for i in range(len(plot_data))]
        plt.figure(figsize=(12, max(10, 0.25 * len(plot_data))))
        plt.barh(plot_data['cleaned_variable'], plot_data['scaled_importance'], color=colors)
        plt.xlabel('Scaled Importance'); plt.title('Feature Importance for Key Independent Variables'); plt.grid(True, axis='x', linestyle='--', linewidth=0.5)
        plt.gca().set_facecolor(COLOR_PALETTE['Color3'])
        plt.tight_layout()
        plt.savefig('Feature_Importance.png', dpi=300)
        print("[SUCCESS] Generated Output File: 'Feature_Importance.png'.")
        files.download('Feature_Importance.png')
        print("[SUCCESS] Sub-step 22.4: Generating Feature Importance Plot Completed Successfully.")

        print("\n[SUCCESS] Step 22: Generating Feature Importance Report Completed Successfully.")
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During Feature Importance Report Generation: {e}")
    finally:
        print("===========================================================================================")

#==============================================================================
# STEP 23: GENERATE SHAP SUMMARY PLOT FOR KEY VARIABLES
#==============================================================================
def generate_shap_summary_plot(best_model, train_df, test_df, name_map, fred_map):
    print("\n===========================================================================================")
    print("STEP 23: Generating SHAP Summary Plot for Key Variables...")
    print("===========================================================================================")
    try:
        #--> Sub-step 23.1: Calculating SHAP Values:
        print("--> Sub-step 23.1: Calculating SHAP Values...")
        if not hasattr(best_model, 'predict_contributions'):
            print("[ERROR] The Best Model Does Not Support Native SHAP Contributions. Skipping This Step.")
            print("===========================================================================================")
            return
        test_h2o = h2o.H2OFrame(test_df)
        algo = best_model.algo
        if algo == 'glm':
            print("Model is GLM, creating a summarized background frame for SHAP calculation...")
            independent_vars = [col for col in train_df.columns if col not in [DEPENDENT_VARIABLE, '_Date']]
            train_for_summary = train_df[independent_vars]
            train_summary_data = shap.kmeans(train_for_summary, 100)
            train_summary_df = pd.DataFrame(train_summary_data.data, columns=train_for_summary.columns)
            background_h2o = h2o.H2OFrame(train_summary_df)
            shap_values_h2o = best_model.predict_contributions(test_h2o, background_frame=background_h2o)
        else:
            shap_values_h2o = best_model.predict_contributions(test_h2o)
        print("[SUCCESS] SHAP Values Have Been Calculated.")
        print("[SUCCESS] Sub-step 23.1: Calculating SHAP Values Completed Successfully.")

        #--> Sub-step 23.2: Preparing Plot Data:
        print("\n--> Sub-step 23.2: Preparing Plot Data...")
        shap_values_df = shap_values_h2o.as_data_frame(use_multi_thread=True)
        shap_values = shap_values_df.iloc[:, :-1].values
        stock_vars = [f"_Daily_Log_Return_{name}" for name in name_map.values()]
        macro_vars = list(fred_map.keys())
        key_independent_vars = stock_vars + macro_vars
        feature_names = shap_values_df.columns[:-1]
        key_indices = [i for i, col in enumerate(feature_names) if col in key_independent_vars]
        filtered_shap_values = shap_values[:, key_indices]
        original_filtered_names = [feature_names[i] for i in key_indices]
        cleaned_feature_names = [name.replace('_Daily_Log_Return_', '').lstrip('_') for name in original_filtered_names]
        filtered_test_data = test_df[original_filtered_names].copy()
        print(f"[SUCCESS] Data for {len(cleaned_feature_names)} Key Independent Variables Has Been Prepared for Plotting.")
        print("[SUCCESS] Sub-step 23.2: Preparing Plot Data Completed Successfully.")

        #--> Sub-step 23.3: Generating SHAP Summary Plot:
        print("\n--> Sub-step 23.3: Generating SHAP Summary Plot...")
        colors = [COLOR_PALETTE['Color4'], COLOR_PALETTE['Color3'], COLOR_PALETTE['Color5']]
        cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)
        plt.figure()
        shap.summary_plot(filtered_shap_values, filtered_test_data, feature_names=cleaned_feature_names, 
                          show=False, plot_size=[12, max(8, 0.25 * len(cleaned_feature_names))],
                          max_display=len(cleaned_feature_names), cmap=cmap)
        plt.title('SHAP Summary Plot for Key Independent Variables')
        plt.tight_layout()
        plt.savefig('SHAP_Summary_Plot.png', dpi=300)
        print("[SUCCESS] Generated Output File: 'SHAP_Summary_Plot.png'.")
        files.download('SHAP_Summary_Plot.png')
        print("[SUCCESS] Sub-step 23.3: Generating SHAP Summary Plot Completed Successfully.")

        print("\n[SUCCESS] Step 23: Generating SHAP Summary Plot Completed Successfully.")
    except Exception as e:
        print(f"\n[ERROR] An Error Occurred During SHAP Summary Plot Generation: {e}")
    finally:
        print("===========================================================================================")

#=============================================================================
#                         --- MAIN EXECUTION FLOW ---
#=============================================================================
if 'IS_ENVIRONMENT_READY' in locals() and IS_ENVIRONMENT_READY:
    try:
        def to_persian_numerals(s):
            persian_map = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
            return str(s).translate(persian_map)

        PROJECT_START_DATE = '1995-09-09'
        PROJECT_END_DATE = '2025-09-28'
        DEPENDENT_VARIABLE = '_Daily_Log_Return_DJI'
        
        if 'ARE_DATA_ASSETS_READY' in locals() and ARE_DATA_ASSETS_READY:
            master_df = create_base_dataframe(PROJECT_START_DATE, PROJECT_END_DATE)
            if master_df is not None:
                all_ohlcv_data = download_ohlcv_data_batch(ticker_info_df, PROJECT_START_DATE, PROJECT_END_DATE)
                if all_ohlcv_data is not None:
                    master_df = process_and_merge_stock_features(master_df, all_ohlcv_data, ticker_info_df, SYMBOL_TO_NAME_MAP)
                    master_df = fetch_and_merge_fred_data(master_df, FRED_TICKERS_MAP)
                    master_df = fetch_and_merge_yfinance_indices(master_df, YFINANCE_TICKERS_MAP)
                    master_df = add_qualitative_variables(master_df, EVENTS_DATA_CSV)
                    master_df = calculate_dependent_variable(master_df)
                    preprocessed_df = handle_missing_values(master_df, ticker_info_df, SYMBOL_TO_NAME_MAP)
                    preprocessed_df = handle_outliers(preprocessed_df)
                    perform_stationarity_analysis(all_ohlcv_data, preprocessed_df, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP, DEPENDENT_VARIABLE); time.sleep(3)
                    perform_correlation_analysis(preprocessed_df, DEPENDENT_VARIABLE, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP); time.sleep(3)
                    optimized_df = optimize_data_types(preprocessed_df)
                    final_ordered_df = finalize_data_structure(optimized_df, ticker_info_df, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP, YFINANCE_TICKERS_MAP, DEPENDENT_VARIABLE); time.sleep(3)
                    generate_descriptive_statistics(final_ordered_df, DEPENDENT_VARIABLE, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP); time.sleep(3)
                    train_df, val_df, test_df = split_dataset(final_ordered_df)
                    if train_df is not None:
                        train_scaled_df, val_scaled_df, test_scaled_df = perform_data_standardization(train_df, val_df, test_df, DEPENDENT_VARIABLE)
                        if train_scaled_df is not None:
                            independent_vars_for_dm_test = [f"_Daily_Log_Return_{name}" for name in SYMBOL_TO_NAME_MAP.values()] + list(FRED_TICKERS_MAP.keys())
                            independent_vars_for_dm_test = [col for col in independent_vars_for_dm_test if col in train_scaled_df.columns]
                            baseline_model_instance = build_baseline_model(train_scaled_df, test_scaled_df, DEPENDENT_VARIABLE, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP); time.sleep(3)
                            best_h2o_model, h2o_leaderboard = discover_optimal_model_with_h2o(train_scaled_df, val_scaled_df, test_scaled_df, DEPENDENT_VARIABLE)
                            if best_h2o_model:
                                time.sleep(5)
                                perform_statistical_significance_test(baseline_model_instance, best_h2o_model, h2o_leaderboard, train_scaled_df, test_scaled_df, DEPENDENT_VARIABLE, independent_vars_for_dm_test); time.sleep(5)
                                generate_feature_importance_report(best_h2o_model, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP); time.sleep(3)
                                generate_shap_summary_plot(best_h2o_model, train_scaled_df, test_scaled_df, SYMBOL_TO_NAME_MAP, FRED_TICKERS_MAP)

    except Exception as e:
        print(f"\n[PIPELINE CRITICAL ERROR] The Execution Halted Due to an Unexpected Error: {e}")
    finally:
        if 'h2o' in globals() and h2o.cluster() is not None and h2o.cluster().is_running():
            h2o.cluster().shutdown()
            print("\n[PIPELINE STATUS] H2O Cluster Has Been Shut Down.")
        print("\n[PIPELINE STATUS] Main Execution Flow Finished.")