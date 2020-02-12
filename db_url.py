#!/usr/bin/python3

global url

def get_url():

    file = open("/home/pi/BHA/db_url.txt", "r")
    var = file.readline()
    print("Current db_url = %s" %var)
    file.close()

    var = input("Enter database URL: ")
    if var == "":
        pass
    else:
        url = open("/home/pi/BHA/db_url.txt", "w")
        url.write(var)
        url.close()
    
    file = open("/home/pi/BHA/db_url.txt", "r")
    var = file.readline()
    print(var)
    file.close()

if __name__=="__main__":
    get_url()