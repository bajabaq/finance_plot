
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import pandas as pd

pd.plotting.register_matplotlib_converters()

# Set the style to seaborn for plotting
plt.style.use('seaborn')


api_token = '88db8332611dff4362711e0364cf55f843937987'

tickers=['VSMAX']

tickers=[]
with open('ticker.txt','r') as fh:
        for line in fh:
                tickers.append(line.strip())
        #endfor
#endwith
        
for ticker in tickers:

	df = pdr.get_data_tiingo(ticker, start='1972-01-01',end='2021-12-11', api_key=api_token)['adjClose']

	df.head()
	df.describe()


	fig, ax = plt.subplots(figsize=(12, 6))# Plot the cumulative returns fot each symbol
	ax.plot(df.loc[ticker])
	ax.legend()
	plt.title('Adjusted Close Price', fontsize=16) # Define the labels for x-axis and y-axis
	plt.ylabel('Adjusted Close Price', fontsize=14)
	plt.xlabel('Year', fontsize=14)
	plt.show()
	plt.close()

	#ax.plot((df.loc[ticker].pct_change()+1.cumprod()-1,label=ticker)
#endfor




