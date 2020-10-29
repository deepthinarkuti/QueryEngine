
Project Overview:
Facilitate the users to enter commands through command prompt and provide query results to the user by querying the data from the CSV files. SELECT, FROM, ORDERBY, COUNTBY, JOIN, TAKE(limit) queries are executed for this project
Approach:
Read the data from the command prompt, parse the data and identify the query requested by the user. Execute the query on the CSV files by converting the data to the data frames and accessing/querying the data according to the input command provided.
Retrieved the resultant data from the CSV files and display the results in the command prompt to the user

Design Decisions:
I have considered various approaches for querying the CSV files. One was using a backend database.
But, after considering all the options, Querying the CSV files directly by parsing the input received through
command prompt and then displaying the results to the users is considered as optimal solution to the problem.


Assumptions:
1.Duplicate column values are allowed in the Join Query for more than 2 CSV files
2.If the same count exists for the COUNTBY, then ORDERBY for such rows is done based on the COUNTBY Column value

Prerequisites:
pandas, python

Steps to run the code:
Please run the main.py for the project and test.py for the unit tests
Unzip the file and run the commands through command prompt

1) Command to run the project:
python main.py FROM city.csv
python main.py FROM city.csv SELECT CityName,CityID
python main.py FROM city.csv TAKE 5
python main.py FROM city.csv ORDERBY CityPop TAKE 10
python main.py FROM city.csv JOIN country.csv CountryCode
python main.py FROM language.csv COUNTBY Language ORDERBY count TAKE 7

2) Command to run the unit tests:
python -m unittest test.py



