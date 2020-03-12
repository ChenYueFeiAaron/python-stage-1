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
import pymongo
import re

def login_thing(c,db,dldata):
    d = dldata.split(' ')
    name = d[1]
    password = d[2]
    myset = db.user
    
    p = myset.find_one({'name':name,'password':password})
    
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
    myset = db.user
    
    r = myset.find_one({'name':name,'password':password})
    print(r)
    
    if r != None:
        c.send(b'RNG')
        return
    sql = [{'name':name,'password':password}]
    try:
        myset.insert(sql)
        c.send(b'ROK')
    except:
        
        c.send(b'fail')
    else:
        print('%s注册成功'%name)   
    
def search_word(c,db,dldata):
    d = dldata.split(' ')
    word = d[2]
    name = d[1]
    myset = db.words

    
    res = myset.find_one({'name':word},{'_id':0,'name':0})
    
    
    

    if res != None:
        sql = [{'name':name,'word':word,'time':time.ctime()}]
        disc = res['description']
        try:
            myset1 = db.history
            myset1.insert(sql)
            
            c.send(disc.encode())

        except Exception as e:
            print(e)
            
            return
        else:
            print('查询完毕')
    else:
        c.send(b'##')
        

def search_his(c,db,dldata):
    h = dldata.split(' ')
    name = h[1]
    dd=''
    myset = db.history
    dh = myset.find_one({'name':name},{'_id':0})
    if dh == None:
        c.send(b'^^')
        print('无记录')
    else:
        dh = myset.find({'name':name},{'_id':0})
        for i in dh:
            dd = '%s : %s"\n"'%(i['word'],i['time'])
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
    conn = pymongo.MongoClient('localhost',27017,connect = False)
    

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
            conn.close()
            sys.exit('服务器退出')

        pid = os.fork()
        if pid <0:
            print('create process failed')
        elif pid == 0:
            s.close()
            db = conn.dict
            client_handler(c,db)
        else:
            c.close()
            continue


if __name__ == '__main__':
    main()
