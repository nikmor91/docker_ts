# -*- coding: UTF-8 -*-
from os import path, listdir
from time import ctime
import pymysql
import time
import array
from numpy import array_equal 

def zp_db(cursor):
  
    try: cursor.execute('CREATE TABLE IF NOT EXISTS resul (equip_id int(5) NOT NULL AUTO_INCREMENT, file_name varchar(100) DEFAULT NULL,status varchar(100) DEFAULT NULL, PRIMARY KEY(equip_id))')
    except pymysql.Error: print('Cant CREATE')

def db_select(cursor):
   
    try: cursor.execute('SELECT * FROM resul WHERE status = "created"')
    except pymysql.Error: print('Cant SELECT')

    rows = [ item for item in cursor.fetchall() ]
    return rows

def db_insert(cursor, data):
        
    try: cursor.execute("INSERT into resul (file_name, status) values (%s, %s)", (data[0], data[1])) 
    except pymysql.Error: print('Cant INSERT')
       
def db_update(cursor, data):
            
    try: cursor.execute("UPDATE resul SET status = %s WHERE equip_id = %s", (data[1], data[0])) 
    except pymysql.Error: print('Cant INSERT')
        
def scan_dir():
    folder = '/var/docker_tz'
    param = []
    for name in listdir(folder):
        full_name = path.join(folder, name)
        if path.isfile(full_name):
            namef, _ext = path.splitext(name)
            time_info = [ctime(fn(full_name)) for fn in (path.getatime, path.getmtime, path.getctime)]
            file = {
               # 'directory': folder,
                #'file': full_name,
                'file_name': namef,
                'last_change_time': time_info[1],
            }
            param.append(namef)
    return param


def main():
    a = 1
    while a < 10:
        time.sleep(60)
        try: db = pymysql.connect('10.6.42.6', 'root', 'q1w2e3!', 'dbscan')
        except pymysql.OperationalError: print('Unknown base name')

        try: cursor = db.cursor()
        except pymysql.Error: print('Cant get cursor')

        zp_db(cursor)
        files = scan_dir()
        files_db = db_select(cursor)
        for file in files:
            if not(next((True for item in files_db if file in item), False)):
                db_insert(cursor, (file, 'created'))
                db.commit()
        for file in files_db:
            if not(next((True for item in files if item in file), False)):
                db_update(cursor, (file[0], 'deleted'))
                db.commit()
        cursor.close()
        db.close()
        time.sleep(60)

if __name__ == '__main__':
    main()
