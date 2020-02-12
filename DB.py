import mysql.connector
from mysql.connector import errorcode
import reader_main
import RPi.GPIO as GPIO
import ant
import time
from time import sleep

db_output_list = [[i*j for j in range(12)] for i in range(12)]
global text_file
text_file = 0
GPIO.setmode(GPIO.BCM)

#global ant_flag

global DB_URL 
DB_URL = '0.0.0.0'

def db():
    #global ant_flg
    global DB_URL
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    found_list = []
    names_unchecked = []
    
    file = open("/home/pi/BHA/db_url.txt", "r")
    DB_URL = file.readline()
    print('Using DB_URL ', DB_URL)
    file.close()
    
    s = ''
    print('Starting DB...')
    print("ANTENNA FLAG", ant.ant_flg)
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
      
      print ("Selecting columns:")
      selallcol = ("SELECT epc FROM pid")
      cursor.execute(selallcol)
      for (selallcol) in cursor:
#          print (selallcol[0])
          pass
#      print ("")
      
      a=reader_main.number_found
      print('number_found=', a)
      print('')
      
      
      global text_file
      text_file = open("/var/tmp/tp.txt", "w")
      '''
      out0 = "SELECT reg FROM epc WHERE name='Emnir Karamehmedovic'"
      print(out0)
      selonecol = (out0)
      cursor.execute(selonecol)
      for (selonecol) in cursor:
          print(">>>", selonecol)
      '''
      for i in range(a):
          buf="'"
          # piece together single epc bytes into string
          for j in range(12):
              # db_output_list[][] is populated
              # in reader_main.reader_process_rx()
              buf += "%s" % (db_output_list[i][j])
#              print(db_output_list[i][j])
          buf += "'"
          out = "SELECT name, msg, reg FROM pid WHERE epc=" + buf
#          print(out)
          #buf =''
 
          selonecol = (out)
          #print(selonecol)
          try:
              cursor.execute(selonecol)
              #print(cursor.description)
              #print(cursor[0])
              #print (selonecol[0], end=" ") #, ' %d' %(x))
              #print (selonecol[1], end=" ")
              #print (selonecol[2])
              #print(cursor)
              #if("MySQLCursor:" in cursor):
                  #pass
              for (selonecol) in cursor:
                  x=len(selonecol[0])
                  #print(x)
                  print (selonecol[0], end=" ") #, ' %d' %(x))
                  print (selonecol[1], end=" ")
                  print (selonecol[2], end=" ")
                  print(len(selonecol[2]))
                  if selonecol[0] != '':
                      if ant.ant_flg == 0:
                          # check the reg column response (contains Yes or No)
                          if selonecol[2] == "Yes":
                              s =  "%s\r\n" % (selonecol[0]+ ": " + selonecol[1]+ ". ")
                          else:
                              names_unchecked.append(selonecol[0])
                              '''
                              y = "".join(map(str,selonecol[0]))
                              z = "'" + y + "'"
                              sel = "epc SET reg='Yes' WHERE name="+ z                            
                              print(sel)
                              
                              cursor.execute(sel)
                              for (sel) in cursor:
                                  print (sel[0])
                              '''    
                              s =  "%s\r\n" % (selonecol[0]+ ": " + "Is now checked in.")
                      else:
                          if selonecol[2] == "Yes":
                              s =  "%s\r\n" % (selonecol[0]+ ": " + selonecol[1]+ ". ")
                          else:
                              s =  "%s\r\n" % (selonecol[0]+ ": " + "Has not checked in.")
                  else:
                      s = '* * * * * * * *\r\n'
#              print ("")
          except:
              print('Exception...')
          else:
              pass
            
          found_list.append(s)
          #text_file.write("This is DB name %d\r\n" % (i))
          # Write received names to file
          #text_file.write(s)
          s = ''
          buf = ''
      
      
      # write appended sorted list
      found_list.sort()
      text_file.write(''.join(map(str,found_list)))
      
      #print(names_unchecked)
      print("")
      #print(names_unchecked)
      for n in range(0, len(names_unchecked)):
          #print(n)
          y = "".join(map(str,names_unchecked[n]))
          z = "'" + y + "'"
          sel = "UPDATE pid SET reg='Yes' WHERE name="+ z                            
          print(sel)
          
          cursor.execute(sel)
          for (sel) in cursor:
              print("W")
              print (sel[0], end=" ") #, ' %d' %(x))
              print (sel[1], end=" ")
              print (sel[2])                            
                           
      #print(names_unchecked)         
      '''
      This GPIO operation generates an interrupt for the Flask server,
      which responds with callback to read the file for display.
      '''
      GPIO.output(4, GPIO.HIGH)
      GPIO.setup(4, GPIO.IN)    
      text_file.close()
       
    cnx.close()
    
    print("")
    print(found_list)
