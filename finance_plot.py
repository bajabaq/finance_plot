#!/usr/bin/python3

import csv
import datetime
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas_datareader as pdr
import pandas
import os
import sys
import yfinance as yf

import finance_plot_aux

def plot_data2(ds):
    pandas.plotting.register_matplotlib_converters()
 
    symbol   = ds['symbol']
    longname = ds['longname']
    adates   = ds['adates']
    avals    = ds['avals']
    avals2   = ds['avals2']
    y        = ds['ays']  #y  = m*x + b
    m        = ds['m']    
    b        = ds['b']
    rms      = ds['rms']
    A        = ds['A']
    B        = ds['B']
    o        = ds['o']    #o  = A*exp(B*x)   
    rms2     = ds['rms2']
    #x  = numeric datetime
    xpyend   = datetime.datetime(today.year-1,12,31) #previous year end
    xnow     = datetime.datetime.today()             #now
    xnyend   = datetime.datetime(today.year,12,31)   #this year end

    #make the prediction
    p_x_vals   = [xnow, xnyend]
    p1_y_vals  = [avals2[0], m*mdates.date2num(xnyend) +b]
    p2_y_vals  = [avals[0], A*np.exp(B*mdates.date2num(xnyend),dtype=np.float128)]
    p1_ym_vals = [y[0], m*mdates.date2num(xnyend) + b]
    p2_ym_vals = [o[0], A*np.exp(B*mdates.date2num(xnyend),dtype=np.float128)]
    
    #make the bounding lines
    y1p = y + 1*rms
    y1m = y - 1*rms
    y2p = y + 2*rms
    y2m = y - 2*rms
    y3p = y + 3*rms
    y3m = y - 3*rms

    #2 vertically stacked subplots
    fig, axs = plt.subplots(2)
    fig.suptitle(symbol+"-"+longname)
    
    fm = "{:0.2e}".format(m)
    fb = "{:0.2e}".format(b)    
    label="y'="+fm + "x+"+ fb

    (ax1,ax2) = axs
    ax1.plot(adates,avals2,'o')
    ax1.plot(adates,y,'k-',label=label)
    ax1.plot(adates,y1p,'g-')
    ax1.plot(adates,y1m,'g-')
    ax1.plot(adates,y2p,'b-')
    ax1.plot(adates,y2m,'b-')
    ax1.plot(adates,y3p,'r-')
    ax1.plot(adates,y3m,'r-')
    ax1.axvline(x=xpyend, color='k', linestyle='--')
    ax1.axvline(x=xnow,   color='k', linestyle='--')
    ax1.axvline(x=xnyend, color='k', linestyle='--')
    ax1.plot(p_x_vals,p1_y_vals)
    ax1.plot(p_x_vals,p1_ym_vals, color='k', linestyle='dotted')

    fA = "{:0.2e}".format(A)
    fB = "{:0.2e}".format(B)    
    label2="y="+fA + "exp("+ fB + "x)"    

    anumdates = mdates.date2num(adates)


    y1p = np.exp(b+1*rms)*np.exp(m*anumdates,dtype=np.float128)
    y1m = np.exp(b-1*rms)*np.exp(m*anumdates,dtype=np.float128)
    y2p = np.exp(b+2*rms)*np.exp(m*anumdates,dtype=np.float128)
    y2m = np.exp(b-2*rms)*np.exp(m*anumdates,dtype=np.float128)
    y3p = np.exp(b+3*rms)*np.exp(m*anumdates,dtype=np.float128)
    y3m = np.exp(b-3*rms)*np.exp(m*anumdates,dtype=np.float128)

    
    ax2.plot(adates,avals,'o')
    ax2.plot(adates,o,'k-',label=label2)
    ax2.plot(adates,y1p,'g-')
    ax2.plot(adates,y1m,'g-')
    ax2.plot(adates,y2p,'b-')
    ax2.plot(adates,y2m,'b-')
    ax2.plot(adates,y3p,'r-')
    ax2.plot(adates,y3m,'r-')
    ax2.axvline(x=xpyend, color='k', linestyle='--')
    ax2.axvline(x=xnow,   color='k', linestyle='--')
    ax2.axvline(x=xnyend, color='k', linestyle='--')
    ax2.plot(p_x_vals,p2_y_vals)
    ax2.plot(p_x_vals,p2_ym_vals, color='k', linestyle='dotted')
    
    #format the ticks
    years     = mdates.YearLocator()
    months    = mdates.MonthLocator(bymonth=[0,12])
    years_fmt = mdates.DateFormatter('%Y')

    for ax in axs:
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)

        ax.legend()
   
        # round to nearest years.
        #datemin = np.datetime64(data['date'][0], 'Y')
        #datemax = np.datetime64(data['date'][-1], 'Y') + np.timedelta64(1, 'Y')
        #ax.set_xlim(datemin, datemax)

        # format the coords message box
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.format_ydata = lambda x: '%1.2f' % x  # format the ln(price).
        ax.grid(True)
    #endfor
    
    fig.autofmt_xdate()
    
    plt.show()

#enddef

def read_data2(sfile,key):
    try:
        with open(sfile,'r') as fh:
            r = csv.DictReader(fh)
            for row in r:
                val = row[key]
            #endfor
        #endwith
    except:
        val = ''
    #endtry
    print(val)
    return val
#enddef

def get_sfile(symbol,type=None):
    sfile = ""
    if type == "data":
        fname = symbol + "-data"    
    else:
        fname = symbol
    #endif
    sfile = os.path.join("data",fname+".csv")
        
    return sfile
#enddef

def yf_data(symbol,sfile2):
    #this call auto-adjusts the close price (change autoadjust=True/False if want different)
    tsymbol = yf.Ticker(symbol)
    
    #get the meta-data and save it
    try:
        tinfo = tsymbol.info
        with open(sfile2, "w") as fh:
            w = csv.DictWriter(fh,fieldnames=tinfo.keys())
            w.writeheader()
            w.writerow(tinfo)
            #endwith
    except Exception as e:
        print("couldn't get info for "+str(symbol)+" because:")
        print("Exception: " + str(e))
        print("This exception is likely because you entered a bad symbol")
        print("check that it is correct and try again")
        sys.exit()
    #endtry
    
    #get the price data and save it
    data    = tsymbol.history(period="max")
    return data
#enddef

def tiingo_data(symbol,sfile2):
    api_token = '88db8332611dff4362711e0364cf55f843937987'

    dtnow = datetime.datetime.today()
    dnow  = dtnow.strftime('%Y-%m-%d')
    print(dnow)
    
    
    df = pdr.get_data_tiingo(symbol, start='1972-01-01',end=dnow, api_key=api_token)['adjClose']

    #df.head()
    #df.describe()
        
    #get the meta-data and save it
    try:
        tinfo = tsymbol.info
        with open(sfile2, "w") as fh:
            w = csv.DictWriter(fh,fieldnames=tinfo.keys())
            w.writeheader()
            w.writerow(tinfo)
            #endwith
    except Exception as e:
        print("couldn't get info for "+str(symbol)+" because:")
        print("Exception: " + str(e))
        print("This exception is likely because you entered a bad symbol")
        print("check that it is correct and try again")
        sys.exit()
    #endtry
    
    #get the price data and save it
    data    = tsymbol.history(period="max")
    return data
#enddef
    
if __name__ == "__main__":
    symbols = []
    if len(sys.argv) == 1:
        print("Getting investments from ticker.txt")
        fh = open("ticker.txt","r")
        for line in fh:
            symbol = line.strip()
            if len(symbol) > 0:
                symbols.append(symbol)
            #endif
        #endfor
    else:
        ticker = sys.argv[1]        
        symbols.append(ticker)
    #endif
 
    today     = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    #5pm = 1700 to allow update
    market_close = datetime.datetime.combine(yesterday, datetime.time(17))

    for symbol in symbols:
        sfile        = get_sfile(symbol)
        get_new_data = False            
        if os.path.isfile(sfile):
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(sfile))
            if mtime < market_close: #new data should be available now
                get_new_data = True
            #else get_new_data = False
            #endif            
        else: #this symbol has not been retrieved before
            get_new_data = True
        #endif        
        print(symbol, "update:", get_new_data)
        sfile = get_sfile(symbol)
        sfile2= get_sfile(symbol,"data")
        if get_new_data:

            data = yf_data(symbol,sfile2)
            #data = tiingo_data(symbol,sfile2)
                    
            data.to_csv(sfile,sep='\t',encoding='utf-8')
        #endif

        (adates,aval,_ph,_pl) = finance_plot_aux.read_data(sfile)
        longname              = read_data2(sfile2,'longName')
        #print(adates, aval)
        (aval2,ays,m,b,rms,A,B,o,rms2,_roi) = finance_plot_aux.fit(adates,aval)

        ds = {}
        ds['symbol']    = symbol
        ds['longname']  = longname
        ds['adates']    = adates
        ds['avals']     = aval
        ds['avals2']    = aval2
        ds['ays']       = ays
        ds['m']         = m
        ds['b']         = b
        ds['rms']       = rms
        ds['A']         = A
        ds['B']         = B
        ds['o']         = o
        ds['rms2']      = rms2
        
        plot_data2(ds)
    #endfor
    
    sys.exit()
#endmain


