import pymysql
import re

class Mysqlpython():
    def __init__(self,database,
                  host = 'localhost',
                  user = 'root',
                  password = '123456',
                  port = 3306,
                  charset = 'utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        self.database = database

    def open(self):
        self.db = pymysql.connect(host=self.host,
                                  user=self.user,
                                  port=self.port,
                                  database=self.database,
                                  password = self.password,
                                  charset=self.charset)
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def zhixing(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            self.db.commit()

        except Exception as e:
            print('failed',e)
        self.close()

def upload_data(database):
    cc = Mysqlpython(database)

    f = open('dict.txt')
    id_d = 0
    while True:
        word = ''
        description = ''
        data = ''
        data = f.readline()
        if not data:
            break
        #print(data)
        
        
        try:
#            word = re.match(r'\S+',data).group()
            l = re.split(r'   +',data)
            word = l[0]
            description = ' '.join(l[1:])
        except (IndexError,AttributeError):
            continue
            
        print(description)


        sql = 'insert into words values(%s,%s,%s)'
        cc.zhixing(sql,[id_d,word,description])
        id_d +=1
        print(id_d)

if __name__ == '__main__':
    upload_data('dict')
