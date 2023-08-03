#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask, render_template, request, send_file
from io import BytesIO
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

exchanges = ["NYSE", "NASDAQ", "NSE", "BSE", "SSE", "NIK", "LSE"]
suffixes = {"NSE": ".NS", "BSE": ".BO", "SSE": ".SS", "LSE": ".L"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    index = request.form['index'].upper()
    stock1 = request.form['stock1'].upper()
    stock2 = request.form['stock2'].upper()
    stock3 = request.form['stock3'].upper()
    datatype = request.form['datatype'].capitalize()

    if index not in exchanges:
        return "Invalid entry: Please choose a valid stock exchange."

    if index in suffixes:
        suffix = suffixes[index]
        stock1 += suffix
        stock2 += suffix
        stock3 += suffix

    stocks = [stock1, stock2, stock3]

    stock_data = yf.download(stocks, start="2010-01-01", end="2024-01-01")
    data = stock_data.loc[:, datatype].copy()
    normdata = data.div(data.iloc[0]).mul(100)

    plt.figure(figsize=[15, 8])
    normdata.plot()
    plt.legend(fontsize=16)

    # Save the plot to a temporary file
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




