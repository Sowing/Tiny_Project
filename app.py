from __future__ import print_function
from flask import Flask, render_template, request, redirect
import pandas
import numpy as np
import flask
from pandas import *



from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

import pandas as pd

app = Flask(__name__)

app.vars={}
@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['Company_Name'] = request.form['ticker']
        if not app.vars['Company_Name']:
            return render_template('error.html')
        '''
        app.vars['Close'] = request.form['Close']
        app.vars['Adj. Close'] = request.form['Adj. Close']        
        app.vars['Open'] = request.form['Open']
        app.vars['Adj. Open'] = request.form['Adj. Open']
        '''
        app.vars['features'] = request.form.getlist('features')
        #print app.vars['Company_Name'],app.vars['features']
        
        Company_Name=app.vars['Company_Name']
        API_url='https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?api_key=a5-JLQBhNfxLnwxfXoUE' % Company_Name
        data = pd.read_csv(API_url,parse_dates=['Date'])
        Colors=["blue","green","yellow","red"]
        Color_index=0
        target_data=data.ix[:,['Open','Adj. Open','Close','Adj. Close']]
        p=figure(x_axis_type="datetime")
        p.xaxis.axis_label = 'Date'
        p.title = 'Data from Quandle WIKI set'
        if 'Close' in app.vars['features']:
            p.line(x=data['Date'],y=target_data['Close'],legend="%s:Close" % Company_Name, line_color=Colors[Color_index])
            Color_index = Color_index +1
        if 'Adj. Close' in app.vars['features']:
            p.line(x=data['Date'],y=target_data['Adj. Close'],legend="%s:Adj. Close" % Company_Name, line_color=Colors[Color_index])
            Color_index = Color_index +1
        if 'Open' in app.vars['features']:
            p.line(x=data['Date'],y=target_data['Open'],legend="%s:Open" % Company_Name, line_color=Colors[Color_index])
            Color_index = Color_index +1
        if 'Adj. Open' in app.vars['features']:
            p.line(x=data['Date'],y=target_data['Adj. Open'],legend="%s:Adj. Open" % Company_Name, line_color=Colors[Color_index])


        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        script, div = components(p, INLINE)
        html = flask.render_template(
            'embed.html',
            plot_script=script,
            plot_div=div,
            js_resources=js_resources,
            css_resources=css_resources,
            Company_Name= Company_Name
        )
        return encode_utf8(html)
        
       # return 'request.method was not a GET!'

if __name__ == '__main__':
  app.run(port=33507)
