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

from flask import Flask, make_response, request, render_template, send_from_directory
from processing import cdbCalculator

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def main_page():
    # Initial graphic preparing
    legend = 'Unit Prices (R$) - Initial Value: R$ 1000'
    legend2 = 'CDI Day Rate (%)'

    if request.method == "POST":
        
        # Prepare graphic variables with the cdbCalculator output
        fromCalculator = cdbCalculator(str(request.form["date-start"]), float(request.form["cdbRate"]), str(request.form["date-end"]))
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
                                filename='results.csv')

    # Return a HTML with chart but no data
    return render_template('line_chart2.html', legend=legend, legend2=legend2)

@app.route('/database_download/<path:filename>')
def database_download(filename):

    return send_from_directory('database_download', filename, as_attachment=True)