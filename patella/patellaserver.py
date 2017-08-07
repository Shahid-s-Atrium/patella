# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
This module controls all flask function - from startup to routing urls to the correct html file.
the html files name, functions, and elements,  for reference

index.html: index is the home page. It has 4 links on it - to input.html, to github, and two placeholder routes to input
input.html: input is the home page for patella. it has 2 forms with 2 text fields each, and two submit buttons.
            form 1:
                text field 1: name: url, POSTs the url to be scraped
                text field 2: name: filetype, POSTs the filetype to be looked for
            form 2:
                text field 1: name: filepath, POSTs the local filepath to be plotted
                text field 2: name: datacol, POSTs the column to use for data
options.html: options is the page where the user selects the correct link or table. It has a lsit of radio buttons
              and a text field to specify the file download name, along with a submit button.
              form 1:
                radio field: name:dlink, list of links as radio buttons, POSTs selected
                text field: name: outname, POSTs name of downloaded file
table.html: table is the page which displays the table  generated from the previously downloaded file. it has 2 text
            fields which allows the user to specify the data and date columns
            form 1:
                text field 1: name = datacol, POSTs data column to be used
                text field 2: name = yrcol, POSTs the date column to be used
plotlocal.html: plotlocal is the page which actually displays the plot. it has no forms, just the bokeh js plot
                components along with the table used to generate it

Every html table has a footer with a link which routes back to /input, while /input has a link to /index, the home page.
"""


'''Local Imports'''
from . import htmlparser as htmlparser

'''Third Party Imports'''
from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'data/'
x_axis_label = ''
y_axis_label = ''
title = ''
urlpath = 'patella'

# A simple function for starting the webservice with varying url prefixes
def startserver(path):
    global urlpath
    urlpath = path
    app.run(debug=True, host='0.0.0.0', port=4444)


# The 'home' page route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name=urlpath)

# the input route for inputting urls and files
@app.route('/<string:var>/input', methods =['POST', 'GET'])
def flask_scrape(var):
    return render_template('input.html', var=var)


# the route which allows users to pick which link they would like to download
@app.route('/<string:var>/options', methods=['POST', 'GET'])
def options(var):
    if request.method == 'POST':
        url = request.form['url']
        filetype = request.form['filetype']

        prompt = 'Choose a link to download:'
        button = 'Download and Create Table'
        filename = 'Name of downloaded file'
        try:
            parseobj = htmlparser.find_download_links(url, filetype, 'datafile.csv', download=False)
            result = parseobj['href_list']
            return render_template('options.html',
                                   result=result,
                                   ftype=filetype,
                                   var=var,
                                   prompt=prompt,
                                   button=button,
                                   filename=filename)
        except Exception as exc:
            htmlparser.prlog(exc)
            return render_template('input.html', error=exc, var=var)



# the route for the options page, which allows users to specify data and time columns
# needs to be updated to allow title, x, and y axis labels to be input - a project from some jquery/js/node.js
@app.route('/<string:var>/table', methods=['POST', 'GET'])
def table(var):
    if request.method == 'POST':
        dlname = request.form['dlink']
        outname = request.form['outname']
        print(outname)
        htmlparser.find_download_links(dlname[:-1], '.csv', outname, download=True)
        table = htmlparser.file_to_htmltable(os.getcwd() + '/data/' + outname)
        return render_template('table.html', linkname=dlname, table=table, var=var)#['template']

# the route whuch rediracts to the page which plots files from a specified path from the input page
@app.route('/<string:var>/plotlocal', methods=['POST', 'GET'])
def plotted(var):
    if request.method == 'POST':
        data_column = request.form['datacol']   # Get the data column input from html form
        result = request.form
        filename = result['filepath']
        filepath = filename
        df = pd.read_table(filepath, ',', header=0, engine='python')
        return htmlparser.compare(df, data_column, x_axis_label, y_axis_label, title, year_col='Year',
                                  urlth=var)  # Return compare() which returns a render_template() object


# the route which links to /table - the final graph you get when the entire process is completed
@app.route('/<string:var>/plot', methods=['POST', 'GET'])
def plot_from_df(var):
    error = 'Sorry, an error has occured, and were not sure what is is (>T-T<)'
    if request.method == 'POST':
        result = request.form # store the form results as result
        data_column = result['datacol']  # get the data column from html form
        year_column = result['yearcol'] # get the year column from the html form
        filepath = os.getcwd() + '/data/' + 'datafile.csv'
        if os.path.isfile(filepath):
            try:
                df = pd.read_table(filepath, ',', header=0, engine='python')
                return htmlparser.compare(df, data_column, x_axis_label, y_axis_label, title, year_col=year_column,
                                      urlth=var)  # Return compare() which returns a render_template() object
            except Exception as exc:
                error = exc
                htmlparser.prlog(error)
                return render_template('input.html', error=error, var=var)
        else:
            htmlparser.prlog(error)
            return render_template('input.html', error=error, var=var)
    

if __name__ == '__main__':
    startserver(urlpath)
