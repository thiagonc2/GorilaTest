# CDB Calculator

This project is a CDB investment calculator, it evaluates the daily price of a single CDB investment given the date of the investment and the date of the evaluation. The CDB default value is of R$1000.00, the CDB price is calculated for each day between the initial and final date, the available dates for evaluation are between 2010-01-04 and 2019-12-03. Once the calculation was done, one can Download the "results.csv" file. Furthermore a log file, "cdbCalculator.log", is available for Download, with the history of the application.

## Installation

* Install Python version 3.8
* Create a new Python Environment
* Clone the Repository and use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirements:

```bash
pip install -r requirements.txt
```

## Usage

In the top-level folder, define the file which will be used in the Flask server:

```python
$env:FLASK_APP = "app"
```

The, run the development server:

```python
flask run
```
Go to your favorite web browser and open:
http://locallhost:5000

## Deployed Application via Azure Web App

[https://gorilatestthiago.azurewebsites.net/](https://gorilatestthiago.azurewebsites.net/)

## Key Python Modules Used

* Python 3.8
* Flask version 1.1.2

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
