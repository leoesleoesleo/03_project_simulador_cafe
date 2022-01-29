import sqlite3
from sqlite3 import Error
import logging
import json
import os

class Sql():    
                
    def sql_connection(self):
        try:
            con = sqlite3.connect('modelo/memory4.db')
            return con
        except Error:
            return "Error"
        """
        finally:
            con.close()
        """
        
    def sql_table(self):
        con = self.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute("CREATE TABLE data_in(data text)")
        con.commit()
            
    def sql_insert(self,data):
        con = self.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute('''INSERT INTO data_in(data) VALUES(?)''', str(data))
        con.commit()
        
    def sql_fetch(self):
        con = self.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM data_in')
        rows = cursorObj.fetchall()
        for row in rows:
            print(row)

sql = Sql()        

sql.sql_table()

"""
ROOT_FILE = os.path.dirname(os.path.realpath('__file__'))
FILE_INPUT = os.path.join(ROOT_FILE, 'json', 'data_in.json')

def json_input(file):
    with open (file,'rb') as file:
        data = json.load(file)
    return data

data = json_input(FILE_INPUT)

sql.sql_insert(data)

"""

#sql.sql_fetch()
