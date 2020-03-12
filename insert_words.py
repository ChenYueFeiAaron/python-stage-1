import pymongo

conn = pymongo.MongoClient('localhost',27017)

db = conn.dict

myset = db.words
FILE = 'dict.txt'

try:
    f = open(FILE)
except:
    print('打开文件失败')
word = ''
desc = ''
for fd in f:
    tem = fd.split(' ')
    word = tem[0]
    desc = ' '.join(tem[1:])
    myset.insert({'name':word,'description':desc})

conn.close()
print('导入完成')