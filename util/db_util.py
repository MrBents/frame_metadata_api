import mysql.connector
from mysql.connector import Error
import sys
import os

class DbUtil():
    
    def __init__(self):
        self.result_list = []
        self.field_names = []

    def getTodaysOrders(self):
        try:
            connection = mysql.connector.connect(host=os.environ['DB_HOST'],
                                                database=os.environ['DB_NAME'],
                                                user=os.environ['DB_USER'],
                                                password=os.environ['DB_PWD'])
            if connection.is_connected():
                cursor = connection.cursor()
                
                cursor.execute('SELECT * FROM PreRoute_by_Orders')
                [self.field_names.append(i[0]) for i in cursor.description]
                [self.result_list.append(result) for result in cursor]

            else:
                print("didn't work")

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
        
   
        return self.dictionarize()

    
    def dictionarize(self):
        new_list = []
        for result in self.result_list:
            new_list.append(dict([(self.field_names[i], result[i]) for i in range(len(result))]))
        return new_list