import socket
import pymysql
import threading
import time
import serial
while True:
    try:
        host = '192.168.1.21'
        port = 4444
        su = socket.socket(socket.AF_INET)
        su.bind((host,port))
        su.listen(1)
        connect,address = su.accept()
        print('Connected by',address)

        def send():
            while True:
                db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
                cur = db.cursor()
                sql = 'SELECT light,dust,moisture,temporature FROM plant ORDER BY date DESC limit 1'
                cur.execute(sql)
                data = cur.fetchone()
                connect.send('ok'+'/'+data[0]+'/'+data[1]+'/'+data[2]+'/'+data[3]+'/')
                print(data)
                time.sleep(2)
                db.close()
            connect.close()
    
        def recv():
            while True:
                data =connect.recv(1024)
                if not data:
                    continue
                elif data.split('/')[0] =='save':
                    print(data)
                    db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
                    cur = db.cursor()
                    sql = 'INSERT INTO value values(%s,%s,%s,%s,%s,%s,%s)'
                    cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),data.split('/')[1],data.split('/')[2],data.split('/')[3],data.split('/')[4],data.split('/')[5],data.split('/')[6]))
                    db.commit()
                    db.close()
            connect.close()
            su.close()
    
        threading._start_new_thread(send,())
        threading._start_new_thread(recv,())


    except:
        pass
