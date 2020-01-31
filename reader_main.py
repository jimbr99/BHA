import DB
from ctypes import *
import ctypes
import binascii
from time import sleep
from numpy import array
import ant

'''
epc_list: 2D list holding full raw input read 
data, which is 23 bytes in length. Twelve
rows of data are collected for further
screening of their crc values to detect and
remove duplicates.
epc_found_list: TODO
'''
global epc_list
global epc_found_list
global epc_output_list
global row
global end1
row = 0
n_detect = 12
m_detect = 23
n_output = 12
epc_list = [[i*j for j in range(m_detect)] for i in range(n_detect)]
epc_found_list = [[i*j for j in range(m_detect)] for i in range(n_detect)]
epc_output_list = [[i*j for j in range(m_detect)] for i in range(n_output)]
n_crc = 12
m_crc = 2
global epc_crc_nondup_list
epc_crc_nondup_list = [[i*j for j in range(m_crc)] for i in range(n_crc)]
'''
epc_dupcrc: 2D list holding input crc 2-byte
values, and which is 23 bytes in length. Twelve
rows screened with duplicates removed. A count
of seemingly unique epc rows is returned for
further filtering.
'''
global epc_crc_dup_list
global epc_row_count
epc_row_count = 0
n_crc = 12
m_crc = 2
epc_crc_dup_list = [[i*j for j in range(m_crc)] for i in range(n_crc)]

global nodups
nodups = [0]*12
global number_found
number_found = 0

#global ant_flg

def python_print_hex(di,Length):
    global epc_list
    global row
#    print("#=============================================================================")
    s = ""
    hexstr = ""
    
    if di == None:
        return 
    tt=0
    for i in di:
        s = '{:02X}'.format(int(i & 0xff))
        hexstr = hexstr + s + " "
        epc_list[row][tt] = s
        tt=tt+1
        if (tt == Length):
            break
    print(hexstr)
#    print("#===========================================================================")

CMD_GET_MODULE_INFO = [0xff,0x06,0x03,0x00,0x00]
CMD_TEST_RESET = [0xff,0x05,0x0F,0x00]
CMD_SET_READER_ENV_MODE = [0xff,0x06,0x14,0x00,0x00,0x42,0x30]
CMD_ANT_GET = [0xff,0x05,0x3F,0x01,0xA0, 0x29]
CMD_ANT = [0xff,0x0F,0x3F,0x00,0x01,0x01,0x00,0x00,0x00,0x01,0x0B,0xB8,0x00,0x14,0xD4,0x0F]
CMD_SINGLE_ID = [0xff,0x05,0xC8,0x00,0x3A,0x5E]
CMD_MULTI_ID = [0xff,0x08,0xC1,0x02,0x05,0x00,0xBC]

#global SendData1

def reader_cmd(cmd, SendData1):
#    global SendData1
    for i in range(len(cmd)):
        SendData1[i] = cmd[i]
        
def reader_cmd_setup(cmd, SendData1, SendData1_length):
#    global SendData1
    for i in range(len(cmd)):
        SendData1[i] = cmd[i]
    SendData1_length[0] = SendData1[1]-1
    
#    Response1=(b'\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00')
#    Response1_length[0]=0
#    Response1_length[1]=0


def reader_main():
    dll=cdll.LoadLibrary('/home/pi/BHA/libSYSIOT_RS232_Driver.so')
    PortString="/dev/ttyUSB0"
    PortBytes=bytes(PortString,encoding="utf8")   
    byte_Sarr300=ctypes.c_byte*37   #300
    byte_Rarr300=ctypes.c_byte*37
    int_arr2=ctypes.c_int*2
#======================================================================================
    SendData1=byte_Sarr300()
    Response1=bytearray(37)
    SendData1_length=int_arr2()
    Response1_length=int_arr2()
    global ant_flg
    
    #CMD_ANT_GET = [0xff,0x05,0x3F,0x01,0xA0, 0x29]
#    print("cmd CMD_ANT_GET")
    reader_cmd_setup(CMD_ANT_GET, SendData1, SendData1_length)
#    print(binascii.hexlify(SendData1))
    Response1=(b'\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00')
    resuilt=dll.SYSIOT_RS232_Python_ExeCution(PortBytes,SendData1_length,SendData1,Response1_length,Response1)
#    print("resuilt:", resuilt)
#    print(binascii.hexlify(Response1))

    
  #  print("cmd CMD_STOP_MULTI...")
    resuilt=dll.SYSIOT_RS232_Python_MultiTagReadStop(PortBytes)
#    print ("SYSIOT_RS232_Python_MultiTagReadStop resuilt:", resuilt) 
    
    #ant_file = open("/var/tmp/ant.txt", "r")
    ant_file = open("/home/pi/BHA/db_url.txt", "r")
    ant.ant_flg = ant_file.readline()
    print("ANTENNA FLAG = ", ant.ant_flg)
    
    # CMD_MULTI_ID = [0xff,0x08,0xC1,0x02,0x05,0x00,0xBC]
  #  print("cmd CMD_MULTI_ID")
    reader_cmd_setup(CMD_MULTI_ID, SendData1, SendData1_length)
    resuilt=dll.SYSIOT_RS232_Python_MultiTagReadStart(PortBytes,SendData1_length,SendData1)
#    print("SYSIOT_RS232_Python_MultiTagReadStart resuilt:", resuilt)
    
    n=1
    global row
    row = 0
    print("read tags")
    while n<=12:
        Response=bytearray(300)
        Response=(b'\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x00')
        Response_length=int_arr2()
        Response_length[0]=0
        Response_length[1]=0

        resuilt=dll.SYSIOT_RS232_Python_MultiTagGetData(PortBytes,Response_length,Response)
#        print("SYSIOT_RS232_Python_MultiTagGetData resuilt:", resuilt)
     #   print("Response_length:", Response_length[0])
     #   print("Response:" , Response)
#        print("Response:")

        if (Response_length[0] > 0) :
                python_print_hex(Response,Response_length[0])
        n=n+1
        row=row+1
        sleep(0.1)
    
   # sleep(0.1)
   # print("cmd CMD_STOP_MULTI")
    resuilt=dll.SYSIOT_RS232_Python_MultiTagReadStop(PortBytes)
    #print(resuilt, end= ' ')
    sleep(0.1)
    resuilt=dll.SYSIOT_RS232_Python_MultiTagReadStop(PortBytes)
#    print ("SYSIOT_RS232_Python_MultiTagReadStop resuilt:", resuilt)
#    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
    return 0

'''
Scan received tag list crc values for duplicate tag entries
by storing data in epc_crc_nondup_list, the non-duplicate list,
only if input crc is not already in that same list list.
'''
def check_dup_crc():
    global epc_crc_dup_list
    global epc_crc_nondup_list
    global end1
    global number_found
    # clear nondup list
    for j in range(12):
        nodups[j] = 0
        for i in range(2):
            epc_crc_nondup_list[j][i] = 0
        #    epc_crc_nondup_list[j][1] = 0
    
    end1=1
    a=end1
    k = 0
    for j in range(12):   
        for i in range(end1):
            a = end1
            if((epc_list[j][1:3]==['FF', 'FF']) or (epc_list[j][1:3]==['AA', 'AA'])):
                print('filtered')
                break
            if((epc_crc_nondup_list[i][0] == epc_crc_dup_list[j][0]) and (epc_crc_nondup_list[i][1] == epc_crc_dup_list[j][1])):
                print('repeat %s %s %d %d %d' %(epc_crc_dup_list[j][0], epc_crc_dup_list[j][1], j, a-1, i ))
                #print('k=%d %s %s' %(k,(epc_crc_nondup_list[i][0]), (epc_crc_nondup_list[i][1]) ))
                k += 1
                break
            else:
                if (i == a-1):
                    epc_crc_nondup_list[a-1][0] = epc_crc_dup_list[j][0]
                    epc_crc_nondup_list[a-1][1] = epc_crc_dup_list[j][1]
                    
                    print('capture %s %s %d %d %d' %((epc_crc_nondup_list[i][0]), (epc_crc_nondup_list[i][1]), j, a-1, i )) #, end = ' ')
                    n=a-1
                    #epc_found(i,j)
                    nodups[i] = j
                    end1 += 1
    print(nodups)
    number_found = end1-1
    print('found=%d' %(number_found))
    
    
    

def epc_found(n,j):
    global epc_list
    global epc_found_list
    for f in range(n):       
        epc_found_list[f][0] = 'W' #epc_list[j][0]
        epc_found_list[f][1] = 'x' #epc_list[j][1]    
    #print(epc_found_list)

    pass

def reader_process_rx():
    global epc_list
    global epc_crc_dup_list
    global epc_crc_nondup_list
    global epc_found_list
    global epc_output_list
    global number_found
    
    print('')
    print('Read data detect buffer...')
    # extraction of epc values
    for k in range(12):
        # bogus crc; fill epc with 0xFF
        if epc_list[k][20:20+2]==['6E', '09']:
            for q in range(23):
                epc_list[k][q] = 'FF'
        # check for timeout
        if epc_list[k][4] == '15':
            print('timeout')
            for q in range(23):
                epc_list[k][q] = 'AA'
            
        for p in range(23):
            #if p==20 and epc_list[k][p:p+2]==['6E', '09']:
            #    print('p=%s ' %(epc_list[k][p:p+2]))
            print(epc_list[k][p], end = ' ')
        print('')   
    print('Get list of crc values.')
    # extraction of crc values
    for k in range(12):
        for p in range(2):
            print(epc_list[k][p+20], end = ' ')
            epc_crc_dup_list[k][p] = epc_list[k][p+20]
    print('')
    
    print('Remove duplicate CRCs.')
    check_dup_crc()
    
    print('List non duplicate CRCs.')
    for k in range(12):
        for p in range(2):
            #epc_crc_dup_list[k][p] = epc_list[k][p+20]
            print(epc_crc_nondup_list[k][p], end = ' ')
    print(' ')
    print('Generate epc found list')
    for k in range(number_found):
        i = 0
        for p in range(23):
            j = nodups[k]
            epc_found_list[k][p] = epc_list[j][p]
            print(epc_found_list[k][p], end = ' ')
        i += 1            
        print('')  
 
    print('\n\n')
    # extraction of epc values
    print("Extract epc values")
    for k in range(number_found):
        for p in range(12):
            #print(epc_list[k][p+8], end = ' ')
            epc_output_list[k][p] = epc_found_list[k][p+8]
            print(epc_output_list[k][p], end = '')
        print('') #'%d' %(k))             
    print('\n\n')
    print('Verify DB Buffer. Remove duplicate epc...')
    print('Transfer to Database...')
    
    for j in range(12):
        for k in range(12):
            DB.db_output_list[j][k] = epc_output_list[j][k]
            
    DB.db()
    
#if __name__ == '__main__':
#    main()

