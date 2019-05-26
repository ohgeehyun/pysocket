import socket
import pymysql
import threading
host = '192.168.0.5'
port = 4444
su = socket.socket(socket.AF_INET)
su.bind((host,port))
su.listen(1)
connect,address = su.accept()
print('Connected by',address)

def send():
    db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
    cur = db.cursor()
    sql = 'SELECT light,dust,moisture,temporature FROM plant ORDER BY date DESC limit 1'
    cur.execute(sql)
    data = cur.fetchone()
    connect.send('ok'+'/'+data[0]+'/'+data[1]+'/'+data[2]+'/'+data[3])
    db.close()
    
def recv():
    data = connect.recv(1024)
    if not data:
        pass
    elif data.split('/')[0] =='save':
        print(data)
        db = pymysql.connect(host='localhost',user='pi',passwd='1111',db='pot_db')
        cur = db.cursor()
        sql = 'INSERT INTO value values(%s,%s,%s,%s,%s,%s)'
        cur.execute(sql,data.split('/')[1],data.split('/')[2],data.spllit('/')[3],data.split('/')[4],data.split('/')[5],data.split('/')[6])
        db.commit()
        db.close()
    
threading._start_new_thread(send,())
threading._start_new_thread(recv,())

connect.close()
su.close()


 
