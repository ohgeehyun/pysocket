import pymysql
import sys
import time
import serial
db = pymysql.connect(host="localhost",user="pi",passwd="1111",db="pot_db")
cur = db.cursor()
ser = serial.Serial("/dev/ttyUSB0",9600)
ser.readline()
while True:
    try:
        data = str(ser.readline())
        sql = "INSERT INTO plant values(%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),data.split('/')[0],data.split('/')[1],data.split('/')[2],data.split('/')[3],data.split('/')[4].strip()))
        db.commit()

    except KeyboardInterrupt:
        ser.close()
        db.close()
        break
            
