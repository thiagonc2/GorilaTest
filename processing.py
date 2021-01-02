# methods to read csv tables and get dates-dailyCDI
import csv
# converts string to datetime object and vice-versa
import datetime
# math for datetime objects
from datetime import datetime, timedelta

# Creates a function for CDB calculation
    # Inputs:
        # investmentDate: date when the investment was made
        # cdbRate: percentage of the CDI that which the CDB will Yield
        # currentDate: date when the investment value shall be evaluated

    # Outputs:
        # outputDates: 
        # outputUnitPrices: 
        # currentPrice: 

debug = False

def cdbCalculator(investmentDate, cdbRate, currentDate):

    # Variables initialization
    currentDateLine = 0
    investmentDateLine = 0
    tcdi = []
    outputDates = []
    outputUnitPrices = []
    outputRates = []
    tcdiA = []

    # Import csv file with dates (without weekeds and holydays) and CDI rates
    with open('CDI_Prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # Create a Python 2D List with the csv file content
        cdiData = list(csv_reader)

    # While loop which runs until the input dates are found in the csv dates
        # Obs1.: The mininum and maximum dates are defined in the html page
        # Obs2.: If the input dates are "non-valid" i.e. weekends and holydays, it searched a "near"...
            # valid date by subtracting 1 day of the original date, until a valid date is found
    validDates = False
    currentHoly = 0
    startHoly = 0

    while validDates == False:
        line_count = 0
        for row in cdiData:
            if row[1] == currentDate:
                currentDateLine = line_count+1
            if row[1] == investmentDate:
                investmentDateLine = line_count+1
                break
            line_count += 1

        # Verify if the evaluation day was found in the list, if not, decrease to meet a valid day
        if currentDateLine == 0:
            currentDate = datetime.strptime(currentDate, "%Y-%m-%d")
            currentDate = currentDate - timedelta(1)
            currentDate = currentDate.strftime("%Y-%m-%d")
            currentHoly = 1

        # Verify if the start day was found in the list, if not, increase to meet a valid day
        if investmentDateLine == 0:
            investmentDate = datetime.strptime(investmentDate, "%Y-%m-%d")
            investmentDate = investmentDate - timedelta(1)
            investmentDate = investmentDate.strftime("%Y-%m-%d")
            startHoly = 1

        # Update de variable if both dates are valid
        if currentDateLine != 0 and investmentDateLine != 0:
            validDates = True

    # Update the list only with days and CDI values within the user evaluation range
    cdiData = cdiData[(currentDateLine-currentHoly):(investmentDateLine-startHoly)]
    #cdiData = cdiData[(currentDateLine):(investmentDateLine)]
    print(currentDateLine)

    # Create a list with daily TCD
    for row in range(len(cdiData)-1,-1,-1):
        tcdi.append(round((((float(cdiData[row][2])/100)+1)**(1/252))-1,8))

    # Create a list with the accumuleted TCD
    line_count3 = 0
    for x in tcdi:
        if line_count3 == 0:
            tcdiA.append(round((1+(tcdi[line_count3]*(cdbRate/100))),16))
        else:
            tcdiA.append(round((1+(tcdi[line_count3]*(cdbRate/100)))*tcdiA[line_count3-1], 16))
        line_count3 += 1

    # Organize and and create output lists
    line_count4 = 0
    for row in cdiData:
        outputDates.insert(line_count4, (cdiData[len(cdiData)-line_count4-1][1]))
        outputUnitPrices.insert(line_count4, (round(tcdiA[line_count4]*1000,8)))
        outputRates.insert(line_count4, (cdiData[len(cdiData)-line_count4-1][2]))
        line_count4 += 1

    # Get CDB price in the evaluation date
    currentPrice = outputUnitPrices[-1]

    # Total yield rate (%)
    totalYield = ((currentPrice - 1000)/1000)*100
    
    # Write results for output
    with open('database_download/results.csv', 'w', newline = '') as result_file:
        result_writer = csv.writer(result_file, delimiter=";")

        for i in range(0,len(outputDates),1):
            result_writer.writerow([outputDates[i],outputUnitPrices[i]])

    # Return outputs for chart and csv output file
    return(outputDates, outputUnitPrices, currentPrice, outputRates, totalYield)

# Output testing
if debug == True:
    investmentDate = "2010-01-09"
    cdbRate = 100
    currentDate = "2019-11-30"
    testOutput = cdbCalculator(investmentDate, cdbRate, currentDate)
    #print(testOutput)