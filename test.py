import unittest
import main
from main import *


class TestQueries(unittest.TestCase):

    def test_printrows(self):
        csvdata = pandas.read_csv('city.csv')
        self.assertEqual(len(printrows(csvdata, 0, len(csvdata))), 4079)
        csvdata = pandas.read_csv('language.csv')
        self.assertEqual(main.printrows(csvdata, 0, len(csvdata))[0][0], 'ABW')
        csvdata = pandas.read_csv('country.csv')
        self.assertEqual(len(main.printrows(csvdata, 0, len(csvdata))), 239)
        csvdata = pandas.read_csv('country.csv')
        self.assertEqual(len(main.printrows(csvdata, 0, 0)), 0)
        csvdata = pandas.read_csv('language.csv')
        self.assertEqual(len(main.printrows(csvdata, 3, 0)), 0)
        csvdata = pandas.read_csv('city.csv')
        self.assertEqual(len(main.printrows(csvdata, -1, -3)), 0)

    def test_TAKE_query_success(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'TAKE', '10']
        self.assertEqual(len(main.identifyquery(sys.argv)), 10)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'TAKE', '5']
        self.assertEqual(len(main.identifyquery(sys.argv)), 5)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'TAKE', '20']
        self.assertEqual(main.identifyquery(sys.argv)[5][0], 6)
        # if limit is greater than number of rows then total rows would be returned
        sys.argv = ['main.py', 'FROM', 'city.csv', 'TAKE', '5050']
        self.assertEqual(len(main.identifyquery(sys.argv)), 4079)

    def test_TAKE_query_failure(self):
        # for negative limit, 0 rows would be returned
        sys.argv = ['main.py', 'FROM', 'language.csv', 'TAKE', '-10']
        self.assertNotEqual(main.identifyquery(sys.argv), -10)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'TAKE', '-50']
        self.assertEqual(main.identifyquery(sys.argv), 0)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'TAKE', '0']
        self.assertEqual(len(main.identifyquery(sys.argv)), 0)

    def test_ORDERBY_query_success(self):
        # If tAKE is added to the query only 10 rows are returned else all the rows are returned in descending order
        sys.argv = ['main.py', 'FROM', 'city.csv', 'ORDERBY', 'CityPop', 'TAKE', '10']
        self.assertEqual(len(main.identifyquery(sys.argv)), 10)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'ORDERBY', 'CityPop']
        self.assertEqual(len(main.identifyquery(sys.argv)), 4079)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'ORDERBY', 'Language']
        self.assertEqual(len(main.identifyquery(sys.argv)), 984)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'ORDERBY', 'CountryName']
        self.assertEqual(len(main.identifyquery(sys.argv)), 239)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'ORDERBY', 'CityPop', 'TAKE', '10']
        self.assertEqual(main.identifyquery(sys.argv)[0][3], 10500000)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'ORDERBY', 'CityPop']
        self.assertEqual(main.identifyquery(sys.argv)[4078][3], 42)

    def test_ORDERBY_query_failure(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'THEN', 'CityPop', 'TAKE', '10']
        self.assertNotEqual(main.identifyquery(sys.argv), 4079)
        # City Pop value without sorting is not equal to value after order by as the highest value is in the first row
        sys.argv = ['main.py', 'FROM', 'city.csv', 'ORDERBY', 'CityPop']
        self.assertNotEqual(main.identifyquery(sys.argv)[0][3], 1780000)
        # Checking if ordered by ascending order or descending order
        sys.argv = ['main.py', 'FROM', 'city.csv', 'ORDERBY', 'CityPop']
        self.assertNotEqual(main.identifyquery(sys.argv)[0][3], 42)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'AND', 'CountryName']
        self.assertNotEqual(main.identifyquery(sys.argv), 239)

    def test_JOIN_query_success(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'JOIN', 'country.csv', 'CountryCode']
        self.assertEqual(len(main.identifyquery(sys.argv)), 4079)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'JOIN', 'city.csv', 'CountryCode']
        self.assertEqual(len(main.identifyquery(sys.argv)), 4086)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'JOIN', 'country.csv', 'CountryCode']
        self.assertEqual(main.identifyquery(sys.argv)[0][1], 'Kabul')
        sys.argv = ['main.py', 'FROM', 'city.csv', 'JOIN', 'country.csv', 'CountryCode']
        self.assertEqual(main.identifyquery(sys.argv)[3][6], 22720000)

    def test_JOIN_query_failure(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'AND', 'country.csv', 'CountryCode']
        self.assertNotEqual(main.identifyquery(sys.argv), 4079)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'THEN', 'country.csv', 'CountryCode']
        self.assertEqual(main.identifyquery(sys.argv), 0)

    def test_FROM_query_success(self):
        sys.argv = ['main.py', 'FROM', 'city.csv']
        self.assertEqual(len(main.identifyquery(sys.argv)), 4079)
        sys.argv = ['main.py', 'FROM', 'language.csv']
        self.assertEqual(len(main.identifyquery(sys.argv)), 984)
        sys.argv = ['main.py', 'FROM', 'country.csv']
        self.assertEqual(len(main.identifyquery(sys.argv)), 239)
        sys.argv = ['main.py', 'FROM', 'country.csv']
        self.assertEqual(main.identifyquery(sys.argv)[0][0], 'ABW')
        sys.argv = ['main.py', 'FROM', 'country.csv']
        self.assertEqual(main.identifyquery(sys.argv)[238][3], 11669000)

    def test_FROM_query_failure(self):
        # Wrong Clause AND instead of FROM in the input
        sys.argv = ['main.py', 'AND', 'city.csv']
        self.assertNotEqual(main.identifyquery(sys.argv), 4079)
        sys.argv = ['main.py', 'AND', 'language.csv']
        self.assertNotEqual(main.identifyquery(sys.argv), 239)
        sys.argv = ['main.py', 'NOT', 'country.csv']
        self.assertEqual(main.identifyquery(sys.argv), 0)

    def test_SELECT_query_success(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'SELECT', 'CityName,CityID']
        self.assertEqual(len(main.identifyquery(sys.argv)), 4079)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'SELECT', 'Language']
        self.assertEqual(len(main.identifyquery(sys.argv)), 984)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'SELECT', 'CountryName,Continent']
        self.assertEqual(len(main.identifyquery(sys.argv)), 239)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'SELECT', 'CityName,CityID']
        self.assertEqual(main.identifyquery(sys.argv)[0][1], 1)
        sys.argv = ['main.py', 'FROM', 'city.csv', 'SELECT', 'CityName,CityID']
        self.assertEqual(main.identifyquery(sys.argv)[4078][0], 'Rafah')

    def test_SELECT_query_failure(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'WHEN', 'Language']
        self.assertNotEqual(main.identifyquery(sys.argv), 4079)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'THEN', 'CityName,CityID']
        self.assertNotEqual(main.identifyquery(sys.argv), 984)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'NOT', 'CountryName,Continent']
        self.assertEqual(main.identifyquery(sys.argv), 0)

    def test_COUNTYBY_query_success(self):
        # If take is given in input then limited rows else all the rows grouped by column name and ordered by count
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count', 'TAKE', '7']
        self.assertEqual(len(main.identifyquery(sys.argv)), 7)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count']
        self.assertEqual(len(main.identifyquery(sys.argv)), 457)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'COUNTBY', 'CountryName', 'ORDERBY', 'count', 'TAKE', '10']
        self.assertEqual(len(main.identifyquery(sys.argv)), 10)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count', 'TAKE', '7']
        self.assertEqual(main.identifyquery(sys.argv)[0][0], 'English')
        # Checking if the order by is done in the ascending order or descending order
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count', 'TAKE', '7']
        self.assertEqual(main.identifyquery(sys.argv)[6][1], 17)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count', 'TAKE', '7']
        self.assertEqual(main.identifyquery(sys.argv)[0][1], 60)

    def test_COUNTYBY_query_failure(self):
        sys.argv = ['main.py', 'FROM', 'city.csv', 'AND', 'CityName,CityID']
        self.assertNotEqual(main.identifyquery(sys.argv), 4079)
        sys.argv = ['main.py', 'FROM', 'language.csv', 'WHEN', 'Language']
        self.assertNotEqual(main.identifyquery(sys.argv), 984)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'THEN', 'CountryName,Continent']
        self.assertEqual(main.identifyquery(sys.argv), 0)
        # Checking if the TAKE is applied
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count', 'TAKE', '7']
        self.assertNotEqual(len(main.identifyquery(sys.argv)), 457)
        # Checking if sorted in ascending or descending order
        sys.argv = ['main.py', 'FROM', 'language.csv', 'COUNTBY', 'Language', 'ORDERBY', 'count', 'TAKE', '7']
        self.assertNotEqual(main.identifyquery(sys.argv)[0][1], 17)

    def test_printselectedcolumns(self):
        csvdata = pandas.read_csv('city.csv')
        sys.argv = ['main.py', 'FROM', 'city.csv', 'SELECT', 'CityName']
        self.assertEqual(len(main.printselectedcolumns(csvdata, len(sys.argv), sys.argv)), 4079)
        csvdata = pandas.read_csv('language.csv')
        sys.argv = ['main.py', 'FROM', 'language.csv', 'SELECT', 'Language']
        self.assertEqual(len(main.printselectedcolumns(csvdata, len(sys.argv), sys.argv)), 984)
        csvdata = pandas.read_csv('country.csv')
        sys.argv = ['main.py', 'FROM', 'country.csv', 'SELECT', 'CountryPop']
        self.assertEqual(len(main.printselectedcolumns(csvdata, len(sys.argv), sys.argv)), 239)
        sys.argv = ['main.py', 'FROM', 'country.csv', 'SELECT', 'CountryPop']
        self.assertEqual(main.printselectedcolumns(csvdata, len(sys.argv), sys.argv)[0][0], 103000)

    def test_printheader(self):
        csvdata = pandas.read_csv('city.csv')
        self.assertEqual(len(main.printheader(csvdata)), 4)
        csvdata = pandas.read_csv('language.csv')
        self.assertEqual(len(main.printheader(csvdata)), 2)
        csvdata = pandas.read_csv('country.csv')
        self.assertEqual(len(main.printheader(csvdata)), 5)
        csvdata = pandas.read_csv('city.csv')
        self.assertEqual(len(main.printheader(csvdata)), 4)
        csvdata = pandas.read_csv('city.csv')
        self.assertEqual(main.printheader(csvdata)[0], 'CityID')
        csvdata = pandas.read_csv('language.csv')
        self.assertEqual(main.printheader(csvdata)[1], 'Language')
