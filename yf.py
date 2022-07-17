
import datetime
import numpy as np
import pandas 
import yfinance as yf

now  = datetime.datetime.now()
nowd = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

#this provides the auto-adjusted close price (change autoadjust=True/False if want different)
#use this vs download which doesn't
agg  = yf.Ticker("VTABX")

ainfo = agg.info
#for k,v in ainfo.items():
#    print(k,v)

#print(ainfo)
print(ainfo['longName'])

exit()
data = agg.history(period="max")

print(data)

data.to_csv('tmp.csv',sep='\t',encoding='utf-8')


#np.savetxt("tmp.txt",data)



