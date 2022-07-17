#!/usr/bin/python3

#this is python3 code

#import alpha_vantage
from alpha_vantage.timeseries import TimeSeries


import csv
import os



if __name__ == "__main__":

   # print(alpha_vantage.__file__)
   # exit()
    print("Running AlphaVantage to search for a symbol...")
    search_phrase = input("Type keywords to search: ")
    
    apikey = "DOA6TBRWMVBB2WWD"

    ts = TimeSeries(key=apikey,output_format='csv')
    data, meta_data = ts.get_symbol_search(keywords=search_phrase)
    
    for row in data:
        row_to_print = ', '.join(row) + "\n"
        print(row_to_print)
    #endfor


#endif

