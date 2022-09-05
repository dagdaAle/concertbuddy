import mysqlx
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import csv
from csv import reader
import datetime
import mysqlx
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


with open('concerti.csv',encoding="utf-8") as csv_file:

    for row in csv_file:
        try:
            conn = mysql.connect(host='localhost', database='concert', user='root', password='Progetto.fitbit22')
            cursor = conn.cursor()
            
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('INSERT INTO concert_buddy.concert(city_name, concert_name, date, image_url) VALUES (%s,%s,%s,%s);',row)
            print('Creating table....')
        except Error as e:
            print("Error while connecting to MySQL", e)