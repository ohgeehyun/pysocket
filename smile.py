import pymysql
import serial
import time
while True:
    ser = serial.Serial("/dev/ttyUSB0",115200)

    error = 0

    db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
    cur = db.cursor()
    sql = 'select * from value ORDER BY data DESC limit 1'
    sql2 = 'select value from current'
    cur.execute(sql)
    data = cur.fetchone()
    lightHigh = int(data[1])
    lightLow = int(data[2])
    dust_v = float(data[3])
    moisture_v = int(data[4])
    tempHigh = int(data[5])
    tempLow = int(data[6])

    sql1 = 'select * from plant ORDER BY date DESC limit 1'
    cur.execute(sql1)
    data1 = cur.fetchone()
    dust = float(data1[1])
    light = int(data1[3])
    moisture = int(data1[2])
    temporature = int(data1[5])


    if light != None:
        if light > lightHigh:
            error +=1
            print('lightHigh')
        elif light < lightLow:
            error +=1
            print('lightLow')
    if dust_v < dust:
        error +=1
        print('dusterror')
    if moisture > moisture_v:
        error +=1
        print('moistureerror')
    if temporature != None:
        if temporature > tempHigh:
            error +=1
            print('tempHigh')
        elif temporature < tempLow:
            error +=1
            print('tempLow')
    print(error)

    if error >=2:
        now = 0
    elif light < lightLow:
        now = 1
    elif moisture >= moisture_v:
        now = 2
    elif light > lightHigh:
        now = 3
    elif temporature <= tempLow:
        now = 4
    elif temporature >= tempHigh:
        now = 5
    elif dust >= dust_v:
        now = 6
    else:
        now = 7
    cur.execute(sql2)
    current = cur.fetchone()



    if now == 0:
        ser.writelines("a")    
    elif now == 1:
        ser.writelines("b")
    elif now == 2:
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
    print(now)
    sql3 = 'update current set value = %s'
    cur.execute(sql3,now)
    db.commit()
    db.close()
    ser.close()
    time.sleep(3)

