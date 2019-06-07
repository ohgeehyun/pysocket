import pymysql
import sys
import time
import serial

db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
cur = db.cursor()
sql = 'update current set value = %s'
cur.execute(sql,'8')
db.close()
ser = serial.Serial("/dev/ttyUSB0",115200)
ser.readline()
ser.readline()
ser.readline()
while True:
    db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
    cur = db.cursor()
    sql = 'INSERT INTO plant values(%s,%s,%s,%s,%s)'
    data = str(ser.readline())
    print(data)
    cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),data.split('/')[1],data.split('/')[2],data.split('/')[3],data.split('/')[4].strip()))
    db.commit()
    sql = 'select * from value ORDER BY date DESC limit 1'
    cur.execute(sql)
    data1 = cur.fetchone()
    lightHigh = float(data1[1])
    lightLow = float(data1[2])
    dust_v = float(data1[3])
    moisture_v = float(data1[4])
    tempHigh = float(data1[5])
    tempLow = float(data1[6])

    temporature = float(data.split('/')[1])
    moisture = float(data.split('/')[2])
    light = float(data.split('/')[3])
    dust = float(data.split('/')[4])

    error = 0
    now = 7
    print(moisture)
    print(moisture_v)

    if light != None:
        if light > lightHigh:
            error += 1
            now = 3
            print('lightHigh')
        elif light < lightLow:
            error += 1
            now = 1
            print('lightLow')
    if dust > dust_v:
        error += 1
        now = 6
        print('dusterror')
    if moisture > moisture_v:
        error += 1
        now = 2
        print('moistureerror')
    if temporature != None:
        if temporature > tempHigh:
            error += 1
            now = 5
            print('tempHigh')
        elif temporature < tempLow:
            error += 1
            now = 4
            print('tempLow')
        
    print(error)
    if error >= 2:
        now = 0

    print(now)
    sql = 'select value from current'
    cur.execute(sql)
    current = cur.fetchone()

    if now != int(current[0]):
        if now == 0:
            ser.writelines("a")
        elif now ==1:
            ser.writelines("b")
        elif now ==2:
            ser.writelines("c")
        elif now == 3:
            ser.writelines("d")
        elif now == 4:
            ser.writelines("e")
        elif now == 5:
            ser.writelines("f")
        elif now == 6:
            ser.writelines("g")
        elif now == 7:
            ser.writelines("h")

        sql = 'update current set value = %s'
        now = str(now)
        cur.execute(sql,now)
        ser.readline()
        ser.readline()
        db.commit()
        db.close()
        
