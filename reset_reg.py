#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode

def main():
    
    file = open("/home/pi/BHA/db_url.txt", "r")
    DB_URL = file.readline()
    print('Using DB_URL ', DB_URL)
    file.close()
    
    print("Reseting column reg")
    try:
      cnx = mysql.connector.connect(user='pi', password='rp3',
                                host= DB_URL, #'192.168.0.154                                                                                                                                                                                                                                                                                                                                                                                                                                                                             ',
                                database='epc1',
                                autocommit=True)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
      cursor = cnx.cursor();
      
      print ("Using epc1 database:") 
      dbname = ("USE epc1")
      cursor.execute(dbname)
      for (dbname) in cursor:
          print (dbname) 
      print ("")
      
      sel = "UPDATE pid SET reg='No' "                            
      print(sel)
          
      cursor.execute(sel)
    cnx.close()

if __name__=="__main__":
    main()
    