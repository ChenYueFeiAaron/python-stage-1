#!/usr/bin/env python3
#coding=utf-8
'''
name:aaron
email:...
data:2020-3-6
description:dictionary
env: python3.5
'''
from socket import *
import os,sys
import time
import pymysql
import re

def login_thing(c,db,dldata):
    d = dldata.split(' ')
    name = d[1]
    password = d[2]
    sql = 'select * from user where \
    name = "%s" and password = "%s"'%(name,password)
    cursor = db.cursor()
    cursor.execute(sql)
    p = cursor.fetchone()
    print(p)
    if p == None:
        c.send(b'DNG')
        print('登录失败')
        return
    else:
        
        c.send(b'DOK')
    '''sql = 'insert into login_rec (name,time) values \
            ("%s","%s")'%(name,time.ctime())
    try:

        cursor.execute(sql)
        db.commit()
        print('记录成功')
    except Exception as e:
        print(e)
        db.rollback()
        return
    '''
        



def regist_thing(c,db,dldata):
    d = dldata.split(' ')
    name = d[1]
    print(name)
    password = d[2]
    sql = 'select * from user where name = "%s"'%name
    cursor = db.cursor()
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        c.send(b'RNG')
        return
    sql = 'insert into user (name,password) values\
                        ("%s","%s")'%(name,password)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'ROK')
    except:
        db.rollback()
        c.send(b'fail')
    else:
        print('%s注册成功'%name)   
    
def search_word(c,db,dldata):
    d = dldata.split(' ')
    word = d[2]
    name = d[1]
    cur = db.cursor()
    def insert_word():
        tm = time.ctime()
        sql = 'insert into history (name,word,time) values \
                ("%s","%s","%s")'%(name,word,tm)
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

    try:
        f = open('dict.txt')
    except:
        print('打开文件失败')
        c.send(b'##')
        return
    while True:
        for file in f:
            s = re.findall(r'\S+',file)
            wordkey = s[0]
            if wordkey == word:
                c.send(file.encode())
                f.close()
                insert_word()
                return
        else:
            print('没有此单词')
            c.send(b'##')
            break
    f.close()
    '''##数据库查询
    sql = 'select discription from words where word = "%s"'%word
    cur.execute(sql)
    disc = cur.fetchone()
    print('name is',name)
    if disc != None:
        sql = 'insert into history (name,word,time) values\
                ("%s","%s","%s")'%(name,word,time.ctime())
        try:
            cur.execute(sql)
            db.commit()
            c.send(disc[0].encode())
        except Exception as e:
            print(e)
            db.rollback()
            return
        else:
            print('查询完毕')
    else:
        c.send(b'##')
        '''

def search_his(c,db,dldata):
    h = dldata.split(' ')
    name = h[1]
    dd=''
    cur = db.cursor()
    sql = 'select word,time from history where name = "%s"'%name
    cur.execute(sql)
    dh = cur.fetchall()
    for i in dh:
        dd +=i[0] + ':' + i[1] + '\n'
    
    if not dd:
        c.send(b'^^')
    else:
        c.send(dd.encode())
def login_out(c,dldata):
    l = dldata.split(' ')
    name = l[1]   
    print('%s已经退出'%name) 

def client_handler(c,db):
    while True:
        data = c.recv(1024).decode()
    #    print(data)
        if not data:
            break
        RequestType = data.split(' ')
        if data[0] == 'Q':
            login_out(c,data)
        elif RequestType[0] == 'R':
            regist_thing(c,db,data)
        elif RequestType[0] == 'D':
            login_thing(c,db,data)
        elif RequestType[0] == 'W':
            search_word(c,db,data)
        elif RequestType[0] == 'H':
            search_his(c,db,data)


    c.close()
    sys.exit(0)


def main():
    db = pymysql.connect(host='localhost',
                         user = 'root',
                         password = '123456',
                         database = 'dict',
                         port = 3306)

    ADDR = ('0.0.0.0',8888)
    s = socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(10)

    while True:
        try:

            c,addr = s.accept()
            print('来至%s的链接'%str(addr))
        except KeyboardInterrupt:
            sys.exit('服务器退出')

        pid = os.fork()
        if pid <0:
            print('create process failed')
        elif pid == 0:
            s.close()
            client_handler(c,db)
        else:
            c.close()
            continue


if __name__ == '__main__':
    main()
