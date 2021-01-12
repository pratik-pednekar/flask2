from flask import Flask, render_template, request, redirect
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from bokeh.plotting import figure
from bokeh.embed import components
#from bokeh.io import output_notebook, push_notebook, show

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/plot',methods = ['POST', 'GET'])
def plot():
    if request.method=='GET':
        return "You came here directly, please visit the home page"
    if request.method=='POST':

        data=request.form
        for key,val in data.items():
            v1 = val

        # Get API data from Alphavantage
        key = 'YG1YG39275HA39T5'
        ticker = 'AAPL'
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker,key)
        response = requests.get(url)
        content = json.loads(response.text)
        dic = content['Time Series (Daily)']
        a = pd.DataFrame.from_dict(dic)
        a = a.transpose()

        # Manipulating dataframe
        newcol = []
        for i in a.columns:
            s = i.split('. ')[1]
            newcol.append(s)
        a.columns = newcol
        cols = a.columns[a.dtypes.eq("object")]
        a = a[cols].apply(pd.to_numeric, errors='coerce')
        oneMonthLag = datetime.now() - timedelta(days=22)
        a.index = pd.to_datetime(a.index)
        c = a.iloc[a.index > oneMonthLag]

        #Plotting using Bokeh
        p = figure(title="simple line example", x_axis_label='Date', y_axis_label='Stock closing',
                   x_axis_type='datetime')
        p.line(c.index, c['close'], legend_label="Close", line_width=2)
        script,div = components(p)

        #return render_template('plot.html',tick=data)
        return render_template('plot.html', div=div, script=script)

if __name__=='__main__':
    app.run(debug=True)
    #app.run(host='localhost', port =5000, debug=True)

"""
m = [1, 2, 3, 4, 5]
n = [.24, .68, .99, .69, .11]
p = figure(title="simple line example", x_axis_label='xaxis', y_axis_label='yaxis')
p.line(m, n, legend_label="Trial", line_width=2)"""