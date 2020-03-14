from socket import *
import sys
import getpass
from hashlib import sha1


def do_login(s):
    n = 0
    while True:
        name = input('请输入姓名：')
        password = getpass.getpass('请输入密码：')
        s1 = sha1()
        password = s1.hexdigest()
        seq = 'D'+' '+ name +' '+password
        s.send(seq.encode())
        data = s.recv(1024)
        
        if data.decode() == 'DOK':
            print('登录成功')
            search(s,name)
            return
        elif n >2:
            return
        else:
            print('用户名或密码错误，请重新输入')
            n +=1
            continue


def search(s,name):
    while True:
        print('''
            ==========查询界面===============
            --1.查词  2.查历史记录 3.退出-- 
            ================================
            ''')  
        try:
            cmd = int(input('输入选项:'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1,2,3]:
            print('请输入正确命令')
        elif cmd == 1:
            search_words(s,name)
        elif cmd == 2:
            search_records(s,name)
        elif cmd == 3:
            quit(s,name)
            return

def quit(s,name):
    msg = 'Q' + ' ' + name
    s.send(msg.encode())
    return


def search_records(s,name):
    msg = 'H' + ' ' + name
    s.send(msg.encode())
    data = s.recv(1024).decode()

    if data == '^^':
        print('此用户还未查询单词')
    else:
        print(data)

def search_words(s,name):
    while True:
        try:
            word = input('请输入你要查找的单词,退出输入$$：')
            if word == '$$':
                return
        except Exception as e:
            print(e)
            continue
        msg = 'W' + ' ' + name + ' ' + word
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == '##':
            print('没有此单词，请重新输入')
        else:
            print(data)
        

def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket(AF_INET,SOCK_STREAM)

    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    while True:
        print('''
            ==========Welcome===========
            ---1.注册   2.登录    3.退出--
            ============================
            ''')
        try:
            cmd = int(input('输入选项:'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1,2,3]:
            print('请输入正确命令！')
            sys.stdin.flush()
            continue

        elif cmd == 1:
            
            do_register(s)
            
        elif cmd == 2:
            
            p = do_login(s)
        elif cmd == 3:
            s.close()
            sys.exit('谢谢使用')




def do_register(s):
    while True:
        name = str(input('输入用户名：'))
        
        password = getpass.getpass('输入密码：')
        password1 = getpass.getpass('请再次输入密码：')
        if (' ' in name) or (' ' in password):
            print('用户名和密码不能有空格')
            continue
        if password != password1:
            print('密码输入不一致，请重新输入')
            continue
        
        #msg = 'R' + ' '+ name +' ' + password
        s1 = sha1()
        password = s1.hexdigest()
        msg = 'R {} {}'.format(name,password)
        s.send(msg.encode())
        data = s.recv(1024)
        if data.decode() == 'ROK':
            print('注册成功')
            search(s,name)
            return
        elif data.decode() == 'RNG':
            print('用户名已存在')
            continue
        else:
            return



if __name__ == '__main__':
    main()