import mysql.connector
import six
import json
import pipes
import os
import platform
import time

class SqlConnection:

    def closeConnection(self):
        try:
            self.cursor.close()
            del self.cursor
            self.conn.close()
        except:
            pass

    def execute(self, command):
        self.cursor.execute(command)
        self.conn.commit()

    def convertValueToSqlString(self, value_field):
        # Si es un string
        if isinstance(value_field, six.string_types):
            sql_string = "'" + value_field.strip().replace("'", "''") + "'"
        else:
            sql_string = str(value_field)

        return sql_string

    """
    Uso:
    sql=SqlConnection()
    sql.insert("match_player_data",["Name_Player","Num_Match","Ranking"],["Federer",10,1])
    """

    def insert(self, name_table, columns, values, verbose=False):
        command = "INSERT INTO " + name_table + "("
        for num_column, column in enumerate(columns):
            command += column
            if num_column < len(columns) - 1:
                command += ","
        command += ") VALUES ("
        for num_field, value_field in enumerate(values):

            command += self.convertValueToSqlString(value_field)
            if num_field < len(values) - 1:
                command += ","

        command += ");"
        try:
            self.cursor.execute(command)
            self.conn.commit()

        except Exception as e:
            print (e)


    """
    Uso:
    sql=SqlConnection()
    sql.select("SELECT Name_Player FROM match_player_data")
    """

    def select(self, command):
        rows = []

        try:
            self.cursor.execute(command)
            rows = self.cursor.fetchall()
        except Exception as e:
            # print (e)
            self.closeConnection()
            self.openSqlDataBaseConnection()
            rows = self.select(command)
        return rows

    def executeSelect(self, command):
        result_raw__select = self.select(command)
        select_dictionary = [dict(zip([key[0] for key in self.cursor.description], row)) for row in result_raw__select]
        return select_dictionary

    def update(self, command):
        self.execute(command)
        # self.closeConnection()

    def deleteAllRowsFromTable(self, name_table):
        command = "DELETE FROM " + name_table
        self.execute(command)
        # self.closeConnection()

    def openSqlDataBaseConnection(self):

        self.conn = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="",
          database="networkcomposite"
        )

        self.cursor = self.conn.cursor()
        # print(self.conn.is_connected())

    def __init__(self):
        correct_connection = False
        while not correct_connection:
            try:
                self.openSqlDataBaseConnection()
                correct_connection = True
            except Exception as e:
                print(str(e))
                time.sleep(1)

# sql = SqlConnection()
# sql.insert(table,[column1,column2],[text1,text2])

