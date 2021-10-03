# DBCalc
A quick tool to help parse output .csv's from UDB and create gradebook .csv's to throw into Canvas

### Written by Brian Caskey on 10/01/2021

## Executable
To get the .exe file, check out the list of releases (probably on the right-hand side of this screen). Your computer will complain about it being malware, and you'll need to convince it that the .exe is safe multiple times. If you aren't comfortable doing so, you can also run it as a python script. Steps to do that are after this section!

Double click on the .exe, you should see a dialogue box appear (if you get an error message, you may need to install Visual C++ Redistributable), see the link below:

https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-160


## Running as Python Script
Python is pretty accesible and easy to run so you're in luck. 
### Windows
First, install python 3.9.x, see the link below. Make sure to have the checkbox for 'ADD TO PATH' checked. 

https://www.python.org/downloads/

Next, open a command terminal in your computer by typing 'cmd' in the search box. In there, you'll need to get the pandas library. Simply type 

`pip install pandas`

and pandas will install itself. Next, navigate to where the python file is in your computer in your cmd terminal. The command will look like: 

`cd \path\to\main.py`

When you are there, simply type

`python main.py`

and the python script will run!

## Dependencies
If you wish to dev on this script, you will need pandas, install it either into your venv or with 

`
pip install pandas
`

## Running
To run DBCalc, simply run the exectuable main.exe. If you wish to run the actual py file, you will simply run 

`
python main.py
`

Either way, a UI should open up. Select the UDB .csv you wish to anlyse and double click on it. The program will churn for a second or two, and then output a 'OUTPUT.CSV' file with your desired output. Happy calc-ing!
