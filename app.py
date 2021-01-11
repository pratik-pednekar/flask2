from flask import Flask, render_template, request, redirect

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from bokeh.plotting import figure, output_file, output_notebook, show

app = Flask(__name__)

@app.route('/')
def test():
	#initialize
	df = pd.DataFrame()
	dfs = []

	#Get API data from Alphavantage
	key = 'YG1YG39275HA39T5'
	ticker = 'AAPL'
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker,
																							 key)
	response = requests.get(url)																										 																									 key)
	content = json.loads(response.text)
	dic = content['Time Series (Daily)']
	a = pd.DataFrame.from_dict(dic)
	a = a.transpose()

	#Manipulating data
	newcol = []
	for i in a.columns:
		s = i.split('. ')[1]
	newcol.append(s)
	a.columns = newcol
	cols = a.columns[a.dtypes.eq("object")]
	a = a[cols].apply(pd.to_numeric, errors='coerce') \
	oneMonthLag = datetime.now() - timedelta(days=22)
	a.index = pd.to_datetime(a.index)
	c = a.iloc[a.index > oneMonthLag]

	#Plotting
	# output to static HTML file #output_notebook()
	output_file("lines.html")
	# create a new plot with a title and axis labels
	p = figure(title="simple line example", x_axis_label='Date', y_axis_label='Stock closing', x_axis_type='datetime')
	# add a line renderer with legend and line thickness
	p.line(c.index, c['close'], legend_label="Close", line_width=2)
	# show the results
	show(p)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)

"""
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/graph',methods=['GET','POST'])
def graph():
	ticker = request.form['stock_pick']
	p,error_message,month,year = plot_stock(ticker)
	script, div =components(p)
	kwargs = {'script':script,'div':div}
	kwargs['title'] = 'Stock Display'
	kwargs['error_message'] = error_message
	return render_template('graph.html',**kwargs)
"""


"""
@app.route('/')
def index():
  return render_template('index.html')"""


"""
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)"""



"""
@app.route('/', methods=['GET', 'POST']))
def login():
    error = None
    
    request.form['username']
                    
    return request.form['username']
    """
