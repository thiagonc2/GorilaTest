# Python Script to calculate a CDB invesment, considering the initial investment date, the CDB rate, ...
# an evaluation date and the CDI daily rate from a csv file

__author__ = "Thiago Neves"
__copyright__ = ""
__credits__ = ["Thiago Neves"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Thiago Neves"
__email__ = "thiago.nc2@gmail.com"
__status__ = "Prototype"

from flask import Flask, make_response, request, render_template, send_from_directory, jsonify
from processing import cdbCalculator
# converts string to datetime object and vice-versa
import datetime
# math for datetime objects
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler

# Initiate App
app = Flask(__name__)
app.config["DEBUG"] = True

# Define logging configuration, file name, path and level
logFile = 'cdbCalculator.log'
handler = RotatingFileHandler('log_download/' + logFile, maxBytes=1000000, backupCount=1)
handler.setLevel(logging.NOTSET)
app.logger.addHandler(handler)

# Main page with CDB Inputs, buttons, chart results
@app.route("/", methods=["GET", "POST"])
def main_page():

    app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'Main Page Opened' )
    test = jsonify({'ip': request.remote_addr})

    # Initial graphic preparing
    legend = 'Unit Prices (R$) - Initial Value: R$ 1000'
    legend2 = 'CDI Day Rate (%)'

    if request.method == "POST":
        
        # Define result file name with current date and time
        filePath = 'results.csv'

        # Prepare graphic variables with the cdbCalculator output
        fromCalculator = cdbCalculator(str(request.form["date-start"]), float(request.form["cdbRate"]), str(request.form["date-end"]), filePath)
        dates = fromCalculator[0]
        unitPrices = fromCalculator[1]
        cdiRates = fromCalculator[3]

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

        # Return a HTML page, with the input form and the graphic
        return render_template('line_chart2.html', values=unitPrices, values2=cdiRates,
                                labels=dates, legend=legend, legend2=legend2,
                                invDate = str(request.form["date-start"]),
                                evDate = str(request.form["date-end"]),
                                cdbRate = str(request.form["cdbRate"]),
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
    return send_from_directory('database_download', filename, attachment_filename= 'results' + '_' + str(datetime.now()) + '.csv', as_attachment=True)

# Page for log Downloads
@app.route('/log_download/<path:logFile>')
def log_download(logFile):

    # Log logfile Download
    app.logger.info('LogInfo[' + str(datetime.now()) + ']: ' + 'File: ' + logFile + ' Downloaded' )
    # Return log file
    return send_from_directory(directory='log_download', filename = logFile ,
                                attachment_filename= 'cdbCalculator' + '_' + str(datetime.now()) + '.log',
                                as_attachment=True)