#!/usr/bin/env python

#### DESCRIPTION ####
# Python Script to calculate a CDB invesment, considering the initial investment date, the CDB rate, ...
# an evaluation date and the CDI daily rate from a csv file.
# Programming Language: Python 3.8
# Wep Framework: Flask 1.1.2 - Werkzeug 1.0.1

__author__ = "Thiago Neves"
__copyright__ = ""
__credits__ = ["Thiago Neves"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Thiago Neves"
__email__ = "thiago.nc2@gmail.com"
__status__ = "Prototype"
__date__ = "2021-01-04"

# Flask functions
from flask import Flask, make_response, request, render_template, send_from_directory, jsonify
# converts string to datetime object and vice-versa
import datetime
# math for datetime objects
from datetime import datetime, timedelta
# Logging
import logging
from logging.handlers import RotatingFileHandler
# File management
import glob, os
from shutil import copyfile
from processing import cdbCalculator

# Initiate App
app = Flask(__name__)
app.config["DEBUG"] = True

# Define logging configuration, file name, path and level
logFile = 'cdbCalculator.log'
handler = RotatingFileHandler(logFile, maxBytes=1000000, backupCount=1)
handler.setLevel(logging.NOTSET)
app.logger.addHandler(handler)

# Main page with CDB Inputs, buttons, chart results
@app.route("/", methods=["GET", "POST"])
def main_page():

    # Rename log file to prevent downloading the same file
    logFile = 'cdbCalculator_' + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + '.log'

    # Log when the page is accessed
    app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'Main Page Accessed ' + 'ip:' + request.remote_addr)

    # Initial graphic preparing
    legend = 'Unit Prices (R$) - Initial Value: R$ 1000'
    legend2 = 'CDI Day Rate (%)'

    if request.method == "POST":

        # Ger user inputs
        dateStartUser = str(request.form["date-start"])
        cdbRateUser = float(request.form["cdbRate"])
        dateEndUser = str(request.form["date-end"])

        # Check if the dates are valid, if not, it means, if the evaluation date is before the start date, return page with exception
        date1 = datetime.strptime(dateStartUser, "%Y-%m-%d")
        date2 = datetime.strptime(dateEndUser, "%Y-%m-%d")
        if date1 > date2:
            return """
                <h2>Invalid dates</h2>
                <a href="/" > Calculate again </a>
            """

        # Prepare graphic variables with the cdbCalculator output
        fromCalculator = cdbCalculator(dateStartUser, cdbRateUser, dateEndUser)
        dates = fromCalculator[0]
        unitPrices = fromCalculator[1]
        cdiRates = fromCalculator[3]
        filePath = fromCalculator[5]

        # Register user inputs in log file
        app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'User Input data ->' + ' Investment Date:' + 
                        dateStartUser + ', CDB Rate:' + str(cdbRateUser) +
                        ', Initial Value:R$1000' + ', Evaluation Date:' + dateEndUser)

        # If there are more than 100 points to display, equally space the list for performance purpose
        if len(dates) > 100:
            unitPrices2 = []
            cdiRates2 = []
            dates2 = []
            interval = 0
            interval = round(len(dates)/100)
            for i in range(0,len(dates),interval):
                dates2.append(dates[i])
                unitPrices2.append(unitPrices[i])
                cdiRates2.append(cdiRates[i])
            # Ensure that last value will be visible
            dates2.append(dates[-1])
            unitPrices2.append(unitPrices[-1])
            cdiRates2.append(cdiRates[-1])
            # Update the lists whose shall be sent to the chart
            dates = dates2
            unitPrices = unitPrices2
            cdiRates = cdiRates2

        # Register main results in log file
        app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'Results ->' + ' Total Yield: ' + 
                        str(fromCalculator[4]) + '%' + ', Final Value: R$' + str(fromCalculator[2]))

        # Return a HTML page, with the input form and the graphic
        return render_template('line_chart2.html', values=unitPrices, values2=cdiRates,
                                labels=dates, legend=legend, legend2=legend2,
                                invDate = dateStartUser,
                                evDate = dateEndUser,
                                cdbRate = cdbRateUser,
                                totalYield = fromCalculator[4],
                                finalValue = fromCalculator[2],
                                filename = filePath, logFile = logFile,
                                downBtn='false')


    # Return a HTML with chart but no data
    return render_template('line_chart2.html', legend=legend, legend2=legend2, downBtn='true', logFile = logFile)

# Page for results Downloads
@app.route('/database_download/<path:filename>')
def database_download(filename):

    # Log results Download
    app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'File: ' + filename + ' Downloaded' )
    # Return results file
    return send_from_directory('database_download', filename, as_attachment=True)

# Page for log Downloads
@app.route('/log_download/<path:logFile>')
def log_download(logFile):

    # Delete file to prevent Browser Downloading the same file, once the address is the same
    for file in glob.glob("log_download/*.log"):
        os.remove(file)

    # Create a copy of the log when download in order to avoid the Browser Download the same file
    logFile = 'cdbCalculator_' + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + '.log'
    copyfile('cdbCalculator.log', 'log_download/' + logFile)

    # Log logfile Download
    app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'File: ' + logFile + ' Downloaded' )
    # Return log file
    return send_from_directory(directory='log_download', filename = logFile, as_attachment=True)