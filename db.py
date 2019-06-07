import pymysql
import sys
import time
import serial
import time
while True:
    try:
        db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
        cur = db.cursor()
        ser = serial.Serial("/dev/ttyUSB0",115200)
        ser.readline()
        data = str(ser.readline())
        sql = 'INSERT INTO plant values(%s,%s,%s,%s,%s)'
        cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),data.split('/')[1],data.split('/')[2],data.split('/')[3],data.split('/')[4].strip()))
        db.commit()
        time.sleep(1)
    except:
        ser.close()
        db.close()
